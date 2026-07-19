"""Mock GasLab payload builders for tests.

These produce dicts that conform to ``comlab.schemas.ingestion.GasLabPayload``.
Used by unit and e2e tests so we don't depend on the real GasLab being
installed in the test environment.

Adding new chemical states? Add a builder here. Tests should always go through
these helpers — never hardcode payloads inline.
"""

from __future__ import annotations


def rich_unmetered_intrusion() -> dict:
    """A severe unmetered-fuel intrusion profile (GDI HPFP leak scenario)."""
    return {
        "chemical_state": "GDI_HPFP_INTERNAL_SEAL_LEAK",
        "gas_co": 4.5,
        "gas_hc": 650,
        "gas_co2": 10.0,
        "gas_o2": 0.1,
        "gas_nox": 50,
        "lambda_chem": 0.82,
        "sample_validity": "VALID",
    }


def ignition_misfire_heavy_hc() -> dict:
    """A high-HC ignition misfire signature."""
    return {
        "chemical_state": "IGNITION_MISFIRE",
        "gas_co": 0.2,
        "gas_hc": 1250,
        "gas_co2": 11.5,
        "gas_o2": 4.5,
        "gas_nox": 120,
        "lambda_chem": 1.18,
        "sample_validity": "VALID",
    }


def egr_intake_dilution() -> dict:
    """Stuck-open EGR valve causing intake dilution at idle."""
    return {
        "chemical_state": "INCOMPLETE_OXIDATION",
        "gas_co": 0.4,
        "gas_hc": 120,
        "gas_co2": 13.0,
        "gas_o2": 1.8,
        "gas_nox": 200,
        "lambda_chem": 1.04,
        "sample_validity": "VALID",
    }


def healthy_baseline() -> dict:
    """A clean Euro 6 idle reading — should produce no fault."""
    return {
        "chemical_state": "STOICHIOMETRIC_BURN",
        "gas_co": 0.05,
        "gas_hc": 8,
        "gas_co2": 14.8,
        "gas_o2": 0.3,
        "gas_nox": 15,
        "lambda_chem": 1.00,
        "sample_validity": "VALID",
    }


def warm_idle_baseline() -> dict:
    """Warm-idle healthy gas reading — canonical GASLab baseline for tests."""
    return {
        "chemical_state": "NORMAL_OPERATION",
        "gas_co": 0.1,
        "gas_hc": 50,
        "gas_co2": 14.5,
        "gas_o2": 0.3,
        "gas_nox": 10,
        "lambda_chem": 1.0,
        "sample_validity": "VALID",
    }



def no_obd_legacy(lambda_measured=1.12):
    """Euro 1/2 legacy car -- no OBD channel; technician entered analyser lambda.

    lambda_chem is stoichiometric (1.00) so the Lambda Truth guard does not
    suppress. lambda_measured defaults to 1.12, which diverges from ground
    truth by 0.12 -- enough to trigger O2_SENSOR_BIASED_HIGH at MODERN
    tolerance (0.02) and LEGACY tolerance (0.10) alike.
    Set lambda_measured=None to test the fully-inert no-OBD + no-measured case.

    Consumer: perception_contradiction.select_perception_lambda (T-FX-7).
    """
    return {
        "chemical_state": "NORMAL_OPERATION",
        "gas_co": 0.1,
        "gas_hc": 50,
        "gas_co2": 14.5,
        "gas_o2": 0.3,
        "gas_nox": 10,
        "lambda_chem": 1.0,
        "sample_validity": "VALID",
        "lambda_measured": lambda_measured,
    }


def sample_invalid() -> dict:
    """Triangle sum outside [14, 18] -- probe leak or analyser fault."""
    return {
        "chemical_state": "SAMPLE_INVALID",
        "gas_co": 0.0,
        "gas_hc": 0,
        "gas_co2": 5.0,
        "gas_o2": 20.0,
        "gas_nox": 0,
        "lambda_chem": 1.50,
        "sample_validity": "INVALID",
    }


def catalyst_overwhelmed() -> dict:
    """Raw fuel hitting catalyst from upstream misfire — cat conversion collapsed."""
    return {
        "chemical_state": "CATALYST_OVERWHELMED",
        "gas_co": 3.5,
        "gas_hc": 800,
        "gas_co2": 9.0,
        "gas_o2": 2.0,
        "gas_nox": 60,
        "lambda_chem": 0.88,
        "sample_validity": "VALID",
    }


def exhaust_air_leak() -> dict:
    """Post-combustion air ingress — pre-O2 exhaust leak driving false-lean."""
    return {
        "chemical_state": "EXHAUST_AIR_LEAK",
        "gas_co": 0.1,
        "gas_hc": 30,
        "gas_co2": 13.0,
        "gas_o2": 4.0,
        "gas_nox": 80,
        "lambda_chem": 1.12,
        "sample_validity": "VALID",
    }


def incomplete_combustion() -> dict:
    """Incomplete burn — low compression, blow-by, or weak spark."""
    return {
        "chemical_state": "INCOMPLETE_COMBUSTION",
        "gas_co": 1.2,
        "gas_hc": 400,
        "gas_co2": 10.0,
        "gas_o2": 6.0,
        "gas_nox": 40,
        "lambda_chem": 1.08,
        "sample_validity": "VALID",
    }


def wrong_valve_timing() -> dict:
    """Timing chain/belt off — globally retarded cam phasing."""
    return {
        "chemical_state": "WRONG_VALVE_TIMING",
        "gas_co": 0.4,
        "gas_hc": 1100,
        "gas_co2": 11.0,
        "gas_o2": 5.5,
        "gas_nox": 30,
        "lambda_chem": 1.15,
        "sample_validity": "VALID",
    }

