"""T-AUD-4m (F-C5-11) — choosing "Rough Idle" no longer writes fabricated misfire counts.

R1 build_diagnose_payload sends no symptom-derived per_cylinder_misfire_counts; R2 the "Misfiring cylinder" slider is
gone. Tags: NEW fails on the base fix/T-AUD-4m spec commit; PIN passes there and after.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import ui_payload as up

APP = Path(__file__).resolve().parents[1] / "app.py"
GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}
OBD5 = {"obd_upstream_o2_val": 0.45, "obd_shrtft1": 1.0, "obd_longft1": 2.0, "obd_engine_rpm": 800,
        "obd_coolant_temp_c": 90.0}
ROUGH = {"triage_tier_1": "🔧 Rough Idle / Shudder", "triage_tier_2": "Surging / hunting idle"}


def _widgets(**over: Any) -> dict[str, Any]:
    w: dict[str, Any] = {
        "vin": "", "dna_module": True, "gas_module": True, "obd_module": True, "dtc_module": False,
        "active_number_of_banks": 1, "active_upstream_o2_type": "NARROWBAND", "active_cylinder_count": 4,
        "triage_occurs_during": "Always", "triage_engine_state": "Running",
    }
    w.update(over)
    return w


def test_rough_idle_sends_no_misfire_counts() -> None:
    """NEW: Rough Idle with a cylinder value and live OBD -> the OBD payload holds no per_cylinder_misfire_counts."""
    payload = up.build_diagnose_payload(_widgets(symptom_misfire_cylinder=1, **ROUGH, **GAS, **OBD5))
    assert "obd" in payload
    assert "per_cylinder_misfire_counts" not in payload["obd"]


def test_rough_idle_without_live_obd_sends_no_obd() -> None:
    """PIN: Rough Idle with no live OBD value typed -> no OBD dict at all."""
    payload = up.build_diagnose_payload(_widgets(**ROUGH, **GAS))
    assert "obd" not in payload


def test_rough_idle_shows_no_misfire_slider() -> None:
    """NEW: picking Rough Idle shows no "Misfiring cylinder" slider."""
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    next(s for s in at.selectbox if s.label == "Primary symptom (Tier 1)").set_value(ROUGH["triage_tier_1"])
    at.run()
    next(s for s in at.selectbox if s.label == "Subfield filter (Tier 2)").set_value(ROUGH["triage_tier_2"])
    at.run()
    assert not at.exception
    assert [s.label for s in at.slider if s.label == "Misfiring cylinder"] == []
