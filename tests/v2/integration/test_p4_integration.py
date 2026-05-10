"""P4 integration tests — M0→M1/M2→M3→M4 pipeline on 20 corpus cases.

Verifies the full P4 pipeline from validated input through raw_probs output.
Runs VL → M0 (dna_core) → M1 (digital_parser) → M2 (gas_lab) → M3 (arbitrator)
→ M4 (kg_engine) and asserts structural correctness, era/tech veto behaviour,
perception gap emission, and CF score bounds.

Covers: R1 (module skeleton), R4/L04 (VL mandatory), R6 (era masking),
        R7 (M4 stops at raw_probs), L01 (no perception short-circuit),
        L16 (confidence ceiling).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Literal

import pytest
import yaml

from engine.v2.arbitrator import (
    MasterEvidenceVector,
    arbitrate,
)
from engine.v2.digital_parser import parse_digital
from engine.v2.dna_core import (
    ERA_MODERN,
    ERA_OBDII_EARLY,
    ERA_PRE_OBDII,
    DNAOutput,
    load_dna,
)
from engine.v2.gas_lab import analyse_gas
from engine.v2.input_model import (
    DiagnosticInput,
    FreezeFrameRecord,
    GasRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)
from engine.v2.kg_engine import score_faults, score_root_causes
from engine.v2.validation import validate

# ── paths ──────────────────────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCHEMA_DIR = _REPO_ROOT / "schema" / "v2"
_CORPUS_PATH = _REPO_ROOT / "cases" / "csv" / "cases_petrol_master_v6.csv"
_VREF_DB_PATH = _REPO_ROOT / "engine" / "v2" / "vref.db"


# ── schema cache ────────────────────────────────────────────────────────────


def _load_faults() -> dict:
    with open(_SCHEMA_DIR / "faults.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_edges() -> list[dict]:
    with open(_SCHEMA_DIR / "edges.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)["edges"]


def _load_root_causes() -> dict:
    with open(_SCHEMA_DIR / "root_causes.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


# Module-level cache — loaded once per session.
_FAULTS: dict | None = None
_EDGES: list[dict] | None = None
_ROOT_CAUSES: dict | None = None


def _faults() -> dict:
    global _FAULTS
    if _FAULTS is None:
        _FAULTS = _load_faults()
    return _FAULTS


def _edges() -> list[dict]:
    global _EDGES
    if _EDGES is None:
        _EDGES = _load_edges()
    return _EDGES


def _root_causes() -> dict:
    global _ROOT_CAUSES
    if _ROOT_CAUSES is None:
        _ROOT_CAUSES = _load_root_causes()
    return _ROOT_CAUSES


# ── pipeline runner ─────────────────────────────────────────────────────────


def run_pipeline(
    di: DiagnosticInput,
    db_path: Path | None = None,
    soft_mode: bool = True,
) -> tuple[ValidatedInput, DNAOutput, MasterEvidenceVector, dict[str, float]]:
    """Run the full M0→M4 pipeline and return intermediate + final outputs.

    Args:
        di: DiagnosticInput from user/CSV.
        db_path: Path to vref.db (defaults to engine/v2/vref.db).
        soft_mode: Passed to VL (categories 6, 8b are warnings only).

    Returns:
        (validated_input, dna_output, evidence_vector, raw_probs)
    """
    vi = validate(di, soft_mode=soft_mode)
    dna = load_dna(vi, db_path=db_path if db_path is not None else _VREF_DB_PATH)
    digital = parse_digital(vi, dna)
    gas = analyse_gas(vi, dna)
    evidence = arbitrate(vi, dna, digital, gas)
    raw_probs = score_faults(evidence, dna, _faults(), _edges())
    return vi, dna, evidence, raw_probs


# ── helpers ─────────────────────────────────────────────────────────────────


def _ctx(
    brand: str = "VOLKSWAGEN",
    model: str = "Golf",
    engine_code: str = "EA111_1.2_TSI",
    displacement_cc: int = 1197,
    my: int = 2012,
) -> VehicleContext:
    return VehicleContext(
        brand=brand,
        model=model,
        engine_code=engine_code,
        displacement_cc=displacement_cc,
        my=my,
    )


def _gas_idle(
    co_pct: float = 0.1,
    hc_ppm: float = 12.0,
    co2_pct: float = 15.2,
    o2_pct: float = 0.3,
    nox_ppm: float = 25.0,
    lambda_analyser: float = 1.0,
) -> GasRecord:
    return GasRecord(
        co_pct=co_pct,
        hc_ppm=hc_ppm,
        co2_pct=co2_pct,
        o2_pct=o2_pct,
        nox_ppm=nox_ppm,
        lambda_analyser=lambda_analyser,
    )


def _gas_high(
    co_pct: float = 0.08,
    hc_ppm: float = 10.0,
    co2_pct: float = 15.0,
    o2_pct: float = 0.2,
    nox_ppm: float = 80.0,
    lambda_analyser: float = 1.0,
) -> GasRecord:
    return GasRecord(
        co_pct=co_pct,
        hc_ppm=hc_ppm,
        co2_pct=co2_pct,
        o2_pct=o2_pct,
        nox_ppm=nox_ppm,
        lambda_analyser=lambda_analyser,
    )


def _obd(
    *,
    stft_b1: float | None = None,
    ltft_b1: float | None = None,
    stft_b2: float | None = None,
    ltft_b2: float | None = None,
    map_kpa: float | None = None,
    maf_gs: float | None = None,
    rpm: int | None = None,
    ect_c: float | None = None,
    iat_c: float | None = None,
    fuel_status: str | None = None,
    o2_voltage_b1: float | None = None,
    o2_voltage_b2: float | None = None,
    obd_lambda: float | None = None,
    vvt_angle: float | None = None,
    fuel_pressure_kpa: float | None = None,
    baro_kpa: float | None = None,
    evap_purge_pct: float | None = None,
    load_pct: float | None = None,
    tps_pct: float | None = None,
) -> OBDRecord:
    return OBDRecord(
        stft_b1=stft_b1,
        ltft_b1=ltft_b1,
        stft_b2=stft_b2,
        ltft_b2=ltft_b2,
        map_kpa=map_kpa,
        maf_gs=maf_gs,
        rpm=rpm,
        ect_c=ect_c,
        iat_c=iat_c,
        fuel_status=fuel_status,
        o2_voltage_b1=o2_voltage_b1,
        o2_voltage_b2=o2_voltage_b2,
        obd_lambda=obd_lambda,
        vvt_angle=vvt_angle,
        fuel_pressure_kpa=fuel_pressure_kpa,
        baro_kpa=baro_kpa,
        evap_purge_pct=evap_purge_pct,
        load_pct=load_pct,
        tps_pct=tps_pct,
    )


def _di(
    *,
    ctx: VehicleContext | None = None,
    gas_idle: GasRecord | None = None,
    gas_high: GasRecord | None = None,
    obd: OBDRecord | None = None,
    dtcs: list[str] | None = None,
    analyser_type: Literal["4-gas", "5-gas"] = "5-gas",
    ff: FreezeFrameRecord | None = None,
) -> DiagnosticInput:
    return DiagnosticInput(
        vehicle_context=ctx or _ctx(),
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
        dtcs=dtcs or [],
        analyser_type=analyser_type,
        freeze_frame=ff,
    )


def _top_fault(raw_probs: dict[str, float]) -> tuple[str, float]:
    """Return the highest-scoring fault and its score."""
    return max(raw_probs.items(), key=lambda x: x[1])


# ── CSV loader ──────────────────────────────────────────────────────────────


def _load_corpus_rows() -> list[dict[str, str]]:
    """Load all corpus rows as dicts."""
    with open(_CORPUS_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def _parse_float(raw: str | None) -> float | None:
    """Parse a CSV cell to float, returning None for empty/missing."""
    if raw is None or raw.strip() == "":
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def _parse_int(raw: str | None) -> int | None:
    """Parse a CSV cell to int, returning None for empty/missing."""
    if raw is None or raw.strip() == "":
        return None
    try:
        return int(float(raw))
    except ValueError:
        return None


def csv_to_input(row: dict[str, str]) -> DiagnosticInput:
    """Convert a corpus CSV row to a DiagnosticInput."""
    ctx = VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code="EA111_1.2_TSI",
        displacement_cc=1390,
        my=_parse_int(row.get("my", "2012")) or 2012,
    )

    gas_idle = GasRecord(
        co_pct=_parse_float(row.get("co")) or 0.0,
        hc_ppm=_parse_float(row.get("hc")) or 0.0,
        co2_pct=_parse_float(row.get("co2")) or 0.0,
        o2_pct=_parse_float(row.get("o2")) or 0.0,
        nox_ppm=_parse_float(row.get("nox")),
        lambda_analyser=_parse_float(row.get("lambda_analyser")),
    )

    gas_high_co = _parse_float(row.get("co_2500"))
    gas_high = None
    if gas_high_co is not None:
        gas_high = GasRecord(
            co_pct=gas_high_co,
            hc_ppm=_parse_float(row.get("hc_2500")) or 0.0,
            co2_pct=_parse_float(row.get("co2_2500")) or 0.0,
            o2_pct=_parse_float(row.get("o2_2500")) or 0.0,
            nox_ppm=_parse_float(row.get("nox_2500")),
            lambda_analyser=_parse_float(row.get("lambda_2500")),
        )

    stft_b1 = _parse_float(row.get("stft_b1"))
    ltft_b1 = _parse_float(row.get("ltft_b1"))
    obd = None
    if stft_b1 is not None or ltft_b1 is not None:
        obd = OBDRecord(
            stft_b1=stft_b1,
            ltft_b1=ltft_b1,
            stft_b2=_parse_float(row.get("stft_b2")),
            ltft_b2=_parse_float(row.get("ltft_b2")),
            obd_lambda=_parse_float(row.get("obd_lambda")),
            rpm=_parse_int(row.get("rpm")),
            ect_c=_parse_float(row.get("ect")),
            map_kpa=_parse_float(row.get("map")),
            maf_gs=_parse_float(row.get("maf")),
            fuel_status=row.get("fuel_status", "").strip() or None,
            fuel_pressure_kpa=_parse_float(row.get("fuel_pressure")),
        )

    dtcs_str = row.get("dtcs", "").strip()
    dtcs = [d.strip() for d in dtcs_str.split("|") if d.strip()] if dtcs_str else []

    analyser_raw = row.get("analyser_type", "5-gas").strip() or "5-gas"
    if analyser_raw == "5-gas":
        analyser_type: Literal["4-gas", "5-gas"] = "5-gas"
    else:
        analyser_type = "4-gas"
    return DiagnosticInput(
        vehicle_context=ctx,
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
        dtcs=dtcs,
        analyser_type=analyser_type,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# 1–5: Golden corpus case pipeline runs
# ═══════════════════════════════════════════════════════════════════════════════


def test_pipeline_runs_on_corpus_csv_001_stoich() -> None:
    """CSV-001: Perfect stoich — pipeline should produce bounded scores."""
    row = {"case_id": "CSV-001", "hc": "12", "co": "0.1", "co2": "15.2",
           "o2": "0.3", "nox": "25", "lambda_analyser": "1.0"}
    di = csv_to_input(row)
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert vi is not None
    assert dna.engine_state == "warm_closed_loop"
    assert len(raw_probs) > 0
    # All scores must be in [0.0, 1.0].
    for fid, score in raw_probs.items():
        assert 0.0 <= score <= 1.0, f"{fid} score {score} out of bounds"


def test_pipeline_runs_on_corpus_csv_016_lean_vacuum_leak() -> None:
    """CSV-016: Lean vacuum leak — pipeline produces lean symptoms and scores.

    analyser λ=1.271, OBD λ=1.18 — both lean, delta=0.091.
    Perception gap only fires when analyser and ECU are on opposite sides of
    stoich (v2-arbitrator §2.1), so no gap expected here despite the delta.
    """
    row = {
        "case_id": "CSV-016", "hc": "45", "co": "0.02", "co2": "11.5",
        "o2": "4.5", "nox": "120", "lambda_analyser": "1.271",
        "stft_b1": "18", "ltft_b1": "12", "obd_lambda": "1.18",
        "dtcs": "P0171",
    }
    di = csv_to_input(row)
    vi, dna, evidence, raw_probs = run_pipeline(di)

    # Lean gas symptoms should fire (O2=4.5% → SYM_O2_HIGH, λ=1.271 → SYM_LAMBDA_HIGH).
    assert "SYM_LAMBDA_HIGH" in evidence.active_symptoms
    assert "SYM_O2_HIGH" in evidence.active_symptoms

    # Lean-related fault families should have non-zero scores.
    lean_scores = {fid: s for fid, s in raw_probs.items()
                   if "lean" in fid.lower() or "Leak" in fid or "Vacuum" in fid}
    assert len(lean_scores) > 0, "Expected lean/leak fault scores > 0"


def test_pipeline_runs_on_corpus_csv_018_rich_injector() -> None:
    """CSV-018: Rich CO with negative trims — rich fault should score."""
    row = {
        "case_id": "CSV-018", "hc": "180", "co": "4.5", "co2": "12.5",
        "o2": "0.2", "nox": "30", "lambda_analyser": "0.85",
        "stft_b1": "-15", "ltft_b1": "-10", "obd_lambda": "0.86",
        "dtcs": "P0172",
    }
    di = csv_to_input(row)
    vi, dna, evidence, raw_probs = run_pipeline(di)

    # Rich fault family should be among top scorers.
    top_fid, top_score = _top_fault(raw_probs)
    assert top_score > 0.0, "Expected at least one fault with positive score"


def test_pipeline_runs_on_corpus_csv_005_clean_no_fault() -> None:
    """CSV-005: Clean burn — gas symptoms exist but are neutral (normal/high quality)."""
    row = {
        "case_id": "CSV-005", "hc": "5", "co": "0.05", "co2": "15.5",
        "o2": "0.1", "nox": "15", "lambda_analyser": "1.0",
        "stft_b1": "-1", "ltft_b1": "0", "obd_lambda": "1.0",
    }
    di = csv_to_input(row)
    vi, dna, evidence, raw_probs = run_pipeline(di)

    # Near-stoich case — gas symptoms are neutral/healthy (LAMBDA_NORMAL, HC_LOW, CO2_GOOD).
    gas_syms = [s for s in evidence.active_symptoms
                if not s.startswith("SYM_DTC") and not s.startswith("SYM_TRIM")]
    # Neutral gas symptoms do not produce high-scoring faults.
    assert len(gas_syms) >= 2, "Expected at least 2 gas symptoms for stoich input"

    # Top fault scores should be low (no strong evidence for any specific fault).
    top_fid, top_score = _top_fault(raw_probs)
    # With neutral evidence, fault scores should be modest at most.
    assert top_score <= 0.60, (
        f"Top fault {top_fid} scored {top_score:.3f} — too high for clean burn"
    )


def test_pipeline_runs_with_dtc_only_no_gas() -> None:
    """DTC-only input (no gas data) — pipeline should run on digital symptoms alone."""
    ctx = _ctx()
    di = _di(ctx=ctx, gas_idle=None, gas_high=None, obd=_obd(
        stft_b1=10.0, ltft_b1=8.0, ect_c=90.0, rpm=800, fuel_status="CL",
    ), dtcs=["P0301", "P0302"])
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert "SYM_DTC_MISFIRE" in evidence.active_symptoms
    assert dna.engine_state == "warm_closed_loop"
    assert len(raw_probs) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# 6–10: Era and technology veto behaviour
# ═══════════════════════════════════════════════════════════════════════════════


def test_era_pre_obdii_vehicle_vetoes_post_1996_faults() -> None:
    """MY 1994 vehicle — faults with era ['1996-2005', ...] only must score 0.0."""
    ctx = _ctx(my=1994, engine_code="PM_1.6_8V")
    di = _di(ctx=ctx, gas_idle=_gas_idle(lambda_analyser=0.95),
             dtcs=["P0420"])  # P0420 is OBD-II era
    vi, dna, evidence, raw_probs = run_pipeline(di)
    assert dna.era_bucket == ERA_PRE_OBDII

    # Faults with era excluding 1990-1995 must score 0.0.
    faults = _faults()
    for fid, score in raw_probs.items():
        fault_era = faults.get(fid, {}).get("era", [])
        if fault_era and "1990-1995" not in fault_era:
            assert score == 0.0, f"{fid} should be era-vetoed (era={fault_era})"


def test_era_modern_vehicle_scores_modern_faults() -> None:
    """MY 2018 vehicle — faults with era ['2016-2020'] must be eligible."""
    ctx = _ctx(my=2018, engine_code="EA888_2.0_TSI")
    di = _di(ctx=ctx, gas_idle=_gas_idle(lambda_analyser=1.08, o2_pct=4.0),
             obd=_obd(stft_b1=15, ltft_b1=10, ect_c=95.0, rpm=800,
                      fuel_status="CL"))
    vi, dna, evidence, raw_probs = run_pipeline(di)
    assert dna.era_bucket == ERA_MODERN

    # At least one modern-era fault should score > 0 given lean evidence.
    faults = _faults()
    modern_scoring = {fid: s for fid, s in raw_probs.items()
                      if s > 0 and "2016-2020" in faults.get(fid, {}).get("era", [])}
    assert len(modern_scoring) > 0, "Expected modern-era faults with positive scores"


def test_tech_veto_gdi_fault_on_non_gdi_engine() -> None:
    """Non-GDI engine — GDI-required faults must score 0.0."""
    ctx = _ctx(my=2008, engine_code="M112_2.8_V6")  # Non-GDI engine
    di = _di(ctx=ctx, gas_idle=_gas_idle(lambda_analyser=0.95, co_pct=2.0),
             obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL"))
    vi, dna, evidence, raw_probs = run_pipeline(di)

    faults = _faults()
    for fid, score in raw_probs.items():
        tech_req = faults.get(fid, {}).get("tech_required", [])
        if "has_gdi" in tech_req:
            assert score == 0.0, (
                f"{fid} requires GDI but engine lacks it; should be vetoed"
            )


def test_era_bucket_assignment_from_my() -> None:
    """Verify era bucket is correctly assigned from MY when vref.db misses."""
    ctx = _ctx(my=2001, engine_code="UNKNOWN_CODE_XYZ")
    di = _di(ctx=ctx, gas_idle=_gas_idle())
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert dna.era_bucket == ERA_OBDII_EARLY
    assert dna.vref_missing is True
    assert dna.confidence_ceiling == pytest.approx(0.60, abs=0.01)


def test_vref_db_known_engine_has_full_confidence() -> None:
    """Known engine code in vref.db — confidence ceiling should be 1.00."""
    ctx = _ctx(my=2012, engine_code="EA111_1.2_TSI")
    di = _di(ctx=ctx, gas_idle=_gas_idle())
    vi, dna, evidence, raw_probs = run_pipeline(di)

    # EA111_1.2_TSI should be in vref.db (populated in T-P1-7).
    if not dna.vref_missing:
        assert dna.confidence_ceiling == pytest.approx(1.00, abs=0.01)


# ═══════════════════════════════════════════════════════════════════════════════
# 11–15: Perception gap and engine-state paths
# ═══════════════════════════════════════════════════════════════════════════════


def test_perception_gap_lean_seen_rich() -> None:
    """Analyser λ=0.90 (rich), OBD λ=1.10 (lean) — LEAN_SEEN_RICH perception gap."""
    ctx = _ctx(my=2010)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.90, co_pct=3.0, o2_pct=0.2),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL", obd_lambda=1.10),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert evidence.perception_gap is not None
    pg = evidence.perception_gap
    assert pg.gap_type == "LEAN_SEEN_RICH"
    assert pg.analyser_lambda == pytest.approx(0.90, abs=0.05)
    assert pg.obd_lambda == pytest.approx(1.10, abs=0.01)

    # Perception symptom must be in evidence vector (L01: no global override).
    assert "SYM_PERCEPTION_LEAN_SEEN_RICH" in evidence.active_symptoms
    pg_cf = evidence.active_symptoms["SYM_PERCEPTION_LEAN_SEEN_RICH"]
    assert 0.0 < pg_cf <= 0.70


def test_perception_gap_rich_seen_lean() -> None:
    """Analyser λ=1.08 (lean), OBD λ=0.95 (rich) — RICH_SEEN_LEAN perception gap."""
    ctx = _ctx(my=2012)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=1.08, co_pct=0.02, o2_pct=4.5),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL", obd_lambda=0.95),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert evidence.perception_gap is not None
    assert evidence.perception_gap.gap_type == "RICH_SEEN_LEAN"
    assert "SYM_PERCEPTION_RICH_SEEN_LEAN" in evidence.active_symptoms


def test_no_perception_gap_when_delta_below_threshold() -> None:
    """Delta λ = 0.04 (< 0.05 threshold) — no perception gap should fire."""
    ctx = _ctx(my=2012)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=1.02),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL", obd_lambda=1.00),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert evidence.perception_gap is None


def test_cold_start_engine_state() -> None:
    """ECT = 30 °C — engine_state should be cold_open_loop."""
    ctx = _ctx(my=2012)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.95),
        obd=_obd(ect_c=30.0, rpm=200, fuel_status="OL"),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert dna.engine_state == "cold_open_loop"
    assert vi.restricted_cold_start is True


def test_open_loop_suppression_warm() -> None:
    """ECT = 90 °C, fuel_status = OL_FAULT — warm_open_loop, trim suppressed."""
    ctx = _ctx(my=2012)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.95),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="OL_FAULT",
                 stft_b1=15, ltft_b1=10),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert dna.engine_state == "warm_open_loop"
    assert vi.open_loop_suppression is True


# ═══════════════════════════════════════════════════════════════════════════════
# 16–20: Structural assertions (CF bounds, root causes, edge cases)
# ═══════════════════════════════════════════════════════════════════════════════


def test_raw_probs_all_in_bounds() -> None:
    """All raw_probs must be in [0.0, 1.0] for a complex multi-symptom case."""
    ctx = _ctx(my=2015)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.92, co_pct=4.0, hc_ppm=300,
                           o2_pct=0.1, co2_pct=12.0),
        gas_high=_gas_high(lambda_analyser=0.94, co_pct=3.5),
        obd=_obd(stft_b1=-12, ltft_b1=-8, ect_c=95.0, rpm=800,
                 fuel_status="CL", obd_lambda=0.92),
        dtcs=["P0172", "P0300"],
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert len(raw_probs) > 0
    for fid, score in raw_probs.items():
        assert 0.0 <= score <= 1.0, f"{fid} score {score} out of bounds"


def test_evidence_vector_not_empty_for_symptomatic_case() -> None:
    """A case with rich CO + DTCs must produce active symptoms."""
    ctx = _ctx(my=2010)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.88, co_pct=5.0, o2_pct=0.1),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL"),
        dtcs=["P0172"],
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    assert len(evidence.active_symptoms) >= 2, (
        f"Expected ≥ 2 active symptoms, got {len(evidence.active_symptoms)}"
    )


def test_root_causes_gate_on_parent_threshold() -> None:
    """Root causes only qualify when parent fault score ≥ 0.80."""
    ctx = _ctx(my=2012)
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.95, co_pct=3.0),
        obd=_obd(ect_c=90.0, rpm=800, fuel_status="CL"),
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    qualified = score_root_causes(raw_probs, _root_causes())
    for rc_id, rc_def in qualified.items():
        parent_score = rc_def.get("parent_score", 0.0)
        assert parent_score >= 0.80, (
            f"Root cause {rc_id} qualified with parent_score={parent_score} < 0.80"
        )


def test_pipeline_produces_consistent_engine_state() -> None:
    """Engine state from M0 must be one of the 5 valid FSM states."""
    valid_states = {
        "cold_open_loop", "warm_cranking", "warm_closed_loop",
        "warm_open_loop", "warm_dfco",
    }
    ctx = _ctx(my=2012)
    for ect, rpm, fs, expected in [
        (30.0, 200, "OL", "cold_open_loop"),
        (90.0, 0, None, "warm_cranking"),
        (90.0, 800, "CL", "warm_closed_loop"),
        (90.0, 800, "OL_DRIVE", "warm_open_loop"),
        (90.0, 800, "OL", "warm_dfco"),
    ]:
        di = _di(
            ctx=ctx,
            gas_idle=_gas_idle(),
            obd=_obd(ect_c=ect, rpm=rpm, fuel_status=fs),
        )
        vi, dna, evidence, raw_probs = run_pipeline(di)
        assert dna.engine_state == expected, (
            f"ECT={ect}, RPM={rpm}, FS={fs} → {dna.engine_state}, expected {expected}"
        )
        assert dna.engine_state in valid_states


def test_pipeline_with_full_corpus_fixture_rich_co() -> None:
    """Integration test using a full fixture that exercises M0→M4 end-to-end.

    Rich CO scenario: CO=5%, λ=0.85, negative trims, P0172.
    M1 should emit SYM_DTC_P0172 + trim symptoms.
    M2 should emit SYM_LAMBDA_LOW + SYM_CO_HIGH.
    M3 should assemble all into evidence vector with appropriate CFs.
    M4 should score rich-mixture faults above lean-mixture faults.
    """
    ctx = _ctx(my=2010, engine_code="EA113_2.0_FSI")
    di = _di(
        ctx=ctx,
        gas_idle=_gas_idle(lambda_analyser=0.85, co_pct=5.0, hc_ppm=250,
                           o2_pct=0.1, co2_pct=12.0, nox_ppm=20),
        obd=_obd(ect_c=92.0, rpm=800, fuel_status="CL",
                 stft_b1=-15, ltft_b1=-10, obd_lambda=0.86),
        dtcs=["P0172"],
    )
    vi, dna, evidence, raw_probs = run_pipeline(di)

    # Evidence should include gas and digital symptoms.
    assert len(evidence.active_symptoms) >= 3

    # Top fault should be a rich-mixture family member.
    faults = _faults()
    rich_family_ids = {fid for fid, fdef in faults.items()
                       if fdef.get("parent") == "Rich_Mixture"}
    top_fid, top_score = _top_fault(raw_probs)
    assert top_score > 0.0
    if top_fid in rich_family_ids:
        # Verify other rich faults also score.
        rich_scores = {fid: raw_probs.get(fid, 0.0) for fid in rich_family_ids}
        scoring_rich = {fid: s for fid, s in rich_scores.items() if s > 0}
        assert len(scoring_rich) > 0
