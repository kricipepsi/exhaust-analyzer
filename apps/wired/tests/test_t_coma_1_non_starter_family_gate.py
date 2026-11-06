"""T-COMA-1 (F-C1-7) — a will_not_start session is decided by the non_starter family only.

R1 the family gate in the registry shim; R2 the NS-NO-RULE abstain verdict when no non_starter rule matches;
R3 abstain_reason "no_rule". Tags: NEW fails on the base fix/T-COMA-1 spec commit; PIN passes there and after.
"""

from __future__ import annotations

import pytest
from test_t_aud_1a_inputs import DECODABLE_VIN, TRIAGE, _raw

from v7.load_corpus import load_corpus
from wired.composition import diagnose

NON_START = dict(TRIAGE, tier_1="vehicle_starting_issues", engine_state="will_not_start",
                 csv_primary_symptom="non_starter")
GASES = {
    "idle_stoich": {"hc": 80, "co": 0.3, "co2": 14.8, "o2": 0.3, "nox": 50},
    "idle_rich": {"hc": 600, "co": 4.0, "co2": 11.5, "o2": 0.2, "nox": 20},
    "idle_lean": {"hc": 300, "co": 0.1, "co2": 12.0, "o2": 4.0, "nox": 30},
    "crank_lean": {"hc": 2500, "co": 0.2, "co2": 2.0, "o2": 18.0, "nox": 0},
}


def _non_starter(tier_2: str, gas: dict) -> dict:
    return _raw(vin=DECODABLE_VIN, gas=dict(gas, engine_state="STABILIZED_IDLE"),
                triage=dict(NON_START, tier_2=tier_2))


@pytest.mark.parametrize("tier_2", ["prolonged_crank_hard_start", "no_crank_silent", "fast_crank_whining"])
@pytest.mark.parametrize("gas", sorted(GASES))
def test_non_starter_without_a_matching_rule_abstains(tier_2: str, gas: str) -> None:
    """NEW: no non_starter rule matches -> NS-NO-RULE, family non_starter, abstained, reason no_rule."""
    v = diagnose(_non_starter(tier_2, GASES[gas])).diagnostic_verdict
    assert (v.fault_family, v.fault_code) == ("non_starter", "NS-NO-RULE")
    assert v.is_fault_detected and v.abstained and v.abstain_reason == "no_rule"
    assert v.confidence_score == 0.0


def test_non_starter_dtc_rule_wins() -> None:
    """NEW: corpus case_006 (will_not_start, P0230) -> NS-004, not the idle-gas families."""
    raw = {cid: r for cid, r, *_ in load_corpus()}["case_006"]
    v = diagnose(raw).diagnostic_verdict
    assert (v.fault_family, v.fault_code) == ("non_starter", "NS-004")
    assert v.confidence_score == pytest.approx(0.85)
    assert v.abstained is False and v.abstain_reason is None


def test_running_session_is_not_gated() -> None:
    """PIN: the same idle-stoich gas on a running engine keeps its idle-gas verdict (EF-004)."""
    v = diagnose(_raw(vin=DECODABLE_VIN, gas=dict(GASES["idle_stoich"], engine_state="STABILIZED_IDLE"))
                 ).diagnostic_verdict
    assert (v.fault_family, v.fault_code) == ("ecu_fault", "EF-004")
    assert not v.abstained
