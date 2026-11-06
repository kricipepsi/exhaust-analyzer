from __future__ import annotations

import copy

from comlab.schemas.response import OrchestratorFinalUIOutput
from obdlab.schemas.dna_view import InductionType as ObdInductionType
from obdlab.schemas.dna_view import O2SensorType

from wired import composition
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
    assert payload.high_idle_lambda is not None


_WIDEBAND_RAW = {
    "vin": "WVWZZZ1KZAP012480",
    "triage": {
        "tier_1": "rough_idle_shudder",
        "tier_2": "constant_vibration_shudder",
        "occurs_during": "always",
        "engine_state": "running",
        "load_state": "idle",
    },
    "gas": {
        "hc": 220,
        "nox": 40,
        "hc_high": 400,
        "nox_high": 150,
        "co": 1.5,
        "co2": 13.0,
        "o2": 0.6,
        "co_high": 0.5,
        "co2_high": 11.5,
        "o2_high": 3.0,
        "lambda_measured": 0.92,
        "lambda_2500": 1.15,
        "engine_state": "STABILIZED_IDLE",
    },
    "obd": {
        "engine_rpm": 800,
        "coolant_temp_c": 88.0,
        "mass_airflow_gps": 20.0,
        "shrtft1": -12.0,
        "longft1": -8.0,
        "number_of_banks": 1,
        "fuel_sys_status": "CL",
        "stft_idle_pct": 3.7,
        "ltft_idle_pct": 17.3,
        "stft_2500_pct": 1.9,
        "ltft_2500_pct": 1.9,
        "pid_wideband_equivalence_ratio": 0.95,
    },
}


def _spy_views(monkeypatch) -> dict:
    """Record the last GASLab and OBDLab DNA views ``diagnose`` builds."""
    seen: dict = {}
    real_gas = composition._build_gas_dna_view
    real_obd = composition._build_obd_dna_view

    def gas_view(*args, **kwargs):
        seen["gas"] = real_gas(*args, **kwargs)
        return seen["gas"]

    def obd_view(*args, **kwargs):
        seen["obd"] = real_obd(*args, **kwargs)
        return seen["obd"]

    monkeypatch.setattr(composition, "_build_gas_dna_view", gas_view)
    monkeypatch.setattr(composition, "_build_obd_dna_view", obd_view)
    return seen


def test_upstream_o2_override_reaches_obdlab_and_gaslab(monkeypatch) -> None:
    """A narrowband override on a wideband-decoded case reaches both labs and runs to a verdict."""
    seen = _spy_views(monkeypatch)
    raw = copy.deepcopy(_WIDEBAND_RAW)
    raw["obd"].pop("pid_wideband_equivalence_ratio")
    raw["obd"]["pid_oxygen_sensor_volts"] = 0.45
    raw["overrides"] = {"upstream_o2_type": "NARROWBAND"}

    result = diagnose(raw)

    assert result.diagnostic_verdict.fault_code != "OBD_INPUT_INCOMPLETE"
    assert seen["obd"].upstream_o2_type == O2SensorType.NARROWBAND_0_TO_1V
    assert seen["gas"].upstream_o2_type == "NARROWBAND"


def test_upstream_o2_override_requires_its_own_reading() -> None:
    """The override decides which O2 reading is required: the wideband ratio alone is incomplete."""
    raw = copy.deepcopy(_WIDEBAND_RAW)
    raw["overrides"] = {"upstream_o2_type": "NARROWBAND"}

    result = diagnose(raw)

    assert result.diagnostic_verdict.fault_code == "OBD_INPUT_INCOMPLETE"


def test_de_cat_override_reaches_gaslab(monkeypatch) -> None:
    """The de-cat override clears ``has_catalyst`` in GASLab's DNA view."""
    seen = _spy_views(monkeypatch)
    raw = _minimal_raw_inputs()
    raw["overrides"] = {"de_cat": True}

    diagnose(raw)

    assert seen["gas"].has_catalyst is False


def test_supercharged_projects_as_turbocharged() -> None:
    """OBDLab's InductionType has no SUPERCHARGED; forced induction projects as TURBOCHARGED."""
    vin_dna = _minimal_vin_dna()
    vin_dna["induction_type"] = "SUPERCHARGED"

    view = composition._build_obd_dna_view(vin_dna)

    assert view.induction_type == ObdInductionType.TURBOCHARGED


def test_turbocharged_projects_unchanged() -> None:
    vin_dna = _minimal_vin_dna()
    vin_dna["induction_type"] = "TURBOCHARGED"

    view = composition._build_obd_dna_view(vin_dna)

    assert view.induction_type == ObdInductionType.TURBOCHARGED
