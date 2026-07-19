from __future__ import annotations

from registry.integration_shim import RegistryV2Router


def test_rings_routes_to_mw001() -> None:
    """Worn rings low-idle gas signature routes to MW-001."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_PISTON_RINGS",
            "sample_validity": "VALID",
            "gas_hc": 380,
            "gas_co2": 12.0,
            "gas_o2": 2.0,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-001"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-001"


def test_valve_seals_routes_to_mw002() -> None:
    """Valve seals low-idle transient HC signature routes to MW-002."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "WORN_VALVE_SEALS",
            "sample_validity": "VALID",
            "gas_hc": 450,
            "gas_co2": 12.0,
        },
        "dtc_lab_output": {"confirmed_dtcs": []},
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-002"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-002"


def test_head_gasket_routes_to_mw003() -> None:
    """Head-gasket coolant leak signature routes to MW-003."""
    payload = {
        "gas_lab_output": {
            "chemical_state": "COOLANT_LEAK_INTERNAL",
            "sample_validity": "VALID",
            "gas_hc": 340,
            "gas_co2": 11.0,
            "gas_o2": 2.5,
            "gas_nox": 20.0,
        },
        "dtc_lab_output": {
            "confirmed_dtcs": [],
            "freeze_frame": {
                "coolant_temp_c": 98.0
            }
        },
    }
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    verdict = output["diagnostic_verdict"]
    assert verdict["fault_code"] == "MW-003"
    assert verdict["fault_family"] == "mechanical_wear"
    assert diagnostics["winner_rule_id"] == "MW-003"
