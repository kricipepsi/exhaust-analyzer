"""Unit tests for the C9 HealthConfirmationState producer and overrides."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
COMLAB_ROOT = WORKSPACE_ROOT / "labs/comlab"
if str(COMLAB_ROOT) not in sys.path:
    sys.path.insert(0, str(COMLAB_ROOT))

from registry.integration_shim import (  # noqa: E402
    HealthConfirmationState,
    _health_confirmation_state,
    _Observation,
    _score_rule,
    _score_rule_raw,
)
from registry.schema_v2 import FaultFamily, Rule  # noqa: E402


def _obs(**pids: float | bool | None) -> _Observation:
    """Build a tight observation with OBD PIDs."""
    # Coerce boolean/ints as float if resolved via typical payload pipeline,
    # but dict supports any types at evaluation.
    return _Observation(obd_pids=dict(pids))


def _rule(rule_id: str, family: FaultFamily = FaultFamily.NO_FAULT) -> Rule:
    """Build a minimal rule whose override may boost/prune."""
    return Rule(
        rule_id=rule_id,
        fault_family=family,
        description="unit-test rule",
        base_weight=0.42,
        competition_group=family.value,
        confidence_ceiling=None,
        passes_cases=["UNIT-C9"],
    )


def test_c9_emit_paths() -> None:
    """Verify SYSTEM_HEALTH_CONFIRMED and SENSOR_HEALTH_UNPROVEN_ABSTAIN conditions."""
    # Healthy case (all readiness complete, no DTCs, good margin, warmup, miles, good stable trims)
    obs_healthy = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
    )
    assert _health_confirmation_state(obs_healthy) is HealthConfirmationState.SYSTEM_HEALTH_CONFIRMED
    assert _score_rule(_rule("NF-001"), obs_healthy) == pytest.approx(0.52)

    # Unhealthy: pending DTC present
    obs_pending_dtc = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=1,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
    )
    assert _health_confirmation_state(obs_pending_dtc) is HealthConfirmationState.SENSOR_HEALTH_UNPROVEN_ABSTAIN
    assert _score_rule(_rule("NF-001"), obs_pending_dtc) == _score_rule_raw(_rule("NF-001"), obs_pending_dtc)

    # Unhealthy: low margin
    obs_low_margin = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=9.5,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
    )
    assert _health_confirmation_state(obs_low_margin) is HealthConfirmationState.SENSOR_HEALTH_UNPROVEN_ABSTAIN

    # Unhealthy: low miles
    obs_low_miles = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=199.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
    )
    assert _health_confirmation_state(obs_low_miles) is HealthConfirmationState.SENSOR_HEALTH_UNPROVEN_ABSTAIN

    # Unhealthy: unstable trims (trim delta > 5.0)
    obs_unstable_trims = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=5.0,
        ltft_idle_pct=0.0,  # TFT idle = 5.0
        stft_2500_pct=-1.0,
        ltft_2500_pct=0.0,  # TFT 2500 = -1.0, Delta = 6.0 > 5.0
    )
    assert _health_confirmation_state(obs_unstable_trims) is HealthConfirmationState.SENSOR_HEALTH_UNPROVEN_ABSTAIN


def test_c9_no_columns_leaves_scoring_untouched() -> None:
    """Verify that absent C9 columns return None and do not boost or prune."""
    obs = _obs(stft_idle_pct=0.0)
    assert _health_confirmation_state(obs) is None
    assert _score_rule(_rule("NF-001"), obs) == _score_rule_raw(_rule("NF-001"), obs)


def test_c9_era2_016_abstain() -> None:
    """Verify that era2_016's specific seed values evaluate to SENSOR_HEALTH_UNPROVEN_ABSTAIN."""
    obs = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=1,
        permanent_dtc_count=0,
        mode06_min_margin_pct=1.9,
        warmup_cycles_since_clear=28,
        miles_since_clear=282.0,
        stft_idle_pct=8.5,
        ltft_idle_pct=11.5,
        stft_2500_pct=3.5,
        ltft_2500_pct=6.1,
    )
    assert _health_confirmation_state(obs) is HealthConfirmationState.SENSOR_HEALTH_UNPROVEN_ABSTAIN
    assert _score_rule(_rule("NF-001"), obs) == _score_rule_raw(_rule("NF-001"), obs)


def test_c6_prune_beats_c9_boost() -> None:
    """Verify that dynamic C6 decisive sensor fault evidence prunes NF rules even if C9 says healthy."""
    obs = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
        # Trigger C6 decisive
        mode06_o2_response_margin_pct=10.0,
    )
    assert _health_confirmation_state(obs) is HealthConfirmationState.SYSTEM_HEALTH_CONFIRMED
    assert _score_rule(_rule("NF-001"), obs) is None


def test_c3_control_fault_beats_c9_boost() -> None:
    """Verify that C3 CONTROL_REFERENCE_FAULT prunes NF rules even if C9 says healthy."""
    obs = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
        # Trigger C3 CONTROL_REFERENCE_FAULT
        koeo_map_baro_delta_kpa=5.0,
    )
    assert _health_confirmation_state(obs) is HealthConfirmationState.SYSTEM_HEALTH_CONFIRMED
    assert _score_rule(_rule("NF-001"), obs) is None


def test_c4_decisive_beats_c9_boost() -> None:
    """Verify that C4 decisive exhaust leak or bias prunes NF rules even if C9 says healthy."""
    obs = _obs(
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=93.2,
        warmup_cycles_since_clear=26,
        miles_since_clear=636.0,
        stft_idle_pct=0.4,
        ltft_idle_pct=-5.8,
        stft_2500_pct=-0.8,
        ltft_2500_pct=-2.0,
        # Trigger C4 LEAK
        co2_idle_pct=10.0,
    )
    assert _health_confirmation_state(obs) is HealthConfirmationState.SYSTEM_HEALTH_CONFIRMED
    assert _score_rule(_rule("NF-001"), obs) is None
