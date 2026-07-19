from __future__ import annotations

from registry.integration_shim import RegistryV2Router


def test_pcv_routes_to_mw008() -> None:
    """PCV-shaped payload routes to MW-008."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "POA_SIGNATURE",
            "sample_validity": "VALID",
            "gas_hc": 610,
            "lambda_chem": 0.93,
            "high_idle_hc": 170,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-008"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-008"


def test_rings_not_stolen_by_pcv() -> None:
    """The R2 rings payload still routes to MW-001, not MW-008."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
            "gas_co2": 12.0,
            "gas_o2": 2.0,
            "high_idle_hc": 450,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-001"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-001"


def test_pcv_needs_high_idle() -> None:
    """A legacy payload without high_idle_hc does not fire MW-008."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "POA_SIGNATURE",
            "sample_validity": "VALID",
            "gas_hc": 610,
            "lambda_chem": 0.93,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] != "MW-008"
    assert diagnostics["winner_rule_id"] != "MW-008"
