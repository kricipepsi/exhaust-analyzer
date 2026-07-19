"""Unit tests for comlab.projection and comlab.schemas.lab_dna_views.

Covers T-P2-2 success criteria:
  - project(target='gas') returns correct GasLabDnaView
  - project(target='obd') returns correct ObdLabDnaView
  - project(target='dtc') returns correct DtcLabDnaView
  - project_all() returns ProjectedViews with all three views populated
  - ValidationError raised for a missing required field
  - Frozen mutation raises ValidationError
  - Horizon fallback from euro_emission_category when resolved_horizon absent
"""

from __future__ import annotations

import copy

import pytest
from pydantic import ValidationError

from comlab.projection import _horizon_from_euro, project, project_all
from comlab.schemas.lab_dna_views import (
    DtcLabDnaView,
    GasLabDnaView,
    ObdLabDnaView,
    ProjectedViews,
)
from comlab.schemas.vocabulary import Horizon


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def modern_vehicle_dna() -> dict:
    """Full VehicleDNA dict for a Euro 5 GDI vehicle — all fields present.

    CoC empirical fields (target_lambda_v112, co_low_idle, co_high_idle)
    live at top-level vin_dna per the upstream vinlab/DNALab contract.
    Only equipment flags (upstream_o2_type, downstream_o2_present,
    has_catalyst, egr_equipped) sit under nested ``emissions``.
    """
    return {
        "vin_dna": {
            "engine_displacement_liters": 2.0,
            "cylinder_count": 4,
            "number_of_banks": 1,
            "euro_emission_category": "EURO_5",
            "fuel_delivery_type": "GDI",
            "induction_type": "TURBOCHARGED",
            "upstream_o2_type": "WIDEBAND_LAMBDA",
            "has_catalyst": True,
            "egr_equipped": True,
            "confidence": "HIGH",
            "resolved_horizon": "HORIZON_MODERN",
            "make": "BMW",
            "model": "320i",
            "model_year": 2015,
            "rated_rpm": 6500,
            "stress_idle_rpm_target": 4000,
            "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
            # CoC empirical targets — top level per upstream vinlab.models.VinDNA
            # (T-COMV2-LAMBDAPROJ-1 / DEP-4)
            "target_lambda_v112": 1.0,
            "co_low_idle": 0.5,
            "co_high_idle": 0.3,

            "emissions": {
                "upstream_o2_type": "WIDEBAND_LAMBDA",
                "downstream_o2_present": True,
                "has_catalyst": True,
                "egr_equipped": True,
            },
        }
    }


@pytest.fixture
def legacy_vehicle_dna_no_horizon() -> dict:
    """Euro 1 vehicle with no resolved_horizon — tests fallback path."""
    return {
        "vin_dna": {
            "engine_displacement_liters": 1.6,
            "cylinder_count": 4,
            "number_of_banks": 1,
            "euro_emission_category": "EURO_1",
            "fuel_delivery_type": "CARBURETOR",
            "induction_type": "NATURALLY_ASPIRATED",
            "upstream_o2_type": "NONE",
            "has_catalyst": False,
            "egr_equipped": False,
            "confidence": "PARTIAL",
            "make": "FIAT",
            "model": "Uno",
            "model_year": 1994,
            "rated_rpm": None,
            "stress_idle_rpm_target": None,
            "air_metering_strategy": "MAP_ONLY_SPEED_DENSITY",

            # No resolved_horizon — triggers _horizon_from_euro fallback
        }
    }


# ---------------------------------------------------------------------------
# project() — per-target projection
# ---------------------------------------------------------------------------


def test_project_gas_modern(modern_vehicle_dna: dict) -> None:
    result = project(modern_vehicle_dna, target="gas")
    assert isinstance(result, GasLabDnaView)
    assert result.engine_displacement_liters == 2.0
    assert result.cylinder_count == 4
    assert result.number_of_banks == 1
    assert result.euro_emission_category == "EURO_5"
    assert result.fuel_delivery_type == "GDI"
    assert result.induction_type == "TURBOCHARGED"
    assert result.upstream_o2_type == "WIDEBAND_LAMBDA"
    assert result.has_catalyst is True
    assert result.egr_equipped is True
    assert result.target_lambda_v112 == 1.0
    assert result.co_low_idle == 0.5
    assert result.co_high_idle == 0.3
    assert result.confidence == "HIGH"
    assert result.resolved_horizon == "HORIZON_MODERN"


def test_project_obd_modern(modern_vehicle_dna: dict) -> None:
    result = project(modern_vehicle_dna, target="obd")
    assert isinstance(result, ObdLabDnaView)
    assert result.engine_displacement_liters == 2.0
    assert result.cylinder_count == 4
    assert result.rated_rpm == 6500
    assert result.stress_idle_rpm_target == 4000
    assert result.air_metering_strategy == "DUAL_MAF_MAP_CROSSCHECK"
    assert result.upstream_o2_type == "WIDEBAND_LAMBDA"
    assert result.induction_type == "TURBOCHARGED"
    assert result.egr_equipped is True
    assert result.resolved_horizon == "HORIZON_MODERN"
    assert result.confidence == "HIGH"


def test_project_dtc_modern(modern_vehicle_dna: dict) -> None:
    result = project(modern_vehicle_dna, target="dtc")
    assert isinstance(result, DtcLabDnaView)
    assert result.make == "BMW"
    assert result.model_year == 2015
    assert result.euro_emission_category == "EURO_5"
    assert result.air_metering_strategy == "DUAL_MAF_MAP_CROSSCHECK"
    assert result.resolved_horizon == "HORIZON_MODERN"

    assert result.has_catalyst is True
    assert result.egr_equipped is True
    assert result.confidence == "HIGH"


def test_project_dtc_does_not_require_model(modern_vehicle_dna: dict) -> None:
    dna = copy.deepcopy(modern_vehicle_dna)
    del dna["vin_dna"]["model"]
    result = project(dna, target="dtc")
    assert isinstance(result, DtcLabDnaView)
    assert not hasattr(result, "model")


def test_project_obd_nullable_fields(modern_vehicle_dna: dict) -> None:
    """ObdLabDnaView has Optional fields that may be None from older payloads."""
    dna = copy.deepcopy(modern_vehicle_dna)
    dna["vin_dna"]["rated_rpm"] = None
    dna["vin_dna"]["stress_idle_rpm_target"] = None
    result = project(dna, target="obd")
    assert isinstance(result, ObdLabDnaView)
    assert result.rated_rpm is None
    assert result.stress_idle_rpm_target is None


# ---------------------------------------------------------------------------
# project_all()
# ---------------------------------------------------------------------------


def test_project_all_returns_all_three_views(modern_vehicle_dna: dict) -> None:
    result = project_all(modern_vehicle_dna)
    assert isinstance(result, ProjectedViews)
    assert isinstance(result.gas, GasLabDnaView)
    assert isinstance(result.obd, ObdLabDnaView)
    assert isinstance(result.dtc, DtcLabDnaView)


# ---------------------------------------------------------------------------
# ValidationError — missing required field
# ---------------------------------------------------------------------------


def test_missing_required_field_raises_validation_error() -> None:
    """Missing a Pydantic-required field (not a pre-extracted one) raises."""
    dna: dict[str, dict] = {
        "vin_dna": {
            "euro_emission_category": "EURO_5",
            "confidence": "HIGH",
            "resolved_horizon": "HORIZON_MODERN",
            # engine_displacement_liters intentionally missing
        }
    }
    with pytest.raises(ValidationError):
        project(dna, target="gas")


def test_missing_make_in_dtc_view_raises(modern_vehicle_dna: dict) -> None:
    dna = copy.deepcopy(modern_vehicle_dna)
    del dna["vin_dna"]["make"]
    with pytest.raises(ValidationError):
        project(dna, target="dtc")


# ---------------------------------------------------------------------------
# Frozen mutation raises
# ---------------------------------------------------------------------------


def test_gas_view_frozen_mutation_raises(modern_vehicle_dna: dict) -> None:
    view = project(modern_vehicle_dna, target="gas")
    with pytest.raises(ValidationError):
        view.engine_displacement_liters = 3.0  # type: ignore[misc]


def test_obd_view_frozen_mutation_raises(modern_vehicle_dna: dict) -> None:
    view = project(modern_vehicle_dna, target="obd")
    with pytest.raises(ValidationError):
        view.cylinder_count = 8  # type: ignore[misc]


def test_dtc_view_frozen_mutation_raises(modern_vehicle_dna: dict) -> None:
    view = project(modern_vehicle_dna, target="dtc")
    with pytest.raises(ValidationError):
        view.make = "Toyota"  # type: ignore[misc]


def test_projected_views_frozen_mutation_raises(modern_vehicle_dna: dict) -> None:
    views = project_all(modern_vehicle_dna)
    with pytest.raises(ValidationError):
        views.gas = views.gas  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Horizon fallback
# ---------------------------------------------------------------------------


def test_horizon_fallback_legacy(legacy_vehicle_dna_no_horizon: dict) -> None:
    result = project(legacy_vehicle_dna_no_horizon, target="gas")
    assert result.resolved_horizon == "HORIZON_LEGACY"


def test_horizon_fallback_euro3_to_adaptive(modern_vehicle_dna: dict) -> None:
    dna = copy.deepcopy(modern_vehicle_dna)
    del dna["vin_dna"]["resolved_horizon"]
    dna["vin_dna"]["euro_emission_category"] = "EURO_3"
    result = project(dna, target="gas")
    assert result.resolved_horizon == "HORIZON_ADAPTIVE"


def test_horizon_fallback_euro7_to_modern(modern_vehicle_dna: dict) -> None:
    dna = copy.deepcopy(modern_vehicle_dna)
    del dna["vin_dna"]["resolved_horizon"]
    dna["vin_dna"]["euro_emission_category"] = "EURO_7"
    result = project(dna, target="gas")
    assert result.resolved_horizon == "HORIZON_MODERN"


# ---------------------------------------------------------------------------
# _horizon_from_euro unit
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "euro, expected",
    [
        ("EURO_1", Horizon.LEGACY),
        ("EURO_2", Horizon.LEGACY),
        ("EURO_3", Horizon.ADAPTIVE),
        ("EURO_4", Horizon.ADAPTIVE),
        ("EURO_5", Horizon.MODERN),
        ("EURO_6", Horizon.MODERN),
        ("EURO_7", Horizon.MODERN),
    ],
)
def test_horizon_from_euro_mapping(euro: str, expected: str) -> None:
    assert _horizon_from_euro(euro) == expected


# ---------------------------------------------------------------------------
# T-COMV2-LAMBDAPROJ-1 — CoC λ projection-path reconcile (DEP-4)
# ---------------------------------------------------------------------------


def test_projection_lambda_paths_land_from_top_level() -> None:
    """CoC fields at vin_dna top level → GasLabDnaView carries real values.

    Before the DEP-4 fix these were read from ``emissions.get()`` which
    the upstream DNALab contract does not populate them in → always None.
    """
    dna: dict[str, dict] = {
        "vin_dna": {
            "engine_displacement_liters": 2.0,
            "cylinder_count": 4,
            "number_of_banks": 1,
            "euro_emission_category": "EURO_5",
            "fuel_delivery_type": "GDI",
            "induction_type": "TURBOCHARGED",
            "upstream_o2_type": "WIDEBAND_LAMBDA",
            "has_catalyst": True,
            "egr_equipped": True,
            "confidence": "HIGH",
            "resolved_horizon": "HORIZON_MODERN",
            # CoC fields at top level per vinlab contract
            "target_lambda_v112": 1.005,
            "co_low_idle": 0.20,
            "co_high_idle": 0.15,
            # emissions carries only equipment flags
            "emissions": {
                "upstream_o2_type": "WIDEBAND_LAMBDA",
                "downstream_o2_present": True,
                "has_catalyst": True,
                "egr_equipped": True,
            },
        }
    }
    view = project(dna, target="gas")
    assert isinstance(view, GasLabDnaView)
    assert view.target_lambda_v112 == 1.005
    assert view.co_low_idle == 0.20
    assert view.co_high_idle == 0.15


def test_projection_lambda_absent_returns_none() -> None:
    """When CoC fields are absent from the payload → GasLabDnaView gets None."""
    dna: dict[str, dict] = {
        "vin_dna": {
            "engine_displacement_liters": 2.0,
            "cylinder_count": 4,
            "number_of_banks": 1,
            "euro_emission_category": "EURO_5",
            "fuel_delivery_type": "GDI",
            "induction_type": "TURBOCHARGED",
            "upstream_o2_type": "WIDEBAND_LAMBDA",
            "has_catalyst": True,
            "egr_equipped": True,
            "confidence": "HIGH",
            "resolved_horizon": "HORIZON_MODERN",
            "emissions": {},
            # No target_lambda_v112, co_low_idle, co_high_idle at top level
        }
    }
    view = project(dna, target="gas")
    assert isinstance(view, GasLabDnaView)
    assert view.target_lambda_v112 is None
    assert view.co_low_idle is None
    assert view.co_high_idle is None


def test_projection_equipment_flags_unchanged() -> None:
    """Equipment flags under emissions.* still project correctly.

    The DEP-4 fix is surgical — it re-points only the CoC λ reads;
    equipment flags were never moved and must keep their existing paths.
    """
    dna: dict[str, dict] = {
        "vin_dna": {
            "engine_displacement_liters": 2.0,
            "cylinder_count": 4,
            "number_of_banks": 1,
            "euro_emission_category": "EURO_5",
            "fuel_delivery_type": "GDI",
            "induction_type": "TURBOCHARGED",
            "upstream_o2_type": "WIDEBAND_LAMBDA",
            "has_catalyst": True,
            "egr_equipped": True,
            "confidence": "HIGH",
            "resolved_horizon": "HORIZON_MODERN",
            "emissions": {},
        }
    }
    view = project(dna, target="gas")
    assert isinstance(view, GasLabDnaView)
    assert view.has_catalyst is True
    assert view.egr_equipped is True
