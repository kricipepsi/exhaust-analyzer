"""Tests for OBD perception-delta channel for ecu_fault (T-OBDV2-ECU-PERCEPT-1)."""

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


def _dna_narrowband() -> ObdLabDnaView:
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )


def _dna_wideband() -> ObdLabDnaView:
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        upstream_o2_type=O2SensorType.WIDEBAND_LINEAR,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )



def _warm_idle_input_nb(**overrides):
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


def _warm_idle_input_wb(**overrides):
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
        "pid_wideband_equivalence_ratio": 1.0,
        "active_dtcs": [],
        "drive_cycles_since_clear": 5,
    }
    base.update(overrides)
    return base


@pytest.fixture
def translator():
    return SensorSignalTranslator()


# ── computability branches ─────────────────────────────────────────────

def test_narrowband_delta_none(translator):
    """Even if commanded_equivalence_ratio is present, narrowband upstream O2 defaults delta to None."""
    dna = _dna_narrowband()
    inp = _warm_idle_input_nb(commanded_equivalence_ratio=1.0)
    payload = translator.translate(inp, dna)
    assert payload.lambda_perception_delta is None


def test_wideband_missing_commanded_delta_none(translator):
    """Wideband upstream O2 lacking commanded_equivalence_ratio results in None delta."""
    dna = _dna_wideband()
    inp = _warm_idle_input_wb()
    assert "commanded_equivalence_ratio" not in inp
    payload = translator.translate(inp, dna)
    assert payload.lambda_perception_delta is None


def test_wideband_with_commanded_delta(translator):
    """Wideband upstream O2 + commanded_equivalence_ratio calculates lambda_perception_delta."""
    dna = _dna_wideband()

    # Case 1: stoichiometric (1.0 vs 1.0)
    inp1 = _warm_idle_input_wb(pid_wideband_equivalence_ratio=1.0, commanded_equivalence_ratio=1.0)
    payload1 = translator.translate(inp1, dna)
    assert payload1.normalized_obd_lambda == 1.0
    assert payload1.lambda_perception_delta == pytest.approx(0.0)

    # Case 2: rich sensor (0.95), lean commanded (1.05)
    # delta = 0.95 - 1.05 = -0.10
    inp2 = _warm_idle_input_wb(pid_wideband_equivalence_ratio=0.95, commanded_equivalence_ratio=1.05)
    payload2 = translator.translate(inp2, dna)
    assert payload2.normalized_obd_lambda == 0.95
    assert payload2.lambda_perception_delta == pytest.approx(-0.10)


# ── invalid input ──────────────────────────────────────────────────────

def test_commanded_non_numeric_raises(translator):
    """Non-numeric commanded_equivalence_ratio raises a PIDValidationError."""
    dna = _dna_wideband()
    inp = _warm_idle_input_wb(commanded_equivalence_ratio="stoich")
    with pytest.raises(PIDValidationError, match="commanded_equivalence_ratio must be numeric"):
        translator.translate(inp, dna)


# ── emitter discipline ──────────────────────────────────────────────────

def test_emitter_discipline_no_verdict(translator):
    """Verify OBDLab stays an emitter and does not construct fault-family verdicts."""
    dna = _dna_wideband()
    inp = _warm_idle_input_wb(pid_wideband_equivalence_ratio=0.95, commanded_equivalence_ratio=1.05)
    payload = translator.translate(inp, dna)

    # Assert no fault-related verdict fields are exposed on the payload schema
    for attr in dir(payload):
        assert "ecu_fault" not in attr.lower()
        assert "fault_family" not in attr.lower()
