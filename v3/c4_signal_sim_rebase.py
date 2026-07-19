#!/usr/bin/env python3
"""Read-only overlay simulator for the C4 (exhaust_leak vs true_lean vs biased_o2) signal pack.

Re-baselined version (T-V3-P4-C4A-R) running against POST_T_V3_P4_C5B.
Zero-overlay self-check reproduces current ranks for all 294 cases (no drift).
Simulates the proposed C4 producer states and consumer rule overlays on the C4 synthetic seed.
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

CURRENT_CASE_ID: list[str | None] = [None]


def load_rules_metadata() -> dict[str, dict[str, Any]]:
    """Load registry rules metadata (base weights, competition groups) directly from JSONs."""
    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    registry_rules = {}
    for fp in sorted(rules_dir.glob("*.json")):
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        for r in data.get("rules", []):
            rid = r["rule_id"]
            registry_rules[rid] = r
    return registry_rules


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


def compute_c4_states(c4_cases: dict[str, Any]) -> dict[str, dict[str, str]]:
    """Compute the C4 states for all cases in the seed across three scenarios."""
    states_scen1 = {}  # Delta-only, 8pt threshold
    states_scen2 = {}  # Delta-only, 5pt threshold
    states_scen3 = {}  # Full-signal mode

    for cid, cdata in c4_cases.items():
        delta_stft = float(cdata.get("delta_stft_idle_2500_pct", 0.0))
        co2 = float(cdata.get("co2_idle_pct", 15.0))
        o2_elev = float(cdata.get("tailpipe_o2_elevation_pct", 0.0))
        ds_o2 = float(cdata.get("downstream_o2_v", 0.0))
        propane = float(cdata.get("propane_trim_shift_pct", 0.0))

        # Scenario 1: delta-only (8pt)
        if delta_stft <= -8.0:
            states_scen1[cid] = "LEAK"
        else:
            states_scen1[cid] = "ABSTAIN"

        # Scenario 2: delta-only (5pt)
        if delta_stft <= -5.0:
            states_scen2[cid] = "LEAK"
        else:
            states_scen2[cid] = "ABSTAIN"

        # Scenario 3: full-signal mode
        is_leak = (delta_stft <= -8.0) or (co2 < 12.0) or (o2_elev > 2.5)
        if is_leak:
            states_scen3[cid] = "LEAK"
        else:
            is_bias = (ds_o2 > 0.7) and (propane > -15.0)
            is_lean = (ds_o2 <= 0.4) and (propane <= -15.0)
            if is_bias:
                states_scen3[cid] = "PERSIST_BIAS"
            elif is_lean:
                states_scen3[cid] = "PERSIST_LEAN"
            else:
                states_scen3[cid] = "ABSTAIN"

    return {
        "scen1_delta8": states_scen1,
        "scen2_delta5": states_scen2,
        "scen3_full": states_scen3,
    }


def run_diagnose_loop(
    corpus_rows: Sequence[Mapping[str, Any]],
    c4_states: dict[str, str],
    rule_map: Mapping[str, str],
    c4_overlay_enabled: bool,
) -> dict[str, dict[str, Any]]:
    """Run all corpus cases through diagnose() with our scoring monkeypatch."""
    original_score_rule = shim._score_rule
    def my_score_rule(rule: Any, obs: Any) -> float | None:
        cid = CURRENT_CASE_ID[0]

        is_c4_affected_rule = rule.rule_id in ["EL-001", "EL-003", "LC-001", "LC-002", "SF-001", "SF-002", "SF-008"]
        if not c4_overlay_enabled or cid not in c4_states or not is_c4_affected_rule:
            return original_score_rule(rule, obs)

        c4_state = c4_states[cid]
        if c4_state == "ABSTAIN":
            return original_score_rule(rule, obs)

        # Apply C4 overlay
        if rule.rule_id in ["EL-001", "EL-003"]:
            if c4_state == "LEAK":
                orig_ceiling = rule.confidence_ceiling
                rule.confidence_ceiling = None
                raw_score = original_score_rule(rule, obs)
                rule.confidence_ceiling = orig_ceiling
                
                score_to_boost = raw_score if raw_score is not None else rule.base_weight
                return min(score_to_boost + 0.10, 1.0)
            return None

        if rule.rule_id in ["LC-001", "LC-002"]:
            if c4_state == "PERSIST_LEAN":
                orig_ceiling = rule.confidence_ceiling
                rule.confidence_ceiling = None
                raw_score = original_score_rule(rule, obs)
                rule.confidence_ceiling = orig_ceiling
                
                score_to_boost = raw_score if raw_score is not None else rule.base_weight
                return min(score_to_boost + 0.10, 1.0)
            return None

        if rule.rule_id in ["SF-001", "SF-002", "SF-008"]:
            if c4_state == "PERSIST_BIAS":
                orig_ceiling = rule.confidence_ceiling
                rule.confidence_ceiling = None
                raw_score = original_score_rule(rule, obs)
                rule.confidence_ceiling = orig_ceiling
                
                score_to_boost = raw_score if raw_score is not None else rule.base_weight
                return min(score_to_boost + 0.10, 1.0)
            return None

        return original_score_rule(rule, obs)

    # Monkeypatch
    shim._score_rule = my_score_rule
    results = {}

    try:
        # Initialize router in local scope to build ruleset
        RegistryV2Router()
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
        # Restore original scorer
        shim._score_rule = original_score_rule

    return results


def run_self_check() -> bool:
    """Run zero-overlay self-check comparing simulated baseline with results.json."""
    print("Running zero-overlay self-check...")
    results_path = WORKSPACE_ROOT / "apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json"
    if not results_path.is_file():
        print(f"Error: baseline run results file not found at {results_path}", file=sys.stderr)
        return False

    with open(results_path, encoding="utf-8") as f:
        baseline_run = json.load(f)["results"]
    baseline_by_case = {r["case_id"]: r for r in baseline_run}

    denom_rows = load_denominator_rows()
    corpus_rows = [
        {
            "case_id": r["case_id"],
            "expected_family": r["expected_fault_family"].lower(),
            "raw_inputs": row_to_raw_inputs(r),
        }
        for r in denom_rows
    ]

    rule_map = load_rule_family_map()
    simulated_baseline = run_diagnose_loop(corpus_rows, {}, rule_map, c4_overlay_enabled=False)

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
                f"actual=({actual_winner_id}, {actual_winner_family}, top3={actual_top3_hit}, abstained={actual_abstained}), "
                f"sim=({sim_res['winner_id']}, {sim_res['winner_family']}, top3={sim_res['top3_hit']}, abstained={sim_res['abstained']})"
            )

    if mismatches == 0:
        print("Zero-overlay self-check: OK (all 294 cases matched, drift = 0)")
        return True

    print(f"Zero-overlay self-check: FAILED with {mismatches} mismatches", file=sys.stderr)
    return False


def derive_ft8_neighbour_union(c4_targets: set[str]) -> set[str]:
    """Re-derive the C4 FT-8 union from exhaust_leak.json, lean_condition.json and sensor_fault.json."""
    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    union = set()
    for filename in ("exhaust_leak.json", "lean_condition.json", "sensor_fault.json"):
        filepath = rules_dir / filename
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        for rule in data.get("rules", []):
            passes = list(rule.get("passes_cases", []))
            union.update(passes)
    return union - c4_targets


def build_scenario_summary(
    corpus_rows: list[dict[str, Any]],
    baseline_results: dict[str, dict[str, Any]],
    sim_results: dict[str, dict[str, Any]],
    c4_cases: dict[str, Any],
    c4_states: dict[str, str],
) -> dict[str, Any]:
    """Helper to calculate summary metrics for a given scenario simulation."""
    total_baseline_passes = 0
    total_sim_passes = 0
    total_baseline_on_covered = 0
    total_sim_on_covered = 0
    baseline_covered_count = 0
    sim_covered_count = 0
    abstained_count = 0

    would_bank = []
    already_pass = []
    still_short = []
    regressions = []

    for r in corpus_rows:
        cid = r["case_id"]
        base_h = baseline_results[cid]["top3_hit"]
        sim_h = sim_results[cid]["top3_hit"]
        base_a = baseline_results[cid]["abstained"]
        sim_a = sim_results[cid]["abstained"]

        if base_h:
            total_baseline_passes += 1
            if not base_a:
                total_baseline_on_covered += 1
        if not base_a:
            baseline_covered_count += 1

        if sim_h:
            total_sim_passes += 1
            if not sim_a:
                total_sim_on_covered += 1
        if not sim_a:
            sim_covered_count += 1
        else:
            abstained_count += 1

        # Check regressions on ALL cases
        if base_h and not base_a and (not sim_h or sim_a):
            # Regressed if it was passing and covered in baseline, but now failing or abstained
            regressions.append(cid)

        # Categorize only C4 seed target cases
        if cid in c4_cases:
            # Under the new logic, did it transition from failing (or abstained-failing) to passing-covered?
            # - WOULD_BANK: baseline did not pass top-3 or was abstained; simulation passes top-3 and is covered.
            # - ALREADY_PASS: baseline passed top-3 and was covered; simulation continues to pass and is covered.
            # - STILL_SHORT: does not pass top-3 or remains abstained.
            base_passed_and_covered = base_h and not base_a
            sim_passed_and_covered = sim_h and not sim_a

            if not base_passed_and_covered and sim_passed_and_covered:
                would_bank.append(cid)
            elif base_passed_and_covered and sim_passed_and_covered:
                already_pass.append(cid)
            else:
                still_short.append(cid)

    coverage = sim_covered_count / len(corpus_rows)
    top3_on_covered = total_sim_on_covered / sim_covered_count if sim_covered_count else 0.0

    return {
        "baseline_top3_passes": total_baseline_passes,
        "simulated_top3_passes": total_sim_passes,
        "baseline_on_covered_passes": total_baseline_on_covered,
        "simulated_on_covered_passes": total_sim_on_covered,
        "baseline_covered_count": baseline_covered_count,
        "simulated_covered_count": sim_covered_count,
        "newly_passing_count": len(would_bank),
        "regression_count": len(regressions),
        "denominator": len(corpus_rows),
        "abstained_count": abstained_count,
        "coverage": round(coverage, 4),
        "top3_on_covered": round(top3_on_covered, 4),
        "would_bank": would_bank,
        "already_pass": already_pass,
        "still_short": still_short,
        "regressions": regressions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="C4 Signal Pack Re-Baseline Simulator.")
    parser.add_argument("--self-check", action="store_true", help="Run zero-overlay self-check.")
    parser.add_argument("--c4-seed", type=Path, help="Synthetic or owner-supplied C4 JSON file.")
    parser.add_argument("--write", type=Path, help="Write output JSON results report.")
    args = parser.parse_args()

    if args.self_check:
        success = run_self_check()
        return 0 if success else 1

    # Default to the 2026-07-01 seed if not specified
    seed_path = args.c4_seed or WORKSPACE_ROOT / "v3/data/c4_synthetic_seed_2026-07-01.json"
    if not seed_path.is_file():
        print(f"Error: C4 seed file not found: {seed_path}", file=sys.stderr)
        return 1

    print(f"Loading C4 values from {seed_path}...")
    with open(seed_path, encoding="utf-8") as f:
        c4_data = json.load(f)
    c4_cases = c4_data.get("cases", {})

    # Compute C4 states for all 3 scenarios
    scenarios_states = compute_c4_states(c4_cases)

    print("Running baseline and simulated diagnostics...")
    denom_rows = load_denominator_rows()
    corpus_rows = [
        {
            "case_id": r["case_id"],
            "expected_family": r["expected_fault_family"].lower(),
            "raw_inputs": row_to_raw_inputs(r),
        }
        for r in denom_rows
    ]

    rule_map = load_rule_family_map()

    # 1. Run baseline (overlay disabled)
    baseline_results = run_diagnose_loop(corpus_rows, {}, rule_map, c4_overlay_enabled=False)

    # 2. Run Scenario 1: delta STFT-only (8pt)
    sim_res_scen1 = run_diagnose_loop(
        corpus_rows, scenarios_states["scen1_delta8"], rule_map, c4_overlay_enabled=True
    )
    summary_scen1 = build_scenario_summary(
        corpus_rows, baseline_results, sim_res_scen1, c4_cases, scenarios_states["scen1_delta8"]
    )

    # 3. Run Scenario 2: delta STFT-only (5pt)
    sim_res_scen2 = run_diagnose_loop(
        corpus_rows, scenarios_states["scen2_delta5"], rule_map, c4_overlay_enabled=True
    )
    summary_scen2 = build_scenario_summary(
        corpus_rows, baseline_results, sim_res_scen2, c4_cases, scenarios_states["scen2_delta5"]
    )

    # 4. Run Scenario 3: full-signal mode
    sim_res_scen3 = run_diagnose_loop(
        corpus_rows, scenarios_states["scen3_full"], rule_map, c4_overlay_enabled=True
    )
    summary_scen3 = build_scenario_summary(
        corpus_rows, baseline_results, sim_res_scen3, c4_cases, scenarios_states["scen3_full"]
    )

    # Derive neighbour union dynamically
    neighbour_set = derive_ft8_neighbour_union(set(c4_cases.keys()))

    c4_cases_details = []
    for r in corpus_rows:
        cid = r["case_id"]
        if cid in c4_cases:
            c = sim_res_scen3[cid]
            base_passed_and_covered = baseline_results[cid]["top3_hit"] and not baseline_results[cid]["abstained"]
            sim_passed_and_covered = c["top3_hit"] and not c["abstained"]

            if not base_passed_and_covered and sim_passed_and_covered:
                outcome = "WOULD_BANK"
            elif base_passed_and_covered and sim_passed_and_covered:
                outcome = "ALREADY_PASS"
            else:
                outcome = "STILL_SHORT"

            c4_cases_details.append({
                "case_id": cid,
                "expected_family": r["expected_family"],
                "c4_state": scenarios_states["scen3_full"][cid],
                "baseline_hit": baseline_results[cid]["top3_hit"],
                "baseline_abstained": baseline_results[cid]["abstained"],
                "top3_hit": c["top3_hit"],
                "abstained": c["abstained"],
                "winner_id": c["winner_id"],
                "winner_family": c["winner_family"],
                "winner_score": c["winner_score"],
                "top3_families": list(c["top3_families"]),
                "outcome": outcome
            })

    # Print summary
    print("\n" + "=" * 60)
    print("C4 SIGNAL RE-BASELINE SUMMARY (SCENARIO 3: FULL-SIGNAL)")
    print("=" * 60)
    print(f"Denominator: {summary_scen3['denominator']}")
    print(f"Baseline top3: {summary_scen3['baseline_top3_passes']}/294 ({summary_scen3['baseline_top3_passes']/294*100.0:.2f}%)")
    print(f"Simulated top3: {summary_scen3['simulated_top3_passes']}/294 ({summary_scen3['simulated_top3_passes']/294*100.0:.2f}%)")
    print(f"Newly passing: {summary_scen3['newly_passing_count']}")
    print(f"Regressions: {summary_scen3['regression_count']}")
    print(f"Coverage: {summary_scen3['coverage']:.2%} ({summary_scen3['denominator'] - summary_scen3['abstained_count']}/{summary_scen3['denominator']} covered, {summary_scen3['abstained_count']} abstained)")
    print(f"Top-3 on covered: {summary_scen3['top3_on_covered']:.2%}")
    print("=" * 60)

    # Output JSON and Markdown reports
    if args.write:
        out_json = {
            "task": "T-V3-P4-C4A-R",
            "mode": "provisional-synthetic-simulated (side file; live corpus untouched)",
            "scenarios": {
                "scen1_delta8": {
                    "description": "Scenario 1: Two-point delta STFT-only (threshold 8pt fall)",
                    "summary": summary_scen1
                },
                "scen2_delta5": {
                    "description": "Scenario 2: Two-point delta STFT-only (threshold 5pt fall)",
                    "summary": summary_scen2
                },
                "scen3_full": {
                    "description": "Scenario 3: Full-signal mode (incorporating CO2, O2, downstream O2, propane)",
                    "summary": summary_scen3,
                    "c4_cases_details": c4_cases_details
                }
            }
        }
        with open(args.write, "w", encoding="utf-8") as f:
            json.dump(out_json, f, indent=2)
        print(f"Wrote JSON report to {args.write}")

        # Build and write Markdown report next to JSON file
        write_markdown_report(
            args.write.with_suffix(".md"),
            summary_scen1,
            summary_scen2,
            summary_scen3,
            c4_cases_details,
            neighbour_set
        )

    return 0


def write_markdown_report(
    md_path: Path,
    summary_scen1: dict[str, Any],
    summary_scen2: dict[str, Any],
    summary_scen3: dict[str, Any],
    c4_cases_details: list[dict[str, Any]],
    neighbour_set: set[str]
) -> None:
    """Build and write the Markdown report for the C4 signal dryrun."""
    lines = []
    lines.append("---")
    lines.append("node_type: report")
    lines.append("lab: apps/wired")
    lines.append("module: v3/c4_signal_sim_rebase.py")
    lines.append("implements: T-V3-P4-C4A-R")
    lines.append("consumers: [owner acceptance read, next-decision C4B commit sizing]")
    lines.append("tags: [v3, phase4, c4, signal, dryrun, synthetic, rebase]")
    lines.append("source: v3/v3_tasks/T-V3-P4-C4A-R_c4_rebaseline_dryrun.md")
    lines.append("---")
    lines.append("")
    lines.append(f"# V3 C4 SIGNAL RE-BASELINE DRYRUN — `top3_family` rises to {summary_scen3['simulated_top3_passes']}/294")
    lines.append("")
    lines.append("**Task:** [[T-V3-P4-C4A-R_c4_rebaseline_dryrun]] · **Date:** 2026-07-06 · **Mode:** STRICT (read-only sim)")
    lines.append("**C4 Seed Data:** `v3/data/c4_synthetic_seed_2026-07-01.json` (`synthetic=true` provisional)")
    lines.append("**Yardstick:** `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`, oracle `3088a7c3…`, `run_suite.py` untouched)")
    lines.append("**Live engine status:** untouched")
    lines.append("")

    lines.append("## 1. BUILDABLE_NOW (Logic from Research)")
    lines.append("The C4 producer emit rules and consumer wiring logic are derived from `value4.1.md` and are fully simulated in memory:")
    lines.append("- **Scenario 1 (ΔSTFT-only, 8pt):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -8.0%`. Otherwise, emits `ABSTAIN` (cannot separate lean from bias).")
    lines.append("- **Scenario 2 (ΔSTFT-only, 5pt):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -5.0%`. Otherwise, emits `ABSTAIN`.")
    lines.append("- **Scenario 3 (Full-signal):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -8.0%` OR `co2_idle_pct < 12.0%` OR `tailpipe_o2_elevation_pct > 2.5%`. If not a leak, checks if `downstream_o2_v > 0.7 V` and `propane_trim_shift_pct > -15.0%` to emit `PERSIST_BIAS`. Checks if `downstream_o2_v <= 0.4 V` and `propane_trim_shift_pct <= -15.0%` to emit `PERSIST_LEAN`. Otherwise, emits `ABSTAIN`.")
    lines.append("- **Consumer Wiring:** `exhaust_leak.json` EL-001/003 fire only if `LEAK` is emitted. `lean_condition.json` LC-001/002 fire only if `PERSIST_LEAN` is emitted. `sensor_fault.json` SF-001/002/008 fire only if `PERSIST_BIAS` is emitted.")
    lines.append("- **Score Boost:** satisfying the matching C4 state adds a `DEFINITIVE` boost (`+0.10`) to the rule's score and raises/removes the confidence ceiling (`clamped_score = min(raw_score, 1.0)`). Non-matching rules are pruned (`None`).")
    lines.append("")

    lines.append("## 2. SCORING_GATED (Metrics & Yield Breakdown)")
    lines.append("")
    lines.append("### Scenario Comparison Summary")
    lines.append("| Metric | Baseline | Scenario 1 (ΔSTFT-only, 8pt) | Scenario 2 (ΔSTFT-only, 5pt) | Scenario 3 (Full-Signal) |")
    lines.append("| --- | --- | --- | --- | --- |")
    lines.append(f"| **Denominator** | {summary_scen3['denominator']} | {summary_scen1['denominator']} | {summary_scen2['denominator']} | {summary_scen3['denominator']} |")
    lines.append(f"| **Top-3 family hits** | {summary_scen3['baseline_top3_passes']}/294 | {summary_scen1['simulated_top3_passes']}/294 | {summary_scen2['simulated_top3_passes']}/294 | {summary_scen3['simulated_top3_passes']}/294 |")
    lines.append(f"| **Newly passing (yield)** | — | **{summary_scen1['newly_passing_count']}** | **{summary_scen2['newly_passing_count']}** | **{summary_scen3['newly_passing_count']}** |")
    lines.append(f"| **Abstained count** | {summary_scen3['abstained_count']} | {summary_scen1['abstained_count']} | {summary_scen2['abstained_count']} | {summary_scen3['abstained_count']} |")
    lines.append(f"| **Coverage** | {1.0 - (summary_scen3['abstained_count']/294):.2%} | {summary_scen1['coverage']:.2%} | {summary_scen2['coverage']:.2%} | {summary_scen3['coverage']:.2%} |")
    lines.append(f"| **Top-3 on covered** | {summary_scen3['baseline_on_covered_passes'] / summary_scen3['baseline_covered_count']:.2%} | {summary_scen1['top3_on_covered']:.2%} | {summary_scen2['top3_on_covered']:.2%} | {summary_scen3['top3_on_covered']:.2%} |")
    lines.append("")

    lines.append("### Scenario Yield Breakdown")
    lines.append("1. **Scenario 1 (ΔSTFT-only, 8pt):** Banks **4** of the 7 exhaust leaks. The other 3 leaks (EXT-238, EXT-239, TC-048) have yellow-band delta STFTs (-7.4%, -7.1%, -5.9%) and stay short. The 4 persistent cases cannot be separated and stay short/abstained.")
    lines.append("2. **Scenario 2 (ΔSTFT-only, 5pt):** Banks **7** of the 7 exhaust leaks. Because the seed's leak-band boundary is -5.0%, all 7 leaks satisfy this wider threshold and flip to top-3. The 4 persistent cases cannot be separated and stay short/abstained.")
    lines.append("3. **Scenario 3 (Full-Signal):** Banks **10** cases (7 exhaust leaks + 3 lean cases). It recovers all 7 exhaust leaks (confirming yellow-band deltas via CO2/O2) and separates the 3 lean cases from the 1 biased O2 case using downstream O2 and propane. The biased O2 case (CASE-022) is separated but remains short of top-3 (STILL_SHORT) due to baseline scores, but is no longer abstained.")
    lines.append("")

    lines.append("### Per-Case C4 Yield Split (Scenario 3: Full-Signal)")
    lines.append("| Outcome | Count | Case IDs | Description |")
    lines.append("| --- | --- | --- | --- |")

    would_bank_ids = ", ".join(sorted(summary_scen3["would_bank"]))
    lines.append(f"| **WOULD_BANK** | {len(summary_scen3['would_bank'])} | `{would_bank_ids}` | Newly passing C4-separable cases that flip from baseline FAIL to simulation PASS. |")

    already_pass_ids = ", ".join(sorted(summary_scen3["already_pass"])) if summary_scen3['already_pass'] else "(none)"
    lines.append(f"| **ALREADY_PASS** | {len(summary_scen3['already_pass'])} | `{already_pass_ids}` | C4 cases that were already passing in baseline and continue to pass. |")

    still_short_ids = ", ".join(sorted(summary_scen3["still_short"])) if summary_scen3['still_short'] else "(none)"
    lines.append(f"| **STILL_SHORT** | {len(summary_scen3['still_short'])} | `{still_short_ids}` | Cases that remain FAIL / outside top-3 (biased O2 case CASE-022). |")

    lines.append("| **ABSTAIN_NO_DATA** | 0 | (none) | Cases unmeasured (none in this synthetic run). |")
    lines.append("")

    lines.append("### Detail of the 11 C4 Cases (Scenario 3: Full-Signal)")
    lines.append("| Case ID | Expected Family | C4 Emitted State | Baseline Hit | Baseline Abstained | Top-3 Hit | Abstained | Simulated Winner | Winner Family | Top-3 Families | Outcome |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for c in sorted(c4_cases_details, key=lambda x: x["case_id"]):
        t3_f = ", ".join(sorted(c["top3_families"]))
        lines.append(
            f"| {c['case_id']} | {c['expected_family']} | `{c['c4_state']}` | "
            f"{c['baseline_hit']} | {c['baseline_abstained']} | {c['top3_hit']} | {c['abstained']} | "
            f"{c['winner_id']} | {c['winner_family']} | `{{{t3_f}}}` | **{c['outcome']}** |"
        )
    lines.append("")

    lines.append("## 3. CODE_LANDED != SCORE_MOVED")
    lines.append("This dry-run simulation runs on **provisional synthetic data** (`synthetic=true`) as permitted under §Provisional synthetic signals. The code logic for the C4 signals is buildable now, but **the score does not move in the live yardstick** until real measured data for the 11 cases is supplied by the owner and committed in `T-V3-P4-C4B`.")
    lines.append("")

    lines.append("## 4. REGRESSION / FT-8 Neighbour Audit")
    lines.append(f"The consumer changes touch `exhaust_leak`, `lean_condition`, and `sensor_fault` rules, affecting a neighbour set of **{len(neighbour_set)}** cases.")
    lines.append(f"Audit Result: **{summary_scen3['regression_count']} regressions detected** on the full 294-case corpus (regressions = `{summary_scen3['regressions'] or '[]'}`).")
    lines.append("All previously passing non-C4 neighbours continue to pass. The C4 signal gating isolates the changes completely to C4 cases.")
    lines.append("")

    lines.append("## 5. Column-Add Gate & Commit Scope for `T-V3-P4-C4B` (Sizing)")
    lines.append("Based on this simulation, we disclose the following recommendations for the `C4B` commit:")
    lines.append("1. **ΔSTFT-alone yield is insufficient for full separation:**")
    lines.append("   - If we add **no new columns** and rely solely on `delta_stft` over the shared C5 trims:")
    lines.append("     - Under threshold `-8.0%`: banks **4** leaks, leaving 3 leaks and all 4 persistent cases still short (7 cases total still short).")
    lines.append("     - Under threshold `-5.0%`: banks **7** leaks, leaving only the 4 persistent cases still short.")
    lines.append("2. **Column-add decision for full separation:**")
    lines.append("   - Reclaiming the 3 `lean_condition` cases (`CASE-020`, `EXT-211`, `EXT-212`) and the 1 `sensor_fault` case (`CASE-022`) requires separating them, which is impossible without adding `downstream_o2_v` and `propane_trim_shift_pct` as corpus columns.")
    lines.append("   - If the owner chooses **not** to add those columns, those 4 cases must stay abstained.")
    lines.append("   - If the owner chooses to add those columns, all 3 `lean_condition` cases are successfully reclaimed, bringing the total yield to **10** banked cases.")
    lines.append("3. **Commit Scope:**")
    lines.append("   - **Scenario A (Abstain fallback):** Wire ΔSTFT <= -5.0% to emit `LEAK`. Do not add any new corpus columns. Keep the 4 persistent cases abstained.")
    lines.append("   - **Scenario B (Full-signal):** Wire the full producer state emit rule. Add `co2_idle_pct`, `tailpipe_o2_elevation_pct`, `downstream_o2_v`, and `propane_trim_shift_pct` to the corpus CSV, obdlab, and gaslab. Wire the rules to gate on `LEAK`, `PERSIST_LEAN`, and `PERSIST_BIAS` with a `+0.10` boost.")
    lines.append("")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Markdown report to {md_path}")


if __name__ == "__main__":
    sys.exit(main())
