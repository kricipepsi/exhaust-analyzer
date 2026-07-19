"""Regression tests for the C6 sensor-dynamics shim producer."""

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
    SensorDynamicsState,
    _control_plausibility_state,
    _Observation,
    _score_rule,
    _score_rule_raw,
    _sensor_dynamics_state,
)
from registry.schema_v2 import FaultFamily, Rule  # noqa: E402


def _obs(**pids: float | None) -> _Observation:
    """Build a tight observation with only the C6 OBD PID slice populated."""
    return _Observation(obd_pids=dict(pids))


def _rule(rule_id: str, family: FaultFamily = FaultFamily.SENSOR_FAULT) -> Rule:
    """Build a minimal rule whose C6 override may boost/prune without raw evidence."""
    return Rule(
        rule_id=rule_id,
        fault_family=family,
        description="unit-test rule",
        base_weight=0.42,
        competition_group=family.value,
        confidence_ceiling=None,
        passes_cases=["UNIT-C6"],
    )


def test_c6_mode06_margin_emits_o2_lazy_and_boosts_sensor_rules() -> None:
    """Mode $06 margin at or below 10% emits the O2 branch and boosts SF rules."""
    obs = _obs(mode06_o2_response_margin_pct=10.0)

    assert _sensor_dynamics_state(obs) is SensorDynamicsState.O2_LAZY_OR_BIASED
    assert _score_rule(_rule("SF-005"), obs) == pytest.approx(0.52)


def test_c6_maf_underread_requires_both_points_and_prunes_no_fault() -> None:
    """MAF underread fires only when both idle and 2500 rpm deltas cross -15%."""
    decisive = _obs(maf_actual_calc_delta_pct_idle=-18.0, maf_actual_calc_delta_pct_2500=-16.0)
    incomplete = _obs(maf_actual_calc_delta_pct_idle=-18.0, maf_actual_calc_delta_pct_2500=None)

    assert _sensor_dynamics_state(decisive) is SensorDynamicsState.MAF_UNDERREAD
    assert _score_rule(_rule("NF-001", FaultFamily.NO_FAULT), decisive) is None
    assert _sensor_dynamics_state(incomplete) is SensorDynamicsState.SENSOR_HEALTH_UNPROVEN_ABSTAIN
    assert _score_rule(_rule("NF-001", FaultFamily.NO_FAULT), incomplete) == _score_rule_raw(_rule("NF-001", FaultFamily.NO_FAULT), incomplete)


def test_c6_healthy_pdf_style_row_emits_no_boost_or_prune() -> None:
    """Healthy dynamic C6 values stay abstained and do not nudge PDF-4G-05-style rows."""
    obs = _obs(
        mode06_o2_response_margin_pct=55.0,
        maf_actual_calc_delta_pct_idle=-1.0,
        maf_actual_calc_delta_pct_2500=1.0,
        maf_gps_idle=3.0,
        maf_gps_2500=11.0,
        calc_airflow_gps_idle=3.0,
        calc_airflow_gps_2500=11.0,
    )

    assert _sensor_dynamics_state(obs) is SensorDynamicsState.SENSOR_HEALTH_UNPROVEN_ABSTAIN
    assert _score_rule(_rule("SF-001"), obs) == _score_rule_raw(_rule("SF-001"), obs)
    assert _score_rule(_rule("NF-002", FaultFamily.NO_FAULT), obs) == _score_rule_raw(
        _rule("NF-002", FaultFamily.NO_FAULT), obs
    )

def test_c3_precedence_prunes_static_c6_but_decisive_c6_reenables_sensor_rules() -> None:
    """C3 prune wins unless decisive dynamic C6 evidence is present on the same row."""
    static_c6 = _obs(dlc_signal_ground_drop_v=0.25, mode06_o2_response_margin_pct=55.0)
    decisive_c6 = _obs(dlc_signal_ground_drop_v=0.25, mode06_o2_response_margin_pct=5.0)

    assert _control_plausibility_state(static_c6) is ControlPlausibilityState.CONTROL_REFERENCE_FAULT
    assert _score_rule(_rule("SF-001"), static_c6) is None
    assert _score_rule(_rule("SF-001"), decisive_c6) == pytest.approx(0.52)


def test_no_c6_columns_leave_no_fault_scoring_untouched() -> None:
    """Rows without the C6 column set do not prune no-fault rules."""
    obs = _obs()

    assert _sensor_dynamics_state(obs) is None
    assert _score_rule(_rule("NF-001", FaultFamily.NO_FAULT), obs) == _score_rule_raw(_rule("NF-001", FaultFamily.NO_FAULT), obs)
