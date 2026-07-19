"""Unit tests for comlab.core.fault_atlas_kg.FaultAtlasKG.

Covers the success criteria for T-P3-1:
- resolve() returns correct KGNode for a specific fault_id
- resolve("OPTIMAL_HEALTH") returns the no_fault sentinel
- resolve("NONEXISTENT") raises KeyError
- All 30 fault IDs resolve correctly
- Load time < 200 ms (laptop cold-start bound)
- ValueError on invalid JSON
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest

from comlab.core.fault_atlas_kg import FaultAtlasKG


ALL_29_IDS: list[str] = [
    "ERR-RM-001", "ERR-RM-002", "ERR-RM-003", "ERR-RM-004",
    "ERR-RM-005", "ERR-RM-006", "ERR-RM-007",
    "ERR-LC-001", "ERR-LC-002", "ERR-LC-003", "ERR-LC-004",
    "ERR-LC-005", "ERR-LC-006",
    "ERR-MF-001", "ERR-MF-002", "ERR-MF-003", "ERR-MF-004",
    "ERR-MF-005", "ERR-MF-006", "ERR-MF-007",
    "ERR-SF-001", "ERR-SF-002", "ERR-SF-003", "ERR-SF-004",
    "ERR-SF-005", "ERR-SF-006",
    "ERR-EF-001", "ERR-EF-002",
    "OPTIMAL_HEALTH",
    "P_NEW_09", "P_NEW_10", "P_NEW_11", "P_NEW_12", "P_NEW_13",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def kg() -> FaultAtlasKG:
    """Module-scoped — loaded once for all tests in this file."""
    return FaultAtlasKG()


# ---------------------------------------------------------------------------
# resolve() happy path
# ---------------------------------------------------------------------------


def test_resolve_returns_correct_kgnode(kg: FaultAtlasKG) -> None:
    node = kg.resolve("ERR-RM-001")
    assert node.fault_name == "worn_valve_stem_seals"
    assert node.fault_family == "rich_mixture"
    assert node.component_group == "Engine Cylinder Head Assembly"
    assert len(node.impacted_subsystems) >= 1
    assert len(node.ui_remediation_steps) >= 1
    assert len(node.differential_siblings) >= 0


def test_resolve_no_fault_sentinel(kg: FaultAtlasKG) -> None:
    node = kg.resolve("OPTIMAL_HEALTH")
    assert node.fault_name == "no_active_fault_detected"
    assert node.fault_family == "no_fault"
    assert node.component_group == "N/A"


def test_resolve_unknown_raises_keyerror(kg: FaultAtlasKG) -> None:
    with pytest.raises(KeyError) as excinfo:
        kg.resolve("NONEXISTENT_ID_THAT_DOES_NOT_EXIST")
    assert "NONEXISTENT_ID_THAT_DOES_NOT_EXIST" in str(excinfo.value)


# ---------------------------------------------------------------------------
# Full dataset coverage
# ---------------------------------------------------------------------------


def test_all_30_ids_resolve(kg: FaultAtlasKG) -> None:
    failed: list[str] = []
    for fid in ALL_29_IDS:
        try:
            node = kg.resolve(fid)
            assert node.fault_name, f"{fid} has empty fault_name"
        except Exception as exc:
            failed.append(f"{fid}: {exc}")
    assert not failed, f"{len(failed)} ID(s) failed to resolve: {failed}"


def test_node_count_is_57(kg: FaultAtlasKG) -> None:
    assert kg.node_count == 108  # T-OIL-3: oil-consumption KG nodes added


# ---------------------------------------------------------------------------
# Performance
# ---------------------------------------------------------------------------


def test_load_time_under_200_ms() -> None:
    """Cold-load time measured from __init__ — must be < 200 ms."""
    start = time.perf_counter()
    FaultAtlasKG()
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert elapsed_ms < 200, f"Load took {elapsed_ms:.1f} ms (limit: 200 ms)"


# ---------------------------------------------------------------------------
# Validation / error handling
# ---------------------------------------------------------------------------


def test_valueerror_on_invalid_json(tmp_path: Path) -> None:
    """A JSON file that is not valid JSON must raise ValueError."""
    kg_dir = tmp_path / "kg_bad_json"
    kg_dir.mkdir()
    (kg_dir / "broken.json").write_text("not valid json", encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        FaultAtlasKG(kg_dir=kg_dir)
    assert "Invalid JSON" in str(excinfo.value)


def test_valueerror_on_schema_mismatch(tmp_path: Path) -> None:
    """A JSON file with a schema violation must raise ValueError."""
    kg_dir = tmp_path / "kg_bad_schema"
    kg_dir.mkdir()
    bad_payload = {
        "schema_version": "bad_version",  # fails pattern ^\d+\.\d+$
        "fault_family": "rich_mixture",
        "nodes": {},
    }
    (kg_dir / "bad.json").write_text(json.dumps(bad_payload), encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        FaultAtlasKG(kg_dir=kg_dir)
    assert "Schema validation failed" in str(excinfo.value)


def test_valueerror_on_family_mismatch(tmp_path: Path) -> None:
    """A node whose fault_family differs from the file family must raise."""
    kg_dir = tmp_path / "kg_bad_family"
    kg_dir.mkdir()
    bad_payload = {
        "schema_version": "1.0",
        "fault_family": "rich_mixture",
        "nodes": {
            "ERR-RM-001": {
                "fault_name": "test",
                "fault_family": "lean_condition",  # mismatched
                "component_group": "Test",
                "impacted_subsystems": ["Test"],
                "mechanical_failure_mode": "Test.",
                "ui_remediation_steps": ["Test."],
                "differential_siblings": [],
            }
        },
    }
    (kg_dir / "mismatch.json").write_text(json.dumps(bad_payload), encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        FaultAtlasKG(kg_dir=kg_dir)
    assert "fault_family" in str(excinfo.value)


def test_valueerror_on_duplicate_id(tmp_path: Path) -> None:
    """Two files containing the same fault_id must raise ValueError."""
    kg_dir = tmp_path / "kg_dup"
    kg_dir.mkdir()
    node_template = {
        "fault_name": "test",
        "fault_family": "rich_mixture",
        "component_group": "Test",
        "impacted_subsystems": ["Test"],
        "mechanical_failure_mode": "Test.",
        "ui_remediation_steps": ["Test."],
        "differential_siblings": [],
    }
    for idx, (fname, family) in enumerate(
        [("a.json", "rich_mixture"), ("b.json", "misfire")]
    ):
        payload = {
            "schema_version": "1.0",
            "fault_family": family,
            "nodes": {"ERR-DUP-001": dict(node_template, fault_family=family)},
        }
        (kg_dir / fname).write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(ValueError) as excinfo:
        FaultAtlasKG(kg_dir=kg_dir)
    assert "Duplicate fault_id" in str(excinfo.value)


def test_filenotfound_on_empty_kg_dir(tmp_path: Path) -> None:
    kg_dir = tmp_path / "kg_empty"
    kg_dir.mkdir()
    with pytest.raises(FileNotFoundError):
        FaultAtlasKG(kg_dir=kg_dir)
