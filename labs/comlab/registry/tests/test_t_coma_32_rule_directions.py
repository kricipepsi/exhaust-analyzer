"""T-COMA-32: two registry rules gated the opposite way to their own descriptions (found by T-AUD-22c, CK0403/CK0469).

- EL-002 (post-cat exhaust leak): "downstream O2 sees excess oxygen (lean)". A narrowband sensor reads lean below
  the ~0.45 V stoichiometric centre (OBD_VOCABULARY §12.1), so the row is o2_downstream < 0.45, not >= 0.45.
- MW-004 (low compression): "low intake vacuum" is a high MAP; map_kpa < 30.0 was strong vacuum. The row is removed
  until a verified weak-vacuum MAP value exists (T-COMA-33); no MAP row of any direction until then.
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
    rule = _rule("exhaust_leak.json", "EL-002")
    rows = [e for e in rule["obd_evidence"] if e["pid"] == "o2_downstream"]
    assert [(e["operator"], e["value"]) for e in rows] == [("lt", 0.45)]
    assert rows[0]["wiki_ref"] == "OBD_VOCABULARY §12.1"  # narrowband bands; §6 is fault families (review M2)
    assert "downstream O2 sees excess oxygen (lean)" in rule["description"]


def test_mw004_has_no_map_row() -> None:
    rule = _rule("mechanical_wear.json", "MW-004")
    assert not [e for e in rule["obd_evidence"] if e["pid"] == "map_kpa"]  # review M1: no unverified "gt X" either
    assert "low intake vacuum" not in rule["description"]
