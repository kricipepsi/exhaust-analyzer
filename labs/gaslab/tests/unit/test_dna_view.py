"""Tests for gaslab.dna_view — GasLabDnaView slim DNA projection."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from gaslab.dna_view import GasLabDnaView


# ---------------------------------------------------------------------------
# Required fields — GAS_WIKI §2.4
# ---------------------------------------------------------------------------


def test_gas_lab_dna_view_required_fields() -> None:
    """All 13 fields from GAS_WIKI §1.4 table are present and typed."""
    view = GasLabDnaView(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT_INJECTION",
        induction_type="NATURALLY_ASPIRATED",
        upstream_o2_type="ZIRCONIA",
        has_catalyst=True,
        egr_equipped=True,
        target_lambda_v112=1.000,
        co_low_idle=0.3,
        co_high_idle=0.3,
        confidence="HIGH",
    )
    assert view.engine_displacement_liters == 2.0
    assert view.cylinder_count == 4
    assert view.number_of_banks == 1
    assert view.euro_emission_category == "Euro 4"
    assert view.fuel_delivery_type == "PORT_INJECTION"
    assert view.induction_type == "NATURALLY_ASPIRATED"
    assert view.upstream_o2_type == "ZIRCONIA"
    assert view.has_catalyst is True
    assert view.egr_equipped is True
    assert view.target_lambda_v112 == 1.000
    assert view.co_low_idle == 0.3
    assert view.co_high_idle == 0.3
    assert view.confidence == "HIGH"


def test_gas_lab_dna_view_optional_fields_default() -> None:
    """Optional fields default to None when not provided."""
    view = GasLabDnaView(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT_INJECTION",
        induction_type="NATURALLY_ASPIRATED",
        upstream_o2_type="ZIRCONIA",
        has_catalyst=True,
        egr_equipped=True,
    )
    assert view.target_lambda_v112 is None
    assert view.co_low_idle is None
    assert view.co_high_idle is None
    assert view.confidence == "NONE"


def test_view_matches_wiki_s1_4() -> None:
    """Assert that GasLabDnaView fields exactly match the 13 fields in wiki §1.4."""
    fields = set(GasLabDnaView.model_fields.keys())
    assert "target_lambda_v112" in fields
    assert "co_high_idle" in fields
    assert "target_lambda_low" not in fields
    assert "target_lambda_high" not in fields
    assert "secondary_air_equipped" not in fields
    assert fields == {
        "engine_displacement_liters",
        "cylinder_count",
        "number_of_banks",
        "euro_emission_category",
        "fuel_delivery_type",
        "induction_type",
        "upstream_o2_type",
        "has_catalyst",
        "egr_equipped",
        "target_lambda_v112",
        "co_low_idle",
        "co_high_idle",
        "confidence",
    }



def test_gas_lab_dna_view_is_frozen() -> None:
    """Mutation must raise — frozen model."""
    view = GasLabDnaView(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT_INJECTION",
        induction_type="NATURALLY_ASPIRATED",
        upstream_o2_type="ZIRCONIA",
        has_catalyst=True,
        egr_equipped=True,
    )
    with pytest.raises(ValidationError):
        view.cylinder_count = 6  # type: ignore[misc]


def test_gas_lab_dna_view_rejects_negative_displacement() -> None:
    """engine_displacement_liters must be > 0."""
    with pytest.raises(ValidationError):
        GasLabDnaView(
            engine_displacement_liters=-0.5,
            cylinder_count=4,
            number_of_banks=1,
            euro_emission_category="Euro 4",
            fuel_delivery_type="PORT_INJECTION",
            induction_type="NATURALLY_ASPIRATED",
            upstream_o2_type="ZIRCONIA",
            has_catalyst=True,
            egr_equipped=True,
        )


def test_gas_lab_dna_view_rejects_invalid_lambda() -> None:
    """target_lambda_v112 must be in [0.5, 2.5] per GAS_VOCABULARY §6."""
    with pytest.raises(ValidationError):
        GasLabDnaView(
            engine_displacement_liters=2.0,
            cylinder_count=4,
            number_of_banks=1,
            euro_emission_category="Euro 4",
            fuel_delivery_type="PORT_INJECTION",
            induction_type="NATURALLY_ASPIRATED",
            upstream_o2_type="ZIRCONIA",
            has_catalyst=True,
            egr_equipped=True,
            target_lambda_v112=3.0,  # out of range
        )


def test_gas_lab_dna_view_rejects_invalid_cylinder_count() -> None:
    """cylinder_count must be in [1, 16]."""
    with pytest.raises(ValidationError):
        GasLabDnaView(
            engine_displacement_liters=2.0,
            cylinder_count=0,
            number_of_banks=1,
            euro_emission_category="Euro 4",
            fuel_delivery_type="PORT_INJECTION",
            induction_type="NATURALLY_ASPIRATED",
            upstream_o2_type="ZIRCONIA",
            has_catalyst=True,
            egr_equipped=True,
        )
