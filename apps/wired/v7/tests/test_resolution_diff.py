"""Tests for the v3 per-case resolution diff harness."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

V7_ROOT = Path(__file__).resolve().parents[1]
if str(V7_ROOT) not in sys.path:
    sys.path.insert(0, str(V7_ROOT))

from fl_tasks.score_v3_yardstick import diff_result_sets, render_diff  # noqa: E402

HASH_LOCK = {"status": "OK"}
IDENTITY = {
    "label": "test",
    "git_sha": "test-sha",
    "env": {"USE_V2_REGISTRY": "unset", "WIRED_OTEL": "unset"},
}


def _oracle_row(case_id: str, expected_fault_family: str) -> dict[str, str]:
    """Minimal oracle row for an accuracy case."""
    return {
        "case_id": case_id,
        "tag": "viable",
        "accuracy_excluded": "false",
        "expected_fault_family": expected_fault_family,
        "expected_state": "named_fault",
        "expected_fault_code": "",
        "expected_confidence_min": "",
        "expected_confidence_max": "",
        "expected_perception_gap": "",
        "expected_demotion_note_contains": "",
        "expected_crash_abort": "none",
    }


def _result_row(case_id: str, actual_fault_family: str, expected_fault_family: str) -> dict[str, Any]:
    """Minimal result row with dimensions already scored for the harness."""
    family_pass = actual_fault_family == expected_fault_family
    return {
        "case_id": case_id,
        "dimensions": {
            "fault_family": "PASS" if family_pass else "FAIL",
            "state": "PASS",
            "fault_code": "NA",
            "confidence": "NA",
            "perception_gap": "NA",
            "demotion_note_contains": "NA",
        },
        "verdict": {"fault_family": actual_fault_family, "state": "named_fault", "differential_siblings": []},
    }


def test_regression_detected() -> None:
    """A passing-before case that fails after is reported as a REGRESSION."""
    corpus_rows = [
        _oracle_row("CASE-PASS", "lean_condition"),
        _oracle_row("CASE-GAIN", "sensor_fault"),
    ]
    before_rows = [
        _result_row("CASE-PASS", "lean_condition", "lean_condition"),
        _result_row("CASE-GAIN", "lean_condition", "sensor_fault"),
    ]
    after_rows = [
        _result_row("CASE-PASS", "sensor_fault", "lean_condition"),
        _result_row("CASE-GAIN", "sensor_fault", "sensor_fault"),
    ]
    localization_modes = {
        "CASE-PASS": {"mode": "SURFACE_DEFECT"},
        "CASE-GAIN": {"mode": "OUTRANKED"},
    }

    diff = diff_result_sets(
        before_rows=before_rows,
        after_rows=after_rows,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
    )
    output = render_diff(diff, HASH_LOCK, IDENTITY, IDENTITY)

    assert diff["movement_counts"] == {"newly_pass": 1, "newly_fail": 1, "unchanged": 0}
    assert diff["regressions"] == ["CASE-PASS"]
    assert "REGRESSIONS: CASE-PASS" in output
    assert "PASS->SURFACE_DEFECT" in output
    assert "OUTRANKED->PASS" in output


def test_clean_after_reports_empty_regressions() -> None:
    """A clean after result reports no REGRESSIONS."""
    corpus_rows = [_oracle_row("CASE-STABLE", "lean_condition")]
    before_rows = [_result_row("CASE-STABLE", "lean_condition", "lean_condition")]
    after_rows = [_result_row("CASE-STABLE", "lean_condition", "lean_condition")]
    localization_modes = {"CASE-STABLE": {"mode": "SURFACE_DEFECT"}}

    diff = diff_result_sets(
        before_rows=before_rows,
        after_rows=after_rows,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
    )
    output = render_diff(diff, HASH_LOCK, IDENTITY, IDENTITY)

    assert diff["movement_counts"] == {"newly_pass": 0, "newly_fail": 0, "unchanged": 1}
    assert diff["regressions"] == []
    assert "REGRESSIONS: (empty)" in output
