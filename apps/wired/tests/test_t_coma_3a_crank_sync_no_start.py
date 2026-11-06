"""T-COMA-3a: a crank-sync DTC (P0335/P0336) on a will_not_start session names NS-005.

Tags: NEW fails on the base fix/T-COMA-3a spec commit (NS-NO-RULE abstain); PIN passes there and after.
"""

from __future__ import annotations

from typing import Any

from test_t_aud_1a_inputs import DECODABLE_VIN, TRIAGE, _raw

from v7.load_corpus import load_corpus
from wired.composition import diagnose

NON_START = dict(TRIAGE, tier_1="vehicle_starting_issues", tier_2="prolonged_crank_hard_start",
                 engine_state="will_not_start", csv_primary_symptom="non_starter")
FF = {"coolant_temp_c": 85.0, "engine_rpm": 0, "calculated_load_pct": 15.0, "manifold_pressure_kpa": 30.0,
      "short_term_ft1": 0.0, "long_term_ft1": 0.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 12.0,
      "intake_air_temp_c": 25.0, "maf_gps": 2.0, "throttle_pos_pct": 5.0, "fuel_system_status": "CL"}


def _non_starter(codes: list[str]) -> Any:
    dtc = {"raw_dtcs": {"$03": codes}, "raw_freeze_frame": dict(FF), "active_mil": True}
    return diagnose(_raw(vin=DECODABLE_VIN, triage=dict(NON_START), dtc=dtc)).diagnostic_verdict


def test_case_040_names_ns005() -> None:
    """NEW: corpus case_040 (P0335) gives non_starter NS-005, not the NS-NO-RULE abstain."""
    raw = next(r for cid, r, *_ in load_corpus() if cid == "case_040")
    v = diagnose(raw).diagnostic_verdict
    assert (v.fault_family, v.fault_code, v.abstained) == ("non_starter", "NS-005", False)


def test_p0336_names_ns005() -> None:
    """NEW: P0336 alone on a non-starter gives NS-005."""
    v = _non_starter(["P0336"])
    assert (v.fault_family, v.fault_code) == ("non_starter", "NS-005")


def test_p0340_alone_stays_no_rule() -> None:
    """PIN: P0340 (CMP) is not a no-start code here; the non-starter abstains."""
    v = _non_starter(["P0340"])
    assert (v.fault_code, v.abstained) == ("NS-NO-RULE", True)
