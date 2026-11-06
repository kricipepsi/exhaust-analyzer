"""T-AUD-4o (F-C5-9) — the labs get the DNA the form was gated with.

R1 a PARTIAL decode is basic mode (FieldMap §1.2); R2 basic mode pins overrides.upstream_o2_type = NARROWBAND.
Tags: NEW fails on the base fix/T-AUD-4o spec commit; PIN passes there and after.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import ui_payload as up

APP = Path(__file__).resolve().parents[1] / "app.py"
PARTIAL_WIDEBAND_VIN = "WVWZZZ1KZAP012480"  # v7 corpus era2_015: vinlab PARTIAL, WIDEBAND_AFR
GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}
OBD5 = {"obd_upstream_o2_val": 0.45, "obd_shrtft1": 1.0, "obd_longft1": 2.0, "obd_engine_rpm": 800,
        "obd_coolant_temp_c": 90.0, "obd_fuel_sys_status": "CL"}
SYM = {"triage_tier_1": "⬇️ Lack of Power / Hesitation", "triage_tier_2": "Flat / sluggish always"}


def _widgets(**over: Any) -> dict[str, Any]:
    w: dict[str, Any] = {
        "vin": PARTIAL_WIDEBAND_VIN, "dna_module": True, "use_decoded_dna": False, "vin_confidence": "NONE",
        "gas_module": True, "obd_module": True, "dtc_module": False, "active_number_of_banks": 1,
        "active_upstream_o2_type": "NARROWBAND", "triage_occurs_during": "Always", "triage_engine_state": "Running",
    }
    w.update(over)
    return w


def test_partial_decode_is_basic_mode() -> None:
    """NEW: a PARTIAL decode shows its confidence, offers no "Use this decoded DNA" box and the volts O2 field."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    at.text_input(key="vin_input").input(PARTIAL_WIDEBAND_VIN)
    at.run()
    assert not at.exception
    assert any("PARTIAL" in str(i.value) for i in at.info)
    assert not [c for c in at.checkbox if "Use this decoded DNA" in c.label]
    assert [n.label for n in at.number_input if n.key == "obd_o2_up"] == ["Upstream O₂ (V)"]


def test_basic_mode_pins_narrowband() -> None:
    """NEW: basic mode sends overrides.upstream_o2_type NARROWBAND, the type the form used."""
    assert up.build_diagnose_payload(_widgets(**SYM, **GAS, **OBD5))["overrides"] == {"upstream_o2_type": "NARROWBAND"}


def test_partial_wideband_vin_runs_in_basic_mode() -> None:
    """NEW: the era2_015 VIN in basic mode with a volts reading gets a verdict, not OBD_INPUT_INCOMPLETE."""
    from wired import diagnose

    v = diagnose(up.build_diagnose_payload(_widgets(**SYM, **GAS, **OBD5))).diagnostic_verdict
    assert v.fault_code != "OBD_INPUT_INCOMPLETE" and v.fault_family != "invalid_input"


def test_high_decode_keeps_its_own_o2_type() -> None:
    """PIN: a HIGH decode with no override pick sends no overrides."""
    w = _widgets(use_decoded_dna=True, vin_confidence="HIGH", active_upstream_o2_type="WIDEBAND_AFR", **SYM, **GAS)
    assert "overrides" not in up.build_diagnose_payload(w)
