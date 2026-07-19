"""Drift guard: allowed_combinations.yaml must match VehicleDNA.md §"Complete
Universal Triage & Diagnostic Mapping Diagram" (2026-06-11).

Update this table whenever VehicleDNA.md's triage diagram changes.
Source: VehicleDNA.md lines 9-47 (diagram), lines 56/109 (JSON examples).
"""

from pathlib import Path

import yaml

_DATA_DIR = Path(__file__).parents[2] / "symptomlab" / "data"

# Authoritative (tier_1, tier_2) pairs per VehicleDNA.md §"Complete Universal
# Triage & Diagnostic Mapping Diagram". Wire-format values derived from the
# diagram labels (snake_case) and confirmed against the JSON examples in the
# same document.
_REFERENCE: set[tuple[str, str]] = {
    ("vehicle_starting_issues",   "no_crank_silent"),
    ("vehicle_starting_issues",   "fast_crank_whining"),
    ("vehicle_starting_issues",   "prolonged_crank_hard_start"),
    ("rough_idle_shudder",        "constant_vibration_shudder"),
    ("rough_idle_shudder",        "surging_hunting_idle"),
    ("rough_idle_shudder",        "stalls_on_cold_start"),
    ("lack_of_power_hesitation",  "flat_sluggish_always"),
    ("lack_of_power_hesitation",  "hesitation_throttle_tip_in"),
    ("lack_of_power_hesitation",  "sudden_jerk_stumble"),
    ("poor_economy_fuel_odor_sound", "just_poor_mpg"),
    ("poor_economy_fuel_odor_sound", "strong_fuel_smell"),
    ("poor_economy_fuel_odor_sound", "knock_pinging_under_load"),
    ("engine_dies_or_stalls",     "when_coasting_to_stop"),
    ("engine_dies_or_stalls",     "intermittent_random_cutout"),
    ("engine_dies_or_stalls",     "backfire_loud_pop"),
    ("visible_exhaust_smoke",     "black_smoke"),
    ("visible_exhaust_smoke",     "blue_oily_smell"),
    ("visible_exhaust_smoke",     "white_sweet_smell"),
    ("oil_consumption",           "blue_smoke_on_cold_start_clears"),
    ("oil_consumption",           "blue_smoke_under_acceleration"),
    ("oil_consumption",           "oil_loss_no_visible_smoke"),
}


def _load_yaml_pairs() -> set[tuple[str, str]]:
    with open(_DATA_DIR / "allowed_combinations.yaml", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    return {
        (tier_1, tier_2)
        for tier_1, tier_2_list in doc["combinations"].items()
        for tier_2 in tier_2_list
    }


def test_yaml_matches_vehicledna_reference() -> None:
    """Every pair in the YAML must be in the VehicleDNA.md reference table."""
    yaml_pairs = _load_yaml_pairs()
    extra = yaml_pairs - _REFERENCE
    assert not extra, (
        f"YAML has pairs not in VehicleDNA.md reference — update the reference "
        f"table in this test or revert the YAML change: {sorted(extra)}"
    )


def test_vehicledna_reference_matches_yaml() -> None:
    """Every pair in the VehicleDNA.md reference table must be in the YAML."""
    yaml_pairs = _load_yaml_pairs()
    missing = _REFERENCE - yaml_pairs
    assert not missing, (
        f"VehicleDNA.md reference has pairs absent from YAML — update "
        f"allowed_combinations.yaml: {sorted(missing)}"
    )
