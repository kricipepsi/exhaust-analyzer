"""Round-trip and contract tests for VehicleDNA."""

from __future__ import annotations

import pytest
from symptomlab.models import LoadState

from dnalab.models import SCHEMA_VERSION, VehicleDNA
from tests.conftest import make_symptom_dna, make_vin_dna


class TestVehicleDNAConstruction:
    def test_new_constructs_successfully(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        assert dna.session_id.startswith("DNA_TX_")
        assert dna.timestamp.endswith("Z")
        assert dna.schema_version == SCHEMA_VERSION
        assert dna.vin_dna.vin == "1FA6P8CF0HXXXXXXX"
        assert dna.symptom_dna.tier_1_primary_symptom == "visible_exhaust_smoke"

    def test_explicit_session_id_and_timestamp(self):
        from datetime import datetime, timezone

        ts = datetime(2026, 5, 17, 9, 10, 0, tzinfo=timezone.utc)
        dna = VehicleDNA.new(
            make_vin_dna(),
            make_symptom_dna(free_text_notes=None),
            session_id="TEST_001",
            timestamp=ts,
        )
        assert dna.session_id == "TEST_001"
        assert dna.timestamp == "2026-05-17T09:10:00Z"

    def test_from_json_payload_rejects_wrong_schema_version(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        payload = dna.to_json_payload()
        payload["schema_version"] = "0.9"
        with pytest.raises(ValueError, match="schema_version mismatch"):
            VehicleDNA.from_json_payload(payload)


class TestVehicleDNASerialization:
    def test_to_json_payload_keys_exactly_five(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        payload = dna.to_json_payload()
        assert set(payload.keys()) == {
            "session_id", "timestamp", "schema_version", "vin_dna", "symptom_dna"
        }

    def test_schema_version_value(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        assert dna.to_json_payload()["schema_version"] == "1.2"

    def test_to_json_returns_string(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        result = dna.to_json()
        assert isinstance(result, str)
        assert '"session_id"' in result
        assert '"vin_dna"' in result
        assert '"symptom_dna"' in result

    def test_no_part_heading_strings_in_payload(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        payload = dna.to_json_payload()
        json_str = dna.to_json()
        for key in payload:
            assert "PART A" not in str(key)
            assert "PART B" not in str(key)
        assert "PART A" not in json_str
        assert "PART B" not in json_str

    def test_round_trip_json_payload(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        payload = dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        assert reconstituted.session_id == dna.session_id
        assert reconstituted.timestamp == dna.timestamp
        assert reconstituted.schema_version == dna.schema_version
        assert reconstituted.vin_dna.vin == dna.vin_dna.vin
        assert reconstituted.vin_dna.cylinder_count == dna.vin_dna.cylinder_count
        assert reconstituted.vin_dna.induction_type == dna.vin_dna.induction_type
        assert (
            reconstituted.symptom_dna.tier_1_primary_symptom
            == dna.symptom_dna.tier_1_primary_symptom
        )
        assert (
            reconstituted.symptom_dna.tier_2_subfield_filter
            == dna.symptom_dna.tier_2_subfield_filter
        )
        assert (
            reconstituted.symptom_dna.environmental_conditions.load_state
            == LoadState.TRANSIENT_ACCELERATION
        )

    def test_vin_dna_nested_shape(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        vin_payload = dna.to_json_payload()["vin_dna"]
        assert vin_payload["vin"] == "1FA6P8CF0HXXXXXXX"
        assert vin_payload["make"] == "Ford"
        assert vin_payload["air_metering_architecture"]["has_maf_sensor"] is True
        assert vin_payload["emissions"]["upstream_o2_type"] == "WIDEBAND_AFR"
        assert vin_payload["euro_emission_category"] == "EURO_6"

    def test_symptom_dna_nested_shape(self):
        dna = VehicleDNA.new(make_vin_dna(), make_symptom_dna(free_text_notes=None))
        sym_payload = dna.to_json_payload()["symptom_dna"]
        assert sym_payload["tier_1_primary_symptom"] == "visible_exhaust_smoke"
        assert sym_payload["tier_2_subfield_filter"] == "black_smoke"
        assert sym_payload["environmental_conditions"]["occurs_during"] == "always"
        assert (
            sym_payload["environmental_conditions"]["load_state"]
            == "transient_acceleration"
        )
