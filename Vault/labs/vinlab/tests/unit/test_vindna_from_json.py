"""Tests for VinDNA.from_json deserialization."""

from __future__ import annotations

import pytest
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
)


def _make_full_payload() -> dict:
    dna = VinDNA(
        vin="1FA6P8CF0HXXXXXXX",
        make="Ford",
        model_year=2017,
        engine_displacement_liters=2.3,
        cylinder_count=4,
        number_of_banks=1,
        induction_type=InductionType.TURBOCHARGED,
        fuel_delivery_type=FuelDeliveryType.GDI,
        air_metering_architecture=AirMeteringArchitecture(
            has_maf_sensor=True,
            has_map_sensor=True,
            primary_load_calculation=PrimaryLoadCalculation.HYBRID_MAF_MAP,
        ),
        emissions=Emissions(
            upstream_o2_type=UpstreamO2Type.WIDEBAND_AFR,
            downstream_o2_present=True,
            downstream_trim_role=DownstreamTrimRole.CATALYST_MONITOR_ONLY,
            egr_equipped=False,
        ),
        euro_emission_category=EuroEmissionCategory.EURO_6,
        stress_idle_rpm_target=4500,
        air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        confidence=VinConfidence.HIGH,
        target_lambda_v112=1.0,
        target_rpm_u2=2500,
    )
    return dna.to_json_payload()


class TestVinDNAFromJsonRoundTrip:
    def test_round_trip_full(self):
        payload = _make_full_payload()
        reconstituted = VinDNA.from_json(payload)
        assert reconstituted.vin == payload["vin"]
        assert reconstituted.make == payload["make"]
        assert not hasattr(reconstituted, "model")
        assert "model" not in reconstituted.to_json_payload()
        assert reconstituted.model_year == payload["model_year"]
        assert (
            reconstituted.engine_displacement_liters
            == payload["engine_displacement_liters"]
        )
        assert reconstituted.cylinder_count == payload["cylinder_count"]
        assert reconstituted.number_of_banks == payload["number_of_banks"]
        assert reconstituted.induction_type == payload["induction_type"]
        assert reconstituted.fuel_delivery_type == payload["fuel_delivery_type"]
        assert reconstituted.euro_emission_category == payload["euro_emission_category"]
        assert reconstituted.resolved_horizon == payload["resolved_horizon"]
        assert reconstituted.stress_idle_rpm_target == payload["stress_idle_rpm_target"]
        assert reconstituted.air_metering_strategy == payload["air_metering_strategy"]
        assert reconstituted.confidence == payload["confidence"]
        assert reconstituted.target_lambda_v112 == 1.0
        assert reconstituted.target_rpm_u2 == 2500
        assert reconstituted.air_metering_architecture.has_maf_sensor is True
        assert reconstituted.air_metering_architecture.has_map_sensor is True
        assert (
            reconstituted.air_metering_architecture.primary_load_calculation
            == "HYBRID_MAF_MAP"
        )
        assert reconstituted.emissions.upstream_o2_type == "WIDEBAND_AFR"
        assert reconstituted.emissions.downstream_o2_present is True
        assert reconstituted.emissions.downstream_trim_role == "CATALYST_MONITOR_ONLY"

    def test_round_trip_minimal(self):
        """Minimal VinDNA with only vin should round-trip through from_json."""
        dna = VinDNA(vin="W" * 17)
        payload = dna.to_json_payload()
        reconstituted = VinDNA.from_json(payload)
        assert reconstituted.vin == "W" * 17
        assert reconstituted.make == ""
        assert not hasattr(reconstituted, "model")
        assert reconstituted.model_year is None
        assert reconstituted.confidence == "NONE"

    def test_optional_coc_fields_preserved_when_absent(self):
        """CoC fields not in payload should remain None."""
        payload = _make_full_payload()
        del payload["target_lambda_v112"]
        del payload["target_rpm_u2"]
        reconstituted = VinDNA.from_json(payload)
        assert reconstituted.target_lambda_v112 is None
        assert reconstituted.target_rpm_u2 is None

    def test_optional_coc_fields_preserved_when_present(self):
        payload = _make_full_payload()
        reconstituted = VinDNA.from_json(payload)
        assert reconstituted.target_lambda_v112 == 1.0
        assert reconstituted.target_rpm_u2 == 2500


class TestVinDNAFromJsonMissingRequired:
    def test_missing_vin_raises_keyerror(self):
        with pytest.raises(KeyError):
            VinDNA.from_json({})

    def test_missing_make_raises_keyerror(self):
        payload = _make_full_payload()
        del payload["make"]
        with pytest.raises(KeyError):
            VinDNA.from_json(payload)

    def test_missing_model_year_raises_keyerror(self):
        payload = _make_full_payload()
        del payload["model_year"]
        with pytest.raises(KeyError):
            VinDNA.from_json(payload)

    def test_missing_air_metering_architecture_raises_keyerror(self):
        payload = _make_full_payload()
        del payload["air_metering_architecture"]
        with pytest.raises(KeyError):
            VinDNA.from_json(payload)

    def test_missing_emissions_raises_keyerror(self):
        payload = _make_full_payload()
        del payload["emissions"]
        with pytest.raises(KeyError):
            VinDNA.from_json(payload)

    def test_missing_confidence_raises_keyerror(self):
        payload = _make_full_payload()
        del payload["confidence"]
        with pytest.raises(KeyError):
            VinDNA.from_json(payload)

    def test_missing_resolved_horizon_derives_from_euro(self):
        """Legacy payloads without resolved_horizon derive it from euro_emission_category."""
        payload = _make_full_payload()
        del payload["resolved_horizon"]
        dna = VinDNA.from_json(payload)
        # EURO_6 → HORIZON_MODERN
        assert dna.resolved_horizon == Horizon.MODERN

    def test_missing_resolved_horizon_euro_1_derives_legacy(self):
        """EURO_1 without resolved_horizon derives HORIZON_LEGACY."""
        payload = _make_full_payload()
        payload["euro_emission_category"] = "EURO_1"
        del payload["resolved_horizon"]
        dna = VinDNA.from_json(payload)
        assert dna.resolved_horizon == Horizon.LEGACY

    def test_nested_defaults_applied_when_sub_keys_missing(self):
        """Nested fields should use defaults when keys are absent."""
        payload = _make_full_payload()
        payload["air_metering_architecture"] = {}
        payload["emissions"] = {}
        reconstituted = VinDNA.from_json(payload)
        assert reconstituted.air_metering_architecture.has_maf_sensor is False
        assert (
            reconstituted.air_metering_architecture.primary_load_calculation
            == "MAP_ONLY"
        )
        assert reconstituted.emissions.upstream_o2_type == "NARROWBAND"
        assert reconstituted.emissions.downstream_o2_present is False
        assert reconstituted.emissions.downstream_trim_role == "NONE"


class TestVinDNAFromJsonInvalidEnum:
    """from_json must reject payloads with invalid enum strings (T-FX-5)."""

    def test_invalid_induction_type_raises_valueerror(self):
        payload = _make_full_payload()
        payload["induction_type"] = "TUNA_SALAD"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_fuel_delivery_type_raises_valueerror(self):
        payload = _make_full_payload()
        payload["fuel_delivery_type"] = "JET_FUEL"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_euro_emission_category_raises_valueerror(self):
        payload = _make_full_payload()
        payload["euro_emission_category"] = "EURO_99"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_air_metering_strategy_raises_valueerror(self):
        payload = _make_full_payload()
        payload["air_metering_strategy"] = "MAGIC_METERING"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_confidence_raises_valueerror(self):
        payload = _make_full_payload()
        payload["confidence"] = "MEDIUM"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_primary_load_calculation_raises_valueerror(self):
        payload = _make_full_payload()
        payload["air_metering_architecture"]["primary_load_calculation"] = "NEITHER"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_upstream_o2_type_raises_valueerror(self):
        payload = _make_full_payload()
        payload["emissions"]["upstream_o2_type"] = "WIDEBAND_O3"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_downstream_trim_role_raises_valueerror(self):
        payload = _make_full_payload()
        payload["emissions"]["downstream_trim_role"] = "TERTIARY_TRIM"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)

    def test_invalid_resolved_horizon_raises_valueerror(self):
        payload = _make_full_payload()
        payload["resolved_horizon"] = "HORIZON_FUTURE"
        with pytest.raises(ValueError):
            VinDNA.from_json(payload)
