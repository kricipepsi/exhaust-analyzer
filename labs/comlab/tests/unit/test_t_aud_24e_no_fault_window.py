from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_NO_FAULT_RULES_PATH = Path(__file__).resolve().parents[2] / "registry" / "rules" / "no_fault.json"


def _obd_evidence_values(rule: dict[str, Any]) -> dict[tuple[str, str], Any]:
    return {
        (entry["pid"], entry["operator"]): entry["value"]
        for entry in rule["obd_evidence"]
        if "value" in entry
    }


def test_no_fault_gas_window_matches_sourced_healthy_values() -> None:
    data = json.loads(_NO_FAULT_RULES_PATH.read_text(encoding="utf-8"))
    rules_by_id = {rule["rule_id"]: rule for rule in data["rules"]}

    nf001_values = _obd_evidence_values(rules_by_id["NF-001"])
    nf002_values = _obd_evidence_values(rules_by_id["NF-002"])

    assert nf001_values[("co", "le")] == 0.3  # wiki: §2 / S001 DVSA MOT 8.2.1
    assert nf001_values[("o2", "le")] == 0.5  # wiki: §2 / S023 working catalyst ceiling
    assert nf002_values[("nox", "le")] == 50.0  # wiki: §8.5 / S028 idle NOx cap
