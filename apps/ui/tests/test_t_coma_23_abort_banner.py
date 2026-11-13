"""T-COMA-23 (F-D2-7): an aborted session shows a red error banner with the code and remediation, never the green
"No fault detected." severity banner."""
from __future__ import annotations

from pathlib import Path

import ui_payload as up
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import SessionMetadata

APP = Path(__file__).resolve().parents[1] / "app.py"
MESSAGE = "Gas readings are missing. Enter all five gas values and re-run."


def _abort():
    meta = SessionMetadata(session_id="6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60", vin_dna_string="WVWZZZ1JZ3W000001",
                           resolved_horizon="HORIZON_MODERN", cylinder_count=4)
    return LabPipelineAggregator().abort_incomplete(meta, "ERR-INPUT-001", MESSAGE)


def test_abort_banner_copy() -> None:
    out = _abort()
    assert up.abort_banner(out.diagnostic_verdict) == f"Diagnosis stopped (ERR-INPUT-001): {MESSAGE}"


def test_app_shows_red_banner_for_an_abort() -> None:
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.session_state["diagnose_result"] = _abort()
    at.run()
    assert f"Diagnosis stopped (ERR-INPUT-001): {MESSAGE}" in [str(e.value) for e in at.error]
    assert "No fault detected." not in [str(s.value) for s in at.success]
