"""Ranked internal GASLab candidates for top-3 emission.

This module exposes the existing rule-engine traversal as scored internal
candidates without changing the JSON boundary.

Source: ``GAS_WIKI §10.5`` and ``GASLabSimple/DESIGN_percent_sourcing.md §7``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.family_map import SIGNATURE_TO_FAMILY
from gaslab.rule_engine import (
    _GAS_KEYS,
    _candidate_rank,
    _definitive_match,
    _matching_fault_candidates,
    _resolve_candidates,
    _signature_values,
    _specificity,
)

_SCORE_ZERO = float(0)  # wiki: GAS_WIKI §10.5 — no-match fallback has no positive evidence
_SCORE_ONE = float(1)  # wiki: GAS_WIKI §10.5 — specificity inverse numerator
_TOP3_LIMIT = 3  # wiki: GAS_WIKI §10.5 — top-3 emission contract
_DNA_HIGH = "HIGH"  # wiki: GAS_WIKI §10.1
_DNA_PARTIAL = "PARTIAL"  # wiki: GAS_WIKI §10.1
_DNA_NONE = "NONE"  # wiki: GAS_WIKI §10.1


class MatchType(StrEnum):
    """Internal match-type buckets for the GASLab top-3 scoring path.

    Source: ``GAS_WIKI §10.5``.
    """

    DEFINITIVE = "DEFINITIVE"
    SPECIFIC = "SPECIFIC"
    CATCH_ALL = "CATCH_ALL"
    FALLBACK = "FALLBACK"


@dataclass(frozen=True)
class CandidateScore:
    """A ranked internal GASLab candidate.

    Source: ``GAS_WIKI §10.5``.
    """

    signature: ChemicalSignature
    match_type: MatchType
    specificity: float
    corroborating_channels: int
    raw_score: float

    @property
    def specificity_inverse(self) -> float:
        """Return the deterministic tie-break value for narrower signatures.

        Source: ``GAS_WIKI §10.5``.
        """
        if self.specificity == float("inf"):
            return _SCORE_ZERO
        return _SCORE_ONE / self.specificity


_CEILING: dict[tuple[MatchType, str], float] = {
    (MatchType.DEFINITIVE, _DNA_HIGH): 0.90,  # wiki: GAS_WIKI §10.5
    (MatchType.DEFINITIVE, _DNA_PARTIAL): 0.69,  # wiki: GAS_WIKI §10.5
    (MatchType.DEFINITIVE, _DNA_NONE): 0.60,  # wiki: GAS_WIKI §10.5
    (MatchType.SPECIFIC, _DNA_HIGH): 0.80,  # wiki: GAS_WIKI §10.5
    (MatchType.SPECIFIC, _DNA_PARTIAL): 0.62,  # wiki: GAS_WIKI §10.5
    (MatchType.SPECIFIC, _DNA_NONE): 0.53,  # wiki: GAS_WIKI §10.5
    (MatchType.CATCH_ALL, _DNA_HIGH): 0.55,  # wiki: GAS_WIKI §10.5
    (MatchType.CATCH_ALL, _DNA_PARTIAL): 0.42,  # wiki: GAS_WIKI §10.5
    (MatchType.CATCH_ALL, _DNA_NONE): 0.37,  # wiki: GAS_WIKI §10.5
    (MatchType.FALLBACK, _DNA_HIGH): 0.50,  # wiki: GAS_WIKI §10.5
    (MatchType.FALLBACK, _DNA_PARTIAL): 0.38,  # wiki: GAS_WIKI §10.5
    (MatchType.FALLBACK, _DNA_NONE): 0.33,  # wiki: GAS_WIKI §10.5
}


def _dna_tier(dna: GasLabDnaView) -> str:
    """Return the DNA confidence tier used by the ceiling table.

    Source: ``GAS_WIKI §10.1`` and ``GAS_WIKI §10.5``.
    """
    tier = dna.confidence.upper()
    if tier in {_DNA_HIGH, _DNA_PARTIAL, _DNA_NONE}:
        return tier
    return _DNA_NONE


def _clamped_confidence(candidate: CandidateScore, dna_tier: str) -> float:
    """Return the candidate confidence after the GAS_WIKI §10.5 ceiling clamp."""
    ceiling = _CEILING[(candidate.match_type, dna_tier)]
    return max(_SCORE_ZERO, min(candidate.raw_score, ceiling))


def _family_sort_key(item: tuple[str, tuple[float, float]]) -> tuple[float, float, str]:
    """Return the deterministic top-3 family ordering key.

    Source: ``GAS_WIKI §10.5``.
    """
    family, (confidence, specificity_inverse) = item
    return (-confidence, -specificity_inverse, family)


def _match_type(name: str, faults: dict) -> MatchType:
    """Return the match type for an ontology candidate name.

    Source: ``GAS_WIKI §10.5``.
    """
    if faults.get(name, {}).get("signature_type") == "catch_all":
        return MatchType.CATCH_ALL
    return MatchType.SPECIFIC


def _corroborating_channels(name: str, reading: GasReading, faults: dict) -> int:
    """Count diagnostic gas channels that corroborate a matched candidate.

    A channel corroborates when the reading is inside the candidate band and the
    band is narrower than the analyser envelope declared by ``SAMPLE_INVALID``.
    Source: ``GAS_WIKI §5`` and ``GAS_WIKI §10.5``.
    """
    entry = faults.get(name)
    envelope = faults.get(ChemicalSignature.SAMPLE_INVALID.value, {}).get("signature", {})
    if entry is None or not envelope:
        return 0

    values = _signature_values(reading)
    signature = entry["signature"]
    count = 0
    for gas_key in _GAS_KEYS:
        bounds = signature[gas_key]
        envelope_bounds = envelope[gas_key]
        is_inside = bounds["min"] <= values[gas_key] <= bounds["max"]
        is_diagnostic = (
            bounds["min"] > envelope_bounds["min"]
            or bounds["max"] < envelope_bounds["max"]
        )
        if is_inside and is_diagnostic:
            count += 1
    return count


def _raw_score(specificity: float, corroborating_channels: int) -> float:
    """Return the unclamped evidence score for a candidate.

    Source: ``GAS_WIKI §10.5``.
    """
    if specificity == float("inf"):
        return _SCORE_ZERO
    return (corroborating_channels / len(_GAS_KEYS)) + (_SCORE_ONE / specificity)  # wiki: GAS_WIKI §10.5


def _candidate_score(
    name: str,
    match_type: MatchType,
    reading: GasReading,
    faults: dict,
) -> CandidateScore:
    """Build a ``CandidateScore`` from an ontology candidate name.

    Source: ``GAS_WIKI §10.5``.
    """
    specificity = _specificity(name, faults)
    corroborating_channels = _corroborating_channels(name, reading, faults)
    return CandidateScore(
        signature=ChemicalSignature(name),
        match_type=match_type,
        specificity=specificity,
        corroborating_channels=corroborating_channels,
        raw_score=_raw_score(specificity, corroborating_channels),
    )


def _fallback_score() -> CandidateScore:
    """Return the absence-of-match fallback candidate.

    Source: ``GAS_WIKI §10.5``.
    """
    return CandidateScore(
        signature=ChemicalSignature.NORMAL_OPERATION,
        match_type=MatchType.FALLBACK,
        specificity=float("inf"),
        corroborating_channels=0,
        raw_score=_SCORE_ZERO,
    )


def _sort_key(candidate: CandidateScore) -> tuple[float, float, str]:
    """Return the deterministic candidate ordering key.

    Source: ``GAS_WIKI §10.5``.
    """
    return (-candidate.raw_score, -candidate.specificity_inverse, candidate.signature.value)


def rank_candidates(
    reading: GasReading,
    dna: GasLabDnaView,
    engine_state: EngineStateBucket,
    ontology: dict,
    block_test_passed: bool = False,
    reading_high: GasReading | None = None,
) -> list[CandidateScore]:
    """Return all surviving GASLab candidates ordered by raw evidence score.

    Source: ``GAS_WIKI §10.5``.
    """
    faults = ontology.get("faults", {})

    definitive = _definitive_match(reading, dna, engine_state, ontology, block_test_passed, reading_high)
    if definitive is not None:
        signature, _validity = definitive
        if signature.value not in faults:
            return [
                CandidateScore(
                    signature=signature,
                    match_type=MatchType.DEFINITIVE,
                    specificity=float("inf"),
                    corroborating_channels=0,
                    raw_score=_SCORE_ZERO,
                )
            ]
        return [_candidate_score(signature.value, MatchType.DEFINITIVE, reading, faults)]

    candidates = _matching_fault_candidates(reading, engine_state, ontology)
    candidates = _resolve_candidates(candidates, reading, dna, ontology, engine_state, reading_high)
    if not candidates:
        return [_fallback_score()]

    ranked = [
        _candidate_score(name, _match_type(name, faults), reading, faults)
        for name in sorted(candidates, key=lambda candidate: _candidate_rank(candidate, faults))
    ]
    return sorted(ranked, key=_sort_key)


def classify_top3(
    reading: GasReading,
    dna: GasLabDnaView,
    engine_state: EngineStateBucket,
    ontology: dict,
    block_test_passed: bool = False,
    reading_high: GasReading | None = None,
) -> list[tuple[str, float]]:
    """Return up to three canonical families with GASLab confidence scores.

    Source: ``GAS_WIKI §10.5`` and ``GASLabSimple/DESIGN_percent_sourcing.md §7``.
    """
    dna_tier = _dna_tier(dna)
    by_family: dict[str, tuple[float, float]] = {}

    for candidate in rank_candidates(
        reading,
        dna,
        engine_state,
        ontology,
        block_test_passed,
        reading_high,
    ):
        family = SIGNATURE_TO_FAMILY[candidate.signature]
        row = (
            _clamped_confidence(candidate, dna_tier),
            candidate.specificity_inverse,
        )
        if family not in by_family or row > by_family[family]:
            by_family[family] = row

    ordered = sorted(by_family.items(), key=_family_sort_key)
    return [
        (family, confidence)
        for family, (confidence, _specificity_inverse) in ordered[:_TOP3_LIMIT]
    ]
