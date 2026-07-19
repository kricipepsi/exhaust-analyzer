"""Explicit round-trip test for VehicleDNA JSON serialization.

Build a VehicleDNA, serialize to JSON payload, deserialize back, and assert
equality of every nested field across both Part A (VinDNA) and Part B (SymptomDNA).
"""

from __future__ import annotations

from symptomlab.models import EngineState, LoadState, OccursDuring

from dnalab.models import VehicleDNA
from tests.conftest import make_symptom_dna, make_vin_dna


class TestVehicleDNARoundTrip:
    def test_full_round_trip_envelope(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna())
        payload = dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        assert reconstituted.session_id == dna.session_id
        assert reconstituted.timestamp == dna.timestamp
        assert reconstituted.schema_version == dna.schema_version

    def test_full_round_trip_vin_dna(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna())
        payload = dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        v = reconstituted.vin_dna
        assert v.vin == "1FA6P8CF0HXXXXXXX"
        assert v.make == "Ford"
        assert v.model_year == 2017
        assert v.engine_displacement_liters == 2.3
        assert v.cylinder_count == 4
        assert v.number_of_banks == 1
        assert v.induction_type == "TURBOCHARGED"
        assert v.fuel_delivery_type == "GDI"
        assert v.euro_emission_category == "EURO_6"
        assert v.stress_idle_rpm_target == 4500
        assert v.air_metering_strategy == "DUAL_MAF_MAP_CROSSCHECK"
        assert v.confidence == "HIGH"
        assert v.rated_rpm == 6500
        assert v.target_lambda_v112 == 1.001
        assert v.target_rpm_u2 == 3000
        assert v.idle_rpm_low == 760
        assert v.co_low_idle == 0.12
        assert v.co_high_idle == 0.08
        assert v.co_type_approval == 1.0
        assert v.hc_type_approval == 90.0
        assert v.nox_type_approval == 60.0
        assert v.hc_nox_type_approval == 120.0
        assert v.co2_type_approval == 168.0
        assert v.noise_stationary_dba == 82.0
        assert v.noise_rpm == 3750
        assert v.noise_driving_dba == 74.0

    def test_full_round_trip_vin_dna_nested(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna())
        payload = dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        ama = reconstituted.vin_dna.air_metering_architecture
        assert ama.has_maf_sensor is True
        assert ama.has_map_sensor is True
        assert ama.primary_load_calculation == "HYBRID_MAF_MAP"
        em = reconstituted.vin_dna.emissions
        assert em.upstream_o2_type == "WIDEBAND_AFR"
        assert em.downstream_o2_present is True
        assert em.egr_equipped is False

    def test_full_round_trip_symptom_dna(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna())
        payload = dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        s = reconstituted.symptom_dna
        assert s.tier_1_primary_symptom == "visible_exhaust_smoke"
        assert s.tier_2_subfield_filter == "black_smoke"
        assert s.free_text_notes == "test note"
        assert s.environmental_conditions.occurs_during == OccursDuring.ALWAYS
        assert s.environmental_conditions.engine_state == EngineState.RUNNING
        assert s.environmental_conditions.load_state == LoadState.TRANSIENT_ACCELERATION

    def test_full_round_trip_json_string(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna())
        json_str = dna.to_json()
        import json
        payload = json.loads(json_str)
        reconstituted = VehicleDNA.from_json_payload(payload)
        assert reconstituted.session_id == dna.session_id
        assert reconstituted.vin_dna.vin == dna.vin_dna.vin
        assert (
            reconstituted.symptom_dna.tier_1_primary_symptom
            == dna.symptom_dna.tier_1_primary_symptom
        )
