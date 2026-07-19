"""Sanity tests for VinDNA instantiation and enum values."""

from __future__ import annotations

import inspect

from vinlab.models import (
    AirMeteringArchitecture,
    AirMeteringStrategy,
    DownstreamTrimRole,
    Emissions,
    EuroEmissionCategory,
    FuelDeliveryType,
    Horizon,
    InductionType,
    PrimaryLoadCalculation,
    UpstreamO2Type,
    VinConfidence,
    VinDNA,
    _derive_horizon_from_euro,
)


def test_vin_dna_instantiates_with_defaults():
    """VinDNA() with only vin= should succeed and have all-None CoC fields."""
    dna = VinDNA(vin="X" * 17)
    assert dna.vin == "X" * 17
    assert dna.make == ""
    assert not hasattr(dna, "model")
    assert dna.model_year is None
    assert dna.engine_displacement_liters == 0.0
    assert dna.cylinder_count == 0
    assert dna.number_of_banks == 1
    assert dna.induction_type == "NATURALLY_ASPIRATED"
    assert dna.fuel_delivery_type == "PORT_INJECTION"
    assert dna.euro_emission_category == "EURO_1"
    assert dna.resolved_horizon == "HORIZON_MODERN"
    assert dna.stress_idle_rpm_target == 3000
    assert dna.confidence == "NONE"
    assert dna.air_metering_strategy == "MAP_ONLY_SPEED_DENSITY"
    assert dna.rated_rpm is None
    # CoC fields are all None by default
    assert dna.target_lambda_v112 is None
    assert dna.target_rpm_u2 is None
    assert dna.co_type_approval is None
    assert dna.noise_rpm is None


def test_vin_dna_nested_defaults():
    """Nested AirMeteringArchitecture and Emissions have correct defaults."""
    dna = VinDNA(vin="1FA6P8CF0HXXXXXXX")
    assert dna.air_metering_architecture.has_maf_sensor is False
    assert dna.air_metering_architecture.has_map_sensor is False
    assert dna.air_metering_architecture.primary_load_calculation == "MAP_ONLY"
    assert dna.emissions.upstream_o2_type == "NARROWBAND"
    assert dna.emissions.downstream_o2_present is False
    assert dna.emissions.downstream_trim_role == "NONE"
    assert dna.emissions.egr_equipped is False


def test_vin_dna_to_json_contract_keys():
    """to_json() must include every key required by SEMANTIC_CONTRACT.md §4.1."""
    dna = VinDNA(vin="1FA6P8CF0HXXXXXXX")
    payload = dna.to_json_payload()
    required = {
        "vin", "make", "model_year",
        "engine_displacement_liters", "cylinder_count", "number_of_banks",
        "induction_type", "fuel_delivery_type",
        "air_metering_architecture", "emissions",
        "euro_emission_category", "resolved_horizon",
        "stress_idle_rpm_target",
        "air_metering_strategy", "confidence",
    }
    missing = required - set(payload.keys())
    assert not missing, f"Missing keys: {missing}"
    assert "model" not in payload
    assert set(payload["air_metering_architecture"].keys()) == {
        "has_maf_sensor", "has_map_sensor", "primary_load_calculation",
    }


def test_vin_dna_to_json_uses_canonical_coc_and_emissions_paths():
    """CoC fields stay top-level; emissions equipment stays under emissions."""
    dna = VinDNA(
        vin="1FA6P8CF0HXXXXXXX",
        emissions=Emissions(has_catalyst=False, egr_equipped=True),
        target_lambda_v112=1.003,
        co_low_idle=0.1,
        co_high_idle=0.2,
    )
    payload = dna.to_json_payload()

    assert payload["target_lambda_v112"] == 1.003
    assert payload["co_low_idle"] == 0.1
    assert payload["co_high_idle"] == 0.2
    assert "target_lambda_v112" not in payload["emissions"]
    assert "co_low_idle" not in payload["emissions"]
    assert "co_high_idle" not in payload["emissions"]
    assert "has_catalyst" not in payload
    assert payload["emissions"]["has_catalyst"] is False
    assert payload["emissions"]["egr_equipped"] is True

    round_tripped = VinDNA.from_json(payload)
    assert round_tripped.emissions.has_catalyst is False
    assert round_tripped.emissions.egr_equipped is True


def test_vin_dna_round_trips_rated_rpm():
    """rated_rpm serializes and deserializes with VinDNA."""
    dna = VinDNA(vin="WBA4W9C5ZLYYYYYYY", rated_rpm=5500)
    payload = dna.to_json_payload()
    assert payload["rated_rpm"] == 5500
    assert VinDNA.from_json(payload).rated_rpm == 5500


def test_decode_known_engine_code_yields_rated_rpm(decoder):
    """B58B30 fixture reads P14_rated_rpm median from the vref baseline."""
    dna = decoder.decode_vin_payload("WBA4W9C5ZLYYYYYYY")
    assert dna.rated_rpm == 5500


def test_decode_unknown_engine_code_leaves_rated_rpm_none(decoder):
    """No resolved engine code means no rated_rpm overlay."""
    dna = decoder.decode_vin_payload("SALLN12P0YAXXXXXX")
    assert dna.rated_rpm is None


def test_enum_values_match_contract():
    """All enums must use exact contract §8 strings."""
    assert FuelDeliveryType.GDI == "GDI"
    assert FuelDeliveryType.PORT_INJECTION == "PORT_INJECTION"
    assert FuelDeliveryType.CARBURETOR == "CARBURETOR"
    assert UpstreamO2Type.NARROWBAND == "NARROWBAND"
    assert UpstreamO2Type.WIDEBAND_AFR == "WIDEBAND_AFR"
    assert UpstreamO2Type.WIDEBAND_LAMBDA == "WIDEBAND_LAMBDA"
    assert UpstreamO2Type.NONE == "NONE"
    assert InductionType.NATURALLY_ASPIRATED == "NATURALLY_ASPIRATED"
    assert InductionType.TURBOCHARGED == "TURBOCHARGED"
    assert InductionType.SUPERCHARGED == "SUPERCHARGED"
    assert VinConfidence.HIGH == "HIGH"
    assert VinConfidence.PARTIAL == "PARTIAL"
    assert VinConfidence.NONE == "NONE"
    assert DownstreamTrimRole.NONE == "NONE"
    assert DownstreamTrimRole.CATALYST_MONITOR_ONLY == "CATALYST_MONITOR_ONLY"
    assert DownstreamTrimRole.SECONDARY_FUEL_TRIM == "SECONDARY_FUEL_TRIM"


def test_no_pfi_in_codebase():
    """'PFI' must not appear — only PORT_INJECTION is valid per contract §8."""
    import vinlab.models as m
    source = inspect.getsource(m)
    assert "PFI" not in source


# -- Enum field isinstance assertions (T-FX-5) --------------------------------


def test_enum_fields_are_str_enum_instances():
    """Every enum-shaped field must carry its StrEnum instance, not a bare str."""
    dna = VinDNA(
        vin="W" * 17,
        induction_type=InductionType.TURBOCHARGED,
        fuel_delivery_type=FuelDeliveryType.GDI,
        air_metering_architecture=AirMeteringArchitecture(
            primary_load_calculation=PrimaryLoadCalculation.HYBRID_MAF_MAP,
        ),
        emissions=Emissions(
            upstream_o2_type=UpstreamO2Type.WIDEBAND_AFR,
        ),
        euro_emission_category=EuroEmissionCategory.EURO_6,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        confidence=VinConfidence.HIGH,
    )

    assert isinstance(dna.induction_type, InductionType)
    assert isinstance(dna.fuel_delivery_type, FuelDeliveryType)
    assert isinstance(dna.euro_emission_category, EuroEmissionCategory)
    assert isinstance(dna.confidence, VinConfidence)
    assert isinstance(dna.air_metering_strategy, AirMeteringStrategy)

    assert isinstance(
        dna.air_metering_architecture.primary_load_calculation,
        PrimaryLoadCalculation,
    )
    assert isinstance(dna.emissions.upstream_o2_type, UpstreamO2Type)
    assert isinstance(dna.emissions.downstream_trim_role, DownstreamTrimRole)


def test_enum_fields_are_str_enum_instances_with_defaults():
    """Default-constructed VinDNA fields must still be StrEnum instances."""
    dna = VinDNA(vin="X" * 17)

    assert isinstance(dna.induction_type, InductionType)
    assert isinstance(dna.fuel_delivery_type, FuelDeliveryType)
    assert isinstance(dna.euro_emission_category, EuroEmissionCategory)
    assert isinstance(dna.confidence, VinConfidence)
    assert isinstance(dna.air_metering_strategy, AirMeteringStrategy)

    assert isinstance(
        dna.air_metering_architecture.primary_load_calculation,
        PrimaryLoadCalculation,
    )
    assert isinstance(dna.emissions.upstream_o2_type, UpstreamO2Type)
    assert isinstance(dna.emissions.downstream_trim_role, DownstreamTrimRole)



# -- DownstreamTrimRole (T-FX-10) ---------------------------------------------


def test_downstream_trim_role_default_is_none():
    """Emissions.downstream_trim_role defaults to NONE."""
    em = Emissions()
    assert em.downstream_trim_role == DownstreamTrimRole.NONE


def test_downstream_trim_role_accepts_each_value():
    """Emissions can be constructed with each DownstreamTrimRole value."""
    for role in DownstreamTrimRole:
        em = Emissions(downstream_trim_role=role)
        assert em.downstream_trim_role is role


# -- resolved_horizon (T-FX-DNA-2) --------------------------------------------


def test_resolved_horizon_default_is_modern():
    """VinDNA.resolved_horizon defaults to HORIZON_MODERN."""
    dna = VinDNA(vin="X" * 17)
    assert dna.resolved_horizon == Horizon.MODERN


def test_resolved_horizon_to_json_emits_string():
    """to_json() emits resolved_horizon as its string value."""
    dna = VinDNA(vin="X" * 17, resolved_horizon=Horizon.LEGACY)
    payload = dna.to_json_payload()
    assert payload["resolved_horizon"] == "HORIZON_LEGACY"


def test_derive_horizon_from_euro_matches_contract():
    """_derive_horizon_from_euro maps all 7 euro categories per contract §6.4."""
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_1) == Horizon.LEGACY
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_2) == Horizon.LEGACY
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_3) == Horizon.ADAPTIVE
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_4) == Horizon.ADAPTIVE
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_5) == Horizon.MODERN
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_6) == Horizon.MODERN
    assert _derive_horizon_from_euro(EuroEmissionCategory.EURO_7) == Horizon.MODERN
