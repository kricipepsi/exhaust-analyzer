"""Regression tests for the wired-v7 multi-dimension scorer."""

from __future__ import annotations

import sys
from pathlib import Path

V7_ROOT = Path(__file__).resolve().parents[1]
if str(V7_ROOT) not in sys.path:
    sys.path.insert(0, str(V7_ROOT))

from run_suite import score_case  # noqa: E402


def _oracle(**overrides: str) -> dict[str, str]:
    """Return a minimal oracle row with all pinned scoring dimensions."""
    row = {
        "expected_fault_family": "lean_condition",
        "expected_fault_code": "ERR-LC-001",
        "expected_state": "named_fault",
        "expected_confidence_min": "0.70",
        "expected_confidence_max": "0.90",
        "expected_perception_gap": "false",
        "expected_demotion_note_contains": "",
        "expected_crash_abort": "none",
    }
    row.update(overrides)
    return row


def _result(**overrides: object) -> dict[str, object]:
    """Return a minimal diagnose() model_dump-shaped output."""
    result: dict[str, object] = {
        "diagnostic_verdict": {
            "is_fault_detected": True,
            "fault_code": "ERR-LC-001",
            "fault_name": "Classic lean condition",
            "fault_family": "lean_condition",
            "display_headline": "Classic lean condition",
            "confidence_score": 0.80,
            "actionable_remediation": "Smoke-test intake for vacuum leaks.",
            "differential_siblings": [],
        },
        "performance_analytics": {
            "lambda_perception_delta": 0.0,
            "o2_sensor_bias_verdict": None,
            "severity_level": "WARNING_DEGRADED_PERFORMANCE",
        },
        "execution_meta": {
            "degradation_mode": "FULL_FUSION",
            "lab_routing_directive": {"reasons": []},
        },
        "fault_enrichment": {
            "mechanical_failure_mode": "Unmetered air causing lean mixture.",
            "ui_remediation_steps": ["Inspect intake tract."],
        },
    }
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key].update(value)  # type: ignore[union-attr]
        else:
            result[key] = value
    return result


def test_all_pinned_accuracy_dimensions_pass() -> None:
    """Matching family/code/state/confidence/perception dimensions all pass."""
    outcomes = score_case(_result(), _oracle())

    assert outcomes == {
        "fault_family": "PASS",
        "fault_code": "PASS",
        "state": "PASS",
        "confidence": "PASS",
        "perception_gap": "PASS",
        "demotion_note_contains": "NA",
    }


def test_confidence_band_miss_fails_only_confidence_dimension() -> None:
    """Out-of-band confidence is isolated to the confidence dimension."""
    result = _result(diagnostic_verdict={"confidence_score": 0.95})

    outcomes = score_case(result, _oracle())

    assert outcomes["confidence"] == "FAIL"
    assert outcomes["fault_family"] == "PASS"
    assert outcomes["fault_code"] == "PASS"


def test_demotion_substring_miss_fails_demotion_dimension() -> None:
    """Missing demotion text fails the demotion_note_contains dimension."""
    outcomes = score_case(_result(), _oracle(expected_demotion_note_contains="catalyst_healthy"))

    assert outcomes["demotion_note_contains"] == "FAIL"
    assert outcomes["fault_family"] == "PASS"


def test_perception_gap_uses_o2_bias_verdict_presence() -> None:
    """A non-null O2 bias verdict satisfies expected_perception_gap=true."""
    result = _result(performance_analytics={"o2_sensor_bias_verdict": "O2_SENSOR_BIASED_HIGH"})

    outcomes = score_case(result, _oracle(expected_perception_gap="true"))

    assert outcomes["perception_gap"] == "PASS"


def test_unexpected_exception_on_well_formed_case_is_crash_failure() -> None:
    """Unexpected diagnose() exceptions fail every dimension for accuracy cases."""
    outcomes = score_case(None, _oracle(), raised_exception=RuntimeError("boom"))

    assert set(outcomes.values()) == {"FAIL"}


def test_expected_validation_error_passes_invalid_case() -> None:
    """Expected validation errors are handled outcomes, not scorer crashes."""
    outcomes = score_case(
        None,
        _oracle(
            expected_fault_family="invalid_input",
            expected_state="invalid_input",
            expected_crash_abort="validation_error",
        ),
        raised_exception=ValueError("bad DTC"),
    )

    assert set(outcomes.values()) == {"PASS"}
