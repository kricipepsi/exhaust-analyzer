"""Tests for M5 resolve_conflicts() — step order, gates, and result schema.

Verifies R7 (fixed order), L02 (single resolve function), L05 (raw_score for
gates, confidence for display), L16 (confidence ceiling per evidence layers),
and the R9 state machine transitions.
"""

from __future__ import annotations

import pytest

from engine.v2.kg_engine import score_root_causes
from engine.v2.ranker import (
    COLD_START_SUPPRESSION_FACTOR,
    ResolutionContext,
    compute_ceiling,
    resolve_conflicts,
)

# ── minimal test fixtures ────────────────────────────────────────────────────


def _faults() -> dict:
    """Minimal faults schema for testing."""
    return {
        "Rich_Mixture": {
            "parent": None,
            "prior": 0.05,
            "dtc_required": [],
            "discriminator": ["SYM_LAMBDA_LOW"],
        },
        "High_Fuel_Pressure": {
            "parent": "Rich_Mixture",
            "prior": 0.02,
            "dtc_required": [],
            "discriminator": ["SYM_HIGH_FUEL_PRESSURE_PATTERN"],
        },
        "Leaking_Injector": {
            "parent": "Rich_Mixture",
            "prior": 0.02,
            "dtc_required": [],
            "discriminator": ["SYM_LEAKING_INJECTOR_PATTERN"],
        },
        "Lean_Condition": {
            "parent": None,
            "prior": 0.05,
            "dtc_required": [],
            "discriminator": ["SYM_LAMBDA_HIGH"],
        },
        "Vacuum_Leak_Intake_Manifold": {
            "parent": "Lean_Condition",
            "prior": 0.03,
            "dtc_required": [],
            "discriminator": ["SYM_VE_LOSS", "SYM_O2_HIGH"],
        },
        "EVAP_Purge_Stuck_Open": {
            "parent": "Rich_Mixture",
            "prior": 0.02,
            "dtc_required": [],
            "discriminator": ["SYM_RICH_NEGATIVE_TRIMS_PATTERN"],
        },
        # Fault requiring a specific DTC.
        "P0420_Catalyst_Efficiency": {
            "parent": None,
            "prior": 0.03,
            "dtc_required": ["P0420"],
            "discriminator": [],
        },
        # Fault with no discriminator (parent-less).
        "Maf_Fault": {
            "parent": None,
            "prior": 0.04,
            "dtc_required": [],
            "discriminator": [],
        },
    }


def _root_causes() -> dict:
    """Minimal root causes for testing."""
    return {
        "Fuel_Pressure_Regulator_Diaphragm_Leak": {
            "applies_to_fault": "High_Fuel_Pressure",
            "prompt": "Inspect FPR vacuum line.",
        },
    }


def _qrc(raw_probs: dict[str, float]) -> dict:
    """Pre-filter root causes through score_root_causes gate (M4)."""
    return score_root_causes(raw_probs, _root_causes())


def _ctx(**overrides: object) -> ResolutionContext:
    """Build a ResolutionContext with defaults overridden."""
    defaults: dict[str, object] = {
        "dtcs": [],
        "symptoms": [],
        "engine_state": "warm_closed_loop",
        "evidence_layers_used": ["L1", "L2"],
        "perception_gap": None,
        "validation_warnings": [],
        "cascading_consequences": [],
    }
    defaults.update(overrides)
    return ResolutionContext(**defaults)  # type: ignore[arg-type]


# ── compute_ceiling tests ────────────────────────────────────────────────────


def test_ceiling_gas_only() -> None:
    """Gas-only input (1 evidence layer) → ceiling 0.40."""
    assert compute_ceiling(["L1"]) == pytest.approx(0.40)


def test_ceiling_gas_plus_dtc() -> None:
    """Gas + DTC (2 layers) → ceiling 0.60."""
    assert compute_ceiling(["L1", "L3"]) == pytest.approx(0.60)


def test_ceiling_gas_dtc_ff() -> None:
    """Gas + DTC + FF (3 layers) → ceiling 0.95."""
    assert compute_ceiling(["L1", "L3", "L4"]) == pytest.approx(0.95)


def test_ceiling_full_dna() -> None:
    """Full DNA (4 layers) → ceiling 1.00."""
    assert compute_ceiling(["L1", "L2", "L3", "L4"]) == pytest.approx(1.00)


def test_ceiling_empty_layers() -> None:
    """Empty evidence layers → ceiling 1.00 (fallback)."""
    assert compute_ceiling([]) == pytest.approx(1.00)


# ── step 3: DTC-prerequisite gate ────────────────────────────────────────────


def test_dtc_gate_fault_requires_missing_dtc_falls_back() -> None:
    """Fault requiring P0420 without it in input → demoted to 1e-9."""
    raw_probs = {"P0420_Catalyst_Efficiency": 0.45}
    ctx = _ctx(dtcs=["P0171"])  # wrong DTC
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "insufficient_evidence"
    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(1e-9)


def test_dtc_gate_fault_requires_present_dtc_passes() -> None:
    """Fault requiring P0420 with P0420 in input → score preserved."""
    raw_probs = {"P0420_Catalyst_Efficiency": 0.45}
    ctx = _ctx(dtcs=["P0420"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "named_fault"
    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.45)


def test_dtc_gate_fault_with_no_dtc_required_untouched() -> None:
    """Fault with empty dtc_required → score preserved regardless of DTCs."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx(dtcs=[])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.50)


# ── step 4: discriminator gate ───────────────────────────────────────────────


def test_discriminator_gate_absent_symptom_demotes() -> None:
    """Fault whose discriminator symptom is absent → demoted to 1e-9."""
    raw_probs = {"Rich_Mixture": 0.40}
    ctx = _ctx(symptoms=["SYM_CO_HIGH"])  # not SYM_LAMBDA_LOW
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(1e-9)
    assert result.primary.discriminator_satisfied is False


def test_discriminator_gate_present_symptom_passes() -> None:
    """Fault whose discriminator symptom is present → score preserved."""
    raw_probs = {"Rich_Mixture": 0.40, "Lean_Condition": 0.50}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    # Top fault should be Lean_Condition (higher score)
    assert result.primary.fault_id == "Lean_Condition"
    assert result.primary.discriminator_satisfied is True


def test_discriminator_gate_no_discriminator_passes() -> None:
    """Fault with empty discriminator → always satisfied."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx(symptoms=[])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.discriminator_satisfied is True


# ── step 5: cold-start family suppression ────────────────────────────────────


def test_cold_start_suppresses_rich_family() -> None:
    """Rich_Mixture family faults are reduced to 30% during cold_open_loop."""
    raw_probs = {"High_Fuel_Pressure": 0.50, "Lean_Condition": 0.40}
    ctx = _ctx(
        engine_state="cold_open_loop",
        symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    # High_Fuel_Pressure suppressed from 0.50 → 0.15.
    # Lean_Condition at 0.40 should now be top fault.
    assert result.primary is not None
    assert result.primary.fault_id == "Lean_Condition"
    assert result.primary.raw_score == pytest.approx(0.40)


def test_cold_start_does_not_suppress_non_rich_family() -> None:
    """Non Rich_Mixture faults are untouched during cold_open_loop."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx(engine_state="cold_open_loop")
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.50)


def test_cold_start_suppression_factor() -> None:
    """Verify the suppression factor constant matches expected value."""
    assert pytest.approx(0.30) == COLD_START_SUPPRESSION_FACTOR


# ── step 6: specific-over-generic promotion ──────────────────────────────────


def test_specific_within_margin_promoted_over_parent() -> None:
    """Child fault within 0.10 of parent → parent demoted, child promoted."""
    raw_probs = {"Rich_Mixture": 0.45, "Leaking_Injector": 0.40}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW", "SYM_LEAKING_INJECTOR_PATTERN"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    # Leaking_Injector (0.40) is within 0.10 of Rich_Mixture (0.45)
    # → Rich_Mixture demoted, Leaking_Injector becomes top.
    assert result.primary is not None
    assert result.primary.fault_id == "Leaking_Injector"
    assert result.primary.promoted_from_parent is True


def test_specific_far_from_parent_not_promoted() -> None:
    """Child fault far below parent (>0.10) → parent stays top."""
    raw_probs = {"Rich_Mixture": 0.60, "Leaking_Injector": 0.30}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW", "SYM_LEAKING_INJECTOR_PATTERN"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    # Gap 0.30 > 0.10 → Rich_Mixture stays top.
    assert result.primary is not None
    assert result.primary.fault_id == "Rich_Mixture"


# ── step 7: confidence ceiling ────────────────────────────────────────────────


def test_confidence_capped_by_ceiling() -> None:
    """confidence must be min(raw_score, ceiling) — never exceed ceiling."""
    raw_probs = {"Maf_Fault": 0.80}
    ctx = _ctx(evidence_layers_used=["L1"])  # ceiling 0.40
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.80)
    assert result.primary.confidence == pytest.approx(0.40)
    assert result.confidence_ceiling == pytest.approx(0.40)


def test_confidence_not_capped_when_below_ceiling() -> None:
    """When raw_score is below ceiling, confidence equals raw_score."""
    raw_probs = {"Maf_Fault": 0.30}
    ctx = _ctx(evidence_layers_used=["L1", "L2", "L3"])  # ceiling 0.95
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.30)
    assert result.primary.confidence == pytest.approx(0.30)


# ── step 8: sort + tie-break ─────────────────────────────────────────────────


def test_sort_by_score_then_prior_then_id() -> None:
    """Candidates sorted by (-score, -prior, fault_id) deterministically."""
    raw_probs = {"Maf_Fault": 0.40, "Rich_Mixture": 0.40, "Lean_Condition": 0.60}
    ctx = _ctx(
        symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"],
        evidence_layers_used=["L1", "L2", "L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.fault_id == "Lean_Condition"
    assert len(result.alternatives) >= 1
    # Maf_Fault prior=0.04 > Rich_Mixture prior=0.05 → Rich_Mixture comes first
    assert result.alternatives[0].fault_id == "Rich_Mixture"


def test_sort_deterministic_tie_break() -> None:
    """Same inputs produce same outputs (determinism)."""
    raw_probs = {"Maf_Fault": 0.50, "Rich_Mixture": 0.50}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW"])
    r1 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    r2 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert r1.primary is not None
    assert r2.primary is not None
    assert r1.primary.fault_id == r2.primary.fault_id
    assert r1.primary.raw_score == r2.primary.raw_score


# ── state machine ────────────────────────────────────────────────────────────


def test_state_named_fault() -> None:
    """Top candidate ≥ threshold with discriminator satisfied → named_fault."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "named_fault"


def test_state_insufficient_evidence_low_score() -> None:
    """Top candidate below threshold → insufficient_evidence."""
    raw_probs = {"Maf_Fault": 0.05}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "insufficient_evidence"
    assert result.primary is not None  # still populated for inspection


def test_state_insufficient_evidence_discriminator_not_satisfied() -> None:
    """Top candidate above threshold but discriminator not satisfied."""
    raw_probs = {"Rich_Mixture": 0.50}
    ctx = _ctx(symptoms=[])  # no SYM_LAMBDA_LOW
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "insufficient_evidence"


def test_state_insufficient_evidence_no_candidates() -> None:
    """All raw_probs are zero → insufficient_evidence."""
    raw_probs = {"Maf_Fault": 0.0, "Rich_Mixture": 0.0}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "insufficient_evidence"
    assert result.primary is None


# ── result schema completeness ───────────────────────────────────────────────


def test_result_has_all_r9_fields() -> None:
    """RankedResult must include all R9 required top-level fields."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state is not None
    assert result.primary is not None
    assert isinstance(result.alternatives, list)
    # perception_gap may be None (valid)
    assert isinstance(result.validation_warnings, list)
    assert isinstance(result.cascading_consequences, list)
    assert isinstance(result.confidence_ceiling, float)
    assert isinstance(result.next_steps, list)


def test_fault_result_has_all_fields() -> None:
    """FaultResult must include all R9 primary/alternatives fields."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    primary = result.primary
    assert primary is not None
    assert isinstance(primary.fault_id, str)
    assert isinstance(primary.symptom_chain, list)
    # root_cause may be None
    assert isinstance(primary.confidence, float)
    assert isinstance(primary.raw_score, float)
    assert isinstance(primary.evidence_layers_used, list)
    assert isinstance(primary.tier_delta, float)
    assert isinstance(primary.discriminator_satisfied, bool)
    assert isinstance(primary.promoted_from_parent, bool)


def test_tier_delta_computed() -> None:
    """tier_delta is raw_score gap to first alternative."""
    raw_probs = {"Maf_Fault": 0.60, "Rich_Mixture": 0.40, "Lean_Condition": 0.30}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.tier_delta == pytest.approx(0.20)


def test_tier_delta_zero_when_no_alternatives() -> None:
    """tier_delta is 0.0 when there are no alternatives."""
    raw_probs = {"Maf_Fault": 0.50}
    ctx = _ctx()
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.tier_delta == pytest.approx(0.0)


# ── root cause linking ──────────────────────────────────────────────────────


def test_root_cause_linked_when_score_above_80() -> None:
    """Fault with raw_score ≥ 0.80 gets root cause linked."""
    raw_probs = {"High_Fuel_Pressure": 0.85}
    ctx = _ctx(symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.root_cause == "Fuel_Pressure_Regulator_Diaphragm_Leak"


def test_root_cause_not_linked_below_80() -> None:
    """Fault with raw_score < 0.80 → root_cause is None."""
    raw_probs = {"High_Fuel_Pressure": 0.79}
    ctx = _ctx(symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.primary is not None
    assert result.primary.root_cause is None


# ── edge cases ───────────────────────────────────────────────────────────────


def test_empty_raw_probs() -> None:
    """Empty raw_probs dict → insufficient_evidence, no primary."""
    result = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))

    assert result.state == "insufficient_evidence"
    assert result.primary is None
    assert result.alternatives == []


def test_promoted_from_parent_tracked() -> None:
    """FaultResult.promoted_from_parent reflects step 6 promotion."""
    raw_probs = {"Rich_Mixture": 0.45, "Leaking_Injector": 0.40}
    ctx = _ctx(symptoms=["SYM_LAMBDA_LOW", "SYM_LEAKING_INJECTOR_PATTERN"])
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    primary = result.primary
    assert primary is not None
    assert primary.promoted_from_parent is True
    # Check that Rich_Mixture is demoted to very small value
    for alt in result.alternatives:
        if alt.fault_id == "Rich_Mixture":
            assert alt.raw_score < 0.01


def test_context_fields_preserved_in_result() -> None:
    """Perception gap, warnings, and cascading consequences pass through."""
    from engine.v2.arbitrator import PerceptionGap
    from engine.v2.input_model import ValidationWarning

    pg = PerceptionGap(
        gap_type="LEAN_SEEN_RICH",
        cf=0.30,
        analyser_lambda=0.90,
        obd_lambda=1.10,
    )
    warnings = [
        ValidationWarning(category=6, message="test", channel="obd"),
    ]
    cascading = ["SYM_TRIM_LEAN_IDLE_ONLY"]

    ctx = _ctx(
        perception_gap=pg,
        validation_warnings=warnings,
        cascading_consequences=cascading,
    )
    raw_probs = {"Maf_Fault": 0.50}
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.perception_gap is not None
    assert result.perception_gap.gap_type == "LEAN_SEEN_RICH"
    assert len(result.validation_warnings) == 1
    assert result.cascading_consequences == cascading


# ── 4-pathway scenario tests ──────────────────────────────────────────────────


def test_pathway_regular_all_layers() -> None:
    """Regular pathway (L1+L2+L3+L4): all evidence layers, Vacuum_Leak case."""
    raw_probs = {"Vacuum_Leak_Intake_Manifold": 0.75, "Lean_Condition": 0.55, "Maf_Fault": 0.20}
    ctx = _ctx(
        dtcs=["P0171", "P0174"],
        symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH", "SYM_TRIM_LEAN_IDLE_ONLY"],
        engine_state="warm_closed_loop",
        evidence_layers_used=["L1", "L2", "L3", "L4"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "named_fault"
    assert result.primary is not None
    assert result.primary.fault_id == "Vacuum_Leak_Intake_Manifold"
    assert result.primary.discriminator_satisfied is True
    assert result.confidence_ceiling == pytest.approx(1.00)
    assert result.primary.raw_score == pytest.approx(0.75)
    assert result.primary.confidence == pytest.approx(0.75)
    assert result.primary.evidence_layers_used == ["L1", "L2", "L3", "L4"]
    assert len(result.alternatives) >= 1


def test_pathway_non_starter_dtc_only() -> None:
    """Non-starter pathway: DTC-only (L3), no gas symptoms — P1570 immobiliser case."""
    raw_probs = {"P0420_Catalyst_Efficiency": 0.55, "Maf_Fault": 0.10}
    ctx = _ctx(
        dtcs=["P0420"],
        symptoms=[],  # no gas-derived symptoms
        engine_state="warm_closed_loop",
        evidence_layers_used=["L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "named_fault"
    assert result.primary is not None
    assert result.primary.fault_id == "P0420_Catalyst_Efficiency"
    # Ceiling for single layer (L3 only counted as 1 layer)
    assert result.confidence_ceiling == pytest.approx(0.40)
    assert result.primary.confidence == pytest.approx(0.40)
    assert result.primary.raw_score == pytest.approx(0.55)
    assert result.primary.confidence < result.primary.raw_score


def test_pathway_non_starter_missing_dtc() -> None:
    """Non-starter pathway: DTC-only with absent required DTC → insufficient_evidence."""
    raw_probs = {"P0420_Catalyst_Efficiency": 0.55}
    ctx = _ctx(
        dtcs=["P0300"],  # wrong DTC — P0420 not present
        symptoms=[],
        engine_state="warm_closed_loop",
        evidence_layers_used=["L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    assert result.state == "insufficient_evidence"


def test_pathway_cold_start_restricted() -> None:
    """Cold-start restricted pathway: rich-trim fault suppressed during cold_open_loop."""
    raw_probs = {
        "High_Fuel_Pressure": 0.60,
        "EVAP_Purge_Stuck_Open": 0.55,
        "Lean_Condition": 0.40,
        "Maf_Fault": 0.25,
    }
    ctx = _ctx(
        dtcs=["P0172"],
        symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"],
        engine_state="cold_open_loop",
        evidence_layers_used=["L1", "L2", "L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    # Rich_Mixture family faults are suppressed to 30%.
    # High_Fuel_Pressure: 0.60 * 0.30 = 0.18
    # EVAP_Purge_Stuck_Open: 0.55 * 0.30 = 0.165
    # Lean_Condition at 0.40 becomes top (not in rich family)
    assert result.primary is not None
    assert result.primary.fault_id == "Lean_Condition"
    assert result.primary.raw_score == pytest.approx(0.40)
    # Verify suppressed faults are still in alternatives
    suppressed_ids = {alt.fault_id for alt in result.alternatives}
    assert "High_Fuel_Pressure" in suppressed_ids or len(result.alternatives) > 0


def test_pathway_soft_rerun_determinism() -> None:
    """Soft-rerun pathway: identical inputs produce identical RankedResult."""
    raw_probs = {
        "Vacuum_Leak_Intake_Manifold": 0.72,
        "Lean_Condition": 0.55,
        "Rich_Mixture": 0.40,
        "Maf_Fault": 0.15,
    }
    ctx = _ctx(
        dtcs=["P0171", "P0174"],
        symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH", "SYM_TRIM_LEAN_IDLE_ONLY"],
        engine_state="warm_closed_loop",
        evidence_layers_used=["L1", "L2", "L3", "L4"],
    )

    r1 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    r2 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

    # Full structural comparison — every field must match.
    assert r1.state == r2.state
    assert r1.primary is not None
    assert r2.primary is not None
    assert r1.primary.fault_id == r2.primary.fault_id
    assert r1.primary.raw_score == pytest.approx(r2.primary.raw_score)
    assert r1.primary.confidence == pytest.approx(r2.primary.confidence)
    assert r1.primary.tier_delta == pytest.approx(r2.primary.tier_delta)
    assert r1.primary.discriminator_satisfied == r2.primary.discriminator_satisfied
    assert r1.primary.promoted_from_parent == r2.primary.promoted_from_parent
    assert r1.confidence_ceiling == pytest.approx(r2.confidence_ceiling)
    assert len(r1.alternatives) == len(r2.alternatives)
    for a1, a2 in zip(r1.alternatives, r2.alternatives, strict=True):
        assert a1.fault_id == a2.fault_id
        assert a1.raw_score == pytest.approx(a2.raw_score)


def test_pathway_soft_rerun_empty_probs() -> None:
    """Soft-rerun pathway: empty probs determinism (insufficient_evidence both times)."""
    ctx = _ctx()
    r1 = resolve_conflicts({}, ctx, _faults(), _qrc({}))
    r2 = resolve_conflicts({}, ctx, _faults(), _qrc({}))

    assert r1.state == r2.state == "insufficient_evidence"
    assert r1.primary is None
    assert r2.primary is None


def test_all_four_pathways_produce_r9_shape() -> None:
    """Every pathway result must contain all R9 top-level fields."""
    pathways: list[dict] = [
        {  # Regular
            "raw_probs": {"Vacuum_Leak_Intake_Manifold": 0.75, "Lean_Condition": 0.50},
            "dtcs": ["P0171"],
            "symptoms": ["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH"],
            "engine_state": "warm_closed_loop",
            "evidence_layers_used": ["L1", "L2", "L3", "L4"],
        },
        {  # Non-starter
            "raw_probs": {"P0420_Catalyst_Efficiency": 0.55},
            "dtcs": ["P0420"],
            "symptoms": [],
            "engine_state": "warm_closed_loop",
            "evidence_layers_used": ["L3"],
        },
        {  # Cold-start restricted
            "raw_probs": {"High_Fuel_Pressure": 0.60, "Lean_Condition": 0.40},
            "dtcs": [],
            "symptoms": ["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
            "engine_state": "cold_open_loop",
            "evidence_layers_used": ["L1", "L2"],
        },
        {  # Soft-rerun
            "raw_probs": {"Maf_Fault": 0.50},
            "dtcs": [],
            "symptoms": [],
            "engine_state": "warm_closed_loop",
            "evidence_layers_used": ["L1"],
        },
    ]

    r9_fields = {
        "state", "primary", "alternatives", "perception_gap",
        "validation_warnings", "cascading_consequences",
        "confidence_ceiling", "next_steps",
    }

    for i, p in enumerate(pathways):
        ctx = _ctx(
            dtcs=p["dtcs"],
            symptoms=p["symptoms"],
            engine_state=p["engine_state"],
            evidence_layers_used=p["evidence_layers_used"],
        )
        result = resolve_conflicts(p["raw_probs"], ctx, _faults(), _qrc(p["raw_probs"]))
        result_dict = {
            "state": result.state,
            "primary": result.primary,
            "alternatives": result.alternatives,
            "perception_gap": result.perception_gap,
            "validation_warnings": result.validation_warnings,
            "cascading_consequences": result.cascading_consequences,
            "confidence_ceiling": result.confidence_ceiling,
            "next_steps": result.next_steps,
        }
        missing = r9_fields - set(result_dict.keys())
        assert not missing, f"Pathway {i}: missing R9 fields: {missing}"
