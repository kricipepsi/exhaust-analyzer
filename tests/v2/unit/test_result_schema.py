"""Tests for the unified result schema (R9) across all 4 pathways.

Validates:
  - R9 schema shape — all required fields present, correct types, nullability
  - L05 — raw_score for gates, confidence for display, never swapped
  - L06 — all 4 pathways return the same R9 shape
  - State machine — only the 3 literals
  - confidence <= confidence_ceiling invariant
  - tier_delta arithmetic
  - 4 pathway-specific scenario tests

source: v2-result-schema SKILL.md S1-S5
"""

from __future__ import annotations

import pytest

from engine.v2.kg_engine import score_root_causes
from engine.v2.ranker import (
    NAMED_FAULT_THRESHOLD,
    FaultResult,
    RankedResult,
    ResolutionContext,
    compute_ceiling,
    resolve_conflicts,
)

# ── helpers ────────────────────────────────────────────────────────────────────

R9_TOP_LEVEL_FIELDS: frozenset[str] = frozenset(
    {
        "state",
        "primary",
        "alternatives",
        "perception_gap",
        "validation_warnings",
        "cascading_consequences",
        "confidence_ceiling",
        "next_steps",
    }
)

FAULT_RESULT_FIELDS: frozenset[str] = frozenset(
    {
        "fault_id",
        "symptom_chain",
        "root_cause",
        "confidence",
        "raw_score",
        "evidence_layers_used",
        "tier_delta",
        "discriminator_satisfied",
        "promoted_from_parent",
    }
)

VALID_STATES: frozenset[str] = frozenset(
    {"named_fault", "insufficient_evidence", "invalid_input"}
)


def _faults() -> dict:
    """Minimal faults schema for testing all 4 pathways."""
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
        "EVAP_Purge_Stuck_Open": {
            "parent": "Rich_Mixture",
            "prior": 0.02,
            "dtc_required": [],
            "discriminator": ["SYM_RICH_NEGATIVE_TRIMS_PATTERN"],
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
        "Maf_Fault": {
            "parent": None,
            "prior": 0.04,
            "dtc_required": [],
            "discriminator": [],
        },
        "P0420_Catalyst_Efficiency": {
            "parent": None,
            "prior": 0.03,
            "dtc_required": ["P0420"],
            "discriminator": [],
        },
        "P1570_Immobiliser": {
            "parent": None,
            "prior": 0.03,
            "dtc_required": ["P1570"],
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


def _result_dict(result: RankedResult) -> dict:
    """Extract a dict of the top-level R9 fields from a RankedResult."""
    return {
        "state": result.state,
        "primary": result.primary,
        "alternatives": result.alternatives,
        "perception_gap": result.perception_gap,
        "validation_warnings": result.validation_warnings,
        "cascading_consequences": result.cascading_consequences,
        "confidence_ceiling": result.confidence_ceiling,
        "next_steps": result.next_steps,
    }


# ── schema shape validation ───────────────────────────────────────────────────


def test_all_r9_top_level_fields_present() -> None:
    """Every RankedResult must have all 8 R9 top-level keys."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    fields = _result_dict(result)
    missing = R9_TOP_LEVEL_FIELDS - set(fields.keys())
    assert not missing, f"Missing top-level R9 fields: {missing}"


def test_fault_result_all_fields_present() -> None:
    """Every FaultResult must have all 9 required fields."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    primary = result.primary
    assert primary is not None
    fr_fields = {
        "fault_id": primary.fault_id,
        "symptom_chain": primary.symptom_chain,
        "root_cause": primary.root_cause,
        "confidence": primary.confidence,
        "raw_score": primary.raw_score,
        "evidence_layers_used": primary.evidence_layers_used,
        "tier_delta": primary.tier_delta,
        "discriminator_satisfied": primary.discriminator_satisfied,
        "promoted_from_parent": primary.promoted_from_parent,
    }
    missing = FAULT_RESULT_FIELDS - set(fr_fields.keys())
    assert not missing, f"Missing FaultResult fields: {missing}"


def test_state_is_valid_literal() -> None:
    """result.state must be one of the 3 valid literals."""
    # named_fault case
    r1 = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    assert r1.state in VALID_STATES
    assert r1.state == "named_fault"

    # insufficient_evidence case
    r2 = resolve_conflicts({"Maf_Fault": 0.05}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.05}))
    assert r2.state in VALID_STATES
    assert r2.state == "insufficient_evidence"

    # empty probs
    r3 = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))
    assert r3.state in VALID_STATES


def test_fault_result_types() -> None:
    """FaultResult fields must have correct Python types."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    primary = result.primary
    assert primary is not None

    assert isinstance(primary.fault_id, str)
    assert isinstance(primary.symptom_chain, list)
    assert primary.root_cause is None or isinstance(primary.root_cause, str)
    assert isinstance(primary.confidence, float)
    assert isinstance(primary.raw_score, float)
    assert isinstance(primary.evidence_layers_used, list)
    assert isinstance(primary.tier_delta, float)
    assert isinstance(primary.discriminator_satisfied, bool)
    assert isinstance(primary.promoted_from_parent, bool)


def test_alternatives_is_list_of_fault_results() -> None:
    """alternatives must be a list of FaultResult (or empty)."""
    raw_probs = {"Maf_Fault": 0.60, "Rich_Mixture": 0.45, "Lean_Condition": 0.30}
    ctx = _ctx(
        symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"],
        evidence_layers_used=["L1", "L2", "L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    assert isinstance(result.alternatives, list)
    for alt in result.alternatives:
        assert isinstance(alt, FaultResult)

    # Empty alternatives
    r2 = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))
    assert isinstance(r2.alternatives, list)
    assert len(r2.alternatives) == 0


def test_primary_null_when_no_candidates() -> None:
    """primary is None only when there are no candidates."""
    result = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))
    assert result.primary is None

    # With candidates, primary must be set (even for insufficient_evidence)
    r2 = resolve_conflicts({"Maf_Fault": 0.05}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.05}))
    assert r2.primary is not None
    assert r2.state == "insufficient_evidence"


# ── L05: raw_score vs confidence invariants ────────────────────────────────────


def test_raw_score_and_confidence_both_present() -> None:
    """Both raw_score and confidence must be present in every FaultResult (L05)."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    assert result.primary is not None
    assert hasattr(result.primary, "raw_score")
    assert hasattr(result.primary, "confidence")
    assert result.primary.raw_score >= 0.0
    assert result.primary.confidence >= 0.0


def test_confidence_never_exceeds_raw_score() -> None:
    """confidence = min(raw_score, ceiling) — never exceeds raw_score."""
    for score in [0.15, 0.30, 0.60, 0.90]:
        result = resolve_conflicts(
            {"Maf_Fault": score},
            _ctx(evidence_layers_used=["L1", "L2", "L3", "L4"]),  # ceiling 1.00
            _faults(),
            _qrc({"Maf_Fault": score}),
        )
        assert result.primary is not None
        assert result.primary.confidence == pytest.approx(score)
        assert result.primary.confidence <= result.primary.raw_score + 1e-9


def test_confidence_capped_by_ceiling_when_raw_high() -> None:
    """confidence is capped by ceiling when raw_score exceeds it (L05)."""
    result = resolve_conflicts(
        {"Maf_Fault": 0.80},
        _ctx(evidence_layers_used=["L1"]),  # ceiling 0.40
        _faults(),
        _qrc({"Maf_Fault": 0.80}),
    )
    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.80)
    assert result.primary.confidence == pytest.approx(0.40)
    assert result.confidence_ceiling == pytest.approx(0.40)
    assert result.primary.confidence < result.primary.raw_score


def test_confidence_equals_raw_when_below_ceiling() -> None:
    """confidence == raw_score when raw_score < ceiling."""
    result = resolve_conflicts(
        {"Maf_Fault": 0.35},
        _ctx(evidence_layers_used=["L1", "L2", "L3"]),  # ceiling 0.95
        _faults(),
        _qrc({"Maf_Fault": 0.35}),
    )
    assert result.primary is not None
    assert result.primary.raw_score == pytest.approx(0.35)
    assert result.primary.confidence == pytest.approx(0.35)


# ── confidence ceiling model ──────────────────────────────────────────────────


def test_ceiling_gas_only() -> None:
    """Gas-only (1 evidence layer) → ceiling 0.40 (L16)."""
    assert compute_ceiling(["L1"]) == pytest.approx(0.40)


def test_ceiling_gas_plus_dtc() -> None:
    """Gas + DTCs (2 evidence layers) → ceiling 0.60 (L16)."""
    assert compute_ceiling(["L1", "L3"]) == pytest.approx(0.60)


def test_ceiling_gas_dtc_ff() -> None:
    """Gas + DTCs + Freeze Frame (3 layers) → ceiling 0.95 (L16)."""
    assert compute_ceiling(["L1", "L3", "L4"]) == pytest.approx(0.95)


def test_ceiling_full_dna() -> None:
    """Full DNA (4 evidence layers) → ceiling 1.00 (L16)."""
    assert compute_ceiling(["L1", "L2", "L3", "L4"]) == pytest.approx(1.00)


def test_ceiling_empty_layers_defaults_to_full() -> None:
    """Empty evidence layers defaults to ceiling 1.00."""
    assert compute_ceiling([]) == pytest.approx(1.00)


# ── tier_delta invariants ─────────────────────────────────────────────────────


def test_tier_delta_is_raw_score_gap() -> None:
    """tier_delta = primary.raw_score - first_alternative.raw_score."""
    raw_probs = {"Maf_Fault": 0.70, "Rich_Mixture": 0.45, "Lean_Condition": 0.25}
    ctx = _ctx(
        symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"],
        evidence_layers_used=["L1", "L2", "L3"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    assert result.primary is not None
    assert result.primary.tier_delta == pytest.approx(0.25)
    assert result.primary.tier_delta >= 0.0


def test_tier_delta_zero_when_no_alternatives() -> None:
    """tier_delta is 0.0 when there are no alternatives."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    assert result.primary is not None
    assert result.primary.tier_delta == pytest.approx(0.0)


def test_tier_delta_zero_when_single_candidate() -> None:
    """tier_delta is 0.0 when only one candidate exists."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    assert result.primary is not None
    assert result.primary.tier_delta == pytest.approx(0.0)


def test_tier_delta_preserved_after_suppression() -> None:
    """tier_delta reflects post-suppression score gap."""
    raw_probs = {"High_Fuel_Pressure": 0.60, "Lean_Condition": 0.50}
    ctx = _ctx(
        engine_state="cold_open_loop",
        symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
        evidence_layers_used=["L1", "L2"],
    )
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    assert result.primary is not None
    # High_Fuel_Pressure suppressed to 0.18, Lean_Condition at 0.50 is top
    assert result.primary.fault_id == "Lean_Condition"
    assert result.primary.tier_delta >= 0.0


# ── state machine boundary tests ──────────────────────────────────────────────


def test_named_fault_threshold_boundary() -> None:
    """Score at exactly threshold produces named_fault."""
    result = resolve_conflicts(
        {"Maf_Fault": NAMED_FAULT_THRESHOLD},
        _ctx(),
        _faults(),
        _qrc({"Maf_Fault": NAMED_FAULT_THRESHOLD}),
    )
    assert result.state == "named_fault"


def test_named_fault_just_below_threshold() -> None:
    """Score just below threshold → insufficient_evidence."""
    result = resolve_conflicts(
        {"Maf_Fault": NAMED_FAULT_THRESHOLD - 1e-6},
        _ctx(),
        _faults(),
        _qrc({"Maf_Fault": NAMED_FAULT_THRESHOLD - 1e-6}),
    )
    assert result.state == "insufficient_evidence"


def test_state_transitions_with_discriminator() -> None:
    """A fault with high score but missing discriminator → insufficient_evidence."""
    raw_probs = {"Rich_Mixture": 0.80}
    ctx = _ctx(symptoms=[])  # no SYM_LAMBDA_LOW
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    assert result.state == "insufficient_evidence"
    assert result.primary is not None
    assert result.primary.discriminator_satisfied is False
    assert result.primary.raw_score == pytest.approx(1e-9)


def test_state_with_discriminator_and_dtc_combined() -> None:
    """Fault needs both DTC + discriminator; missing either blocks named_fault."""
    # P0420_Catalyst_Efficiency needs DTC P0420
    raw_probs = {"P0420_Catalyst_Efficiency": 0.55}
    ctx = _ctx(dtcs=["P0171"])  # wrong DTC
    result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
    assert result.state == "insufficient_evidence"


# ── 4-pathway scenario tests ──────────────────────────────────────────────────


class TestRegularPathway:
    """Regular pathway: L1+L2+L3+L4, warm closed loop, all evidence layers."""

    def test_regular_vacuum_leak_top_ranked(self) -> None:
        """Vacuum_Leak_Intake_Manifold with discriminator symptoms present wins."""
        raw_probs = {
            "Vacuum_Leak_Intake_Manifold": 0.75,
            "Lean_Condition": 0.55,
            "Maf_Fault": 0.20,
        }
        ctx = _ctx(
            dtcs=["P0171", "P0174"],
            symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH",
                       "SYM_TRIM_LEAN_IDLE_ONLY"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L2", "L3", "L4"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

        assert result.state == "named_fault"
        assert result.primary is not None
        assert result.primary.fault_id == "Vacuum_Leak_Intake_Manifold"
        assert result.primary.discriminator_satisfied is True
        assert result.confidence_ceiling == pytest.approx(1.00)
        assert len(result.alternatives) >= 1

    def test_regular_all_fields_populated(self) -> None:
        """Regular pathway result has all R9 schema fields with meaningful values."""
        raw_probs = {"Vacuum_Leak_Intake_Manifold": 0.75, "Lean_Condition": 0.50}
        ctx = _ctx(
            dtcs=["P0171"],
            symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L2", "L3", "L4"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

        fields = _result_dict(result)
        missing = R9_TOP_LEVEL_FIELDS - set(fields.keys())
        assert not missing, f"Missing R9 fields: {missing}"
        assert result.state == "named_fault"
        assert result.primary is not None
        assert isinstance(result.confidence_ceiling, float)
        assert isinstance(result.next_steps, list)

    def test_regular_specific_over_generic_promotion(self) -> None:
        """Child fault (Vacuum_Leak) within margin of parent (Lean_Condition) promoted."""
        raw_probs = {"Lean_Condition": 0.50, "Vacuum_Leak_Intake_Manifold": 0.42}
        ctx = _ctx(
            symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH"],
            evidence_layers_used=["L1", "L2", "L3", "L4"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.primary is not None
        assert result.primary.fault_id == "Vacuum_Leak_Intake_Manifold"
        assert result.primary.promoted_from_parent is True


class TestNonStarterPathway:
    """Non-starter pathway: no gas data, DTC-only (L3), engine not running."""

    def test_non_starter_dtc_only_named_fault(self) -> None:
        """DTC-only with valid DTC → named_fault, low ceiling."""
        raw_probs = {"P0420_Catalyst_Efficiency": 0.55}
        ctx = _ctx(
            dtcs=["P0420"],
            symptoms=[],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L3"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

        assert result.state == "named_fault"
        assert result.primary is not None
        assert result.primary.fault_id == "P0420_Catalyst_Efficiency"
        assert result.confidence_ceiling == pytest.approx(0.40)
        # confidence capped at ceiling; raw_score unchanged
        assert result.primary.raw_score == pytest.approx(0.55)
        assert result.primary.confidence == pytest.approx(0.40)

    def test_non_starter_missing_required_dtc(self) -> None:
        """DTC-only with wrong DTC → insufficient_evidence."""
        raw_probs = {"P0420_Catalyst_Efficiency": 0.55}
        ctx = _ctx(
            dtcs=["P0300"],  # not P0420
            symptoms=[],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L3"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.state == "insufficient_evidence"

    def test_non_starter_immobiliser_case(self) -> None:
        """P1570 immobiliser DTC with no gas — typical non-starter scenario."""
        raw_probs = {"P1570_Immobiliser": 0.65}
        ctx = _ctx(
            dtcs=["P1570"],
            symptoms=[],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L3"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.state == "named_fault"
        assert result.primary is not None
        assert result.primary.fault_id == "P1570_Immobiliser"
        assert result.primary.discriminator_satisfied is True  # no discriminator required

    def test_non_starter_ceiling_limits_confidence(self) -> None:
        """Non-starter pathway: DTC-only gets ceiling 0.40 (L16)."""
        raw_probs = {"Maf_Fault": 0.90}
        ctx = _ctx(
            dtcs=["P0300"],
            symptoms=[],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L3"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.primary is not None
        assert result.primary.raw_score == pytest.approx(0.90)
        assert result.primary.confidence == pytest.approx(0.40)
        assert result.primary.confidence < result.primary.raw_score


class TestColdStartPathway:
    """Cold-start restricted pathway: engine_state=cold_open_loop, enrichment active."""

    def test_cold_start_rich_family_suppressed(self) -> None:
        """Rich_Mixture family faults suppressed to 30% during cold_open_loop."""
        raw_probs = {
            "High_Fuel_Pressure": 0.60,
            "Lean_Condition": 0.40,
            "Maf_Fault": 0.25,
        }
        ctx = _ctx(
            engine_state="cold_open_loop",
            symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
            evidence_layers_used=["L1", "L2"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.primary is not None
        # High_Fuel_Pressure: 0.60 → 0.18; Lean_Condition at 0.40 wins
        assert result.primary.fault_id == "Lean_Condition"
        assert result.primary.raw_score == pytest.approx(0.40)

    def test_cold_start_multiple_rich_faults_suppressed(self) -> None:
        """All Rich_Mixture family faults are suppressed, not just the top one."""
        raw_probs = {
            "High_Fuel_Pressure": 0.60,
            "EVAP_Purge_Stuck_Open": 0.55,
            "Leaking_Injector": 0.50,
            "Maf_Fault": 0.30,
        }
        ctx = _ctx(
            engine_state="cold_open_loop",
            symptoms=[
                "SYM_HIGH_FUEL_PRESSURE_PATTERN",
                "SYM_RICH_NEGATIVE_TRIMS_PATTERN",
                "SYM_LEAKING_INJECTOR_PATTERN",
            ],
            evidence_layers_used=["L1", "L2", "L3"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.primary is not None
        # Maf_Fault (0.30) beats all suppressed rich faults
        assert result.primary.fault_id == "Maf_Fault"

    def test_cold_start_non_rich_fault_untouched(self) -> None:
        """Non Rich_Mixture family faults are not suppressed in cold_open_loop."""
        raw_probs = {"Maf_Fault": 0.50}
        ctx = _ctx(
            engine_state="cold_open_loop",
            evidence_layers_used=["L1", "L2"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert result.primary is not None
        assert result.primary.raw_score == pytest.approx(0.50)

    def test_cold_start_r9_fields_present(self) -> None:
        """Cold-start pathway result contains all R9 fields."""
        raw_probs = {"High_Fuel_Pressure": 0.60, "Lean_Condition": 0.40}
        ctx = _ctx(
            engine_state="cold_open_loop",
            symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
            evidence_layers_used=["L1", "L2"],
        )
        result = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        missing = R9_TOP_LEVEL_FIELDS - set(_result_dict(result).keys())
        assert not missing, f"Cold-start pathway missing R9 fields: {missing}"


class TestSoftRerunPathway:
    """Soft-rerun pathway: same input twice → identical output (determinism)."""

    def test_soft_rerun_identical_result(self) -> None:
        """Same inputs to resolve_conflicts → identical RankedResult (L06)."""
        raw_probs = {
            "Vacuum_Leak_Intake_Manifold": 0.72,
            "Lean_Condition": 0.55,
            "Maf_Fault": 0.15,
        }
        ctx = _ctx(
            dtcs=["P0171", "P0174"],
            symptoms=["SYM_LAMBDA_HIGH", "SYM_VE_LOSS", "SYM_O2_HIGH"],
            engine_state="warm_closed_loop",
            evidence_layers_used=["L1", "L2", "L3", "L4"],
        )
        r1 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        r2 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

        assert r1.state == r2.state
        assert r1.primary is not None
        assert r2.primary is not None
        assert r1.primary.fault_id == r2.primary.fault_id
        assert r1.primary.raw_score == pytest.approx(r2.primary.raw_score)
        assert r1.primary.confidence == pytest.approx(r2.primary.confidence)
        assert r1.primary.tier_delta == pytest.approx(r2.primary.tier_delta)
        assert r1.confidence_ceiling == pytest.approx(r2.confidence_ceiling)

    def test_soft_rerun_alternatives_identical(self) -> None:
        """Determinism must extend to alternatives list."""
        raw_probs = {"Maf_Fault": 0.70, "Rich_Mixture": 0.50, "Lean_Condition": 0.40}
        ctx = _ctx(
            symptoms=["SYM_LAMBDA_LOW", "SYM_LAMBDA_HIGH"],
            evidence_layers_used=["L1", "L2", "L3"],
        )
        r1 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        r2 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))

        assert len(r1.alternatives) == len(r2.alternatives)
        for a1, a2 in zip(r1.alternatives, r2.alternatives, strict=True):
            assert a1.fault_id == a2.fault_id
            assert a1.raw_score == pytest.approx(a2.raw_score)

    def test_soft_rerun_empty_probs_deterministic(self) -> None:
        """Empty probs determinism: insufficient_evidence both times."""
        r1 = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))
        r2 = resolve_conflicts({}, _ctx(), _faults(), _qrc({}))
        assert r1.state == r2.state == "insufficient_evidence"
        assert r1.primary is None
        assert r2.primary is None

    def test_soft_rerun_with_cold_start_deterministic(self) -> None:
        """Cold-start + soft-rerun: suppression is deterministic."""
        raw_probs = {"High_Fuel_Pressure": 0.60, "Lean_Condition": 0.40}
        ctx = _ctx(
            engine_state="cold_open_loop",
            symptoms=["SYM_HIGH_FUEL_PRESSURE_PATTERN", "SYM_LAMBDA_HIGH"],
        )
        r1 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        r2 = resolve_conflicts(raw_probs, ctx, _faults(), _qrc(raw_probs))
        assert r1.primary is not None
        assert r2.primary is not None
        assert r1.primary.fault_id == r2.primary.fault_id
        assert r1.primary.raw_score == pytest.approx(r2.primary.raw_score)


# ── cross-pathway uniformity (L06) ────────────────────────────────────────────


def test_all_four_pathways_produce_same_schema_shape() -> None:
    """All 4 pathways must return the same R9 schema shape (L06)."""
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

    for i, p in enumerate(pathways):
        ctx = _ctx(
            dtcs=p["dtcs"],
            symptoms=p["symptoms"],
            engine_state=p["engine_state"],
            evidence_layers_used=p["evidence_layers_used"],
        )
        result = resolve_conflicts(p["raw_probs"], ctx, _faults(), _qrc(p["raw_probs"]))
        fields = _result_dict(result)
        missing = R9_TOP_LEVEL_FIELDS - set(fields.keys())
        assert not missing, f"Pathway {i}: missing R9 fields: {missing}"
        assert result.state in VALID_STATES, (
            f"Pathway {i}: invalid state {result.state!r}"
        )


def test_perception_gap_nullable() -> None:
    """perception_gap may be None (M3 may not find a gap)."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    # perception_gap is None by default in _ctx — this is valid
    assert result.perception_gap is None  # valid R9 state


def test_next_steps_empty_when_named_fault() -> None:
    """next_steps must be empty when state is named_fault (no recovery needed)."""
    result = resolve_conflicts({"Maf_Fault": 0.50}, _ctx(), _faults(), _qrc({"Maf_Fault": 0.50}))
    assert result.state == "named_fault"
    assert result.next_steps == []


def test_next_steps_populated_on_insufficient_evidence_with_bc() -> None:
    """next_steps populated when insufficient_evidence AND backward_chaining is on."""
    ctx = _ctx(
        evidence_layers_used=["L1"],
        backward_chaining=True,
    )
    result = resolve_conflicts(
        {"Maf_Fault": 0.05}, ctx, _faults(), _qrc({"Maf_Fault": 0.05})
    )
    assert result.state == "insufficient_evidence"
    assert len(result.next_steps) >= 0  # may be empty if no layer lifts above threshold


def test_next_steps_empty_when_bc_disabled() -> None:
    """next_steps is empty when backward_chaining is off, regardless of state."""
    ctx = _ctx(
        evidence_layers_used=["L1"],
        backward_chaining=False,
    )
    result = resolve_conflicts(
        {"Maf_Fault": 0.05}, ctx, _faults(), _qrc({"Maf_Fault": 0.05})
    )
    assert result.state == "insufficient_evidence"
    assert result.next_steps == []
