"""Tests for gaslab.contracts — enums, GasReading, GasLabPayload."""

from __future__ import annotations

import pytest

from gaslab.contracts import (
    AFR_STOICH,
    Hcv,
    CatalystStatus,
    ChemicalSignature,
    EngineStateBucket,
    GasBehavior,
    GasLabPayload,
    GasReading,
    LambdaBand,
    SampleValidity,
)


# ---------------------------------------------------------------------------
# ChemicalSignature — GAS_VOCABULARY §3
# ---------------------------------------------------------------------------


def test_chemical_signature_has_34_values() -> None:
    """The enum must have exactly 34 members — the contract surface."""
    assert len(ChemicalSignature) == 34  # vocab: GAS_VOCABULARY §3


def test_chemical_signature_is_34_value() -> None:
    """Assert 34 values, WRONG_VALVE_TIMING absent, and three new cam states present."""
    vals = {m.value for m in ChemicalSignature}
    assert len(ChemicalSignature) == 34  # vocab: GAS_VOCABULARY §3
    assert "WRONG_VALVE_TIMING" not in vals
    assert {
        "CAM_TIMING_RETARDED_MAP",
        "CAM_TIMING_RETARDED_MAF",
        "CAM_TIMING_ADVANCED",
    } <= vals  # vocab: GAS_VOCABULARY §3


def test_chemical_signature_is_strenum() -> None:
    """JSON-friendly serialisation required by SEMANTIC_CONTRACT.md."""
    assert ChemicalSignature.NORMAL_OPERATION == "NORMAL_OPERATION"
    assert ChemicalSignature.RICH_MIXTURE == "RICH_MIXTURE"
    assert ChemicalSignature.SAMPLE_INVALID == "SAMPLE_INVALID"


# ---------------------------------------------------------------------------
# LambdaBand — GAS_VOCABULARY §4
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "band,expected",
    [
        (LambdaBand.HEAVILY_RICH, "HEAVILY_RICH"),
        (LambdaBand.BORDERLINE_RICH, "BORDERLINE_RICH"),
        (LambdaBand.STOICHIOMETRIC, "STOICHIOMETRIC"),
        (LambdaBand.CATALYST_LIGHT_OFF, "CATALYST_LIGHT_OFF"),
        (LambdaBand.CATALYST_PEAK_EFFICIENCY, "CATALYST_PEAK_EFFICIENCY"),
        (LambdaBand.BORDERLINE_LEAN, "BORDERLINE_LEAN"),
        (LambdaBand.HEAVILY_LEAN, "HEAVILY_LEAN"),
    ],
)
def test_lambda_band_values(band: LambdaBand, expected: str) -> None:
    assert band == expected


# ---------------------------------------------------------------------------
# EngineStateBucket — GAS_VOCABULARY §7
# ---------------------------------------------------------------------------


def test_engine_state_bucket_invalid_state() -> None:
    """COLD_OPEN_LOOP_INVALID is the rejection sentinel."""
    assert EngineStateBucket.COLD_OPEN_LOOP_INVALID == "COLD_OPEN_LOOP_INVALID"


def test_engine_state_bucket_has_four_values() -> None:
    assert len(EngineStateBucket) == 4  # vocab: GAS_VOCABULARY §7


# ---------------------------------------------------------------------------
# GasReading — GAS_VOCABULARY §2.1
# ---------------------------------------------------------------------------


def test_gas_reading_all_fields_required() -> None:
    """Construction succeeds with all five fields."""
    r = GasReading(hc=100, co=0.5, co2=14.0, o2=1.0, nox=50)
    assert r.hc == 100
    assert r.co == 0.5
    assert r.co2 == 14.0
    assert r.o2 == 1.0
    assert r.nox == 50


def test_gas_reading_is_frozen() -> None:
    r = GasReading(hc=100, co=0.5, co2=14.0, o2=1.0, nox=50)
    with pytest.raises(Exception):
        r.hc = 200  # type: ignore[misc]


def test_gas_reading_rejects_missing_nox() -> None:
    """4-gas reading is rejected — NOₓ is required per GAS_VOCABULARY §2."""
    with pytest.raises(TypeError):
        GasReading(hc=100, co=0.5, co2=14.0, o2=1.0)  # type: ignore[arg-type]  # noqa: F821


@pytest.mark.parametrize(
    "field,value",
    [
        ("hc", -1),
        ("hc", 20_001),
        ("co", -0.1),
        ("co", 15.1),
        ("co2", -0.1),
        ("co2", 22.1),
        ("o2", -0.1),
        ("o2", 22.1),
        ("nox", -1),
        ("nox", 5_001),
    ],
)
def test_gas_reading_rejects_out_of_envelope(field: str, value: float | int) -> None:
    """Every gas field validates against analyser envelope — GAS_VOCABULARY §2."""
    kwargs = {"hc": 100, "co": 0.5, "co2": 14.0, "o2": 1.0, "nox": 50}
    kwargs[field] = value
    with pytest.raises(ValueError):
        GasReading(**kwargs)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# GasLabPayload — GAS_VOCABULARY §12.1
# ---------------------------------------------------------------------------


def test_gas_lab_payload_rejects_out_of_envelope() -> None:
    """Pydantic rejects values outside analyser measurement ranges."""
    with pytest.raises(Exception):
        GasLabPayload(
            chemical_state=ChemicalSignature.NORMAL_OPERATION,
            gas_co=25.0,  # above 15.0 max
            gas_hc=650,
            gas_co2=9.5,
            gas_o2=0.1,
            gas_nox=15,
            lambda_chem=1.0,
            sample_validity=SampleValidity.VALID,
        )


def test_gas_lab_payload_rejects_negative_hc() -> None:
    with pytest.raises(Exception):
        GasLabPayload(
            chemical_state=ChemicalSignature.NORMAL_OPERATION,
            gas_co=0.5,
            gas_hc=-1,  # negative
            gas_co2=9.5,
            gas_o2=0.1,
            gas_nox=15,
            lambda_chem=1.0,
            sample_validity=SampleValidity.VALID,
        )


def test_gas_lab_payload_valid_construction() -> None:
    """A well-formed payload passes validation."""
    p = GasLabPayload(
        chemical_state=ChemicalSignature.RICH_MIXTURE,
        gas_co=4.5,
        gas_hc=650,
        gas_co2=9.5,
        gas_o2=0.1,
        gas_nox=15,
        lambda_chem=0.82,
        sample_validity=SampleValidity.VALID,
    )
    assert p.chemical_state == ChemicalSignature.RICH_MIXTURE
    assert p.gas_co == 4.5
    assert p.lambda_chem == 0.82


# ---------------------------------------------------------------------------
# GasLabPayload.lambda_measured — T-FX-7 no-OBD perception source
# ---------------------------------------------------------------------------


def test_gas_lab_payload_lambda_measured_defaults_to_none() -> None:
    """lambda_measured is optional — omitting it yields None (OBD-present cars)."""
    p = GasLabPayload(
        chemical_state=ChemicalSignature.NORMAL_OPERATION,
        gas_co=0.1,
        gas_hc=50,
        gas_co2=14.5,
        gas_o2=0.3,
        gas_nox=10,
        lambda_chem=1.0,
        sample_validity=SampleValidity.VALID,
    )
    assert p.lambda_measured is None


def test_gas_lab_payload_lambda_measured_accepts_in_range() -> None:
    """lambda_measured within [0.5, 2.0] is accepted.  vocab: GAS_VOCABULARY §2/§6."""
    p = GasLabPayload(
        chemical_state=ChemicalSignature.NORMAL_OPERATION,
        gas_co=0.1,
        gas_hc=50,
        gas_co2=14.5,
        gas_o2=0.3,
        gas_nox=10,
        lambda_chem=1.0,
        sample_validity=SampleValidity.VALID,
        lambda_measured=1.12,
    )
    assert p.lambda_measured == 1.12


@pytest.mark.parametrize("bad_val", [0.49, 2.01])
def test_gas_lab_payload_lambda_measured_rejects_out_of_range(bad_val: float) -> None:
    """lambda_measured outside [0.5, 2.0] raises validation error.  vocab: GAS_VOCABULARY §2/§6."""
    with pytest.raises(Exception):
        GasLabPayload(
            chemical_state=ChemicalSignature.NORMAL_OPERATION,
            gas_co=0.1,
            gas_hc=50,
            gas_co2=14.5,
            gas_o2=0.3,
            gas_nox=10,
            lambda_chem=1.0,
            sample_validity=SampleValidity.VALID,
            lambda_measured=bad_val,
        )


# ---------------------------------------------------------------------------
# Constants — GAS_VOCABULARY §6
# ---------------------------------------------------------------------------


def test_hcv_constant() -> None:
    """Hcv = 1.85 per GAS_VOCABULARY §6."""
    assert Hcv == 1.85  # vocab: GAS_VOCABULARY §6


def test_afr_stoich_constant() -> None:
    """AFR_stoich = 14.71 per GAS_VOCABULARY §6."""
    assert AFR_STOICH == 14.71  # vocab: GAS_VOCABULARY §6


# ---------------------------------------------------------------------------
# Remaining enum existence checks
# ---------------------------------------------------------------------------


def test_sample_validity_has_four_values() -> None:
    assert len(SampleValidity) == 4  # vocab: GAS_VOCABULARY §5


def test_gas_behavior_has_six_values() -> None:
    assert len(GasBehavior) == 6  # vocab: GAS_VOCABULARY §8


def test_catalyst_status_has_four_values() -> None:
    assert len(CatalystStatus) == 4  # vocab: GAS_VOCABULARY §9
