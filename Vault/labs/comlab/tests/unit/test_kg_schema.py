"""Unit tests for comlab.schemas.kg + comlab/config/kg/_kg_schema.json.

Covers the success criteria for T-P1-1:
- KGNode validates a valid node
- KGNode rejects mechanical_failure_mode > 280 chars
- KGNode rejects ui_remediation_steps with 9 items
- KGNode rejects unknown fault_family
- _kg_schema.json validates a hand-crafted good node
- _kg_schema.json rejects an invalid node (unknown fault_family)
"""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
from pydantic import ValidationError

from comlab.schemas.kg import KGFile, KGNode


SCHEMA_PATH = (
    Path(__file__).resolve().parents[2]
    / "comlab"
    / "config"
    / "kg"
    / "_kg_schema.json"
)


VALID_NODE_DICT: dict[str, object] = {
    "fault_name": "worn_valve_stem_seals",
    "fault_family": "rich_mixture",
    "component_group": "Engine Mechanical",
    "impacted_subsystems": ["Valve Train"],
    "mechanical_failure_mode": "Oil drawn past worn valve stem seals into combustion chamber.",
    "ui_remediation_steps": ["Inspect for blue smoke at startup."],
    "differential_siblings": ["ERR-RM-002"],
}


# ---------------------------------------------------------------------------
# KGNode (Pydantic) — happy path and rejection
# ---------------------------------------------------------------------------


def test_kgnode_accepts_valid_payload() -> None:
    node = KGNode.model_validate(VALID_NODE_DICT)
    assert node.fault_name == "worn_valve_stem_seals"
    assert node.fault_family == "rich_mixture"
    assert node.differential_siblings == ["ERR-RM-002"]
    assert node.editor_severity_hint is None


def test_kgnode_rejects_mechanical_failure_mode_over_280_chars() -> None:
    payload = dict(VALID_NODE_DICT)
    payload["mechanical_failure_mode"] = "x" * 281  # lld: §3.4 — max_length=280
    with pytest.raises(ValidationError) as excinfo:
        KGNode.model_validate(payload)
    assert "mechanical_failure_mode" in str(excinfo.value)


def test_kgnode_rejects_nine_remediation_steps() -> None:
    payload = dict(VALID_NODE_DICT)
    payload["ui_remediation_steps"] = [f"step {i}" for i in range(9)]  # lld: §3.4 — max_length=8
    with pytest.raises(ValidationError) as excinfo:
        KGNode.model_validate(payload)
    assert "ui_remediation_steps" in str(excinfo.value)


def test_kgnode_rejects_unknown_fault_family() -> None:
    payload = dict(VALID_NODE_DICT)
    payload["fault_family"] = "air_induction"  # not one of the 6 valid families
    with pytest.raises(ValidationError) as excinfo:
        KGNode.model_validate(payload)
    assert "fault_family" in str(excinfo.value)


def test_kgfile_accepts_valid_payload() -> None:
    kg_file = KGFile.model_validate(
        {
            "schema_version": "1.0",
            "fault_family": "rich_mixture",
            "nodes": {"ERR-RM-001": VALID_NODE_DICT},
        }
    )
    assert kg_file.schema_version == "1.0"
    assert "ERR-RM-001" in kg_file.nodes


# ---------------------------------------------------------------------------
# _kg_schema.json (jsonschema) — happy path and rejection
# ---------------------------------------------------------------------------


def _load_schema() -> dict[str, object]:
    with SCHEMA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def test_json_schema_validates_good_file() -> None:
    schema = _load_schema()
    good = {
        "schema_version": "1.0",
        "fault_family": "rich_mixture",
        "nodes": {"ERR-RM-001": VALID_NODE_DICT},
    }
    jsonschema.validate(good, schema)


def test_json_schema_rejects_unknown_fault_family() -> None:
    schema = _load_schema()
    bad_node = dict(VALID_NODE_DICT)
    bad_node["fault_family"] = "air_induction"
    bad = {
        "schema_version": "1.0",
        "fault_family": "rich_mixture",
        "nodes": {"ERR-RM-001": bad_node},
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)


def test_json_schema_rejects_overlong_mechanical_failure_mode() -> None:
    schema = _load_schema()
    bad_node = dict(VALID_NODE_DICT)
    bad_node["mechanical_failure_mode"] = "x" * 281
    bad = {
        "schema_version": "1.0",
        "fault_family": "rich_mixture",
        "nodes": {"ERR-RM-001": bad_node},
    }
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad, schema)
