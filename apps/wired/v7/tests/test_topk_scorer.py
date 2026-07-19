"""Tests for the v3 top-3 + abstain scorer metrics."""

from __future__ import annotations

import sys
from pathlib import Path

V7_ROOT = Path(__file__).resolve().parents[1]
if str(V7_ROOT) not in sys.path:
    sys.path.insert(0, str(V7_ROOT))

from fl_tasks.score_v3_yardstick import (  # noqa: E402
    build_identity,
    summarize,
)


def _oracle_row(
    case_id: str,
    expected_fault_family: str,
    expected_state: str = "named_fault",
) -> dict[str, str]:
    """Minimal oracle row for accuracy cases."""
    return {
        "case_id": case_id,
        "tag": "viable",
        "accuracy_excluded": "false",
        "expected_fault_family": expected_fault_family,
        "expected_state": expected_state,
        "expected_fault_code": "",
        "expected_confidence_min": "",
        "expected_confidence_max": "",
        "expected_perception_gap": "",
        "expected_demotion_note_contains": "",
        "expected_crash_abort": "none",
    }


def _result_row(
    case_id: str,
    actual_fault_family: str,
    expected_fault_family: str,
    actual_state: str = "named_fault",
    expected_state: str = "named_fault",
    differential_siblings: list[dict] | None = None,
    abstained: bool = False,
) -> dict:
    """Minimal diagnose() output row matching scoreboard expectations."""
    verdict = {
        "fault_family": actual_fault_family,
        "state": actual_state,
        "fault_code": "MF-001",
        "confidence_score": 0.0,
        "perception_gap": "NA",
        "demotion_note_contains": "NA",
        "is_fault_detected": actual_state != "insufficient_evidence",
        "abstained": abstained,
    }
    if differential_siblings is not None:
        verdict["differential_siblings"] = differential_siblings
    # Compute dimension outcomes (what the scoreboard expects in dimensions)
    family_pass = (actual_fault_family.lower() == expected_fault_family.lower())
    state_pass = (actual_state == expected_state)
    dimensions = {
        "fault_family": "PASS" if family_pass else "FAIL",
        "state": "PASS" if state_pass else "FAIL",
        "fault_code": "NA",
        "confidence": "NA",
        "perception_gap": "NA",
        "demotion_note_contains": "NA",
    }
    return {
        "case_id": case_id,
        "dimensions": dimensions,
        "verdict": verdict,
        "abstained": abstained,
    }


def test_top3_family_counts_runnerup() -> None:
    """A case whose winner family is WRONG but a differential sibling matches expected
    should PASS top3_family and FAIL single_verdict."""
    oracle_rows = [
        _oracle_row("CASE-TOP3-001", "lean_condition"),
    ]
    result_rows = [
        _result_row(
            "CASE-TOP3-001",
            actual_fault_family="sensor_fault",  # WRONG winner
            expected_fault_family="lean_condition",
            differential_siblings=[
                {"fault_id": "LC-001", "fault_name": "Lean Condition", "confidence_score": 0.85, "source": "runtime"},
                {"fault_id": "SF-002", "fault_name": "O2 Sensor Fault", "confidence_score": 0.90, "source": "runtime"},
            ],
        ),
    ]
    localization_modes = {"CASE-TOP3-001": {"mode": "OUTRANKED"}}
    corpus_rows = oracle_rows
    identity = build_identity("test-top3")
    summary = summarize(
        label="test",
        result_rows=result_rows,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
        identity=identity,
    )
    overall = summary["overall"]
    assert "top3_family_pass" in overall, "top3_family_pass metric missing"
    assert "top3_family_pct" in overall, "top3_family_pct metric missing"
    assert overall["primary_pass"] == 0, "single_verdict should FAIL (wrong winner)"
    assert overall["top3_family_pass"] == 1, "top3_family should PASS (sibling matches)"


def test_top3_family_counts_distinct_families() -> None:
    """T-V3-D6-SCORERWIN: the top-3 window counts three DISTINCT families, not the
    first two sibling entries. A same-family duplicate in an early slot must not crowd
    out a genuine top-3 hit. Siblings [misfire, misfire, lean_condition] with winner
    misfire and expected lean_condition must PASS (it FAILS under the old [:2] logic,
    which sees only {misfire})."""
    oracle_rows = [
        _oracle_row("CASE-DISTINCT-001", "lean_condition"),
    ]
    result_rows = [
        _result_row(
            "CASE-DISTINCT-001",
            actual_fault_family="misfire",  # winner
            expected_fault_family="lean_condition",
            differential_siblings=[
                {"fault_id": "MF-002", "fault_family": "misfire", "confidence_score": 0.80, "source": "runtime"},
                {"fault_id": "MF-003", "fault_family": "misfire", "confidence_score": 0.75, "source": "runtime"},
                {"fault_id": "LC-001", "fault_family": "lean_condition", "confidence_score": 0.70, "source": "runtime"},
            ],
        ),
    ]
    localization_modes = {"CASE-DISTINCT-001": {"mode": "OUTRANKED"}}
    corpus_rows = oracle_rows
    identity = build_identity("test-distinct")
    summary = summarize(
        label="test",
        result_rows=result_rows,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
        identity=identity,
    )
    overall = summary["overall"]
    assert overall["primary_pass"] == 0, "single_verdict should FAIL (wrong winner)"
    assert overall["top3_family_pass"] == 1, (
        "top3_family should PASS: the distinct-family window is "
        "{misfire, lean_condition}, not just {misfire} from the first two entries"
    )


def test_abstain_not_counted_wrong() -> None:
    """An abstained case counts against coverage, is excluded from top3_on_covered,
    and is never scored as a wrong family."""
    oracle_rows = [
        _oracle_row("CASE-ABSTAIN-001", "lean_condition"),
        _oracle_row("CASE-ABSTAIN-002", "lean_condition"),
    ]
    result_rows = [
        _result_row(
            "CASE-ABSTAIN-001",
            actual_fault_family="lean_condition",
            expected_fault_family="lean_condition",
            differential_siblings=[],
        ),
        _result_row(
            "CASE-ABSTAIN-002",
            actual_fault_family="sensor_fault",  # WRONG
            expected_fault_family="lean_condition",
            differential_siblings=[],  # no siblings to save it
            abstained=True,
        ),
    ]
    localization_modes = {
        "CASE-ABSTAIN-001": {"mode": "SURFACE_DEFECT"},
        "CASE-ABSTAIN-002": {"mode": "DATA_GAP"},
    }
    corpus_rows = oracle_rows
    identity = build_identity("test-abstain")
    summary = summarize(
        label="test",
        result_rows=result_rows,
        corpus_rows=corpus_rows,
        localization_modes=localization_modes,
        identity=identity,
    )
    overall = summary["overall"]
    # Implementation must add these metrics
    assert "coverage" in overall, "coverage metric missing"
    assert "top3_on_covered_pass" in overall, "top3_on_covered_pass metric missing"
    assert "top3_on_covered_pct" in overall, "top3_on_covered_pct metric missing"
    assert "total_abstained" in overall, "total_abstained metric missing"
    # Coverage = non-abstained / total = 1/2 = 0.5
    assert overall["coverage"] == 0.5
    # top3_on_covered only counts the non-abstained case
    assert overall["top3_on_covered_pass"] == 1
    assert overall["top3_on_covered_pct"] == 100.0
    assert overall["total_abstained"] == 1
    # The abstained case should not count as a wrong family in primary metrics
    assert overall["primary_pass"] == 1
    assert overall["family_pass"] == 1



def test_synthetic_split_reconciles_with_top3(monkeypatch) -> None:
    """T-SHIP-2: banked_real + banked_synthetic must equal top3_family_pass."""
    import fl_tasks.score_v3_yardstick as sv

    monkeypatch.setattr(sv, "load_rule_family_map", lambda: {})
    monkeypatch.setattr(sv, "load_synthetic_case_ids", lambda: {"C2": {"case_b"}})
    corpus = [_oracle_row("case_a", "misfire"), _oracle_row("case_b", "rich_mixture")]
    results = [
        {
            "case_id": "case_a",
            "dimensions": {"fault_family": "PASS", "state": "PASS"},
            "verdict": {"fault_family": "misfire", "differential_siblings": [], "abstained": False},
        },
        {
            "case_id": "case_b",
            "dimensions": {"fault_family": "PASS", "state": "PASS"},
            "verdict": {"fault_family": "rich_mixture", "differential_siblings": [], "abstained": False},
        },
    ]
    modes = {"case_a": {"mode": "OUTRANKED"}, "case_b": {"mode": "OUTRANKED"}}
    summary = sv.summarize(
        label="t", result_rows=results, corpus_rows=corpus,
        localization_modes=modes, identity={"label": "t"},
    )
    overall = summary["overall"]
    assert overall["top3_family_pass"] == 2
    assert overall["top3_banked_real"] == 1
    assert overall["top3_banked_synthetic"] == 1
    assert overall["top3_banked_synthetic_by_cluster"] == {"C2": 1}
    assert overall["top3_banked_real"] + overall["top3_banked_synthetic"] == overall["top3_family_pass"]
