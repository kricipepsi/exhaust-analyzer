"""M4 — Knowledge Graph engine: tech/era veto pre-pass and CF combination scoring.

R2: two-layer inference — subtractive vetoes (Layer A) + MYCIN CF combination (Layer B).
R6: era masking applied here — fault nodes outside the vehicle's era bucket score 0.0.
R7: resolve_conflicts() lives in M5 only — M4 produces raw_probs only, never calls it.
L01: scores from active_symptoms entries only, never from perception_gap directly.
L05: produces raw_score values for gating; confidence scaling is M5's job.

Source: v2-cf-inference §1–§5.
"""

from __future__ import annotations

from engine.v2.arbitrator import MasterEvidenceVector
from engine.v2.dna_core import (
    ERA_CAN,
    ERA_MODERN,
    ERA_OBDII_EARLY,
    ERA_PRE_OBDII,
    DNAOutput,
)

# ── era bucket → YAML era range string mapping ────────────────────────────────
# DNAOutput uses symbolic constants; faults.yaml uses year-range strings.
# source: v2-era-masking §2 era buckets

_ERA_BUCKET_TO_RANGE: dict[str, str] = {
    ERA_PRE_OBDII: "1990-1995",
    ERA_OBDII_EARLY: "1996-2005",
    ERA_CAN: "2006-2015",
    ERA_MODERN: "2016-2020",
}


# ── CF combination ────────────────────────────────────────────────────────────


def combine_cf(weights: list[float]) -> float:
    """Combine certainty factors using the MYCIN CF rule.

    For two positive CFs:  CF_combined(a,b) = a + b·(1 − a)
    For opposite signs:    CF_combined(a,b) = (a + b) / (1 − min(|a|,|b|))
    For two negatives:     symmetric MYCIN on absolute values.

    Boundary cases (source: v2-cf-inference §4 golden outputs):
      combine_cf([]) → 0.0
      combine_cf([1.0, 1.0]) → 1.0  (bounded, never > 1.0)

    Args:
        weights: CF values in [-1.0, 1.0].

    Returns:
        Combined CF in [-1.0, 1.0].
    """
    if not weights:
        return 0.0
    if len(weights) == 1:
        return weights[0]

    result = weights[0]
    for w in weights[1:]:
        if result >= 0.0 and w >= 0.0:
            result = result + w * (1.0 - result)
        elif result <= 0.0 and w <= 0.0:
            result = result + w * (1.0 + result)
        else:
            denom = 1.0 - min(abs(result), abs(w))
            result = 0.0 if denom == 0.0 else (result + w) / denom

    return result


# ── public entry point ────────────────────────────────────────────────────────


def score_faults(
    evidence: MasterEvidenceVector,
    dna: DNAOutput,
    faults: dict,
    edges: list[dict],
) -> dict[str, float]:
    """Score every fault against the evidence vector using CF inference.

    Scoring order (R2):
      1. Tech pre-veto — fault requires a tech flag the engine lacks → 0.0
      2. Era pre-veto  — fault era list does not include vehicle's era → 0.0
      3. Hard edge veto — incoming edge with weight == −1.0 from an active
         symptom → 0.0
      4. Positive CF combination — MYCIN rule on (edge_weight × symptom_cf)
         contributions from active symptoms
      5. Inhibitory subtraction — subtract |contributions| of inhibitory edges
         (−1.0 < w < 0), floor at 0.0

    M4 never calls resolve_conflicts() (R7).  Output is raw_probs — raw_score
    values for M5 gating, NOT display confidence.

    Args:
        evidence: M3 output — active_symptoms (symptom_id → cf_weight).
        dna: M0 output — tech_mask, era_bucket for pre-veto passes.
        faults: Parsed faults.yaml (fault_id → fault_def).
        edges: Parsed edges.yaml list of {source, target, weight, ...}.

    Returns:
        raw_probs: fault_id → raw_score in [0.0, 1.0].
    """
    # Build reverse edge index: target_fault → list of incoming edges.
    incoming: dict[str, list[dict]] = {}
    for edge in edges:
        target = edge["target"]
        incoming.setdefault(target, []).append(edge)

    era_range = _ERA_BUCKET_TO_RANGE.get(dna.era_bucket, ERA_MODERN)
    active = evidence.active_symptoms

    raw_probs: dict[str, float] = {}

    for fault_id, fault in faults.items():
        # ── 1. Tech pre-veto ──────────────────────────────────────────
        if _tech_vetoed(fault, dna.tech_mask):
            raw_probs[fault_id] = 0.0
            continue

        # ── 2. Era pre-veto ───────────────────────────────────────────
        if era_range not in fault.get("era", ()):
            raw_probs[fault_id] = 0.0
            continue

        fault_edges = incoming.get(fault_id, [])

        # ── 3. Hard edge veto ─────────────────────────────────────────
        if _has_hard_veto(fault_edges, active):
            raw_probs[fault_id] = 0.0
            continue

        # ── 4. Positive CF combination ────────────────────────────────
        positives: list[float] = []
        inhibitors: list[float] = []
        for edge in fault_edges:
            src = edge["source"]
            if src not in active:
                continue
            w = float(edge["weight"])
            cf = float(active[src])
            contribution = w * cf
            if w > 0.0:
                positives.append(contribution)
            elif w > -1.0:
                inhibitors.append(abs(contribution))

        cf_score = combine_cf(positives)

        # ── 5. Inhibitory subtraction ─────────────────────────────────
        score = max(0.0, cf_score - sum(inhibitors))
        raw_probs[fault_id] = score

    return raw_probs


# ── veto helpers ──────────────────────────────────────────────────────────────


def _tech_vetoed(fault: dict, tech_mask: dict[str, bool]) -> bool:
    """Return True if the fault requires a tech flag the engine lacks."""
    return any(
        not tech_mask.get(flag, False) for flag in fault.get("tech_required", ())
    )


def _has_hard_veto(edges: list[dict], active: dict[str, float]) -> bool:
    """Return True if any incoming edge has weight == −1.0 from an active symptom."""
    return any(
        edge["source"] in active and float(edge["weight"]) == -1.0
        for edge in edges
    )
