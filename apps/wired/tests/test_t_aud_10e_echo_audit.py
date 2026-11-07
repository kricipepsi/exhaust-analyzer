"""T-AUD-10e (F-C5-7, PRD 5.5): wired.diagnose echoes the typed inputs in user_input_echo_audit.

Tags: NEW fails on the base fix/T-AUD-10d (wired sends no echo, so COMLab emits the empty sentinel).
"""

from __future__ import annotations

import copy
from typing import Any

from wired.composition import diagnose

DECODABLE_VIN = "WME01MC01XH072806"
TRIAGE = {
    "tier_1": "lack_of_power_hesitation",
    "tier_2": "flat_sluggish_always",
    "occurs_during": "always",
    "engine_state": "running",
    "load_state": "idle",
}
GAS = {"hc": 80, "co": 0.3, "co2": 14.8, "o2": 0.3, "nox": 50, "engine_state": "STABILIZED_IDLE"}
OBD = {
    "pid_oxygen_sensor_volts": 0.45,
    "shrtft1": 1.0,
    "longft1": 2.0,
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "number_of_banks": 1,
    "shrtft2": None,
    "longft2": None,
}
DTC = {"raw_dtcs": {"$03": ["P0131", "P0300"], "$07": ["P0340"]}}


def _groups(res) -> list[tuple[str, str, dict[str, Any]]]:
    return [(g.screen_id, g.label, g.fields) for g in res.user_input_echo_audit.groups]


def test_full_run_echoes_every_input_verbatim() -> None:
    """NEW: one group per sent input, in screen order, with the values as typed (checked after the run)."""
    raw = {"vin": DECODABLE_VIN, "triage": TRIAGE, "gas": GAS, "obd": OBD,
           "overrides": {"upstream_o2_type": "NARROWBAND", "de_cat": True}}
    sent = copy.deepcopy(raw)
    res = diagnose(raw)
    assert res.execution_meta.degradation_mode == "FULL_FUSION"
    assert _groups(res) == [
        ("vehicle_context", "Vehicle and symptom",
         {"vin": DECODABLE_VIN, **TRIAGE, "override_upstream_o2_type": "NARROWBAND", "override_de_cat": True}),
        ("gas", "Gas readings", sent["gas"]),
        ("obd", "OBD live data", sent["obd"]),
    ]
    assert raw == sent


def test_absent_inputs_give_no_group() -> None:
    """NEW: only the vehicle group (VIN alone, no triage) and gas when nothing else is sent."""
    res = diagnose({"vin": "UNKNOWNVIN0000000", "gas": GAS})
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"
    assert _groups(res) == [
        ("vehicle_context", "Vehicle and symptom", {"vin": "UNKNOWNVIN0000000"}),
        ("gas", "Gas readings", GAS),
    ]


def test_incomplete_input_abort_carries_the_echo() -> None:
    """NEW: the incomplete-input abort (a DTC with no freeze frame, PRD 5.8) still echoes what was typed."""
    res = diagnose({"vin": "UNKNOWNVIN0000000", "triage": TRIAGE, "gas": GAS, "obd": OBD, "dtc": DTC})
    assert res.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert "Freeze frame is incomplete" in res.diagnostic_verdict.actionable_remediation
    assert _groups(res) == [
        ("vehicle_context", "Vehicle and symptom", {"vin": "UNKNOWNVIN0000000", **TRIAGE}),
        ("gas", "Gas readings", GAS),
        ("obd", "OBD live data", OBD),
        ("dtc", "DTCs and freeze frame", DTC),
    ]


def test_out_of_range_abort_carries_the_echo() -> None:
    """NEW: the out-of-range abort (catalyst_index_ratio 5.0 > 2.0) still echoes what was typed."""
    obd = dict(OBD, catalyst_index_ratio=5.0)
    res = diagnose({"vin": "UNKNOWNVIN0000000", "triage": TRIAGE, "gas": GAS, "obd": obd})
    assert res.execution_meta.degradation_mode == "FATAL_INCOMPLETE"
    assert "catalyst_index_ratio" in res.diagnostic_verdict.actionable_remediation
    assert _groups(res)[2] == ("obd", "OBD live data", obd)
