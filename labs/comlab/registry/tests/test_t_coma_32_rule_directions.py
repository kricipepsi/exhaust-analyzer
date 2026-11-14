"""T-COMA-32: two registry rules gated the opposite way to their own descriptions (found by T-AUD-22c, CK0403/CK0469).

- EL-002 (post-cat exhaust leak): "downstream O2 sees excess oxygen (lean)". A narrowband sensor reads lean below
  the ~0.45 V stoichiometric centre (OBD_VOCABULARY §12.1), so the row is o2_downstream < 0.45, not >= 0.45.
- MW-004 (low compression): "low intake vacuum" is a high MAP; map_kpa < 30.0 was strong vacuum. The row is removed
  until a verified weak-vacuum MAP value exists.
"""
from __future__ import annotations

import json
from pathlib import Path

RULES = Path(__file__).resolve().parents[1] / "rules"


def _rule(file: str, rule_id: str) -> dict:
    data = json.loads((RULES / file).read_text(encoding="utf-8"))
    rules = data["rules"] if isinstance(data, dict) else data
    return next(r for r in rules if r["rule_id"] == rule_id)


def test_el002_downstream_o2_reads_lean() -> None:
    rows = [e for e in _rule("exhaust_leak.json", "EL-002")["obd_evidence"] if e["pid"] == "o2_downstream"]
    assert [(e["operator"], e["value"]) for e in rows] == [("lt", 0.45)]
    assert "lean" in _rule("exhaust_leak.json", "EL-002")["description"]


def test_mw004_has_no_strong_vacuum_row() -> None:
    rule = _rule("mechanical_wear.json", "MW-004")
    assert not [e for e in rule["obd_evidence"] if e["pid"] == "map_kpa" and e["operator"] in ("lt", "le")]
    assert "low intake vacuum" not in rule["description"]
