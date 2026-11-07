"""T-AUD-10d (F-C5-7): severity ribbon, skipped-lab notices, horizon meaning, impacted subsystems.

Tags: NEW fails on the base spec commit (no helpers). Revision 02: exact copy, all four notices, placement order.
"""

from __future__ import annotations

import typing
from pathlib import Path
from types import SimpleNamespace as NS

import ui_payload as U
from comlab.schemas.response import HorizonLit, LabRoutingDirectiveOut, SeverityLit

APP = Path(__file__).resolve().parents[1] / "app.py"


def test_every_severity_has_its_exact_banner() -> None:
    """NEW: each SeverityLit value maps to the PRD 5.1 call and copy, exactly."""
    assert set(U.SEVERITY_BANNER) == set(typing.get_args(SeverityLit))
    assert U.severity_banner("CRITICAL_IMMEDIATE_STOP") == ("error", "Critical: do not drive.")
    assert U.severity_banner("WARNING_DEGRADED_PERFORMANCE") == ("warning", "Warning: safe to drive, schedule repair.")
    assert U.severity_banner("OPTIMAL_HEALTH") == ("success", "No fault detected.")


def test_routing_notices_follow_the_flags() -> None:
    """NEW: one exact PRD 5.6 notice per true flag, in PRD order; none when all four are false."""
    flags = ("suppress_gaslab", "suppress_obd_live_pids", "suppress_mode06_ui", "cold_start_mode")
    assert tuple(f for f, _ in U.ROUTING_NOTICES) == flags
    assert set(flags) <= set(LabRoutingDirectiveOut.model_fields)
    assert U.routing_notices(NS(**{f: False for f in flags})) == []
    assert U.routing_notices(NS(**{f: True for f in flags})) == [
        "Gas analyser inputs skipped because the symptom is 'vehicle won't start'.",
        "Live OBD PIDs skipped because the engine was not running.",
        "Mode $06 monitor section skipped — monitors are not ready when the engine is not running.",
        "Cold-start hypothesis was active — some warm-only rules were down-weighted.",
    ]


def test_every_horizon_has_its_exact_meaning() -> None:
    """NEW: each HorizonLit value has its era sentence (wiki 04 era table), exactly."""
    assert set(U.HORIZON_MEANING) == set(typing.get_args(HorizonLit))
    assert U.horizon_meaning("HORIZON_LEGACY") == "Euro 1-2 era tuning applied (pre-1997 to about 2001)."
    assert U.horizon_meaning("HORIZON_ADAPTIVE") == "Euro 3-4 era tuning applied (about 2001-2011)."
    assert U.horizon_meaning("HORIZON_MODERN") == "Euro 5-6 era tuning applied (about 2011 onward)."


def test_app_renders_the_panels_above_the_abstain_split() -> None:
    """NEW: banner, notices and horizon render before `if verdict.abstained:`; badges are in the enrichment block."""
    text = APP.read_text(encoding="utf-8")
    split = text.index("if verdict.abstained:")
    for needle in ("severity_banner(analytics.severity_level)", "routing_notices(meta.lab_routing_directive)",
                   "horizon_meaning(meta.resolved_horizon)"):
        assert -1 < text.index(needle) < split, needle
    assert "getattr(st, sev_kind)(sev_text)" in text
    badges = text.index("if enrichment.impacted_subsystems:")
    assert text.index("Knowledge Graph Enrichment") < badges
    assert '"**Impacted Subsystems:** "' in text[badges:badges + 300]
