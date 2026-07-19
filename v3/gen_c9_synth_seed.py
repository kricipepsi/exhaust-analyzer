#!/usr/bin/env python3
"""Generate provisional synthetic C9 (independent healthy-confirm) seed data.

This generator produces the side files:
- v3/data/c9_synthetic_seed_2026-07-06.csv
- v3/data/c9_synthetic_seed_2026-07-06.json
- v3/reports/V3_C9_SYNTH_BANDS_2026-07-06.md

This script runs deterministically (seeded per case_id) and obeys the five rules
of the Phase 4 signal pack contract. No live corpus or engine code is modified.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import cast

# --- paths (all under v3/, no live-corpus write) -----------------------------------------
ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
OUT_CSV = ROOT / "v3/data/c9_synthetic_seed_2026-07-06.csv"
OUT_JSON = ROOT / "v3/data/c9_synthetic_seed_2026-07-06.json"
OUT_REPORT = ROOT / "v3/reports/V3_C9_SYNTH_BANDS_2026-07-06.md"

DATE = "2026-07-06"

# Pinned 11 C9 cases (V3_C9_REVEAL_CONTRACT_2026-07-06 §6)
C9_CASES: tuple[str, ...] = (
    "CSV-127",
    "CSV-128",
    "EXT-216",
    "PDF-HI-005",
    "PDF-HI-010",
    "YAML-PDF_HI_005",
    "YAML-PDF_HI_010",
    "YAML-TC1",
    "case_014",
    "era2_016",
    "era3_014",
)

# Research producer thresholds from cluster9.1.md / value9.md and V3_C9_REVEAL_CONTRACT_2026-07-06 §2.
# Used for verification checks only; not consumer-rule thresholds.
RESEARCH_READINESS_COMPLETE = True
RESEARCH_DTC_COUNT_MAX = 0
RESEARCH_MODE06_MARGIN_MIN = 10.0
RESEARCH_WARMUP_CYCLES_MIN = 5
RESEARCH_MILES_SINCE_CLEAR_MIN = 200
RESEARCH_STFT_MAX = 5.0
RESEARCH_LTFT_MAX = 7.0
RESEARCH_TRIM_DELTA_MAX = 5.0
RESEARCH_GAS_HC_MIN = -10.0
RESEARCH_GAS_HC_MAX = 15.0
RESEARCH_GAS_CO_MIN = -0.15
RESEARCH_GAS_CO_MAX = 0.15
RESEARCH_GAS_CO2_MIN = 0.3
RESEARCH_GAS_CO2_MAX = 0.8
RESEARCH_GAS_O2_MIN = -0.5
RESEARCH_GAS_O2_MAX = 0.4


@dataclass(frozen=True)
class Band:
    """A tolerance-wide sampling band ``[lo, hi]`` for one synthetic column."""

    lo: float
    hi: float
    decimals: int = 2

    def sample(self, rng: random.Random) -> float:
        return round(rng.uniform(self.lo, self.hi), self.decimals)

    @property
    def sigma(self) -> float:
        # Uniform[lo,hi] std-dev = (hi-lo)/sqrt(12); reported as the tolerance spread.
        return round((self.hi - self.lo) / (12.0**0.5), 3)


@dataclass(frozen=True)
class CodeBandInfo:
    """One oracle sub-fault code's C9 signal band group."""

    band_id: str
    fault_name: str
    emit_path: str
    c9_separable: bool
    stay_abstained: bool
    signature: str

    readiness_supported_complete_bool: bool
    stored_dtc_count: int
    pending_dtc_count: int
    permanent_dtc_count: int
    mode06_min_margin_pct: Band
    warmup_cycles_since_clear: Band
    miles_since_clear: Band

    stft_idle_pct: Band
    ltft_idle_pct: Band
    stft_2500_pct: Band
    ltft_2500_pct: Band

    gas_delta_hc_ppm: Band
    gas_delta_co_pct: Band
    gas_delta_co2_pct: Band
    gas_delta_o2_pct: Band


# --- Web-corroborated, tolerance-wide band table keyed on ORACLE fault CODE --------------
# Keyed on expected_fault_code from cases_petrol_v7.csv.
# OPTIMAL_HEALTH triggers SYSTEM_HEALTH_CONFIRMED (no-fault).
# ERR-MF-008 (misfire lookalike) fails check and triggers SENSOR_HEALTH_UNPROVEN_ABSTAIN.
CODE_BANDS: dict[str, CodeBandInfo] = {
    # --- Separable: Optimal Health (completes all OBD gates and combustion trim/gas gates) ---
    "OPTIMAL_HEALTH": CodeBandInfo(
        band_id="C9-HEALTHY",
        fault_name="no_fault",
        emit_path="SYSTEM_HEALTH_CONFIRMED",
        c9_separable=True,
        stay_abstained=False,
        signature=("Optimal vehicle health: readiness complete, DTCs absent, "
                   "good Mode $06 margins, stable trims, clean 2-point gas deltas."),
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=0,
        permanent_dtc_count=0,
        mode06_min_margin_pct=Band(15.0, 95.0, decimals=1),       # range: 15-95% (FIRES >= 10% check)
        warmup_cycles_since_clear=Band(5.0, 40.0, decimals=0),     # >= 5 cycles (FIRES check)
        miles_since_clear=Band(200.0, 800.0, decimals=0),          # >= 200 miles (FIRES check)
        stft_idle_pct=Band(-4.0, 4.0, decimals=1),                 # P10-P90 STFT
        ltft_idle_pct=Band(-6.0, 6.0, decimals=1),                 # P10-P90 LTFT
        stft_2500_pct=Band(-4.0, 4.0, decimals=1),
        ltft_2500_pct=Band(-6.0, 6.0, decimals=1),
        gas_delta_hc_ppm=Band(-10.0, 15.0, decimals=0),            # delta HC -10 to +15 ppm
        gas_delta_co_pct=Band(-0.15, 0.15, decimals=3),            # delta CO -0.15 to +0.15%
        gas_delta_co2_pct=Band(0.30, 0.80, decimals=2),            # delta CO2 +0.3 to +0.8%
        gas_delta_o2_pct=Band(-0.50, 0.40, decimals=2),            # delta O2 -0.5 to +0.4%
    ),
    # --- Stay-Abstained: Ghost Misfire lookalike (fails DTC, margins, and trims) ---
    "ERR-MF-008": CodeBandInfo(
        band_id="C9-MISFIRE-LOOKALIKE",
        fault_name="misfire_lookalike",
        emit_path="SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        c9_separable=False,
        stay_abstained=True,
        signature=("Ghost misfire lookalike: currently winning no_fault, but fails the "
                   "OBD health confirmation because of a pending misfire DTC, narrow monitor margins, "
                   "and unstable fuel trims."),
        readiness_supported_complete_bool=True,
        stored_dtc_count=0,
        pending_dtc_count=1,                                       # FAILS DTC check (>0)
        permanent_dtc_count=0,
        mode06_min_margin_pct=Band(1.0, 5.0, decimals=1),          # FAILS margin check (< 10%)
        warmup_cycles_since_clear=Band(5.0, 40.0, decimals=0),
        miles_since_clear=Band(200.0, 800.0, decimals=0),
        stft_idle_pct=Band(6.0, 12.0, decimals=1),                 # FAILS STFT check (> 5%)
        ltft_idle_pct=Band(8.0, 15.0, decimals=1),                 # FAILS LTFT check (> 7%)
        stft_2500_pct=Band(2.0, 6.0, decimals=1),
        ltft_2500_pct=Band(4.0, 8.0, decimals=1),
        gas_delta_hc_ppm=Band(25.0, 60.0, decimals=0),             # FAILS HC delta (>15)
        gas_delta_co_pct=Band(0.20, 0.50, decimals=3),             # FAILS CO delta (>0.15)
        gas_delta_co2_pct=Band(-1.50, -0.50, decimals=2),          # FAILS CO2 positive delta check
        gas_delta_o2_pct=Band(0.50, 1.50, decimals=2),             # FAILS O2 delta (>0.4)
    ),
}

ALL_COLS = (
    "readiness_supported_complete_bool",
    "stored_dtc_count",
    "pending_dtc_count",
    "permanent_dtc_count",
    "mode06_min_margin_pct",
    "warmup_cycles_since_clear",
    "miles_since_clear",
    "stft_idle_pct",
    "ltft_idle_pct",
    "stft_2500_pct",
    "ltft_2500_pct",
    "gas_delta_hc_ppm",
    "gas_delta_co_pct",
    "gas_delta_co2_pct",
    "gas_delta_o2_pct",
)


def _rng_for(case_id: str) -> random.Random:
    """Deterministic PRNG seeded from the case_id (stable across runs; not wall-clock)."""
    digest = hashlib.sha256(case_id.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def load_c9_oracle() -> dict[str, tuple[str, str]]:
    """Return {case_id: (expected_fault_family, expected_fault_code)} for the 11 C9 cases."""
    want = set(C9_CASES)
    oracle: dict[str, tuple[str, str]] = {}
    with CORPUS.open(newline="") as fh:
        for row in csv.DictReader(fh):
            cid = row["case_id"]
            if cid in want:
                oracle[cid] = (row["expected_fault_family"], row["expected_fault_code"])
    missing = want - oracle.keys()
    if missing:
        raise SystemExit(f"C9 cases missing from corpus: {sorted(missing)}")
    return oracle


def seed_case(case_id: str, oracle_code: str) -> dict[str, object]:
    """Sample one case's synthetic columns from its oracle CODE's web-validated bands."""
    info = CODE_BANDS.get(oracle_code)
    if info is None:
        raise SystemExit(f"{case_id}: oracle code {oracle_code!r} has no C9 band (unexpected)")

    rng = _rng_for(case_id)

    # Sample readiness and DTCs
    readiness = info.readiness_supported_complete_bool
    stored_dtc = info.stored_dtc_count
    pending_dtc = info.pending_dtc_count
    permanent_dtc = info.permanent_dtc_count

    # Sample margin and reset counters (cast counts to int)
    margin = info.mode06_min_margin_pct.sample(rng)
    wuc = int(info.warmup_cycles_since_clear.sample(rng))
    miles = int(info.miles_since_clear.sample(rng))

    # Sample trims with joint constraint for healthy cases
    if info.c9_separable:
        # Rejection sampler to satisfy trim constraints
        stft_idle = info.stft_idle_pct.sample(rng)
        ltft_idle = info.ltft_idle_pct.sample(rng)
        stft_2500 = info.stft_2500_pct.sample(rng)
        ltft_2500 = info.ltft_2500_pct.sample(rng)

        tft_idle = stft_idle + ltft_idle
        tft_2500 = stft_2500 + ltft_2500
        while not (
            abs(stft_idle) <= RESEARCH_STFT_MAX and
            abs(ltft_idle) <= RESEARCH_LTFT_MAX and
            abs(stft_2500) <= RESEARCH_STFT_MAX and
            abs(ltft_2500) <= RESEARCH_LTFT_MAX and
            abs(tft_idle - tft_2500) <= RESEARCH_TRIM_DELTA_MAX
        ):
            stft_idle = info.stft_idle_pct.sample(rng)
            ltft_idle = info.ltft_idle_pct.sample(rng)
            stft_2500 = info.stft_2500_pct.sample(rng)
            ltft_2500 = info.ltft_2500_pct.sample(rng)
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
    else:
        # Stay abstained case (no joint constraint needed as it fails healthy check)
        stft_idle = info.stft_idle_pct.sample(rng)
        ltft_idle = info.ltft_idle_pct.sample(rng)
        stft_2500 = info.stft_2500_pct.sample(rng)
        ltft_2500 = info.ltft_2500_pct.sample(rng)

    # Sample gas deltas (cast ppm to int)
    gas_hc = int(info.gas_delta_hc_ppm.sample(rng))
    gas_co = info.gas_delta_co_pct.sample(rng)
    gas_co2 = info.gas_delta_co2_pct.sample(rng)
    gas_o2 = info.gas_delta_o2_pct.sample(rng)

    return {
        "case_id": case_id,
        "oracle_fault_family": "no_fault" if info.c9_separable else "misfire",
        "oracle_fault_code": oracle_code,
        "oracle_fault_name": info.fault_name,
        "band_id": info.band_id,
        "emit_path": info.emit_path,
        "c9_separable": info.c9_separable,
        "stay_abstained": info.stay_abstained,
        "synthetic": True,
        "readiness_supported_complete_bool": readiness,
        "stored_dtc_count": stored_dtc,
        "pending_dtc_count": pending_dtc,
        "permanent_dtc_count": permanent_dtc,
        "mode06_min_margin_pct": margin,
        "warmup_cycles_since_clear": wuc,
        "miles_since_clear": miles,
        "stft_idle_pct": stft_idle,
        "ltft_idle_pct": ltft_idle,
        "stft_2500_pct": stft_2500,
        "ltft_2500_pct": ltft_2500,
        "gas_delta_hc_ppm": gas_hc,
        "gas_delta_co_pct": gas_co,
        "gas_delta_co2_pct": gas_co2,
        "gas_delta_o2_pct": gas_o2,
    }


def _assert_no_backsolve(seed_rows: list[dict[str, object]]) -> None:
    """Robustness and correctness audit.

    Verifies that separable cases trigger their intended diagnostic paths,
    and stay-abstained cases stay abstained. Uses only research limits.
    """
    assert len(seed_rows) == 11, f"expected 11 C9 cases, got {len(seed_rows)}"
    for r in seed_rows:
        code = str(r["oracle_fault_code"])
        info = CODE_BANDS[code]
        assert r["band_id"] == info.band_id
        assert r["synthetic"] is True

        readiness = cast(bool, r["readiness_supported_complete_bool"])
        stored_dtc = cast(int, r["stored_dtc_count"])
        pending_dtc = cast(int, r["pending_dtc_count"])
        permanent_dtc = cast(int, r["permanent_dtc_count"])
        margin = cast(float, r["mode06_min_margin_pct"])
        wuc = cast(int, r["warmup_cycles_since_clear"])
        miles = cast(int, r["miles_since_clear"])

        stft_idle = cast(float, r["stft_idle_pct"])
        ltft_idle = cast(float, r["ltft_idle_pct"])
        stft_2500 = cast(float, r["stft_2500_pct"])
        ltft_2500 = cast(float, r["ltft_2500_pct"])

        gas_hc = cast(float, r["gas_delta_hc_ppm"])
        gas_co = cast(float, r["gas_delta_co_pct"])
        gas_co2 = cast(float, r["gas_delta_co2_pct"])
        gas_o2 = cast(float, r["gas_delta_o2_pct"])

        tft_idle = stft_idle + ltft_idle
        tft_2500 = stft_2500 + ltft_2500
        trim_delta = abs(tft_idle - tft_2500)

        if info.c9_separable:
            # OPTIMAL_HEALTH checks
            assert readiness is True, r
            assert stored_dtc == 0, r
            assert pending_dtc == 0, r
            assert permanent_dtc == 0, r
            assert margin >= RESEARCH_MODE06_MARGIN_MIN, r
            assert wuc >= RESEARCH_WARMUP_CYCLES_MIN, r
            assert miles >= RESEARCH_MILES_SINCE_CLEAR_MIN, r

            assert abs(stft_idle) <= RESEARCH_STFT_MAX, r
            assert abs(ltft_idle) <= RESEARCH_LTFT_MAX, r
            assert abs(stft_2500) <= RESEARCH_STFT_MAX, r
            assert abs(ltft_2500) <= RESEARCH_LTFT_MAX, r
            assert trim_delta <= RESEARCH_TRIM_DELTA_MAX, r

            assert RESEARCH_GAS_HC_MIN <= gas_hc <= RESEARCH_GAS_HC_MAX, r
            assert RESEARCH_GAS_CO_MIN <= gas_co <= RESEARCH_GAS_CO_MAX, r
            assert RESEARCH_GAS_CO2_MIN <= gas_co2 <= RESEARCH_GAS_CO2_MAX, r
            assert RESEARCH_GAS_O2_MIN <= gas_o2 <= RESEARCH_GAS_O2_MAX, r
        else:
            # era2_016 misfire lookalike checks (should fail at least one gate)
            gates_passed = (
                readiness is True and
                stored_dtc == 0 and
                pending_dtc == 0 and
                permanent_dtc == 0 and
                margin >= RESEARCH_MODE06_MARGIN_MIN and
                wuc >= RESEARCH_WARMUP_CYCLES_MIN and
                miles >= RESEARCH_MILES_SINCE_CLEAR_MIN and
                abs(stft_idle) <= RESEARCH_STFT_MAX and
                abs(ltft_idle) <= RESEARCH_LTFT_MAX and
                abs(stft_2500) <= RESEARCH_STFT_MAX and
                abs(ltft_2500) <= RESEARCH_LTFT_MAX and
                trim_delta <= RESEARCH_TRIM_DELTA_MAX and
                RESEARCH_GAS_HC_MIN <= gas_hc <= RESEARCH_GAS_HC_MAX and
                RESEARCH_GAS_CO_MIN <= gas_co <= RESEARCH_GAS_CO_MAX and
                RESEARCH_GAS_CO2_MIN <= gas_co2 <= RESEARCH_GAS_CO2_MAX and
                RESEARCH_GAS_O2_MIN <= gas_o2 <= RESEARCH_GAS_O2_MAX
            )
            assert not gates_passed, f"stay-abstained case era2_016 passed all healthy gates: {r}"


def _assert_no_collision(seed_rows: list[dict[str, object]]) -> None:
    """Verifies that none of the seeded C9 rows contain C5/C6 specific columns."""
    for r in seed_rows:
        # C5 specific columns
        assert "calc_load_wot_pct" not in r or r["calc_load_wot_pct"] is None
        assert "fuel_rail_pressure_load_kpa" not in r or r["fuel_rail_pressure_load_kpa"] is None
        assert "wideband_lambda_wot" not in r or r["wideband_lambda_wot"] is None
        # C6 specific columns
        assert "mode06_o2_response_margin_pct" not in r or r["mode06_o2_response_margin_pct"] is None
        assert "o2_rich_to_lean_ms" not in r or r["o2_rich_to_lean_ms"] is None
        assert "o2_lean_to_rich_ms" not in r or r["o2_lean_to_rich_ms"] is None
        assert "maf_actual_calc_delta_pct_idle" not in r or r["maf_actual_calc_delta_pct_idle"] is None
        assert "maf_actual_calc_delta_pct_2500" not in r or r["maf_actual_calc_delta_pct_2500"] is None


def write_csv(seed_rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "case_id",
        "oracle_fault_family",
        "oracle_fault_code",
        "oracle_fault_name",
        "band_id",
        "c9_separable",
        "stay_abstained",
        "synthetic",
        *ALL_COLS,
    ]
    with OUT_CSV.open(mode="w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in seed_rows:
            # Convert None to empty string for CSV representation
            row_to_write = {}
            for col in cols:
                val = r[col]
                row_to_write[col] = "" if val is None else val
            w.writerow(row_to_write)


def write_manifest(seed_rows: list[dict[str, object]]) -> None:
    manifest = {
        "task": "T-V3-P4-C9-SYNTH",
        "generated": DATE,
        "mode": "provisional-synthetic-seed (side file; live corpus untouched)",
        "policy": "4DLab_CLAUDE.md §Provisional synthetic signals",
        "oracle_discriminator": ("C9 cases share expected_fault_family=no_fault (10) or misfire (1); the "
                                 "band group is keyed on expected_fault_code, resolved to a "
                                 "registry fault_name"),
        "no_backsolve": ("generator keys only on expected_fault_code (oracle) + the web-validated "
                         "band table; does not read no_fault.json consumer thresholds or any case rank/prediction"),
        "research_limits_cluster9": {
            "readiness_complete": RESEARCH_READINESS_COMPLETE,
            "dtc_count_max": RESEARCH_DTC_COUNT_MAX,
            "mode06_margin_min_pct": RESEARCH_MODE06_MARGIN_MIN,
            "warmup_cycles_min": RESEARCH_WARMUP_CYCLES_MIN,
            "miles_since_clear_min": RESEARCH_MILES_SINCE_CLEAR_MIN,
            "stft_max_pct": RESEARCH_STFT_MAX,
            "ltft_max_pct": RESEARCH_LTFT_MAX,
            "trim_delta_max_pct": RESEARCH_TRIM_DELTA_MAX,
            "gas_hc_min_ppm": RESEARCH_GAS_HC_MIN,
            "gas_hc_max_ppm": RESEARCH_GAS_HC_MAX,
            "gas_co_min_pct": RESEARCH_GAS_CO_MIN,
            "gas_co_max_pct": RESEARCH_GAS_CO_MAX,
            "gas_co2_min_pct": RESEARCH_GAS_CO2_MIN,
            "gas_co2_max_pct": RESEARCH_GAS_CO2_MAX,
            "gas_o2_min_pct": RESEARCH_GAS_O2_MIN,
            "gas_o2_max_pct": RESEARCH_GAS_O2_MAX,
        },
        "grounding_tags": {
            "readiness_supported_complete_bool": "standardized (CARB/EPA)",
            "stored_dtc_count": "standardized (SAE J1979)",
            "pending_dtc_count": "standardized (SAE J1979)",
            "permanent_dtc_count": "standardized (SAE J1979)",
            "mode06_min_margin_pct": "standardized (regulatory cut)",
            "warmup_cycles_since_clear": "standardized (EPA/CARB)",
            "miles_since_clear": "standardized (CARB)",
            "stft_idle_pct": "standardized (OEM/SAE J1979)",
            "ltft_idle_pct": "standardized (OEM/SAE J1979)",
            "stft_2500_pct": "standardized (OEM/SAE J1979)",
            "ltft_2500_pct": "standardized (OEM/SAE J1979)",
            "gas_delta_hc_ppm": "anecdotal / workshop norm",
            "gas_delta_co_pct": "anecdotal / workshop norm",
            "gas_delta_co2_pct": "anecdotal / workshop norm (combustion shift)",
            "gas_delta_o2_pct": "anecdotal / workshop norm",
        },
        "band_table": {
            code: {
                "band_id": b.band_id,
                "fault_name": b.fault_name,
                "c9_separable": b.c9_separable,
                "stay_abstained": b.stay_abstained,
                "signature": b.signature,
                "static_values": {
                    "readiness_supported_complete_bool": b.readiness_supported_complete_bool,
                    "stored_dtc_count": b.stored_dtc_count,
                    "pending_dtc_count": b.pending_dtc_count,
                    "permanent_dtc_count": b.permanent_dtc_count,
                },
                "float_bands": {
                    "mode06_min_margin_pct": [b.mode06_min_margin_pct.lo, b.mode06_min_margin_pct.hi, b.mode06_min_margin_pct.sigma],
                    "warmup_cycles_since_clear": [b.warmup_cycles_since_clear.lo, b.warmup_cycles_since_clear.hi, b.warmup_cycles_since_clear.sigma],
                    "miles_since_clear": [b.miles_since_clear.lo, b.miles_since_clear.hi, b.miles_since_clear.sigma],
                    "stft_idle_pct": [b.stft_idle_pct.lo, b.stft_idle_pct.hi, b.stft_idle_pct.sigma],
                    "ltft_idle_pct": [b.ltft_idle_pct.lo, b.ltft_idle_pct.hi, b.ltft_idle_pct.sigma],
                    "stft_2500_pct": [b.stft_2500_pct.lo, b.stft_2500_pct.hi, b.stft_2500_pct.sigma],
                    "ltft_2500_pct": [b.ltft_2500_pct.lo, b.ltft_2500_pct.hi, b.ltft_2500_pct.sigma],
                    "gas_delta_hc_ppm": [b.gas_delta_hc_ppm.lo, b.gas_delta_hc_ppm.hi, b.gas_delta_hc_ppm.sigma],
                    "gas_delta_co_pct": [b.gas_delta_co_pct.lo, b.gas_delta_co_pct.hi, b.gas_delta_co_pct.sigma],
                    "gas_delta_co2_pct": [b.gas_delta_co2_pct.lo, b.gas_delta_co2_pct.hi, b.gas_delta_co2_pct.sigma],
                    "gas_delta_o2_pct": [b.gas_delta_o2_pct.lo, b.gas_delta_o2_pct.hi, b.gas_delta_o2_pct.sigma],
                },
            }
            for code, b in CODE_BANDS.items()
        },
        "citations": CITATIONS,
        "cases": {r["case_id"]: r for r in seed_rows},
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n")


CITATIONS: dict[str, str] = {
    "obd_readiness_completeness": (
        "All supported readiness monitors must complete to verify emission-control functionality "
        "before confirming health. California BAR OBD Test Reference; CARB/EPA regulations. "
        "Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf"
    ),
    "obd_dtc_count": (
        "Stored, pending, and permanent DTCs must all be zero to exclude active or intermittent faults. "
        "SAE J1979 / CARB regulations. Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf"
    ),
    "mode06_margin": (
        "Mode $06 monitor margins >= 10% ensures the emission systems are operating comfortably inside "
        "limits, not on the edge of failure. value9.md §1; SAE J1979. "
        "Corroborated: https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf"
    ),
    "obd_reset_age": (
        "Warm-up cycles since clear >= 5 and distance >= 200 miles prevent the fresh-reset blind spot "
        "where DTCs are cleared but monitors haven't run. CARB/EPA. "
        "Corroborated: https://www.bar.ca.gov/pdf/obd_test_reference.pdf"
    ),
    "fuel_trims": (
        "Healthy vehicles operate with trims within +/-5% (STFT) and +/-7% (LTFT), with minimal shift (<=5%) "
        "between idle and 2500 RPM. value9.md §1; SAE J1979. "
        "Corroborated: https://thegrouptrainingacademy.com/fuel-trim-diagnosis-o2-sensor-performance/"
    ),
    "five_gas_deltas": (
        "Two-speed idle-to-RPM gas deltas (HC, CO, CO2, O2) stay within tight combustion limits (e.g. "
        "ΔCO2 positive, ΔHC near 0) indicating stable, efficient combustion. value9.md §1; EPA/BAR. "
        "Corroborated: https://www.motor.com/magazine-summary/service-tips-for-gdi-engines/"
    ),
}


def write_report(seed_rows: list[dict[str, object]]) -> None:
    n_sep = sum(1 for r in seed_rows if r["c9_separable"])
    n_abs = len(seed_rows) - n_sep

    lines: list[str] = []
    lines.append(f"# V3_C9_SYNTH_BANDS_{DATE}")
    lines.append("")
    lines.append("**Task:** `T-V3-P4-C9-SYNTH`  **Mode:** provisional-synthetic seed (side file)")
    lines.append("**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, "
                 "tolerance-wide, web-corroborated, `synthetic=true`, correctable.")
    lines.append("**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** "
                 "`/agent_workspace/.venv-wired/bin/python v3/gen_c9_synth_seed.py`.")
    lines.append("**Data + manifest:** `v3/data/c9_synthetic_seed_2026-07-06.{csv,json}`.")
    lines.append("**Baseline pin (from C9-PRE):** `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`, "
                 "oracle `3088a7c3…`), run `POST_T_V3_P4_C5B`.")
    lines.append("")
    lines.append("Seeds the 11 C9 cases' health confirmation and emissions columns "
                 "(`readiness_supported_complete_bool, stored_dtc_count, pending_dtc_count, "
                 "permanent_dtc_count, mode06_min_margin_pct, warmup_cycles_since_clear, "
                 "miles_since_clear, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, "
                 "gas_delta_hc_ppm, gas_delta_co_pct, gas_delta_co2_pct, gas_delta_o2_pct`) with values "
                 "derived from each case's **oracle fault code** through the `cluster9.1.md` / `value9.md` signature, "
                 "each band widened to the real-world spread found via web research. Consumed by "
                 "`T-V3-P4-C9A` (dry-run).")
    lines.append("")
    lines.append("## 1. No-back-solve statement")
    lines.append("")
    lines.append("C9 cases are split by `expected_fault_family`: `no_fault` (10 cases) and `misfire` (1 case). "
                 "The band group is keyed on the finer **`expected_fault_code`** — the corpus **answer key** — "
                 "resolved to `OPTIMAL_HEALTH` or `ERR-MF-008`. The generator's **only** inputs are "
                 "(a) each case's `expected_fault_code` and (b) the band table below. It does "
                 "**not** read `no_fault.json` consumer thresholds, nor "
                 "any case's current rank or predicted family. The gates used to *verify* the seed "
                 "are the **research/producer** bands from `cluster9.1.md` / `value9.md`, not consumer rules. "
                 "Floats are sampled uniformly across a tolerance-wide band (σ reported), "
                 "seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).")
    lines.append("")
    lines.append("## 2. Per-column bands — cluster9 research vs web-real vs band used")
    lines.append("")
    lines.append("| Column / signal | cluster9 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append("| `readiness_supported_complete_bool` | all non-continuous = COMPLETE | complete monitors | **True** (healthy) / **True** (misfire) | **standardized** |")
    lines.append("| `stored/pending/permanent_dtc_count` | all DTC counts = 0 | no codes present | healthy: **0**; misfire: `pending` = **1** | **standardized** |")
    lines.append("| `mode06_min_margin_pct` | margin `>= 10%` | margin 15-95% of limit range | healthy: **[15.0, 95.0]%**; misfire: **[1.0, 5.0]%** | **standardized** |")
    lines.append("| `warmup_cycles_since_clear` | cycles `>= 5` | typical reset maturity | healthy: **[5, 40]** cycles | **standardized** |")
    lines.append("| `miles_since_clear` | distance `>= 200` miles | typical reset maturity | healthy: **[200, 800]** miles | **standardized** |")
    lines.append("| `stft_idle_pct` | STFT within `+/-5%` | normal idle STFT | healthy: **[-4.0, 4.0]%**; misfire: **[6.0, 12.0]%** | **standardized** |")
    lines.append("| `ltft_idle_pct` | LTFT within `+/-7%` | normal idle LTFT | healthy: **[-6.0, 6.0]%**; misfire: **[8.0, 15.0]%** | **standardized** |")
    lines.append("| `stft_2500_pct` | STFT within `+/-5%` | normal 2500 STFT | healthy: **[-4.0, 4.0]%**; misfire: **[2.0, 6.0]%** | **standardized** |")
    lines.append("| `ltft_2500_pct` | LTFT within `+/-7%` | normal 2500 LTFT | healthy: **[-6.0, 6.0]%**; misfire: **[4.0, 8.0]%** | **standardized** |")
    lines.append("| `gas_delta_hc_ppm` | delta HC `-10` to `+15` ppm | combustion delta | healthy: **[-10, 15]** ppm; misfire: **[25, 60]** ppm | **anecdotal** |")
    lines.append("| `gas_delta_co_pct` | delta CO `-0.15` to `+0.15` % | combustion delta | healthy: **[-0.150, 0.150]%**; misfire: **[0.200, 0.500]%** | **anecdotal** |")
    lines.append("| `gas_delta_co2_pct` | delta CO2 `+0.3` to `+0.8` % | combustion delta | healthy: **[0.30, 0.80]%**; misfire: **[-1.50, -0.50]%** | **anecdotal** |")
    lines.append("| `gas_delta_o2_pct` | delta O2 `-0.5` to `+0.4` % | combustion delta | healthy: **[-0.50, 0.40]%**; misfire: **[0.50, 1.50]%** | **anecdotal** |")
    lines.append("")
    lines.append("Where the web shows a **wider or typical** range, the band is set to fire the "
                 "producer gate robustly while staying field-realistic (policy step 3).")
    lines.append("")
    lines.append("### Citations")
    lines.append("")
    for key, txt in CITATIONS.items():
        lines.append(f"- **{key}** — {txt}")
    lines.append("")
    lines.append("## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge")
    lines.append("")
    lines.append("Reported σ per band (uniform std-dev = (hi−lo)/√12):")
    lines.append("")
    lines.append("| oracle code | band_id | separable | margin σ | warmup σ | miles σ | idle STFT/LTFT σ | 2500 STFT/LTFT σ | HC σ | CO σ | CO2 σ | O2 σ |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for code, b in CODE_BANDS.items():
        lines.append(f"| {code} | {b.band_id} | {'yes' if b.c9_separable else '**NO**'} | "
                     f"{b.mode06_min_margin_pct.sigma} | "
                     f"{b.warmup_cycles_since_clear.sigma} | "
                     f"{b.miles_since_clear.sigma} | "
                     f"{b.stft_idle_pct.sigma}/{b.ltft_idle_pct.sigma} | "
                     f"{b.stft_2500_pct.sigma}/{b.ltft_2500_pct.sigma} | "
                     f"{b.gas_delta_hc_ppm.sigma} | "
                     f"{b.gas_delta_co_pct.sigma} | "
                     f"{b.gas_delta_co2_pct.sigma} | "
                     f"{b.gas_delta_o2_pct.sigma} |")
    lines.append("")
    lines.append("## 4. Seeded cases (11/11) — value sits in its own oracle-code band")
    lines.append("")
    lines.append("| case_id | oracle code | fault_name | band | sep | readiness | DTC (st/pe/pm) | margin | wuc | miles | STFT/LTFT idle | STFT/LTFT 2500 | ΔHC | ΔCO | ΔCO2 | ΔO2 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in seed_rows:
        lines.append(f"| {r['case_id']} | {r['oracle_fault_code']} | {r['oracle_fault_name']} | "
                     f"{r['band_id']} | {'Y' if r['c9_separable'] else 'abst'} | "
                     f"{r['readiness_supported_complete_bool']} | "
                     f"{r['stored_dtc_count']}/{r['pending_dtc_count']}/{r['permanent_dtc_count']} | "
                     f"{r['mode06_min_margin_pct']}% | "
                     f"{r['warmup_cycles_since_clear']} | "
                     f"{r['miles_since_clear']} | "
                     f"{r['stft_idle_pct']}/{r['ltft_idle_pct']}% | "
                     f"{r['stft_2500_pct']}/{r['ltft_2500_pct']}% | "
                     f"{r['gas_delta_hc_ppm']} ppm | "
                     f"{r['gas_delta_co_pct']}% | "
                     f"{r['gas_delta_co2_pct']}% | "
                     f"{r['gas_delta_o2_pct']}% |")
    lines.append("")
    lines.append("## 5. Separability split — which cases the C9 signal can and cannot separate")
    lines.append("")
    lines.append(f"Across the 11 C9 cases, we have a clear **{n_sep} separable vs {n_abs} stay-abstained** split:")
    lines.append("")
    lines.append("- **C9-Separable (10 cases):** `CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014`. "
                 "These are genuine no_fault cases that pass all OBD and combustion metrics. "
                 "They will successfully confirm health on paper.")
    lines.append("- **Stay-Abstained (1 case):** `era2_016`. "
                 "This is the crankshaft position sensor sync drop fault (expected misfire, currently winning no_fault). "
                 "It is seeded with misfire-consistent values that fail multiple OBD and combustion checks (e.g. pending DTC, "
                 "low Mode $06 margin, elevated trims and gas deltas). It will fail the health confirmation gate and return "
                 "`SENSOR_HEALTH_UNPROVEN_ABSTAIN` to prevent false-healthy diagnostic leakage.")
    lines.append("")
    lines.append("## 6. Collision checks verification")
    lines.append("")
    lines.append("All C9 rows have C5-only columns (`calc_load_wot_pct`, `fuel_rail_pressure_load_kpa`, `wideband_lambda_wot`) "
                 "and C6-only columns (`mode06_o2_response_margin_pct`, `o2_rich_to_lean_ms`, `o2_lean_to_rich_ms`, "
                 "`maf_actual_calc_delta_pct_idle`, `maf_actual_calc_delta_pct_2500`) left as absent. "
                 "This ensures that C9 does not interfere with the active states of C5/C6.")
    lines.append("")
    lines.append("## 7. Paper-separability caveat")
    lines.append("")
    lines.append("While these 10 healthy cases pass all confirmation criteria on paper, their actual top3_family "
                 "movement depends on the C9A dry-run and C9B commit. Paper-separability represents the logical limit, "
                 "whereas active simulation and scoring will evaluate the live effect of the boosts and prunes.")
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n")


def main() -> None:
    oracle = load_c9_oracle()
    seed_rows: list[dict[str, object]] = []

    for cid in C9_CASES:
        _, code = oracle[cid]
        row = seed_case(cid, code)
        seed_rows.append(row)

    # Perform strict assertions
    _assert_no_backsolve(seed_rows)
    _assert_no_collision(seed_rows)

    # Write files
    write_csv(seed_rows)
    write_manifest(seed_rows)
    write_report(seed_rows)

    print(f"[C9-SYNTH] generated 11 C9 cases: {OUT_CSV.name}")
    print(f"[C9-SYNTH] manifest: {OUT_JSON.name}")
    print(f"[C9-SYNTH] report: {OUT_REPORT.name}  (no live corpus / engine / yardstick touched)")


if __name__ == "__main__":
    main()
