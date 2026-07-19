"""Integration smoke test — exercises the full OBDLab pipeline end-to-end.

Covers:
  - Minimal valid input + dna_view=None + assert payload round-trips.
  - 2-bank V-engine with both bank trims.
  - STRESS_IDLE with wideband O2 passthrough.
  - PID bounds violation propagates error.
  - Cold engine with dna_view=None.
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
from obdlab.schemas.vocabulary import RpmStateBucket, VEValidity


@pytest.fixture(scope="module")
def translator():
    return SensorSignalTranslator()


@pytest.fixture(scope="module")
def dna_high():
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )


# ── smoke: minimal valid input + None DNA ──────────────────────────────

def test_smoke_minimal_input_none_dna(translator):
    """Minimal valid input + dna_view=None → payload emitted, JSON round-trips."""
    inputs = {
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
    payload = translator.translate(inputs, dna_view=None)

    assert isinstance(payload, OBDLivePayload)
    assert payload.engine_warmed is True
    assert payload.rpm_state_bucket == RpmStateBucket.STABILIZED_IDLE
    assert payload.engine_rpm == 800

    json_str = payload.model_dump_json()
    reloaded = OBDLivePayload.model_validate_json(json_str)
    assert reloaded == payload


# ── smoke: 2-bank V-engine ─────────────────────────────────────────────

def test_smoke_2_bank_v_engine(translator, dna_high):
    """2-bank V-engine: both bank-1 and bank-2 trims in payload."""
    inputs = {
        "engine_rpm": 800,
        "coolant_temp_c": 92.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 35.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "shrtft2": -8.0,
        "longft2": -12.0,
        "number_of_banks": 2,
        "fuel_sys_status": "Closed_Loop",
        "pid_oxygen_sensor_volts": 0.45,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    payload = translator.translate(inputs, dna_high)

    assert payload.shrtft2 == -8.0
    assert payload.longft2 == -12.0
    assert payload.total_trim_correction_delta == pytest.approx(-8.0)
    assert payload.total_trim_correction_delta_b2 == pytest.approx(-20.0)


# ── smoke: STRESS_IDLE with wideband O2 ────────────────────────────────

def test_smoke_stress_idle_wideband(translator):
    """STRESS_IDLE bucket with wideband O2 passthrough."""
    dna = ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.WIDEBAND_LINEAR,
        induction_type=InductionType.TURBOCHARGED,
        confidence=VinConfidence.HIGH,
    )
    inputs = {
        "engine_rpm": 4000,
        "coolant_temp_c": 94.0,
        "calculated_engine_load_pct": 50.0,
        "mass_airflow_gps": 18.0,
        "manifold_vacuum_kpa": 45.0,
        "intake_air_temp_c": 40.0,
        "shrtft1": -5.0,
        "longft1": -8.0,
        "pid_wideband_equivalence_ratio": 0.98,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    payload = translator.translate(inputs, dna)

    assert payload.rpm_state_bucket == RpmStateBucket.STRESS_IDLE
    assert payload.normalized_obd_lambda == pytest.approx(0.98)


# ── smoke: PID bounds violation propagates ─────────────────────────────

def test_smoke_bounds_violation(translator, dna_high):
    """engine_rpm > 8000 raises PIDValidationError."""
    inputs = {
        "engine_rpm": 9000,
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
    with pytest.raises(PIDValidationError):
        translator.translate(inputs, dna_high)


# ── smoke: cold engine + None DNA ──────────────────────────────────────

def test_smoke_cold_engine_none_dna(translator):
    """Cold engine (ECT=40°C) + dna_view=None → COLD_OPEN_LOOP_INVALID, analytics frozen."""
    inputs = {
        "engine_rpm": 800,
        "coolant_temp_c": 40.0,
        "calculated_engine_load_pct": 22.0,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 30.0,
        "intake_air_temp_c": 15.0,
        "shrtft1": -3.0,
        "longft1": -5.0,
        "number_of_banks": 1,
        "fuel_sys_status": "Open_Loop_Cold",
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    payload = translator.translate(inputs, dna_view=None)

    assert payload.engine_warmed is False
    assert payload.rpm_state_bucket == RpmStateBucket.COLD_OPEN_LOOP_INVALID
    assert payload.normalized_obd_lambda == pytest.approx(1.0)
    assert payload.total_trim_correction_delta == 0.0
    assert payload.ve_validity == VEValidity.UNKNOWN
    assert payload.ve_pct == 0.0  # wiki: §10 — 0.0 sentinel when analytics frozen
    # Payload still emitted
    assert payload.engine_rpm == 800
    assert payload.coolant_temp_c == 40.0
