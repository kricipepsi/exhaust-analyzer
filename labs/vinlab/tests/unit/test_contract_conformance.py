"""SEMANTIC_CONTRACT.md §9 conformance tests."""

from __future__ import annotations

import pytest
from vinlab.decoder import VINDecodeError

# -- §9.1 Schema test -------------------------------------------------------

REQUIRED_TOP_KEYS = {
    "vin", "make", "model_year",
    "engine_displacement_liters", "cylinder_count", "number_of_banks",
    "induction_type", "fuel_delivery_type",
    "air_metering_architecture", "emissions",
    "euro_emission_category", "resolved_horizon",
    "stress_idle_rpm_target", "confidence",
    "air_metering_strategy",
}

REQUIRED_ARCH_KEYS = {"has_maf_sensor", "has_map_sensor", "primary_load_calculation"}

REQUIRED_EMISSIONS_KEYS = {
    "upstream_o2_type", "downstream_o2_present", "downstream_trim_role",
    "has_catalyst", "egr_equipped",
}


def test_schema_top_keys(decoder):
    """§9.1: to_json() includes all required top-level keys."""
    dna = decoder.decode_vin_payload("VF1CB05CF25935016")
    payload = dna.to_json_payload()
    missing = REQUIRED_TOP_KEYS - set(payload.keys())
    assert not missing, f"Missing top-level keys: {missing}"
    assert "model" not in payload


def test_schema_air_metering_architecture_shape(decoder):
    """§9.1: air_metering_architecture is a dict with exactly 3 keys."""
    dna = decoder.decode_vin_payload("VF1CB05CF25935016")
    arch = dna.to_json_payload()["air_metering_architecture"]
    assert set(arch.keys()) == REQUIRED_ARCH_KEYS


def test_schema_emissions_shape(decoder):
    """§9.1: emissions is a dict with exactly 7 keys."""
    dna = decoder.decode_vin_payload("VF1CB05CF25935016")
    emissions = dna.to_json_payload()["emissions"]
    assert set(emissions.keys()) == REQUIRED_EMISSIONS_KEYS


# -- §9.2 Enum-value test ---------------------------------------------------

VALID_FUEL_DELIVERY = {"GDI", "PORT_INJECTION", "CARBURETOR"}
VALID_O2_TYPE = {
    "NARROWBAND",
    "WIDEBAND_AFR",
    "WIDEBAND_LAMBDA",
    "WIDEBAND_NB_SIM",
    "NONE",
}
VALID_INDUCTION = {"NATURALLY_ASPIRATED", "TURBOCHARGED", "SUPERCHARGED"}
VALID_CONFIDENCE = {"HIGH", "PARTIAL", "NONE"}
VALID_EURO = {"EURO_1", "EURO_2", "EURO_3", "EURO_4", "EURO_5", "EURO_6", "EURO_7"}
VALID_STRATEGY = {"DUAL_MAF_MAP_CROSSCHECK", "MAP_ONLY_SPEED_DENSITY", "MAF_ONLY"}
VALID_LOAD_CALC = {"HYBRID_MAF_MAP", "MAP_ONLY", "MAF_ONLY"}


def _safe_decode(decoder, vin):
    """Decode a VIN, returning None for out-of-scope vehicles."""
    try:
        return decoder.decode_vin_payload(vin)
    except VINDecodeError:
        return None


def test_enum_fuel_delivery_type(decoder, sample_vins):
    """§9.2: fuel_delivery_type is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        assert dna.fuel_delivery_type in VALID_FUEL_DELIVERY, (
            f"{vin}: {dna.fuel_delivery_type}"
        )


def test_enum_upstream_o2_type(decoder, sample_vins):
    """§9.2: emissions.upstream_o2_type is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        assert dna.emissions.upstream_o2_type in VALID_O2_TYPE, (
            f"{vin}: {dna.emissions.upstream_o2_type}"
        )


def test_enum_induction_type(decoder, sample_vins):
    """§9.2: induction_type is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        assert dna.induction_type in VALID_INDUCTION, (
            f"{vin}: {dna.induction_type}"
        )


def test_enum_confidence(decoder):
    """§9.2: confidence is always a contract enum value."""
    dna = decoder.decode_vin_payload("VF1CB05CF25935016")
    assert dna.confidence in VALID_CONFIDENCE


def test_enum_euro_emission(decoder, sample_vins):
    """§9.2: euro_emission_category is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        assert dna.euro_emission_category in VALID_EURO, (
            f"{vin}: {dna.euro_emission_category}"
        )


def test_enum_air_metering_strategy(decoder, sample_vins):
    """§9.2: air_metering_strategy is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        assert dna.air_metering_strategy in VALID_STRATEGY, (
            f"{vin}: {dna.air_metering_strategy}"
        )


def test_enum_primary_load_calculation(decoder, sample_vins):
    """§9.2: primary_load_calculation is always a contract enum value."""
    vins = sample_vins[:5] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        plc = dna.air_metering_architecture.primary_load_calculation
        assert plc in VALID_LOAD_CALC, f"{vin}: {plc}"


# -- §9.3 Cross-field consistency -------------------------------------------

def test_air_metering_consistency(decoder, sample_vins):
    """§9.3: has_maf/has_map, strategy, and load_calculation are consistent."""
    vins = sample_vins[:10] if sample_vins else ["VF1CB05CF25935016"]
    for vin in vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        payload = dna.to_json_payload()
        arch = payload["air_metering_architecture"]
        strategy = payload["air_metering_strategy"]
        plc = arch["primary_load_calculation"]

        has_maf = arch["has_maf_sensor"]
        has_map = arch["has_map_sensor"]

        if has_maf and has_map:
            assert strategy == "DUAL_MAF_MAP_CROSSCHECK", (
                f"{vin}: expected DUAL_MAF_MAP_CROSSCHECK, got {strategy}"
            )
            assert plc == "HYBRID_MAF_MAP", (
                f"{vin}: expected HYBRID_MAF_MAP, got {plc}"
            )
        elif not has_maf and has_map:
            assert strategy == "MAP_ONLY_SPEED_DENSITY", (
                f"{vin}: expected MAP_ONLY_SPEED_DENSITY, got {strategy}"
            )
            assert plc == "MAP_ONLY", (
                f"{vin}: expected MAP_ONLY, got {plc}"
            )
        elif has_maf and not has_map:
            assert strategy == "MAF_ONLY", (
                f"{vin}: expected MAF_ONLY, got {strategy}"
            )
            assert plc == "MAF_ONLY", (
                f"{vin}: expected MAF_ONLY, got {plc}"
            )


def test_emissions_downstream_o2_post_1996(decoder):
    """§9.3: downstream_o2_present is True for model year >= 1996 (OBD-II mandate)."""
    # VF1CB05CF25935016 → model_year=2002
    dna = decoder.decode_vin_payload("VF1CB05CF25935016")
    assert dna.emissions.downstream_o2_present is True


def test_sample_vins_within_year_bounds(decoder, sample_vins):
    """Decodable sample VINs have model years within 1990-2020."""
    if not sample_vins:
        pytest.skip("No sample VINs available")
    decoded = 0
    for vin in sample_vins:
        dna = _safe_decode(decoder, vin)
        if dna is None:
            continue
        decoded += 1
        if dna.model_year is None:
            continue
        assert 1990 <= dna.model_year <= 2020, (
            f"{vin}: model_year={dna.model_year} out of range"
        )
    assert decoded > 0, "No sample VINs were decodable"
