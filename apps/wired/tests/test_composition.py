from __future__ import annotations

from comlab.schemas.response import OrchestratorFinalUIOutput

from wired.composition import _run_gaslab, diagnose


def _minimal_raw_inputs() -> dict:
    return {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "triage": {
            "tier_1": "rough_idle_shudder",
            "tier_2": "constant_vibration_shudder",
            "occurs_during": "always",
            "engine_state": "running",
            "load_state": "idle",
        },
        "gas": {
            "co": 0.1,
            "co2": 14.5,
            "o2": 0.3,
            "hc": 50,
            "nox": 10,
            "engine_state": "STABILIZED_IDLE",
        },
    }


def _minimal_vin_dna() -> dict:
    return {
        "vin": "WBA4W9C5ZLYYYYYYY",
        "resolved_horizon": "HORIZON_MODERN",
        "cylinder_count": 4,
        "number_of_banks": 1,
        "engine_displacement_liters": 2.0,
        "euro_emission_category": "EURO_6",
        "fuel_delivery_type": "PORT_INJECTION",
        "induction_type": "NATURALLY_ASPIRATED",
        "air_metering_strategy": "MAP_ONLY_SPEED_DENSITY",
        "confidence": "HIGH",
        "emissions": {
            "upstream_o2_type": "NARROWBAND_0_TO_1V",
            "has_catalyst": True,
            "egr_equipped": False,
        },
    }


def test_diagnose_returns_verdict() -> None:
    """Minimal valid raw inputs run end-to-end and return a COMLab verdict."""
    result = diagnose(_minimal_raw_inputs())

    assert isinstance(result, OrchestratorFinalUIOutput)
    assert result.diagnostic_verdict.fault_code


def test_high_idle_forwarded() -> None:
    """Gas ``*_high`` raw fields are forwarded onto COMLab's GasLabPayload mirror."""
    gas_inputs = {
        "co": 0.1,
        "co2": 14.5,
        "o2": 0.3,
        "hc": 50,
        "nox": 10,
        "co_high": 0.2,
        "co2_high": 14.0,
        "o2_high": 0.4,
        "hc_high": 120,
        "nox_high": 15,
        "engine_state": "STABILIZED_IDLE",
    }

    payload = _run_gaslab(gas_inputs, _minimal_vin_dna())

    assert payload.high_idle_hc == 120
    assert payload.high_idle_co == 0.2
    assert payload.high_idle_co2 == 14.0
    assert payload.high_idle_o2 == 0.4
    assert payload.high_idle_nox == 15
    assert payload.high_idle_lambda is not None
