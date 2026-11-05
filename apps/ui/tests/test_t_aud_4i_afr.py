"""T-AUD-4i — a wideband-AFR reading is sent to OBDLab as lambda (F-C5-3)."""

from __future__ import annotations

from typing import Any

import pytest

import ui_payload as up

_W: dict[str, Any] = {
    "vin": "WVWZZZ1KZAP012480",
    "dna_module": True,
    "gas_module": False,
    "obd_module": True,
    "dtc_module": False,
    "active_number_of_banks": 1,
    "obd_shrtft1": 1.0,
    "obd_longft1": 2.0,
    "obd_engine_rpm": 800,
    "obd_coolant_temp_c": 90.0,
}


@pytest.mark.parametrize(("afr", "lam"), [(14.7, 1.0), (10.0, 0.6803), (20.0, 1.3605)])
def test_afr_is_sent_as_lambda(afr: float, lam: float) -> None:
    p = up.build_diagnose_payload(dict(_W, active_upstream_o2_type="WIDEBAND_AFR", obd_upstream_o2_val=afr))
    assert p["obd"]["pid_wideband_equivalence_ratio"] == lam


def test_wideband_lambda_is_unchanged() -> None:
    p = up.build_diagnose_payload(dict(_W, active_upstream_o2_type="WIDEBAND_LAMBDA", obd_upstream_o2_val=0.95))
    assert p["obd"]["pid_wideband_equivalence_ratio"] == 0.95
