"""Unit tests for dna_core.py (M0) — tech mask, era mask, engine-state FSM.

Covers: vref.db hit, vref.db miss, engine-state FSM transitions,
era bucket derivation, tech mask flag defaults.
"""

from __future__ import annotations

from pathlib import Path

from engine.v2.dna_core import (
    ERA_CAN,
    ERA_PRE_OBDII,
    DNAOutput,
    _compute_engine_state,
    _my_to_era,
    load_dna,
)
from engine.v2.input_model import (
    DiagnosticInput,
    FreezeFrameRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)

# ── helpers ─────────────────────────────────────────────────────────────────

_VREF_DB = Path(__file__).resolve().parents[3] / "engine" / "v2" / "vref.db"


def _sample_ctx(engine_code: str = "EA111_1.2_TSI", my: int = 2012) -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code=engine_code,
        displacement_cc=1197,
        my=my,
    )


def _validated(ctx: VehicleContext | None = None, obd: OBDRecord | None = None) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=ctx or _sample_ctx(),
            dtcs=[],
            analyser_type="5-gas",
            obd=obd,
        ),
        valid_channels={"obd", "dtcs"},
    )


# ── vref.db hit ─────────────────────────────────────────────────────────────


def test_load_dna_vref_hit() -> None:
    """Known engine code returns populated DNAOutput with correct era."""
    vi = _validated(ctx=_sample_ctx("EA111_1.2_TSI", my=2012))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert isinstance(dna, DNAOutput)
    assert dna.era_bucket == ERA_CAN
    assert dna.tech_mask["has_turbo"] is True
    assert dna.tech_mask["has_gdi"] is True
    assert dna.tech_mask["has_vvt"] is True
    assert dna.tech_mask["is_v_engine"] is False
    assert dna.vref_missing is False
    assert dna.confidence_ceiling == 1.00
    assert dna.target_rpm_u2 == 2500
    assert dna.target_lambda_v112 == 1.0


# ── vref.db miss ────────────────────────────────────────────────────────────


def test_load_dna_vref_miss() -> None:
    """Unknown engine code triggers fallback defaults and warning."""
    vi = _validated(ctx=_sample_ctx("NONEXISTENT_ENGINE", my=1998))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.vref_missing is True
    assert dna.confidence_ceiling == 0.60
    assert dna.era_bucket == "ERA_OBDII_EARLY"
    assert all(flag is False for flag in dna.tech_mask.values())
    assert dna.target_rpm_u2 == 2500
    assert dna.target_lambda_v112 == 1.000
    assert len(dna.warnings) == 1
    assert dna.warnings[0].category == 0
    assert "vref.db miss" in dna.warnings[0].message


# ── engine-state FSM ────────────────────────────────────────────────────────


def test_engine_state_cold_open_loop() -> None:
    """ECT < 75 yields cold_open_loop regardless of RPM/fuel_status."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=30.0, rpm=800, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "cold_open_loop"


def test_engine_state_warm_cranking() -> None:
    """ECT >= 75 with RPM=0 yields warm_cranking."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=85.0, rpm=0),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_cranking"


def test_engine_state_warm_closed_loop() -> None:
    """ECT >= 75, RPM > 0, CL fuel_status yields warm_closed_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=90.0, rpm=2500, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


def test_engine_state_warm_open_loop() -> None:
    """ECT >= 75, RPM > 0, OL_FAULT yields warm_open_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=95.0, rpm=3000, fuel_status="OL_FAULT"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_open_loop"


def test_engine_state_warm_open_loop_ol_drive() -> None:
    """OL_DRIVE also maps to warm_open_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=88.0, rpm=1500, fuel_status="OL_DRIVE"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_open_loop"


def test_engine_state_warm_dfco() -> None:
    """Fuel status OL (decel fuel cut) yields warm_dfco."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=80.0, rpm=2500, fuel_status="OL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_dfco"


def test_engine_state_ff_ect_fallback() -> None:
    """ECT from freeze frame when OBD ECT is missing."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(rpm=800, fuel_status="CL"),
        freeze_frame=FreezeFrameRecord(ect_c=30.0, rpm=800),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "cold_open_loop"


# ── era bucket derivation ───────────────────────────────────────────────────


def test_my_to_era_pre_obdii() -> None:
    """MY 1990–1995 maps to ERA_PRE_OBDII."""
    assert _my_to_era(1990) == ERA_PRE_OBDII
    assert _my_to_era(1993) == ERA_PRE_OBDII
    assert _my_to_era(1995) == ERA_PRE_OBDII


def test_my_to_era_obdii_early() -> None:
    """MY 1996–2005 maps to ERA_OBDII_EARLY."""
    assert _my_to_era(1996) == "ERA_OBDII_EARLY"
    assert _my_to_era(2000) == "ERA_OBDII_EARLY"
    assert _my_to_era(2005) == "ERA_OBDII_EARLY"


def test_my_to_era_can() -> None:
    """MY 2006–2015 maps to ERA_CAN."""
    assert _my_to_era(2006) == ERA_CAN
    assert _my_to_era(2010) == ERA_CAN
    assert _my_to_era(2015) == ERA_CAN


def test_my_to_era_modern() -> None:
    """MY 2016–2020 maps to ERA_MODERN."""
    assert _my_to_era(2016) == "ERA_MODERN"
    assert _my_to_era(2020) == "ERA_MODERN"
