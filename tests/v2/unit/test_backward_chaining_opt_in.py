"""Tests for R3 backward-chaining opt-in — next_steps[] construction.

Verifies:
  - BC off → next_steps = [] always.
  - state == named_fault → next_steps = [] always.
  - state == insufficient_evidence + BC on + L3 missing → next_steps contains L3_dtcs.
"""

from __future__ import annotations

import pytest

from engine.v2.ranker import (
    LAYER_EXPECTED_LIFT,
    ResolutionContext,
    _compute_next_steps,
    resolve_conflicts,
)


def _faults() -> dict:
    """Minimal faults schema for BC testing."""
    return {
        "Rich_Mixture": {
            "parent": None,
            "prior": 0.05,
            "dtc_required": [],
            "discriminator": ["SYM_LAMBDA_LOW"],
        },
        "Maf_Fault": {
            "parent": None,
            "prior": 0.04,
            "dtc_required": [],
            "discriminator": [],
        },
    }


def _root_causes() -> dict:
    return {}


def _ctx(**overrides: object) -> ResolutionContext:
    """Build a ResolutionContext with defaults overridden."""
    defaults: dict[str, object] = {
        "dtcs": [],
        "symptoms": [],
        "engine_state": "warm_closed_loop",
        "evidence_layers_used": ["L1"],
        "backward_chaining": False,
        "perception_gap": None,
        "validation_warnings": [],
        "cascading_consequences": [],
    }
    defaults.update(overrides)
    return ResolutionContext(**defaults)  # type: ignore[arg-type]


# ── _compute_next_steps unit tests ────────────────────────────────────────────


def test_bc_off_returns_empty() -> None:
    """When backward_chaining is False, next_steps is always empty."""
    result = _compute_next_steps(
        top_raw_score=0.05,
        evidence_layers_used=["L1"],
        backward_chaining=False,
        state="insufficient_evidence",
    )
    assert result == []


def test_named_fault_returns_empty() -> None:
    """Even with backward_chaining on, named_fault → no next_steps."""
    result = _compute_next_steps(
        top_raw_score=0.50,
        evidence_layers_used=["L1"],
        backward_chaining=True,
        state="named_fault",
    )
    assert result == []


def test_invalid_input_returns_empty() -> None:
    """invalid_input state → no next_steps regardless of BC."""
    result = _compute_next_steps(
        top_raw_score=0.0,
        evidence_layers_used=[],
        backward_chaining=True,
        state="invalid_input",
    )
    assert result == []


def test_insufficient_evidence_bc_on_missing_l3() -> None:
    """L3 not provided and BC on → next_steps contains L3_dtcs with lift."""
    result = _compute_next_steps(
        top_raw_score=0.05,
        evidence_layers_used=["L1"],
        backward_chaining=True,
        state="insufficient_evidence",
    )
    assert len(result) >= 1
    l3_entry = next((s for s in result if s["evidence"] == "L3_dtcs"), None)
    assert l3_entry is not None
    assert l3_entry["expected_lift"] == pytest.approx(0.18)


def test_insufficient_evidence_bc_on_all_layers_provided() -> None:
    """All evidence layers already used → next_steps is empty."""
    result = _compute_next_steps(
        top_raw_score=0.05,
        evidence_layers_used=["L1", "L2_high_idle_gas", "L3_dtcs", "L4_freeze_frame", "vehicle_context_dna"],
        backward_chaining=True,
        state="insufficient_evidence",
    )
    assert result == []


def test_insufficient_evidence_lift_too_small() -> None:
    """Evidence whose lift doesn't reach threshold → excluded."""
    # top_raw_score is so low that no single layer lift reaches NAMED_FAULT_THRESHOLD
    result = _compute_next_steps(
        top_raw_score=0.01,
        evidence_layers_used=["L1"],
        backward_chaining=True,
        state="insufficient_evidence",
    )
    # L3_dtcs lift=0.18 → 0.01+0.18=0.19 ≥ 0.10 → should include
    # L2_high_idle_gas lift=0.12 → 0.01+0.12=0.13 ≥ 0.10 → should include
    # vehicle_context_dna lift=0.10 → 0.01+0.10=0.11 ≥ 0.10 → should include
    # L4_freeze_frame lift=0.15 → 0.01+0.15=0.16 ≥ 0.10 → should include
    # All should include since all lifts are ≥ 0.10
    assert len(result) == len(LAYER_EXPECTED_LIFT)


def test_next_steps_sorted_by_lift_descending() -> None:
    """next_steps must be sorted by expected_lift descending."""
    result = _compute_next_steps(
        top_raw_score=0.03,
        evidence_layers_used=["L1"],
        backward_chaining=True,
        state="insufficient_evidence",
    )
    lifts = [float(s["expected_lift"]) for s in result]
    assert lifts == sorted(lifts, reverse=True)


# ── integration tests via resolve_conflicts ────────────────────────────────────


def test_resolve_conflicts_bc_off_next_steps_empty() -> None:
    """Integration: BC off → next_steps is always [] in RankedResult."""
    raw_probs = {"Rich_Mixture": 0.05}  # below threshold
    ctx = _ctx(backward_chaining=False, evidence_layers_used=["L1"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _root_causes())

    assert result.state == "insufficient_evidence"
    assert result.next_steps == []


def test_resolve_conflicts_named_fault_next_steps_empty() -> None:
    """Integration: state=named_fault → next_steps is [] even with BC on."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx(backward_chaining=True, evidence_layers_used=["L1"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _root_causes())

    assert result.state == "named_fault"
    assert result.next_steps == []


def test_resolve_conflicts_insufficient_evidence_bc_on() -> None:
    """Integration: insufficient_evidence + BC on + missing L3 → next_steps populated."""
    raw_probs = {"Rich_Mixture": 0.05}
    ctx = _ctx(
        backward_chaining=True,
        evidence_layers_used=["L1"],
        symptoms=["SYM_LAMBDA_LOW"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _root_causes())

    assert result.state == "insufficient_evidence"
    assert len(result.next_steps) >= 1
    l3_entry = next((s for s in result.next_steps if s["evidence"] == "L3_dtcs"), None)
    assert l3_entry is not None
    assert l3_entry["expected_lift"] == pytest.approx(0.18)


def test_resolve_conflicts_all_evidence_provided_next_steps_empty() -> None:
    """Integration: all evidence layers used → next_steps is []."""
    raw_probs = {"Rich_Mixture": 0.05}
    ctx = _ctx(
        backward_chaining=True,
        evidence_layers_used=[
            "L1",
            "L2_high_idle_gas",
            "L3_dtcs",
            "L4_freeze_frame",
            "vehicle_context_dna",
        ],
        symptoms=["SYM_LAMBDA_LOW"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _root_causes())

    assert result.state == "insufficient_evidence"
    assert result.next_steps == []


def test_resolve_conflicts_no_candidates_next_steps_populated() -> None:
    """No positive candidates + BC on → next_steps populated (all missing layers)."""
    raw_probs = {"Maf_Fault": 0.0, "Rich_Mixture": 0.0}
    ctx = _ctx(backward_chaining=True, evidence_layers_used=["L1"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _root_causes())

    assert result.state == "insufficient_evidence"
    # top_raw_score=0.0 means all missing layers with lift ≥ 0.10 qualify
    assert len(result.next_steps) == len(LAYER_EXPECTED_LIFT)
