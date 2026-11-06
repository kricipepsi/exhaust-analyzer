"""T-COMA-3b: a will_not_start gas sample is a cranking sample; NS-001..003 score from its chemistry.

Tags: NEW fails on the base fix/T-COMA-3b spec commit (GASLab rejects every cranking sample); PIN passes there and after.
"""

from __future__ import annotations

from typing import Any

from test_t_aud_1a_inputs import DECODABLE_VIN, TRIAGE, _raw

from v7.load_corpus import load_corpus
from wired.composition import diagnose

NON_START = dict(TRIAGE, tier_1="vehicle_starting_issues", tier_2="prolonged_crank_hard_start",
                 engine_state="will_not_start", csv_primary_symptom="non_starter")
FF = {"coolant_temp_c": 85.0, "engine_rpm": 200, "calculated_load_pct": 15.0, "manifold_pressure_kpa": 30.0,
      "short_term_ft1": 0.0, "long_term_ft1": 0.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 12.0,
      "intake_air_temp_c": 25.0, "maf_gps": 2.0, "throttle_pos_pct": 5.0, "fuel_system_status": "CL"}
PARTIAL_BURN = {"hc": 1500, "co": 0.5, "co2": 6.0, "o2": 10.0, "nox": 5, "engine_state": "STABILIZED_IDLE"}


def _corpus(case_id: str) -> Any:
    raw = next(r for cid, r, *_ in load_corpus() if cid == case_id)
    return diagnose(raw).diagnostic_verdict


def test_real_003_flooded_names_ns002() -> None:
    """NEW: corpus REAL-003 (CO 3.24 %, CO2 1.16 %) gives NS-002, not the NS-NO-RULE abstain."""
    v = _corpus("REAL-003")
    assert (v.fault_family, v.fault_code, v.abstained) == ("non_starter", "NS-002", False)


def test_case_007_no_fuel_names_ns001() -> None:
    """NEW: corpus case_007 (CO2 4.0 %, CO 0.02 %) gives NS-001."""
    v = _corpus("case_007")
    assert (v.fault_family, v.fault_code, v.abstained) == ("non_starter", "NS-001", False)


def test_partial_burn_with_cranking_rpm_names_ns003() -> None:
    """NEW: CO2 6 %, CO 0.5 % and a 200 rpm freeze frame give NS-003 (INCOMPLETE_COMBUSTION)."""
    dtc = {"raw_dtcs": {"$03": []}, "raw_freeze_frame": dict(FF), "active_mil": False}
    v = diagnose(_raw(vin=DECODABLE_VIN, gas=dict(PARTIAL_BURN), triage=dict(NON_START), dtc=dtc)).diagnostic_verdict
    assert (v.fault_family, v.fault_code, v.abstained) == ("non_starter", "NS-003", False)


def test_component_dtc_outranks_lean_chemistry() -> None:
    """PIN: case_006 (P0230) keeps NS-004 and case_040 (P0335) keeps NS-005 over the lean NS-001."""
    assert _corpus("case_006").fault_code == "NS-004"
    assert _corpus("case_040").fault_code == "NS-005"


def test_running_engine_sample_on_a_non_starter_abstains() -> None:
    """PIN: CO2 14.8 % under will_not_start is not a cranking sample; the session still abstains."""
    v = diagnose(_raw(vin=DECODABLE_VIN, triage=dict(NON_START))).diagnostic_verdict
    assert (v.fault_code, v.abstained, v.abstain_reason) == ("NS-NO-RULE", True, "no_rule")
