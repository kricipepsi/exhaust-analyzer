"""Tests for SymptomDNA.from_json deserialization."""

from __future__ import annotations

from typing import Any

import pytest

from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
    SymptomValidationError,
)


def _make_full_payload() -> dict[str, Any]:
    dna = SymptomDNA(
        tier_1_primary_symptom="visible_exhaust_smoke",
        tier_2_subfield_filter="black_smoke",
        environmental_conditions=EnvironmentalConditions(
            occurs_during=OccursDuring.ALWAYS,
            engine_state=EngineState.RUNNING,
            load_state=LoadState.COASTING_DECELERATION,
        ),
        free_text_notes="observed at cold start",
    )
    return dna.to_json_payload()


class TestSymptomDNAFromJsonRoundTrip:
    def test_round_trip_full(self) -> None:
        """Assert that a complete valid JSON payload successfully round-trips to SymptomDNA."""
        payload = _make_full_payload()
        reconstituted = SymptomDNA.from_json(payload)
        assert reconstituted.tier_1_primary_symptom == payload["tier_1_primary_symptom"]
        assert reconstituted.tier_2_subfield_filter == payload["tier_2_subfield_filter"]
        assert reconstituted.free_text_notes == "observed at cold start"
        assert reconstituted.environmental_conditions.occurs_during == OccursDuring.ALWAYS
        assert reconstituted.environmental_conditions.engine_state == EngineState.RUNNING
        assert (
            reconstituted.environmental_conditions.load_state
            == LoadState.COASTING_DECELERATION
        )

    def test_round_trip_minimal(self) -> None:
        """SymptomDNA with no free_text_notes should round-trip."""
        dna = SymptomDNA(
            tier_1_primary_symptom="rough_idle_shudder",
            tier_2_subfield_filter="surging_hunting_idle",
            environmental_conditions=EnvironmentalConditions(
                occurs_during=OccursDuring.COLD_ONLY,
                engine_state=EngineState.RUNNING,
                load_state=LoadState.STEADY_CRUISE,
            ),
        )
        payload = dna.to_json_payload()
        reconstituted = SymptomDNA.from_json(payload)
        assert reconstituted.tier_1_primary_symptom == "rough_idle_shudder"
        assert reconstituted.tier_2_subfield_filter == "surging_hunting_idle"
        assert reconstituted.free_text_notes is None
        assert reconstituted.environmental_conditions.occurs_during == OccursDuring.COLD_ONLY
        assert reconstituted.environmental_conditions.load_state == LoadState.STEADY_CRUISE

    def test_optional_free_text_notes_when_absent(self) -> None:
        """Assert that free_text_notes is set to None if absent from the payload."""
        payload = _make_full_payload()
        del payload["free_text_notes"]
        reconstituted = SymptomDNA.from_json(payload)
        assert reconstituted.free_text_notes is None


class TestSymptomDNAFromJsonMissingRequired:
    def test_missing_tier_1_raises_keyerror(self) -> None:
        """Assert that missing tier_1_primary_symptom key raises SymptomValidationError."""
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json({})

    def test_missing_tier_2_raises_validation_error(self) -> None:
        """Assert that missing tier_2_subfield_filter key raises SymptomValidationError."""
        payload = _make_full_payload()
        del payload["tier_2_subfield_filter"]
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_missing_environmental_conditions_raises_validation_error(self) -> None:
        """Assert that missing environmental_conditions section raises SymptomValidationError."""
        payload = _make_full_payload()
        del payload["environmental_conditions"]
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_missing_occurs_during_raises_validation_error(self) -> None:
        """Assert that missing occurs_during key inside environment raises SymptomValidationError."""
        payload = _make_full_payload()
        del payload["environmental_conditions"]["occurs_during"]
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_missing_engine_state_raises_validation_error(self) -> None:
        """Assert that missing engine_state key inside environment raises SymptomValidationError."""
        payload = _make_full_payload()
        del payload["environmental_conditions"]["engine_state"]
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_missing_load_state_defaults_to_idle(self) -> None:
        """Pre-load-state payloads default to idle for deterministic migration."""
        # WHY: Pre-load-state payloads default to idle for deterministic migration.
        payload = _make_full_payload()
        del payload["environmental_conditions"]["load_state"]
        reconstituted = SymptomDNA.from_json(payload)
        assert reconstituted.environmental_conditions.load_state == LoadState.IDLE


class TestSymptomDNAFromJsonInvalidEnum:
    """from_json must reject payloads with invalid enum strings."""

    def test_invalid_occurs_during_raises_validation_error(self) -> None:
        """Assert that an invalid occurs_during enum string is rejected by from_json."""
        payload = _make_full_payload()
        payload["environmental_conditions"]["occurs_during"] = "SOMETIMES"
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_invalid_engine_state_raises_validation_error(self) -> None:
        """Assert that an invalid engine_state enum string is rejected by from_json."""
        payload = _make_full_payload()
        payload["environmental_conditions"]["engine_state"] = "STALLED"
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)

    def test_invalid_load_state_raises_validation_error(self) -> None:
        """Assert that an invalid load_state enum string is rejected by from_json."""
        payload = _make_full_payload()
        payload["environmental_conditions"]["load_state"] = "LAUNCH"
        with pytest.raises(SymptomValidationError):
            SymptomDNA.from_json(payload)


class TestSymptomDNAFromJsonNoPairValidation:
    """from_json() does NOT validate (tier_1, tier_2) catalog membership.
    This is intentional — see SymptomDNA.from_json() docstring.
    """

    def test_unknown_pair_accepted(self) -> None:
        """from_json() accepts an unknown (tier_1, tier_2) pair without error.
        Callers responsible for catalog validation must use resolve() instead.
        """
        dna = SymptomDNA.from_json({
            "tier_1_primary_symptom": "visible_exhaust_smoke",
            "tier_2_subfield_filter": "this_pair_is_not_in_the_catalog",
            "environmental_conditions": {
                "occurs_during": "always",
                "engine_state": "running",
                "load_state": "idle",
            },
        })
        assert dna.tier_2_subfield_filter == "this_pair_is_not_in_the_catalog"
