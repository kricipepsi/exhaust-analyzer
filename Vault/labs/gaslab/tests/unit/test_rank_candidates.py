"""Tests for ranked GASLab candidates."""

from __future__ import annotations

from copy import deepcopy

import pytest

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.ranking import MatchType, rank_candidates
from gaslab.rule_engine import classify


@pytest.fixture(scope="module")
def ontology() -> dict:
    """Load the production ontology once for ranking tests."""
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
        hc=15, co=0.2, co2=15.0, o2=0.2, nox=50,
    )
    defaults.update(overrides)
    return GasReading(**defaults)  # type: ignore[arg-type]


def test_returns_all_matching_candidates(ontology: dict) -> None:
    """A multi-match reading returns every survivor, not only the winner."""
    candidates = rank_candidates(
        _reading(),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    signatures = {candidate.signature for candidate in candidates}

    assert ChemicalSignature.NORMAL_OPERATION in signatures
    assert ChemicalSignature.TIMING_RETARDED in signatures
    assert ChemicalSignature.FLAT_CAMSHAFT in signatures
    assert ChemicalSignature.WORN_PISTON_RINGS in signatures
    assert ChemicalSignature.VVT_FAILURE in signatures
    assert len(candidates) >= 5


def test_match_type_definitive_for_grammar_override(ontology: dict) -> None:
    """A named grammar override yields one DEFINITIVE candidate."""
    candidates = rank_candidates(
        _reading(hc=1500, co=0.2, co2=10.0, o2=5.0, nox=30),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert [(candidate.signature, candidate.match_type) for candidate in candidates] == [
        (ChemicalSignature.IGNITION_MISFIRE, MatchType.DEFINITIVE),
    ]


def test_match_type_catch_all_for_poa_vvt(ontology: dict) -> None:
    """A POA/VVT catch-all match is tagged as CATCH_ALL."""
    candidates = rank_candidates(
        _reading(hc=600, co=0.2, co2=13.7, o2=0.2, nox=100),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )

    assert candidates[0].signature == ChemicalSignature.POA_SIGNATURE
    assert candidates[0].match_type == MatchType.CATCH_ALL
    assert {candidate.match_type for candidate in candidates} == {MatchType.CATCH_ALL}


def test_match_type_fallback_when_no_candidate(ontology: dict) -> None:
    """No bound match yields NORMAL_OPERATION as a FALLBACK candidate."""
    no_match_ontology = deepcopy(ontology)
    no_match_ontology["faults"] = {}

    candidates = rank_candidates(
        _reading(hc=900, co=0.2, co2=14.0, o2=0.2, nox=900),
        _dna(),
        EngineStateBucket.STABILIZED_IDLE,
        no_match_ontology,
    )

    assert [(candidate.signature, candidate.match_type) for candidate in candidates] == [
        (ChemicalSignature.NORMAL_OPERATION, MatchType.FALLBACK),
    ]


def test_raw_score_monotone_in_corroboration(ontology: dict) -> None:
    """For SPECIFIC candidates, more corroborating channels means higher score."""
    candidates = rank_candidates(
        _reading(hc=250, co=0.8, co2=13.0, o2=0.4, nox=80),
        _dna(egr_equipped=True),
        EngineStateBucket.STABILIZED_IDLE,
        ontology,
    )
    by_signature = {candidate.signature: candidate for candidate in candidates}

    rich = by_signature[ChemicalSignature.RICH_MIXTURE]
    egr_open = by_signature[ChemicalSignature.EGR_STUCK_OPEN]

    assert rich.match_type == MatchType.SPECIFIC
    assert egr_open.match_type == MatchType.SPECIFIC
    assert rich.corroborating_channels > egr_open.corroborating_channels
    assert rich.raw_score > egr_open.raw_score


def test_ordering_deterministic(ontology: dict) -> None:
    """Ordering is stable and follows the exact ranking key."""
    reading = _reading()
    dna = _dna()

    first = rank_candidates(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)
    second = rank_candidates(reading, dna, EngineStateBucket.STABILIZED_IDLE, ontology)

    assert first == second
    assert first == sorted(
        first,
        key=lambda candidate: (
            -candidate.raw_score,
            -candidate.specificity_inverse,
            candidate.signature.value,
        ),
    )


def test_classify_single_verdict_unchanged(ontology: dict) -> None:
    """The existing single-verdict API remains unchanged."""
    result = classify(_reading(), _dna(), EngineStateBucket.STABILIZED_IDLE, ontology)

    assert result == (ChemicalSignature.NORMAL_OPERATION, SampleValidity.VALID)
