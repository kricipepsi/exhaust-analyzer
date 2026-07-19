#!/usr/bin/env python3
"""Generate provisional synthetic C3 (ECU/control-system fault) seed data.

Task: T-V3-P4-C3-SYNTH. Produces a **side file** of research-grounded, web-corroborated,
tolerance-wide synthetic control-plausibility values for the 22 C3 cases, each derived from
that case's **oracle fault code** (ground truth) via the `cluster3_prepped.md` signature.
Flagged ``synthetic=true``. It does NOT write the live corpus, wire any producer/consumer,
or move any score — those are C3A (dry-run) / C3B (commit).

No-back-solve invariant (audited by ``_assert_no_backsolve``): the generator's only inputs
are (a) each case's ``expected_fault_code`` from the corpus oracle column and (b) the
web-validated band table below. It never reads ``ecu_fault.json`` / ``sensor_fault.json``
consumer thresholds, nor any case's current rank/prediction. The research limits used for
reporting/verification are the *research/producer* limits from ``cluster3_prepped.md``
(Quantitative Diagnostic Signature Mapping, lines 183-188), not consumer rules.

All 22 C3 cases share ``expected_fault_family = ecu_fault``; the discriminating band group
therefore comes from the finer ``expected_fault_code`` (the answer key), resolved to a
registry ``fault_name`` for readability. Five sub-faults map to bands:
  ERR-EF-006 ecu_fault_lean_bias   -> ground-offset (ΔV_gnd) + gas-vs-OBD divergence  [separable]
  ERR-EF-007 ecu_fault_rich_bias   -> 5V-ref/MAP over-voltage (KOEO split) + divergence [separable]
  ERR-ECU-001 ecu_internal_processor_fault (P0606) -> bidirectional unresponsive + low Vbatt [separable]
  ERR-EF-002 ecu_fault_poa_context -> oil-burning POA gas signature (physical confounder) [STAY-ABSTAINED]
  ERR-EF-008 ecu_fault_intermittent -> fault not active at test (no signal in one snapshot) [STAY-ABSTAINED]

Determinism: each case is sampled with a PRNG seeded from a SHA-256 of its case_id, so
reruns are byte-identical (no wall-clock / unseeded randomness).

Run: ``/agent_workspace/.venv-wired/bin/python v3/gen_c3_synth_seed.py``
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
OUT_CSV = ROOT / "v3/data/c3_synthetic_seed_2026-07-05.csv"
OUT_JSON = ROOT / "v3/data/c3_synthetic_seed_2026-07-05.json"
OUT_REPORT = ROOT / "v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md"

DATE = "2026-07-05"

# The 22 C3 cases (pinned by the task spec / V3_C3_REVEAL_CONTRACT_2026-07-05 §4).
# CASE-039 is the CLASSIFIER_FIXABLE_REROUTED overlay (not in the acq-spec C3 list of 21);
# it is included here per the task's explicit case list.
C3_CASES: tuple[str, ...] = (
    "CASE-039", "CSV-041", "CSV-045", "CSV-123", "CSV-124", "CSV-125", "CSV-126",
    "ECU-001", "ECU-009", "EXP-N002", "EXP-N004", "EXP-N005", "EXP-N018", "EXP-N019",
    "EXT-221", "TC-021", "YAML-CSV41", "YAML-CSV45", "YAML-RULE_NOx_1", "YAML-TC47",
    "case_001", "case_013",
)

# Research producer thresholds from cluster3_prepped.md Quantitative Signature Mapping
# (lines 183-188) — reporting + assertion validation only, NOT consumer-rule thresholds.
RESEARCH_LAMBDA_DIVERGENCE_LIMIT = 0.05    # Δλ ≥ 0.05 -> gas-vs-OBD divergence (CONTROL_REFERENCE_FAULT)
RESEARCH_MAP_BARO_SPLIT_LIMIT = 5.0        # |P_MAP − P_BARO| ≥ 5 kPa -> static pressure split
RESEARCH_GROUND_DROP_LIMIT = 0.20          # ΔV_gnd > 0.20 V -> signal-ground offset
RESEARCH_MODULE_VOLTAGE_MIN = 12.0         # KOEO control-module voltage < 12.0 V -> supply/ground suspect
RESEARCH_BIDIRECTIONAL_O2_DELTA_LIMIT = 0.1  # O2 swing < 0.1 V under ±25% steps -> unresponsive (bool False)


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
    """One oracle sub-fault code's band group over the six C3 columns.

    ``bidirectional_ok`` is DETERMINISTIC per fault (not sampled): the P0606 processor
    fault cannot be trusted to execute/return the fuel-override step, so it alone maps
    to ``False``; every other C3 fault leaves the fuel loop able to respond.
    """

    band_id: str
    fault_name: str
    c3_separable: bool
    stay_abstained: bool
    signature: str
    koeo_map_baro_delta_kpa: Band
    module_voltage_loaded_v: Band
    dlc_signal_ground_drop_v: Band
    gas_obd_lambda_delta: Band
    lambda_perception_delta: Band
    bidirectional_ok: bool


# --- Web-corroborated, tolerance-wide band table, keyed on ORACLE fault CODE --------------
# Every separable band is set with margin *past* the research limit so a case fires the
# producer gate across its WHOLE spread (not on a knife-edge); every stay-abstained band is
# set safely BELOW every gate so the confounder/intermittent cases honestly do NOT fire.
CODE_BANDS: dict[str, CodeBandInfo] = {
    # --- Separable: ground-offset lean bias (ΔV_gnd + gas-vs-OBD divergence) --------------
    "ERR-EF-006": CodeBandInfo(
        band_id="C3-LEAN-BIAS",
        fault_name="ecu_fault_lean_bias",
        c3_separable=True,
        stay_abstained=False,
        signature=("Sensor-ground offset: ΔV_gnd shifts O2 reading, ECU perceives rich, "
                   "pulls fuel negative -> engine runs physically lean; gas reads lean while "
                   "OBD commands rich (divergence). MAP/BARO normal (not a ref fault)."),
        koeo_map_baro_delta_kpa=Band(0.0, 3.5, decimals=1),   # normal: ground fault, not ref
        module_voltage_loaded_v=Band(11.8, 13.6, decimals=2),  # supply ok-ish; ground is the fault
        dlc_signal_ground_drop_v=Band(0.22, 0.45, decimals=3),  # FIRES > 0.20 across whole band
        gas_obd_lambda_delta=Band(0.06, 0.14, decimals=3),      # FIRES >= 0.05
        lambda_perception_delta=Band(0.06, 0.15, decimals=3),   # ECU perceives rich vs actual lean
        bidirectional_ok=True,  # sensor still swings around a shifted baseline (web-corroborated)
    ),
    # --- Separable: 5V-ref / MAP over-voltage rich bias (KOEO split + divergence) ---------
    "ERR-EF-007": CodeBandInfo(
        band_id="C3-RICH-BIAS",
        fault_name="ecu_fault_rich_bias",
        c3_separable=True,
        stay_abstained=False,
        signature=("Injector-driver leakage / MAP 5V-ref over-voltage: ECU perceives lean, "
                   "adds fuel -> engine runs physically rich; KOEO MAP-vs-BARO split from the "
                   "ref drift; gas reads rich while OBD commands lean (divergence)."),
        koeo_map_baro_delta_kpa=Band(5.5, 12.0, decimals=1),  # FIRES >= 5 kPa across whole band
        module_voltage_loaded_v=Band(13.0, 14.6, decimals=2),  # supply normal/high
        dlc_signal_ground_drop_v=Band(0.02, 0.09, decimals=3),  # normal (< 0.10): not a ground fault
        gas_obd_lambda_delta=Band(0.06, 0.14, decimals=3),      # FIRES >= 0.05
        lambda_perception_delta=Band(0.06, 0.15, decimals=3),   # ECU perceives lean vs actual rich
        bidirectional_ok=True,
    ),
    # --- Separable: P0606 internal processor fault (bidirectional unresponsive + low Vbatt) -
    "ERR-ECU-001": CodeBandInfo(
        band_id="C3-PROCESSOR",
        fault_name="ecu_internal_processor_fault",
        c3_separable=True,
        stay_abstained=False,
        signature=("P0606: internal processor/memory self-test failure. Engine runs normally "
                   "(gas is sole ground truth) but ALL ECU-reported values are unreliable; "
                   "the module cannot be trusted to execute a bidirectional fuel override -> "
                   "no O2 response (bool False). Weak supply voltage a common trigger."),
        koeo_map_baro_delta_kpa=Band(0.0, 3.5, decimals=1),    # engine runs normal -> pressures ok
        module_voltage_loaded_v=Band(9.5, 11.9, decimals=2),   # LOW < 12.0 (weak/unstable supply)
        dlc_signal_ground_drop_v=Band(0.04, 0.16, decimals=3),  # moderate (below 0.20 gate)
        gas_obd_lambda_delta=Band(0.06, 0.13, decimals=3),      # OBD data untrustworthy -> diverges
        lambda_perception_delta=Band(0.06, 0.14, decimals=3),
        bidirectional_ok=False,  # DETERMINISTIC: processor cannot be trusted to respond
    ),
    # --- STAY-ABSTAINED: oil-burning POA physical confounder (C3-PRE §6) -------------------
    "ERR-EF-002": CodeBandInfo(
        band_id="C3-POA-CONFOUNDER",
        fault_name="ecu_fault_poa_context",
        c3_separable=False,
        stay_abstained=True,
        signature=("Oil-burning POA gas chemistry: a co-existing PHYSICAL exhaust-stream fault "
                   "independently shifts chemistry, so gas and OBD AGREE (no gas-vs-OBD "
                   "divergence). The Δλ test fails to trigger -> C3 signal cannot separate. "
                   "Seeded honestly BELOW every producer gate; STAYS ABSTAINED."),
        koeo_map_baro_delta_kpa=Band(0.0, 3.5, decimals=1),    # no ref split
        module_voltage_loaded_v=Band(12.4, 14.4, decimals=2),  # normal supply
        dlc_signal_ground_drop_v=Band(0.02, 0.09, decimals=3),  # normal (< 0.10)
        gas_obd_lambda_delta=Band(0.00, 0.04, decimals=3),      # below 0.05: no divergence
        lambda_perception_delta=Band(0.00, 0.04, decimals=3),
        bidirectional_ok=True,  # physical fault, not a control fault: loop responds
    ),
    # --- STAY-ABSTAINED: intermittent fault not active during the session ------------------
    "ERR-EF-008": CodeBandInfo(
        band_id="C3-INTERMITTENT",
        fault_name="ecu_fault_intermittent_normal_test",
        c3_separable=False,
        stay_abstained=True,
        signature=("Intermittent ECU fault not active at test time; engine runs normally in "
                   "the one idle snapshot. No control-plausibility signal present to measure "
                   "-> seeded healthy BELOW every gate; STAYS ABSTAINED."),
        koeo_map_baro_delta_kpa=Band(0.0, 3.0, decimals=1),
        module_voltage_loaded_v=Band(12.4, 14.4, decimals=2),
        dlc_signal_ground_drop_v=Band(0.02, 0.08, decimals=3),
        gas_obd_lambda_delta=Band(0.00, 0.03, decimals=3),
        lambda_perception_delta=Band(0.00, 0.03, decimals=3),
        bidirectional_ok=True,
    ),
}

FLOAT_COLS = (
    "koeo_map_baro_delta_kpa",
    "module_voltage_loaded_v",
    "dlc_signal_ground_drop_v",
    "gas_obd_lambda_delta",
    "lambda_perception_delta",
)
BOOL_COL = "bidirectional_fuel_response_ok_bool"
ALL_COLS = (*FLOAT_COLS, BOOL_COL)


def _rng_for(case_id: str) -> random.Random:
    """Deterministic PRNG seeded from the case_id (stable across runs; not wall-clock)."""
    digest = hashlib.sha256(case_id.encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def load_c3_oracle() -> dict[str, str]:
    """Return {case_id: expected_fault_code} for the 22 C3 cases.

    C3 membership is the pinned ``C3_CASES`` list; the oracle sub-fault comes from the corpus
    ``expected_fault_code`` (ground truth) — NOT from any consumer rule or current rank.
    """
    want = set(C3_CASES)
    oracle: dict[str, str] = {}
    with CORPUS.open(newline="") as fh:
        for row in csv.DictReader(fh):
            cid = row["case_id"]
            if cid in want:
                oracle[cid] = row["expected_fault_code"]
    missing = want - oracle.keys()
    if missing:
        raise SystemExit(f"C3 cases missing from corpus: {sorted(missing)}")
    return oracle


def seed_case(case_id: str, oracle_code: str) -> dict[str, object]:
    """Sample one case's synthetic columns from its oracle CODE's web-validated bands."""
    info = CODE_BANDS.get(oracle_code)
    if info is None:
        raise SystemExit(f"{case_id}: oracle code {oracle_code!r} has no C3 band (unexpected)")

    rng = _rng_for(case_id)
    values: dict[str, float] = {
        "koeo_map_baro_delta_kpa": info.koeo_map_baro_delta_kpa.sample(rng),
        "module_voltage_loaded_v": info.module_voltage_loaded_v.sample(rng),
        "dlc_signal_ground_drop_v": info.dlc_signal_ground_drop_v.sample(rng),
        "gas_obd_lambda_delta": info.gas_obd_lambda_delta.sample(rng),
        "lambda_perception_delta": info.lambda_perception_delta.sample(rng),
    }
    return {
        "case_id": case_id,
        "oracle_fault_family": "ecu_fault",
        "oracle_fault_code": oracle_code,
        "oracle_fault_name": info.fault_name,
        "band_id": info.band_id,
        "c3_separable": info.c3_separable,
        "stay_abstained": info.stay_abstained,
        "synthetic": True,
        **values,
        BOOL_COL: info.bidirectional_ok,
    }


def _assert_no_backsolve(seed_rows: list[dict[str, object]]) -> None:
    """Reconciliation + robustness audit.

    Every value sits in its OWN oracle-code band; every C3-separable case fires at least one
    producer gate across its whole spread (not a knife-edge); every stay-abstained case sits
    safely BELOW every gate (honest non-firing). Uses the research/producer limits only —
    never a consumer-rule value.
    """
    assert len(seed_rows) == 22, f"expected 22 C3 cases, got {len(seed_rows)}"
    for r in seed_rows:
        code = str(r["oracle_fault_code"])
        info = CODE_BANDS[code]
        assert r["band_id"] == info.band_id, f"band mismatch {r['case_id']}"
        assert r["synthetic"] is True

        map_baro = cast(float, r["koeo_map_baro_delta_kpa"])
        vmod = cast(float, r["module_voltage_loaded_v"])
        gnd = cast(float, r["dlc_signal_ground_drop_v"])
        dlam = cast(float, r["gas_obd_lambda_delta"])
        bidir_ok = cast(bool, r[BOOL_COL])

        if info.c3_separable:
            # at least one producer gate must fire; assert the group's designed discriminator
            if code == "ERR-EF-006":
                assert gnd > RESEARCH_GROUND_DROP_LIMIT, r
                assert dlam >= RESEARCH_LAMBDA_DIVERGENCE_LIMIT, r
            elif code == "ERR-EF-007":
                assert map_baro >= RESEARCH_MAP_BARO_SPLIT_LIMIT, r
                assert dlam >= RESEARCH_LAMBDA_DIVERGENCE_LIMIT, r
            elif code == "ERR-ECU-001":
                assert bidir_ok is False, r  # deterministic separator
                assert vmod < RESEARCH_MODULE_VOLTAGE_MIN, r
        else:
            # stay-abstained: honestly fires NO gate anywhere in the spread
            assert map_baro < RESEARCH_MAP_BARO_SPLIT_LIMIT, r
            assert gnd <= RESEARCH_GROUND_DROP_LIMIT, r
            assert dlam < RESEARCH_LAMBDA_DIVERGENCE_LIMIT, r
            assert bidir_ok is True, r
            assert vmod >= RESEARCH_MODULE_VOLTAGE_MIN, r


def write_csv(seed_rows: list[dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    cols = ["case_id", "oracle_fault_family", "oracle_fault_code", "oracle_fault_name",
            "band_id", "c3_separable", "stay_abstained", "synthetic", *ALL_COLS]
    with OUT_CSV.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in seed_rows:
            w.writerow({c: r[c] for c in cols})


# --- Web-corroboration citations (one per signature band / threshold) --------------------
CITATIONS: dict[str, str] = {
    "ground_drop_standard": (
        "Ground-circuit voltage drop max 0.1 V (0.2 V for a wire/cable run); computer/sensor "
        "grounds are the strictest — Fluke: any reading > 0.10 V on a computer ground is a "
        "fault, and as little as 0.30 V on a computer ground causes trouble; CARDONE ECM "
        "bulletin: allowable drop 0.1 V, > 0.3 V unacceptable. [STANDARDIZED] "
        "fluke.com/en-us/learn/blog/automotive/electrical-automotive-troubleshooting; "
        "aa1car.com/library/voltage_drop_testing.htm; cardone.com PT77-0008"
    ),
    "ground_offset_lean_mechanism": (
        "A positive ground offset raises the O2 voltage the ECU sees; the ECU reads a genuinely "
        "stoichiometric/lean mixture as RICH and commands negative fuel trim, driving the engine "
        "physically lean — the tell is the contradiction between sensor/OBD command and actual "
        "chemistry. [empirical/field] vehicleservicepros.com fuel-trims-downstream-o2; "
        "fordfiesta.org O2-sensors-reading-rich-fuel-trims-adding-more-fuel"
    ),
    "koeo_map_baro": (
        "With the key on, engine off, manifold pressure equals ambient barometric pressure "
        "(~98-102 kPa at sea level); MAP and BARO should read equal/very-similar at KOEO, and a "
        "significant MAP-vs-BARO difference sets a plausibility DTC (e.g. P0069). [manufacturer-"
        "typical] aa1car.com/library/map_sensors.htm; engineerfix.com/how-to-test-a-map-sensor-"
        "with-a-scan-tool; underhoodservice.com/follow-the-map-sensor"
    ),
    "lambda_divergence": (
        "Gas-to-OBD divergence Δλ = |λ_OBD − λ_tailpipe| ≥ 0.05 flags a control-reference fault "
        "(exhaust analyzer reads lean while OBD trims command rich, or vice-versa). "
        "[EMPIRICAL-ANECDOTAL — practitioner heuristic, not an OEM/SAE constant] "
        "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping line 183"
    ),
    "processor_p0606": (
        "P0606 = ECM internal CPU/RAM/ROM self-test failure; the module cannot correctly "
        "interpret its 50+ sensor inputs so ALL ECU-reported data is untrustworthy — yet the "
        "engine frequently runs normally (MIL only). Weak battery (< 12.4 V) / poor grounds are "
        "common triggers. [manufacturer-typical] obd-codes.com/p0606; fixdapp.com/blog/p0606-"
        "code; skanyx.com/codes/p0606"
    ),
    "bidirectional_response": (
        "Active bidirectional fuel-override (±25% / −12.5% steps) with an O2 swing < 0.1 V "
        "indicates the loop is unresponsive to command; a healthy loop swings and the propane/"
        "override test confirms sensor responsiveness. [manufacturer-typical] "
        "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping line 188"
    ),
}


def write_manifest(seed_rows: list[dict[str, object]]) -> None:
    manifest = {
        "task": "T-V3-P4-C3-SYNTH",
        "generated": DATE,
        "mode": "provisional-synthetic-seed (side file; live corpus untouched)",
        "policy": "4DLab_CLAUDE.md §Provisional synthetic signals",
        "oracle_discriminator": ("all 22 C3 cases share expected_fault_family=ecu_fault; the "
                                 "band group is keyed on the finer expected_fault_code (answer "
                                 "key), resolved to a registry fault_name"),
        "no_backsolve": ("generator keys only on corpus expected_fault_code (oracle) + the "
                         "web-validated band table; does not read ecu_fault.json / "
                         "sensor_fault.json thresholds or any case rank/prediction"),
        "research_limits_cluster3": {
            "lambda_divergence_ge": RESEARCH_LAMBDA_DIVERGENCE_LIMIT,
            "map_baro_split_ge_kpa": RESEARCH_MAP_BARO_SPLIT_LIMIT,
            "ground_drop_gt_v": RESEARCH_GROUND_DROP_LIMIT,
            "module_voltage_min_v": RESEARCH_MODULE_VOLTAGE_MIN,
            "bidirectional_o2_delta_lt_v": RESEARCH_BIDIRECTIONAL_O2_DELTA_LIMIT,
        },
        "grounding_tags": {
            "gas_obd_lambda_delta": "empirical-anecdotal (Δλ ≥ 0.05; practitioner heuristic)",
            "lambda_perception_delta": "empirical-anecdotal (derived from the same divergence)",
            "dlc_signal_ground_drop_v": "standardized (0.1/0.2 V DMM voltage-drop convention)",
            "koeo_map_baro_delta_kpa": "manufacturer-typical (KOEO MAP=BARO plausibility)",
            "module_voltage_loaded_v": "manufacturer-typical (KOEO supply ≥ 12.0 V pre-gate)",
            "bidirectional_fuel_response_ok_bool": ("manufacturer-typical; DETERMINISTIC per "
                                                    "fault (not sampled) — only P0606 -> False"),
        },
        "band_table": {
            code: {
                "band_id": b.band_id,
                "fault_name": b.fault_name,
                "c3_separable": b.c3_separable,
                "stay_abstained": b.stay_abstained,
                "signature": b.signature,
                "bidirectional_ok": b.bidirectional_ok,
                "float_bands": {
                    "koeo_map_baro_delta_kpa": [b.koeo_map_baro_delta_kpa.lo, b.koeo_map_baro_delta_kpa.hi, b.koeo_map_baro_delta_kpa.sigma],
                    "module_voltage_loaded_v": [b.module_voltage_loaded_v.lo, b.module_voltage_loaded_v.hi, b.module_voltage_loaded_v.sigma],
                    "dlc_signal_ground_drop_v": [b.dlc_signal_ground_drop_v.lo, b.dlc_signal_ground_drop_v.hi, b.dlc_signal_ground_drop_v.sigma],
                    "gas_obd_lambda_delta": [b.gas_obd_lambda_delta.lo, b.gas_obd_lambda_delta.hi, b.gas_obd_lambda_delta.sigma],
                    "lambda_perception_delta": [b.lambda_perception_delta.lo, b.lambda_perception_delta.hi, b.lambda_perception_delta.sigma],
                },
            }
            for code, b in CODE_BANDS.items()
        },
        "citations": CITATIONS,
        "cases": {r["case_id"]: r for r in seed_rows},
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(manifest, indent=2, sort_keys=False) + "\n")


def write_report(seed_rows: list[dict[str, object]]) -> None:
    by_code: dict[str, list[dict[str, object]]] = {}
    for r in seed_rows:
        by_code.setdefault(str(r["oracle_fault_code"]), []).append(r)

    n_sep = sum(1 for r in seed_rows if r["c3_separable"])
    n_abs = len(seed_rows) - n_sep

    lines: list[str] = []
    lines.append(f"# V3_C3_SYNTH_BANDS_{DATE}")
    lines.append("")
    lines.append("**Task:** `T-V3-P4-C3-SYNTH`  **Mode:** provisional-synthetic seed (side file)")
    lines.append("**Policy:** `4DLab_CLAUDE.md` §Provisional synthetic signals — grounded, "
                 "tolerance-wide, web-corroborated, `synthetic=true`, correctable.")
    lines.append("**Writes live corpus / engine / rules / yardstick:** no. **Regenerate:** "
                 "`/agent_workspace/.venv-wired/bin/python v3/gen_c3_synth_seed.py`.")
    lines.append("**Data + manifest:** `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}`.")
    lines.append("**Baseline pin (from C3-PRE):** `V3_YARDSTICK_2026-07-05` (csv `3df2e8cb…`, "
                 "oracle `3088a7c3…`), run `POST_T_V3_P4_C2B`.")
    lines.append("")
    lines.append("Seeds the 22 C3 cases' control-plausibility columns "
                 "(`koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, "
                 "gas_obd_lambda_delta, lambda_perception_delta, "
                 "bidirectional_fuel_response_ok_bool`) with values derived from each case's "
                 "**oracle fault code** through the `cluster3_prepped.md` signature "
                 "(lines 183-188), each band widened to the real-world spread found via web "
                 "research. Consumed by `T-V3-P4-C3A` (dry-run) and `C3B` (commit).")
    lines.append("")
    lines.append("## 1. No-back-solve statement")
    lines.append("")
    lines.append("All 22 C3 cases share `expected_fault_family = ecu_fault`, so the band group "
                 "is keyed on the finer **`expected_fault_code`** — the corpus **answer key** — "
                 "resolved to a registry `fault_name`. The generator's **only** inputs are "
                 "(a) each case's `expected_fault_code` and (b) the band table below. It does "
                 "**not** read `ecu_fault.json` / `sensor_fault.json` consumer thresholds, nor "
                 "any case's current rank or predicted family. The Δλ≥0.05, |MAP−BARO|≥5 kPa, "
                 "ΔV_gnd>0.20 V, Vmod<12.0 V and O2-swing<0.1 V limits used to *verify* the seed "
                 "are the **research/producer** bands from `cluster3_prepped.md`, not consumer "
                 "rules. Floats are sampled uniformly across a tolerance-wide band (σ reported), "
                 "seeded deterministically per `case_id` (SHA-256; no wall-clock randomness). "
                 "The bool is **deterministic** per fault (only P0606 → `False`), not sampled.")
    lines.append("")
    lines.append("## 2. Per-column bands — cluster3 research vs web-real vs band used")
    lines.append("")
    lines.append("| Column / signal | cluster3 producer threshold | Web-real range (cited) | Band used (tolerance-wide) | Grounding |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append("| `dlc_signal_ground_drop_v` — bias/offset | `> 0.20 V` (signal ground) | computer-ground fault > 0.10 V; trouble at 0.30 V | lean-bias ∈ **[0.22, 0.45] V** (fires); others ≤ 0.16 V | **standardized** |")
    lines.append("| `gas_obd_lambda_delta` (Δλ) | `>= 0.05` divergence | practitioner heuristic (no OEM constant) | separable ∈ **[0.06, 0.14]** (fires); abstain ≤ 0.04 | **empirical-anecdotal** |")
    lines.append("| `lambda_perception_delta` | derived from divergence | ECU perceived-vs-actual λ gap | separable ∈ **[0.06, 0.15]**; abstain ≤ 0.04 | **empirical-anecdotal** |")
    lines.append("| `koeo_map_baro_delta_kpa` | `>= 5 kPa` static split | KOEO MAP≈BARO ~98-102 kPa; split sets P0069 | rich-bias ∈ **[5.5, 12.0] kPa** (fires); others < 3.5 | **manufacturer-typical** |")
    lines.append("| `module_voltage_loaded_v` | `< 12.0 V` supply suspect | P0606 triggered by weak battery < 12.4 V | processor ∈ **[9.5, 11.9] V** (low); others ≥ 11.8 | **manufacturer-typical** |")
    lines.append("| `bidirectional_fuel_response_ok_bool` | O2 swing `< 0.1 V` → unresponsive | active-test/propane confirms responsiveness | **False** only for P0606; **True** otherwise (deterministic) | **manufacturer-typical** |")
    lines.append("")
    lines.append("Where the web shows a **wider or stricter** range than the research answer "
                 "(computer grounds fault below 0.10 V vs the 0.20 V signal-ground gate), the "
                 "band is set to fire the producer gate robustly while staying field-realistic "
                 "(policy step 3). Bands are stated separately per oracle sub-fault below.")
    lines.append("")
    lines.append("### Citations")
    lines.append("")
    for key, txt in CITATIONS.items():
        lines.append(f"- **{key}** — {txt}")
    lines.append("")
    lines.append("## 3. Tolerance width (σ) — fires/clears across the WHOLE spread, not a knife-edge")
    lines.append("")
    lines.append("Worst-case corners: lean-bias ground drop low corner = **0.22 V > 0.20**; "
                 "rich-bias MAP-BARO low corner = **5.5 kPa ≥ 5.0**; processor Vmod high corner "
                 "= **11.9 V < 12.0**; every separable Δλ low corner = **0.06 ≥ 0.05**. Every "
                 "abstain-group high corner sits BELOW every gate (Δλ ≤ 0.04, ground ≤ 0.09 V, "
                 "MAP-BARO ≤ 3.5 kPa). Reported σ per band (uniform std-dev = (hi−lo)/√12):")
    lines.append("")
    lines.append("| oracle code | band_id | separable | map-baro σ | Vmod σ | gnd-drop σ | Δλ σ | perception σ | bidir_ok |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for code, b in CODE_BANDS.items():
        lines.append(f"| {code} | {b.band_id} | {'yes' if b.c3_separable else '**NO**'} | "
                     f"{b.koeo_map_baro_delta_kpa.sigma} | {b.module_voltage_loaded_v.sigma} | "
                     f"{b.dlc_signal_ground_drop_v.sigma} | {b.gas_obd_lambda_delta.sigma} | "
                     f"{b.lambda_perception_delta.sigma} | {b.bidirectional_ok} |")
    lines.append("")
    lines.append("## 4. Seeded cases (22/22) — value sits in its own oracle-code band")
    lines.append("")
    lines.append("| case_id | oracle code | fault_name | band | sep | MAP-BARO kPa | Vmod V | gnd V | Δλ | perc. | bidir_ok |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in seed_rows:
        lines.append(f"| {r['case_id']} | {r['oracle_fault_code']} | {r['oracle_fault_name']} | "
                     f"{r['band_id']} | {'Y' if r['c3_separable'] else 'abst'} | "
                     f"{r['koeo_map_baro_delta_kpa']} | {r['module_voltage_loaded_v']} | "
                     f"{r['dlc_signal_ground_drop_v']} | {r['gas_obd_lambda_delta']} | "
                     f"{r['lambda_perception_delta']} | {r[BOOL_COL]} |")
    lines.append("")
    lines.append("## 5. Separability split — which cases the C3 signal can and cannot separate")
    lines.append("")
    lines.append(f"The 22 C3 cases split by oracle code: "
                 f"**{len(by_code.get('ERR-EF-006', []))} lean-bias (ERR-EF-006), "
                 f"{len(by_code.get('ERR-EF-007', []))} rich-bias (ERR-EF-007), "
                 f"{len(by_code.get('ERR-ECU-001', []))} processor/P0606 (ERR-ECU-001), "
                 f"{len(by_code.get('ERR-EF-002', []))} POA-confounder (ERR-EF-002), "
                 f"{len(by_code.get('ERR-EF-008', []))} intermittent (ERR-EF-008)**.")
    lines.append("")
    lines.append(f"- **C3-SEPARABLE ({n_sep}):** ERR-EF-006 + ERR-EF-007 + ERR-ECU-001. The "
                 "ControlPlausibilityState producer separates these three: lean-bias fires the "
                 "ground-drop (>0.20 V) + Δλ divergence gates; rich-bias fires the KOEO MAP-BARO "
                 "split (≥5 kPa) + Δλ; the P0606 processor fault fires the deterministic "
                 "bidirectional-unresponsive gate (`bool=False`) with a low supply voltage. C3A "
                 "should predict these flip toward top-3.")
    lines.append(f"- **STAY-ABSTAINED ({n_abs}):** the C3-PRE §6 confounders. "
                 f"**{len(by_code.get('ERR-EF-002', []))} POA-context (ERR-EF-002)** — a "
                 "co-existing PHYSICAL oil-burning fault shifts exhaust chemistry so gas and OBD "
                 "AGREE; the Δλ test fails to trigger, so C3 cannot separate them. "
                 f"**{len(by_code.get('ERR-EF-008', []))} intermittent (ERR-EF-008)** — the fault "
                 "is not active in the single idle snapshot, so no control-plausibility signal "
                 "exists to measure. Both are seeded **honestly below every producer gate** "
                 "(never into a passing band) and flagged `stay_abstained=true`; they remain "
                 "abstained under the C3 producer/consumer until a different discriminator "
                 f"(physical-fault isolation, or repeat sampling) lands. **{n_sep} + {n_abs} = 22.** ✔")
    lines.append("")
    lines.append("> **Never read synthetic-seeded passes as real-world accuracy.** The manifest "
                 "`synthetic=true` + downstream scoreboard split keep them distinguishable; the "
                 "Δλ discriminator is **empirical-anecdotal** (C3-PRE §7) and must be confirmed "
                 "against real vehicle data before it is trusted as a live win.")
    lines.append("")
    lines.append("## Provenance / guardrails")
    lines.append("")
    lines.append("- Side file only: no write to `cases_petrol_v7.csv` / `corpus_curated.csv`, no "
                 "engine/lab/registry/rule edit, no re-score, no yardstick mint, no abstain-dial "
                 "change. Writes only under `v3/`. `Vault/` untouched. No `graphify`/frozen-graph "
                 "rebuild. `run_suite.py` untouched. No secrets.")
    lines.append("- Inputs: corpus `expected_fault_code` (oracle) for the pinned 22 `C3_CASES` + "
                 "the web-validated band table. Producer thresholds cited to "
                 "`v3/research/research_answers/cluster3_prepped.md` and "
                 "`v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md`. Governs `T-V3-P4-C3A` / `C3B`.")
    lines.append("")
    OUT_REPORT.write_text("\n".join(lines))


def main() -> None:
    oracle = load_c3_oracle()
    seed_rows = [seed_case(cid, code) for cid, code in sorted(oracle.items())]
    _assert_no_backsolve(seed_rows)

    write_csv(seed_rows)
    write_manifest(seed_rows)
    write_report(seed_rows)

    code_counts: dict[str, int] = {}
    for r in seed_rows:
        code_counts[str(r["oracle_fault_code"])] = code_counts.get(str(r["oracle_fault_code"]), 0) + 1
    separable = sum(1 for r in seed_rows if r["c3_separable"])
    print(f"[C3-SYNTH] seeded {len(seed_rows)}/22 cases  ->  {OUT_CSV.name}, {OUT_JSON.name}")
    print(f"[C3-SYNTH] oracle-code split: {code_counts}")
    print(f"[C3-SYNTH] C3-separable: {separable}; stay-abstained: {len(seed_rows) - separable}")
    print(f"[C3-SYNTH] report: {OUT_REPORT.name}  (no live corpus / engine / yardstick touched)")


if __name__ == "__main__":
    main()
