"""Unit tests for dna_core.py (M0) — tech mask, era mask, engine-state FSM.

Covers: vref.db hit, vref.db miss, engine-state FSM transitions,
era bucket derivation, tech mask flag defaults, signal extraction helpers.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from engine.v2.dna_core import (
    ERA_CAN,
    ERA_MODERN,
    ERA_OBDII_EARLY,
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
    extract_ect,
    extract_fuel_status,
    extract_rpm,
)
from engine.v2.vin.prior_context import EngineDNA

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


def _validated(
    ctx: VehicleContext | None = None,
    obd: OBDRecord | None = None,
    ff: FreezeFrameRecord | None = None,
) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=ctx or _sample_ctx(),
            dtcs=[],
            analyser_type="5-gas",
            obd=obd,
            freeze_frame=ff,
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


def test_load_dna_vref_pre_obdii_engine() -> None:
    """PRE_OBDII engine has no VVT/GDI/turbo and NB O2 sensor."""
    vi = _validated(ctx=_sample_ctx("M44B19", my=1994))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.era_bucket == ERA_PRE_OBDII
    assert dna.tech_mask["has_vvt"] is False
    assert dna.tech_mask["has_gdi"] is False
    assert dna.tech_mask["has_turbo"] is False
    assert dna.o2_type == "NB"
    assert dna.vref_missing is False
    assert dna.confidence_ceiling == 1.00


def test_load_dna_vref_modern_engine() -> None:
    """MODERN era engine has all tech flags and WB O2 sensor."""
    vi = _validated(ctx=_sample_ctx("AJ20_Petrol_2.0T", my=2018))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.era_bucket == ERA_MODERN
    assert dna.tech_mask["has_vvt"] is True
    assert dna.tech_mask["has_gdi"] is True
    assert dna.tech_mask["has_turbo"] is True
    assert dna.o2_type == "WB"
    assert dna.vref_missing is False


def test_load_dna_vref_no_vvt_engine() -> None:
    """Engine without VVT has has_vvt=False in tech_mask (prerequisite for M4 veto)."""
    vi = _validated(ctx=_sample_ctx("T-Jet_1.4", my=2008))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.tech_mask["has_vvt"] is False
    assert dna.tech_mask["has_turbo"] is True
    assert dna.vref_missing is False


def test_load_dna_vref_obdii_early_nb_o2() -> None:
    """OBDII_EARLY era with narrowband O2 sensor."""
    vi = _validated(ctx=_sample_ctx("EA111_1.4_16V", my=2002))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.era_bucket == ERA_OBDII_EARLY
    assert dna.o2_type == "NB"
    assert dna.tech_mask["has_turbo"] is False
    assert dna.tech_mask["has_vvt"] is False
    assert dna.vref_missing is False


# ── vref.db miss ────────────────────────────────────────────────────────────


def test_load_dna_vref_miss() -> None:
    """Unknown engine code triggers fallback defaults and warning."""
    vi = _validated(ctx=_sample_ctx("NONEXISTENT_ENGINE", my=1998))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.vref_missing is True
    assert dna.confidence_ceiling == 0.60
    assert dna.era_bucket == ERA_OBDII_EARLY
    assert all(flag is False for flag in dna.tech_mask.values())
    assert dna.target_rpm_u2 == 2500
    assert dna.target_lambda_v112 == 1.000
    assert len(dna.warnings) == 1
    assert dna.warnings[0].category == 0
    assert "vref.db miss" in dna.warnings[0].message


def test_load_dna_vref_miss_pre_obdii_era() -> None:
    """vref.db miss on MY=1992 derives ERA_PRE_OBDII from MY alone."""
    vi = _validated(ctx=_sample_ctx("UNKNOWN_OLD", my=1992))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.vref_missing is True
    assert dna.era_bucket == ERA_PRE_OBDII
    assert dna.confidence_ceiling == 0.60


def test_load_dna_vref_miss_modern_era() -> None:
    """vref.db miss on MY=2019 derives ERA_MODERN from MY alone."""
    vi = _validated(ctx=_sample_ctx("UNKNOWN_NEW", my=2019))
    dna = load_dna(vi, db_path=_VREF_DB)

    assert dna.vref_missing is True
    assert dna.era_bucket == ERA_MODERN
    assert dna.confidence_ceiling == 0.60


# ── VIN fallback bridge (T-FX-3) ─────────────────────────────────────────────


def _vin_dna_high(
    induction: str | None = None,
    injection: str | None = None,
    o2_arch: str | None = None,
    cylinders: int | None = None,
    engine_code: str | None = "TEST_ENGINE",
) -> EngineDNA:
    """Build a high-confidence EngineDNA with specific tech fields."""
    return EngineDNA(
        source="vininfo+dna",
        confidence="high",
        make="TEST",
        engine_code=engine_code,
        induction=induction,  # type: ignore[arg-type]
        injection=injection,  # type: ignore[arg-type]
        o2_arch=o2_arch,  # type: ignore[arg-type]
        cylinders=cylinders,
    )


def _vin_dna_partial() -> EngineDNA:
    """Build a partial-confidence EngineDNA (should NOT trigger bridge)."""
    return EngineDNA(
        source="wmi_only",
        confidence="partial",
        make="TEST",
    )


def _ctx_with_vin(
    engine_code: str = "NONEXISTENT",
    my: int = 2015,
) -> VehicleContext:
    """VehicleContext with a VIN that passes format validation."""
    return VehicleContext(
        brand="TEST",
        model="X",
        engine_code=engine_code,
        displacement_cc=2000,
        my=my,
        vin="WBA12345678900001",
    )


def test_vref_miss_vin_high_turbo() -> None:
    """vref miss + VIN high + induction=turbo → has_turbo=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(induction="turbo")):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.vref_missing is True
    assert dna.tech_mask["has_turbo"] is True
    assert dna.tech_mask["has_gdi"] is False
    assert dna.tech_mask["is_v_engine"] is False
    assert dna.o2_type == "NB"


def test_vref_miss_vin_high_super() -> None:
    """vref miss + VIN high + induction=super → has_turbo=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(induction="super")):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_turbo"] is True


def test_vref_miss_vin_high_gdi() -> None:
    """vref miss + VIN high + injection=gdi → has_gdi=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(injection="gdi")):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_gdi"] is True
    assert dna.tech_mask["has_turbo"] is False


def test_vref_miss_vin_high_tsi() -> None:
    """vref miss + VIN high + injection=tsi → has_gdi=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(injection="tsi")):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_gdi"] is True


def test_vref_miss_vin_high_wideband() -> None:
    """vref miss + VIN high + o2_arch=wideband → o2_type='WB'."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(o2_arch="wideband")):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.o2_type == "WB"


def test_vref_miss_vin_high_v6() -> None:
    """vref miss + VIN high + cylinders=6 → is_v_engine=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(cylinders=6)):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["is_v_engine"] is True


def test_vref_miss_vin_high_v8() -> None:
    """vref miss + VIN high + cylinders=8 → is_v_engine=True."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(cylinders=8)):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["is_v_engine"] is True


def test_vref_miss_vin_high_inline4() -> None:
    """vref miss + VIN high + cylinders=4 → is_v_engine=False (inline-4)."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(cylinders=4)):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["is_v_engine"] is False


def test_vref_miss_vin_high_combined() -> None:
    """vref miss + VIN high with all fields → all bridge flags set."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_high(
             induction="turbo", injection="gdi", o2_arch="wideband", cylinders=8,
         )):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_turbo"] is True
    assert dna.tech_mask["has_gdi"] is True
    assert dna.tech_mask["is_v_engine"] is True
    assert dna.o2_type == "WB"


def test_vref_miss_vin_partial_no_bridge() -> None:
    """vref miss + VIN partial confidence → bridge does NOT fire."""
    vi = _validated(ctx=_ctx_with_vin())
    with patch("engine.v2.dna_core._query_vref", return_value=None), \
         patch("engine.v2.vin.resolve", return_value=_vin_dna_partial()):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_turbo"] is False
    assert dna.tech_mask["has_gdi"] is False
    assert dna.tech_mask["is_v_engine"] is False
    assert dna.o2_type == "NB"


def test_vref_miss_vin_none_no_bridge() -> None:
    """vref miss + VIN None (no VIN at all) → bridge does NOT fire."""
    vi = _validated(ctx=_sample_ctx("NONEXISTENT", my=2015))
    with patch("engine.v2.dna_core._query_vref", return_value=None):
        dna = load_dna(vi, db_path=Path("nonexistent.db"))

    assert dna.tech_mask["has_turbo"] is False
    assert dna.tech_mask["has_gdi"] is False
    assert dna.tech_mask["is_v_engine"] is False
    assert dna.o2_type == "NB"


def test_vref_hit_vin_high_not_overridden() -> None:
    """vref hit + VIN high → tech_mask from vref.db, NOT overridden by VIN."""
    vi = _validated(ctx=VehicleContext(
        brand="TEST", model="X",
        engine_code="EA111_1.2_TSI",
        displacement_cc=1197, my=2012,
        vin="WBA12345678900001",
    ))
    # VIN says NA + MPFI → would override if bridge fired on hit path
    with patch("engine.v2.vin.resolve", return_value=_vin_dna_high(
            induction="na", injection="mpfi", o2_arch="narrowband", cylinders=4,
            engine_code=None,  # don't override engine_code for vref lookup
        )):
        dna = load_dna(vi, db_path=_VREF_DB)

    # vref.db hit — bridge must NOT fire; values come from vref.db
    assert dna.vref_missing is False
    assert dna.tech_mask["has_turbo"] is True   # vref.db says turbo
    assert dna.tech_mask["has_gdi"] is True      # vref.db says GDI
    assert dna.confidence_ceiling == 1.00        # vref.db hit ceiling


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


def test_engine_state_cold_open_loop_rpm_zero() -> None:
    """Cold engine with RPM=0 still yields cold_open_loop (cold takes priority)."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=10.0, rpm=0, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "cold_open_loop"


def test_engine_state_cold_open_loop_ol_fault() -> None:
    """Cold engine with OL_FAULT still yields cold_open_loop (cold takes priority)."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=40.0, rpm=2500, fuel_status="OL_FAULT"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "cold_open_loop"


def test_engine_state_cold_boundary_74_9() -> None:
    """ECT=74.9 still triggers cold_open_loop (threshold is strictly < 75)."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=74.9, rpm=1200, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "cold_open_loop"


def test_engine_state_warm_boundary_75_0() -> None:
    """ECT=75.0 is NOT cold — goes to warm_closed_loop with RPM>0, CL."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=75.0, rpm=800, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


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


def test_engine_state_warm_closed_loop_cl_fault() -> None:
    """CL_FAULT also maps to warm_closed_loop (FSM table row)."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=95.0, rpm=2000, fuel_status="CL_FAULT"),
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


def test_engine_state_no_ect_defaults_closed() -> None:
    """No ECT data, RPM > 0, CL → defaults to warm_closed_loop (not cold)."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(rpm=800, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


def test_engine_state_no_rpm_defaults_closed() -> None:
    """ECT >= 75, no RPM data, CL → defaults to warm_closed_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=90.0, fuel_status="CL"),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


def test_engine_state_fuel_status_none_defaults_closed() -> None:
    """ECT >= 75, RPM > 0, no fuel_status → defaults to warm_closed_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=90.0, rpm=1500),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


def test_engine_state_no_data_at_all() -> None:
    """No OBD, no FF → all signals None → defaults to warm_closed_loop."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
    )
    vi = ValidatedInput(raw=diag, valid_channels={"dtcs"})
    assert _compute_engine_state(vi) == "warm_closed_loop"


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


def test_engine_state_ff_rpm_fallback() -> None:
    """RPM from freeze frame when OBD RPM is missing."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=90.0, fuel_status="CL"),
        freeze_frame=FreezeFrameRecord(rpm=0, ect_c=95.0),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_cranking"


def test_engine_state_ff_fuel_status_fallback() -> None:
    """fuel_status from freeze frame when OBD fuel_status is missing."""
    ctx = _sample_ctx()
    diag = DiagnosticInput(
        vehicle_context=ctx,
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(ect_c=95.0, rpm=2500),
        freeze_frame=FreezeFrameRecord(fuel_status="OL_FAULT", ect_c=95.0),
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"})
    assert _compute_engine_state(vi) == "warm_open_loop"


# ── era bucket derivation ───────────────────────────────────────────────────


def test_my_to_era_pre_obdii() -> None:
    """MY 1990–1995 maps to ERA_PRE_OBDII."""
    assert _my_to_era(1990) == ERA_PRE_OBDII
    assert _my_to_era(1993) == ERA_PRE_OBDII
    assert _my_to_era(1995) == ERA_PRE_OBDII


def test_my_to_era_obdii_early() -> None:
    """MY 1996–2005 maps to ERA_OBDII_EARLY."""
    assert _my_to_era(1996) == ERA_OBDII_EARLY
    assert _my_to_era(2000) == ERA_OBDII_EARLY
    assert _my_to_era(2005) == ERA_OBDII_EARLY


def test_my_to_era_can() -> None:
    """MY 2006–2015 maps to ERA_CAN."""
    assert _my_to_era(2006) == ERA_CAN
    assert _my_to_era(2010) == ERA_CAN
    assert _my_to_era(2015) == ERA_CAN


def test_my_to_era_modern() -> None:
    """MY 2016–2020 maps to ERA_MODERN."""
    assert _my_to_era(2016) == ERA_MODERN
    assert _my_to_era(2020) == ERA_MODERN


def test_my_to_era_unknown_falls_back_to_modern() -> None:
    """MY > 2020 falls back to ERA_MODERN (VL will handle out-of-range)."""
    assert _my_to_era(2021) == ERA_MODERN


# ── signal extraction helpers ───────────────────────────────────────────────


def _vi_from_records(
    obd: OBDRecord | None = None,
    ff: FreezeFrameRecord | None = None,
) -> ValidatedInput:
    """Build ValidatedInput with only obd and freeze_frame set (no gas)."""
    ctx = _sample_ctx()
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=ctx,
            dtcs=[],
            analyser_type="5-gas",
            obd=obd,
            freeze_frame=ff,
        ),
        valid_channels={"obd", "dtcs"},
    )


def test_extract_ect_obd_priority() -> None:
    """ECT from OBD takes priority over freeze frame."""
    vi = _vi_from_records(
        obd=OBDRecord(ect_c=90.0),
        ff=FreezeFrameRecord(ect_c=30.0),
    )
    assert extract_ect(vi.raw.obd, vi.raw.freeze_frame) == 90.0


def test_extract_ect_ff_fallback() -> None:
    """ECT falls back to freeze frame when OBD ECT is None."""
    vi = _vi_from_records(
        obd=OBDRecord(rpm=800),
        ff=FreezeFrameRecord(ect_c=55.0),
    )
    assert extract_ect(vi.raw.obd, vi.raw.freeze_frame) == 55.0


def test_extract_ect_none() -> None:
    """ECT returns None when both OBD and FF have no ECT."""
    vi = _vi_from_records(
        obd=OBDRecord(rpm=800),
    )
    assert extract_ect(vi.raw.obd, vi.raw.freeze_frame) is None


def test_extract_ect_none_no_obd() -> None:
    """ECT returns None when there is no OBD and no FF."""
    vi = _vi_from_records()
    assert extract_ect(vi.raw.obd, vi.raw.freeze_frame) is None


def test_extract_rpm_obd_priority() -> None:
    """RPM from OBD takes priority over freeze frame."""
    vi = _vi_from_records(
        obd=OBDRecord(rpm=3000),
        ff=FreezeFrameRecord(rpm=800),
    )
    assert extract_rpm(vi.raw.obd, vi.raw.freeze_frame) == 3000


def test_extract_rpm_ff_fallback() -> None:
    """RPM falls back to freeze frame when OBD RPM is None."""
    vi = _vi_from_records(
        obd=OBDRecord(ect_c=90.0),
        ff=FreezeFrameRecord(rpm=2500),
    )
    assert extract_rpm(vi.raw.obd, vi.raw.freeze_frame) == 2500


def test_extract_rpm_none() -> None:
    """RPM returns None when both OBD and FF have no RPM."""
    vi = _vi_from_records(
        obd=OBDRecord(ect_c=90.0),
    )
    assert extract_rpm(vi.raw.obd, vi.raw.freeze_frame) is None


def test_extract_fuel_status_obd_priority() -> None:
    """fuel_status from OBD takes priority over freeze frame."""
    vi = _vi_from_records(
        obd=OBDRecord(fuel_status="OL_FAULT"),
        ff=FreezeFrameRecord(fuel_status="CL"),
    )
    assert extract_fuel_status(vi.raw.obd, vi.raw.freeze_frame) == "OL_FAULT"


def test_extract_fuel_status_ff_fallback() -> None:
    """fuel_status falls back to freeze frame when OBD fuel_status is None."""
    vi = _vi_from_records(
        obd=OBDRecord(ect_c=90.0, rpm=800),
        ff=FreezeFrameRecord(fuel_status="OL_DRIVE"),
    )
    assert extract_fuel_status(vi.raw.obd, vi.raw.freeze_frame) == "OL_DRIVE"


def test_extract_fuel_status_none() -> None:
    """fuel_status returns None when both OBD and FF have no fuel_status."""
    vi = _vi_from_records(
        obd=OBDRecord(ect_c=90.0, rpm=800),
    )
    assert extract_fuel_status(vi.raw.obd, vi.raw.freeze_frame) is None


# ── DNAOutput dataclass ─────────────────────────────────────────────────────


def test_dna_output_default_warnings() -> None:
    """DNAOutput warnings default to empty list."""
    dna = DNAOutput(
        engine_state="warm_closed_loop",
        era_bucket=ERA_CAN,
        tech_mask={"has_vvt": True, "has_gdi": False},
        o2_type="WB",
        target_rpm_u2=2500,
        target_lambda_v112=1.000,
        vref_missing=False,
        confidence_ceiling=1.00,
    )
    assert dna.warnings == []


def test_dna_output_slots() -> None:
    """DNAOutput uses __slots__ — no __dict__."""
    dna = DNAOutput(
        engine_state="warm_closed_loop",
        era_bucket=ERA_CAN,
        tech_mask={},
        o2_type="NB",
        target_rpm_u2=2500,
        target_lambda_v112=1.000,
        vref_missing=False,
        confidence_ceiling=1.00,
    )
    with pytest.raises(AttributeError):
        _ = dna.__dict__  # type: ignore[attr-defined]  # noqa: B018


# ── parametrized FSM table conformance ──────────────────────────────────────

_FSM_TABLE: list[tuple[float | None, int | None, str | None, str]] = [
    # (ect_c, rpm, fuel_status, expected_engine_state)
    # v2-era-masking §4 engine-state FSM — every row has a test
    (30.0, 800, "CL", "cold_open_loop"),
    (30.0, 0, "CL", "cold_open_loop"),
    (30.0, 800, "OL_FAULT", "cold_open_loop"),
    (30.0, None, None, "cold_open_loop"),
    (85.0, 0, None, "warm_cranking"),
    (85.0, 0, "CL", "warm_cranking"),
    (85.0, 0, "OL_FAULT", "warm_cranking"),
    (85.0, 800, "CL", "warm_closed_loop"),
    (85.0, 800, "CL_FAULT", "warm_closed_loop"),
    (85.0, 3000, "OL_FAULT", "warm_open_loop"),
    (85.0, 3000, "OL_DRIVE", "warm_open_loop"),
    (85.0, 2500, "OL", "warm_dfco"),
    # Missing-data defaults
    (None, 800, "CL", "warm_closed_loop"),
    (85.0, None, "CL", "warm_closed_loop"),
    (85.0, 800, None, "warm_closed_loop"),
    (None, None, None, "warm_closed_loop"),
]


@pytest.mark.parametrize("ect_c, rpm, fuel_status, expected", _FSM_TABLE)
def test_fsm_table_conformance(
    ect_c: float | None,
    rpm: int | None,
    fuel_status: str | None,
    expected: str,
) -> None:
    """Every row in v2-era-masking §4 FSM table maps to the correct state."""
    obd_kwargs: dict[str, object] = {}
    if ect_c is not None:
        obd_kwargs["ect_c"] = ect_c
    if rpm is not None:
        obd_kwargs["rpm"] = rpm
    if fuel_status is not None:
        obd_kwargs["fuel_status"] = fuel_status

    diag = DiagnosticInput(
        vehicle_context=_sample_ctx(),
        dtcs=[],
        analyser_type="5-gas",
        obd=OBDRecord(**obd_kwargs) if obd_kwargs else None,  # type: ignore[arg-type]
    )
    vi = ValidatedInput(raw=diag, valid_channels={"obd"} if obd_kwargs else {"dtcs"})
    assert _compute_engine_state(vi) == expected
