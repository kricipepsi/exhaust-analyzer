"""Regression tests for the C5 lean-root-cause shim producer."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
COMLAB_ROOT = WORKSPACE_ROOT / "labs/comlab"
if str(COMLAB_ROOT) not in sys.path:
    sys.path.insert(0, str(COMLAB_ROOT))

from registry.integration_shim import (  # noqa: E402
    ControlPlausibilityState,
    LeanRootCauseState,
    SensorDynamicsState,
    _control_plausibility_state,
    _lean_root_cause_state,
    _Observation,
    _score_rule,
    _sensor_dynamics_state,
)
from registry.schema_v2 import FaultFamily, Rule  # noqa: E402


def _obs(**pids: float | None) -> _Observation:
    """Build a tight observation with only the C5/C3/C6 OBD PID slice populated."""
    return _Observation(obd_pids=dict(pids))


def _rule(rule_id: str, family: FaultFamily = FaultFamily.LEAN_CONDITION) -> Rule:
    """Build a minimal rule whose override may boost/prune without raw evidence."""
    return Rule(
        rule_id=rule_id,
        fault_family=family,
        description="unit-test rule",
        base_weight=0.42,
        competition_group=family.value,
        confidence_ceiling=None,
        passes_cases=["UNIT-C5"],
    )


def test_c5_each_emit_path() -> None:
    """Test each C5 emit path evaluates correctly."""
    # 1. VACUUM_LEAK_TRIM_PATTERN
    obs_vac = _obs(stft_idle_pct=5.0, ltft_idle_pct=10.0, stft_2500_pct=0.0, ltft_2500_pct=0.0)
    assert _lean_root_cause_state(obs_vac) is LeanRootCauseState.VACUUM_LEAK_TRIM_PATTERN

    # 2. FUEL_DELIVERY_SHORTFALL
    obs_fuel_port = _obs(stft_idle_pct=0.0, ltft_idle_pct=0.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                         wideband_lambda_wot=1.06, fuel_rail_pressure_load_kpa=250.0)
    assert _lean_root_cause_state(obs_fuel_port) is LeanRootCauseState.FUEL_DELIVERY_SHORTFALL

    obs_fuel_di = _obs(stft_idle_pct=0.0, ltft_idle_pct=0.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                       wideband_lambda_wot=1.06, fuel_rail_pressure_load_kpa=11000.0)
    assert _lean_root_cause_state(obs_fuel_di) is LeanRootCauseState.FUEL_DELIVERY_SHORTFALL

    # 3. MAF_UNDERREAD
    obs_maf = _obs(stft_idle_pct=0.0, ltft_idle_pct=0.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                   calc_load_wot_pct=75.0, stft_load_pct=1.0, ltft_load_pct=1.0)
    assert _lean_root_cause_state(obs_maf) is LeanRootCauseState.MAF_UNDERREAD


def test_c5_static_only_idle_only_abstain() -> None:
    """Test static-only/idle-only row evaluates to abstain no-op (SENSOR_HEALTH_UNPROVEN_ABSTAIN)."""
    obs_static = _obs(stft_idle_pct=5.0, ltft_idle_pct=5.0, stft_2500_pct=5.0, ltft_2500_pct=5.0)
    assert _lean_root_cause_state(obs_static) is LeanRootCauseState.SENSOR_HEALTH_UNPROVEN_ABSTAIN


def test_c5_none_column_paths() -> None:
    """Test None-column paths (e.g. rail pressure None, MAF None) handle correctly."""
    obs_rail_none = _obs(stft_idle_pct=0.0, ltft_idle_pct=0.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                         wideband_lambda_wot=1.06, fuel_rail_pressure_load_kpa=None)
    assert _lean_root_cause_state(obs_rail_none) is LeanRootCauseState.SENSOR_HEALTH_UNPROVEN_ABSTAIN

    obs_maf_none = _obs(stft_idle_pct=0.0, ltft_idle_pct=0.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                        calc_load_wot_pct=None, stft_load_pct=None, ltft_load_pct=None)
    assert _lean_root_cause_state(obs_maf_none) is LeanRootCauseState.SENSOR_HEALTH_UNPROVEN_ABSTAIN


def test_c5_egr_healthy_row_emits_nothing() -> None:
    """EGR healthy/lookalike row emits SENSOR_HEALTH_UNPROVEN_ABSTAIN."""
    obs_egr = _obs(stft_idle_pct=1.0, ltft_idle_pct=1.0, stft_2500_pct=1.0, ltft_2500_pct=1.0,
                   calc_load_wot_pct=90.0, stft_load_pct=0.0, ltft_load_pct=0.0,
                   fuel_rail_pressure_load_kpa=350.0, wideband_lambda_wot=0.85)
    assert _lean_root_cause_state(obs_egr) is LeanRootCauseState.SENSOR_HEALTH_UNPROVEN_ABSTAIN


def test_c5_c3_precedence() -> None:
    """C3 precedence: synthetic both-states row -> C3 wins (C5 override is bypassed)."""
    obs = _obs(dlc_signal_ground_drop_v=0.25,
               stft_idle_pct=5.0, ltft_idle_pct=10.0, stft_2500_pct=0.0, ltft_2500_pct=0.0)

    assert _control_plausibility_state(obs) is ControlPlausibilityState.CONTROL_REFERENCE_FAULT
    assert _lean_root_cause_state(obs) is LeanRootCauseState.VACUUM_LEAK_TRIM_PATTERN

    assert _score_rule(_rule("LC-001"), obs) is None
    assert _score_rule(_rule("EF-001", FaultFamily.ECU_FAULT), obs) == pytest.approx(0.52)


def test_c5_c6_collision() -> None:
    """C6-collision: MAF delta alone fires neither; both decisive -> C5 wins."""
    obs_maf_alone = _obs(maf_actual_calc_delta_pct_idle=-20.0, maf_actual_calc_delta_pct_2500=-20.0)
    assert _sensor_dynamics_state(obs_maf_alone) is SensorDynamicsState.MAF_UNDERREAD
    assert _lean_root_cause_state(obs_maf_alone) is None

    obs_both = _obs(stft_idle_pct=5.0, ltft_idle_pct=10.0, stft_2500_pct=0.0, ltft_2500_pct=0.0,
                    maf_actual_calc_delta_pct_idle=-20.0, maf_actual_calc_delta_pct_2500=-20.0)

    assert _sensor_dynamics_state(obs_both) is SensorDynamicsState.MAF_UNDERREAD
    assert _lean_root_cause_state(obs_both) is LeanRootCauseState.VACUUM_LEAK_TRIM_PATTERN

    assert _score_rule(_rule("LC-001"), obs_both) == pytest.approx(0.52)
    assert _score_rule(_rule("SF-005", FaultFamily.SENSOR_FAULT), obs_both) is None


def test_c5_no_columns_leaves_scoring_untouched() -> None:
    """A row without C5 columns (trims None) returns None and does not alter scoring."""
    obs = _obs()
    assert _lean_root_cause_state(obs) is None
    assert _score_rule(_rule("LC-001"), obs) is None
