"""T-COMA-13 (F-C1-8): trims reported while the fuel loop is open are not scored (COMLab_BDD "Trim evidence is
suppressed outside closed loop"). Tags: NEW fails on the base; PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

OPEN = ["OL", "OL_DRIVE", "OL_FAULT"]


def _payload(source: str, status: str | None) -> dict:
    if source == "obd":
        obd = {"shrtft1": 10.0, "longft1": 20.0, "trim_analytics_gate": "VALID", "fuel_system_status": status}
        return {"obd_live_data": obd}
    ff = {"short_term_ft1": 10.0, "long_term_ft1": 20.0, "coolant_temp_c": 90.0, "fuel_system_status": status}
    return {"dtc_lab_output": {"freeze_frame": ff}}


@pytest.mark.parametrize("source", ["obd", "ff"])
@pytest.mark.parametrize("status", OPEN)
def test_open_loop_trims_are_not_scored(source, status):
    """NEW: with the loop open, neither live nor freeze-frame trims resolve."""
    from registry.integration_shim import _resolve_pid_from_payload

    payload = _payload(source, status)
    assert _resolve_pid_from_payload(payload, "shrtft1") is None
    assert _resolve_pid_from_payload(payload, "longft1") is None


@pytest.mark.parametrize("source", ["obd", "ff"])
@pytest.mark.parametrize("status", ["CL", None])
def test_closed_or_unknown_loop_trims_are_scored(source, status):
    """PIN: closed loop, or no status reported, keeps today's trims."""
    from registry.integration_shim import _resolve_pid_from_payload

    payload = _payload(source, status)
    assert _resolve_pid_from_payload(payload, "shrtft1") == 10.0
    assert _resolve_pid_from_payload(payload, "longft1") == 20.0


def test_open_loop_on_normal_gas_is_not_a_lean_verdict():
    """NEW: NORMAL_OPERATION chemistry with +20 % LTFT / +10 % STFT reported in OL_FAULT names no lean or rich fault."""
    from registry.integration_shim import RegistryV2Router

    payload = {
        "gas_lab_output": {"chemical_state": "NORMAL_OPERATION", "sample_validity": "VALID"},
        **_payload("obd", "OL_FAULT"),
    }
    payload["dtc_lab_output"] = {"freeze_frame": _payload("ff", "OL_FAULT")["dtc_lab_output"]["freeze_frame"]}
    out, diag = RegistryV2Router().route_case_with_diagnostics(payload)
    assert out["diagnostic_verdict"]["fault_family"] not in ("lean_condition", "rich_mixture")
