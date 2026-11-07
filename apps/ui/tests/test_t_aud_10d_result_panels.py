"""T-AUD-10d (F-C5-7): severity ribbon, skipped-lab notices, horizon meaning, impacted subsystems.

Tags: NEW fails on the base spec commit (no helpers).
"""

from __future__ import annotations

import typing
from pathlib import Path
from types import SimpleNamespace as NS

import ui_payload as U
from comlab.schemas.response import HorizonLit, SeverityLit

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_every_severity_has_a_banner() -> None:
    """NEW: each SeverityLit value maps to a Streamlit call and PRD 5.1 copy."""
    assert set(U.SEVERITY_BANNER) == set(typing.get_args(SeverityLit))
    assert U.severity_banner("CRITICAL_IMMEDIATE_STOP") == ("error", "Critical: do not drive.")
    assert U.severity_banner("OPTIMAL_HEALTH")[0] == "success"


def test_routing_notices_follow_the_flags() -> None:
    """NEW: one notice per true flag, in PRD order; none when all four are false."""
    off = NS(suppress_gaslab=False, suppress_obd_live_pids=False, suppress_mode06_ui=False, cold_start_mode=False)
    assert U.routing_notices(off) == []
    non_starter = NS(suppress_gaslab=True, suppress_obd_live_pids=True, suppress_mode06_ui=False, cold_start_mode=False)
    got = U.routing_notices(non_starter)
    assert len(got) == 2 and got[0].startswith("Gas analyser inputs skipped") and got[1].startswith("Live OBD PIDs")


def test_every_horizon_has_a_meaning() -> None:
    """NEW: each HorizonLit value has an era sentence."""
    assert set(U.HORIZON_MEANING) == set(typing.get_args(HorizonLit))
    assert "Euro 3-4" in U.horizon_meaning("HORIZON_ADAPTIVE")


def test_app_renders_the_four_panels() -> None:
    """NEW: app.py calls the three helpers and renders impacted_subsystems."""
    text = APP.read_text(encoding="utf-8")
    for needle in ("severity_banner(analytics.severity_level)", "routing_notices(meta.lab_routing_directive)",
                   "horizon_meaning(meta.resolved_horizon)", "enrichment.impacted_subsystems"):
        assert needle in text, needle
