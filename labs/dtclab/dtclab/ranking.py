"""DTCLab Phase 2 scorer — per-family confidence from §16 weights + §14.2 DNA gating.

rank_candidates() turns the family map (T-DT2-1) into ranked (family, raw_confidence,
match_type) rows.  Confidence is sourced entirely from the already-canonical
DTC_CONFIDENCE_WEIGHTS (DTC_VOCABULARY.md §16) and DNA-confidence gate (§14.2).
No new numeric literal.  No clamping (T-DT2-3).  No sum-1 normalisation (DESIGN §4).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

import yaml

from dtclab.family_map import ROUTING_TAG_TO_FAMILY
from dtclab.schemas.dna_view import DtcLabDnaView, VinConfidence
from dtclab.schemas.payload import DTCLabPayload
from dtclab.schemas.vocabulary import (
    DTC_CONFIDENCE_WEIGHTS,
    DTCRoutingTag,
    Mode06MonitorState,
)

__all__ = [
    "MatchType",
    "CandidateScore",
    "rank_candidates",
    "classify_top3",
]

logger = logging.getLogger(__name__)

# =============================================================================
# MatchType — DTC-state-derived evidence tier
# =============================================================================


class MatchType(StrEnum):
    """Evidence-strength tier derived from the strongest contributing source.

    Source: DTC_VOCABULARY.md §16 weights → tier mapping.
    """

    DEFINITIVE = "DEFINITIVE"      # wiki: §16 — CONFIRMED / PERMANENT (weight 1.0)
    INDICATIVE = "INDICATIVE"      # wiki: §16 — PENDING (weight 0.5)
    MONITOR_WEAK = "MONITOR_WEAK"  # wiki: §16 — Mode $06 CRITICAL_FAIL (0.7) / MARGINAL (0.4)
    MONITOR_PASS = "MONITOR_PASS"  # wiki: §16 — Mode $06 PASSED (0.0)


# =============================================================================
# CandidateScore
# =============================================================================


@dataclass(frozen=True)
class CandidateScore:
    """Single fault-family candidate with raw confidence and evidence tier.

    Fields consumed by T-DT2-3 (classify_top3) → T-DTW-1 (LabResult adapter).
    """

    family: str                 # canonical family from ROUTING_TAG_TO_FAMILY
    raw_confidence: float       # max §16 weight × dna_factor  # wiki: §16, §14.2
    match_type: MatchType       # evidence tier from strongest contributor


# =============================================================================
# DNA gate confidence factors — DTC_VOCABULARY.md §14.2
# =============================================================================

_DNA_FACTOR_HIGH: float = 1.0     # wiki: §14.2 — gate holds; full confidence
_DNA_FACTOR_PARTIAL: float = 0.7  # wiki: §14.2 — downgrade (partial DNA)
_DNA_FACTOR_NONE: float = 0.5     # wiki: §14.2 — pure DTC pattern (no DNA)


# =============================================================================
# Cached routing-rule loader (module-level — loaded once per session)
# =============================================================================

# Per-rule tuple: (compiled_pattern, tag, dna_gate_name | None)
_RuleEntry = tuple[re.Pattern[str], DTCRoutingTag, str | None]
_routing_rules_cache: list[_RuleEntry] | None = None


def _load_routing_rules() -> list[_RuleEntry]:
    """Load and compile routing rules from dtclab/config/routing_tag_map.yaml.

    Cached at module level — the file is read once per session.
    """
    global _routing_rules_cache
    if _routing_rules_cache is not None:
        return _routing_rules_cache

    config_path = Path(__file__).parent / "config" / "routing_tag_map.yaml"
    with open(config_path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)

    rules: list[_RuleEntry] = []
    for entry in data["entries"]:
        tag = DTCRoutingTag(entry["tag"])
        dna_gate: str | None = entry.get("dna_gate")
        for pattern_str in entry["patterns"]:
            rules.append((re.compile(pattern_str), tag, dna_gate))

    _routing_rules_cache = rules
    return rules


# =============================================================================
# Per-family tagging helpers
# =============================================================================

_TagSet = frozenset[DTCRoutingTag]
_family_tag_cache: dict[str, _TagSet] | None = None
_family_gate_cache: dict[str, set[str]] | None = None


def _build_family_index() -> tuple[dict[str, _TagSet], dict[str, set[str]]]:
    """Build family → tags and family → dna_gate_names indices.

    Returns:
        (family_tags, family_gates) where family_tags maps family→tags and
        family_gates maps family→set of dna_gate_name strings.
    """
    global _family_tag_cache, _family_gate_cache
    if _family_tag_cache is not None and _family_gate_cache is not None:
        return _family_tag_cache, _family_gate_cache

    rules = _load_routing_rules()
    ft: dict[str, set[DTCRoutingTag]] = {}
    fg: dict[str, set[str]] = {}

    for tag, family in ROUTING_TAG_TO_FAMILY.items():
        if family is None:
            continue
        ft.setdefault(family, set()).add(tag)

    # Collect DNA gate names for each family
    for _, tag, gate in rules:
        family = ROUTING_TAG_TO_FAMILY.get(tag)
        if family is not None and gate is not None:
            fg.setdefault(family, set()).add(gate)

    _family_tag_cache = {f: frozenset(t) for f, t in ft.items()}
    _family_gate_cache = fg
    return _family_tag_cache, _family_gate_cache


def _dna_factor_for_family(
    family_gates: dict[str, set[str]],
    family: str,
    dna_view: DtcLabDnaView | None,
) -> float:
    """Return the DNA confidence multiplier for *family*.

    Ungated families always return 1.0.  DNA-gated families apply §14.2:
      - HIGH  → full confidence (1.0)
      - PARTIAL → reduced (0.7) with logged downgrade
      - NONE/None → reduced (0.5) — pure DTC-pattern routing
    """
    if family not in family_gates:
        return 1.0  # wiki: §14.2 — no gate on this family

    if dna_view is None:
        return _DNA_FACTOR_NONE  # wiki: §14.3 — None ≡ NONE

    confidence = dna_view.confidence

    if confidence == VinConfidence.HIGH:
        return _DNA_FACTOR_HIGH  # wiki: §14.2 — gate holds

    if confidence == VinConfidence.PARTIAL:
        logger.info(
            "dna_confidence_downgraded: family=%s confidence=%s factor=%s",
            family, confidence.value, _DNA_FACTOR_PARTIAL,
        )
        return _DNA_FACTOR_PARTIAL  # wiki: §14.2 — logged downgrade

    return _DNA_FACTOR_NONE  # wiki: §14.2 — NONE → pure DTC pattern


def _match_type_for_weight(weight: float) -> MatchType:
    """Map a §16 confidence weight to its MatchType evidence tier."""
    if weight == DTC_CONFIDENCE_WEIGHTS["confirmed"]:
        return MatchType.DEFINITIVE  # wiki: §16 — 1.0
    if weight == DTC_CONFIDENCE_WEIGHTS["permanent"]:
        return MatchType.DEFINITIVE  # wiki: §16 — 1.0
    if weight == DTC_CONFIDENCE_WEIGHTS["pending"]:
        return MatchType.INDICATIVE  # wiki: §16 — 0.5
    if weight in (
        DTC_CONFIDENCE_WEIGHTS["mode06_critical_fail"],
        DTC_CONFIDENCE_WEIGHTS["mode06_marginal"],
    ):
        return MatchType.MONITOR_WEAK  # wiki: §16 — 0.7 / 0.4
    return MatchType.MONITOR_PASS  # wiki: §16 — 0.0


# =============================================================================
# Public API
# =============================================================================


def rank_candidates(
    payload: DTCLabPayload,
    *,
    dna_view: DtcLabDnaView | None = None,
) -> list[CandidateScore]:
    """Score each fault family observed in *payload* using §16 weights + §14.2 DNA gating.

    For each canonical family reachable from ``payload.routing_tags``:
      1. Compute the max §16 weight across all contributing DTCs (confirmed=1.0,
         permanent=1.0, pending=0.5) and Mode $06 monitors (CRITICAL_FAIL=0.7,
         MARGINAL=0.4, PASSED=0.0).
      2. Multiply by the §14.2 DNA confidence factor for DNA-gated families.
      3. Set ``MatchType`` from the strongest contributing evidence source.

    Context-only tags (family=None) and POA_HISTORY are excluded — they do not
    produce candidates.

    Args:
        payload: Full DTCLab output (DTC lists + routing tags + Mode $06 monitors).
        dna_view: Optional DNA view for §14.2 confidence gating.

    Returns:
        Candidates sorted by ``raw_confidence`` descending, then family name.
        Empty list when no routable tags are present.
    """
    rules = _load_routing_rules()
    family_tags, family_gates = _build_family_index()

    # Per-family accumulators
    family_max_weight: dict[str, float] = {}
    family_best_match: dict[str, MatchType] = {}

    # ------------------------------------------------------------------
    # Seed families from routing tags (present even without DTC evidence)
    # ------------------------------------------------------------------

    for tag in payload.routing_tags:
        family = ROUTING_TAG_TO_FAMILY.get(tag)
        if family is None:
            continue
        if family not in family_max_weight:
            family_max_weight[family] = DTC_CONFIDENCE_WEIGHTS["mode06_passed"]
            family_best_match[family] = MatchType.MONITOR_PASS

    # ------------------------------------------------------------------
    # DTC evidence — CONFIRMED (1.0), PERMANENT (1.0), PENDING (0.5)
    # ------------------------------------------------------------------

    _dtc_sources: list[tuple[list[str], str]] = [
        (payload.confirmed_dtcs, "confirmed"),
        (payload.permanent_dtcs, "permanent"),
        (payload.pending_dtcs, "pending"),
    ]

    for dtc_list, weight_key in _dtc_sources:
        weight = DTC_CONFIDENCE_WEIGHTS[weight_key]
        match_type = _match_type_for_weight(weight)
        for dtc in dtc_list:
            for pattern, tag, _dna_gate in rules:
                if not pattern.match(dtc):
                    continue
                family = ROUTING_TAG_TO_FAMILY.get(tag)
                if family is None:
                    continue  # context-only / POA_HISTORY
                if weight > family_max_weight.get(family, -1.0):
                    family_max_weight[family] = weight
                    family_best_match[family] = match_type
                break  # first matching rule wins per the mapper convention

    # ------------------------------------------------------------------
    # Mode $06 evidence — global max across all monitors, applied to all families
    # ------------------------------------------------------------------

    max_monitor_weight = DTC_CONFIDENCE_WEIGHTS["mode06_passed"]  # 0.0
    max_monitor_type = MatchType.MONITOR_PASS
    for monitor in payload.mode_06_monitors.values():
        if monitor.state == Mode06MonitorState.CRITICAL_FAIL:
            w = DTC_CONFIDENCE_WEIGHTS["mode06_critical_fail"]
            if w > max_monitor_weight:
                max_monitor_weight = w
                max_monitor_type = MatchType.MONITOR_WEAK
        elif monitor.state == Mode06MonitorState.PENDING_FAIL_MARGINAL:
            w = DTC_CONFIDENCE_WEIGHTS["mode06_marginal"]
            if w > max_monitor_weight:
                max_monitor_weight = w
                max_monitor_type = MatchType.MONITOR_WEAK

    # Apply monitor evidence to every active family (global contribution)
    if max_monitor_weight > DTC_CONFIDENCE_WEIGHTS["mode06_passed"]:
        for family in family_max_weight:
            if max_monitor_weight > family_max_weight[family]:
                family_max_weight[family] = max_monitor_weight
                family_best_match[family] = max_monitor_type

    # ------------------------------------------------------------------
    # Apply DNA gate factor + assemble results
    # ------------------------------------------------------------------

    candidates: list[CandidateScore] = []
    for family, max_weight in family_max_weight.items():
        dna_factor = _dna_factor_for_family(family_gates, family, dna_view)
        # No clamping — T-DT2-3 owns clamp_to_01
        raw_confidence = max_weight * dna_factor
        match_type = family_best_match[family]

        candidates.append(
            CandidateScore(
                family=family,
                raw_confidence=raw_confidence,
                match_type=match_type,
            )
        )

    # Sort: highest confidence first, then family name for determinism
    candidates.sort(key=lambda c: (-c.raw_confidence, c.family))
    return candidates


# =============================================================================
# Phase 2 exit — classify_top3
# =============================================================================


def classify_top3(
    payload: DTCLabPayload,
    *,
    dna_view: DtcLabDnaView | None = None,
) -> list[tuple[str, float]]:
    """Top-3 (family, confidence∈[0,1]) candidates for Bayesian fusion (FU-1).

    Calls ``rank_candidates`` (T-DT2-2), clamps each raw confidence to [0,1]
    via the trivial unit-interval bound (no family-keyed or tier-keyed constant
    — DESIGN §6), deduplicates families keeping the max confidence, sorts by
    ``(-confidence, family)`` for deterministic tie-breaking, and returns at
    most three entries.

    No sum-1 normalisation — Bayesian ``combine()`` does fusion/normalisation
    (DESIGN §4).  No ``LabResult``/``LabCandidate`` construction — that is the
    Wired adapter ``T-DTW-1``.

    Args:
        payload: Full DTCLab output.
        dna_view: Optional DNA view for §14.2 confidence gating.

    Returns:
        Up to 3 ``(canonical_family, confidence)`` pairs, sorted descending
        by confidence then alphabetically by family.  Empty when no routable
        tags are present.
    """
    candidates = rank_candidates(payload, dna_view=dna_view)

    seen_families: set[str] = set()
    result: list[tuple[str, float]] = []

    for c in candidates:
        if c.family in seen_families:
            continue
        # wiki: §16, §14.2 — clamp to unit interval only (no family-keyed ceiling)
        confidence = min(max(c.raw_confidence, 0.0), 1.0)
        seen_families.add(c.family)
        result.append((c.family, confidence))

    # rank_candidates already sorts by (-raw_confidence, family), so after
    # clamp + dedup the order is preserved.  Re-sort to be safe after clamp.
    result.sort(key=lambda item: (-item[1], item[0]))

    return result[:3]
