"""Tests for SemanticConsistencyChecker — 3 Physics Gates, thermal gate,
closed-loop sanity."""

import pytest

from obdlab.core.exceptions import SemanticConsistencyError
from obdlab.core.semantic_consistency_checker import SemanticConsistencyChecker
from obdlab.schemas.dna_view import (
    ObdLabDnaView,
)
from obdlab.schemas.vocabulary import RpmStateBucket


def _make_dna() -> ObdLabDnaView:
    return ObdLabDnaView.model_validate({
        "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
        "upstream_o2_type": "WIDEBAND_LINEAR",
        "induction_type": "NATURALLY_ASPIRATED",
        "emissions": {"egr_equipped": True},
        "resolved_horizon": "HORIZON_MODERN",
        "confidence": "HIGH",
        "rated_rpm": 6500,
        "engine_displacement_liters": 2.0,
        "stress_idle_rpm_target": 4000,
    })



def _pids(**overrides) -> dict:
    """Build a default valid sanitized_pids dict; override specific fields."""
    defaults = {
        "vss": 0,
        "engine_rpm": 800,
        "coolant_temp_c": 90,
        "calculated_engine_load_pct": 25,
        "mass_airflow_gps": 3.5,
        "manifold_vacuum_kpa": 35,
        "shrtft1": -5.0,
        "longft1": -10.0,
        "shrtft2": None,
        "longft2": None,
        "intake_air_temp_c": 30,
        "number_of_banks": 1,
        "fuel_sys_status": "Closed_Loop",
        "calculated_ve": 65.0,
        "rpm_state_bucket": "STABILIZED_IDLE",
    }
    defaults.update(overrides)
    return defaults


def _make_checker() -> SemanticConsistencyChecker:
    return SemanticConsistencyChecker()


# ======================================================================
# Physics_Gate_1 — VSS vs stalled engine
# ======================================================================

def test_gate1_pass_normal_idle():
    """VSS=0, RPM=800 → no error (vehicle stationary, engine running)."""
    checker = _make_checker()
    pids = _pids(vss=0, engine_rpm=800)
    result = checker.evaluate(pids, None)
    assert "Physics_Gate_1" in result["gates_passed"]


def test_gate1_fail_vehicle_moving_engine_stalled():
    """VSS=25, RPM=200 → SemanticConsistencyError."""
    checker = _make_checker()
    pids = _pids(vss=25, engine_rpm=200)
    with pytest.raises(SemanticConsistencyError, match="Physics_Gate_1"):
        checker.evaluate(pids, None)


def test_gate1_pass_missing_vss():
    """VSS absent → skip gate gracefully."""
    checker = _make_checker()
    pids = _pids(vss=None, engine_rpm=200)
    del pids["vss"]
    result = checker.evaluate(pids, None)
    assert "Physics_Gate_1" in result["gates_passed"]


# ======================================================================
# Physics_Gate_2 — closed loop expected above 80 °C
# ======================================================================

def test_gate2_pass_warm_closed_loop():
    """ECT=90, Closed_Loop → no error."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=90, fuel_sys_status="Closed_Loop")
    result = checker.evaluate(pids, None)
    assert "Physics_Gate_2" in result["gates_passed"]


def test_gate2_fail_hot_open_loop_cold():
    """ECT=85, Open_Loop_Cold → SemanticConsistencyError."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=85, fuel_sys_status="Open_Loop_Cold")
    with pytest.raises(SemanticConsistencyError, match="Physics_Gate_2"):
        checker.evaluate(pids, None)


def test_gate2_pass_cold_open_loop():
    """ECT=40, Open_Loop_Cold → no error (engine is genuinely cold)."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=40, fuel_sys_status="Open_Loop_Cold")
    result = checker.evaluate(pids, None)
    assert "Physics_Gate_2" in result["gates_passed"]





# ======================================================================
# Physics_Gate_4 — trim safety limits
# ======================================================================

def test_gate4_pass_normal_trims():
    """shrtft1=-5, longft1=-10 → no error (within safety range)."""
    checker = _make_checker()
    pids = _pids(shrtft1=-5.0, longft1=-10.0)
    result = checker.evaluate(pids, None)
    assert "Physics_Gate_4" in result["gates_passed"]


def test_gate4_fail_shrtft1_below_min():
    """shrtft1=-128 → SemanticConsistencyError (below widened OBD-rail bound)."""
    checker = _make_checker()
    pids = _pids(shrtft1=-128.0)
    with pytest.raises(SemanticConsistencyError, match="Physics_Gate_4"):
        checker.evaluate(pids, None)


def test_gate4_fail_longft1_above_max():
    """longft1=128 → SemanticConsistencyError (above widened OBD-rail bound)."""
    checker = _make_checker()
    pids = _pids(longft1=128.0)
    with pytest.raises(SemanticConsistencyError, match="Physics_Gate_4"):
        checker.evaluate(pids, None)


# ======================================================================
# Thermal gate (§4.1)
# ======================================================================

def test_thermal_gate_cold_engine():
    """ECT=40 → COLD_OPEN_LOOP_INVALID override, engine_warmed=false."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=40)
    result = checker.evaluate(pids, None)
    assert result["rpm_state_bucket_override"] == RpmStateBucket.COLD_OPEN_LOOP_INVALID
    assert result["engine_warmed"] is False


def test_thermal_gate_warm_engine():
    """ECT=90 → no override, engine_warmed=true."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=90)
    result = checker.evaluate(pids, None)
    assert result["rpm_state_bucket_override"] is None
    assert result["engine_warmed"] is True


def test_thermal_gate_exactly_at_cutoff():
    """ECT=75 → no override, engine_warmed=true (cutoff is < 75)."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=75)
    result = checker.evaluate(pids, None)
    assert result["rpm_state_bucket_override"] is None
    assert result["engine_warmed"] is True


# ======================================================================
# Closed-loop sanity gate (§4.2)
# ======================================================================

def test_closed_loop_sanity_warm_closed():
    """ECT=90, Closed_Loop → trim_analytics_suspect=false."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=90, fuel_sys_status="Closed_Loop")
    result = checker.evaluate(pids, None)
    assert result["trim_analytics_suspect"] is False


def test_closed_loop_sanity_warm_open_loop():
    """ECT=90, Open_Loop_Fault → trim_analytics_suspect=true.

    Uses a non-"Open_Loop_Cold" fuel status to avoid triggering
    Physics_Gate_2 (which specifically catches Open_Loop_Cold above 80 °C).
    """
    checker = _make_checker()
    pids = _pids(coolant_temp_c=90, fuel_sys_status="Open_Loop_Fault")
    result = checker.evaluate(pids, None)
    assert result["trim_analytics_suspect"] is True


def test_closed_loop_sanity_cold_open_loop():
    """ECT=40, Open_Loop_Cold → trim_analytics_suspect=false (engine cold, expected)."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=40, fuel_sys_status="Open_Loop_Cold")
    result = checker.evaluate(pids, None)
    assert result["trim_analytics_suspect"] is False


# ======================================================================
# Integration — multiple gates, result dict shape
# ======================================================================

def test_all_gates_pass_healthy_engine():
    """All gates pass on a healthy warm engine → result fields correct."""
    checker = _make_checker()
    pids = _pids()
    dna = _make_dna()
    result = checker.evaluate(pids, dna)
    assert result["rpm_state_bucket_override"] is None
    assert result["engine_warmed"] is True
    assert result["trim_analytics_suspect"] is False
    assert result["gates_passed"] == [
        "Physics_Gate_1", "Physics_Gate_2",
        "Physics_Gate_4",
    ]


def test_first_failing_gate_stops_processing():
    """Gate 1 failure means Gate 2-4 are not recorded in gates_passed."""
    checker = _make_checker()
    pids = _pids(vss=25, engine_rpm=200)
    with pytest.raises(SemanticConsistencyError, match="Physics_Gate_1"):
        checker.evaluate(pids, None)


def test_thermal_gate_before_physics_gates():
    """Cold engine → thermal gate still fires even though physics gates pass."""
    checker = _make_checker()
    pids = _pids(coolant_temp_c=40)
    result = checker.evaluate(pids, None)
    assert result["rpm_state_bucket_override"] == RpmStateBucket.COLD_OPEN_LOOP_INVALID
    assert result["engine_warmed"] is False
    assert "Physics_Gate_1" in result["gates_passed"]
