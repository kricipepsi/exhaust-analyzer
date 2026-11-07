"""T-AUD-10e (F-C5-7, PRD 5.5): the results pane shows the input echo in a collapsed expander.

Tags: NEW fails on the base fix/T-AUD-10d (no input_echo_rows, no expander).
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import ui_payload as U
from comlab.schemas.ingestion import UserInputEchoAudit, UserInputEchoFieldGroup

APP = Path(__file__).resolve().parents[1] / "app.py"


def _echo(*groups: UserInputEchoFieldGroup) -> UserInputEchoAudit:
    return UserInputEchoAudit(submitted_at=datetime.now(timezone.utc), groups=list(groups))


def test_rows_keep_order_and_format_each_value() -> None:
    """NEW: group and field order kept; None is a dash, a list or dict is JSON, the rest is str."""
    echo = _echo(
        UserInputEchoFieldGroup(screen_id="vehicle_context", label="Vehicle and symptom",
                                fields={"vin": "WME01MC01XH072806", "override_de_cat": True}),
        UserInputEchoFieldGroup(screen_id="obd", label="OBD live data",
                                fields={"shrtft1": 1.0, "shrtft2": None, "engine_rpm": 800}),
        UserInputEchoFieldGroup(screen_id="dtc", label="DTCs and freeze frame",
                                fields={"raw_dtcs": {"$03": ["P0131"]}}),
    )
    assert U.input_echo_rows(echo) == [
        ("Vehicle and symptom", [("vin", "WME01MC01XH072806"), ("override_de_cat", "True")]),
        ("OBD live data", [("shrtft1", "1.0"), ("shrtft2", "—"), ("engine_rpm", "800")]),
        ("DTCs and freeze frame", [("raw_dtcs", '{"$03": ["P0131"]}')]),
    ]


def test_empty_echo_gives_no_rows() -> None:
    """NEW: the sentinel (no groups), an empty group and None all give []."""
    assert U.input_echo_rows(_echo()) == []
    assert U.input_echo_rows(_echo(UserInputEchoFieldGroup(screen_id="gas", label="Gas readings", fields={}))) == []
    assert U.input_echo_rows(None) == []


def test_app_renders_the_echo_collapsed_after_both_branches() -> None:
    """NEW: the expander is collapsed, reads res.user_input_echo_audit and sits after the abstain/verdict split."""
    text = APP.read_text(encoding="utf-8")
    call = text.index("input_echo_rows(res.user_input_echo_audit)")
    assert text.index('st.subheader("🔧 Actionable Remediation")') < text.index("Performance & Perception Analytics") < call
    assert 'st.expander("Show what I typed →", expanded=False)' in text[call:call + 300]
    assert call < text.index("Calibration Caveat")
    # Indented at the pane level (8 spaces), not inside the else branch, so abstain and abort results show it too.
    assert "\n        echo_groups = input_echo_rows(res.user_input_echo_audit)\n" in text
