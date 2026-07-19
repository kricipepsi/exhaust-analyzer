"""Tests for GASLab top-3 family emission."""

from __future__ import annotations

from copy import deepcopy

import pytest

import gaslab.ranking as ranking
from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.family_map import CANONICAL_FAMILIES
from gaslab.ontology_loader import load_ontology
from gaslab.ranking import CandidateScore, MatchType


@pytest.fixture(scope="module")
def ontology() -> dict:
    """Load the production ontology once for classify_top3 tests."""
    return load_ontology()


def _dna(**overrides: object) -> GasLabDnaView:
    """Build a minimal valid ``GasLabDnaView`` with optional overrides."""
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT",
        induction_type="NA",
        upstream_o2_type="WIDEBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


def _reading(**overrides: object) -> GasReading:
    """Build a nominal ``GasReading`` with optional overrides."""
    defaults: dict[str, object] = dict(
        hc=15,
        co=0.2,
        co2=15.0,
        o2=0.2,
        nox=50,
    )
    defaults.update(overrides)
    return GasReading(**defaults)  # type: ignore[arg-type]


def _candidate(
    signature: ChemicalSignature,
    *,
    match_type: MatchType = MatchType.SPECIFIC,
    specificity: float = 2.0,
    raw_score: float = 0.8,
) -> CandidateScore:
    """Build a ranked candidate for isolated top-3 behavior tests."""
    return CandidateScore(
        signature=signature,
        match_type=match_type,
        specificity=specificity,
        corroborating_channels=5,
        raw_score=raw_score,
    )


def test_returns_at_most_three(ontology: dict) -> None:
    """Top-3 emission returns no more than three family rows."""
    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert len(result) <= 3


def test_confidences_in_unit_interval(ontology: dict) -> None:
    """Every top-3 confidence is inside the closed unit interval."""
    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert all(0.0 <= confidence <= 1.0 for _family, confidence in result)


def test_ceiling_clamp_applied(monkeypatch: pytest.MonkeyPatch, ontology: dict) -> None:
    """The GAS_WIKI §10.5 ceiling clamps the emitted confidence."""
    monkeypatch.setattr(
        ranking,
        "rank_candidates",
        lambda *args, **kwargs: [
            _candidate(
                ChemicalSignature.RICH_MIXTURE,
                match_type=MatchType.DEFINITIVE,
                raw_score=2.0,
            )
        ],
    )

    high = ranking.classify_top3(
        _reading(),
        _dna(confidence="HIGH"),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )
    none = ranking.classify_top3(
        _reading(),
        _dna(confidence="NONE"),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert high == [("rich_mixture", 0.9)]
    assert none == [("rich_mixture", 0.6)]


def test_family_dedup_keeps_max(monkeypatch: pytest.MonkeyPatch, ontology: dict) -> None:
    """Multiple signatures in one family collapse to the highest confidence."""
    monkeypatch.setattr(
        ranking,
        "rank_candidates",
        lambda *args, **kwargs: [
            _candidate(ChemicalSignature.WORN_ENGINE, raw_score=0.3),
            _candidate(ChemicalSignature.WORN_PISTON_RINGS, raw_score=0.7),
        ],
    )

    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert result == [("mechanical_wear", 0.7)]


def test_families_are_canonical(ontology: dict) -> None:
    """Every emitted family belongs to the canonical fusion vocabulary."""
    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert all(family in CANONICAL_FAMILIES for family, _confidence in result)


def test_tie_break_deterministic(monkeypatch: pytest.MonkeyPatch, ontology: dict) -> None:
    """Equal confidence ties break by specificity, then family name."""
    monkeypatch.setattr(
        ranking,
        "rank_candidates",
        lambda *args, **kwargs: [
            _candidate(ChemicalSignature.RICH_MIXTURE, specificity=4.0, raw_score=0.4),
            _candidate(ChemicalSignature.LEAN_MIXTURE, specificity=2.0, raw_score=0.4),
            _candidate(ChemicalSignature.NORMAL_OPERATION, specificity=2.0, raw_score=0.4),
        ],
    )

    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert result == [
        ("lean_condition", 0.4),
        ("no_fault", 0.4),
        ("rich_mixture", 0.4),
    ]


def test_fallback_emits_no_fault(ontology: dict) -> None:
    """A no-match reading emits the no_fault family under the fallback ceiling."""
    no_match_ontology = deepcopy(ontology)
    no_match_ontology["faults"] = {}

    result = ranking.classify_top3(
        _reading(hc=900, co=0.2, co2=14.0, o2=0.2, nox=900),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        no_match_ontology,
    )

    assert len(result) == 1
    assert result[0][0] == "no_fault"
    assert result[0][1] <= 0.5


def test_does_not_normalise_to_one(
    monkeypatch: pytest.MonkeyPatch,
    ontology: dict,
) -> None:
    """GASLab emits independent confidences without sum-1 normalisation."""
    monkeypatch.setattr(
        ranking,
        "rank_candidates",
        lambda *args, **kwargs: [
            _candidate(ChemicalSignature.RICH_MIXTURE, raw_score=0.8),
            _candidate(ChemicalSignature.LEAN_MIXTURE, raw_score=0.8),
            _candidate(ChemicalSignature.NORMAL_OPERATION, raw_score=0.8),
        ],
    )

    result = ranking.classify_top3(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert sum(confidence for _family, confidence in result) > 1.0
