"""Tests for ranker.py — known_issues prior boost tiebreaker.

Verifies that curated known_issues faults receive a sort-key boost
(_KNOWN_ISSUE_PRIOR_BOOST = 0.05) in Step 8 without changing raw_score
or confidence.
"""

from __future__ import annotations

from engine.v2.ranker import ResolutionContext, resolve_conflicts


def _basic_faults() -> dict:
    """Minimal faults for tiebreaker testing."""
    return {
        "Vacuum_Leak": {
            "parent": None,
            "prior": 0.10,
            "dtc_required": [],
            "discriminator": [],
        },
        "Maf_Fault": {
            "parent": None,
            "prior": 0.10,
            "dtc_required": [],
            "discriminator": [],
        },
    }


class TestKnownIssuesPriorBoost:
    """T-FX-6: known_issues tiebreaker sort nudge."""

    def test_known_issue_ranks_first_on_equal_score(self) -> None:
        """Two faults with equal raw_score — the known_issue fault ranks first."""
        raw_probs = {"Vacuum_Leak": 0.50, "Maf_Fault": 0.50}

        ctx = ResolutionContext(
            dtcs=[],
            symptoms=["SYM_LAMBDA_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L3"],
            known_issues=["Vacuum_Leak"],
        )

        result = resolve_conflicts(
            raw_probs, ctx, _basic_faults(), qualified_root_causes={},
        )

        assert result.primary is not None
        assert result.primary.fault_id == "Vacuum_Leak", (
            f"known-issue fault should rank first, got {result.primary.fault_id}"
        )

    def test_known_issue_does_not_change_raw_score(self) -> None:
        """Known-issue boost does NOT alter raw_score — only sort order."""
        raw_probs = {"Vacuum_Leak": 0.50, "Maf_Fault": 0.60}

        ctx = ResolutionContext(
            dtcs=[],
            symptoms=["SYM_LAMBDA_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L3"],
            known_issues=["Vacuum_Leak"],
        )

        result = resolve_conflicts(
            raw_probs, ctx, _basic_faults(), qualified_root_causes={},
        )

        assert result.primary is not None
        # Maf_Fault has higher raw_score (0.60 > 0.50), so it should still win
        # even though Vacuum_Leak is a known issue (boost is only 0.05).
        assert result.primary.fault_id == "Maf_Fault", (
            f"higher raw_score fault should win, got {result.primary.fault_id}"
        )
        assert result.primary.raw_score == 0.60

    def test_known_issue_empty_list_no_effect(self) -> None:
        """When known_issues is empty, ranking is unchanged."""
        raw_probs = {"Vacuum_Leak": 0.50, "Maf_Fault": 0.50}

        ctx = ResolutionContext(
            dtcs=[],
            symptoms=["SYM_LAMBDA_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L3"],
            known_issues=[],
        )

        result = resolve_conflicts(
            raw_probs, ctx, _basic_faults(), qualified_root_causes={},
        )

        assert result.primary is not None
        # With equal scores, equal priors, and no known_issues, sort falls back
        # to alphabetical fault_id tiebreak: "Maf_Fault" < "Vacuum_Leak"
        assert result.primary.fault_id == "Maf_Fault", (
            f"alphabetical tiebreak should pick Maf_Fault, got {result.primary.fault_id}"
        )

    def test_known_issue_not_in_candidates_ignored(self) -> None:
        """A known_issue entry not in raw_probs is silently ignored."""
        raw_probs = {"Maf_Fault": 0.50}

        ctx = ResolutionContext(
            dtcs=[],
            symptoms=["SYM_LAMBDA_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L3"],
            known_issues=["Timing_Chain_Stretch"],
        )

        result = resolve_conflicts(
            raw_probs, ctx, _basic_faults(), qualified_root_causes={},
        )

        assert result.primary is not None
        assert result.primary.fault_id == "Maf_Fault"
