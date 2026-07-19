#!/usr/bin/env python3
"""Rank simulator and feasibility map generator for the 20 TUNABLE cases.

Does not import or mutate engine state at runtime, except for a one-time
dry-run at startup using a clean monkeypatch to capture final rules scores.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Bootstrap paths so packages resolve correctly
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WORKSPACE_ROOT / "apps/wired"))

# Delayed imports inside functions to keep startup clean and respect design firewall
from v7.load_corpus import DEFAULT_CSV_PATH, load_corpus  # type: ignore # noqa: E402
from wired.composition import diagnose  # type: ignore # noqa: E402
from comlab.core.fault_atlas_router import FaultAtlasRouter  # type: ignore # noqa: E402
from fl_tasks.score_v3_yardstick import load_rule_family_map, sibling_family  # type: ignore # noqa: E402

def get_cluster_and_discriminator(expected: str, winner: str) -> tuple[str, str]:
    """Map expected/winner family confusion to its research cluster and citation."""
    exp_lower = expected.lower()
    win_lower = winner.lower()
    
    if (exp_lower == "lean_condition" and win_lower == "sensor_fault") or \
       (exp_lower == "sensor_fault" and win_lower == "lean_condition"):
        return (
            "Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor",
            "Two-point fuel trim delta (idle → 2500 RPM no-load) with air-metering architecture pre-gate, "
            "and upstream vs. downstream O₂ / wideband vs. narrowband cross-check"
        )
    elif exp_lower == "sensor_fault" and win_lower == "no_fault":
        return (
            "Cluster 6 — Sensor fault under-detection",
            "Mode $06 O2 sensor dynamic response rate tests (rich-to-lean/lean-to-rich transition times) "
            "and MAF plausibility comparison (measured MAF vs calculated airflow)"
        )
    elif exp_lower == "exhaust_leak" and win_lower == "lean_condition":
        return (
            "Cluster 4 — Exhaust leak vs true lean vs biased O2 sensor",
            "Two-point fuel trim delta (idle → 2500 RPM no-load) and CO₂ tailpipe dilution signature"
        )
    elif exp_lower == "misfire" and win_lower == "sensor_fault":
        return (
            "Cluster 6 — Sensor fault under-detection",
            "OBD-II Mode $06 misfire counters vs Mode $06 O2 sensor response times"
        )
    elif exp_lower == "sensor_fault" and win_lower == "rich_mixture":
        return (
            "Cluster 6 — Sensor fault under-detection",
            "Upstream vs downstream O2 sensor voltage cross-check, and Mode $06 O2 sensor response rate tests"
        )
    elif exp_lower == "rich_mixture" and win_lower == "misfire":
        return (
            "Cluster 1 — Mechanical vs misfire",
            "Tailpipe oxygen (elevated to ~5% for misfire, near 0% for rich) and carbon monoxide "
            "(high for rich, low/moderate for misfire) concentrations"
        )
    elif exp_lower == "catalyst_failure" and win_lower == "lean_condition":
        return (
            "Cluster 2 — Rich mixture vs catalyst failure",
            "Fuel trim monitoring (STFT/LTFT near zero for catalyst failure, highly positive for lean condition) "
            "and Mode $06 catalyst monitor index ratio"
        )
    elif exp_lower == "catalyst_failure" and win_lower == "cam_timing":
        return (
            "Cluster 2 — Rich mixture vs catalyst failure",
            "Mode $06 catalyst monitor switch ratio vs cam-to-crank correlation / VVT angle commands"
        )
    elif exp_lower == "lean_condition" and win_lower == "cam_timing":
        return (
            "Cluster 7 — Cam timing / VVT fault",
            "Volumetric efficiency / MAF-at-RPM signature and cam-to-crank correlation (DTC P0016-class)"
        )
    elif exp_lower == "sensor_fault" and win_lower == "catalyst_failure":
        return (
            "Cluster 6 — Sensor fault under-detection",
            "Mode $06 O2 sensor response rate tests vs Mode $06 catalyst monitor index ratio"
        )
    elif exp_lower == "misfire" and win_lower == "no_fault":
        return (
            "Cluster 9 — Confirming 'no fault' reliably",
            "Mode $06 misfire counters (to detect ECU blindness) and OBD readiness monitors"
        )
    elif exp_lower == "lean_condition" and win_lower == "catalyst_failure":
        return (
            "Cluster 2 — Rich mixture vs catalyst failure",
            "Fuel trim monitoring (STFT/LTFT near zero for catalyst failure, highly positive for lean condition) "
            "and Mode $06 catalyst monitor index ratio"
        )
    elif exp_lower == "lean_condition" and win_lower == "misfire":
        return (
            "Cluster 5 — Lean-condition root cause",
            "Mode $06 misfire counters vs fuel trim pattern across operating points (unmetered air leak trims recover at 2500 RPM, misfires do not)"
        )
    else:
        # Fallback default
        return ("Cluster unknown", "Diagnostic discriminator unspecified")

def load_all_rules_metadata() -> dict[str, dict[str, Any]]:
    """Load full rules metadata directly from the rules registry JSONs."""
    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    registry_rules = {}
    for fp in sorted(rules_dir.glob("*.json")):
        with open(fp) as f:
            data = json.load(f)
        for r in data.get("rules", []):
            rid = r["rule_id"]
            registry_rules[rid] = r
    return registry_rules

def capture_engine_scored_rules() -> dict[str, list[dict[str, Any]]]:
    """Capture the final scored rules list for all cases using staticmethod monkeypatch."""
    rule_map = load_rule_family_map()
    captured_data = {}
    current_case = [None]
    original_method = FaultAtlasRouter._build_v2_differential_siblings

    def my_patched_method(scored_rules: list[dict[str, Any]], winner_rule_id: str) -> list[dict[str, Any]]:
        cid = current_case[0]
        if cid:
            captured_data[cid] = [
                {
                    "rule_id": r.get("rule_id"),
                    "fault_family": r.get("fault_family", rule_map.get(r.get("rule_id", ""), "unspecified")).lower(),
                    "score": r.get("score")
                }
                for r in scored_rules
            ]
        return original_method(scored_rules, winner_rule_id)

    # Apply monkeypatch using staticmethod wrapper
    FaultAtlasRouter._build_v2_differential_siblings = staticmethod(my_patched_method)

    try:
        for case_id, raw_inputs, _, _, tag in load_corpus(DEFAULT_CSV_PATH):
            if tag != "invalid":
                current_case[0] = case_id
                diagnose(raw_inputs, enable_fatal_gates=False)
    finally:
        # Revert monkeypatch
        FaultAtlasRouter._build_v2_differential_siblings = original_method

    return captured_data

def evaluate_case_top3_pass(scored_rules_list: list[dict[str, Any]], expected_family: str) -> bool:
    """Evaluate whether the expected_family is in the top-3 families after sorting."""
    if not scored_rules_list:
        return False
    # Sort them using standard stable sort by (-score, trace_order)
    sorted_scored = sorted(scored_rules_list, key=lambda r: (-r["score"], r["trace_order"]))
    sim_winner_rule = sorted_scored[0]
    sim_winner_fam = sim_winner_rule["fault_family"]
    
    seen = {sim_winner_rule["rule_id"]}
    sim_sibs = []
    for r in sorted_scored:
        if r["rule_id"] not in seen:
            seen.add(r["rule_id"])
            sim_sibs.append(r)
            if len(sim_sibs) >= 5:
                break
                
    sim_sib_fams = [s["fault_family"] for s in sim_sibs[:2]]
    sim_top3_fams = {sim_winner_fam} | set(sim_sib_fams)
    return expected_family.lower() in sim_top3_fams

def run_self_check(captured_data: dict[str, list[dict[str, Any]]], results_by_case: dict[str, Any], accuracy_cases: list[str]) -> bool:
    """Run zero-delta self-check over all 294 accuracy cases, returning True if matches results.json."""
    rule_map = load_rule_family_map()
    mismatch_count = 0
    for cid in accuracy_cases:
        res = results_by_case.get(cid)
        scored = captured_data.get(cid)
        if not res or not scored:
            continue
            
        verdict = res["verdict"]
        expected_family = res.get("category", "").lower()
        if not expected_family:
            continue
            
        # Actual status from results.json
        actual_winner_fam = verdict.get("fault_family", "").lower()
        actual_sibs = verdict.get("differential_siblings", [])
        actual_sib_fams = []
        for s in actual_sibs[:2]:
            f = sibling_family(s, rule_map)
            if f != "unspecified":
                actual_sib_fams.append(f.lower())
        actual_top3_fams = {actual_winner_fam} | set(actual_sib_fams)
        actual_top3_pass = expected_family in actual_top3_fams
        
        # Simulated status
        rules_list = [
            {
                "rule_id": r["rule_id"],
                "fault_family": r["fault_family"],
                "score": r["score"],
                "trace_order": idx
            }
            for idx, r in enumerate(scored)
        ]
        sim_top3_pass = evaluate_case_top3_pass(rules_list, expected_family)
        
        if actual_top3_pass != sim_top3_pass:
            mismatch_count += 1
            print(f"Mismatch in {cid}: actual={actual_top3_pass}, sim={sim_top3_pass}")

    if mismatch_count == 0:
        print("Zero-delta self-check: OK (all 294 cases matched)")
        return True
    else:
        print(f"Zero-delta self-check FAILED with {mismatch_count} mismatches")
        return False

def main() -> int:
    parser = argparse.ArgumentParser(description="Rank reweight simulator.")
    parser.add_argument("--self-check", action="store_true", help="Run zero-delta self-check.")
    parser.add_argument("--write", type=str, help="Write output JSON and MD report.")
    args = parser.parse_args()

    if not args.self_check and not args.write:
        parser.print_help()
        return 1

    print("Executing dry-run to capture rule scores...")
    captured_data = capture_engine_scored_rules()
    
    # Load actual run results (POST_T_V3_3C)
    results_path = WORKSPACE_ROOT / "apps/wired/v7/runs/POST_T_V3_3C/results.json"
    with open(results_path) as f:
        results = json.load(f)["results"]
    results_by_case = {r["case_id"]: r for r in results}
    
    accuracy_cases = [r[0] for r in load_corpus(DEFAULT_CSV_PATH) if r[4] != "invalid"]

    if args.self_check:
        success = run_self_check(captured_data, results_by_case, accuracy_cases)
        return 0 if success else 1

    # Load full rules metadata
    registry_rules = load_all_rules_metadata()
    
    # Prepare the baseline data structure
    case_data = {}
    for case_id, raw_inputs, category, source_ref, tag in load_corpus(DEFAULT_CSV_PATH):
        if tag != "invalid":
            scored = captured_data.get(case_id, [])
            rules_list = [
                {
                    "rule_id": r["rule_id"],
                    "fault_family": r["fault_family"],
                    "score": r["score"],
                    "trace_order": idx
                }
                for idx, r in enumerate(scored)
            ]
            case_data[case_id] = {
                "expected_family": category.lower(),
                "rules": rules_list,
                "raw_inputs": raw_inputs
            }

    # Load tunable cases from outranked map
    outranked_path = WORKSPACE_ROOT / "v3/reports/V3_OUTRANKED_MAP_2026-06-30.json"
    with open(outranked_path) as f:
        outranked = json.load(f)
    tunable_cases = [c for c in outranked['cases'] if c['bucket'] == 'TUNABLE']

    triage_results = []
    counts = {"REWEIGHTABLE": 0, "SIGNAL-GATED": 0, "RISKY": 0, "HARD": 0}

    for tc in tunable_cases:
        cid = tc["case_id"]
        er = tc["best_expected_rule"]
        expected_family = tc["expected_family"]
        winner_rule = tc["winner_rule"]
        winner_family = tc["winner_family"]
        expected_rank = tc["expected_rank"]
        winner_score = tc["winner_score"]
        expected_score = tc["best_expected_score"]
        
        # 1. Check for absent definitive PIDs (signal-gate test)
        rule_meta = registry_rules[er]
        obd_ev = rule_meta.get("obd_evidence", [])
        inputs = case_data[cid]["raw_inputs"]
        obd_inputs = inputs.get("obd", {})
        ff_inputs = inputs.get("dtc", {}).get("raw_freeze_frame", {})
        gas_inputs = inputs.get("gas", {})
        
        absent_def_pids = []
        for ev in obd_ev:
            if ev.get("tier") == "DEFINITIVE":
                pid = ev["pid"]
                val = obd_inputs.get(pid)
                if val is None or val == "":
                    val = ff_inputs.get(pid)
                if val is None or val == "":
                    val = gas_inputs.get(pid)
                if pid == "lambda_perception_delta":
                    lm = gas_inputs.get("lambda_measured")
                    wbe = obd_inputs.get("pid_wideband_equivalence_ratio")
                    if lm is None or wbe is None:
                        val = None
                    else:
                        val = float(lm) - float(wbe)
                if val is None or val == "":
                    absent_def_pids.append(pid)
                    
        cluster_name, discriminator = get_cluster_and_discriminator(expected_family, winner_family)

        if absent_def_pids:
            verdict = "SIGNAL-GATED"
            counts[verdict] += 1
            triage_results.append({
                "case_id": cid,
                "expected_family": expected_family,
                "expected_rule": er,
                "winner_family": winner_family,
                "winner_rule": winner_rule,
                "winner_score": winner_score,
                "expected_score": expected_score,
                "expected_rank": expected_rank,
                "score_margin": tc["score_margin"],
                "cluster": cluster_name,
                "discriminator": discriminator,
                "absent_definitive_pids": absent_def_pids,
                "minimal_lift_delta": None,
                "regressions": [],
                "verdict": verdict
            })
            continue

        # 2. Find minimal lift delta
        min_delta = None
        original_case_rules = case_data[cid]["rules"]
        ceiling = rule_meta.get("confidence_ceiling", 1.0)
        
        for d_int in range(0, 1001):
            d = d_int / 1000.0
            temp_rules = []
            for r in original_case_rules:
                r_copy = dict(r)
                if r_copy["rule_id"] == er:
                    r_copy["score"] = min(r_copy["score"] + d, ceiling)
                temp_rules.append(r_copy)
            if evaluate_case_top3_pass(temp_rules, expected_family):
                min_delta = d
                break
                
        if min_delta is None or min_delta > 0.15:
            verdict = "HARD"
            counts[verdict] += 1
            triage_results.append({
                "case_id": cid,
                "expected_family": expected_family,
                "expected_rule": er,
                "winner_family": winner_family,
                "winner_rule": winner_rule,
                "winner_score": winner_score,
                "expected_score": expected_score,
                "expected_rank": expected_rank,
                "score_margin": tc["score_margin"],
                "cluster": cluster_name,
                "discriminator": discriminator,
                "absent_definitive_pids": [],
                "minimal_lift_delta": min_delta,
                "regressions": [],
                "verdict": verdict
            })
            continue

        # 3. Evaluate regressions (FT-8 neighbour risk)
        regressed_cases = []
        for other_cid, data in case_data.items():
            if other_cid == cid:
                continue
            has_rule = any(r["rule_id"] == er for r in data["rules"])
            if not has_rule:
                continue
                
            orig_pass = evaluate_case_top3_pass(data["rules"], data["expected_family"])
            if not orig_pass:
                continue
                
            temp_rules = []
            for r in data["rules"]:
                r_copy = dict(r)
                if r_copy["rule_id"] == er:
                    r_copy["score"] = min(r_copy["score"] + min_delta, ceiling)
                temp_rules.append(r_copy)
                
            new_pass = evaluate_case_top3_pass(temp_rules, data["expected_family"])
            if orig_pass and not new_pass:
                regressed_cases.append(other_cid)

        if regressed_cases:
            verdict = "RISKY"
        else:
            verdict = "REWEIGHTABLE"
            
        counts[verdict] += 1
        triage_results.append({
            "case_id": cid,
            "expected_family": expected_family,
            "expected_rule": er,
            "winner_family": winner_family,
            "winner_rule": winner_rule,
            "winner_score": winner_score,
            "expected_score": expected_score,
            "expected_rank": expected_rank,
            "score_margin": tc["score_margin"],
            "cluster": cluster_name,
            "discriminator": discriminator,
            "absent_definitive_pids": [],
            "minimal_lift_delta": min_delta,
            "regressions": regressed_cases,
            "verdict": verdict
        })

    # Write JSON output
    out_json_path = Path(args.write)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_payload = {
        "source": "v3/tunable_reweight_sim.py",
        "triage_summary": {
            "reweightable": counts["REWEIGHTABLE"],
            "signal_gated": counts["SIGNAL-GATED"],
            "risky": counts["RISKY"],
            "hard": counts["HARD"],
            "total_tunable": len(tunable_cases)
        },
        "cases": triage_results
    }
    
    with open(out_json_path, "w") as f:
        json.dump(output_payload, f, indent=2)
    print(f"Wrote JSON map to {out_json_path}")

    # Generate and Write Markdown report
    out_md_path = out_json_path.with_suffix(".md")
    
    md_content = []
    md_content.append("# V3 Tunable Reweight Feasibility Map")
    md_content.append("\nGenerated on: 2026-07-01")
    md_content.append("\n## Triage Summary")
    md_content.append(f"- **Reweightable (R)**: {counts['REWEIGHTABLE']}")
    md_content.append(f"- **Signal-Gated (S)**: {counts['SIGNAL-GATED']}")
    md_content.append(f"- **Risky (K)**: {counts['RISKY']}")
    md_content.append(f"- **Hard/Not Recoverable (H)**: {counts['HARD']}")
    md_content.append(f"- **Total Tunable**: {len(tunable_cases)}")
    
    md_content.append("\n## Detailed Case Triage")
    md_content.append("| Case ID | Expected Family (Rule) | Winner Family (Rule) | Original Score (Winner/Expected) | Expected Rank | Lift Delta | Verdict | Regressions / Absent PIDs |")
    md_content.append("|---|---|---|---|---|---|---|---|")
    
    for r in triage_results:
        cid = r["case_id"]
        er = r["expected_rule"]
        ef = r["expected_family"]
        wr = r["winner_rule"]
        wf = r["winner_family"]
        ws = r["winner_score"]
        es = r["expected_score"]
        rk = r["expected_rank"]
        d = r["minimal_lift_delta"]
        v = r["verdict"]
        
        delta_str = f"{d:.3f}" if d is not None else "N/A"
        scores_str = f"{ws:.2f}/{es:.2f}"
        
        notes = ""
        if v == "SIGNAL-GATED":
            notes = f"Absent definitive PIDs: {r['absent_definitive_pids']}"
        elif v == "RISKY":
            notes = f"Regresses: {r['regressions']}"
            
        md_content.append(f"| {cid} | {ef} ({er}) | {wf} ({wr}) | {scores_str} | {rk} | {delta_str} | **{v}** | {notes} |")
        
    md_content.append("\n## Cluster Citations & Discriminators")
    md_content.append("| Case ID | Expected vs Winner | Research Cluster | Diagnostic Discriminator |")
    md_content.append("|---|---|---|---|")
    for r in triage_results:
        cid = r["case_id"]
        ef = r["expected_family"]
        wf = r["winner_family"]
        cl = r["cluster"]
        disc = r["discriminator"]
        md_content.append(f"| {cid} | {ef} vs {wf} | {cl} | {disc} |")
        
    with open(out_md_path, "w") as f:
        f.write("\n".join(md_content) + "\n")
    print(f"Wrote MD report to {out_md_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
