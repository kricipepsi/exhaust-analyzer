"""T-AUD-4j: the triage reaches COMLab when the VIN does not decode (F-C5-5)."""

from __future__ import annotations

from wired.composition import _symptom_without_vin, diagnose

_TRIAGE = {
    "tier_1": "vehicle_starting_issues",
    "tier_2": "prolonged_crank_hard_start",
    "occurs_during": "cold_only",
    "engine_state": "will_not_start",
    "load_state": "idle",
}
_GAS = {"co": 0.1, "co2": 14.5, "o2": 0.3, "hc": 50, "nox": 10, "engine_state": "STABILIZED_IDLE"}


def test_routing_applies_without_a_decodable_vin() -> None:
    result = diagnose({"vin": "UNKNOWNVIN0000000", "triage": dict(_TRIAGE), "gas": dict(_GAS)})
    directive = result.execution_meta.lab_routing_directive
    assert directive.suppress_gaslab is True
    assert directive.cold_start_mode is True


def test_symptom_without_vin_resolves_the_triage() -> None:
    assert _symptom_without_vin(dict(_TRIAGE))


def test_incomplete_or_invalid_triage_gives_no_symptom() -> None:
    assert _symptom_without_vin({}) == {}
    assert _symptom_without_vin(dict(_TRIAGE, tier_2="no_such_tier_2")) == {}
