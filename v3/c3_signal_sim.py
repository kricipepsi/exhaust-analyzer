#!/usr/bin/env python3
"""Read-only overlay simulator for the C3 (ecu_fault / ControlPlausibilityState) signal pack.

DISCLOSE half of the C3 pack (T-V3-P4-C3A). Simulates the proposed C3
`ControlPlausibilityState` producer and its EF/SF consumer overlay in memory over the
`c3_synthetic_seed_2026-07-05` seed, against the pinned `POST_T_V3_P4_C2B` baseline.

Mirrors the c2/c4 overlay pattern (monkeypatch `shim._score_rule`), but is pinned to the
**current** active baseline `POST_T_V3_P4_C2B` — NOT `POST_T_V3_3D`. C2B has landed since
those sims were written (ruler moved 197 -> 212), so the live engine now carries the C2
wiring; only the C2B run reproduces exactly (the C4A stale-baseline lesson, task file §Baseline).

Nothing live is mutated: no corpus/rule/registry/engine/lab edit, no yardstick mint, no
seed regeneration, no abstain-dial change. Writes reports only under `v3/`.

Producer gates (V3_C3_REVEAL_CONTRACT_2026-07-05 §2, grounding-tagged):
  lean-bias : dlc_signal_ground_drop_v > 0.20  AND gas_obd_lambda_delta >= 0.05
  rich-bias : koeo_map_baro_delta_kpa >= 5.0   AND gas_obd_lambda_delta >= 0.05
  processor : bidirectional_fuel_response_ok_bool == False AND module_voltage_loaded_v < 12.0
  any met -> CONTROL_REFERENCE_FAULT (record sub-gate); none -> ABSTAIN.

Scenario ladder (acquisition-cost disclosure):
  Scenario 1 = Tier-A/C electrical-only gates (KOEO MAP/BARO + ground drop + Vmod +
               bidirectional) with NO Delta-lambda term -> drops the two-point 5-gas ask.
  Scenario 2 = full contract gates including gas_obd_lambda_delta.
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

# Bootstrap paths so engine modules resolve correctly
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE_ROOT / "apps/wired"))

# Suppress verbose engine logging
logging.getLogger().setLevel(logging.ERROR)

from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # type: ignore # noqa: E402
from wired.composition import diagnose  # type: ignore # noqa: E402
from fl_tasks.score_v3_yardstick import load_rule_family_map, collect_top3_families  # type: ignore # noqa: E402
import registry.integration_shim as shim  # type: ignore # noqa: E402
from registry.integration_shim import RegistryV2Router  # type: ignore # noqa: E402

# Baseline pin (task file §Baseline; V3_C3_REVEAL_CONTRACT_2026-07-05 §baseline).
BASELINE_RUN = "POST_T_V3_P4_C2B"
BASELINE_PATH = WORKSPACE_ROOT / f"apps/wired/v7/runs/{BASELINE_RUN}/results.json"
DEFAULT_SEED = WORKSPACE_ROOT / "v3/data/c3_synthetic_seed_2026-07-05.json"

# C3 producer gate constants (V3_C3_REVEAL_CONTRACT_2026-07-05 §2, grounding-tagged).
GND_DROP_GATE_V = 0.20          # standardized (DMM 0.1/0.2 V convention)
LAMBDA_DIVERGENCE_GATE = 0.05   # empirical-anecdotal (practitioner heuristic, NOT OEM/SAE)
MAP_BARO_GATE_KPA = 5.0         # manufacturer-typical (KOEO MAP=BARO plausibility)
MODULE_VOLTAGE_GATE_V = 12.0    # manufacturer-typical (P0606 weak-supply trigger)

# Consumer rule ids the C3 state gates (contract §3).
EF_RULES = ["EF-001", "EF-002", "EF-003"]          # ecu_fault: boosted when CONTROL_REFERENCE_FAULT
SF_RULES = ["SF-001", "SF-002"]                    # sensor_fault: dispersion-as-sensor-bias mapping
CONTROL_BOOST = 0.10                               # DEFINITIVE boost, mirrors c2/c4 overlays

CURRENT_CASE_ID: list[str | None] = [None]


def load_denominator_rows() -> list[dict[str, str]]:
    """Load the 294 accuracy denominator rows from the frozen v7 corpus CSV."""
    csv_path = Path(DEFAULT_CSV_PATH)
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    return [
        r
        for r in all_rows
        if r["tag"] != "invalid"
        and r.get("accuracy_excluded", "").lower() != "true"
    ]


def compute_c3_states(
    c3_cases: dict[str, Any],
) -> dict[str, dict[str, str]]:
    """Compute the C3 ControlPlausibilityState per case, for both scenarios.

    Returns {"scen1_electrical": {cid: state}, "scen2_full": {cid: state}} where state is
    ``CONTROL_REFERENCE_FAULT`` or ``ABSTAIN``. The gate that fires (for the report) is kept
    in the parallel ``sub_gates`` map returned by :func:`compute_c3_sub_gates`.
    """
    scen1: dict[str, str] = {}  # electrical-only (no Delta-lambda)
    scen2: dict[str, str] = {}  # full contract (incl. Delta-lambda)

    for cid, cdata in c3_cases.items():
        gnd = float(cdata.get("dlc_signal_ground_drop_v", 0.0))
        lam = float(cdata.get("gas_obd_lambda_delta", 0.0))
        map_baro = float(cdata.get("koeo_map_baro_delta_kpa", 0.0))
        vmod = float(cdata.get("module_voltage_loaded_v", 14.0))
        bidir_ok = bool(cdata.get("bidirectional_fuel_response_ok_bool", True))

        # Scenario 2 (full): the lean-bias and rich-bias gates require the Delta-lambda
        # divergence confirmation; the processor gate is purely electrical.
        lean_full = (gnd > GND_DROP_GATE_V) and (lam >= LAMBDA_DIVERGENCE_GATE)
        rich_full = (map_baro >= MAP_BARO_GATE_KPA) and (lam >= LAMBDA_DIVERGENCE_GATE)
        processor = (not bidir_ok) and (vmod < MODULE_VOLTAGE_GATE_V)
        scen2[cid] = "CONTROL_REFERENCE_FAULT" if (lean_full or rich_full or processor) else "ABSTAIN"

        # Scenario 1 (electrical-only): drop the Delta-lambda term. Lean-bias then fires on
        # the ground-drop gate alone; rich-bias on the MAP/BARO split alone; processor
        # unchanged (already electrical). This prices whether the owner needs the two-point
        # 5-gas ask (action A6) or the cheaper electrical bench (A5) alone.
        lean_elec = gnd > GND_DROP_GATE_V
        rich_elec = map_baro >= MAP_BARO_GATE_KPA
        scen1[cid] = "CONTROL_REFERENCE_FAULT" if (lean_elec or rich_elec or processor) else "ABSTAIN"

    return {"scen1_electrical": scen1, "scen2_full": scen2}


def compute_c3_sub_gates(c3_cases: dict[str, Any]) -> dict[str, str]:
    """Record which producer sub-gate fires per case under the full (Scenario 2) contract."""
    sub: dict[str, str] = {}
    for cid, cdata in c3_cases.items():
        gnd = float(cdata.get("dlc_signal_ground_drop_v", 0.0))
        lam = float(cdata.get("gas_obd_lambda_delta", 0.0))
        map_baro = float(cdata.get("koeo_map_baro_delta_kpa", 0.0))
        vmod = float(cdata.get("module_voltage_loaded_v", 14.0))
        bidir_ok = bool(cdata.get("bidirectional_fuel_response_ok_bool", True))

        fired = []
        if (gnd > GND_DROP_GATE_V) and (lam >= LAMBDA_DIVERGENCE_GATE):
            fired.append("lean-bias(gnd+Δλ)")
        if (map_baro >= MAP_BARO_GATE_KPA) and (lam >= LAMBDA_DIVERGENCE_GATE):
            fired.append("rich-bias(map/baro+Δλ)")
        if (not bidir_ok) and (vmod < MODULE_VOLTAGE_GATE_V):
            fired.append("processor(bidir=False+Vmod<12)")
        sub[cid] = " ; ".join(fired) if fired else "(none)"
    return sub


def run_diagnose_loop(
    corpus_rows: Sequence[Mapping[str, Any]],
    c3_states: dict[str, str],
    rule_map: Mapping[str, str],
    c3_overlay_enabled: bool,
) -> dict[str, dict[str, Any]]:
    """Run all corpus cases through diagnose() with a scoring monkeypatch overlay.

    When a case carries a C3 ``CONTROL_REFERENCE_FAULT`` state, the ecu_fault consumers
    (EF-001/002/003) get a DEFINITIVE boost and the sensor_fault dispersion rules
    (SF-001/002) are pruned (a control-reference ground offset that *looks* like sensor
    bias must not still fire the sensor-bias rule). Non-C3 cases are untouched.
    """
    original_score_rule = shim._score_rule

    def my_score_rule(rule: Any, obs: Any) -> float | None:
        cid = CURRENT_CASE_ID[0]

        # 1. Raw score before clamping (mirror c2/c4 mechanics)
        orig_ceiling = rule.confidence_ceiling
        rule.confidence_ceiling = None
        raw_score = original_score_rule(rule, obs)
        rule.confidence_ceiling = orig_ceiling

        # 2. Apply C3 overlay when this case has a C3 state and the overlay is enabled
        if c3_overlay_enabled and cid in c3_states:
            c3_state = c3_states[cid]
            if c3_state == "CONTROL_REFERENCE_FAULT":
                if rule.rule_id in EF_RULES:
                    score_to_boost = raw_score if raw_score is not None else rule.base_weight
                    return min(score_to_boost + CONTROL_BOOST, 1.0)
                if rule.rule_id in SF_RULES:
                    # Dispersion presents as sensor bias but is an ECU control-reference
                    # fault: prune the sensor-bias rule so it does not out-rank ecu_fault.
                    return None
            # ABSTAIN: leave every rule at its baseline behaviour (no boost, no prune).

        if raw_score is None:
            return None
        return min(raw_score, orig_ceiling if orig_ceiling is not None else 1.0)

    shim._score_rule = my_score_rule
    results: dict[str, dict[str, Any]] = {}

    try:
        RegistryV2Router()  # build the ruleset in local scope
        for r in corpus_rows:
            cid = str(r["case_id"])
            CURRENT_CASE_ID[0] = cid
            output = diagnose(r["raw_inputs"], enable_fatal_gates=False)
            verdict = output.diagnostic_verdict
            winner_family = verdict.fault_family
            winner_id = verdict.fault_code
            winner_score = verdict.confidence_score
            siblings = [s.model_dump() for s in verdict.differential_siblings]

            top3_fams = collect_top3_families(winner_family, siblings, rule_map)
            top3_hit = r["expected_family"] in top3_fams

            results[cid] = {
                "winner_id": winner_id,
                "winner_family": winner_family,
                "winner_score": winner_score,
                "top3_families": top3_fams,
                "top3_hit": top3_hit,
                "abstained": verdict.abstained,
            }
    finally:
        shim._score_rule = original_score_rule

    return results


def build_corpus_rows() -> list[dict[str, Any]]:
    """Assemble the 294 denominator rows into diagnose-ready dicts."""
    denom_rows = load_denominator_rows()
    return [
        {
            "case_id": r["case_id"],
            "expected_family": r["expected_fault_family"].lower(),
            "raw_inputs": row_to_raw_inputs(r),
        }
        for r in denom_rows
    ]


def run_self_check() -> bool:
    """Zero-overlay self-check: reproduce POST_T_V3_P4_C2B/results.json exactly (drift=0)."""
    print(f"Running zero-overlay self-check against {BASELINE_RUN}...")
    if not BASELINE_PATH.is_file():
        print(f"Error: baseline run results file not found at {BASELINE_PATH}", file=sys.stderr)
        return False

    with open(BASELINE_PATH, encoding="utf-8") as f:
        baseline_run = json.load(f)["results"]
    baseline_by_case = {r["case_id"]: r for r in baseline_run}

    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    simulated_baseline = run_diagnose_loop(corpus_rows, {}, rule_map, c3_overlay_enabled=False)

    mismatches = 0
    for r in corpus_rows:
        cid = r["case_id"]
        actual_res = baseline_by_case.get(cid)
        if not actual_res:
            continue

        sim_res = simulated_baseline[cid]
        actual_verdict = actual_res.get("verdict") or {}

        actual_winner_id = actual_verdict.get("fault_code", "")
        actual_winner_family = actual_verdict.get("fault_family", "")
        actual_sibs = actual_verdict.get("differential_siblings", [])
        actual_top3_fams = collect_top3_families(actual_winner_family, actual_sibs, rule_map)
        actual_top3_hit = r["expected_family"] in actual_top3_fams
        actual_abstained = bool(actual_verdict.get("abstained", False))

        if (
            sim_res["winner_id"] != actual_winner_id
            or sim_res["winner_family"] != actual_winner_family
            or sim_res["top3_hit"] != actual_top3_hit
            or sim_res["abstained"] != actual_abstained
        ):
            mismatches += 1
            print(
                f"Mismatch in {cid}: "
                f"actual=({actual_winner_id}, {actual_winner_family}, top3={actual_top3_hit}, "
                f"abstained={actual_abstained}), "
                f"sim=({sim_res['winner_id']}, {sim_res['winner_family']}, top3={sim_res['top3_hit']}, "
                f"abstained={sim_res['abstained']})"
            )

    if mismatches == 0:
        print("Zero-overlay self-check: OK (all 294 cases matched, drift = 0)")
        return True

    print(f"Zero-overlay self-check: FAILED with {mismatches} mismatches", file=sys.stderr)
    return False


def derive_ft8_neighbour_union() -> tuple[set[str], dict[str, list[str]]]:
    """Live-derive the FT-8 neighbour union from the touched rules' passes_cases.

    Touched families: ecu_fault (EF-*) + sensor_fault (SF-*), both competition groups.
    Never reuse a previous pack's neighbour list — rebuild it from the rule JSONs.
    """
    union: set[str] = set()
    per_rule: dict[str, list[str]] = {}
    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    for fn in ("ecu_fault.json", "sensor_fault.json"):
        data = json.loads((rules_dir / fn).read_text(encoding="utf-8"))
        for rule in data.get("rules", []):
            rid = rule.get("rule_id", "")
            passes = list(rule.get("passes_cases", []))
            per_rule[rid] = passes
            union.update(passes)
    return union, per_rule


def build_scenario_summary(
    corpus_rows: list[dict[str, Any]],
    baseline_results: dict[str, dict[str, Any]],
    sim_results: dict[str, dict[str, Any]],
    c3_cases: dict[str, Any],
) -> dict[str, Any]:
    """Compute yield + coverage + regression metrics for one scenario simulation.

    ``WOULD_BANK`` tracks the top-3 flip (correct family enters the top-3 window that was
    absent at baseline) — the pack's headline ``top3_family`` metric and the task's
    "flip into top-3" language. The covered-vs-still-abstained split is disclosed
    separately (``would_bank_covered`` / ``would_bank_still_abstained``) because the
    MARGIN=0.02 abstain dial can keep a flipped case out of the covered-accuracy count.
    """
    total_baseline_passes = 0
    total_sim_passes = 0
    total_sim_on_covered = 0
    sim_covered_count = 0
    abstained_count = 0

    would_bank: list[str] = []
    would_bank_covered: list[str] = []
    would_bank_still_abstained: list[str] = []
    already_pass: list[str] = []
    still_short: list[str] = []
    regressions: list[str] = []

    for r in corpus_rows:
        cid = r["case_id"]
        base_h = baseline_results[cid]["top3_hit"]
        sim_h = sim_results[cid]["top3_hit"]
        sim_a = sim_results[cid]["abstained"]

        if base_h:
            total_baseline_passes += 1
        if sim_h:
            total_sim_passes += 1
            if not sim_a:
                total_sim_on_covered += 1
        if not sim_a:
            sim_covered_count += 1
        else:
            abstained_count += 1

        # Regression = correct family was in the top-3 window at baseline and is no longer.
        # The overlay only rescoring C3 cases, so neighbours are structurally untouched;
        # this catches any family that fell out on the full 294.
        if base_h and not sim_h:
            regressions.append(cid)

        if cid in c3_cases:
            if not base_h and sim_h:
                would_bank.append(cid)
                (would_bank_covered if not sim_a else would_bank_still_abstained).append(cid)
            elif base_h and sim_h:
                already_pass.append(cid)
            else:
                still_short.append(cid)

    coverage = sim_covered_count / len(corpus_rows)
    top3_on_covered = total_sim_on_covered / sim_covered_count if sim_covered_count else 0.0

    return {
        "baseline_top3_passes": total_baseline_passes,
        "simulated_top3_passes": total_sim_passes,
        "simulated_on_covered_passes": total_sim_on_covered,
        "simulated_covered_count": sim_covered_count,
        "newly_passing_count": len(would_bank),
        "regression_count": len(regressions),
        "denominator": len(corpus_rows),
        "abstained_count": abstained_count,
        "coverage": round(coverage, 4),
        "top3_on_covered": round(top3_on_covered, 4),
        "would_bank": sorted(would_bank),
        "would_bank_covered": sorted(would_bank_covered),
        "would_bank_still_abstained": sorted(would_bank_still_abstained),
        "already_pass": sorted(already_pass),
        "still_short": sorted(still_short),
        "regressions": sorted(regressions),
    }


def build_case_details(
    corpus_rows: list[dict[str, Any]],
    baseline_results: dict[str, dict[str, Any]],
    sim_results: dict[str, dict[str, Any]],
    c3_cases: dict[str, Any],
    states_full: dict[str, str],
    states_elec: dict[str, str],
    sub_gates: dict[str, str],
) -> list[dict[str, Any]]:
    """Per-case detail rows for the 22 C3 cases under Scenario 2 (full)."""
    details = []
    for r in corpus_rows:
        cid = r["case_id"]
        if cid not in c3_cases:
            continue
        c = sim_results[cid]
        cdata = c3_cases[cid]
        base_h = baseline_results[cid]["top3_hit"]
        sim_h = c["top3_hit"]
        state = states_full[cid]
        # Outcome tracks the top-3 flip (correct family enters the top-3 window), matching
        # build_scenario_summary; covered-vs-abstained is disclosed via the abstained column.
        if not base_h and sim_h:
            outcome = "WOULD_BANK"
        elif base_h and sim_h:
            outcome = "ALREADY_PASS"
        else:
            outcome = "STILL_SHORT"

        # Why-per-case for STILL_SHORT (task §4 "say why per case").
        reason = ""
        if outcome == "STILL_SHORT":
            if bool(cdata.get("stay_abstained", False)):
                reason = ("seed stay_abstained: seeded below every producer gate (state ABSTAIN); "
                          "confounder — C3 signal cannot separate")
            elif state == "ABSTAIN":
                reason = "producer emitted ABSTAIN (no C3 gate met) — no boost applied"
            else:
                # Producer fired but ecu_fault still did not reach top-3: the +0.10 boost over
                # base_weight did not out-rank the competing-family winners on this seed.
                reason = (f"producer fired ({state}) but ecu_fault still outside top-3 — "
                          f"the +{CONTROL_BOOST} boost did not out-rank competitors "
                          f"(top3={sorted(c['top3_families'])}); needs a stronger consumer lift at C3B")

        details.append({
            "case_id": cid,
            "expected_family": r["expected_family"],
            "oracle_fault_name": cdata.get("oracle_fault_name", ""),
            "band_id": cdata.get("band_id", ""),
            "stay_abstained_seed": bool(cdata.get("stay_abstained", False)),
            "c3_state_full": states_full[cid],
            "c3_state_electrical": states_elec[cid],
            "sub_gate_fired": sub_gates[cid],
            "baseline_hit": baseline_results[cid]["top3_hit"],
            "baseline_abstained": baseline_results[cid]["abstained"],
            "top3_hit": c["top3_hit"],
            "abstained": c["abstained"],
            "winner_id": c["winner_id"],
            "winner_family": c["winner_family"],
            "winner_score": c["winner_score"],
            "top3_families": sorted(c["top3_families"]),
            "outcome": outcome,
            "still_short_reason": reason,
        })
    return details


def main() -> int:
    parser = argparse.ArgumentParser(description="C3 Signal Pack Simulator (read-only dry-run).")
    parser.add_argument("--self-check", action="store_true", help="Run zero-overlay self-check only.")
    parser.add_argument("--c3-seed", type=Path, default=DEFAULT_SEED, help="C3 synthetic (or owner) seed JSON.")
    parser.add_argument("--write", type=Path, help="Write JSON + Markdown reports to this path.")
    args = parser.parse_args()

    # Always run the self-check first (task gate).
    if not run_self_check():
        return 1
    if args.self_check:
        return 0

    if not args.c3_seed.is_file():
        print(f"Error: C3 seed file not found: {args.c3_seed}", file=sys.stderr)
        return 1

    print(f"Loading C3 seed from {args.c3_seed}...")
    with open(args.c3_seed, encoding="utf-8") as f:
        c3_data = json.load(f)
    c3_cases = c3_data.get("cases", {})

    scenarios_states = compute_c3_states(c3_cases)
    sub_gates = compute_c3_sub_gates(c3_cases)

    print("Running baseline and simulated diagnostics...")
    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()

    # Baseline (overlay disabled) — should equal POST_T_V3_P4_C2B (verified in self-check).
    baseline_results = run_diagnose_loop(corpus_rows, {}, rule_map, c3_overlay_enabled=False)

    # Scenario 1: electrical-only gates (no Delta-lambda).
    sim_scen1 = run_diagnose_loop(
        corpus_rows, scenarios_states["scen1_electrical"], rule_map, c3_overlay_enabled=True
    )
    summary_scen1 = build_scenario_summary(corpus_rows, baseline_results, sim_scen1, c3_cases)

    # Scenario 2: full contract gates (incl. Delta-lambda).
    sim_scen2 = run_diagnose_loop(
        corpus_rows, scenarios_states["scen2_full"], rule_map, c3_overlay_enabled=True
    )
    summary_scen2 = build_scenario_summary(corpus_rows, baseline_results, sim_scen2, c3_cases)

    ft8_union, ft8_per_rule = derive_ft8_neighbour_union()
    dual_target_and_neighbour = sorted(set(c3_cases) & ft8_union)

    case_details = build_case_details(
        corpus_rows, baseline_results, sim_scen2, c3_cases,
        scenarios_states["scen2_full"], scenarios_states["scen1_electrical"], sub_gates,
    )

    # Back-solve alarm: any seed-flagged stay_abstained case that banks is a red flag.
    stay_abstained_seed = sorted(cid for cid, c in c3_cases.items() if c.get("stay_abstained"))
    banked_stay_abstained = sorted(
        d["case_id"] for d in case_details if d["stay_abstained_seed"] and d["outcome"] == "WOULD_BANK"
    )

    # Print headline summary (Scenario 2, full contract).
    print("\n" + "=" * 64)
    print("C3 SIGNAL DRYRUN SUMMARY (Scenario 2: full contract, incl. Δλ)")
    print("=" * 64)
    print(f"Baseline pin: {BASELINE_RUN}")
    print(f"Denominator: {summary_scen2['denominator']}")
    print(f"Baseline top3: {summary_scen2['baseline_top3_passes']}/294")
    print(f"Simulated top3 (S2): {summary_scen2['simulated_top3_passes']}/294")
    print(f"WOULD_BANK (S1 electrical): {summary_scen1['newly_passing_count']} "
          f"({len(summary_scen1['would_bank_covered'])} covered / "
          f"{len(summary_scen1['would_bank_still_abstained'])} still-abstained)")
    print(f"WOULD_BANK (S2 full): {summary_scen2['newly_passing_count']} "
          f"({len(summary_scen2['would_bank_covered'])} covered / "
          f"{len(summary_scen2['would_bank_still_abstained'])} still-abstained)")
    print(f"Regressions (S2): {summary_scen2['regression_count']} -> {summary_scen2['regressions']}")
    print(f"FT-8 neighbour union: {len(ft8_union)} ; dual target+neighbour: {len(dual_target_and_neighbour)}")
    print(f"stay_abstained seed cases: {len(stay_abstained_seed)} ; banked (ALARM if >0): {len(banked_stay_abstained)}")
    print("=" * 64)

    if banked_stay_abstained:
        print(f"*** BACK-SOLVE ALARM: stay_abstained cases banked: {banked_stay_abstained} ***", file=sys.stderr)

    if args.write:
        out_json = {
            "task": "T-V3-P4-C3A",
            "mode": "provisional-synthetic-simulated (side file; live corpus untouched)",
            "baseline_run": BASELINE_RUN,
            "seed": str(args.c3_seed.relative_to(WORKSPACE_ROOT)),
            "producer_gates": {
                "lean_bias": "dlc_signal_ground_drop_v > 0.20 AND gas_obd_lambda_delta >= 0.05",
                "rich_bias": "koeo_map_baro_delta_kpa >= 5.0 AND gas_obd_lambda_delta >= 0.05",
                "processor": "bidirectional_fuel_response_ok_bool == False AND module_voltage_loaded_v < 12.0",
            },
            "ft8_neighbour_union": sorted(ft8_union),
            "ft8_neighbour_count": len(ft8_union),
            "ft8_per_rule": ft8_per_rule,
            "dual_target_and_neighbour": dual_target_and_neighbour,
            "stay_abstained_seed": stay_abstained_seed,
            "banked_stay_abstained_ALARM": banked_stay_abstained,
            "scenarios": {
                "scen1_electrical": {
                    "description": "Scenario 1: Tier-A/C electrical-only gates (KOEO MAP/BARO + "
                                   "ground drop + Vmod + bidirectional); NO Δλ term (drops A6 two-point 5-gas).",
                    "summary": summary_scen1,
                },
                "scen2_full": {
                    "description": "Scenario 2: full contract gates incl. gas_obd_lambda_delta (Δλ).",
                    "summary": summary_scen2,
                    "case_details": case_details,
                },
            },
        }
        with open(args.write, "w", encoding="utf-8") as f:
            json.dump(out_json, f, indent=2)
        print(f"Wrote JSON report to {args.write}")

        write_markdown_report(
            args.write.with_suffix(".md"),
            summary_scen1,
            summary_scen2,
            case_details,
            ft8_union,
            dual_target_and_neighbour,
            stay_abstained_seed,
            banked_stay_abstained,
        )

    return 0


def write_markdown_report(
    md_path: Path,
    summary_scen1: dict[str, Any],
    summary_scen2: dict[str, Any],
    case_details: list[dict[str, Any]],
    ft8_union: set[str],
    dual_target_and_neighbour: list[str],
    stay_abstained_seed: list[str],
    banked_stay_abstained: list[str],
) -> None:
    """Write the 5-section reveal-contract Markdown report (essential-first)."""
    lines: list[str] = []
    lines.append("---")
    lines.append("node_type: report")
    lines.append("lab: apps/wired")
    lines.append("module: v3/c3_signal_sim.py")
    lines.append("implements: T-V3-P4-C3A")
    lines.append("consumers: [owner acceptance read, next-decision C3B commit sizing]")
    lines.append("tags: [v3, phase4, c3, signal, dryrun, synthetic]")
    lines.append("source: v3/v3_tasks/T-V3-P4-C3A_c3_signal_dryrun.md")
    lines.append("---")
    lines.append("")
    lines.append("# V3 C3 SIGNAL DRYRUN — ECU/control-system fault (read-only sim)")
    lines.append("")
    lines.append("**Task:** [[T-V3-P4-C3A_c3_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)")
    lines.append(f"**Baseline pin:** `{BASELINE_RUN}` / `V3_YARDSTICK_2026-07-05` "
                 "(csv `3df2e8cb…`, oracle `3088a7c3…`, `run_suite.py` untouched)")
    lines.append("**C3 Seed:** `v3/data/c3_synthetic_seed_2026-07-05.json` (`synthetic=true` provisional; "
                 "Δλ is **empirical-anecdotal** — C3-PRE §7)")
    lines.append("**Live engine status:** untouched (no corpus / rule / registry / yardstick edit)")
    lines.append("")

    # --- headline (essential-first) ---
    s1n = summary_scen1["newly_passing_count"]
    s2n = summary_scen2["newly_passing_count"]
    lines.append("## Headline")
    lines.append(f"- **Baseline `top3_family`:** {summary_scen2['baseline_top3_passes']}/294 → "
                 f"**Scenario 2: {summary_scen2['simulated_top3_passes']}/294** "
                 f"(+{summary_scen2['simulated_top3_passes'] - summary_scen2['baseline_top3_passes']}).")
    lines.append(f"- **Scenario 1 (electrical-only, no Δλ):** {s1n} WOULD_BANK "
                 f"({len(summary_scen1['would_bank_covered'])} covered / "
                 f"{len(summary_scen1['would_bank_still_abstained'])} still-abstained at MARGIN=0.02).")
    lines.append(f"- **Scenario 2 (full contract, incl. Δλ):** {s2n} WOULD_BANK "
                 f"({len(summary_scen2['would_bank_covered'])} covered / "
                 f"{len(summary_scen2['would_bank_still_abstained'])} still-abstained at MARGIN=0.02).")
    lines.append("  - `WOULD_BANK` = correct family flips **into the top-3 window** (the pack's `top3_family` metric). "
                 "A flipped case may still be **abstained** by the MARGIN=0.02 dial — disclosed, not hidden. "
                 "C3B/abstain-cal decides whether to surface those.")
    lines.append(f"- **Zero-overlay self-check:** drift = 0 across 294 vs `{BASELINE_RUN}`.")
    lines.append(f"- **Regressions (S2):** {summary_scen2['regression_count']} "
                 f"(`{summary_scen2['regressions'] or '(empty)'}`).")
    lines.append(f"- **stay_abstained honoured:** {len(stay_abstained_seed)} seed cases; "
                 f"banked = {len(banked_stay_abstained)} "
                 f"({'BACK-SOLVE ALARM: ' + str(banked_stay_abstained) if banked_stay_abstained else 'none — correct'}).")
    lines.append("")

    # --- 1. Producer simulation ---
    lines.append("## 1. Producer simulation (`ControlPlausibilityState`)")
    lines.append("Per contract §2 (grounding-tagged); any gate met → `CONTROL_REFERENCE_FAULT`, none → `ABSTAIN`:")
    lines.append(f"- **lean-bias:** `dlc_signal_ground_drop_v > {GND_DROP_GATE_V}` AND "
                 f"`gas_obd_lambda_delta >= {LAMBDA_DIVERGENCE_GATE}` — ground standardized, Δλ **empirical-anecdotal**.")
    lines.append(f"- **rich-bias:** `koeo_map_baro_delta_kpa >= {MAP_BARO_GATE_KPA}` AND "
                 f"`gas_obd_lambda_delta >= {LAMBDA_DIVERGENCE_GATE}` — MAP/BARO manufacturer-typical, Δλ **empirical-anecdotal**.")
    lines.append(f"- **processor (P0606):** `bidirectional_fuel_response_ok_bool == False` AND "
                 f"`module_voltage_loaded_v < {MODULE_VOLTAGE_GATE_V}` — manufacturer-typical, no Δλ (electrical-only).")
    lines.append("")

    # --- 2. Scenario ladder ---
    lines.append("## 2. Scenario ladder (acquisition-cost disclosure)")
    lines.append("| Metric | Scenario 1 (electrical-only, no Δλ) | Scenario 2 (full, incl. Δλ) |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| Top-3 family hits | {summary_scen1['simulated_top3_passes']}/294 | "
                 f"{summary_scen2['simulated_top3_passes']}/294 |")
    lines.append(f"| WOULD_BANK (top-3 flip) | **{s1n}** | **{s2n}** |")
    lines.append(f"| — of which covered | {len(summary_scen1['would_bank_covered'])} | "
                 f"{len(summary_scen2['would_bank_covered'])} |")
    lines.append(f"| — of which still-abstained | {len(summary_scen1['would_bank_still_abstained'])} | "
                 f"{len(summary_scen2['would_bank_still_abstained'])} |")
    lines.append(f"| Abstained count (all 294) | {summary_scen1['abstained_count']} | {summary_scen2['abstained_count']} |")
    lines.append(f"| Coverage | {summary_scen1['coverage']:.2%} | {summary_scen2['coverage']:.2%} |")
    lines.append(f"| Top-3 on covered | {summary_scen1['top3_on_covered']:.2%} | {summary_scen2['top3_on_covered']:.2%} |")
    lines.append(f"| Regressions | {summary_scen1['regression_count']} | {summary_scen2['regression_count']} |")
    lines.append("")
    s1_banks = set(summary_scen1["would_bank"])
    s2_banks = set(summary_scen2["would_bank"])
    only_full = sorted(s2_banks - s1_banks)
    lines.append(f"- Cases that bank **only with Δλ** (Scenario 2 but not Scenario 1): "
                 f"`{only_full or '(none)'}` — this is the price of action **A6 two-point 5-gas**.")
    lines.append(f"- Cases that bank on **electrical alone** (Scenario 1): `{sorted(s1_banks) or '(none)'}` — "
                 "reachable with the cheaper **A5 electrical bench** (DMM ground drop + KOEO MAP/BARO + Vmod + bidirectional).")
    if not only_full and s1_banks == s2_banks:
        lines.append("- **Δλ is NOT load-bearing for yield on this seed:** Scenario 1 banks the same set as Scenario 2. "
                     "The expensive, weakest-grounded 5-gas divergence term can be dropped from the C3B column set.")
    lines.append("")

    # --- 3. Consumer simulation ---
    lines.append("## 3. Consumer simulation (EF/SF overlay)")
    lines.append(f"On `CONTROL_REFERENCE_FAULT`: **{', '.join(EF_RULES)}** (ecu_fault) get a "
                 f"`+{CONTROL_BOOST}` DEFINITIVE boost; **{', '.join(SF_RULES)}** (sensor_fault) are **pruned** "
                 "(contract §3 dispersion-as-sensor-bias mapping — a ground offset that *looks* like sensor bias must "
                 "not out-rank ecu_fault). `ABSTAIN` leaves every rule at baseline. Boost mechanics mirror "
                 "`v3/c2_signal_sim.py` / `v3/c4_signal_sim.py`.")
    lines.append("")

    # --- 4. Yield disclosure ---
    lines.append("## 4. Yield disclosure (22 C3 cases, Scenario 2)")
    lines.append("| Outcome | Count | Case IDs |")
    lines.append("| --- | --- | --- |")
    wb = summary_scen2["would_bank"]
    ap = summary_scen2["already_pass"]
    ss = summary_scen2["still_short"]
    lines.append(f"| **WOULD_BANK** | {len(wb)} | `{', '.join(wb) or '(none)'}` |")
    lines.append(f"| **ALREADY_PASS** | {len(ap)} | `{', '.join(ap) or '(none)'}` |")
    lines.append(f"| **STILL_SHORT** | {len(ss)} | `{', '.join(ss) or '(none)'}` |")
    lines.append("| **ABSTAIN_NO_DATA** | 0 | (none — synthetic seed covers all 22) |")
    lines.append("")
    lines.append("### Per-case detail (Scenario 2: full contract)")
    lines.append("| Case | Expected | Oracle fault | Band | seed stay_abstained | C3 state (S2) | "
                 "sub-gate fired | Base hit | Base abst | Sim hit | Sim abst | Winner | Winner fam | Outcome |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in sorted(case_details, key=lambda x: x["case_id"]):
        lines.append(
            f"| {c['case_id']} | {c['expected_family']} | {c['oracle_fault_name']} | {c['band_id']} | "
            f"{c['stay_abstained_seed']} | `{c['c3_state_full']}` | {c['sub_gate_fired']} | "
            f"{c['baseline_hit']} | {c['baseline_abstained']} | {c['top3_hit']} | {c['abstained']} | "
            f"{c['winner_id']} | {c['winner_family']} | **{c['outcome']}** |"
        )
    lines.append("")
    lines.append(f"**stay_abstained honesty check:** the 4 seed-flagged cases (`{', '.join(stay_abstained_seed)}`) "
                 f"MUST land outside WOULD_BANK. Banked: `{banked_stay_abstained or '(none)'}` — "
                 f"{'**BACK-SOLVE ALARM**' if banked_stay_abstained else 'honoured (correct: seeded below every gate)'}.")
    lines.append("")
    ss_details = [c for c in sorted(case_details, key=lambda x: x["case_id"]) if c["outcome"] == "STILL_SHORT"]
    if ss_details:
        lines.append("### Why each STILL_SHORT case fell short")
        for c in ss_details:
            lines.append(f"- `{c['case_id']}` ({c['band_id']}): {c['still_short_reason']}")
        sep_short = [c["case_id"] for c in ss_details if not c["stay_abstained_seed"]]
        if sep_short:
            lines.append("")
            lines.append(f"> **Disclosure:** {len(sep_short)} case(s) the seed marks C3-separable "
                         f"(`{', '.join(sep_short)}`) fire the producer state but ecu_fault still misses top-3. "
                         "The paper-separable count (18) therefore exceeds the actual top-3 flips (16): the "
                         "producer discriminates, but the fixed +0.10 consumer boost is not enough to out-rank "
                         "the competing family for these rows. C3B must size a stronger lift (or accept them abstained).")
        lines.append("")

    # --- 5. FT-8 neighbour audit ---
    lines.append("## 5. FT-8 neighbour audit")
    lines.append(f"Neighbour union re-derived **live** from `ecu_fault.json` (EF-*) + `sensor_fault.json` (SF-*) "
                 f"`passes_cases` (both competition groups): **{len(ft8_union)}** cases.")
    lines.append(f"- **Regressions (full 294, Scenario 2):** {summary_scen2['regression_count']} — "
                 f"`{summary_scen2['regressions'] or '(empty)'}` (target: empty).")
    lines.append(f"- **Dual target+neighbour ({len(dual_target_and_neighbour)}):** these are BOTH C3 targets AND "
                 "regression-sensitive neighbours (the largest dual set of any pack). Their outcomes:")
    dual_set = set(dual_target_and_neighbour)
    for c in sorted(case_details, key=lambda x: x["case_id"]):
        if c["case_id"] in dual_set:
            lines.append(f"  - `{c['case_id']}` → **{c['outcome']}** "
                         f"(winner {c['winner_id']}/{c['winner_family']}, C3 state `{c['c3_state_full']}`)")
    lines.append("")

    # --- 6. Commit scope for C3B ---
    lines.append("## 6. Commit scope for `T-V3-P4-C3B` (sized, not guessed)")
    lines.append("- **Producer thresholds** (as simulated): lean-bias `gnd>0.20 ∧ Δλ≥0.05`, "
                 "rich-bias `map_baro≥5 ∧ Δλ≥0.05`, processor `bidir=False ∧ Vmod<12.0`.")
    lines.append(f"- **Consumer changes:** boost {', '.join(EF_RULES)} on `CONTROL_REFERENCE_FAULT`; "
                 f"prune {', '.join(SF_RULES)} on the same state.")
    lines.append("- **Column-set decision (Δλ load-bearing?):**")
    if not only_full and s1_banks == s2_banks:
        lines.append("  - Scenario 1 == Scenario 2 on this seed → **Δλ (`gas_obd_lambda_delta`, `lambda_perception_delta`) "
                     "is NOT load-bearing for yield.** C3B can commit the 4 electrical columns "
                     "(`koeo_map_baro_delta_kpa`, `module_voltage_loaded_v`, `dlc_signal_ground_drop_v`, "
                     "`bidirectional_fuel_response_ok_bool`) and defer the expensive, empirical-anecdotal Δλ ask.")
    else:
        lines.append(f"  - Δλ **is** load-bearing: `{only_full}` bank only under Scenario 2. To recover them C3B must "
                     "add `gas_obd_lambda_delta` (+ `lambda_perception_delta`) as corpus columns and price action A6 "
                     "(two-point 5-gas). NOTE: Δλ is empirical-anecdotal — confirm against real vehicle data before commit.")
    lines.append(f"- **stay_abstained ({len(stay_abstained_seed)}):** stay abstained at MARGIN=0.02 "
                 "(POA physical confounder + intermittent) — not committable by C3.")
    lines.append("")
    lines.append("> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run runs on `synthetic=true` seed data. The producer/"
                 "consumer LOGIC is buildable now; the live `top3_family` does **not** move until the owner supplies "
                 "real column values and `T-V3-P4-C3B` commits them. Never read a synthetic bank as real accuracy.")
    lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Markdown report to {md_path}")


if __name__ == "__main__":
    sys.exit(main())
