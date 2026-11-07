"""T-COMA-5 (F-C1-3): when a no-fault rule wins, the verdict reports no fault and OPTIMAL_HEALTH.

Tags: NEW fails on the base (NF-001 won with is_fault_detected=True, WARNING); PIN passes on the base and after.
"""

from __future__ import annotations

from wired.composition import diagnose

GAS = {"hc": 30, "co": 0.1, "co2": 15.0, "o2": 0.3, "nox": 40, "engine_state": "STABILIZED_IDLE"}
OBD = {
    "pid_oxygen_sensor_volts": 0.45,
    "shrtft1": 0.0,
    "longft1": 0.0,
    "engine_rpm": 800,
    "coolant_temp_c": 90.0,
    "number_of_banks": 1,
    "shrtft2": None,
    "longft2": None,
}


def test_no_fault_winner_is_reported_healthy():
    """NEW: pristine gas and neutral trims -> NF-001 wins -> is_fault_detected False, severity OPTIMAL_HEALTH."""
    res = diagnose({"vin": "UNKNOWNVIN0000000", "gas": GAS, "obd": OBD})
    v = res.diagnostic_verdict
    assert (v.fault_code, v.fault_family) == ("NF-001", "no_fault")  # precondition: the no-fault rule won
    assert v.is_fault_detected is False
    assert res.performance_analytics.severity_level == "OPTIMAL_HEALTH"


def test_fault_winner_still_reports_a_fault():
    """PIN: a fault-family winner keeps is_fault_detected True and WARNING_DEGRADED_PERFORMANCE."""
    res = diagnose({"vin": "UNKNOWNVIN0000000", "gas": GAS})
    v = res.diagnostic_verdict
    assert v.fault_family not in ("no_fault", "invalid_input")
    assert v.is_fault_detected is True
    assert res.performance_analytics.severity_level == "WARNING_DEGRADED_PERFORMANCE"
