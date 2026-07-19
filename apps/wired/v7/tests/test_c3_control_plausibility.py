"""Regression tests for the C3 control-plausibility shim producer."""

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
    _control_plausibility_state,
    _Observation,
    _score_rule,
)
from registry.schema_v2 import FaultFamily, Rule  # noqa: E402


def _obs(**pids: float | None) -> _Observation:
    """Build a tight observation with only the C3 OBD PID slice populated."""
    return _Observation(obd_pids=dict(pids))


def _rule(rule_id: str, family: FaultFamily = FaultFamily.ECU_FAULT) -> Rule:
    """Build a minimal rule whose C3 override may boost/prune without raw evidence."""
    return Rule(
        rule_id=rule_id,
        fault_family=family,
        description="unit-test rule",
        base_weight=0.42,
        competition_group=family.value,
        confidence_ceiling=None,
        passes_cases=["UNIT-C3"],
    )


@pytest.mark.parametrize(
    ("pids", "expected"),
    [
        ({"dlc_signal_ground_drop_v": 0.201}, ControlPlausibilityState.CONTROL_REFERENCE_FAULT),
        ({"koeo_map_baro_delta_kpa": 5.0}, ControlPlausibilityState.CONTROL_REFERENCE_FAULT),
        (
            {"bidirectional_fuel_response_ok_bool": 0.0, "module_voltage_loaded_v": 11.99},
            ControlPlausibilityState.CONTROL_REFERENCE_FAULT,
        ),
        (
            {
                "dlc_signal_ground_drop_v": 0.084,
                "koeo_map_baro_delta_kpa": 1.5,
                "bidirectional_fuel_response_ok_bool": 1.0,
                "module_voltage_loaded_v": 12.97,
            },
            None,
        ),
    ],
)
def test_c3_control_plausibility_state_gates(pids: dict[str, float], expected: ControlPlausibilityState | None) -> None:
    """The three Scenario-1 gates emit the state; a stay-abstained seed stays quiet."""
    assert _control_plausibility_state(_obs(**pids)) is expected


def test_c3_control_plausibility_boosts_ef_and_prunes_sf() -> None:
    """CONTROL_REFERENCE_FAULT boosts EF rules and prunes competing sensor-fault rules."""
    obs = _obs(dlc_signal_ground_drop_v=0.25)

    assert _score_rule(_rule("EF-001"), obs) == pytest.approx(0.52)
    assert _score_rule(_rule("SF-001", FaultFamily.SENSOR_FAULT), obs) is None
