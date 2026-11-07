"""T-COMA-11 (F-C1-10): after the prior / discriminator re-sort, the verdict's confidence is the named fault's own score.

Tags: NEW fails on the base (the new top rule's score was written into the verdict); PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

from v7.load_corpus import load_corpus
from wired.composition import diagnose

SCORED = [
    {"rule_id": "NS-001", "fault_family": "non_starter", "score": 0.95},
    {"rule_id": "MF-002", "fault_family": "misfire", "score": 0.90},
]


def test_score_of_the_named_rule_not_the_top():
    """NEW: the named rule's score is returned even when another rule now ranks first."""
    from comlab.core.fault_atlas_router import _reported_fault_score

    assert _reported_fault_score(SCORED, {"fault_code": "MF-002", "confidence_score": 0.5}) == 0.90


def test_falls_back_to_the_current_confidence():
    """NEW: a verdict whose rule is not in the ranking keeps its confidence."""
    from comlab.core.fault_atlas_router import _reported_fault_score

    assert _reported_fault_score(SCORED, {"fault_code": "XX-999", "confidence_score": 0.42}) == 0.42


@pytest.mark.parametrize(("case_id", "code", "confidence"), [("CASE-013", "LC-002", 0.96), ("CASE-016", "LC-002", 0.91)])
def test_corpus_case_reports_its_own_score(case_id, code, confidence):
    """NEW: two v7 corpus cases whose card showed another rule's 1.00 now show LC-002's own score."""
    raw = next(r for cid, r, *_ in load_corpus() if cid == case_id)
    v = diagnose(raw).diagnostic_verdict
    assert v.fault_code == code
    assert round(v.confidence_score, 4) == confidence
