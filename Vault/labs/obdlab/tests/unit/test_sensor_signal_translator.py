"""End-to-end tests for SensorSignalTranslator per T-P0-8.

Covers:
  - HIGH-confidence DNA + warm steady idle → full payload
  - dna_view=None + same input → defaults (DUAL_MAF_MAP + NARROWBAND O2)
  - Cold input (ECT < 75) → bucket override + analytics frozen + payload emitted
  - Bank-2 fields present → 2-bank payload
  - Out-of-range input → PIDValidationError propagates
"""

import pytest

from obdlab.core.exceptions import PIDValidationError
from obdlab.core.sensor_signal_translator import SensorSignalTranslator
from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)
from obdlab.schemas.payload import OBDLivePayload
from obdlab.schemas.vocabulary import (
    FuelSystemStatus,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    RpmStateBucket,
    TrimAnalyticsGate,
    VEValidity,
)

# ── helpers ────────────────────────────────────────────────────────────

def _dna_high() -> ObdLabDnaView:
    """Return a HIGH-confidence ObdLabDnaView for a typical NA 2.0L."""
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )


def _warm_idle_input(**overrides):
    """Return a raw user input dict for warm steady idle."""
    base = {
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 35.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "pid_oxygen_sensor_volts": 0.45,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    base.update(overrides)
    return base


@pytest.fixture
def translator():
    return SensorSignalTranslator()


# ── end-to-end — HIGH-confidence DNA ───────────────────────────────────

def test_warm_idle_high_dna(translator):
    """Warm steady idle + HIGH confidence DNA → full payload."""
    payload = translator.translate(_warm_idle_input(), _dna_high())

    assert isinstance(payload, OBDLivePayload)
    assert payload.engine_warmed is True
    assert payload.rpm_state_bucket == RpmStateBucket.STABILIZED_IDLE
    assert payload.engine_rpm == 800
    assert payload.coolant_temp_c == 92.0
    assert payload.calculated_engine_load_pct == 22.0
    assert payload.mass_airflow_gps == 3.5
    assert payload.manifold_vacuum_kpa == 30.0
    assert payload.shrtft1 == -3.0
    assert payload.longft1 == -5.0
    assert payload.shrtft2 is None  # bank-2 null contract
    assert payload.longft2 is None
    # VE should be valid for this healthy setup
    assert payload.ve_validity == VEValidity.VALID
    assert payload.ve_pct >= 0.0
    assert payload.maf_status == NodeMAFStatus.REAL_SENSOR_FEED
    assert payload.map_status == NodeMAPStatus.REAL_SENSOR_FEED
    # Analytics gate should be VALID for healthy warm idle
    assert payload.trim_analytics_gate == TrimAnalyticsGate.VALID
    # O2 failure should be NO_FAULT for healthy sensor
    assert payload.o2_failure_mode == O2FailureMode.NO_FAULT
    # Fuel system status should be CL
    assert payload.fuel_system_status == FuelSystemStatus.CL
    # Lambda should be ~stoich (narrowband 0.45 V)
    assert 0.7 <= payload.normalized_obd_lambda <= 1.3
    # TFT should be shrtft1 + longft1
    assert payload.total_trim_correction_delta == pytest.approx(-8.0)
    assert payload.freeze_frame_pids == {}


def test_round_trip_json(translator):
    """Payload model_dump_json round-trips cleanly."""
    payload = translator.translate(_warm_idle_input(), _dna_high())
    json_str = payload.model_dump_json()
    reloaded = OBDLivePayload.model_validate_json(json_str)
    assert reloaded == payload


# ── dna_view=None — defaults ───────────────────────────────────────────

def test_null_dna_still_emits_payload(translator):
    """dna_view=None: pipeline uses DUAL_MAF_MAP + NARROWBAND defaults."""
    payload = translator.translate(_warm_idle_input(), dna_view=None)

    assert isinstance(payload, OBDLivePayload)
    assert payload.engine_warmed is True
    assert payload.rpm_state_bucket == RpmStateBucket.STABILIZED_IDLE
    # VE returns UNKNOWN without displacement (dna_view=None)
    assert payload.ve_validity == VEValidity.UNKNOWN
    # Lambda normalized (narrowband 0.45 V)
    assert payload.normalized_obd_lambda == pytest.approx(1.0)
    # O2 failure mode is NO_FAULT for healthy narrowband
    assert payload.o2_failure_mode == O2FailureMode.NO_FAULT
    # Fuel system status should be CL
    assert payload.fuel_system_status == FuelSystemStatus.CL


def test_null_dna_narrowband_o2_default(translator):
    """dna_view=None → narrowband O2 path (pid_oxygen_sensor_volts used)."""
    inp = _warm_idle_input(pid_oxygen_sensor_volts=0.15)
    payload = translator.translate(inp, dna_view=None)
    # 0.15 V → LEAN zone → lambda 1.05
    assert payload.normalized_obd_lambda == pytest.approx(1.05)


# ── cold engine ────────────────────────────────────────────────────────

def test_cold_engine_bucket_override(translator):
    """ECT < 75 → COLD_OPEN_LOOP_INVALID, analytics frozen, payload emitted."""
    inp = _warm_idle_input(coolant_temp_c=40.0)
    payload = translator.translate(inp, _dna_high())

    assert payload.engine_warmed is False
    assert payload.rpm_state_bucket == RpmStateBucket.COLD_OPEN_LOOP_INVALID
    # Analytics frozen
    assert payload.normalized_obd_lambda == pytest.approx(1.0)  # stoich default
    assert payload.total_trim_correction_delta == 0.0
    assert payload.ve_validity == VEValidity.UNKNOWN
    assert payload.ve_pct == 0.0  # wiki: §10 — 0.0 sentinel when analytics frozen
    assert payload.o2_failure_mode == O2FailureMode.NO_FAULT
    # Payload still emitted with engine RPM etc.
    assert payload.engine_rpm == 800
    assert payload.coolant_temp_c == 40.0


def test_cold_engine_ect_74_degrees(translator):
    """ECT = 74.0 (just below 75 threshold) triggers cold override."""
    inp = _warm_idle_input(coolant_temp_c=74.0)
    payload = translator.translate(inp, _dna_high())
    assert payload.rpm_state_bucket == RpmStateBucket.COLD_OPEN_LOOP_INVALID
    assert payload.engine_warmed is False


def test_warm_engine_ect_75_degrees(translator):
    """ECT = 75.0 (at threshold) — no cold override."""
    inp = _warm_idle_input(coolant_temp_c=75.0)
    payload = translator.translate(inp, _dna_high())
    assert payload.rpm_state_bucket != RpmStateBucket.COLD_OPEN_LOOP_INVALID
    assert payload.engine_warmed is True


# ── 2-bank payload ─────────────────────────────────────────────────────

def test_2_bank_payload(translator):
    """2-bank V-engine: shrtft2 and longft2 populated in payload."""
    inp = _warm_idle_input(
        number_of_banks=2,
        shrtft1=-3.0,
        longft1=-5.0,
        shrtft2=-8.0,
        longft2=-12.0,
    )
    payload = translator.translate(inp, _dna_high())

    assert payload.shrtft2 == -8.0
    assert payload.longft2 == -12.0
    # TFT = bank1 only; bank2 separate per §12.1
    assert payload.total_trim_correction_delta == pytest.approx(-8.0)
    assert payload.total_trim_correction_delta_b2 == pytest.approx(-20.0)


def test_1_bank_bank2_fields_null(translator):
    """1-bank engine: shrtft2 and longft2 are null."""
    payload = translator.translate(_warm_idle_input(), _dna_high())
    assert payload.shrtft2 is None
    assert payload.longft2 is None


# ── STRESS_IDLE bucket ─────────────────────────────────────────────────

def test_stress_idle_bucket(translator):
    """RPM at stress_idle_rpm_target → STRESS_IDLE bucket."""
    inp = _warm_idle_input(
        engine_rpm=4000,
        calculated_engine_load_pct=50.0,
        mass_airflow_gps=15.0,
    )
    payload = translator.translate(inp, _dna_high())
    assert payload.rpm_state_bucket == RpmStateBucket.STRESS_IDLE


# ── error propagation ──────────────────────────────────────────────────

def test_out_of_range_rpm_propagates_error(translator):
    """engine_rpm > 8000 raises PIDValidationError."""
    inp = _warm_idle_input(engine_rpm=9000)
    with pytest.raises(PIDValidationError):
        translator.translate(inp, _dna_high())


def test_out_of_range_coolant_temp_propagates_error(translator):
    """coolant_temp_c > 140 raises PIDValidationError."""
    inp = _warm_idle_input(coolant_temp_c=150.0)
    with pytest.raises(PIDValidationError):
        translator.translate(inp, _dna_high())


def test_bank2_null_contract_violation(translator):
    """shrtft2 non-null with number_of_banks=1 raises PIDValidationError."""
    inp = _warm_idle_input(number_of_banks=1, shrtft2=5.0)
    with pytest.raises(PIDValidationError):
        translator.translate(inp, _dna_high())


def test_bank2_null_longft2_contract_violation(translator):
    """longft2 non-null with number_of_banks=1 raises PIDValidationError."""
    inp = _warm_idle_input(number_of_banks=1, longft2=5.0)
    with pytest.raises(PIDValidationError):
        translator.translate(inp, _dna_high())


# ── wideband O2 path ───────────────────────────────────────────────────

def test_wideband_o2_passthrough(translator):
    """WIDEBAND_LINEAR upstream_o2_type → direct lambda passthrough."""
    dna = ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.WIDEBAND_LINEAR,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )
    inp = _warm_idle_input(pid_wideband_equivalence_ratio=0.98)
    payload = translator.translate(inp, dna)
    assert payload.normalized_obd_lambda == pytest.approx(0.98)


# ── public surface ─────────────────────────────────────────────────────

def test_public_import():
    """from obdlab import SensorSignalTranslator, OBDLivePayload succeeds."""
    from obdlab import OBDLivePayload, SensorSignalTranslator  # noqa: F811
    assert SensorSignalTranslator is not None
    assert OBDLivePayload is not None


def test_iat_tps_inputs_and_ground_trace(translator):
    """Test IAT and TPS validate, IAT flows into VE, and ground trace passes without OBD verdict."""
    dna = _dna_high()

    # 1. Verify bounds and emit
    inp = _warm_idle_input(intake_air_temp_c=140.0, throttle_pos_pct=100.0)
    payload = translator.translate(inp, dna)
    assert payload.intake_air_temp_c == 140.0
    assert payload.throttle_pos_pct == 100.0

    # Test out of bounds in translate propagates PIDValidationError
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(intake_air_temp_c=141.0), dna)
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(throttle_pos_pct=100.1), dna)

    # 2. Verify IAT flows into ve_engine VE calculations
    # Changing IAT should change ve_pct (as air density changes)
    payload_cool = translator.translate(_warm_idle_input(intake_air_temp_c=0.0), dna)
    payload_hot = translator.translate(_warm_idle_input(intake_air_temp_c=80.0), dna)
    assert payload_cool.ve_pct is not None
    assert payload_hot.ve_pct is not None
    assert payload_cool.ve_pct != payload_hot.ve_pct

    # 3. Ground-trace fixture: IAT/ECT/TPS = -40 / -40 / 100 carries through
    # without OBD raising a verdict (OBDLab does not emit diagnostic verdicts, only fields)
    ground_trace_inp = _warm_idle_input(
        coolant_temp_c=-40.0,
        intake_air_temp_c=-40.0,
        throttle_pos_pct=100.0,
    )
    payload_gt = translator.translate(ground_trace_inp, dna)
    assert payload_gt.coolant_temp_c == -40.0
    assert payload_gt.intake_air_temp_c == -40.0
    assert payload_gt.throttle_pos_pct == 100.0
    # Confirm emitter discipline: no diagnostic_verdict/ecu_hw_verdict exists on OBDLivePayload
    assert not hasattr(payload_gt, "diagnostic_verdict")
    assert not hasattr(payload_gt, "ecu_hw_verdict")


def test_control_module_voltage_v_inputs(translator):
    """Test control_module_voltage_v validates, default value works, and low-rail carries through without OBD verdict."""
    dna = _dna_high()

    # 1. Default value when not provided
    inp_default = _warm_idle_input()
    payload_default = translator.translate(inp_default, dna)
    assert payload_default.control_module_voltage_v == 14.0

    # 2. Verify bounds and emit
    inp_valid = _warm_idle_input(control_module_voltage_v=18.0)
    payload_valid = translator.translate(inp_valid, dna)
    assert payload_valid.control_module_voltage_v == 18.0

    inp_valid_low = _warm_idle_input(control_module_voltage_v=0.0)
    payload_valid_low = translator.translate(inp_valid_low, dna)
    assert payload_valid_low.control_module_voltage_v == 0.0

    # Test out of bounds in translate propagates PIDValidationError
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(control_module_voltage_v=-0.1), dna)
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(control_module_voltage_v=18.1), dna)

    # 3. Ground-trace/low-rail fixture: control_module_voltage_v = 11.0 V carries through
    # without OBD raising a verdict (OBDLab does not emit diagnostic verdicts, only fields)
    low_rail_inp = _warm_idle_input(control_module_voltage_v=11.0)
    payload_lr = translator.translate(low_rail_inp, dna)
    assert payload_lr.control_module_voltage_v == 11.0
    # Confirm emitter discipline: no electrical_verdict/charging_verdict/ecu_fault exists on OBDLivePayload
    assert not hasattr(payload_lr, "electrical_verdict")
    assert not hasattr(payload_lr, "charging_verdict")


def test_per_cylinder_misfire_counts_inputs(translator):
    """Test per_cylinder_misfire_counts validates, default value works, and carries through without OBD verdict."""
    dna = _dna_high()

    # 1. Default value when not provided is None
    inp_default = _warm_idle_input()
    payload_default = translator.translate(inp_default, dna)
    assert payload_default.per_cylinder_misfire_counts is None

    # 2. Verify valid dictionary and conversion in translate
    inp_valid = _warm_idle_input(per_cylinder_misfire_counts={1: 12, 2: 0, 3: 1, 4: 0})  # wiki: research/chunks/fuel-trim/17
    payload_valid = translator.translate(inp_valid, dna)
    assert payload_valid.per_cylinder_misfire_counts == {1: 12, 2: 0, 3: 1, 4: 0}  # wiki: research/chunks/fuel-trim/17

    # Test out of bounds in translate propagates PIDValidationError
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(per_cylinder_misfire_counts="invalid"), dna)

    # 3. Ground-trace/emitter discipline check:
    # Confirm emitter discipline: no misfire_verdict/misfire_localisation/catalyst_meltdown_verdict exists on OBDLivePayload
    assert not hasattr(payload_valid, "misfire_verdict")
    assert not hasattr(payload_valid, "misfire_localisation")
    assert not hasattr(payload_valid, "catalyst_meltdown_verdict")


def test_ltft_cell_vector_inputs(translator):
    """Test ltft_cell_vector validates, default value works, and carries through without OBD verdict."""
    dna = _dna_high()

    # 1. Default value when not provided is None
    inp_default = _warm_idle_input()
    payload_default = translator.translate(inp_default, dna)
    assert payload_default.ltft_cell_vector is None

    # 2. Verify valid dictionary and conversion in translate
    inp_valid = _warm_idle_input(ltft_cell_vector={0: 2.5, 17: -5.0})  # wiki: research/chunks/fuel-trim/13
    payload_valid = translator.translate(inp_valid, dna)
    assert payload_valid.ltft_cell_vector == {0: 2.5, 17: -5.0}  # wiki: research/chunks/fuel-trim/13

    # Test out of bounds in translate propagates PIDValidationError
    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(ltft_cell_vector="invalid"), dna)

    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(ltft_cell_vector={-1: 5.0}), dna)  # wiki: research/chunks/fuel-trim/13

    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(ltft_cell_vector={0: -128.0}), dna)  # wiki: research/chunks/fuel-trim/13

    with pytest.raises(PIDValidationError):
        translator.translate(_warm_idle_input(ltft_cell_vector={0: 128.0}), dna)  # wiki: research/chunks/fuel-trim/13

    # 3. Ground-trace/emitter discipline check:
    # Confirm emitter discipline: no region_localisation/localisation/fault_family/lambda_chem/gas_ exists on OBDLivePayload
    assert not hasattr(payload_valid, "region_localisation")
    assert not hasattr(payload_valid, "localisation")
    assert not hasattr(payload_valid, "fault_family")


def test_wideband_offset_via_translator(translator):
    """Verify wideband offset candidate detection flows correctly through translate()."""
    dna = ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.WIDEBAND_LINEAR,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )
    # Prepare input for warm, steady idle but with equivalence ratio indicating offset
    inp = {
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 35.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "pid_wideband_equivalence_ratio": 1.08,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    payload = translator.translate(inp, dna)
    assert payload.normalized_obd_lambda == 1.08
    assert payload.o2_failure_mode == O2FailureMode.WIDEBAND_OFFSET_CANDIDATE



