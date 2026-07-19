"""DNA view schema drift guard (T-P0-2).

Verifies DtcLabDnaView, DtcEmissionsView, and the four mirror enums in
dtclab/schemas/dna_view.py match DTC_VOCABULARY.md §14.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from dtclab.schemas.dna_view import (
    AirMeteringStrategy,
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
    VinConfidence,
)

VOCAB_PATH = (
    Path(__file__).parent.parent.parent
    / "docs" / "DTC_VOCABULARY.md"
)
VOCAB = VOCAB_PATH.read_text(encoding="utf-8")


# =============================================================================
# Field-count tests
# =============================================================================


def test_dna_view_fields():
    """DtcLabDnaView must have all 8 canonical fields from DTC_VOCABULARY.md §14."""
    expected = {
        "make",
        "model",
        "model_year",
        "euro_emission_category",
        "air_metering_strategy",
        "resolved_horizon",
        "emissions",
        "confidence",
    }
    assert set(DtcLabDnaView.model_fields) == expected


def test_emissions_view_fields():
    """DtcEmissionsView must have the 2 bool flags from DTC_VOCABULARY.md §14."""
    expected = {
        "has_catalyst",
        "egr_equipped",
    }
    assert set(DtcEmissionsView.model_fields) == expected


# =============================================================================
# Enum count tests
# =============================================================================


def test_euro_emission_category_count():
    """EuroEmissionCategory must have 8 values per DTC_VOCABULARY.md §14.1."""
    assert len(list(EuroEmissionCategory)) == 8


def test_air_metering_strategy_count():
    """AirMeteringStrategy must have 3 values per DTC_VOCABULARY.md §14.1."""
    assert len(list(AirMeteringStrategy)) == 3


def test_resolved_horizon_count():
    """ResolvedHorizon must have 3 values per DTC_VOCABULARY.md §14.1."""
    assert len(list(ResolvedHorizon)) == 3


def test_vin_confidence_count():
    """VinConfidence must have 3 values per DTC_VOCABULARY.md §14.1."""
    assert len(list(VinConfidence)) == 3


# =============================================================================
# Enum value tests
# =============================================================================


def test_confidence_values():
    """VinConfidence must expose HIGH, PARTIAL, NONE per DTC_VOCABULARY.md §14.1."""
    assert set(VinConfidence) == {"HIGH", "PARTIAL", "NONE"}


# =============================================================================
# Drift guard — every enum value must appear verbatim in the wiki
# =============================================================================

DNA_VIEW_ENUMS = [
    (EuroEmissionCategory, 8),
    (AirMeteringStrategy, 3),
    (ResolvedHorizon, 3),
    (VinConfidence, 3),
]


@pytest.mark.parametrize(("enum_cls", "expected_count"), DNA_VIEW_ENUMS)
def test_dna_view_drift_guard(enum_cls, expected_count):
    """Every DNA-view enum value must appear verbatim in DTC_VOCABULARY.md."""
    members = list(enum_cls)
    assert len(members) == expected_count, (
        f"{enum_cls.__name__} has {len(members)} members; "
        f"expected {expected_count}"
    )
    for member in enum_cls:
        assert member.value in VOCAB, (
            f"{enum_cls.__name__}.{member.name} = {member.value!r} "
            f"not found in DTC_VOCABULARY.md"
        )


# =============================================================================
# model_validate round-trip
# =============================================================================


def test_model_validate_round_trip_high_confidence():
    """DtcLabDnaView must round-trip through model_validate with all fields."""
    view = DtcLabDnaView.model_validate(
        {
            "make": "Toyota",
            "model": "Corolla",
            "model_year": 2010,
            "euro_emission_category": "EURO_4",
            "air_metering_strategy": "MAF",
            "resolved_horizon": "HORIZON_CLASSIC",
            "emissions": {
                "has_catalyst": True,
                "egr_equipped": False,
},
            "confidence": "HIGH",
        }
    )
    assert view.make == "Toyota"
    assert view.model == "Corolla"
    assert view.model_year == 2010
    assert view.euro_emission_category == EuroEmissionCategory.EURO_4
    assert view.air_metering_strategy == AirMeteringStrategy.MAF
    assert view.resolved_horizon == ResolvedHorizon.HORIZON_CLASSIC
    assert view.emissions.has_catalyst is True
    assert view.emissions.egr_equipped is False
    assert view.confidence == VinConfidence.HIGH


def test_model_validate_with_none_confidence():
    """DtcLabDnaView must accept confidence=NONE (no-DNA fallback)."""
    view = DtcLabDnaView.model_validate(
        {
            "make": "Ford",
            "model": "Focus",
            "model_year": 2005,
            "euro_emission_category": "EURO_3",
            "air_metering_strategy": "MAF",
            "resolved_horizon": "HORIZON_CLASSIC",
            "emissions": {
                "has_catalyst": True,
                "egr_equipped": True,
},
            "confidence": "NONE",
        }
    )
    assert view.confidence == VinConfidence.NONE


def test_import_is_local():
    """DtcLabDnaView must be importable from dtclab.schemas.dna_view only."""
    import dtclab.schemas.dna_view as dv

    assert dv.DtcLabDnaView is DtcLabDnaView
    assert dv.DtcEmissionsView is DtcEmissionsView
