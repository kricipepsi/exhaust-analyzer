from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from registry.integration_shim import RegistryV2Router


COMLAB_ROOT = Path(__file__).resolve().parents[2]
COMLAB_PROPOSALS_DIR = COMLAB_ROOT / "comlab" / "config" / "proposals"
COMLAB_KG_DIR = (COMLAB_ROOT / "comlab" / "config" / "kg").resolve()

OIL_TIER2_MARKERS = {
    "blue_smoke_on_cold_start_clears",
    "blue_smoke_under_acceleration",
    "oil_loss_no_visible_smoke",
}
OIL_KG_NODE_IDS = {"P_NEW_09", "P_NEW_10", "P_NEW_11", "P_NEW_12", "P_NEW_13"}
FUTURE_CONSUMER_TASK_IDS = {"T-OIL-R4", "T-OIL-R5", "U-OIL-KG-1"}


def _loads_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _future_consumer_mentions_task(value: object) -> bool:
    return isinstance(value, str) and any(
        task_id in value for task_id in FUTURE_CONSUMER_TASK_IDS
    )


def test_live_route_does_not_load_comlab_kg(monkeypatch: Any) -> None:
    opened_kg_paths: list[Path] = []
    original_open = Path.open

    def guarded_open(self: Path, *args: Any, **kwargs: Any) -> Any:
        resolved = self.resolve()
        if resolved.is_relative_to(COMLAB_KG_DIR):
            opened_kg_paths.append(resolved)
            raise AssertionError(f"live registry route opened COMLab KG: {resolved}")
        return original_open(self, *args, **kwargs)

    monkeypatch.setattr(Path, "open", guarded_open)

    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(
        {
            "gas_lab_output": {
                "chemical_state": "WORN_PISTON_RINGS",
                "sample_validity": "VALID",
                "gas_hc": 380,
                "gas_co2": 12.0,
                "gas_o2": 2.0,
            },
            "dtc_lab_output": {"confirmed_dtcs": []},
        }
    )

    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-001"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-001"
    assert opened_kg_paths == []


def test_oil_proposals_have_future_consumer() -> None:
    entries = _loads_yaml(COMLAB_PROPOSALS_DIR / "entries.yaml")
    proposals = _loads_yaml(COMLAB_PROPOSALS_DIR / "proposals.yaml")

    symptom_registry = next(entry for entry in entries if entry["id"] == "COMLab-A")
    oil_mappings = [
        mapping
        for mapping in symptom_registry["mappings"]
        if mapping.get("tier_1") == "oil_consumption"
        and mapping.get("tier_2") in OIL_TIER2_MARKERS
    ]
    assert {mapping["tier_2"] for mapping in oil_mappings} == OIL_TIER2_MARKERS
    for mapping in oil_mappings:
        assert _future_consumer_mentions_task(mapping.get("future_consumer")), mapping

    oil_kg_registry = next(entry for entry in entries if entry["id"] == "COMLab-OIL-KG")
    for family in oil_kg_registry["new_fault_families"]:
        assert _future_consumer_mentions_task(family.get("future_consumer")), family

    proposed_nodes = [
        node
        for proposal in proposals
        for node in proposal.get("fault_nodes", [])
        if node.get("fault_id") in OIL_KG_NODE_IDS
    ]
    assert {node["fault_id"] for node in proposed_nodes} == OIL_KG_NODE_IDS
    for node in proposed_nodes:
        assert node.get("proposal_only") is True, node
        assert _future_consumer_mentions_task(node.get("future_consumer")), node
