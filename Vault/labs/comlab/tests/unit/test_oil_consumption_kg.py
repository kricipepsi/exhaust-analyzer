from __future__ import annotations

from pathlib import Path

import yaml

from comlab.core.fault_atlas_kg import FaultAtlasKG


EXPECTED_OIL_NODES = {
    "P_NEW_09": {
        "fault_name": "oil_consumption_worn_piston_rings",
        "component_group": "Engine Mechanical (Piston Rings)",
    },
    "P_NEW_10": {
        "fault_name": "oil_consumption_worn_valve_stem_seals",
        "component_group": "Engine Mechanical (Valve Stem Seals)",
    },
    "P_NEW_11": {
        "fault_name": "oil_consumption_pcv_stuck_open",
        "component_group": "Engine Mechanical (PCV/Crankcase)",
    },
    "P_NEW_12": {
        "fault_name": "oil_consumption_head_gasket_oil_breach",
        "component_group": "Engine Mechanical (Head Gasket)",
    },
    "P_NEW_13": {
        "fault_name": "oil_consumption_turbo_turbine_seal_leak",
        "component_group": "Engine Mechanical (Turbo Oil Seal)",
    },
}

EXPECTED_NEW_FAMILIES = {
    "Engine Mechanical (Piston Rings)",
    "Engine Mechanical (PCV/Crankcase)",
    "Engine Mechanical (Turbo Oil Seal)",
}


def test_t_oil_3_fault_nodes_resolve_from_kg() -> None:
    kg = FaultAtlasKG()

    for fault_id, expected in EXPECTED_OIL_NODES.items():
        node = kg.resolve(fault_id)
        assert node.fault_family == "mechanical_wear"
        assert node.fault_name == expected["fault_name"]
        assert node.component_group == expected["component_group"]
        assert node.ui_remediation_steps


def test_t_oil_3_proposal_registers_new_oil_fault_families() -> None:
    entries_path = (
        Path(__file__).resolve().parents[2]
        / "comlab"
        / "config"
        / "proposals"
        / "entries.yaml"
    )
    entries = yaml.safe_load(entries_path.read_text(encoding="utf-8"))
    oil_kg = next(entry for entry in entries if entry["id"] == "COMLab-OIL-KG")

    assert oil_kg["owning_ledger"] == "planning/oil_consumption T-OIL-3"
    assert {family["name"] for family in oil_kg["new_fault_families"]} == EXPECTED_NEW_FAMILIES
    assert {node["fault_id"] for node in oil_kg["fault_nodes"]} == set(EXPECTED_OIL_NODES)
