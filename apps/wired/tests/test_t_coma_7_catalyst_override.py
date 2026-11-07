"""T-COMA-7 (F-C1-4, ADR-0010): a flashing MIL with a P030x confirmed code forces CRITICAL_IMMEDIATE_STOP on the
default path. Tags: NEW fails on the base (the v2 path returned before the override); PIN passes on the base and after.
"""

from __future__ import annotations

from typing import Any

import pytest
from test_t_aud_1a_inputs import GAS, OBD, TRIAGE

from wired.composition import diagnose

FF = {"coolant_temp_c": 88.0, "engine_rpm": 800, "calculated_load_pct": 25.0, "manifold_pressure_kpa": 35.0,
      "short_term_ft1": 0.0, "long_term_ft1": 0.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0,
      "intake_air_temp_c": 25.0, "maf_gps": 3.0, "throttle_pos_pct": 5.0, "fuel_system_status": "CL"}


def _severity(codes: list[str], flashing: bool) -> Any:
    dtc = {"raw_dtcs": {"$03": codes}, "raw_freeze_frame": dict(FF), "active_mil": True, "mil_flashing": flashing}
    res = diagnose({"vin": "UNKNOWNVIN0000000", "triage": TRIAGE, "gas": GAS, "obd": dict(OBD), "dtc": dtc})
    assert res.execution_meta.degradation_mode != "FATAL_INCOMPLETE"  # precondition: the run completed
    return res.performance_analytics.severity_level


@pytest.mark.parametrize("code", ["P0300", "P0301", "P0304"])
def test_flashing_mil_with_misfire_code_forces_critical(code):
    """NEW: wiki 07 §RULE_CAT_OVERRIDE: mil_flashing and a confirmed ^P030[0-9]$ code -> CRITICAL_IMMEDIATE_STOP."""
    assert _severity([code], flashing=True) == "CRITICAL_IMMEDIATE_STOP"


@pytest.mark.parametrize(("codes", "flashing"), [(["P0301"], False), (["P0171"], True), ([], True)])
def test_override_needs_both_conditions(codes, flashing):
    """PIN: a steady MIL with P0301, or a flashing MIL without a P030x code, is not forced to CRITICAL."""
    assert _severity(codes, flashing) != "CRITICAL_IMMEDIATE_STOP"
