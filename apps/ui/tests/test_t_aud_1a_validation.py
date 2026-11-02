"""T-AUD-1a — UI field validation and payload building (rulings R2, R3, R5, R6, R7).

``validate_widgets`` turns a blank, unticked or pasted form into field issues before a
run; ``build_diagnose_payload`` never raises on user input and omits what was not typed.
Tags: NEW fails on the base ``audit-r2`` commit; PIN passes there and after.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import ui_payload as up

APP = Path(__file__).resolve().parents[1] / "app.py"
SYM = {"triage_tier_1": "⬇️ Lack of Power / Hesitation", "triage_tier_2": "Flat / sluggish always"}
GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}
OBD5 = {
    "obd_upstream_o2_val": 0.45,
    "obd_shrtft1": 1.0,
    "obd_longft1": 2.0,
    "obd_engine_rpm": 800,
    "obd_coolant_temp_c": 90.0,
}
FF12 = {
    "ff_calculated_load_pct": 20.0,
    "ff_engine_rpm": 800,
    "ff_coolant_temp_c": 90.0,
    "ff_short_term_ft1": 1.0,
    "ff_long_term_ft1": 2.0,
    "ff_manifold_pressure_kpa": 35,
    "ff_vehicle_speed_kmh": 0,
    "ff_ignition_advance_deg": 10.0,
    "ff_intake_air_temp_c": 25.0,
    "ff_maf_gps": 3.0,
    "ff_throttle_pos_pct": 0.0,
    "ff_fuel_system_status": "CL",
}


def _widgets(**over: Any) -> dict[str, Any]:
    """The first-load form: all four module boxes ticked, nothing typed."""
    w: dict[str, Any] = {
        "vin": "",
        "dna_module": True,
        "gas_module": True,
        "obd_module": True,
        "dtc_module": True,
        "active_number_of_banks": 1,
        "active_upstream_o2_type": "NARROWBAND",
        "triage_tier_1": "—",
        "triage_tier_2": "—",
        "triage_occurs_during": "Always",
        "triage_engine_state": "Running",
        "dtc_memory_status": "Normal",
        "dtc_confirmed": "",
        "dtc_pending": "",
        "dtc_permanent": "",
        "mode06_monitors": [],
    }
    w.update(over)
    return w


def _fields(widgets: dict[str, Any]) -> set[str]:
    return {issue.field for issue in up.validate_widgets(widgets)}


def _messages(widgets: dict[str, Any]) -> str:
    return "\n".join(issue.message for issue in up.validate_widgets(widgets))


# --- R2 ----------------------------------------------------------------------


def test_r2_invalid_triage_is_field_issue() -> None:
    """NEW: a complete but invalid Tier 1 / Tier 2 pair is a field issue, not a result-pane error."""
    w = _widgets(triage_tier_1="🚫 Vehicle Won't Start", triage_tier_2="Flat / sluggish always", **GAS)
    assert "triage_tier_2" in _fields(w)


# --- R3 ----------------------------------------------------------------------


def test_r3_blank_gas_field_is_field_issue() -> None:
    """NEW: GASLab ticked and CO2 blank -> one field issue on gas_co2."""
    assert _fields(_widgets(**SYM, **dict(GAS, gas_co2=None))) == {"gas_co2"}


def test_r3_gaslab_unticked_no_gas_issue() -> None:
    """NEW (correction C6): GASLab unticked -> no gas field issue."""
    assert not {f for f in _fields(_widgets(gas_module=False, **SYM)) if f.startswith("gas_")}


def test_r3_high_idle_help_states_all_or_nothing() -> None:
    """NEW: the high-idle field help states the all-or-nothing rule."""
    for key in ("gas_hc_high", "gas_co_high", "gas_co2_high", "gas_o2_high", "gas_nox_high"):
        assert "all five" in up.FIELD_HELP[key].explanation


def test_r3_gaslab_untick_keeps_values_apptest() -> None:
    """NEW: GASLab untick and re-tick keeps the typed low-idle values."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    typed = {"gas_hc": 120, "gas_co": 0.5, "gas_co2": 14.5, "gas_o2": 0.4, "gas_nox": 30}
    for key, value in typed.items():
        at.number_input(key=key).set_value(value)
    at.run()
    gas_box = next(c for c in at.checkbox if c.label == "GASLab")
    gas_box.uncheck()
    at.run()
    gas_box = next(c for c in at.checkbox if c.label == "GASLab")
    gas_box.check()
    at.run()
    assert [at.number_input(key=k).value for k in typed] == list(typed.values())


# --- R5 ----------------------------------------------------------------------


def test_r5_untouched_obd_and_dtc_omitted() -> None:
    """NEW (correction C7): default OBD/DTC boxes ticked and untouched -> no obd and no dtc dict."""
    payload = up.build_diagnose_payload(_widgets(**SYM, **GAS))
    assert "obd" not in payload
    assert "dtc" not in payload
    assert not up.validate_widgets(_widgets(**SYM, **GAS))


def test_r5_one_obd_value_requires_five() -> None:
    """NEW: one live OBD value typed -> the other 4 required OBD fields are field issues."""
    assert _fields(_widgets(dtc_module=False, obd_engine_rpm=800, **SYM, **GAS)) == {
        "obd_upstream_o2_val",
        "obd_shrtft1",
        "obd_longft1",
        "obd_coolant_temp_c",
    }


def test_r5_o2_type_none_is_field_issue() -> None:
    """NEW (correction C5): O2 type NONE with every other OBD field typed -> issue on the O2 type."""
    w = _widgets(dtc_module=False, active_upstream_o2_type="NONE", **SYM, **GAS, **OBD5)
    assert _fields(w) == {"active_upstream_o2_type"}


def test_r5_misfire_only_sends_no_obd() -> None:
    """NEW (correction C4): a misfire-cylinder pick alone sends no OBD dict, and the run is not OBD-incomplete."""
    from wired import diagnose

    w = _widgets(
        dtc_module=False,
        triage_tier_1="🔧 Rough Idle / Shudder",
        triage_tier_2="Constant shudder / vibration",
        symptom_misfire_cylinder=2,
        active_cylinder_count=4,
        **GAS,
    )
    payload = up.build_diagnose_payload(w)
    assert "obd" not in payload
    assert not up.validate_widgets(w)
    assert diagnose(payload).diagnostic_verdict.fault_code != "OBD_INPUT_INCOMPLETE"


def test_r5_confirmed_code_requires_freeze_frame() -> None:
    """NEW: a confirmed code typed -> each blank freeze-frame field is a field issue."""
    fields = _fields(_widgets(obd_module=False, dtc_confirmed="P0171", **SYM, **GAS))
    assert fields == {k for k in FF12}


def test_r5_mil_only_sends_dtc_with_codes_cleared() -> None:
    """PIN (correction C7): MIL ticked -> a DTC dict is sent, carrying codes_cleared."""
    payload = up.build_diagnose_payload(_widgets(obd_module=False, dtc_active_mil=True, **SYM, **GAS))
    assert payload["dtc"]["active_mil"] is True
    assert payload["dtc"]["codes_cleared"] is False


def test_r5_mode06_row_sends_dtc() -> None:
    """PIN (correction K3): a valid Mode 06 row alone sends the DTC dict (the base sends one whenever DTCLab is ticked)."""
    w = _widgets(obd_module=False, mode06_monitors=[{"monitor_id": "MID_21_TID_01", "margin_pct": 5.0}],
                 **SYM, **GAS)
    payload = up.build_diagnose_payload(w)
    assert payload["dtc"]["raw_mode06"] == {"MID_21_TID_01": 5.0}
    assert "codes_cleared" in payload["dtc"]


# --- R6 ----------------------------------------------------------------------


def test_r6_dtc_separators_and_notes() -> None:
    """NEW: comma, semicolon, slash and space split; a parenthesised note is not a token."""
    for text in ("P0171, P0420", "P0171;P0420", "P0171/P0420", "p0171 p0420 (pending)"):
        w = _widgets(obd_module=False, dtc_confirmed=text, **SYM, **GAS, **FF12)
        assert up.build_diagnose_payload(w)["dtc"]["raw_dtcs"]["$03"] == ["P0171", "P0420"], text
        assert not up.validate_widgets(w), text


def test_r6_invalid_tokens_listed_and_omitted() -> None:
    """NEW: invalid tokens are listed in a field issue and left out of the payload."""
    w = _widgets(obd_module=False, dtc_pending="P0171 GARBAGE X12", **SYM, **GAS)
    assert up.build_diagnose_payload(w)["dtc"]["raw_dtcs"]["$07"] == ["P0171"]
    assert "dtc_pending" in _fields(w)
    assert "GARBAGE" in _messages(w) and "X12" in _messages(w)


def test_r6_invalid_monitor_id_listed_and_omitted() -> None:
    """NEW: an invalid Monitor ID is listed in a field issue and left out of the payload."""
    rows = [{"monitor_id": "21-01", "margin_pct": 5.0}, {"monitor_id": "MID_21_TID_01", "margin_pct": 4.0}]
    w = _widgets(obd_module=False, mode06_monitors=rows, **SYM, **GAS, **FF12)
    assert up.build_diagnose_payload(w)["dtc"]["raw_mode06"] == {"MID_21_TID_01": 4.0}
    assert "mode06_monitors" in _fields(w)
    assert "21-01" in _messages(w)


# --- R7 ----------------------------------------------------------------------


def test_r7_blank_form_warns_and_skips_diagnose_apptest() -> None:
    """NEW: a blank first-load form -> field warnings, no st.error, diagnose() not called."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    next(b for b in at.button if b.label == "🔬 Run Diagnostic Seam").click()
    at.run()
    assert not at.exception
    assert not [e.value for e in at.error]
    assert len(at.warning) >= 5
    assert "raw_payload" not in at.session_state
