"""Comprehensive tests for SymptomLab validator and models."""

from pathlib import Path

import pytest

from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
)
from symptomlab.validator import SymptomValidationError, SymptomValidator


REVISED_PAIRS = [
    ("vehicle_starting_issues", "no_crank_silent"),
    ("vehicle_starting_issues", "fast_crank_whining"),
    ("vehicle_starting_issues", "prolonged_crank_hard_start"),
    ("rough_idle_shudder", "constant_vibration_shudder"),
    ("rough_idle_shudder", "surging_hunting_idle"),
    ("rough_idle_shudder", "stalls_on_cold_start"),
    ("lack_of_power_hesitation", "flat_sluggish_always"),
    ("lack_of_power_hesitation", "hesitation_throttle_tip_in"),
    ("lack_of_power_hesitation", "sudden_jerk_stumble"),
    ("poor_economy_fuel_odor_sound", "just_poor_mpg"),
    ("poor_economy_fuel_odor_sound", "strong_fuel_smell"),
    ("poor_economy_fuel_odor_sound", "knock_pinging_under_load"),
    ("engine_dies_or_stalls", "when_coasting_to_stop"),
    ("engine_dies_or_stalls", "intermittent_random_cutout"),
    ("engine_dies_or_stalls", "backfire_loud_pop"),
    ("visible_exhaust_smoke", "black_smoke"),
    ("visible_exhaust_smoke", "blue_oily_smell"),
    ("visible_exhaust_smoke", "white_sweet_smell"),
    ("oil_consumption", "blue_smoke_on_cold_start_clears"),
    ("oil_consumption", "blue_smoke_under_acceleration"),
    ("oil_consumption", "oil_loss_no_visible_smoke"),
]

DROPPED_LEGACY_PAIRS = [
    ("vehicle_wont_start", "normal_crank_zero_rpm"),
    ("rough_idle_shudder", "cold_engine_only"),
    ("rough_idle_shudder", "hot_engine_only"),
    ("rough_idle_shudder", "constant_shudder"),
    ("lack_of_power_hesitation", "only_high_rpm_highway"),
    ("poor_economy_fuel_odor", "just_poor_mpg"),
    ("poor_economy_fuel_odor", "strong_fuel_smell"),
    ("poor_economy_fuel_odor", "right_after_fillup"),
    ("engine_dies_or_stalls", "intermittent_random"),
    ("engine_dies_or_stalls", "only_when_hot"),
    ("visible_exhaust_smoke", "blue_oily"),
]


class TestAll21Combinations:
    def test_bad_17_pair_catalog_rejected(self, bad_allowed_path: Path) -> None:
        """Assert that catalogs not defining exactly 21 combinations are rejected."""
        with pytest.raises(ValueError, match="exactly 21 pairs"):
            SymptomValidator(bad_allowed_path)

    def test_catalog_matches_revised_research_pairs(self, allowed_pairs: list[tuple[str, str]]) -> None:
        """Assert that the parsed catalog combinations match the revised 21 authoritative pairs."""
        assert allowed_pairs == REVISED_PAIRS

    def test_all_pairs_validated(
        self, validator: SymptomValidator, allowed_pairs: list[tuple[str, str]]
    ) -> None:
        """Assert that all 21 combinations in the catalog are successfully validated."""
        for tier_1, tier_2 in allowed_pairs:
            result = validator.validate(
                tier_1, tier_2,
                occurs_during="always", engine_state="running", load_state="idle",
            )
            assert isinstance(result, SymptomDNA)
            assert result.tier_1_primary_symptom == tier_1
            assert result.tier_2_subfield_filter == tier_2

    def test_known_good_rich_smoke(self, validator: SymptomValidator) -> None:
        """Assert that a known good rich smoke configuration is successfully validated."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state="idle",
        )
        assert result.to_json_payload()["tier_1_primary_symptom"] == "visible_exhaust_smoke"
        assert result.to_json_payload()["tier_2_subfield_filter"] == "black_smoke"


class TestRejection:
    def test_unknown_tier_1(self, validator: SymptomValidator) -> None:
        """Assert that an unrecognized tier_1 value raises SymptomValidationError with valid hints."""
        with pytest.raises(SymptomValidationError) as exc:
            validator.validate(
                "nonexistent", "_",
                occurs_during="always", engine_state="running", load_state="idle",
            )
        msg = str(exc.value)
        assert "Valid tier_1 values" in msg

    def test_unknown_tier_2_known_tier_1(self, validator: SymptomValidator) -> None:
        """Assert that an unrecognized tier_2 for a known tier_1 raises SymptomValidationError with hints."""
        with pytest.raises(SymptomValidationError) as exc:
            validator.validate(
                "visible_exhaust_smoke", "fuchsia",
                occurs_during="always", engine_state="running", load_state="idle",
            )
        msg = str(exc.value)
        assert "Valid tier_2" in msg
        assert "visible_exhaust_smoke" in msg

    def test_invalid_occurs_during(self, validator: SymptomValidator) -> None:
        """Assert that invalid occurs_during values are rejected."""
        with pytest.raises(SymptomValidationError):
            validator.validate(
                "visible_exhaust_smoke", "black_smoke",
                occurs_during="MONDAY", engine_state="running", load_state="idle",
            )

    def test_invalid_engine_state(self, validator: SymptomValidator) -> None:
        """Assert that invalid engine_state values are rejected."""
        with pytest.raises(SymptomValidationError):
            validator.validate(
                "visible_exhaust_smoke", "black_smoke",
                occurs_during="always", engine_state="floating", load_state="idle",
            )

    def test_invalid_load_state(self, validator: SymptomValidator) -> None:
        """Assert that invalid load_state values are rejected."""
        with pytest.raises(SymptomValidationError):
            validator.validate(
                "visible_exhaust_smoke", "black_smoke",
                occurs_during="always", engine_state="running", load_state="launch",
            )

    @pytest.mark.parametrize(("tier_1", "tier_2"), DROPPED_LEGACY_PAIRS)
    def test_dropped_legacy_pairs_rejected(self, validator: SymptomValidator, tier_1: str, tier_2: str) -> None:
        """Assert that legacy combinations no longer present in the revised catalog are rejected."""
        with pytest.raises(SymptomValidationError):
            validator.validate(
                tier_1, tier_2,
                occurs_during="always", engine_state="running", load_state="idle",
            )


class TestAllEnumValues:
    @pytest.mark.parametrize("value", ["always", "cold_only", "hot_only", "intermittent"])
    def test_occurs_during_accepted(self, validator: SymptomValidator, value: str) -> None:
        """Assert that occurs_during enum values are correctly accepted and mapped."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during=value, engine_state="running", load_state="idle",
        )
        assert result.environmental_conditions.occurs_during == value

    @pytest.mark.parametrize("value", ["running", "cranking", "will_not_start"])
    def test_engine_state_accepted(self, validator: SymptomValidator, value: str) -> None:
        """Assert that engine_state enum values are correctly accepted and mapped."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state=value, load_state="idle",
        )
        assert result.environmental_conditions.engine_state == value

    @pytest.mark.parametrize(
        "value",
        ["idle", "steady_cruise", "transient_acceleration", "coasting_deceleration"],
    )
    def test_load_state_accepted(self, validator: SymptomValidator, value: str) -> None:
        """Assert that load_state enum values are correctly accepted and mapped."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state=value,
        )
        assert result.environmental_conditions.load_state == value


class TestFreeTextNotes:
    def test_omitted(self, validator: SymptomValidator) -> None:
        """Assert that free_text_notes is None when omitted."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state="idle",
        )
        assert result.free_text_notes is None

    def test_explicit_none(self, validator: SymptomValidator) -> None:
        """Assert that free_text_notes is None when explicitly set to None."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state="idle",
            free_text_notes=None,
        )
        assert result.free_text_notes is None

    def test_some_text(self, validator: SymptomValidator) -> None:
        """Assert that free_text_notes preserves custom strings."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state="idle",
            free_text_notes="tech note here",
        )
        assert result.free_text_notes == "tech note here"


class TestJSONShape:
    def test_exact_four_keys(self, validator: SymptomValidator) -> None:
        """Assert that the serialized payload contains exactly the 4 required keys."""
        result = validator.validate(
            "visible_exhaust_smoke", "black_smoke",
            occurs_during="always", engine_state="running", load_state="idle",
        )
        keys = set(result.to_json_payload().keys())
        assert keys == {
            "tier_1_primary_symptom",
            "tier_2_subfield_filter",
            "environmental_conditions",
            "free_text_notes",
        }

    def test_no_extra_keys(self, validator: SymptomValidator) -> None:
        """Assert that the payload has exactly 4 keys with no extra additions."""
        result = validator.validate(
            "rough_idle_shudder", "surging_hunting_idle",
            occurs_during="cold_only", engine_state="running", load_state="idle",
        )
        payload = result.to_json_payload()
        assert len(payload) == 4


class TestImmutability:
    def test_symptom_dna_frozen(self) -> None:
        """Assert that SymptomDNA dataclass attributes cannot be reassigned."""
        dna = SymptomDNA(
            tier_1_primary_symptom="test",
            tier_2_subfield_filter="test",
            environmental_conditions=EnvironmentalConditions(
                occurs_during=OccursDuring.ALWAYS,
                engine_state=EngineState.RUNNING,
                load_state=LoadState.IDLE,
            ),
        )
        with pytest.raises(Exception):
            dna.tier_1_primary_symptom = "other"  # type: ignore[misc]

    def test_symptom_dna_hashable(self) -> None:
        """Assert that SymptomDNA instances are hashable."""
        dna = SymptomDNA(
            tier_1_primary_symptom="test",
            tier_2_subfield_filter="test",
            environmental_conditions=EnvironmentalConditions(
                occurs_during=OccursDuring.ALWAYS,
                engine_state=EngineState.RUNNING,
                load_state=LoadState.IDLE,
            ),
        )
        h = hash(dna)
        assert isinstance(h, int)

    def test_environmental_conditions_frozen(self) -> None:
        """Assert that EnvironmentalConditions dataclass attributes cannot be reassigned."""
        ec = EnvironmentalConditions(
            occurs_during=OccursDuring.ALWAYS,
            engine_state=EngineState.RUNNING,
            load_state=LoadState.IDLE,
        )
        with pytest.raises(Exception):
            ec.occurs_during = OccursDuring.COLD_ONLY  # type: ignore[misc]

    def test_occurs_during_str_equality(self) -> None:
        """Assert string equality behavior for OccursDuring enum."""
        assert OccursDuring("always") == OccursDuring.ALWAYS
        assert OccursDuring.ALWAYS == "always"
