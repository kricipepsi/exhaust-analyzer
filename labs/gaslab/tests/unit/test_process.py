"""Tests for ``gaslab/process.py`` — public entry point."""

from __future__ import annotations

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasLabPayload, GasReading, SampleValidity
from gaslab.dna_view import GasLabDnaView
from gaslab.process import GasLabContext, process


def _dna(**overrides: object) -> GasLabDnaView:
    defaults: dict[str, object] = dict(
        engine_displacement_liters=2.0,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="Euro 4",
        fuel_delivery_type="PORT",
        induction_type="NA",
        upstream_o2_type="WIDEBAND",
        has_catalyst=True,
        egr_equipped=False,
        confidence="HIGH",
    )
    defaults.update(overrides)
    return GasLabDnaView(**defaults)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# test_payload_round_trip
# ---------------------------------------------------------------------------


def test_payload_round_trip() -> None:
    """GasLabPayload survives model_dump_json → model_validate_json round-trip."""
    original = GasLabPayload(
        chemical_state=ChemicalSignature.NORMAL_OPERATION,
        gas_co=0.2,
        gas_hc=15,
        gas_co2=15.0,
        gas_o2=0.2,
        gas_nox=50,
        lambda_chem=1.004,
        sample_validity=SampleValidity.VALID,
    )
    restored = GasLabPayload.model_validate_json(original.model_dump_json())
    assert restored == original


# ---------------------------------------------------------------------------
# test_process_happy_path
# ---------------------------------------------------------------------------


def test_process_happy_path() -> None:
    """End-to-end: process() with a normal reading returns NORMAL_OPERATION."""
    reading = GasReading(hc=15, co=0.2, co2=15.0, o2=0.2, nox=50)
    dna = _dna()
    context = GasLabContext(
        dna=dna,
        engine_state=EngineStateBucket.STABILIZED_IDLE,
    )
    result = process(reading, context)
    assert result.chemical_state == ChemicalSignature.NORMAL_OPERATION
    assert result.sample_validity == SampleValidity.VALID
    assert result.gas_co == 0.2
    assert result.gas_hc == 15
    assert result.gas_co2 == 15.0
    assert result.gas_o2 == 0.2
    assert result.gas_nox == 50
    assert 0.5 <= result.lambda_chem <= 2.5


def test_emits_high_idle_block() -> None:
    """process() with high-idle reading populates high-idle fields in the output payload."""
    reading = GasReading(hc=15, co=0.2, co2=15.0, o2=0.2, nox=50)
    reading_high = GasReading(hc=30, co=0.1, co2=14.8, o2=0.4, nox=120)
    dna = _dna()
    context = GasLabContext(
        dna=dna,
        engine_state=EngineStateBucket.STABILIZED_IDLE,
        reading_high=reading_high,
    )
    result = process(reading, context)
    assert result.high_idle_hc == 30
    assert result.high_idle_co == 0.1
    assert result.high_idle_co2 == 14.8
    assert result.high_idle_o2 == 0.4
    assert result.high_idle_nox == 120
    assert result.high_idle_lambda is not None
    assert 0.5 <= result.high_idle_lambda <= 2.5
