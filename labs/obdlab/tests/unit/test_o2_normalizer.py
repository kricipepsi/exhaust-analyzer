"""Tests for O2Normalizer — 2-branch O2 normalisation per OBDLab_KG_Wiki.md §11."""

import pytest

from obdlab.core.exceptions import PIDValidationError
from obdlab.core.o2_normalizer import (
    O2Normalizer,
)
from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)
from obdlab.schemas.vocabulary import (
    FuelSystemStatus,
    O2FailureMode,
    O2NormalizationMode,
)


def _dna_view(sensor_type=O2SensorType.NARROWBAND_0_TO_1V):
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=sensor_type,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )



@pytest.fixture
def normalizer():
    return O2Normalizer()


# ==================================================================
# Narrowband — 3-zone midpoint tests
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.25, 1.05),   # wiki: §11.1 — LEAN_STATE midpoint
    (0.45, 1.00),   # wiki: §11.1 — STOICHIOMETRIC_CENTER midpoint
    (0.70, 0.95),   # wiki: §11.1 — RICH_STATE midpoint
])
def test_narrowband_zone_midpoints(normalizer, volts, expected_lambda):
    """Each narrowband zone midpoint maps to the correct lambda."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA


# ==================================================================
# Narrowband — boundary tests
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.10, 1.05),   # wiki: §11.1 — lower bound of LEAN_STATE
    (0.40, 1.05),   # wiki: §11.1 — upper bound of LEAN_STATE
    (0.41, 1.00),   # wiki: §11.1 — lower bound of STOICHIOMETRIC_CENTER
    (0.50, 1.00),   # wiki: §11.1 — upper bound of STOICHIOMETRIC_CENTER
    (0.51, 0.95),   # wiki: §11.1 — lower bound of RICH_STATE
    (0.90, 0.95),   # wiki: §11.1 — upper bound of RICH_STATE
])
def test_narrowband_zone_boundaries(normalizer, volts, expected_lambda):
    """Zone boundaries map to the correct lambda values."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA


# ==================================================================
# Narrowband — out-of-range
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.09, 1.05),   # wiki: §11 — below minimum hardware voltage → clamped lean
    (0.91, 0.95),   # wiki: §11 — above maximum hardware voltage → clamped rich
    (1.50, 0.95),   # wiki: §11 — far above max → clamped rich
    (-0.10, 1.05),  # wiki: §11 — negative voltage → clamped lean
])
def test_narrowband_out_of_range_degrade(normalizer, volts, expected_lambda):
    """Voltage outside [0.10, 0.90] returns O2_CHANNEL_FAULT with clamped lambda."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.O2_CHANNEL_FAULT


# ==================================================================
# Wideband — typical value passthrough
# ==================================================================

@pytest.mark.parametrize("ratio", [
    0.95,   # wiki: §11.2 — slightly rich
    1.00,   # wiki: §11.2 — stoichiometric
    1.05,   # wiki: §11.2 — slightly lean
])
def test_wideband_passthrough(normalizer, ratio):
    """Wideband equivalence ratio passes through unchanged."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {"pid_wideband_equivalence_ratio": ratio}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == ratio
    assert mode == O2NormalizationMode.WIDEBAND_PASSTHROUGH


# ==================================================================
# Wideband — out-of-range
# ==================================================================

@pytest.mark.parametrize("ratio,expected_lambda", [
    (0.69, 0.70),   # wiki: §11.2 — below 0.7 minimum → clamped to min
    (1.31, 1.30),   # wiki: §11.2 — above 1.3 maximum → clamped to max
])
def test_wideband_out_of_range_degrade(normalizer, ratio, expected_lambda):
    """Wideband ratio outside [0.7, 1.3] returns O2_CHANNEL_FAULT with clamped lambda."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {"pid_wideband_equivalence_ratio": ratio}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.O2_CHANNEL_FAULT


# ==================================================================
# Wideband — boundary values pass
# ==================================================================

@pytest.mark.parametrize("ratio", [
    0.70,   # wiki: §5 — lower bound of valid lambda range
    1.30,   # wiki: §5 — upper bound of valid lambda range
])
def test_wideband_boundaries_pass(normalizer, ratio):
    """Boundary values 0.7 and 1.3 are valid and pass through."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {"pid_wideband_equivalence_ratio": ratio}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == ratio
    assert mode == O2NormalizationMode.WIDEBAND_PASSTHROUGH


# ==================================================================
# DNA default — no dna_view → narrowband fallback
# ==================================================================

def test_dna_none_defaults_to_narrowband(normalizer):
    """Without DNA, narrowband is assumed and narrowband input is accepted."""
    pids = {"pid_oxygen_sensor_volts": 0.45}
    result_lambda, mode, failure = normalizer.normalize(pids, None)
    assert result_lambda == 1.00
    assert mode == O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA


# ==================================================================
# Missing input fields
# ==================================================================

def test_narrowband_missing_voltage_raises(normalizer):
    """When DNA says NARROWBAND but pid_oxygen_sensor_volts is missing."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"engine_rpm": 800}
    with pytest.raises(PIDValidationError, match="pid_oxygen_sensor_volts missing"):
        normalizer.normalize(pids, dna)


def test_wideband_missing_ratio_raises(normalizer):
    """When DNA says WIDEBAND but pid_wideband_equivalence_ratio is missing."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {"engine_rpm": 800}
    with pytest.raises(PIDValidationError, match="pid_wideband_equivalence_ratio missing"):
        normalizer.normalize(pids, dna)


# ==================================================================
# Non-numeric input rejection
# ==================================================================

def test_narrowband_non_numeric_raises(normalizer):
    """Non-numeric narrowband voltage raises PIDValidationError."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": "lean"}
    with pytest.raises(PIDValidationError, match="numeric"):
        normalizer.normalize(pids, dna)


def test_wideband_non_numeric_raises(normalizer):
    """Non-numeric wideband ratio raises PIDValidationError."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {"pid_wideband_equivalence_ratio": "stoich"}
    with pytest.raises(PIDValidationError, match="numeric"):
        normalizer.normalize(pids, dna)


# ==================================================================
# Wideband-in-NB-simulation — zone midpoint tests §11.3
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.25, 1.05),   # wiki: §11.3 — LEAN_STATE midpoint
    (0.45, 1.00),   # wiki: §11.3 — STOICHIOMETRIC_CENTER midpoint
    (0.70, 0.95),   # wiki: §11.3 — RICH_STATE midpoint
])
def test_wb_nb_sim_zone_midpoints(normalizer, volts, expected_lambda):
    """Each zone midpoint maps to correct lambda with WIDEBAND_NB_SIM mode."""
    dna = _dna_view(O2SensorType.WIDEBAND_NB_SIM)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA


# ==================================================================
# Wideband-in-NB-simulation — boundary tests §11.3
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.10, 1.05),   # wiki: §11.3 — lower bound of LEAN_STATE
    (0.40, 1.05),   # wiki: §11.3 — upper bound of LEAN_STATE
    (0.41, 1.00),   # wiki: §11.3 — lower bound of STOICHIOMETRIC_CENTER
    (0.50, 1.00),   # wiki: §11.3 — upper bound of STOICHIOMETRIC_CENTER
    (0.51, 0.95),   # wiki: §11.3 — lower bound of RICH_STATE
    (0.90, 0.95),   # wiki: §11.3 — upper bound of RICH_STATE
])
def test_wb_nb_sim_zone_boundaries(normalizer, volts, expected_lambda):
    """Zone boundaries map to correct lambda with WIDEBAND_NB_SIM mode."""
    dna = _dna_view(O2SensorType.WIDEBAND_NB_SIM)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA


# ==================================================================
# Wideband-in-NB-simulation — mode is NOT narrowband
# ==================================================================

def test_wb_nb_sim_mode_is_not_narrowband(normalizer):
    """Returned mode is WIDEBAND_NB_SIM, not NARROWBAND_VOLTAGE_TO_LAMBDA."""
    dna = _dna_view(O2SensorType.WIDEBAND_NB_SIM)
    pids = {"pid_oxygen_sensor_volts": 0.45}
    _result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert mode == O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA
    assert mode != O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA


# ==================================================================
# Wideband-in-NB-simulation — out-of-range §11.3
# ==================================================================

@pytest.mark.parametrize("volts,expected_lambda", [
    (0.09, 1.05),   # wiki: §11.3 — below minimum → clamped lean
    (0.91, 0.95),   # wiki: §11.3 — above maximum → clamped rich
])
def test_wb_nb_sim_out_of_range_degrade(normalizer, volts, expected_lambda):
    """Voltage outside [0.10, 0.90] returns O2_CHANNEL_FAULT for WB_NB_SIM."""
    dna = _dna_view(O2SensorType.WIDEBAND_NB_SIM)
    pids = {"pid_oxygen_sensor_volts": volts}
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == expected_lambda
    assert mode == O2NormalizationMode.O2_CHANNEL_FAULT


# ==================================================================
# Wideband-in-NB-simulation — missing PID
# ==================================================================

def test_wb_nb_sim_missing_voltage_raises(normalizer):
    """When DNA says WIDEBAND_NB_SIM but pid_oxygen_sensor_volts is missing."""
    dna = _dna_view(O2SensorType.WIDEBAND_NB_SIM)
    pids = {"engine_rpm": 800}
    with pytest.raises(PIDValidationError, match="pid_oxygen_sensor_volts missing"):
        normalizer.normalize(pids, dna)


# ==================================================================
# T-OBD-WIRE-1 — new O2FailureMode return tests
# ==================================================================

def test_channel_fault_low_voltage_gives_stuck_lean(normalizer):
    """O2_CHANNEL_FAULT + clamped lean lambda → STUCK_LEAN (wiki: §6.7)."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": 0.05}
    _lambda, mode, failure = normalizer.normalize(pids, dna)
    assert mode == O2NormalizationMode.O2_CHANNEL_FAULT
    assert failure == O2FailureMode.STUCK_LEAN


def test_channel_fault_high_voltage_gives_stuck_rich(normalizer):
    """O2_CHANNEL_FAULT + clamped rich lambda → STUCK_RICH (wiki: §6.7)."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": 0.95}
    _lambda, mode, failure = normalizer.normalize(pids, dna)
    assert mode == O2NormalizationMode.O2_CHANNEL_FAULT
    assert failure == O2FailureMode.STUCK_RICH


def test_healthy_narrowband_gives_no_fault(normalizer):
    """Healthy narrowband voltage → NO_FAULT (wiki: §6.7)."""
    dna = _dna_view(O2SensorType.NARROWBAND_0_TO_1V)
    pids = {"pid_oxygen_sensor_volts": 0.45}
    _lambda, mode, failure = normalizer.normalize(pids, dna)
    assert mode == O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA
    assert failure == O2FailureMode.NO_FAULT


# ==================================================================
# T-OBDV2-4 — Wideband Offset Candidate Tests
# ==================================================================

def test_wideband_offset_candidate_trigger(normalizer):
    """WIDEBAND_LINEAR + persistent |λ-1| > 0.05 → WIDEBAND_OFFSET_CANDIDATE."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == 1.08
    assert mode == O2NormalizationMode.WIDEBAND_PASSTHROUGH
    assert failure == O2FailureMode.WIDEBAND_OFFSET_CANDIDATE


def test_wideband_offset_in_band_gives_no_fault(normalizer):
    """WIDEBAND_LINEAR + persistent |λ-1| <= 0.05 → NO_FAULT."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.03,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    result_lambda, mode, failure = normalizer.normalize(pids, dna)
    assert result_lambda == 1.03
    assert mode == O2NormalizationMode.WIDEBAND_PASSTHROUGH
    assert failure == O2FailureMode.NO_FAULT


def test_wideband_offset_transient_cold_gives_no_fault(normalizer):
    """WIDEBAND_LINEAR + cold engine → NO_FAULT."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 60,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    _result_lambda, _mode, failure = normalizer.normalize(pids, dna)
    assert failure == O2FailureMode.NO_FAULT


def test_wideband_offset_transient_open_loop_gives_no_fault(normalizer):
    """WIDEBAND_LINEAR + Open Loop → NO_FAULT."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.OL,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    _result_lambda, _mode, failure = normalizer.normalize(pids, dna)
    assert failure == O2FailureMode.NO_FAULT


def test_wideband_offset_transient_wot_gives_no_fault(normalizer):
    """WIDEBAND_LINEAR + WOT → NO_FAULT."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 95,
        "dfco_active": False,
    }
    _result_lambda, _mode, failure = normalizer.normalize(pids, dna)
    assert failure == O2FailureMode.NO_FAULT


def test_wideband_offset_transient_dfco_gives_no_fault(normalizer):
    """WIDEBAND_LINEAR + DFCO → NO_FAULT."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 15,
        "dfco_active": True,
    }
    _result_lambda, _mode, failure = normalizer.normalize(pids, dna)
    assert failure == O2FailureMode.NO_FAULT


def test_emitter_discipline_offset(normalizer):
    """Assertion of emitter discipline: only Candidate returned, no verdict, no gas comparison."""
    dna = _dna_view(O2SensorType.WIDEBAND_LINEAR)
    pids = {
        "pid_wideband_equivalence_ratio": 1.08,
        "coolant_temp_c": 80,
        "fuel_sys_status": FuelSystemStatus.CL,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    _lambda, _mode, failure = normalizer.normalize(pids, dna)
    # The normalizer must only return WIDEBAND_OFFSET_CANDIDATE, not SENSOR_FAULT
    assert failure == O2FailureMode.WIDEBAND_OFFSET_CANDIDATE
    assert failure.value == "WIDEBAND_OFFSET_CANDIDATE"
    # Verify no SENSOR_FAULT in failure
    assert "SENSOR_FAULT" not in failure.value
