"""Unit tests for the C4 signal commit shim logic and collision rules."""

from __future__ import annotations

import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
COMLAB_ROOT = WORKSPACE_ROOT / "labs/comlab"
if str(COMLAB_ROOT) not in sys.path:
    sys.path.insert(0, str(COMLAB_ROOT))

import pytest
from registry.integration_shim import (
    C4SignalState,
    ControlPlausibilityState,
    LeanRootCauseState,
    SensorDynamicsState,
    _build_observation,
    _c4_signal_state,
    _control_plausibility_state,
    _lean_root_cause_state,
    _score_rule,
    _score_rule_raw,
    _sensor_dynamics_state,
)
from registry.schema_v2 import FaultFamily, Rule


def _obs(**pids: float | None) -> _Observation:
    """Build a tight observation with the specified OBD PIDs."""
    from registry.integration_shim import _Observation
    return _Observation(obd_pids=dict(pids))


def _rule(rule_id: str, family: FaultFamily = FaultFamily.LEAN_CONDITION) -> Rule:
    """Build a minimal rule for scoring overrides."""
    return Rule(
        rule_id=rule_id,
        fault_family=family,
        description="test rule",
        base_weight=0.52,
        competition_group="test",
        passes_cases=["dummy_case"],
    )


def test_c4_emit_paths() -> None:
    """Verify each C4 signal state evaluates correctly under Scenario 3."""
    # 1. LEAK via delta_stft
    obs_leak_delta = _obs(stft_idle_pct=10.0, stft_2500_pct=2.0, co2_idle_pct=14.0)
    assert _c4_signal_state(obs_leak_delta) is C4SignalState.LEAK

    # 2. LEAK via CO2 dilution
    obs_leak_co2 = _obs(stft_idle_pct=0.0, stft_2500_pct=0.0, co2_idle_pct=10.0)
    assert _c4_signal_state(obs_leak_co2) is C4SignalState.LEAK

    # 3. LEAK via elevated O2
    obs_leak_o2 = _obs(stft_idle_pct=0.0, stft_2500_pct=0.0, co2_idle_pct=14.0, tailpipe_o2_elevation_pct=3.0)
    assert _c4_signal_state(obs_leak_o2) is C4SignalState.LEAK

    # 4. PERSIST_BIAS
    obs_bias = _obs(stft_idle_pct=0.0, stft_2500_pct=0.0, co2_idle_pct=14.0, downstream_o2_v=0.8, propane_trim_shift_pct=-10.0)
    assert _c4_signal_state(obs_bias) is C4SignalState.PERSIST_BIAS

    # 5. PERSIST_LEAN
    obs_lean = _obs(stft_idle_pct=0.0, stft_2500_pct=0.0, co2_idle_pct=14.0, downstream_o2_v=0.3, propane_trim_shift_pct=-20.0)
    assert _c4_signal_state(obs_lean) is C4SignalState.PERSIST_LEAN

    # 6. ABSTAIN
    obs_abstain = _obs(stft_idle_pct=0.0, stft_2500_pct=0.0, co2_idle_pct=14.0, downstream_o2_v=0.5, propane_trim_shift_pct=-10.0)
    assert _c4_signal_state(obs_abstain) is C4SignalState.ABSTAIN

    # 7. Completely absent
    obs_none = _obs()
    assert _c4_signal_state(obs_none) is None


def test_c4_no_distinct_data_returns_none() -> None:
    """Verify that a case with trims but NO C4 distinct columns returns None (prevents C5 leaks)."""
    # This has delta_stft = -15.0 which would normally be a LEAK, but because no C4 distinct
    # columns (co2, tailpipe_o2, downstream_o2, propane) are populated, it returns None.
    obs_only_trims = _obs(stft_idle_pct=15.0, stft_2500_pct=0.0)
    assert _c4_signal_state(obs_only_trims) is None


def test_c4_c5_collision_leak_wins() -> None:
    """Verify C4 LEAK overrides C5 vacuum leak on conflict (C4 direct gas wins over C5 indirect trims)."""
    # Trims satisfy C5 vacuum leak, but C4 gas confirms LEAK
    obs_leak = _obs(
        stft_idle_pct=16.0, ltft_idle_pct=0.0, stft_2500_pct=1.0, ltft_2500_pct=0.0,
        co2_idle_pct=9.0
    )
    assert _lean_root_cause_state(obs_leak) is LeanRootCauseState.VACUUM_LEAK_TRIM_PATTERN
    assert _c4_signal_state(obs_leak) is C4SignalState.LEAK

    # Scoring check: EL-001 is boosted, LC-001 is pruned
    assert _score_rule(_rule("EL-001", FaultFamily.EXHAUST_LEAK), obs_leak) == pytest.approx(0.62)
    assert _score_rule(_rule("LC-001"), obs_leak) is None


def test_c4_c5_collision_c5_wins_on_bias() -> None:
    """Verify C5 (better-grounded lean) overrides C4 PERSIST_BIAS (anecdotal bias check)."""
    # Trims/WOT satisfy C5 fuel shortfall, C4 O2/propane suggest PERSIST_BIAS
    obs_bias = _obs(
        stft_idle_pct=15.0, stft_2500_pct=10.0,
        co2_idle_pct=14.0, downstream_o2_v=0.8, propane_trim_shift_pct=-10.0,
        wideband_lambda_wot=1.06, fuel_rail_pressure_load_kpa=250.0
    )
    assert _lean_root_cause_state(obs_bias) is LeanRootCauseState.FUEL_DELIVERY_SHORTFALL
    assert _c4_signal_state(obs_bias) is C4SignalState.PERSIST_BIAS

    # Scoring check: LC-001 is boosted, SF-001 is pruned
    assert _score_rule(_rule("LC-001"), obs_bias) == pytest.approx(0.62)
    assert _score_rule(_rule("SF-001", FaultFamily.SENSOR_FAULT), obs_bias) is None
