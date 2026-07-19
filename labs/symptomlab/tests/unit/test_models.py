"""Sanity tests for SymptomLab models."""

from collections.abc import Callable

import pytest

from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
)


def test_symptom_dna_to_json_keys(
    make_symptom_dna: Callable[..., SymptomDNA],
) -> None:
    """Assert that the serialized SymptomDNA JSON payload contains the exact 4 contract keys."""
    dna = make_symptom_dna()
    payload = dna.to_json_payload()
    assert payload.keys() == {
        "tier_1_primary_symptom",
        "tier_2_subfield_filter",
        "environmental_conditions",
        "free_text_notes",
    }
    assert payload["free_text_notes"] is None
    assert payload["environmental_conditions"]["occurs_during"] == "always"
    assert payload["environmental_conditions"]["engine_state"] == "running"
    assert payload["environmental_conditions"]["load_state"] == "idle"


@pytest.mark.parametrize("tier_2", ["blue_oily_smell", "white_sweet_smell"])
def test_symptom_dna_preserves_reworked_visible_exhaust_strings(
    make_symptom_dna: Callable[..., SymptomDNA],
    tier_2: str,
) -> None:
    """Assert that revised visible exhaust strings are preserved in the JSON payload."""
    dna = make_symptom_dna(
        tier_2_subfield_filter=tier_2,
    )

    assert dna.to_json_payload()["tier_2_subfield_filter"] == tier_2


def test_symptom_dna_is_frozen(
    make_symptom_dna: Callable[..., SymptomDNA],
) -> None:
    """Assert that SymptomDNA instances are frozen and write-protected."""
    dna = make_symptom_dna(
        tier_1_primary_symptom="rough_idle_shudder",
        tier_2_subfield_filter="surging_hunting_idle",
        environmental_conditions=EnvironmentalConditions(
            occurs_during=OccursDuring.COLD_ONLY,
            engine_state=EngineState.RUNNING,
            load_state=LoadState.STEADY_CRUISE,
        ),
    )
    with pytest.raises(Exception):
        dna.tier_1_primary_symptom = "other"  # type: ignore[misc]


def test_enum_values() -> None:
    """Assert that all contract enum values match the specific domain string representations."""
    assert OccursDuring.ALWAYS == "always"
    assert OccursDuring.COLD_ONLY == "cold_only"
    assert OccursDuring.HOT_ONLY == "hot_only"
    assert OccursDuring.INTERMITTENT == "intermittent"

    assert EngineState.RUNNING == "running"
    assert EngineState.CRANKING == "cranking"
    assert EngineState.WONT_START == "will_not_start"

    assert LoadState.IDLE == "idle"
    assert LoadState.STEADY_CRUISE == "steady_cruise"
    assert LoadState.TRANSIENT_ACCELERATION == "transient_acceleration"
    assert LoadState.COASTING_DECELERATION == "coasting_deceleration"
