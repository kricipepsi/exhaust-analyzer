from __future__ import annotations

from registry.integration_shim import RegistryV2Router


def test_turbo_routes_to_mw009() -> None:
    """Turbo-shaped payload routes to MW-009."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "POA_SIGNATURE",
            "sample_validity": "VALID",
            "gas_hc": 720,
            "gas_co": 0.07,
            "lambda_chem": 1.00,
            "high_idle_hc": 130,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-009"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-009"


def test_pcv_not_stolen_by_turbo() -> None:
    """The R4 PCV payload (lambda_chem=0.93) still routes to MW-008, not MW-009."""
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


def test_turbo_needs_high_idle() -> None:
    """Legacy payload without high_idle_hc does not fire MW-009."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "POA_SIGNATURE",
            "sample_validity": "VALID",
            "gas_hc": 720,
            "gas_co": 0.07,
            "lambda_chem": 1.00,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] != "MW-009"
    assert diagnostics["winner_rule_id"] != "MW-009"
