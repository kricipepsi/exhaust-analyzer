"""Drift guard for physical_sensor_bounds.json against OBDLab_KG_Wiki.md §3.1.

Ensures every row in the JSON bounds matches the canonical table row-for-row.
"""

import json
from pathlib import Path

import pytest

OBDLAB_ROOT = Path(__file__).resolve().parents[2]
BOUNDS_PATH = OBDLAB_ROOT / "obdlab" / "config" / "physical_sensor_bounds.json"
WIKI_PATH = OBDLAB_ROOT / "wiki" / "OBDLab_KG_Wiki.md"  # v2: wiki/ co-located in lab

# Expected bounds from OBDLab_KG_Wiki.md §3.1
EXPECTED_BOUNDS = {
    "engine_rpm":               {"min": 0,    "max": 8000,   "unit": "RPM"},
    "coolant_temp_c":           {"min": -40,  "max": 140,    "unit": "°C"},
    "calculated_engine_load_pct": {"min": 0,  "max": 100,    "unit": "%"},
    "mass_airflow_gps":         {"min": 0,    "max": 655.35, "unit": "g/s"},
    "manifold_vacuum_kpa":      {"min": 0,    "max": 255,    "unit": "kPa"},
    # Widened from OBD-nominal [-100, 99.22] to OBD-rail [-127, 127] per T-W-6 —
    # railed fuel-trim values are a sensor_fault signal; rejecting them at the
    # PID gate causes signal loss (cases case_025, case_026).
    "shrtft1":                  {"min": -127, "max": 127,    "unit": "%"},
    "longft1":                  {"min": -127, "max": 127,    "unit": "%"},
    "shrtft2":                  {"min": -127, "max": 127,    "unit": "%"},
    "longft2":                  {"min": -127, "max": 127,    "unit": "%"},
    "intake_air_temp_c":        {"min": -40,  "max": 140,    "unit": "°C"},
    "throttle_pos_pct":         {"min": 0,    "max": 100,    "unit": "%"},
    "control_module_voltage_v": {"min": 0,    "max": 18,     "unit": "V"},
}


def _load_bounds():
    with open(BOUNDS_PATH, encoding="utf-8") as fh:
        return json.load(fh)


# --- Field count ---

def test_bounds_field_count():
    config = _load_bounds()
    assert len(config["bounds"]) == 12, (
        f"Expected 12 fields per §3.1, got {len(config['bounds'])}"
    )


# --- Row-by-row match ---

@pytest.mark.parametrize("field, expected", list(EXPECTED_BOUNDS.items()))
def test_bound_row_matches_wiki(field, expected):
    config = _load_bounds()
    actual = config["bounds"].get(field)
    assert actual is not None, f"{field} missing from physical_sensor_bounds.json"
    assert actual["min"] == expected["min"], (
        f"{field} min: expected {expected['min']}, got {actual['min']}"
    )
    assert actual["max"] == expected["max"], (
        f"{field} max: expected {expected['max']}, got {actual['max']}"
    )
    assert actual["unit"] == expected["unit"], (
        f"{field} unit: expected {expected['unit']}, got {actual['unit']}"
    )


# --- Provenance ---

def test_source_wiki_present():
    config = _load_bounds()
    assert config.get("source_wiki") == "OBDLab_KG_Wiki.md §3.1", (
        "source_wiki key missing or incorrect"
    )


def test_bank2_contract_present():
    config = _load_bounds()
    contract = config.get("bank_2_null_contract")
    assert contract is not None, "bank_2_null_contract section missing"
    assert "source_wiki" in contract, "bank_2_null_contract missing source_wiki"
    assert contract["source_wiki"] == "OBDLab_KG_Wiki.md §3.1"


# --- Wiki text drift: every field name appears in the wiki §3.1 ---

def test_all_field_names_in_wiki():
    wiki_text = WIKI_PATH.read_text(encoding="utf-8")
    for field in EXPECTED_BOUNDS:
        assert field in wiki_text, f"{field} not found in OBDLab_KG_Wiki.md"


# --- Extra: no fields beyond the 10 ---

def test_no_extra_fields():
    config = _load_bounds()
    actual = set(config["bounds"].keys())
    expected = set(EXPECTED_BOUNDS.keys())
    assert actual == expected, f"Extra fields: {actual - expected}"
