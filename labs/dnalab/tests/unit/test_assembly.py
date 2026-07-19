"""Integration and contract tests for build_vehicle_dna."""

from __future__ import annotations

import re

import pytest
from symptomlab.validator import SymptomValidationError
from vinlab.decoder import VINDecodeError

from dnalab.assembly import build_vehicle_dna
from dnalab.models import SCHEMA_VERSION, VehicleDNA
from tests.conftest import (
    fake_decode_returning,
    fake_resolve_returning,
    make_symptom_dna,
    make_vin_dna,
)

VIN_DNA_REQUIRED_KEYS = {
    "vin", "make", "model_year",
    "engine_displacement_liters", "cylinder_count", "number_of_banks",
    "induction_type", "fuel_delivery_type",
    "air_metering_architecture", "air_metering_strategy",
    "emissions", "euro_emission_category", "resolved_horizon",
    "stress_idle_rpm_target", "rated_rpm", "confidence",
    "target_lambda_v112", "target_rpm_u2", "idle_rpm_low",
    "co_low_idle", "co_high_idle", "co_type_approval",
    "hc_type_approval", "nox_type_approval", "hc_nox_type_approval",
    "co2_type_approval", "noise_stationary_dba", "noise_rpm",
    "noise_driving_dba",
}

SYMPTOM_DNA_EXACT_KEYS = {
    "tier_1_primary_symptom",
    "tier_2_subfield_filter",
    "environmental_conditions",
    "free_text_notes",
}


class TestBuildVehicleDNA:
    def test_happy_path_composes_vehicle_dna_from_fakes(
        self, monkeypatch, sample_vin, sample_triage
    ):
        vin_dna = make_vin_dna(vin=sample_vin, make="FakeMake")
        symptom_dna = make_symptom_dna(tier_2_subfield_filter="fake_smoke")
        monkeypatch.setattr(
            "dnalab.assembly._decode_vin", fake_decode_returning(vin_dna)
        )
        monkeypatch.setattr(
            "dnalab.assembly._resolve_symptom", fake_resolve_returning(symptom_dna)
        )

        dna = build_vehicle_dna(sample_vin, sample_triage)
        assert isinstance(dna, VehicleDNA)
        assert dna.vin_dna.vin == sample_vin
        assert dna.vin_dna.make == "FakeMake"
        assert dna.symptom_dna.tier_2_subfield_filter == "fake_smoke"

    def test_session_id_format(self, sample_dna):
        assert sample_dna.session_id.startswith("DNA_TX_")

    def test_timestamp_iso8601_utc(self, sample_dna):
        pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        assert re.match(pattern, sample_dna.timestamp) is not None

    def test_contract_top_level_keys(self, sample_dna):
        payload = sample_dna.to_json_payload()
        assert set(payload.keys()) == {
            "session_id", "timestamp", "schema_version", "vin_dna", "symptom_dna"
        }
        assert payload["schema_version"] == "1.2"
        assert (
            payload["symptom_dna"]["environmental_conditions"]["load_state"]
            == "transient_acceleration"
        )

    def test_vin_dna_keys_superset(self, sample_dna):
        payload = sample_dna.to_json_payload()
        vin_keys = set(payload["vin_dna"].keys())
        missing = VIN_DNA_REQUIRED_KEYS - vin_keys
        assert not missing, f"Missing VinDNA keys: {missing}"

    def test_symptom_dna_keys_exact(self, sample_dna):
        payload = sample_dna.to_json_payload()
        sym_keys = set(payload["symptom_dna"].keys())
        assert sym_keys == SYMPTOM_DNA_EXACT_KEYS

    def test_round_trip_json_payload(self, sample_dna):
        payload = sample_dna.to_json_payload()
        reconstituted = VehicleDNA.from_json_payload(payload)
        assert reconstituted.session_id == sample_dna.session_id
        assert reconstituted.timestamp == sample_dna.timestamp
        assert reconstituted.schema_version == sample_dna.schema_version
        assert reconstituted.vin_dna.vin == sample_dna.vin_dna.vin
        assert reconstituted.symptom_dna.tier_1_primary_symptom == \
            sample_dna.symptom_dna.tier_1_primary_symptom

    def test_invalid_vin_propagates(self, monkeypatch, invalid_vin, sample_triage):
        def fake_decode_raises(vin):
            raise VINDecodeError(vin)

        monkeypatch.setattr("dnalab.assembly._decode_vin", fake_decode_raises)
        monkeypatch.setattr(
            "dnalab.assembly._resolve_symptom",
            fake_resolve_returning(make_symptom_dna()),
        )

        with pytest.raises(VINDecodeError):
            build_vehicle_dna(invalid_vin, sample_triage)

    def test_missing_triage_key_raises_before_resolve(self, monkeypatch, sample_vin):
        resolve_called = False

        def fake_resolve_unexpected(**kwargs):
            nonlocal resolve_called
            resolve_called = True
            return make_symptom_dna()

        monkeypatch.setattr(
            "dnalab.assembly._decode_vin", fake_decode_returning(make_vin_dna())
        )
        monkeypatch.setattr("dnalab.assembly._resolve_symptom", fake_resolve_unexpected)

        bad = {"tier_1": "rough_idle"}  # tier_2, occurs_during, engine_state absent
        with pytest.raises(SymptomValidationError):
            build_vehicle_dna(sample_vin, bad)
        assert resolve_called is False

    def test_invalid_triage_propagates(self, monkeypatch, sample_vin):
        def fake_resolve_raises(**kwargs):
            raise SymptomValidationError("bad triage")

        monkeypatch.setattr(
            "dnalab.assembly._decode_vin", fake_decode_returning(make_vin_dna())
        )
        monkeypatch.setattr("dnalab.assembly._resolve_symptom", fake_resolve_raises)

        bad_triage = {
            "tier_1": "nonexistent_symptom",
            "tier_2": "nonsense",
            "occurs_during": "never",
            "engine_state": "flying",
            "load_state": "launch",
        }
        with pytest.raises(SymptomValidationError):
            build_vehicle_dna(sample_vin, bad_triage)


class TestSchemaVersion:
    def test_schema_version_constant(self):
        assert SCHEMA_VERSION == "1.2"
