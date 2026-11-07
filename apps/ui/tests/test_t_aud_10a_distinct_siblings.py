"""T-AUD-10a (F-C5-8): the sibling cards show distinct families, not the first two siblings.

Tags: NEW fails on the base spec commit (no distinct_family_siblings).
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace as NS

import ui_payload as U

APP = Path(__file__).resolve().parents[1] / "app.py"


def _v(winner: str, *fams: str) -> NS:
    sibs = [NS(fault_id=f"S{i}", fault_family=f) for i, f in enumerate(fams)]
    return NS(fault_family=winner, differential_siblings=sibs)


def test_skips_winner_family_and_repeats() -> None:
    """NEW: winner misfire; siblings misfire, misfire, rich, rich, lean -> rich, lean."""
    got = U.distinct_family_siblings(_v("misfire", "misfire", "misfire", "rich_mixture", "rich_mixture", "lean_condition"))
    assert [s.fault_id for s in got] == ["S2", "S4"]


def test_caps_at_two_distinct_families() -> None:
    """NEW (revision 02): three other families -> the first two in COMLab's order; limit=1 -> one."""
    v = _v("misfire", "rich_mixture", "misfire", "lean_condition", "sensor_fault")
    assert [s.fault_id for s in U.distinct_family_siblings(v)] == ["S0", "S2"]
    assert [s.fault_id for s in U.distinct_family_siblings(v, limit=1)] == ["S0"]


def test_fewer_than_two_distinct_is_not_padded() -> None:
    """NEW: only one other family -> one card; none -> no card."""
    assert [s.fault_id for s in U.distinct_family_siblings(_v("misfire", "misfire", "rich_mixture", "misfire"))] == ["S1"]
    assert U.distinct_family_siblings(_v("misfire", "misfire", "misfire")) == []


def test_app_uses_the_helper_in_both_branches() -> None:
    """NEW: both sibling loops in app.py go through the helper; no raw [:2] slice is left."""
    text = APP.read_text(encoding="utf-8")
    assert text.count("enumerate(distinct_family_siblings(verdict))") == 2
    assert "differential_siblings[:2]" not in text
