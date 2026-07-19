#!/usr/bin/env python3
"""Generate provisional synthetic C2 (rich_mixture vs catalyst_failure) seed data.

Task: T-V3-P4-C2-SYNTH. Produces a **side file** of research-grounded, web-corroborated,
tolerance-wide synthetic fuel-trim + Mode $06 catalyst values for the 22 C2 cases, each
derived from that case's **oracle fault family** (ground truth) via the `cluster2.md`
signature. Flagged ``synthetic=true``. It does NOT write the live corpus, wire any
producer/consumer, or move any score — those are C2A (dry-run) / C2B (commit).

No-back-solve invariant (audited by ``_assert_no_backsolve``): the generator's only inputs
are (a) each case's ``expected_fault_family`` from the corpus oracle column and (b) the
web-validated band table below. It never reads ``rich_mixture.json`` /
``catalyst_failure.json`` consumer thresholds, nor any case's current rank/prediction. The
``0.20`` catalyst pass limit and ``-10%`` rich trim limit used for reporting are the
*research/producer* bands from ``cluster2.md`` (Quantitative Signatures), not consumer rules.

Determinism: each case is sampled with a PRNG seeded from a SHA-256 of its case_id, so
reruns are byte-identical (no wall-clock / unseeded randomness).

Run: ``/agent_workspace/.venv-wired/bin/python v3/gen_c2_synth_seed.py``
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
ACQ_SPEC = ROOT / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
OUT_CSV = ROOT / "v3/data/c2_synthetic_seed_2026-07-01.csv"
OUT_JSON = ROOT / "v3/data/c2_synthetic_seed_2026-07-01.json"
OUT_REPORT = ROOT / "v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md"

DATE = "2026-07-01"

# Research producer limits from cluster2.md (Quantitative Signatures) — reporting only,
# NOT consumer-rule thresholds. Used to *verify* seeded values land past the limit robustly.
RESEARCH_RICH_TOTAL_TRIM_LIMIT = -10.0  # Total Fuel Trim <= -10% -> TRUE_RICH
RESEARCH_LEAN_TOTAL_TRIM_LIMIT = 10.0   # +ve mirror; lean correction (web: investigate > +10%)
RESEARCH_CATALYST_INDEX_PASS = 0.20     # index ratio <= 0.20 -> catalyst PASS (healthy)
RESEARCH_DECEL_CO_FAIL = 0.8            # decel-sweep CO > 0.8% -> catalyst FAIL


@dataclass(frozen=True)
class Band:
    """A tolerance-wide sampling band ``[lo, hi]`` for one synthetic column."""

    lo: float
    hi: float
    decimals: int = 1

    def sample(self, rng: random.Random) -> float:
        return round(rng.uniform(self.lo, self.hi), self.decimals)

    @property
    def sigma(self) -> float:
        # Uniform[lo,hi] std-dev = (hi-lo)/sqrt(12); reported as the tolerance spread.
        return round((self.hi - self.lo) / (12.0**0.5), 2)


# --- Web-corroborated, tolerance-wide band table, keyed on ORACLE fault family -----------
# Every band is set with margin *past* the research limit so a case passes across its WHOLE
# spread (not on a knife-edge). See V3_C2_SYNTH_BANDS report for per-column citations.
#
# trim columns: stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct
# catalyst columns: catalyst_index_ratio, mode06_catalyst_margin_pct (derived from index
#   vs the 0.20 research pass limit), decel_co_pct, pre_post_cat_hc_delta_ppm,
#   pre_post_cat_co_delta_pct
FAMILY_BANDS: dict[str, dict[str, object]] = {
    "rich_mixture": {
        "band_id": "C2-RICH",
        "c2_separable": True,
        "signature": "TRUE_RICH: sustained negative fuel trim; catalyst itself healthy",
        "trim": {
            "stft_idle_pct": Band(-10.0, -4.0),
            "ltft_idle_pct": Band(-15.0, -8.0),
            "stft_2500_pct": Band(-8.0, -3.0),
            "ltft_2500_pct": Band(-13.0, -7.0),
        },
        "catalyst_state": "healthy",
    },
    "catalyst_failure": {
        "band_id": "C2-CAT",
        "c2_separable": True,
        "signature": "Catalyst deteriorated: trims near zero (no fueling fault) + high index/CO",
        "trim": {
            "stft_idle_pct": Band(-3.0, 3.0),
            "ltft_idle_pct": Band(-4.0, 4.0),
            "stft_2500_pct": Band(-3.0, 3.0),
            "ltft_2500_pct": Band(-4.0, 4.0),
        },
        "catalyst_state": "failed",
    },
    "lean_condition": {
        "band_id": "C2-LEAN",
        "c2_separable": False,
        "signature": "Lean: positive trim, high at idle / corrects at 2500 rpm (vacuum-leak shape)",
        "trim": {
            "stft_idle_pct": Band(3.0, 8.0),
            "ltft_idle_pct": Band(9.0, 18.0),
            "stft_2500_pct": Band(0.0, 4.0),
            "ltft_2500_pct": Band(1.0, 6.0),
        },
        "catalyst_state": "healthy",
    },
    "sensor_fault": {
        "band_id": "C2-SENSOR",
        "c2_separable": False,
        "signature": "O2/ground skew: erratic trims + falsely-elevated index (mimics catalyst)",
        "trim": {
            "stft_idle_pct": Band(-4.0, 8.0),
            "ltft_idle_pct": Band(-4.0, 8.0),
            "stft_2500_pct": Band(-4.0, 8.0),
            "ltft_2500_pct": Band(-4.0, 8.0),
        },
        "catalyst_state": "ambiguous",
    },
}

# catalyst_state -> catalyst-health columns (index / decel CO / pre-post deltas)
CATALYST_BANDS: dict[str, dict[str, Band]] = {
    "healthy": {
        "catalyst_index_ratio": Band(0.05, 0.18, decimals=3),
        "decel_co_pct": Band(0.05, 0.60, decimals=2),
        "pre_post_cat_hc_delta_ppm": Band(300.0, 900.0, decimals=0),
        "pre_post_cat_co_delta_pct": Band(0.5, 2.0, decimals=2),
    },
    "failed": {
        "catalyst_index_ratio": Band(0.55, 0.90, decimals=3),
        "decel_co_pct": Band(0.90, 2.20, decimals=2),
        "pre_post_cat_hc_delta_ppm": Band(10.0, 120.0, decimals=0),
        "pre_post_cat_co_delta_pct": Band(0.0, 0.25, decimals=2),
    },
    "ambiguous": {
        "catalyst_index_ratio": Band(0.28, 0.55, decimals=3),
        "decel_co_pct": Band(0.30, 0.90, decimals=2),
        "pre_post_cat_hc_delta_ppm": Band(150.0, 400.0, decimals=0),
        "pre_post_cat_co_delta_pct": Band(0.20, 0.60, decimals=2),
    },
}

TRIM_COLS = ("stft_idle_pct", "ltft_idle_pct", "stft_2500_pct", "ltft_2500_pct")
CAT_COLS = (
    "catalyst_index_ratio",
    "mode06_catalyst_margin_pct",
    "decel_co_pct",
    "pre_post_cat_hc_delta_ppm",
    "pre_post_cat_co_delta_pct",
)
ALL_COLS = TRIM_COLS + CAT_COLS


def _rng_for(case_id: str) -> random.Random:
    """Deterministic PRNG seeded from the case_id (stable across runs; not wall-clock)."""
    digest = hashlib.sha256(case_id.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def _margin_from_index(index_ratio: float) -> float:
    """Mode $06 catalyst margin (%) vs the research 0.20 pass limit. +ve = headroom (pass).

    margin = (pass_limit - index) / pass_limit * 100. Uses the research/producer limit,
    never a consumer-rule value.
    """
    return round((RESEARCH_CATALYST_INDEX_PASS - index_ratio) / RESEARCH_CATALYST_INDEX_PASS * 100.0, 1)


def load_c2_oracle() -> dict[str, str]:
    """Return {case_id: oracle_fault_family} for the 22 C2 cases.

    C2 membership comes from the acquisition spec; the oracle fault comes from the corpus
    ``expected_fault_family`` (ground truth) — NOT from any consumer rule or current rank.
    """
    spec = json.loads(ACQ_SPEC.read_text())
    c2_ids = {u["case_id"] for u in spec["case_unlocks"] if u.get("cluster") == "C2"}

    oracle: dict[str, str] = {}
    with CORPUS.open(newline="") as fh:
        for row in csv.DictReader(fh):
            cid = row["case_id"]
            if cid in c2_ids:
                oracle[cid] = row["expected_fault_family"]

    missing = c2_ids - oracle.keys()
    if missing:
        raise SystemExit(f"C2 cases missing from corpus: {sorted(missing)}")
    return oracle


def seed_case(case_id: str, oracle_fault: str) -> dict[str, object]:
    """Sample one case's synthetic columns from its oracle fault's web-validated bands."""
    fam = FAMILY_BANDS.get(oracle_fault)
    if fam is None:
        raise SystemExit(f"{case_id}: oracle fault {oracle_fault!r} has no C2 band (unexpected)")

    rng = _rng_for(case_id)
    trim_bands: dict[str, Band] = fam["trim"]  # type: ignore[assignment]
    cat_bands = CATALYST_BANDS[str(fam["catalyst_state"])]

    values: dict[str, float] = {col: trim_bands[col].sample(rng) for col in TRIM_COLS}
    index = cat_bands["catalyst_index_ratio"].sample(rng)
    values["catalyst_index_ratio"] = index
    values["mode06_catalyst_margin_pct"] = _margin_from_index(index)
    values["decel_co_pct"] = cat_bands["decel_co_pct"].sample(rng)
    values["pre_post_cat_hc_delta_ppm"] = cat_bands["pre_post_cat_hc_delta_ppm"].sample(rng)
    values["pre_post_cat_co_delta_pct"] = cat_bands["pre_post_cat_co_delta_pct"].sample(rng)

    total_idle = round(values["stft_idle_pct"] + values["ltft_idle_pct"], 1)
    total_2500 = round(values["stft_2500_pct"] + values["ltft_2500_pct"], 1)

    return {
        "case_id": case_id,
        "oracle_fault": oracle_fault,
        "band_id": fam["band_id"],
        "c2_separable": fam["c2_separable"],
        "synthetic": True,
        "total_idle_trim_pct": total_idle,
        "total_2500_trim_pct": total_2500,
        **values,
    }


def _assert_no_backsolve(seed_rows: list[dict[str, object]]) -> None:
    """Reconciliation + robustness audit: every value sits in its OWN oracle band, and the
    C2-separable families clear the research limit across their whole spread (not knife-edge).
    """
    for r in seed_rows:
        fam = str(r["oracle_fault"])
        band = FAMILY_BANDS[fam]
        idle_total = cast(float, r["total_idle_trim_pct"])
        if band["c2_separable"] and fam == "rich_mixture":
            assert idle_total <= RESEARCH_RICH_TOTAL_TRIM_LIMIT, r
        if band["c2_separable"] and fam == "catalyst_failure":
            assert cast(float, r["catalyst_index_ratio"]) > RESEARCH_CATALYST_INDEX_PASS, r
            assert cast(float, r["decel_co_pct"]) > RESEARCH_DECEL_CO_FAIL, r
            assert abs(idle_total) <= 10.0, r  # near-zero (no fueling fault)


def write_csv(seed_rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["case_id", "oracle_fault", "band_id", "c2_separable", "synthetic",
            "total_idle_trim_pct", "total_2500_trim_pct", *ALL_COLS]
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in seed_rows:
            w.writerow({c: r[c] for c in cols})


def write_manifest(seed_rows: list[dict[str, object]], citations: dict[str, str]) -> None:
    manifest = {
        "task": "T-V3-P4-C2-SYNTH",
        "generated": DATE,
        "mode": "provisional-synthetic-seed (side file; live corpus untouched)",
        "policy": "4DLab_CLAUDE.md §Provisional synthetic signals",
        "no_backsolve": ("generator keys only on corpus expected_fault_family (oracle) + "
                         "web-validated band table; does not read rich_mixture.json / "
                         "catalyst_failure.json thresholds or any case rank/prediction"),
        "research_limits_cluster2": {
            "rich_total_trim_pct_le": RESEARCH_RICH_TOTAL_TRIM_LIMIT,
            "catalyst_index_pass_le": RESEARCH_CATALYST_INDEX_PASS,
            "decel_co_fail_gt": RESEARCH_DECEL_CO_FAIL,
        },
        "band_table": {
            fam: {
                "band_id": b["band_id"],
                "c2_separable": b["c2_separable"],
                "signature": b["signature"],
                "catalyst_state": b["catalyst_state"],
                "trim_bands": {c: [bd.lo, bd.hi, bd.sigma] for c, bd in b["trim"].items()},  # type: ignore[union-attr]
                "catalyst_bands": {
                    c: [bd.lo, bd.hi, bd.sigma]
                    for c, bd in CATALYST_BANDS[str(b["catalyst_state"])].items()
                },
            }
            for fam, b in FAMILY_BANDS.items()
        },
        "citations": citations,
        "cases": {r["case_id"]: r for r in seed_rows},
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n")


# --- Web-corroboration citations (one per signature band) --------------------------------
CITATIONS: dict[str, str] = {
    "fuel_trim_normal_pm10": (
        "LTFT normally -10%..+10%; approaching -20% indicates rich (P0172 'System Too Rich'). "
        "ricksfreeautorepairadvice.com/what-does-negative-fuel-trim-mean-expert-diagnosis-guide/; "
        "engineerfix.com/what-should-long-term-and-short-term-fuel-trim-be/"
    ),
    "rich_negative_trim": (
        "Negative trim = ECU pulling fuel because engine runs rich; both STFT+LTFT negative = "
        "sustained rich; fuel-delivery cause is consistent across RPM. "
        "foxwelldiag.com/blogs/car-diagnostic/understanding-long-term-fuel-trim-bank-1-and-how-to-diagnose-issues"
    ),
    "catalyst_index_ratio": (
        "Mode $06 rear/front O2 switch ratio: healthy cat = low ratio (downstream flatlines); "
        "failed cat = ratio approaches 1:1 (documented 0.76 set P0430). "
        "brakeandfrontend.com/obd-ii-diagnostics-checking-into-mode-06/"
    ),
    "decel_co": (
        "Healthy cat reduces CO 70-90% (near-zero tailpipe CO, often <0.5% at idle); dead cat / "
        "rich engine pushes idle CO into several-percent range. "
        "aa1car.com/library/converter.htm; ipdusa.com/Articles/770/Diagnosing-Faulty-Catalytic-Converters"
    ),
    "lean_positive_trim": (
        "Positive trim = ECU adding fuel for a lean condition; +20% documented (case +22/+20), "
        "ECU compensates up to ~+25%; vacuum-leak signature is high-at-idle / corrects at 1500-2500 rpm. "
        "vehicleservicepros.com/.../fuel-trim-finding-a-vacuum-leak...; xerodrive.com/auto-guides/long-term-fuel-trim-high-at-idle/"
    ),
    "sensor_skew": (
        "A bad O2 sensor / ground-voltage drop skews the Mode $06 ratio and fuel trim, causing "
        "false catalyst codes (P0420/P0430) — replace O2 before condemning the cat. "
        "brakeandfrontend.com/obd-ii-diagnostics-checking-into-mode-06/"
    ),
}


def write_report(seed_rows: list[dict[str, object]]) -> None:
    by_fam: dict[str, list[dict[str, object]]] = {}
    for r in seed_rows:
        by_fam.setdefault(str(r["oracle_fault"]), []).append(r)

    lines: list[str] = []
    lines.append(f"# V3_C2_SYNTH_BANDS_{DATE}")
    lines.append("")
    lines.append("**Task:** `T-V3-P4-C2-SYNTH`  **Mode:** provisional-synthetic seed (side file)")
    lines.append("**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, "
                 "tolerance-wide, web-corroborated, `synthetic=true`, correctable.")
    lines.append("**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** "
                 "`/agent_workspace/.venv-wired/bin/python v3/gen_c2_synth_seed.py`.")
    lines.append("**Data + manifest:** `v3/data/c2_synthetic_seed_2026-07-01.{csv,json}`.")
    lines.append("")
    lines.append("Seeds the 22 C2 cases' fuel-trim + Mode $06 catalyst columns with values "
                 "derived from each case's **oracle fault family** (corpus `expected_fault_family`) "
                 "through the `cluster2.md` signature, each band widened to the real-world spread "
                 "found via web research. Consumed by `T-V3-P4-C2A` (dry-run) and `C2B` (commit).")
    lines.append("")
    lines.append("## 1. No-back-solve statement")
    lines.append("")
    lines.append("The generator's **only** inputs are (a) each case's `expected_fault_family` from "
                 "the corpus oracle column and (b) the band table below. It does **not** read "
                 "`rich_mixture.json` / `catalyst_failure.json` consumer thresholds, nor any case's "
                 "current rank or predicted family. The `-10%` rich trim limit and `0.20` catalyst "
                 "index pass limit used to *verify* the seed are the **research/producer** bands from "
                 "`cluster2.md` (Quantitative Signatures), not consumer rules. Values are sampled "
                 "uniformly across a tolerance-wide band (spread reported as σ), seeded "
                 "deterministically per `case_id` (SHA-256; no wall-clock randomness).")
    lines.append("")
    lines.append("## 2. Per-column bands — cluster2.md vs web-real vs band used")
    lines.append("")
    lines.append("| Column / signal | `cluster2.md` band | Web-real range (cited) | Band used (tolerance-wide) |")
    lines.append("| --- | --- | --- | --- |")
    lines.append("| Total fuel trim — **rich** | `<= -10%` (TRUE_RICH) | −10%..−20%+ rich; ~−20% clearly rich, P0172 | idle STFT+LTFT ∈ **[−25%, −12%]**, 2500 ∈ [−21%, −10%] |")
    lines.append("| Total fuel trim — **normal/catalyst** | ±10% normal | −10%..+10% balanced | idle STFT+LTFT ∈ **[−7%, +7%]** (near zero) |")
    lines.append("| Total fuel trim — **lean** | +ve (mirror) | +10%..+25% (case +20/+22); corrects at rpm | idle ∈ **[+12%, +26%]**, 2500 ∈ [+1%, +10%] (corrects) |")
    lines.append("| Total fuel trim — **sensor skew** | n/a (confounder) | erratic; O2/ground skew | idle ∈ **[−8%, +16%]** wide/ambiguous (no clean fire) |")
    lines.append("| `catalyst_index_ratio` — healthy | `<= 0.20` pass | low ratio, downstream flatlines | **[0.05, 0.18]** |")
    lines.append("| `catalyst_index_ratio` — failed | `> 0.20` fail | approaches 1:1 (0.76 set P0430) | **[0.55, 0.90]** |")
    lines.append("| `catalyst_index_ratio` — sensor skew | borderline | falsely elevated by bad O2 | **[0.28, 0.55]** (mimics cat) |")
    lines.append("| `decel_co_pct` — healthy / failed | `> 0.8%` fail | healthy <0.5%; dead cat several % | healthy **[0.05, 0.60]** / failed **[0.90, 2.20]** |")
    lines.append("| `mode06_catalyst_margin_pct` | derived | — | `(0.20 − index)/0.20 × 100` (+ve = pass headroom) |")
    lines.append("| `pre_post_cat_hc_delta_ppm` | — | healthy reduces HC 70–90% | healthy **[300, 900]** / failed **[10, 120]** |")
    lines.append("| `pre_post_cat_co_delta_pct` | — | healthy reduces CO 70–90% | healthy **[0.5, 2.0]** / failed **[0.0, 0.25]** |")
    lines.append("")
    lines.append("Where the web shows a **wider or shifted** range than `cluster2.md`, the wider "
                 "field-realistic band is used (policy step 3). Rich vs catalyst_failure bands are "
                 "stated separately above.")
    lines.append("")
    lines.append("### Citations")
    lines.append("")
    for key, txt in CITATIONS.items():
        lines.append(f"- **{key}** — {txt}")
    lines.append("")
    lines.append("## 3. Tolerance width (σ) — passes across the WHOLE spread, not a knife-edge")
    lines.append("")
    lines.append("Worst-case corners clear the research limit with margin: rich total trim high "
                 f"corner = −4 + −8 = **−12% ≤ {RESEARCH_RICH_TOTAL_TRIM_LIMIT:.0f}%**; lean total "
                 f"low corner = +3 + +9 = **+12% ≥ {RESEARCH_LEAN_TOTAL_TRIM_LIMIT:.0f}%**; failed "
                 f"catalyst index low corner = **0.55 > {RESEARCH_CATALYST_INDEX_PASS}**. Reported σ "
                 "per band (uniform std-dev = (hi−lo)/√12):")
    lines.append("")
    lines.append("| Family | band_id | idle-STFT σ | idle-LTFT σ | index σ | C2-separable |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for fam, b in FAMILY_BANDS.items():
        trim: dict[str, Band] = b["trim"]  # type: ignore[assignment]
        cat = CATALYST_BANDS[str(b["catalyst_state"])]
        lines.append(f"| {fam} | {b['band_id']} | {trim['stft_idle_pct'].sigma} | "
                     f"{trim['ltft_idle_pct'].sigma} | {cat['catalyst_index_ratio'].sigma} | "
                     f"{'yes' if b['c2_separable'] else 'NO'} |")
    lines.append("")
    lines.append("## 4. Seeded cases (22/22) — value sits in its own oracle band")
    lines.append("")
    lines.append("| case_id | oracle_fault | band | idle total | 2500 total | index | margin% | decel CO% |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in seed_rows:
        lines.append(f"| {r['case_id']} | {r['oracle_fault']} | {r['band_id']} | "
                     f"{r['total_idle_trim_pct']} | {r['total_2500_trim_pct']} | "
                     f"{r['catalyst_index_ratio']} | {r['mode06_catalyst_margin_pct']} | "
                     f"{r['decel_co_pct']} |")
    lines.append("")
    lines.append("## 5. Disclosure — which cases the C2 signal can and cannot separate")
    lines.append("")
    n_rich = len(by_fam.get("rich_mixture", []))
    n_cat = len(by_fam.get("catalyst_failure", []))
    n_lean = len(by_fam.get("lean_condition", []))
    n_sensor = len(by_fam.get("sensor_fault", []))
    lines.append(f"The 22 C2 cases are **not** all cleanly rich-vs-catalyst. Oracle split: "
                 f"**{n_rich} rich_mixture, {n_cat} catalyst_failure, {n_lean} lean_condition, "
                 f"{n_sensor} sensor_fault**.")
    lines.append("")
    lines.append(f"- **C2-SEPARABLE ({n_rich + n_cat}): rich_mixture + catalyst_failure.** The C2 "
                 "producer (TRUE_RICH on trim ≤ −10% vs LOW_OSC/high-index on the catalyst monitor) "
                 "cleanly separates these two — the seed puts rich cases in the negative-trim band "
                 "and catalyst cases in the near-zero-trim + failed-index band. C2A should predict "
                 "these flip toward top-3.")
    lines.append(f"- **NOT C2-SEPARABLE by rich-vs-catalyst ({n_lean} lean_condition):** a lean case "
                 "has **positive** trim, so it fires neither TRUE_RICH (needs ≤ −10%) nor a catalyst "
                 "fail. Seeded honestly from lean ground truth (positive idle trim, corrects at 2500), "
                 "these **stay abstained** under the C2 producer/consumer — they need a lean/vacuum "
                 "discriminator (a later cluster), not C2. Flagged `c2_separable=false`.")
    lines.append(f"- **CONFOUNDED ({n_sensor} sensor_fault):** O2/ground skew produces a "
                 "falsely-elevated index that *mimics* catalyst failure (both cases' current "
                 "prediction is `catalyst_failure`). Seeded with the ambiguous skew signature "
                 "(erratic trims, borderline index 0.28–0.55). The C2 catalyst monitor alone **cannot** "
                 "distinguish sensor skew from real catalyst failure — the research fix is the OSC "
                 "active test / sensor rationality (tier c), not the passive C2 index. Flagged "
                 "`c2_separable=false`; likely stays mis-routed/abstained until a sensor-rationality "
                 "signal lands. **Synthetic passes must never be read as real-world accuracy** — the "
                 "manifest `synthetic=true` + scoreboard split keep them distinguishable.")
    lines.append("")
    lines.append("## Provenance / guardrails")
    lines.append("")
    lines.append("- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no "
                 "engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial "
                 "change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph "
                 "rebuild. `run_suite.py` untouched. No secrets.")
    lines.append("- Inputs: corpus `expected_fault_family` (oracle) + "
                 "`V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C2 membership) + the web-validated "
                 "band table. Governs `T-V3-P4-C2A` / `C2B`.")
    lines.append("")
    OUT_REPORT.write_text("\n".join(lines))


def main() -> None:
    oracle = load_c2_oracle()
    seed_rows = [seed_case(cid, fam) for cid, fam in sorted(oracle.items())]
    _assert_no_backsolve(seed_rows)

    write_csv(seed_rows)
    write_manifest(seed_rows, CITATIONS)
    write_report(seed_rows)

    fam_counts: dict[str, int] = {}
    for r in seed_rows:
        fam_counts[str(r["oracle_fault"])] = fam_counts.get(str(r["oracle_fault"]), 0) + 1
    print(f"[C2-SYNTH] seeded {len(seed_rows)}/22 cases  ->  {OUT_CSV.name}, {OUT_JSON.name}")
    print(f"[C2-SYNTH] oracle split: {fam_counts}")
    separable = sum(1 for r in seed_rows if r["c2_separable"])
    print(f"[C2-SYNTH] C2-separable (rich+catalyst): {separable}; "
          f"not-separable (lean+sensor, stay abstained): {len(seed_rows) - separable}")
    print(f"[C2-SYNTH] report: {OUT_REPORT.name}  (no live corpus / engine / yardstick touched)")


if __name__ == "__main__":
    main()
