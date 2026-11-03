"""T-AUD-1c — freeze frame whenever a DTC dict is sent (R1) and GASLab named in the gas message (R2).

Tags: NEW fails on the base ``audit-r2`` commit; PIN passes there and after.
"""

from __future__ import annotations

from typing import Any

import ui_payload as up
from wired import diagnose

SYM = {"triage_tier_1": "⬇️ Lack of Power / Hesitation", "triage_tier_2": "Flat / sluggish always"}


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


def test_r1_pending_only_requires_ff() -> None:
    """NEW: a pending-only DTC form asks for all 12 freeze-frame fields."""
    assert set(up.FF_REQUIRED_FIELDS) <= _fields(_widgets(dtc_pending="P0171"))


def test_r1_mil_only_requires_ff() -> None:
    """NEW: a MIL-only DTC form asks for all 12 freeze-frame fields."""
    assert set(up.FF_REQUIRED_FIELDS) <= _fields(_widgets(dtc_active_mil=True))


def test_r1_mode06_only_requires_ff() -> None:
    """NEW: a Mode 06-only DTC form asks for all 12 freeze-frame fields."""
    w = _widgets(mode06_monitors=[{"monitor_id": "MID_01_TID_01", "margin_pct": 5.0}])
    assert set(up.FF_REQUIRED_FIELDS) <= _fields(w)


def test_r1_no_dtc_dict_no_ff_issue() -> None:
    """PIN: nothing typed and MIL unticked sends no DTC dict, so no ``ff_`` issue."""
    assert not {f for f in _fields(_widgets()) if f.startswith("ff_")}


def test_r2_gas_message_names_gaslab() -> None:
    """NEW: a run with GASLab unticked tells the user to tick GASLab."""
    w = _widgets(gas_module=False, obd_module=False, dtc_module=False, **SYM)
    result = diagnose(up.build_diagnose_payload(w))
    verdict = result.diagnostic_verdict
    assert verdict.fault_code == "GAS_INPUT_INCOMPLETE"
    assert "Tick GASLab" in verdict.actionable_remediation


def test_r2_gas_help_says_required() -> None:
    """NEW: the GASLab help text says the module is required for every run."""
    assert "Required for every run" in up.FIELD_HELP["gas_module"].explanation
