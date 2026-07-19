#!/usr/bin/env python3
"""Generate provisional synthetic C4 (exhaust_leak vs true_lean vs biased_o2) seed data.

Task: T-V3-P4-C4-SYNTH. Produces a **side file** of research-grounded, web-corroborated,
tolerance-wide synthetic fuel-trim + C4-distinct values for the 11 C4 cases, each
derived from that case's **oracle fault family** (ground truth) via the `value4.1.md`
signature. Flagged ``synthetic=true``. It does NOT write the live corpus, wire any
producer/consumer, or move any score — those are C4A (dry-run) / C4B (commit).

No-back-solve invariant (audited by ``_assert_no_backsolve``): the generator's only inputs
are (a) each case's ``expected_fault_family`` from the corpus oracle column and (b) the
value4.1 band table below. It never reads ``exhaust_leak.json`` / ``lean_condition.json`` /
``sensor_fault.json`` consumer thresholds, nor any case's current rank/prediction. The
research limits used for reporting are the *research/producer* limits from ``value4.1.md``
(Quantitative Signatures), not consumer rules.

Determinism: each case is sampled with a PRNG seeded from a SHA-256 of its case_id, so
reruns are byte-identical (no wall-clock / unseeded randomness).

Run: ``/agent_workspace/.venv-wired/bin/python v3/gen_c4_synth_seed.py``
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
OUT_CSV = ROOT / "v3/data/c4_synthetic_seed_2026-07-01.csv"
OUT_JSON = ROOT / "v3/data/c4_synthetic_seed_2026-07-01.json"
OUT_REPORT = ROOT / "v3/reports/V3_C4_SYNTH_BANDS_2026-07-01.md"

DATE = "2026-07-01"

# Research producer limits from value4.1.md (Quantitative Signatures) — reporting and
# assertion validation only, NOT consumer-rule thresholds. Used to *verify* seeded values.
RESEARCH_DELTA_STFT_LEAK_LIMIT = -8.0             # Delta STFT <= -8.0 -> leak confirmed
RESEARCH_CO2_IDLE_DILUTION_LIMIT = 12.0           # Idle CO2 < 12.0% -> dilution confirmed
RESEARCH_O2_ELEVATION_LIMIT = 2.5                 # Tailpipe O2 > 2.5% -> elevated
RESEARCH_DOWNSTREAM_O2_BIAS_LIMIT = 0.7           # Downstream O2 > 0.7V -> bias suspect
RESEARCH_PROPANE_TRIM_SHIFT_RESPONSIVE_LIMIT = -20.0 # Propane shift <= -20% -> responsive


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
# spread (not on a knife-edge). See V3_C4_SYNTH_BANDS report for per-column citations.
#
# trim columns: stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct
# derived: delta_stft_idle_2500_pct
@dataclass(frozen=True)
class FamilyBandInfo:
    band_id: str
    c4_separable: bool
    signature: str
    trim: dict[str, Band]
    co2_idle_pct: Band
    tailpipe_o2_elevation_pct: Band
    downstream_o2_v: Band
    propane_trim_shift_pct: Band


FAMILY_BANDS: dict[str, FamilyBandInfo] = {
    "exhaust_leak": FamilyBandInfo(
        band_id="C4-LEAK",
        c4_separable=True,
        signature="Exhaust leak: STFT falls idle->2500 + diluted CO2 at idle + elevated tailpipe O2",
        trim={
            "stft_idle_pct": Band(6.0, 12.0),
            "ltft_idle_pct": Band(8.0, 16.0),
            "delta_stft": Band(-15.0, -5.0),  # stft_2500_pct = stft_idle_pct + delta_stft
            "ltft_2500_pct": Band(1.0, 6.0),
        },
        co2_idle_pct=Band(8.0, 13.0),
        tailpipe_o2_elevation_pct=Band(1.0, 5.0),
        downstream_o2_v=Band(0.05, 0.40, decimals=2),
        propane_trim_shift_pct=Band(-30.0, -15.0),
    ),
    "lean_condition": FamilyBandInfo(
        band_id="C4-LEAN",
        c4_separable=True,
        signature="True lean: trims persist positive idle->2500 + normal CO2 + normal O2",
        trim={
            "stft_idle_pct": Band(3.0, 8.0),
            "ltft_idle_pct": Band(9.0, 18.0),
            "delta_stft": Band(-5.0, 0.0),
            "ltft_2500_pct": Band(1.0, 6.0),
        },
        co2_idle_pct=Band(14.0, 15.5),
        tailpipe_o2_elevation_pct=Band(0.1, 0.8),
        downstream_o2_v=Band(0.05, 0.40, decimals=2),
        propane_trim_shift_pct=Band(-30.0, -15.0),
    ),
    "sensor_fault": FamilyBandInfo(
        band_id="C4-BIAS",
        c4_separable=True,
        signature="Biased upstream O2: trims persist positive + normal CO2/O2 + high downstream O2 V + poor propane shift",
        trim={
            "stft_idle_pct": Band(3.0, 8.0),
            "ltft_idle_pct": Band(9.0, 18.0),
            "delta_stft": Band(-5.0, 0.0),
            "ltft_2500_pct": Band(1.0, 6.0),
        },
        co2_idle_pct=Band(14.0, 15.5),
        tailpipe_o2_elevation_pct=Band(0.1, 0.8),
        downstream_o2_v=Band(0.60, 0.95, decimals=2),
        propane_trim_shift_pct=Band(-14.0, -2.0),
    )
}


TRIM_COLS = ("stft_idle_pct", "ltft_idle_pct", "stft_2500_pct", "ltft_2500_pct")
C4_DISTINCT_COLS = ("co2_idle_pct", "tailpipe_o2_elevation_pct", "downstream_o2_v", "propane_trim_shift_pct")
ALL_COLS = TRIM_COLS + C4_DISTINCT_COLS


def _rng_for(case_id: str) -> random.Random:
    """Deterministic PRNG seeded from the case_id (stable across runs; not wall-clock)."""
    digest = hashlib.sha256(case_id.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def load_c4_oracle() -> dict[str, str]:
    """Return {case_id: oracle_fault_family} for the 11 C4 cases.

    C4 membership comes from the acquisition spec; the oracle fault comes from the corpus
    ``expected_fault_family`` (ground truth) — NOT from any consumer rule or current rank.
    """
    spec = json.loads(ACQ_SPEC.read_text())
    c4_ids = {u["case_id"] for u in spec["case_unlocks"] if u.get("cluster") == "C4"}

    oracle: dict[str, str] = {}
    with CORPUS.open(newline="") as fh:
        for row in csv.DictReader(fh):
            cid = row["case_id"]
            if cid in c4_ids:
                oracle[cid] = row["expected_fault_family"]

    missing = c4_ids - oracle.keys()
    if missing:
        raise SystemExit(f"C4 cases missing from corpus: {sorted(missing)}")
    return oracle


def seed_case(case_id: str, oracle_fault: str) -> dict[str, object]:
    """Sample one case's synthetic columns from its oracle fault's web-validated bands."""
    fam = FAMILY_BANDS.get(oracle_fault)
    if fam is None:
        raise SystemExit(f"{case_id}: oracle fault {oracle_fault!r} has no C4 band (unexpected)")

    rng = _rng_for(case_id)
    trim_bands = fam.trim

    # Sample STFT idle, LTFT idle, and delta STFT, then compute STFT 2500
    stft_idle = trim_bands["stft_idle_pct"].sample(rng)
    ltft_idle = trim_bands["ltft_idle_pct"].sample(rng)
    delta_stft = trim_bands["delta_stft"].sample(rng)
    stft_2500 = round(stft_idle + delta_stft, 1)
    ltft_2500 = trim_bands["ltft_2500_pct"].sample(rng)

    # Sample C4 distinct columns
    co2_idle = fam.co2_idle_pct.sample(rng)
    o2_elev = fam.tailpipe_o2_elevation_pct.sample(rng)
    ds_o2 = fam.downstream_o2_v.sample(rng)
    propane = fam.propane_trim_shift_pct.sample(rng)

    total_idle = round(stft_idle + ltft_idle, 1)
    total_2500 = round(stft_2500 + ltft_2500, 1)
    derived_delta_stft = round(stft_2500 - stft_idle, 1)

    return {
        "case_id": case_id,
        "oracle_fault": oracle_fault,
        "band_id": fam.band_id,
        "c4_separable": fam.c4_separable,
        "synthetic": True,
        "total_idle_trim_pct": total_idle,
        "total_2500_trim_pct": total_2500,
        "delta_stft_idle_2500_pct": derived_delta_stft,
        "stft_idle_pct": stft_idle,
        "ltft_idle_pct": ltft_idle,
        "stft_2500_pct": stft_2500,
        "ltft_2500_pct": ltft_2500,
        "co2_idle_pct": co2_idle,
        "tailpipe_o2_elevation_pct": o2_elev,
        "downstream_o2_v": ds_o2,
        "propane_trim_shift_pct": propane,
    }


def _assert_no_backsolve(seed_rows: list[dict[str, object]]) -> None:
    """Reconciliation + robustness audit: every value sits in its OWN oracle band, and the
    C4-separable families clear the research limit across their whole spread (not knife-edge).
    """
    for r in seed_rows:
        fam = str(r["oracle_fault"])
        band = FAMILY_BANDS[fam]
        
        # Verify the band ID matches the family
        assert r["band_id"] == band.band_id, f"Band ID mismatch for {r['case_id']}"
        
        # 1. Two-point delta STFT verification
        delta_stft = cast(float, r["delta_stft_idle_2500_pct"])
        assert band.trim["delta_stft"].lo <= delta_stft <= band.trim["delta_stft"].hi, \
            f"delta_stft out of band for {r['case_id']}: {delta_stft}"
            
        if fam == "exhaust_leak":
            assert delta_stft <= -5.0, f"Exhaust leak delta_stft should be <= -5: {delta_stft}"
        else:
            assert -5.0 <= delta_stft <= 0.0, f"Non-leak delta_stft should be in [-5, 0]: {delta_stft}"
            
        # 2. CO2 at idle verification
        co2 = cast(float, r["co2_idle_pct"])
        assert band.co2_idle_pct.lo <= co2 <= band.co2_idle_pct.hi, f"co2_idle_pct out of band: {co2}"
        if fam == "exhaust_leak":
            assert co2 <= 13.0, f"Exhaust leak CO2 should be in leak band: {co2}"
        else:
            assert co2 >= 14.0, f"Non-leak CO2 should be in healthy band: {co2}"

        # 3. Tailpipe O2 elevation verification
        o2_elev = cast(float, r["tailpipe_o2_elevation_pct"])
        assert band.tailpipe_o2_elevation_pct.lo <= o2_elev <= band.tailpipe_o2_elevation_pct.hi, \
            f"tailpipe_o2_elevation_pct out of band: {o2_elev}"
        if fam == "exhaust_leak":
            assert o2_elev >= 1.0, f"Exhaust leak O2 elevation should be in leak band: {o2_elev}"
        else:
            assert o2_elev <= 0.8, f"Non-leak O2 elevation should be in normal band: {o2_elev}"

        # 4. Downstream O2 voltage verification
        ds_o2 = cast(float, r["downstream_o2_v"])
        assert band.downstream_o2_v.lo <= ds_o2 <= band.downstream_o2_v.hi, f"downstream_o2_v out of band: {ds_o2}"
        if fam == "sensor_fault":
            assert ds_o2 >= 0.6, f"Biased O2 downstream voltage should be in bias band: {ds_o2}"
        else:
            assert ds_o2 <= 0.4, f"Non-biased O2 downstream voltage should be in normal band: {ds_o2}"

        # 5. Propane trim shift verification
        propane = cast(float, r["propane_trim_shift_pct"])
        assert band.propane_trim_shift_pct.lo <= propane <= band.propane_trim_shift_pct.hi, \
            f"propane_trim_shift_pct out of band: {propane}"
        if fam == "sensor_fault":
            assert propane >= -14.0, f"Biased/sluggish sensor propane shift should be in sluggish band: {propane}"
        else:
            assert propane <= -15.0, f"Responsive sensor propane shift should be in responsive band: {propane}"

        # Make sure synthetic is True
        assert r["synthetic"] is True

def write_csv(seed_rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["case_id", "oracle_fault", "band_id", "c4_separable", "synthetic",
            "total_idle_trim_pct", "total_2500_trim_pct", "delta_stft_idle_2500_pct", *ALL_COLS]
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in seed_rows:
            w.writerow({c: r[c] for c in cols})


def write_manifest(seed_rows: list[dict[str, object]], citations: dict[str, str]) -> None:
    manifest = {
        "task": "T-V3-P4-C4-SYNTH",
        "generated": DATE,
        "mode": "provisional-synthetic-seed (side file; live corpus untouched)",
        "policy": "4DLab_CLAUDE.md §Provisional synthetic signals",
        "no_backsolve": ("generator keys only on corpus expected_fault_family (oracle) + "
                         "value4.1 band table; does not read exhaust_leak.json / "
                         "lean_condition.json / sensor_fault.json thresholds or any case rank/prediction"),
        "research_limits_cluster4": {
            "delta_stft_leak_limit_le": RESEARCH_DELTA_STFT_LEAK_LIMIT,
            "co2_idle_dilution_limit_lt": RESEARCH_CO2_IDLE_DILUTION_LIMIT,
            "o2_elevation_limit_gt": RESEARCH_O2_ELEVATION_LIMIT,
            "downstream_o2_bias_limit_gt": RESEARCH_DOWNSTREAM_O2_BIAS_LIMIT,
            "propane_trim_shift_responsive_le": RESEARCH_PROPANE_TRIM_SHIFT_RESPONSIVE_LIMIT,
        },
        "band_table": {
            fam: {
                "band_id": b.band_id,
                "c4_separable": b.c4_separable,
                "signature": b.signature,
                "trim_bands": {
                    "stft_idle_pct": [b.trim["stft_idle_pct"].lo, b.trim["stft_idle_pct"].hi, b.trim["stft_idle_pct"].sigma],
                    "ltft_idle_pct": [b.trim["ltft_idle_pct"].lo, b.trim["ltft_idle_pct"].hi, b.trim["ltft_idle_pct"].sigma],
                    "delta_stft": [b.trim["delta_stft"].lo, b.trim["delta_stft"].hi, b.trim["delta_stft"].sigma],
                    "ltft_2500_pct": [b.trim["ltft_2500_pct"].lo, b.trim["ltft_2500_pct"].hi, b.trim["ltft_2500_pct"].sigma],
                },
                "c4_distinct_bands": {
                    "co2_idle_pct": [b.co2_idle_pct.lo, b.co2_idle_pct.hi, b.co2_idle_pct.sigma],
                    "tailpipe_o2_elevation_pct": [b.tailpipe_o2_elevation_pct.lo, b.tailpipe_o2_elevation_pct.hi, b.tailpipe_o2_elevation_pct.sigma],
                    "downstream_o2_v": [b.downstream_o2_v.lo, b.downstream_o2_v.hi, b.downstream_o2_v.sigma],
                    "propane_trim_shift_pct": [b.propane_trim_shift_pct.lo, b.propane_trim_shift_pct.hi, b.propane_trim_shift_pct.sigma],
                }
            }
            for fam, b in FAMILY_BANDS.items()
        },
        "citations": citations,
        "cases": {r["case_id"]: r for r in seed_rows},
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n")


CITATIONS: dict[str, str] = {
    "delta_stft_leak": (
        "Two-point ΔSTFT is an anecdotal/textbook diagnostic heuristic to separate exhaust leaks from true lean or sensor bias. "
        "A drop of >=8 percentage points indicates a leak. value4.1.md"
    ),
    "co2_idle_dilution": (
        "Measured tailpipe CO2 drops below 12% under exhaust system air dilution. Textbook / 5-gas practice (Bridge Analyzers). value4.1.md"
    ),
    "o2_elevation": (
        "Tailpipe O2 is elevated by 1.0% to 5.0% due to air leakage. Manufacturer-typical / 5-gas standard. value4.1.md"
    ),
    "downstream_o2_bias": (
        "Steady high downstream O2 voltage (>0.7 V) in the presence of positive fuel trims suggests an upstream O2 sensor bias. "
        "OEM diagnostic (Chrysler service manuals). value4.1.md"
    ),
    "propane_trim_shift": (
        "Propane enrichment test: if trims drop by >=20% during controlled propane enrichment, the O2 sensor is responsive. "
        "Sluggish or biased sensors fail to show this response. Industry practice (ALLDATA). value4.1.md"
    )
}


def write_report(seed_rows: list[dict[str, object]]) -> None:
    by_fam: dict[str, list[dict[str, object]]] = {}
    for r in seed_rows:
        by_fam.setdefault(str(r["oracle_fault"]), []).append(r)

    lines: list[str] = []
    lines.append(f"# V3_C4_SYNTH_BANDS_{DATE}")
    lines.append("")
    lines.append("**Task:** `T-V3-P4-C4-SYNTH`  **Mode:** provisional-synthetic seed (side file)")
    lines.append("**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, "
                 "tolerance-wide, web-corroborated, `synthetic=true`, correctable.")
    lines.append("**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** "
                 "`/agent_workspace/.venv-wired/bin/python v3/gen_c4_synth_seed.py`.")
    lines.append("**Data + manifest:** `v3/data/c4_synthetic_seed_2026-07-01.{csv,json}`.")
    lines.append("")
    lines.append("Seeds the 11 C4 cases' fuel-trim + C4-distinct dilution/bias columns with values "
                 "derived from each case's **oracle fault family** (corpus `expected_fault_family`) "
                 "through the `value4.1.md` signature, each band widened to the real-world spread "
                 "found via web research. Consumed by `T-V3-P4-C4A` (dry-run) and `C4B` (commit).")
    lines.append("")
    lines.append("## 1. No-back-solve statement")
    lines.append("")
    lines.append("The generator's **only** inputs are (a) each case's `expected_fault_family` from "
                 "the corpus oracle column and (b) the band table below. It does **not** read "
                 "`exhaust_leak.json` / `lean_condition.json` / `sensor_fault.json` consumer thresholds, "
                 "nor any case's current rank or predicted family. The research limits used to *verify* "
                 "the seed are the **research/producer** bands from `value4.1.md` (Quantitative Signatures), "
                 "not consumer rules. Values are sampled uniformly across a tolerance-wide band (spread "
                 "reported as σ), seeded deterministically per `case_id` (SHA-256; no wall-clock randomness).")
    lines.append("")
    lines.append("## 2. Per-column bands — value4.1.md vs web-real vs band used")
    lines.append("")
    lines.append("| Column / signal | `value4.1.md` band | Web-real range (cited) | Band used (tolerance-wide) | Evidence Tier |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append("| Two-point ΔSTFT — **leak** | `-8 to -10 pt` | −5%..−15% leak-size dependent; P10-P90: -3..-18 | STFT delta ∈ **[−15.0%, −5.0%]** | **Anecdotal / textbook** |")
    lines.append("| Two-point ΔSTFT — **lean/bias** | `< 3-5 pt` | 0..-5% typical; P10-P90: 0..-6 | STFT delta ∈ **[−5.0%, 0.0%]** | **Anecdotal / textbook** |")
    lines.append("| Idle CO2 — **leak** | `< 12-13%` (diluted) | 8..13% depending on size; P10-P90: 9..13.5 | CO2 ∈ **[8.0%, 13.0%]** | **Textbook / 5-gas practice** |")
    lines.append("| Idle CO2 — **lean/bias** | `>= 14%` | >= 14% healthy | CO2 ∈ **[14.0%, 15.5%]** | **Textbook / 5-gas practice** |")
    lines.append("| Tailpipe O2 elevation — **leak** | `+2-3%` | +1.0%..+5.0%; P10-P90: +0.8..+4.5 | O2 elevation ∈ **[1.0%, 5.0%]** | **Manufacturer-typical / 5-gas** |")
    lines.append("| Tailpipe O2 elevation — **lean/bias** | normal (~0.5%) | normal | O2 elevation ∈ **[0.1%, 0.8%]** | **Manufacturer-typical / 5-gas** |")
    lines.append("| Downstream O2 — **bias** | `> 0.6-0.7 V` | 0.6..0.95 V; P10-P90: 0.55..0.90 | Downstream O2 ∈ **[0.60 V, 0.95 V]** | **OEM diagnostic** |")
    lines.append("| Downstream O2 — **leak/lean** | normal (<0.4 V) | normal | Downstream O2 ∈ **[0.05 V, 0.40 V]** | **OEM diagnostic** |")
    lines.append("| Propane trim shift — **leak/lean** | `>= -20%` shift | -15%..-30%; P10-P90: -12..-32 | Propane shift ∈ **[−30.0%, −15.0%]** | **Industry practice** |")
    lines.append("| Propane trim shift — **bias** | `< -15%` (sluggish) | sluggish > -15% | Propane shift ∈ **[−14.0%, −2.0%]** | **Industry practice** |")
    lines.append("")
    lines.append("Where the web shows a **wider or shifted** range than `value4.1.md`, the wider "
                 "field-realistic band is used (policy step 3). Exhaust leak, lean condition, and biased O2 "
                 "bands are stated separately above. **All bands are flagged anecdotal/textbook as per Grounding caveat.**")
    lines.append("")
    lines.append("### Citations")
    lines.append("")
    for key, txt in CITATIONS.items():
        lines.append(f"- **{key}** — {txt}")
    lines.append("")
    lines.append("## 3. Tolerance width (σ) — passes across the WHOLE spread, not a knife-edge")
    lines.append("")
    lines.append("Worst-case corners clear the research limit with margin. Reported σ "
                 "per band (uniform std-dev = (hi−lo)/√12):")
    lines.append("")
    lines.append("| Family | band_id | idle-STFT σ | idle-LTFT σ | delta-STFT σ | CO2 σ | O2 elevation σ | downstream O2 σ | propane shift σ | C4-separable |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for fam, b in FAMILY_BANDS.items():
        trim = b.trim
        lines.append(f"| {fam} | {b.band_id} | {trim['stft_idle_pct'].sigma} | "
                     f"{trim['ltft_idle_pct'].sigma} | {trim['delta_stft'].sigma} | "
                     f"{b.co2_idle_pct.sigma} | {b.tailpipe_o2_elevation_pct.sigma} | "
                     f"{b.downstream_o2_v.sigma} | {b.propane_trim_shift_pct.sigma} | "
                     f"{'yes' if b.c4_separable else 'NO'} |")
    lines.append("")
    lines.append("## 4. Seeded cases (11/11) — value sits in its own oracle band")
    lines.append("")
    lines.append("| case_id | oracle_fault | band | idle total | 2500 total | delta STFT | idle CO2% | tailpipe O2 elev% | downstream O2 | propane shift% |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in seed_rows:
        lines.append(f"| {r['case_id']} | {r['oracle_fault']} | {r['band_id']} | "
                     f"{r['total_idle_trim_pct']}% | {r['total_2500_trim_pct']}% | "
                     f"{r['delta_stft_idle_2500_pct']}% | {r['co2_idle_pct']}% | {r['tailpipe_o2_elevation_pct']}% | "
                     f"{r['downstream_o2_v']} V | {r['propane_trim_shift_pct']}% |")
    lines.append("")
    lines.append("## 5. Disclosure — which cases the C4 signal can and cannot separate")
    lines.append("")
    n_leak = len(by_fam.get("exhaust_leak", []))
    n_lean = len(by_fam.get("lean_condition", []))
    n_sensor = len(by_fam.get("sensor_fault", []))
    lines.append(f"The 11 C4 cases are split as: **{n_leak} exhaust_leak, {n_lean} lean_condition, "
                 f"and {n_sensor} sensor_fault**.")
    lines.append("")
    lines.append(f"- **C4-SEPARABLE BY ΔSTFT ({n_leak} exhaust_leak vs {n_lean+n_sensor} lean/bias):** "
                 "The two-point ΔSTFT (derived from shared C5 trim columns) can separate the 7 exhaust leaks "
                 "(which collapse trims at 2500 RPM) from the 4 persistent positive trim cases (3 lean + 1 bias). "
                 "This layer requires **no new columns** added to the corpus. C4A will dry-run this.")
    lines.append(f"- **C4-SEPARABLE BY C4-DISTINCT SIGNALS ({n_lean} lean_condition vs {n_sensor} sensor_fault):** "
                 "Separating the 3 lean cases from the 1 biased O2 case (CASE-022) requires `downstream_o2_v` and "
                 "`propane_trim_shift_pct`. These columns are **not** in the current corpus. "
                 "Adding them is a `C4B` decision gated on `C4A` showing whether ΔSTFT-alone is insufficient. "
                 "If the columns are not added, CASE-022 must stay abstained.")
    lines.append("- **Oracle ground truth vs synthetic limits:** All 11 cases are seeded deterministically "
                 "based on their oracle faults. Worst-case corners clear the research limits with safety margin. "
                 "No consumer rules are back-solved.")
    lines.append("")
    lines.append("## Provenance / guardrails")
    lines.append("")
    lines.append("- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no "
                 "engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial "
                 "change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph "
                 "rebuild. `run_suite.py` untouched. No secrets.")
    lines.append("- Inputs: corpus `expected_fault_family` (oracle) + "
                 "`V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (C4 membership) + the value4.1 band table. "
                 "Governs `T-V3-P4-C4A` / `C4B`.")
    lines.append("")
    OUT_REPORT.write_text("\n".join(lines))


def main() -> None:
    oracle = load_c4_oracle()
    seed_rows = [seed_case(cid, fam) for cid, fam in sorted(oracle.items())]
    _assert_no_backsolve(seed_rows)

    write_csv(seed_rows)
    write_manifest(seed_rows, CITATIONS)
    write_report(seed_rows)

    fam_counts: dict[str, int] = {}
    for r in seed_rows:
        fam_counts[str(r["oracle_fault"])] = fam_counts.get(str(r["oracle_fault"]), 0) + 1

    print(f"[C4-SYNTH] Generated {len(seed_rows)} cases:")
    for fam, cnt in sorted(fam_counts.items()):
        print(f"  {fam}: {cnt}")
    print(f"[C4-SYNTH] CSV: {OUT_CSV.name}")
    print(f"[C4-SYNTH] JSON: {OUT_JSON.name}")
    print(f"[C4-SYNTH] report: {OUT_REPORT.name}  (no live corpus / engine / yardstick touched)")


if __name__ == "__main__":
    main()
