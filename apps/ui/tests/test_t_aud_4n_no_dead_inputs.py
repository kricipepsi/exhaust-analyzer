"""T-AUD-4n (F-C4-6, F-C5-10 part) — the UI offers no input that no code reads.

R1 Fuel blend and Mileage go; R2 the high-idle measured lambda (gas_lambda_2500) goes. Tags: NEW fails on the base
fix/T-AUD-4n spec commit; PIN passes there and after.
"""

from __future__ import annotations

from pathlib import Path

import ui_payload as up

APP = Path(__file__).resolve().parents[1] / "app.py"
GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}
HIGH = {"gas_hc_high": 40, "gas_co_high": 0.2, "gas_co2_high": 14.9, "gas_o2_high": 0.2, "gas_nox_high": 60}


def _app():
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    assert not at.exception
    return at


def test_no_fuel_blend_or_mileage_widget() -> None:
    """NEW: the form shows no Fuel Blend or Mileage choice (``_check_radio`` draws keyed checkboxes)."""
    keys = [c.key for c in _app().checkbox if c.key]
    assert not [k for k in keys if k.startswith(("fuel_blend__", "mileage__"))], keys
    assert any(k.startswith("dtc_memory_status__") for k in keys)


def test_no_high_idle_measured_lambda_widget() -> None:
    """NEW: the GASLab (High Idle) panel has no measured-lambda input."""
    keys = [n.key for n in _app().number_input]
    assert "gas_lambda_high" not in keys and "gas_hc_high" in keys


def test_payload_sends_no_lambda_2500() -> None:
    """NEW: a stale gas_lambda_2500 widget value is not sent; the four high-idle gases still are."""
    w = {"vin": "", "gas_module": True, "obd_module": False, "dtc_module": False, "dna_module": False,
         "active_number_of_banks": 1, "gas_lambda_2500": 1.02, **GAS, **HIGH}
    gas = up.build_diagnose_payload(w)["gas"]
    assert "lambda_2500" not in gas
    assert {"co_high", "co2_high", "o2_high", "hc_high", "nox_high"} <= set(gas)


def test_field_help_has_no_dead_entries() -> None:
    """NEW: FIELD_HELP has no fuel_blend, mileage or gas_lambda_2500 entry."""
    assert not {"fuel_blend", "mileage", "gas_lambda_2500"} & set(up.FIELD_HELP)
