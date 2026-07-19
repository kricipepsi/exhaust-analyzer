"""DNALab test fixtures."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pytest
from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
)
from vinlab.models import (
    AirMeteringArchitecture,
    AirMeteringStrategy,
    Emissions,
    EuroEmissionCategory,
    FuelDeliveryType,
    Horizon,
    InductionType,
    PrimaryLoadCalculation,
    UpstreamO2Type,
    VinConfidence,
    VinDNA,
)

from dnalab.models import VehicleDNA


def make_vin_dna(**overrides: Any) -> VinDNA:
    defaults: dict[str, Any] = {
        "vin": "1FA6P8CF0HXXXXXXX",
        "make": "Ford",
        "model_year": 2017,
        "engine_displacement_liters": 2.3,
        "cylinder_count": 4,
        "number_of_banks": 1,
        "induction_type": InductionType.TURBOCHARGED,
        "fuel_delivery_type": FuelDeliveryType.GDI,
        "air_metering_architecture": AirMeteringArchitecture(
            has_maf_sensor=True,
            has_map_sensor=True,
            primary_load_calculation=PrimaryLoadCalculation.HYBRID_MAF_MAP,
        ),
        "emissions": Emissions(
            upstream_o2_type=UpstreamO2Type.WIDEBAND_AFR,
            downstream_o2_present=True,
            egr_equipped=False,
        ),
        "euro_emission_category": EuroEmissionCategory.EURO_6,
        "resolved_horizon": Horizon.MODERN,
        "stress_idle_rpm_target": 4500,
        "rated_rpm": 6500,
        "confidence": VinConfidence.HIGH,
        "air_metering_strategy": AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        "target_lambda_v112": 1.001,
        "target_rpm_u2": 3000,
        "idle_rpm_low": 760,
        "co_low_idle": 0.12,
        "co_high_idle": 0.08,
        "co_type_approval": 1.0,
        "hc_type_approval": 90.0,
        "nox_type_approval": 60.0,
        "hc_nox_type_approval": 120.0,
        "co2_type_approval": 168.0,
        "noise_stationary_dba": 82.0,
        "noise_rpm": 3750,
        "noise_driving_dba": 74.0,
    }
    defaults.update(overrides)
    return VinDNA(**defaults)


def make_symptom_dna(**overrides: Any) -> SymptomDNA:
    defaults: dict[str, Any] = {
        "tier_1_primary_symptom": "visible_exhaust_smoke",
        "tier_2_subfield_filter": "black_smoke",
        "environmental_conditions": EnvironmentalConditions(
            occurs_during=OccursDuring.ALWAYS,
            engine_state=EngineState.RUNNING,
            load_state=LoadState.TRANSIENT_ACCELERATION,
        ),
        "free_text_notes": "test note",
    }
    defaults.update(overrides)
    return SymptomDNA(**defaults)


def fake_decode_returning(vin_dna: VinDNA) -> Callable[[str], VinDNA]:
    def fake_decode(vin: str) -> VinDNA:
        return vin_dna

    return fake_decode


def fake_resolve_returning(symptom_dna: SymptomDNA) -> Callable[..., SymptomDNA]:
    def fake_resolve(**kwargs: Any) -> SymptomDNA:
        return symptom_dna

    return fake_resolve


@pytest.fixture(scope="session")
def sample_vin() -> str:
    return "VF1CB05CF25935016"


@pytest.fixture(scope="session")
def sample_triage() -> dict:
    return {
        "tier_1": "visible_exhaust_smoke",
        "tier_2": "black_smoke",          # SEMANTIC_CONTRACT.md §4.2
        "occurs_during": "always",
        "engine_state": "running",
        "load_state": "transient_acceleration",
    }


@pytest.fixture(scope="session")
def sample_dna() -> VehicleDNA:
    return VehicleDNA.new(make_vin_dna(), make_symptom_dna())


@pytest.fixture(scope="session")
def invalid_vin() -> str:
    return "XXXXXXXXXXXXXXX"
