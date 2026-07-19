"""Unit tests for the 6 populated ``comlab/config/kg/<family>.json`` files.

Covers the success criteria for T-P2-1:
- All 6 files exist, total 30 nodes, correct counts per family
- All expected fault_ids present
- Every node validates against _kg_schema.json
- No unknown enum values
- mechanical_failure_mode <= 280 chars for every node
- All differential_siblings resolve to known fault IDs
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

import jsonschema

# ---------------------------------------------------------------------------
# paths
# ---------------------------------------------------------------------------

KG_DIR = (
    Path(__file__).resolve().parents[2] / "comlab" / "config" / "kg"
)
SCHEMA_PATH = KG_DIR / "_kg_schema.json"

EXPECTED_FAMILIES = {
    "rich_mixture": 13,
    "lean_condition": 10,
    "misfire": 10,
    "sensor_fault": 8,
    "ecu_fault": 9,
    "catalyst_failure": 9,
    "exhaust_leak": 8,
    "ignition_fault": 7,
    "mechanical_wear": 13,
    "cam_timing": 8,
    "non_starter": 6,
    "no_fault": 1,
    "invalid_input": 6,
}

EXPECTED_IDS = {
    # rich_mixture — 11
    "ERR-RM-001", "ERR-RM-002", "ERR-RM-003", "ERR-RM-004",
    "ERR-RM-005", "ERR-RM-006", "ERR-RM-007",
    "ERR-RM-008", "ERR-RM-009", "ERR-RM-010", "ERR-RM-011",
    # lean_condition — 8
    "ERR-LC-001", "ERR-LC-002", "ERR-LC-003", "ERR-LC-004",
    "ERR-LC-005", "ERR-LC-006", "ERR-LC-008", "ERR-LC-009",
    # misfire — 7
    "ERR-MF-001", "ERR-MF-002", "ERR-MF-003", "ERR-MF-004",
    "ERR-MF-005", "ERR-MF-006", "ERR-MF-007",
    # sensor_fault — 6
    "ERR-SF-001", "ERR-SF-002", "ERR-SF-003",
    "ERR-SF-004", "ERR-SF-005", "ERR-SF-006",
    # ecu_fault — 6
    "ERR-EF-001", "ERR-EF-002", "ERR-EF-003", "ERR-EF-004",
    "ERR-EF-005", "ERR-ECU-001",
    # catalyst_failure — 7
    "ERR-CF-001", "ERR-CF-002", "ERR-CF-003", "ERR-CF-004",
    "ERR-CF-005", "ERR-CF-006", "ERR-CF-007",
    # exhaust_leak — 6
    "ERR-EL-001", "ERR-EL-002", "ERR-EL-003",
    "ERR-EL-004", "ERR-EL-005", "ERR-EL-006",
    # ignition_fault — 3
    "ERR-IF-001", "ERR-IF-002", "ERR-IF-003",
    # mechanical_wear — 6
    "ERR-MW-001", "ERR-MW-002", "ERR-MW-003", "ERR-MW-004",
    "ERR-MW-005", "ERR-MW-006",
    # cam_timing — 6
    "ERR-CT-001", "ERR-CT-002", "ERR-CT-003", "ERR-CT-004",
    "ERR-CT-005", "ERR-CT-006",
    # non_starter — 6
    "ERR-NS-001", "ERR-NS-002", "ERR-NS-003",
    "ERR-NS-004", "ERR-NS-005", "ERR-NS-006",
    # no_fault — 1
    "OPTIMAL_HEALTH",
    # invalid_input — 6
    "ERR-II-001", "ERR-II-002", "ERR-II-003", "ERR-II-004",
    "ERR-II-005", "ERR-II-006",
    # --- T-FX-REG-5 additions (28 nodes) ---
    # ignition_fault +4
    "ERR-IF-004", "ERR-IF-005", "ERR-IF-006", "ERR-IF-007",
    # exhaust_leak +2
    "ERR-EL-007", "ERR-EL-008",
    # mechanical_wear +2
    "ERR-MW-007", "ERR-MW-008",
    # oil-consumption expansion (T-OIL-3) +5
    "P_NEW_09", "P_NEW_10", "P_NEW_11", "P_NEW_12", "P_NEW_13",
    # ecu_fault +3
    "ERR-EF-006", "ERR-EF-007", "ERR-EF-008",
    # lean_condition +2
    "ERR-LC-010", "ERR-LC-011",
    # rich_mixture +2
    "ERR-RM-012", "ERR-RM-013",
    # sensor_fault +2
    "ERR-SF-007", "ERR-SF-008",
    # catalyst_failure +2
    "ERR-CF-008", "ERR-CF-009",
    # cam_timing +2
    "ERR-CT-007", "ERR-CT-008",
    # misfire +3
    "ERR-MF-008", "ERR-MF-009", "ERR-MF-010",
}

VALID_FAMILIES = frozenset(EXPECTED_FAMILIES)
VALID_SEVERITIES = frozenset({"INFORMATIONAL", "WATCH", "REPAIR", "URGENT"})

# lld: §3.4 — field constraints
MECH_FAILURE_MODE_MAX = 280  # lld: §3.4 KGNode.mechanical_failure_mode
REMEDIATION_STEPS_MIN = 1  # lld: §3.4 KGNode.ui_remediation_steps min_length
REMEDIATION_STEPS_MAX = 8  # lld: §3.4 KGNode.ui_remediation_steps max_length
DIFF_SIBLINGS_MAX = 5  # lld: §3.3 Q1 ruling


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_all() -> dict[str, dict[str, object]]:
    """Load all 6 family JSON files, returning {family: data}."""
    result: dict[str, dict[str, object]] = {}
    for family in EXPECTED_FAMILIES:
        path = KG_DIR / f"{family}.json"
        if path.is_file():
            result[family] = json.loads(path.read_text(encoding="utf-8"))
    return result


def _all_nodes() -> dict[str, dict[str, object]]:
    """Flat dict of all {fault_id: node} across all 6 files."""
    nodes: dict[str, dict[str, object]] = {}
    for data in _load_all().values():
        for fid, node in cast(dict[str, object], data["nodes"]).items():
            nodes[fid] = cast(dict[str, object], node)
    return nodes


def _load_schema() -> dict[str, object]:
    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# existence and counts
# ---------------------------------------------------------------------------

def test_all_six_files_exist() -> None:
    for family in EXPECTED_FAMILIES:
        path = KG_DIR / f"{family}.json"
        assert path.is_file(), f"missing: {path}"


def test_total_node_count() -> None:
    all_nodes = _all_nodes()
    assert len(all_nodes) == 108, f"expected 108 nodes, got {len(all_nodes)}"


def test_node_count_per_family() -> None:
    for family, expected in EXPECTED_FAMILIES.items():
        data = json.loads(
            (KG_DIR / f"{family}.json").read_text(encoding="utf-8")
        )
        actual = len(data["nodes"])
        assert actual == expected, f"{family}: expected {expected}, got {actual}"


def test_all_fault_ids_present() -> None:
    all_ids = set(_all_nodes().keys())
    missing = EXPECTED_IDS - all_ids
    extra = all_ids - EXPECTED_IDS
    assert not missing, f"missing ids: {sorted(missing)}"
    assert not extra, f"extra ids: {sorted(extra)}"


# ---------------------------------------------------------------------------
# schema validation
# ---------------------------------------------------------------------------

def test_all_nodes_validate_against_schema() -> None:
    schema = _load_schema()
    errors: list[str] = []
    for family in EXPECTED_FAMILIES:
        path = KG_DIR / f"{family}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        try:
            jsonschema.validate(data, schema)
        except jsonschema.ValidationError as exc:
            errors.append(f"{family}: {exc.message}")
    assert not errors, "\n".join(errors)


# ---------------------------------------------------------------------------
# field constraints
# ---------------------------------------------------------------------------

def test_no_unknown_fault_family_values() -> None:
    bad: list[tuple[str, str]] = []
    for fid, node in _all_nodes().items():
        family = node.get("fault_family", "")
        if family not in VALID_FAMILIES:
            bad.append((fid, str(family)))
    assert not bad, f"unknown fault_family values: {bad}"


def test_mechanical_failure_mode_max_280_chars() -> None:
    bad: list[tuple[str, int]] = []
    for fid, node in _all_nodes().items():
        mfm = str(node.get("mechanical_failure_mode", ""))
        if len(mfm) > MECH_FAILURE_MODE_MAX:
            bad.append((fid, len(mfm)))
    assert not bad, f"overlong mechanical_failure_mode: {bad}"


def test_ui_remediation_steps_count() -> None:
    bad: list[tuple[str, int]] = []
    for fid, node in _all_nodes().items():
        steps = node.get("ui_remediation_steps", [])
        if not isinstance(steps, list):
            bad.append((fid, -1))
        else:
            n = len(steps)
            if n < REMEDIATION_STEPS_MIN or n > REMEDIATION_STEPS_MAX:
                bad.append((fid, n))
    assert not bad, f"invalid ui_remediation_steps count: {bad}"


def test_differential_siblings_max_5() -> None:
    bad: list[tuple[str, int]] = []
    for fid, node in _all_nodes().items():
        sibs = node.get("differential_siblings", [])
        if isinstance(sibs, list) and len(sibs) > DIFF_SIBLINGS_MAX:
            bad.append((fid, len(sibs)))
    assert not bad, f"too many differential_siblings: {bad}"


# ---------------------------------------------------------------------------
# cross-file integrity
# ---------------------------------------------------------------------------

def test_differential_siblings_resolve() -> None:
    all_ids = set(_all_nodes().keys())
    dangling: list[tuple[str, str]] = []
    for fid, node in _all_nodes().items():
        for sib in cast(list[object], node.get("differential_siblings", [])):
            if sib not in all_ids:
                dangling.append((fid, str(sib)))
    assert not dangling, f"dangling siblings: {dangling}"


def test_fault_family_matches_file() -> None:
    bad: list[tuple[str, str, str]] = []
    for family, data in _load_all().items():
        for fid, raw_node in cast(dict[str, object], data["nodes"]).items():
            node = cast(dict[str, object], raw_node)
            node_family = str(node.get("fault_family", ""))
            if node_family != family:
                bad.append((fid, node_family, family))
    assert not bad, f"family mismatch (node_family vs file): {bad}"


# ---------------------------------------------------------------------------
# enum validity
# ---------------------------------------------------------------------------

def test_editor_severity_hint_values() -> None:
    bad: list[tuple[str, str]] = []
    for fid, node in _all_nodes().items():
        hint = node.get("editor_severity_hint")
        if hint is not None and hint not in VALID_SEVERITIES:
            bad.append((fid, str(hint)))
    assert not bad, f"invalid editor_severity_hint: {bad}"
