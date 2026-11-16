"""T-AUD-24k: the SF perception-delta gates sit outside healthy OBD-to-analyser agreement (|delta| 0.05)."""

import json
from pathlib import Path

import pytest

RULES = Path(__file__).resolve().parents[2] / "registry" / "rules" / "sensor_fault.json"


def _delta_gates() -> list[tuple[str, str, float]]:
    rules = json.loads(RULES.read_text(encoding="utf-8"))["rules"]
    return [
        (r["rule_id"], e["operator"], e["value"])
        for r in rules
        for k in ("obd_evidence", "chemistry_evidence")
        for e in r.get(k, [])
        if e.get("pid") == "lambda_perception_delta"
    ]


def test_sf_delta_gates_count() -> None:
    """SF-001 and SF-002 hold one delta gate each, SF-003 to SF-008 two each: 14 gates."""
    assert len(_delta_gates()) == 14


@pytest.mark.parametrize(("op", "value"), [("gt", 0.05), ("lt", -0.05)])
def test_sf_delta_gates_at_005(op: str, value: float) -> None:
    """T-AUD-23e: +/-0.03 fires inside healthy agreement (S016, S037, S038, S040); +/-0.05 = SF-003 NORMAL band."""
    gates = [g for g in _delta_gates() if g[1] == op]
    assert gates and all(g[2] == pytest.approx(value) for g in gates), gates
