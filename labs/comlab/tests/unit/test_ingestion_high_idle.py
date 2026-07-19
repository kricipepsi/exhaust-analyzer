"""Unit tests for high-idle GasLabPayload optional fields validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from comlab.schemas.ingestion import GasLabPayload, SampleValidity


def test_gaslab_payload_accepts_high_idle() -> None:
    """GasLabPayload accepts all high-idle optional fields and populates them correctly."""
    data = {
        "chemical_state": "WORN_PISTON_RINGS",
        "gas_co": 0.2,
        "gas_hc": 120,
        "gas_co2": 14.5,
        "gas_o2": 0.3,
        "gas_nox": 50,
        "lambda_chem": 1.0,
        "sample_validity": SampleValidity.VALID,
        "high_idle_hc": 380,
        "high_idle_co": 0.15,
        "high_idle_co2": 15.0,
        "high_idle_o2": 0.2,
        "high_idle_nox": 40,
        "high_idle_lambda": 1.002,
    }
    payload = GasLabPayload(**data)
    assert payload.high_idle_hc == 380
    assert payload.high_idle_co == 0.15
    assert payload.high_idle_co2 == 15.0
    assert payload.high_idle_o2 == 0.2
    assert payload.high_idle_nox == 40
    assert payload.high_idle_lambda == 1.002


def test_gaslab_payload_backward_compatibility() -> None:
    """GasLabPayload remains backward-compatible by defaulting high-idle fields to None."""
    data = {
        "chemical_state": "WORN_PISTON_RINGS",
        "gas_co": 0.2,
        "gas_hc": 120,
        "gas_co2": 14.5,
        "gas_o2": 0.3,
        "gas_nox": 50,
        "lambda_chem": 1.0,
        "sample_validity": SampleValidity.VALID,
    }
    payload = GasLabPayload(**data)
    assert payload.high_idle_hc is None
    assert payload.high_idle_co is None
    assert payload.high_idle_co2 is None
    assert payload.high_idle_o2 is None
    assert payload.high_idle_nox is None
    assert payload.high_idle_lambda is None


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("high_idle_hc", -1),
        ("high_idle_hc", 20001),
        ("high_idle_co", -0.1),
        ("high_idle_co", 15.1),
        ("high_idle_co2", -0.1),
        ("high_idle_co2", 22.1),
        ("high_idle_o2", -0.1),
        ("high_idle_o2", 22.1),
        ("high_idle_nox", -1),
        ("high_idle_nox", 5001),
        ("high_idle_lambda", 0.49),
        ("high_idle_lambda", 2.51),
    ],
)
def test_gaslab_payload_rejects_out_of_bounds_high_idle(field: str, bad_value: float | int) -> None:
    """GasLabPayload validates high-idle bounds and rejects invalid inputs."""
    data = {
        "chemical_state": "WORN_PISTON_RINGS",
        "gas_co": 0.2,
        "gas_hc": 120,
        "gas_co2": 14.5,
        "gas_o2": 0.3,
        "gas_nox": 50,
        "lambda_chem": 1.0,
        "sample_validity": SampleValidity.VALID,
    }
    data[field] = bad_value
    with pytest.raises(ValidationError):
        GasLabPayload(**data)
