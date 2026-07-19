#!/usr/bin/env python3
"""Generate provisional synthetic C6 (sensor fault under-detection) seed data.

This is a side-file generator for T-V3-P4-C6-SYNTH. It writes only under v3/:

* v3/data/c6_synthetic_seed_2026-07-05.csv
* v3/data/c6_synthetic_seed_2026-07-05.json
* v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md

Inputs are deliberately narrow: the pinned C6 case list, each row's oracle
``expected_fault_code`` from the v7 corpus, and the band table below. The generator
never reads consumer rule JSON, runtime ranks, run traces, or current predictions.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
OUT_CSV = ROOT / "v3/data/c6_synthetic_seed_2026-07-05.csv"
OUT_JSON = ROOT / "v3/data/c6_synthetic_seed_2026-07-05.json"
OUT_REPORT = ROOT / "v3/reports/V3_C6_SYNTH_BANDS_2026-07-05.md"

DATE = "2026-07-05"

C6_CASES: tuple[str, ...] = (
    "CASE-045",
    "CASE-048",
    "YAML-TC46",
    "CASE-014",
    "EXT-229",
    "EXT-230",
    "YAML-CSV25",
    "case_046",
    "era1_006",
    "CSV-025",
    "EXP-N020",
    "PDF-4G-05",
    "TC-046",
    "era2_012",
)

# Research/producer gates from V3_C6_REVEAL_CONTRACT_2026-07-05 §2 / cluster6.md.
# These are used only for seed validation; they are not consumer-rule thresholds.
MODE06_SUSPICIOUS_MARGIN_MAX_PCT = 10.0
O2_RESPONSE_SLOW_MS = 600.0
MAF_UNDERREAD_MIN_SHORTFALL_PCT = -15.0
MAF_NORMAL_ABS_DELTA_MAX_PCT = 6.0


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
        return round((self.hi - self.lo) / (12.0**0.5), 3)


@dataclass(frozen=True)
class CodeBandInfo:
    """One oracle sub-fault code's C6 signal band group."""

    band_id: str
    fault_name: str
    emit_path: str
    c6_separable: bool
    stay_abstained: bool
    maf_applicable: bool
    o2_architecture: str
    signature: str
    mode06_o2_response_margin_pct: Band
    o2_rich_to_lean_ms: Band
    o2_lean_to_rich_ms: Band
    maf_actual_calc_delta_pct_idle: Band | None
    maf_actual_calc_delta_pct_2500: Band | None
    calc_airflow_gps_idle: Band | None
    calc_airflow_gps_2500: Band | None


# Web-corroborated, tolerance-wide band table keyed on ORACLE fault CODE.
# O2-fault groups fire only the O2-dynamics gates; the MAF-underread group fires only the
# MAF plausibility gates. The misfire lookalike is deliberately healthy on every C6 signal.
CODE_BANDS: dict[str, CodeBandInfo] = {
    "ERR-SF-001": CodeBandInfo(
        band_id="C6-O2-LAZY",
        fault_name="upstream_o2_sensor_lazy_response",
        emit_path="O2_LAZY_OR_BIASED",
        c6_separable=True,
        stay_abstained=False,
        maf_applicable=True,
        o2_architecture="switching-or-Mode06-OEM-monitor",
        signature=("Lazy/bias O2 sensor: vehicle Mode $06 margin is close to the stored limit "
                   "and active rich↔lean transitions are slow. MAF plausibility remains normal, "
                   "so C6A can ladder O2-only vs all-column scenarios."),
        mode06_o2_response_margin_pct=Band(2.0, 8.0, decimals=1),
        o2_rich_to_lean_ms=Band(650.0, 1100.0, decimals=0),
        o2_lean_to_rich_ms=Band(620.0, 1050.0, decimals=0),
        maf_actual_calc_delta_pct_idle=Band(-4.0, 4.0, decimals=1),
        maf_actual_calc_delta_pct_2500=Band(-4.0, 4.0, decimals=1),
        calc_airflow_gps_idle=Band(2.3, 3.7, decimals=2),
        calc_airflow_gps_2500=Band(8.5, 13.5, decimals=2),
    ),
    "ERR-SF-005": CodeBandInfo(
        band_id="C6-O2-IMPLAUSIBLE-NORMAL-CHEM",
        fault_name="sensor_fault_normal_operation",
        emit_path="O2_LAZY_OR_BIASED",
        c6_separable=True,
        stay_abstained=False,
        maf_applicable=True,
        o2_architecture="switching-or-Mode06-OEM-monitor",
        signature=("Normal gas chemistry with sensor-fault symptoms: the engine is chemically "
                   "healthy, but OBD sensor dynamics are implausible. Seed as O2 dynamics fault; "
                   "MAF branch remains normal."),
        mode06_o2_response_margin_pct=Band(3.0, 9.0, decimals=1),
        o2_rich_to_lean_ms=Band(700.0, 1200.0, decimals=0),
        o2_lean_to_rich_ms=Band(680.0, 1150.0, decimals=0),
        maf_actual_calc_delta_pct_idle=Band(-5.0, 5.0, decimals=1),
        maf_actual_calc_delta_pct_2500=Band(-5.0, 5.0, decimals=1),
        calc_airflow_gps_idle=Band(2.2, 3.8, decimals=2),
        calc_airflow_gps_2500=Band(8.0, 14.0, decimals=2),
    ),
    "ERR-SF-004": CodeBandInfo(
        band_id="C6-MAF-UNDERREAD",
        fault_name="sensor_fault_vvt_context",
        emit_path="MAF_UNDERREAD",
        c6_separable=True,
        stay_abstained=False,
        maf_applicable=True,
        o2_architecture="O2-dynamics-healthy",
        signature=("Sensor-fault/VVT-context lookalike carried by airflow rationality: O2 dynamics "
                   "stay healthy, while measured MAF is sustained >15% low against modeled airflow "
                   "at both warm idle and 2500 rpm."),
        mode06_o2_response_margin_pct=Band(35.0, 75.0, decimals=1),
        o2_rich_to_lean_ms=Band(90.0, 220.0, decimals=0),
        o2_lean_to_rich_ms=Band(90.0, 230.0, decimals=0),
        maf_actual_calc_delta_pct_idle=Band(-28.0, -18.0, decimals=1),
        maf_actual_calc_delta_pct_2500=Band(-27.0, -18.0, decimals=1),
        calc_airflow_gps_idle=Band(2.4, 3.9, decimals=2),
        calc_airflow_gps_2500=Band(9.0, 14.5, decimals=2),
    ),
    "ERR-MF-005": CodeBandInfo(
        band_id="C6-HEALTHY-LOOKALIKE-MISFIRE",
        fault_name="misfire_lookalike_pdf_4g_05",
        emit_path="SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        c6_separable=False,
        stay_abstained=True,
        maf_applicable=True,
        o2_architecture="C6-dynamics-healthy-lookalike",
        signature=("Named lookalike: oracle is misfire while the current engine says sensor_fault. "
                   "Seed all C6 dynamics healthy so C6 stops supporting the wrong sensor verdict; "
                   "the case remains for a misfire discriminator, not a C6 pass."),
        mode06_o2_response_margin_pct=Band(40.0, 80.0, decimals=1),
        o2_rich_to_lean_ms=Band(80.0, 210.0, decimals=0),
        o2_lean_to_rich_ms=Band(80.0, 220.0, decimals=0),
        maf_actual_calc_delta_pct_idle=Band(-3.0, 3.0, decimals=1),
        maf_actual_calc_delta_pct_2500=Band(-3.0, 3.0, decimals=1),
        calc_airflow_gps_idle=Band(2.2, 3.7, decimals=2),
        calc_airflow_gps_2500=Band(8.5, 13.5, decimals=2),
    ),
}

FLOAT_COLS = (
    "mode06_o2_response_margin_pct",
    "o2_rich_to_lean_ms",
    "o2_lean_to_rich_ms",
    "maf_actual_calc_delta_pct_idle",
    "maf_actual_calc_delta_pct_2500",
    "maf_gps_idle",
    "maf_gps_2500",
    "calc_airflow_gps_idle",
    "calc_airflow_gps_2500",
)
ALL_COLS = FLOAT_COLS

CITATIONS: dict[str, str] = {
    "mode06_monitor_framework": (
        "Mode $06 / J1979-style monitor reporting exposes recent monitor results and limits; "
        "the transport is standardized, but the numeric O2 response limit is manufacturer-"
        "specific. [standardized-transport / manufacturer-specific numeric limit] "
        "cluster6.md lines 114-115, 155, 171; CARB OBD II final regulation: "
        "https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf"
    ),
    "o2_response_direction": (
        "O2 deterioration is defined by delayed/slow response and activity loss; public sources "
        "support direction strongly but not a universal ms fail line. Seed uses wide slow bands "
        "(620-1200 ms) only as provisional synthetic evidence. [manufacturer-typical] "
        "cluster6.md lines 147-157; CARB OBD II final regulation: "
        "https://www.arb.ca.gov/regact/2015/obdii2015/finalregorder2.pdf"
    ),
    "maf_component_accuracy": (
        "Bosch HFM public data gives component-level accuracy/time response anchors; C6 widens "
        "the vehicle-level separator beyond component error and model uncertainty. "
        "[empirical-inferred] cluster6.md line 161; Bosch HFM2 datasheet mirror: "
        "https://www.farnell.com/datasheets/69647.pdf"
    ),
    "maf_contamination_rationality": (
        "DENSO describes MAF contamination/electronics effects that corrupt ECU load input, and "
        "trade diagnostic sources corroborate comparing measured MAF against an alternate modeled "
        "air path. [empirical-inferred / professional trade corroboration] "
        "https://www.denso-am.eu/products/engine-management-systems/mass-air-flow-sensors#textContent-33196; "
        "https://gearsmagazine.com/magazine/a-breath-of-fresh-air-8-pin-mass-airflow-sensors/"
    ),
    "static_rejected": (
        "Single static O2 voltage, AFR, or MAF magnitude is rejected; dynamic inconsistency or "
        "monitor/rationality evidence is required. [physics/regulatory rationale] "
        "cluster6.md lines 126-129, 188-193; V3_C6_REVEAL_CONTRACT_2026-07-05 §9"
    ),
}


def _rng_for(case_id: str) -> random.Random:
    digest = hashlib.sha256(case_id.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def load_c6_oracle() -> dict[str, tuple[str, str]]:
    """Return {case_id: (expected_fault_family, expected_fault_code)} for C6 cases."""
    want = set(C6_CASES)
    oracle: dict[str, tuple[str, str]] = {}
    with CORPUS.open(newline="") as fh:
        for row in csv.DictReader(fh):
            cid = row["case_id"]
            if cid in want:
                oracle[cid] = (row["expected_fault_family"], row["expected_fault_code"])
    missing = want - oracle.keys()
    if missing:
        raise SystemExit(f"C6 cases missing from corpus: {sorted(missing)}")
    return oracle


def _maf_actual(calc: float, delta_pct: float) -> float:
    return round(calc * (1.0 + delta_pct / 100.0), 2)


def seed_case(case_id: str, oracle_family: str, oracle_code: str) -> dict[str, object]:
    """Sample one case's synthetic C6 columns from its oracle CODE's band."""
    info = CODE_BANDS.get(oracle_code)
    if info is None:
        raise SystemExit(f"{case_id}: oracle code {oracle_code!r} has no C6 band")

    rng = _rng_for(case_id)
    mode_margin = info.mode06_o2_response_margin_pct.sample(rng)
    rich_to_lean = info.o2_rich_to_lean_ms.sample(rng)
    lean_to_rich = info.o2_lean_to_rich_ms.sample(rng)

    if info.maf_applicable:
        assert info.maf_actual_calc_delta_pct_idle is not None
        assert info.maf_actual_calc_delta_pct_2500 is not None
        assert info.calc_airflow_gps_idle is not None
        assert info.calc_airflow_gps_2500 is not None
        delta_idle = info.maf_actual_calc_delta_pct_idle.sample(rng)
        delta_2500 = info.maf_actual_calc_delta_pct_2500.sample(rng)
        calc_idle = info.calc_airflow_gps_idle.sample(rng)
        calc_2500 = info.calc_airflow_gps_2500.sample(rng)
        maf_idle = _maf_actual(calc_idle, delta_idle)
        maf_2500 = _maf_actual(calc_2500, delta_2500)
    else:
        delta_idle = None
        delta_2500 = None
        calc_idle = None
        calc_2500 = None
        maf_idle = None
        maf_2500 = None

    return {
        "case_id": case_id,
        "oracle_fault_family": oracle_family,
        "oracle_fault_code": oracle_code,
        "oracle_fault_name": info.fault_name,
        "band_id": info.band_id,
        "emit_path": info.emit_path,
        "c6_separable": info.c6_separable,
        "stay_abstained": info.stay_abstained,
        "maf_applicable": info.maf_applicable,
        "o2_architecture": info.o2_architecture,
        "synthetic": True,
        "mode06_o2_response_margin_pct": mode_margin,
        "o2_rich_to_lean_ms": rich_to_lean,
        "o2_lean_to_rich_ms": lean_to_rich,
        "maf_actual_calc_delta_pct_idle": delta_idle,
        "maf_actual_calc_delta_pct_2500": delta_2500,
        "maf_gps_idle": maf_idle,
        "maf_gps_2500": maf_2500,
        "calc_airflow_gps_idle": calc_idle,
        "calc_airflow_gps_2500": calc_2500,
    }


def _assert_no_backsolve(seed_rows: list[dict[str, object]]) -> None:
    """Reconcile membership and prove C6 bands fire/clear from producer limits only."""
    assert len(seed_rows) == 14, f"expected 14 C6 cases, got {len(seed_rows)}"
    seen = {str(r["case_id"]) for r in seed_rows}
    assert seen == set(C6_CASES), seen

    for r in seed_rows:
        code = str(r["oracle_fault_code"])
        info = CODE_BANDS[code]
        assert r["band_id"] == info.band_id, f"band mismatch {r['case_id']}"
        assert r["synthetic"] is True

        mode_margin = cast(float, r["mode06_o2_response_margin_pct"])
        rtl = cast(float, r["o2_rich_to_lean_ms"])
        ltr = cast(float, r["o2_lean_to_rich_ms"])
        maf_idle = cast(float | None, r["maf_actual_calc_delta_pct_idle"])
        maf_2500 = cast(float | None, r["maf_actual_calc_delta_pct_2500"])

        o2_gate = mode_margin <= MODE06_SUSPICIOUS_MARGIN_MAX_PCT or rtl >= O2_RESPONSE_SLOW_MS or ltr >= O2_RESPONSE_SLOW_MS
        maf_gate = (
            maf_idle is not None
            and maf_2500 is not None
            and maf_idle <= MAF_UNDERREAD_MIN_SHORTFALL_PCT
            and maf_2500 <= MAF_UNDERREAD_MIN_SHORTFALL_PCT
        )

        if info.emit_path == "O2_LAZY_OR_BIASED":
            assert info.c6_separable
            assert o2_gate, r
            assert not maf_gate, r
            assert maf_idle is not None and abs(maf_idle) <= MAF_NORMAL_ABS_DELTA_MAX_PCT, r
            assert maf_2500 is not None and abs(maf_2500) <= MAF_NORMAL_ABS_DELTA_MAX_PCT, r
        elif info.emit_path == "MAF_UNDERREAD":
            assert info.c6_separable
            assert not o2_gate, r
            assert maf_gate, r
        elif info.emit_path == "SENSOR_HEALTH_UNPROVEN_ABSTAIN":
            assert info.stay_abstained
            assert not o2_gate, r
            assert not maf_gate, r
            assert maf_idle is not None and abs(maf_idle) <= MAF_NORMAL_ABS_DELTA_MAX_PCT, r
            assert maf_2500 is not None and abs(maf_2500) <= MAF_NORMAL_ABS_DELTA_MAX_PCT, r
        else:
            raise AssertionError(f"unknown emit path {info.emit_path}")

        if not info.maf_applicable:
            for col in (
                "maf_actual_calc_delta_pct_idle",
                "maf_actual_calc_delta_pct_2500",
                "maf_gps_idle",
                "maf_gps_2500",
                "calc_airflow_gps_idle",
                "calc_airflow_gps_2500",
            ):
                assert r[col] is None, (r["case_id"], col, r[col])


def write_csv(seed_rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "case_id",
        "oracle_fault_family",
        "oracle_fault_code",
        "oracle_fault_name",
        "band_id",
        "emit_path",
        "c6_separable",
        "stay_abstained",
        "maf_applicable",
        "o2_architecture",
        "synthetic",
        *ALL_COLS,
    ]
    with OUT_CSV.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=cols)
        writer.writeheader()
        for row in seed_rows:
            writer.writerow({c: row[c] for c in cols})


def _float_band_json(band: Band | None) -> list[float] | None:
    if band is None:
        return None
    return [band.lo, band.hi, band.sigma]


def write_manifest(seed_rows: list[dict[str, object]]) -> None:
    manifest = {
        "task": "T-V3-P4-C6-SYNTH",
        "generated": DATE,
        "mode": "provisional-synthetic-seed (side file; live corpus untouched)",
        "policy": "4DLab_CLAUDE.md §Provisional synthetic signals",
        "baseline": {
            "yardstick": "V3_YARDSTICK_2026-07-05-C3B",
            "csv_hash": "9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283",
            "oracle_hash": "3088a7c3",
            "named_run": "POST_T_V3_P4_C3B",
        },
        "oracle_discriminator": (
            "13/14 C6 cases are expected_fault_family=sensor_fault, so bands are keyed on "
            "the finer corpus expected_fault_code; PDF-4G-05 is keyed as oracle misfire and "
            "seeded healthy on every C6 signal."
        ),
        "no_backsolve": (
            "generator inputs are only the pinned C6 case list, corpus oracle "
            "expected_fault_family/expected_fault_code, and this band table; it does not read "
            "sensor_fault/no_fault consumer thresholds, run traces, current ranks, or predictions"
        ),
        "producer_limits_cluster6": {
            "mode06_suspicious_margin_pct_max": MODE06_SUSPICIOUS_MARGIN_MAX_PCT,
            "o2_response_slow_ms_min": O2_RESPONSE_SLOW_MS,
            "maf_underread_shortfall_pct_at_both_points_max": MAF_UNDERREAD_MIN_SHORTFALL_PCT,
            "maf_normal_abs_delta_pct_max": MAF_NORMAL_ABS_DELTA_MAX_PCT,
        },
        "grounding_tags": {
            "mode06_o2_response_margin_pct": "standardized-transport / manufacturer-specific numeric limit",
            "o2_rich_to_lean_ms": "manufacturer-typical; direction strong, universal ms bound weak",
            "o2_lean_to_rich_ms": "manufacturer-typical; direction strong, universal ms bound weak",
            "maf_actual_calc_delta_pct_idle": "empirical-inferred; >10-15% low vs model, widened beyond component error",
            "maf_actual_calc_delta_pct_2500": "empirical-inferred; >10-15% low vs model, widened beyond component error",
            "maf_gps_idle": "derived synthetic from modeled airflow and delta; None when MAF is not applicable",
            "maf_gps_2500": "derived synthetic from modeled airflow and delta; None when MAF is not applicable",
            "calc_airflow_gps_idle": "modeled airflow support value; None when MAF is not applicable",
            "calc_airflow_gps_2500": "modeled airflow support value; None when MAF is not applicable",
        },
        "band_table": {
            code: {
                "band_id": band.band_id,
                "fault_name": band.fault_name,
                "emit_path": band.emit_path,
                "c6_separable": band.c6_separable,
                "stay_abstained": band.stay_abstained,
                "maf_applicable": band.maf_applicable,
                "o2_architecture": band.o2_architecture,
                "signature": band.signature,
                "float_bands": {
                    "mode06_o2_response_margin_pct": _float_band_json(band.mode06_o2_response_margin_pct),
                    "o2_rich_to_lean_ms": _float_band_json(band.o2_rich_to_lean_ms),
                    "o2_lean_to_rich_ms": _float_band_json(band.o2_lean_to_rich_ms),
                    "maf_actual_calc_delta_pct_idle": _float_band_json(band.maf_actual_calc_delta_pct_idle),
                    "maf_actual_calc_delta_pct_2500": _float_band_json(band.maf_actual_calc_delta_pct_2500),
                    "calc_airflow_gps_idle": _float_band_json(band.calc_airflow_gps_idle),
                    "calc_airflow_gps_2500": _float_band_json(band.calc_airflow_gps_2500),
                },
            }
            for code, band in CODE_BANDS.items()
        },
        "citations": CITATIONS,
        "cases": {str(r["case_id"]): r for r in seed_rows},
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n")


def _count_by(seed_rows: list[dict[str, object]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in seed_rows:
        value = str(row[key])
        counts[value] = counts.get(value, 0) + 1
    return counts


def write_report(seed_rows: list[dict[str, object]]) -> None:
    by_code = _count_by(seed_rows, "oracle_fault_code")
    by_emit = _count_by(seed_rows, "emit_path")
    n_sep = sum(1 for row in seed_rows if row["c6_separable"])
    n_abs = len(seed_rows) - n_sep
    maf_less = sum(1 for row in seed_rows if not row["maf_applicable"])

    lines: list[str] = []
    lines.append(f"# V3_C6_SYNTH_BANDS_{DATE}")
    lines.append("")
    lines.append("**Task:** `T-V3-P4-C6-SYNTH`  **Mode:** provisional-synthetic seed (side file)")
    lines.append("**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, tolerance-wide, web-corroborated, `synthetic=true`, correctable.")
    lines.append("**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** `/agent_workspace/.venv-wired/bin/python v3/gen_c6_synth_seed.py`.")
    lines.append("**Data + manifest:** `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}`.")
    lines.append("**Baseline pin (from C6-PRE):** `V3_YARDSTICK_2026-07-05-C3B` (csv `9f530695…`, oracle `3088a7c3…`), run `POST_T_V3_P4_C3B`.")
    lines.append("")
    lines.append("Seeds the 14 C6 cases' sensor-dynamics columns (`mode06_o2_response_margin_pct`, rich↔lean O2 timing, and two-point MAF actual-vs-calculated airflow) with values derived from each case's **oracle fault code** through the `cluster6.md` signature and C6-PRE contract. Consumed by `T-V3-P4-C6A` (dry-run) and `C6B` (commit).")
    lines.append("")
    lines.append("## 1. No-back-solve statement")
    lines.append("")
    lines.append("The generator's only data inputs are the pinned 14 C6 case IDs, each case's corpus oracle `expected_fault_family` / `expected_fault_code`, and the band table below. It does **not** read `sensor_fault.json`, `no_fault.json`, current ranks, predicted families, run traces, or any C6A/C6B consumer thresholds. The limits used in assertions are the **producer/research** limits from `cluster6.md` and `V3_C6_REVEAL_CONTRACT_2026-07-05.md`: Mode $06 margin relative to the vehicle limit, O2 response direction/slow timing, and MAF sustained >10–15% under-read at both points. Floats are sampled uniformly with a deterministic SHA-256-per-case seed; MAF g/s values are derived from modeled airflow and the sampled delta.")
    lines.append("")
    lines.append("## 2. Per-column bands — cluster6 research vs web-real vs band used")
    lines.append("")
    lines.append("| Column / signal | cluster6 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append("| `mode06_o2_response_margin_pct` | Use vehicle Mode $06 result vs stored min/max; low margin or exceeded limit emits O2_LAZY_OR_BIASED | monitor framework standardized; numeric limit vehicle-specific | O2-fault ∈ **[2, 9]%** margin (fires); healthy/MAF/misfire ∈ **[35, 80]%** | **standardized-transport / manufacturer-specific numeric limit** |")
    lines.append("| `o2_rich_to_lean_ms` | Longer-than-expected rich→lean response is positive evidence; not a universal ms line | CARB response-rate direction strong; example thresholds are OEM-specific | O2-fault ∈ **[650, 1200] ms**; healthy/MAF/misfire ∈ **[80, 220] ms** | **manufacturer-typical** |")
    lines.append("| `o2_lean_to_rich_ms` | Longer-than-expected lean→rich response is positive evidence; not a universal ms line | public evidence supports slow transition direction, not fleet threshold | O2-fault ∈ **[620, 1150] ms**; healthy/MAF/misfire ∈ **[80, 230] ms** | **manufacturer-typical** |")
    lines.append("| `maf_actual_calc_delta_pct_idle` | Sustained measured-MAF shortfall >10–15% vs modeled airflow at warm idle | Bosch HFM accuracy ±4%; vehicle-level screen widened beyond model/VE uncertainty | MAF-underread ∈ **[-28, -18]%** (fires); others ∈ **[-5, +5]%** | **empirical-inferred** |")
    lines.append("| `maf_actual_calc_delta_pct_2500` | Sustained measured-MAF shortfall >10–15% vs modeled airflow at 2500 rpm | same; must persist at both points | MAF-underread ∈ **[-27, -18]%** (fires); others ∈ **[-5, +5]%** | **empirical-inferred** |")
    lines.append("| `maf_gps_idle`, `maf_gps_2500` | source g/s supporting the delta | MAF is fast/accurate when healthy but contamination can bias reading | derived from `calc_airflow * (1 + delta/100)`; None only when MAF not applicable | **derived / correctable** |")
    lines.append("| `calc_airflow_gps_idle`, `calc_airflow_gps_2500` | modeled-airflow reference path | alternate MAP/RPM/IAT/BARO path corroborates MAF rationality | idle modeled **[2.2, 3.9] g/s**; 2500 modeled **[8.0, 14.5] g/s** | **empirical-inferred support** |")
    lines.append("")
    lines.append("### Citations")
    lines.append("")
    for key, value in CITATIONS.items():
        lines.append(f"- **{key}** — {value}")
    lines.append("")
    lines.append("## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge")
    lines.append("")
    lines.append("Worst-case corners: O2-fault Mode $06 high corner = **9% ≤ 10%** and O2 response low corner = **620 ms ≥ 600 ms**; MAF-underread high corner = **-18% ≤ -15%** at both points; healthy/lookalike O2 response high corner = **230 ms < 600 ms**, Mode $06 low corner = **35% > 10%**, and healthy MAF deltas stay within ±5%. Reported σ uses uniform std-dev `(hi−lo)/√12`.")
    lines.append("")
    lines.append("| oracle code | band_id | emit path | separable | MAF applicable | Mode06 σ | R→L σ | L→R σ | MAF idle σ | MAF 2500 σ |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for code, band in CODE_BANDS.items():
        idle_sigma = "None" if band.maf_actual_calc_delta_pct_idle is None else str(band.maf_actual_calc_delta_pct_idle.sigma)
        rpm_sigma = "None" if band.maf_actual_calc_delta_pct_2500 is None else str(band.maf_actual_calc_delta_pct_2500.sigma)
        lines.append(f"| {code} | {band.band_id} | {band.emit_path} | {'yes' if band.c6_separable else '**NO**'} | {band.maf_applicable} | {band.mode06_o2_response_margin_pct.sigma} | {band.o2_rich_to_lean_ms.sigma} | {band.o2_lean_to_rich_ms.sigma} | {idle_sigma} | {rpm_sigma} |")
    lines.append("")
    lines.append("## 4. Seeded cases (14/14) — value sits in its own oracle-code band")
    lines.append("")
    lines.append("| case_id | oracle code | fault_name | band | emit | sep | Mode06 % | R→L ms | L→R ms | MAF Δ idle % | MAF Δ 2500 % | MAF g/s idle | calc g/s idle | MAF g/s 2500 | calc g/s 2500 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in seed_rows:
        lines.append(f"| {row['case_id']} | {row['oracle_fault_code']} | {row['oracle_fault_name']} | {row['band_id']} | {row['emit_path']} | {'Y' if row['c6_separable'] else 'abst'} | {row['mode06_o2_response_margin_pct']} | {row['o2_rich_to_lean_ms']} | {row['o2_lean_to_rich_ms']} | {row['maf_actual_calc_delta_pct_idle']} | {row['maf_actual_calc_delta_pct_2500']} | {row['maf_gps_idle']} | {row['calc_airflow_gps_idle']} | {row['maf_gps_2500']} | {row['calc_airflow_gps_2500']} |")
    lines.append("")
    lines.append("## 5. Separability split — which cases the C6 signal can and cannot separate")
    lines.append("")
    lines.append(f"Oracle-code split: **{by_code}**. Emit-path split: **{by_emit}**. MAF-less/speed-density modeled cases: **{maf_less}**; if later vehicle identity marks any row speed-density, this generator already preserves the invariant by writing `None` to all MAF columns for `maf_applicable=false` bands.")
    lines.append("")
    lines.append(f"- **C6-SEPARABLE ({n_sep}):** `ERR-SF-001` + `ERR-SF-005` use the O2 dynamics path (`O2_LAZY_OR_BIASED`): low Mode $06 margin and slow rich↔lean response, with normal MAF plausibility. `ERR-SF-004` uses the MAF path (`MAF_UNDERREAD`): healthy O2 dynamics, but sustained >15% measured-MAF shortfall at both idle and 2500 rpm. These are synthetic C6A inputs only, not live accuracy wins.")
    lines.append(f"- **STAY-ABSTAINED ({n_abs}):** `PDF-4G-05` (`ERR-MF-005`) is the named lookalike from the task: oracle `misfire`, current engine `sensor_fault`. It is seeded below every C6 gate (healthy Mode $06 margin, healthy O2 timing, healthy MAF deltas) so C6 stops supporting the wrong sensor verdict; it remains for a misfire discriminator. **{n_sep} + {n_abs} = 14.** ✔")
    lines.append("")
    lines.append("> **Never read synthetic-seeded passes as real-world accuracy.** The manifest `synthetic=true` and downstream synthetic-vs-real split keep these correctable. Mode $06 numeric limits are manufacturer-specific, O2 ms bands are manufacturer-typical rather than universal, and MAF shortfall is empirical-inferred until validated on real vehicles.")
    lines.append("")
    lines.append("## Provenance / guardrails")
    lines.append("")
    lines.append("- Side file only: no write to `cases_petrol_v7.csv`, no engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.")
    lines.append("- Inputs: corpus oracle `expected_fault_family` / `expected_fault_code` for the pinned 14 `C6_CASES` + the band table above. Producer thresholds cited to `v3/research/research_answers/cluster6.md` and `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md`. Governs `T-V3-P4-C6A` / `C6B`.")
    lines.append("- Live web fetch note: the session attempted the mandated firecrawl path; CLI was not installed, then installed, but reported unauthenticated. This report therefore cites the already-landed, web-corroborated `cluster6.md` source set and its primary URLs rather than adding scratch `.firecrawl/` artifacts.")
    lines.append("")
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines))


def main() -> None:
    oracle = load_c6_oracle()
    seed_rows = [seed_case(cid, family, code) for cid, (family, code) in sorted(oracle.items())]
    _assert_no_backsolve(seed_rows)

    write_csv(seed_rows)
    write_manifest(seed_rows)
    write_report(seed_rows)

    separable = sum(1 for row in seed_rows if row["c6_separable"])
    print(f"[C6-SYNTH] seeded {len(seed_rows)}/14 cases  ->  {OUT_CSV.name}, {OUT_JSON.name}")
    print(f"[C6-SYNTH] oracle-code split: {_count_by(seed_rows, 'oracle_fault_code')}")
    print(f"[C6-SYNTH] emit-path split: {_count_by(seed_rows, 'emit_path')}")
    print(f"[C6-SYNTH] C6-separable: {separable}; stay-abstained: {len(seed_rows) - separable}")
    print(f"[C6-SYNTH] report: {OUT_REPORT.name}  (no live corpus / engine / yardstick touched)")


if __name__ == "__main__":
    main()
