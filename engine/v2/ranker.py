"""M5 — Ranker: resolve_conflicts() 8-step ordered loop and result assembly.

R7: single conflict-resolution function.  L02: fixed order, no post-inference
stacking.  R9: unified result schema across all 4 pathways.  L05: raw_score for
gate logic, confidence for display only — never swap.  L16: confidence ceiling
keys on evidence layers used, not data submitted.

Steps 1 (tech veto) and 2 (era veto) are applied in M4 (kg_engine.py), NOT here.
Steps 3–8 run in this module in fixed order, asserted by
test_resolve_conflicts_order.py.

Source: v2-result-schema §1–§5.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.v2.arbitrator import PerceptionGap
from engine.v2.input_model import ValidationWarning

# ── constants ─────────────────────────────────────────────────────────────────
# source: v2-result-schema §3 state machine

NAMED_FAULT_THRESHOLD: float = 0.10
"""raw_score must reach this threshold for state = named_fault."""

# source: v2-result-schema §4 step 6
SPECIFIC_MARGIN: float = 0.10
"""Maximum score gap between child and parent for specific-over-generic promotion."""

# source: v2-result-schema §4 step 5 — cold-start enrichment false-positive family
COLD_START_RICH_FAMILY: frozenset[str] = frozenset(
    {
        "Rich_Mixture",
        "High_Fuel_Pressure",
        "Leaking_Injector",
        "EVAP_Purge_Stuck_Open",
        "Fuel_Pressure_Regulator_Fault",
        "Return_Line_Restricted",
    }
)

# source: v2-result-schema §4 step 5 — cold-start suppression factor
COLD_START_SUPPRESSION_FACTOR: float = 0.30

# ── evidence-layer ceiling table ──────────────────────────────────────────────
# source: v2-result-schema §2 confidence ceiling model

_CEILING_TABLE: dict[int, float] = {
    1: 0.40,  # gas only
    2: 0.60,  # gas + DTCs
    3: 0.95,  # gas + DTCs + freeze frame
    4: 1.00,  # full DNA (all layers + vehicle context)
}


# ── output dataclasses ────────────────────────────────────────────────────────


@dataclass(slots=True)
class FaultResult:
    """A single fault result within the RankedResult (R9 primary/alternatives shape).

    L05: raw_score is the internal gate value; confidence is the display value
    capped by confidence_ceiling.  Never use confidence in gate logic.
    """

    fault_id: str
    symptom_chain: list[str]
    root_cause: str | None
    confidence: float
    raw_score: float
    evidence_layers_used: list[str]
    tier_delta: float
    discriminator_satisfied: bool
    promoted_from_parent: bool


@dataclass
class RankedResult:
    """M5 output — unified result schema (R9).

    All 4 pathways (regular, non-starter, cold-start restricted, soft-rerun)
    return this exact shape.  L06: no pathway-specific field divergence.
    """

    state: str  # named_fault | insufficient_evidence | invalid_input
    primary: FaultResult | None
    alternatives: list[FaultResult]
    perception_gap: PerceptionGap | None
    validation_warnings: list[ValidationWarning]
    cascading_consequences: list[str]
    confidence_ceiling: float
    next_steps: list[dict]


@dataclass(slots=True)
class ResolutionContext:
    """Context bundle passed to resolve_conflicts() from the pipeline orchestrator.

    Carries everything M5 needs that is not the raw_probs vector or the schema
    (faults/root_causes are passed separately to keep resolve_conflicts()
    testable without YAML I/O).
    """

    dtcs: list[str]
    symptoms: list[str]
    engine_state: str
    evidence_layers_used: list[str]
    perception_gap: PerceptionGap | None = None
    validation_warnings: list[ValidationWarning] = field(default_factory=list)
    cascading_consequences: list[str] = field(default_factory=list)


# ── public entry point ────────────────────────────────────────────────────────


def resolve_conflicts(
    raw_probs: dict[str, float],
    ctx: ResolutionContext,
    faults: dict,
    root_causes: dict,
) -> RankedResult:
    """Run the 8-step ordered conflict-resolution loop (R7, L02).

    Steps 1 (tech veto) and 2 (era veto) are applied in M4.  This function
    runs steps 3–8 in fixed order:
      3. DTC-prerequisite gate — faults requiring a DTC the input lacks
         fall back to parent score or 1e-9.
      4. Discriminator gate — faults requiring a symptom not present
         fall back to parent score or 1e-9.
      5. Cold-start family suppression — Rich_Mixture family faults
         are reduced to 30% during cold_open_loop.
      6. Specific-over-generic margin promotion — child faults within
         0.10 of their parent are promoted above the parent.
      7. Confidence ceiling — every candidate score is capped at the
         evidence-layer ceiling.
      8. Sort + deterministic tie-break — by (-score, -prior, fault_id).

    Args:
        raw_probs: fault_id → raw_score from M4 (score_faults() output).
        ctx: ResolutionContext with dtcs, symptoms, engine_state, layers,
             perception_gap, validation_warnings, cascading_consequences.
        faults: Parsed faults.yaml (fault_id → fault_def).
        root_causes: Parsed root_causes.yaml (rc_id → root_cause_def).

    Returns:
        RankedResult with primary, alternatives, state, and all R9 fields.
    """
    # Start from positive-scoring candidates only.
    candidates = {fid: p for fid, p in raw_probs.items() if p > 0.0}

    # ── Step 3: DTC-prerequisite gate ───────────────────────────────────
    _apply_dtc_gate(candidates, ctx.dtcs, faults)

    # ── Step 4: Discriminator gate ─────────────────────────────────────
    _apply_discriminator_gate(candidates, ctx.symptoms, faults)

    # ── Step 5: Cold-start family suppression ──────────────────────────
    if ctx.engine_state == "cold_open_loop":
        _suppress_cold_start(candidates)

    # ── Step 6: Specific-over-generic margin promotion ──────────────────
    promoted = _promote_specific_within_margin(candidates, faults, SPECIFIC_MARGIN)

    # ── Step 7: Confidence ceiling ─────────────────────────────────────
    ceiling = compute_ceiling(ctx.evidence_layers_used)

    # ── Step 8: Sort + deterministic tie-break ─────────────────────────
    ranked = sorted(
        candidates.items(),
        key=lambda x: (-x[1], -faults.get(x[0], {}).get("prior", 0.0), x[0]),
    )

    return _build_result(ranked, promoted, ctx, faults, root_causes, ceiling)


# ── ceiling computation ───────────────────────────────────────────────────────


def compute_ceiling(evidence_layers_used: list[str]) -> float:
    """Return the confidence ceiling for the given evidence layers.

    source: v2-result-schema §2 confidence ceiling model

    | Evidence layers used | Ceiling |
    | Gas only (L1 or L2)  | 0.40    |
    | Gas + DTCs           | 0.60    |
    | Gas + DTCs + FF      | 0.95    |
    | Full DNA              | 1.00    |

    Args:
        evidence_layers_used: List of layer identifiers (e.g. ["L1", "L3"]).

    Returns:
        Ceiling value in [0.40, 1.00].
    """
    count = len(evidence_layers_used)
    return _CEILING_TABLE.get(count, 1.00)


# ── step 3: DTC-prerequisite gate ────────────────────────────────────────────


def _apply_dtc_gate(
    candidates: dict[str, float],
    dtcs: list[str],
    faults: dict,
) -> None:
    """Demote faults whose dtc_required list is not satisfied by the input DTCs.

    When a fault requires a DTC not present, its score falls back to its
    parent's score (if parent is in candidates) or 1e-9 (trace presence
    for alternatives).
    """
    for fid in list(candidates):
        fault_def = faults.get(fid, {})
        required = fault_def.get("dtc_required", [])
        if not required:
            continue
        if any(d in dtcs for d in required):
            continue
        parent = fault_def.get("parent")
        candidates[fid] = candidates.get(parent, 0.0) if parent else 0.0
        if candidates[fid] <= 0.0:
            candidates[fid] = 1e-9


# ── step 4: discriminator gate ───────────────────────────────────────────────


def _apply_discriminator_gate(
    candidates: dict[str, float],
    symptoms: list[str],
    faults: dict,
) -> None:
    """Demote faults whose discriminator symptoms are not present.

    A discriminator is a symptom (or set of symptoms) that uniquely
    distinguishes a fault from its siblings (L03).  When the required
    discriminator symptom is absent, the fault falls back to parent score
    or 1e-9.
    """
    for fid in list(candidates):
        fault_def = faults.get(fid, {})
        discriminator = fault_def.get("discriminator", [])
        if not discriminator:
            continue
        if any(s in symptoms for s in discriminator):
            continue
        parent = fault_def.get("parent")
        candidates[fid] = candidates.get(parent, 0.0) if parent else 0.0
        if candidates[fid] <= 0.0:
            candidates[fid] = 1e-9


# ── step 5: cold-start suppression ───────────────────────────────────────────


def _suppress_cold_start(candidates: dict[str, float]) -> None:
    """Reduce Rich_Mixture family scores during cold_open_loop enrichment.

    During cold start, the ECU runs open-loop enrichment, causing rich
    exhaust that can falsely activate rich-mixture faults.  Scores for
    COLD_START_RICH_FAMILY members are multiplied by 0.30.

    source: v2-result-schema §4 step 5
    source: v2-design-rules L18 (fuel-status gate)
    """
    for fid in COLD_START_RICH_FAMILY:
        if fid in candidates:
            candidates[fid] *= COLD_START_SUPPRESSION_FACTOR


# ── step 6: specific-over-generic margin promotion ───────────────────────────


def _promote_specific_within_margin(
    candidates: dict[str, float],
    faults: dict,
    margin: float,
) -> set[str]:
    """Promote child faults that score within margin of their parent.

    Specific-over-generic preference: when a child fault is within `margin`
    raw_score points of its parent, the parent is demoted so the child
    outranks it.  Returns the set of fault IDs that were promoted.

    source: v2-result-schema §4 step 6
    """
    promoted: set[str] = set()
    for fid, score in candidates.items():
        parent = faults.get(fid, {}).get("parent")
        if parent is None or parent not in candidates:
            continue
        if candidates[parent] - score <= margin:
            candidates[parent] = 1e-9
            promoted.add(fid)
    return promoted


# ── result assembly ──────────────────────────────────────────────────────────


def _build_result(
    ranked: list[tuple[str, float]],
    promoted: set[str],
    ctx: ResolutionContext,
    faults: dict,
    root_causes: dict,
    ceiling: float,
) -> RankedResult:
    """Assemble the RankedResult from the ranked candidate list.

    R9: primary + up to 2 alternatives.  L05: confidence ≤ ceiling.
    L05: raw_score for gates, confidence for display.
    """
    alternatives: list[FaultResult] = []
    primary: FaultResult | None = None

    for idx, (fid, raw_score) in enumerate(ranked):
        fault_def = faults.get(fid, {})
        discriminator = fault_def.get("discriminator", [])
        discriminator_satisfied = (
            not discriminator
            or any(s in ctx.symptoms for s in discriminator)
        )

        # Determine root cause if parent score ≥ 0.80 (R2 / L16).
        root_cause = _find_root_cause(fid, raw_score, root_causes)

        fr = FaultResult(
            fault_id=fid,
            symptom_chain=[],  # populated in T-P5-2 backward-chaining
            root_cause=root_cause,
            confidence=min(raw_score, ceiling),
            raw_score=raw_score,
            evidence_layers_used=list(ctx.evidence_layers_used),
            tier_delta=0.0,  # computed below for primary
            discriminator_satisfied=discriminator_satisfied,
            promoted_from_parent=(fid in promoted),
        )

        if idx == 0:
            primary = fr
        elif idx <= 2:
            alternatives.append(fr)

    # Compute tier_delta for primary.
    if primary is not None and alternatives:
        primary.tier_delta = primary.raw_score - alternatives[0].raw_score

    # Determine state (R9 state machine).
    state = _determine_state(primary)

    return RankedResult(
        state=state,
        primary=primary,
        alternatives=alternatives,
        perception_gap=ctx.perception_gap,
        validation_warnings=list(ctx.validation_warnings),
        cascading_consequences=list(ctx.cascading_consequences),
        confidence_ceiling=ceiling,
        next_steps=[],  # populated in T-P5-2 backward-chaining
    )


def _find_root_cause(
    fault_id: str,
    raw_score: float,
    root_causes: dict,
) -> str | None:
    """Find the best root cause for a fault if parent threshold is met.

    source: R2/L16 — root cause only populated when raw_score ≥ 0.80.
    When multiple root causes apply to the same fault, the first defined
    in root_causes.yaml wins.
    """
    if raw_score < 0.80:
        return None
    for rc_id, rc_def in root_causes.items():
        if rc_def.get("applies_to_fault") == fault_id:
            return rc_id
    return None


def _determine_state(primary: FaultResult | None) -> str:
    """Determine result state from the top candidate.

    source: v2-result-schema §3 state machine
    """
    if primary is None:
        return "insufficient_evidence"
    if primary.raw_score < NAMED_FAULT_THRESHOLD:
        return "insufficient_evidence"
    if not primary.discriminator_satisfied:
        return "insufficient_evidence"
    return "named_fault"
