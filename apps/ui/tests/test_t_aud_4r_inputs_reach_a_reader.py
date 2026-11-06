"""T-AUD-4r (F-C5-10 rest): every input the form offers reaches a reader.

R1 no free-text notes; R2 no OBD high-idle panel; R3 no Mode $06 result-state choice; R4 the coolant block test
reaches GASLab. Tags: NEW fails on the base fix/T-AUD-4r spec commit; PIN passes there and after.
"""

from __future__ import annotations

from pathlib import Path

import ui_payload as up

APP = Path(__file__).resolve().parents[1] / "app.py"


def _app():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    assert not at.exception
    return at


def test_no_notes_and_no_obd_high_idle_panel() -> None:
    """NEW: no free-text notes box and no OBDLab (High Idle) panel (OBDLab ticked)."""
    at = _app()
    assert not [t for t in at.text_area if t.label == "Free-text notes"]
    obd = next(c for c in at.checkbox if "OBD" in (c.label or ""))
    obd.check().run()
    assert not at.exception
    labels = [e.label for e in at.expander]
    assert not [x for x in labels if "OBDLab (High Idle)" in x], labels
    assert [x for x in labels if "OBDLab" in x], labels
    assert not [n.key for n in at.number_input if (n.key or "").startswith("obd_") and n.key.endswith("_high")]


def test_mode06_rows_have_no_state_choice() -> None:
    """NEW: a Mode $06 row offers the margin only; the source shows no result-state selectbox."""
    src = APP.read_text(encoding="utf-8")
    assert "mon_state_" not in src
    assert "DTCLab derives it from the margin" in src


def test_block_test_widget_reaches_the_gas_payload() -> None:
    """NEW: the GASLab panel offers the coolant block test, and the app sends its value."""
    at = _app()
    box = next(c for c in at.checkbox if c.key == "gas_block_test")
    assert box.value is False
    src = APP.read_text(encoding="utf-8")
    assert '"gas_block_test_passed": gas_block_test,' in src


def test_block_test_payload_mapping() -> None:
    """PIN: a ticked block test reaches gas.block_test_passed; unticked sends nothing."""
    base = {"gas_module": True, "gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}
    assert up.build_diagnose_payload(dict(base, gas_block_test_passed=True))["gas"]["block_test_passed"] is True
    assert "block_test_passed" not in up.build_diagnose_payload(dict(base, gas_block_test_passed=False))["gas"]


def test_block_test_help_names_the_coolant_test() -> None:
    """NEW: the tooltip describes the coolant block test, not a backpressure test."""
    text = up.FIELD_HELP["gas_block_test_passed"].explanation
    assert "coolant" in text and "backpressure" not in text
