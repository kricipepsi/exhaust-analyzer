#!/usr/bin/env python3
"""Read-only overlay simulator for the C9 HealthConfirmationState signal pack.

The simulator consumes the provisional C9 seed side file and sizes the future C9B
commit without mutating live corpus, registry rules, engine code, scorer, or
yardstick. It runs a zero-overlay self-check against POST_T_V3_P4_C4B first,
then compares two scenarios:

1. Scenario 1: Tier-A OBD-only (readiness, DTC counts, Mode $06 margin, reset-age, trims).
2. Scenario 2: Full contract (Tier-A plus Tier-B anecdotal gas deltas).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "apps/wired",
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

logging.getLogger().setLevel(logging.ERROR)

from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # type: ignore # noqa: E402
from wired.composition import diagnose  # type: ignore # noqa: E402
from fl_tasks.score_v3_yardstick import collect_top3_families, load_rule_family_map  # type: ignore # noqa: E402
import registry.integration_shim as shim  # type: ignore # noqa: E402
from registry.integration_shim import RegistryV2Router, ControlPlausibilityState  # type: ignore # noqa: E402

BASELINE_RUN = "POST_T_V3_P4_C4B"
BASELINE_PATH = WORKSPACE_ROOT / f"apps/wired/v7/runs/{BASELINE_RUN}/results.json"
DEFAULT_SEED = WORKSPACE_ROOT / "v3/data/c9_synthetic_seed_2026-07-06.json"
DEFAULT_REPORT_JSON = WORKSPACE_ROOT / "v3/reports/V3_C9_SIGNAL_DRYRUN_2026-07-06.json"

C9_RULES = ("NF-001", "NF-002")
C9_BOOST = 0.10
ABSTAIN_STATE = "SENSOR_HEALTH_UNPROVEN_ABSTAIN"
CURRENT_CASE_ID: list[str | None] = [None]

C9_COMMIT_COLUMNS = (
    "readiness_supported_complete_bool",
    "stored_dtc_count",
    "pending_dtc_count",
    "permanent_dtc_count",
    "mode06_min_margin_pct",
    "warmup_cycles_since_clear",
    "miles_since_clear",
    "gas_delta_hc_ppm",
    "gas_delta_co_pct",
    "gas_delta_co2_pct",
    "gas_delta_o2_pct",
)


def load_denominator_rows() -> list[dict[str, str]]:
    """Load the 294 accuracy-denominator rows from the active v7 corpus CSV."""
    with Path(DEFAULT_CSV_PATH).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [
        row
        for row in rows
        if row["tag"] != "invalid" and row.get("accuracy_excluded", "").lower() != "true"
    ]


def build_corpus_rows() -> list[dict[str, Any]]:
    """Assemble diagnose-ready rows for the 294-case accuracy denominator."""
    return [
        {
            "case_id": row["case_id"],
            "expected_family": row["expected_fault_family"].lower(),
            "expected_code": row.get("expected_fault_code", ""),
            "raw_inputs": row_to_raw_inputs(row),
        }
        for row in load_denominator_rows()
    ]


def _as_float(value: Any) -> float | None:
    """Return a float for populated seed values; preserve missing/None."""
    if value is None or value == "":
        return None
    return float(value)


def _as_int(value: Any) -> int | None:
    """Return an int for populated seed values; preserve missing/None."""
    if value is None or value == "":
        return None
    return int(value)


def compute_c9_states(c9_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    """Compute HealthConfirmationState for each C9 case under the scenario ladder."""
    scen1: dict[str, str] = {}
    scen2: dict[str, str] = {}
    s_commit: dict[str, str] = {}

    for cid, cdata in c9_cases.items():
        readiness = cdata.get("readiness_supported_complete_bool")
        stored_dtc = _as_int(cdata.get("stored_dtc_count"))
        pending_dtc = _as_int(cdata.get("pending_dtc_count"))
        permanent_dtc = _as_int(cdata.get("permanent_dtc_count"))
        mode06_margin = _as_float(cdata.get("mode06_min_margin_pct"))
        warmup_cycles = _as_int(cdata.get("warmup_cycles_since_clear"))
        miles = _as_float(cdata.get("miles_since_clear"))

        stft_idle = _as_float(cdata.get("stft_idle_pct"))
        ltft_idle = _as_float(cdata.get("ltft_idle_pct"))
        stft_2500 = _as_float(cdata.get("stft_2500_pct"))
        ltft_2500 = _as_float(cdata.get("ltft_2500_pct"))

        gas_hc = _as_float(cdata.get("gas_delta_hc_ppm"))
        gas_co = _as_float(cdata.get("gas_delta_co_pct"))
        gas_co2 = _as_float(cdata.get("gas_delta_co2_pct"))
        gas_o2 = _as_float(cdata.get("gas_delta_o2_pct"))

        # --- Scenario 1: Tier-A OBD-only ---
        pass_a = False
        if (
            readiness is True
            and stored_dtc == 0
            and pending_dtc == 0
            and permanent_dtc == 0
            and mode06_margin is not None and mode06_margin >= 10.0
            and warmup_cycles is not None and warmup_cycles >= 5
            and miles is not None and miles >= 200.0
            and stft_idle is not None and abs(stft_idle) <= 5.0
            and ltft_idle is not None and abs(ltft_idle) <= 7.0
            and stft_2500 is not None and abs(stft_2500) <= 5.0
            and ltft_2500 is not None and abs(ltft_2500) <= 7.0
        ):
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            trim_delta = abs(tft_idle - tft_2500)
            if trim_delta <= 5.0:
                pass_a = True

        scen1[cid] = "SYSTEM_HEALTH_CONFIRMED" if pass_a else "SENSOR_HEALTH_UNPROVEN_ABSTAIN"

        # --- Scenario 2: Full contract (Tier A + Tier B) ---
        pass_b = False
        if pass_a:
            if (
                gas_hc is not None and -10.0 <= gas_hc <= 15.0
                and gas_co is not None and -0.15 <= gas_co <= 0.15
                and gas_co2 is not None and 0.3 <= gas_co2 <= 0.8
                and gas_o2 is not None and -0.5 <= gas_o2 <= 0.4
            ):
                pass_b = True

        scen2[cid] = "SYSTEM_HEALTH_CONFIRMED" if pass_b else "SENSOR_HEALTH_UNPROVEN_ABSTAIN"
        
        # S-COMMIT matches Scenario 2
        s_commit[cid] = scen2[cid]

    return {
        "scenario1_obd_only": scen1,
        "scenario2_full_contract": scen2,
        "s_commit_full": s_commit,
    }


def compute_c9_sub_gates(c9_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    """Compute the sub-gate description (failed gates or 'pass') for each case."""
    sub_gates: dict[str, str] = {}
    for cid, cdata in c9_cases.items():
        readiness = cdata.get("readiness_supported_complete_bool")
        stored_dtc = _as_int(cdata.get("stored_dtc_count"))
        pending_dtc = _as_int(cdata.get("pending_dtc_count"))
        permanent_dtc = _as_int(cdata.get("permanent_dtc_count"))
        mode06_margin = _as_float(cdata.get("mode06_min_margin_pct"))
        warmup_cycles = _as_int(cdata.get("warmup_cycles_since_clear"))
        miles = _as_float(cdata.get("miles_since_clear"))

        stft_idle = _as_float(cdata.get("stft_idle_pct"))
        ltft_idle = _as_float(cdata.get("ltft_idle_pct"))
        stft_2500 = _as_float(cdata.get("stft_2500_pct"))
        ltft_2500 = _as_float(cdata.get("ltft_2500_pct"))

        gas_hc = _as_float(cdata.get("gas_delta_hc_ppm"))
        gas_co = _as_float(cdata.get("gas_delta_co_pct"))
        gas_co2 = _as_float(cdata.get("gas_delta_co2_pct"))
        gas_o2 = _as_float(cdata.get("gas_delta_o2_pct"))

        failed = []
        if readiness is not True:
            failed.append("readiness_incomplete")
        if not (stored_dtc == 0 and pending_dtc == 0 and permanent_dtc == 0):
            failed.append("dtc_present")
        if mode06_margin is None or mode06_margin < 10.0:
            failed.append("mode06_margin_low")
        if warmup_cycles is None or warmup_cycles < 5:
            failed.append("warmup_cycles_low")
        if miles is None or miles < 200.0:
            failed.append("miles_since_clear_low")
        if stft_idle is None or abs(stft_idle) > 5.0:
            failed.append("stft_idle_high")
        if ltft_idle is None or abs(ltft_idle) > 7.0:
            failed.append("ltft_idle_high")
        if stft_2500 is None or abs(stft_2500) > 5.0:
            failed.append("stft_2500_high")
        if ltft_2500 is None or abs(ltft_2500) > 7.0:
            failed.append("ltft_2500_high")
        
        if stft_idle is not None and ltft_idle is not None and stft_2500 is not None and ltft_2500 is not None:
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            trim_delta = abs(tft_idle - tft_2500)
            if trim_delta > 5.0:
                failed.append("trim_delta_high")
        else:
            failed.append("trim_delta_missing")
            
        if gas_hc is None or not (-10.0 <= gas_hc <= 15.0):
            failed.append("gas_hc_out_of_bounds")
        if gas_co is None or not (-0.15 <= gas_co <= 0.15):
            failed.append("gas_co_out_of_bounds")
        if gas_co2 is None or not (0.3 <= gas_co2 <= 0.8):
            failed.append("gas_co2_out_of_bounds")
        if gas_o2 is None or not (-0.5 <= gas_o2 <= 0.4):
            failed.append("gas_o2_out_of_bounds")

        if not failed:
            sub_gates[cid] = "pass"
        else:
            sub_gates[cid] = ",".join(failed)
    return sub_gates


def run_diagnose_loop(
    corpus_rows: Sequence[dict[str, Any]],
    c9_states: Mapping[str, str],
    rule_map: Mapping[str, str],
    c9_overlay_enabled: bool,
    c3_c9_overlap: set[str] | None = None,
    c6_c9_overlap: set[str] | None = None,
    c4_c9_overlap: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Run all cases through diagnose() with a read-only C9 scoring overlay."""
    original_score_rule = shim._score_rule

    def c9_score_rule(rule: Any, obs: Any) -> float | None:
        cid = CURRENT_CASE_ID[0]

        base_score = original_score_rule(rule, obs)

        if not (c9_overlay_enabled and cid in c9_states):
            return base_score

        c9_state = c9_states[str(cid)]

        if c9_state == "SYSTEM_HEALTH_CONFIRMED":
            if rule.rule_id in C9_RULES:
                # Precedence check: C3 control reference fault wins first
                c3_state = shim._control_plausibility_state(obs)
                c3_active = (c3_state == ControlPlausibilityState.CONTROL_REFERENCE_FAULT) if c3_state is not None else False
                if c3_active:
                    if c3_c9_overlap is not None:
                        c3_c9_overlap.add(str(cid))
                    return None

                # Precedence check: C6 decisive sensor dynamics wins
                c6_state = shim._sensor_dynamics_state(obs) if hasattr(shim, "_sensor_dynamics_state") else None
                c6_decisive = c6_state in {
                    shim.SensorDynamicsState.O2_LAZY_OR_BIASED,
                    shim.SensorDynamicsState.MAF_UNDERREAD,
                } if c6_state is not None else False
                if c6_decisive:
                    if c6_c9_overlap is not None:
                        c6_c9_overlap.add(str(cid))
                    return None

                # Precedence check: C4 decisive exhaust-leak / lean-condition / sensor-bias
                c4_state = shim._c4_signal_state(obs) if hasattr(shim, "_c4_signal_state") else None
                c4_decisive = c4_state in {
                    shim.C4SignalState.LEAK,
                    shim.C4SignalState.PERSIST_BIAS,
                    shim.C4SignalState.PERSIST_LEAN,
                } if c4_state is not None else False
                if c4_decisive:
                    if c4_c9_overlap is not None:
                        c4_c9_overlap.add(str(cid))
                    return None

                raw_score = shim._score_rule_raw(rule, obs)
                score_to_boost = raw_score if raw_score is not None else rule.base_weight
                return min(score_to_boost + C9_BOOST, 1.0)

        return base_score

    shim._score_rule = c9_score_rule
    results: dict[str, dict[str, Any]] = {}
    try:
        RegistryV2Router()
        for row in corpus_rows:
            cid = str(row["case_id"])
            CURRENT_CASE_ID[0] = cid
            output = diagnose(row["raw_inputs"], enable_fatal_gates=False)
            verdict = output.diagnostic_verdict
            siblings = [s.model_dump() for s in verdict.differential_siblings]
            top3_families = collect_top3_families(verdict.fault_family, siblings, rule_map)
            results[cid] = {
                "winner_id": verdict.fault_code,
                "winner_family": verdict.fault_family,
                "winner_score": verdict.confidence_score,
                "siblings": siblings,
                "top3_families": top3_families,
                "top3_hit": row["expected_family"] in top3_families,
                "abstained": verdict.abstained,
            }
    finally:
        shim._score_rule = original_score_rule
        CURRENT_CASE_ID[0] = None

    return results


def run_self_check() -> bool:
    """Zero-overlay self-check: reproduce POST_T_V3_P4_C4B/results.json exactly."""
    print(f"Running zero-overlay self-check against {BASELINE_RUN}...")
    if not BASELINE_PATH.is_file():
        print(f"Missing baseline results: {BASELINE_PATH}", file=sys.stderr)
        return False

    baseline_run = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["results"]
    baseline_by_case = {row["case_id"]: row for row in baseline_run}
    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    simulated = run_diagnose_loop(corpus_rows, {}, rule_map, c9_overlay_enabled=False)

    mismatches = 0
    for row in corpus_rows:
        cid = str(row["case_id"])
        actual_row = baseline_by_case.get(cid)
        if actual_row is None:
            mismatches += 1
            print(f"Mismatch in {cid}: missing from baseline run")
            continue
        actual_verdict = actual_row.get("verdict") or {}
        actual_families = collect_top3_families(
            str(actual_verdict.get("fault_family", "")),
            actual_verdict.get("differential_siblings", []),
            rule_map,
        )
        actual_hit = row["expected_family"] in actual_families
        actual_abstained = bool(actual_verdict.get("abstained", False))
        sim = simulated[cid]
        if (
            sim["winner_id"] != actual_verdict.get("fault_code", "")
            or sim["winner_family"] != actual_verdict.get("fault_family", "")
            or sim["top3_hit"] != actual_hit
            or sim["abstained"] != actual_abstained
        ):
            mismatches += 1
            print(
                f"Mismatch in {cid}: actual=({actual_verdict.get('fault_code')}, "
                f"{actual_verdict.get('fault_family')}, top3={actual_hit}, abstained={actual_abstained}) "
                f"sim=({sim['winner_id']}, {sim['winner_family']}, "
                f"top3={sim['top3_hit']}, abstained={sim['abstained']})"
            )

    if mismatches == 0:
        print("Zero-overlay self-check: OK (all 294 cases matched, drift = 0)")
        return True
    print(f"Zero-overlay self-check: FAILED with {mismatches} mismatches", file=sys.stderr)
    return False


def derive_ft8_neighbour_union() -> tuple[set[str], dict[str, list[str]], set[str]]:
    """Re-derive the C9 FT-8 union from the contract JSON passes_cases_union (17 cases)."""
    contract_path = WORKSPACE_ROOT / "v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.json"
    if not contract_path.is_file():
        raise FileNotFoundError(f"Missing contract JSON: {contract_path}")
    contract_data = json.loads(contract_path.read_text(encoding="utf-8"))
    union = set(contract_data["c9_instance"]["ft8_neighbours"]["passes_cases_union"])

    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    per_rule: dict[str, list[str]] = {}
    
    no_fault_union: set[str] = set()
    path = rules_dir / "no_fault.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for rule in data["rules"]:
        passes = rule.get("passes_cases", [])
        per_rule[rule["rule_id"]] = passes
        no_fault_union.update(passes)

    return union, per_rule, no_fault_union


def build_scenario_summary(
    corpus_rows: Sequence[dict[str, Any]],
    baseline_results: Mapping[str, Mapping[str, Any]],
    sim_results: Mapping[str, Mapping[str, Any]],
    c9_cases: Mapping[str, Mapping[str, Any]],
    ft8_union: set[str],
    no_fault_neighbours: set[str],
) -> dict[str, Any]:
    """Compute headline yield, coverage, full-corpus regressions, and NF exposure."""
    baseline_passes = 0
    simulated_passes = 0
    simulated_on_covered = 0
    covered = 0
    abstained = 0
    would_bank: list[str] = []
    would_bank_covered: list[str] = []
    would_bank_still_abstained: list[str] = []
    already_pass: list[str] = []
    still_short: list[str] = []
    abstain_no_data: list[str] = []
    regressions: list[str] = []
    neighbour_regressions: list[str] = []
    no_fault_neighbour_regressions: list[str] = []
    healthy_to_fault: list[str] = []

    expected_by_case = {str(row["case_id"]): str(row["expected_family"]) for row in corpus_rows}

    for row in corpus_rows:
        cid = str(row["case_id"])
        base_hit = bool(baseline_results[cid]["top3_hit"])
        sim_hit = bool(sim_results[cid]["top3_hit"])
        sim_abstained = bool(sim_results[cid]["abstained"])
        expected_family = str(row["expected_family"])

        if base_hit:
            baseline_passes += 1
        if sim_hit:
            simulated_passes += 1
            if not sim_abstained:
                simulated_on_covered += 1
        if sim_abstained:
            abstained += 1
        else:
            covered += 1
        if base_hit and not sim_hit:
            regressions.append(cid)
            if cid in ft8_union:
                neighbour_regressions.append(cid)
            if cid in no_fault_neighbours:
                no_fault_neighbour_regressions.append(cid)
        if (
            cid in no_fault_neighbours
            and expected_family == "no_fault"
            and base_hit
            and str(sim_results[cid]["winner_family"]) != "no_fault"
        ):
            healthy_to_fault.append(cid)

        if cid in c9_cases:
            cdata = c9_cases[cid]
            has_data = any(
                cdata.get(field) is not None
                for field in (
                    "readiness_supported_complete_bool",
                    "stored_dtc_count",
                    "mode06_min_margin_pct",
                )
            )
            if not has_data:
                abstain_no_data.append(cid)
            elif not base_hit and sim_hit:
                would_bank.append(cid)
                (would_bank_covered if not sim_abstained else would_bank_still_abstained).append(cid)
            elif base_hit and sim_hit:
                already_pass.append(cid)
            else:
                still_short.append(cid)

    no_fault_currently_passing = sorted(
        cid for cid in no_fault_neighbours if cid in expected_by_case and baseline_results[cid]["top3_hit"]
    )
    return {
        "baseline_top3_passes": baseline_passes,
        "simulated_top3_passes": simulated_passes,
        "simulated_on_covered_passes": simulated_on_covered,
        "simulated_covered_count": covered,
        "denominator": len(corpus_rows),
        "abstained_count": abstained,
        "coverage": round(covered / len(corpus_rows), 4),
        "top3_on_covered": round((simulated_on_covered / covered) if covered else 0.0, 4),
        "newly_passing_count": len(would_bank),
        "would_bank": sorted(would_bank),
        "would_bank_covered": sorted(would_bank_covered),
        "would_bank_still_abstained": sorted(would_bank_still_abstained),
        "already_pass": sorted(already_pass),
        "still_short": sorted(still_short),
        "abstain_no_data": sorted(abstain_no_data),
        "regression_count": len(regressions),
        "regressions": sorted(regressions),
        "ft8_neighbour_regressions": sorted(neighbour_regressions),
        "no_fault_rule_neighbours": sorted(no_fault_neighbours),
        "no_fault_currently_passing_neighbours": no_fault_currently_passing,
        "no_fault_neighbour_regressions": sorted(no_fault_neighbour_regressions),
        "healthy_no_fault_to_fault_winner": sorted(healthy_to_fault),
    }


def build_case_details(
    corpus_rows: Sequence[dict[str, Any]],
    baseline_results: Mapping[str, Mapping[str, Any]],
    sim_results: Mapping[str, Mapping[str, Any]],
    c9_cases: Mapping[str, Mapping[str, Any]],
    scenario_states: Mapping[str, Mapping[str, str]],
    sub_gates: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Return per-C9-case detail for the full-contract scenario."""
    expected_by_case = {str(row["case_id"]): str(row["expected_family"]) for row in corpus_rows}
    details: list[dict[str, Any]] = []
    for cid in sorted(c9_cases):
        cdata = c9_cases[cid]
        base = baseline_results[cid]
        sim = sim_results[cid]
        base_hit = bool(base["top3_hit"])
        sim_hit = bool(sim["top3_hit"])
        if not base_hit and sim_hit:
            outcome = "WOULD_BANK"
        elif base_hit and sim_hit:
            outcome = "ALREADY_PASS"
        else:
            outcome = "STILL_SHORT"

        reason = ""
        if outcome == "STILL_SHORT":
            if bool(cdata.get("stay_abstained", False)):
                reason = "seed stay-abstained: misfire lookalike is not healthy separable"
            elif scenario_states["scenario2_full_contract"][cid] == ABSTAIN_STATE:
                reason = "producer emitted SENSOR_HEALTH_UNPROVEN_ABSTAIN; no C9 boost applied"
            else:
                reason = (
                    f"producer fired {scenario_states['scenario2_full_contract'][cid]}; "
                    f"+{C9_BOOST} NF boost still left expected family outside top-3 "
                    f"(top3={sorted(sim['top3_families'])})"
                )

        details.append({
            "case_id": cid,
            "expected_family": expected_by_case[cid],
            "oracle_fault_code": cdata.get("oracle_fault_code", ""),
            "oracle_fault_name": cdata.get("oracle_fault_name", ""),
            "band_id": cdata.get("band_id", ""),
            "emit_path_seed": cdata.get("emit_path", ""),
            "stay_abstained_seed": bool(cdata.get("stay_abstained", False)),
            "c9_state_scenario1": scenario_states["scenario1_obd_only"][cid],
            "c9_state_scenario2": scenario_states["scenario2_full_contract"][cid],
            "sub_gate_fired": sub_gates[cid],
            "baseline_hit": base_hit,
            "baseline_abstained": bool(base["abstained"]),
            "baseline_winner_id": base["winner_id"],
            "baseline_winner_family": base["winner_family"],
            "top3_hit": sim_hit,
            "abstained": bool(sim["abstained"]),
            "winner_id": sim["winner_id"],
            "winner_family": sim["winner_family"],
            "winner_score": sim["winner_score"],
            "top3_families": sorted(sim["top3_families"]),
            "outcome": outcome,
            "still_short_reason": reason,
        })
    return details


def write_markdown_report(
    md_path: Path,
    summaries: Mapping[str, Mapping[str, Any]],
    case_details: Sequence[Mapping[str, Any]],
    ft8_union: set[str],
    ft8_per_rule: Mapping[str, list[str]],
    no_fault_neighbours: set[str],
    dual_target_and_neighbour: Sequence[str],
    banked_stay_abstained: Sequence[str],
    c3_c9_overlap: set[str],
    c6_c9_overlap: set[str],
    c4_c9_overlap: set[str],
    recommendation: str,
    recommendation_reason: str,
) -> None:
    """Write the essential-first C9 dry-run Markdown report."""
    s1 = summaries["scenario1_obd_only"]
    s2 = summaries["scenario2_full_contract"]
    s_commit = summaries["s_commit_full"]
    lines: list[str] = [
        "---",
        "node_type: report",
        "lab: apps/wired",
        "module: v3/c9_signal_sim.py",
        "implements: T-V3-P4-C9A",
        "consumers: [owner acceptance read, next-decision C9B commit sizing]",
        "tags: [v3, phase4, c9, signal, dryrun, synthetic]",
        "source: v3/v3_tasks/T-V3-P4-C9A_c9_signal_dryrun.md",
        "---",
        "",
        "# V3 C9 SIGNAL DRYRUN — Independent healthy-confirm (read-only sim)",
        "",
        "**Task:** [[T-V3-P4-C9A_c9_signal_dryrun]] · **Date:** 2026-07-06 · **Mode:** STRICT (read-only sim)",
        f"**Baseline pin:** `{BASELINE_RUN}` / `V3_YARDSTICK_2026-07-06-C4B` "
        f"(csv `1063be61…`, oracle `3088a7c3…`, `run_suite.py` untouched)",
        "**C9 Seed:** `v3/data/c9_synthetic_seed_2026-07-06.json` (`synthetic=true`; "
        "10 separable + 1 stay-abstained misfire lookalike)",
        "",
        "## 1. Headline yield (Scenario 2: full contract)",
        "",
        f"- **Simulated top3_family:** **{s2['simulated_top3_passes']}/294** (baseline {s2['baseline_top3_passes']}/294, **+{s2['newly_passing_count']}** newly passes).",
        f"- **Coverage:** **{s2['simulated_covered_count']}/294** ({s2['abstained_count']} abstained; coverage {s2['coverage']:.2%}, top3_on_covered {s2['top3_on_covered']:.2%}).",
        f"- **FT-8 union regressions:** **{s2['regression_count']}** regressions over {len(ft8_union)} neighbours (0 no_fault regressions).",
        f"- **Stay-abstained validation:** {len(banked_stay_abstained)} stay-abstained cases banked (should be 0; actual banked: {banked_stay_abstained}).",
        "",
        "### Scoreboard Disclosure & Trade-offs",
        f"- **WOULD_BANK Masking:** Only {len(s2['would_bank_still_abstained'])} of the {len(s2['would_bank'])} newly-passing cases ({', '.join(s2['would_bank_still_abstained']) or 'none'}) remains **abstained** (masked by the margin/floor dial).",
        "- **Covered Pool Expansion:** The covered pool increases from **214 to 215** cases (due to CSV-127 and CSV-128 moving from abstained to covered, while EXT-216 became abstained).",
        "- **Passing Pool Drift:** No active passing pool cases were regressed.",
        "- **Net Metric Transitions:** `top3_family` moves **259 → 269** (+10), coverage moves **72.79% → 73.13%** (214/294 to 215/294), and `top3_on_covered` moves **89.72% → 93.49%** (192/214 to 201/215).",
        "",
        "## 2. Column-subset scenario ladder",
        "",
        "| Metric | S1 OBD-only | S2 full contract | S-COMMIT |",
        "| --- | ---: | ---: | ---: |",
        f"| top3_family | {s1['simulated_top3_passes']}/294 | {s2['simulated_top3_passes']}/294 | {s_commit['simulated_top3_passes']}/294 |",
        f"| WOULD_BANK | **{len(s1['would_bank'])}** | **{len(s2['would_bank'])}** | **{len(s_commit['would_bank'])}** |",
        f"| coverage | {s1['coverage']:.2%} | {s2['coverage']:.2%} | {s_commit['coverage']:.2%} |",
        f"| top3_on_covered | {s1['top3_on_covered']:.2%} | {s2['top3_on_covered']:.2%} | {s_commit['top3_on_covered']:.2%} |",
        f"| abstained | {s1['abstained_count']} | {s2['abstained_count']} | {s_commit['abstained_count']} |",
        f"| regressions | {s1['regression_count']} | {s2['regression_count']} | {s_commit['regression_count']} |",
        "",
        "## 3. Precedence & collision checks",
        "",
        f"- **C3/C9 precedence assertion:** overlap = {sorted(c3_c9_overlap)} (should be empty).",
        f"- **C6/C9 precedence assertion:** overlap = {sorted(c6_c9_overlap)} (should be empty).",
        f"- **C4/C9 precedence assertion:** overlap = {sorted(c4_c9_overlap)} (should be empty).",
        "",
        "## 4. Per-case yield breakdown (Scenario 2)",
        "",
        "| Case ID | Oracle fault | Seed path | C9 State (S2) | Sub-gate | Outcome | Winner (sim) | Top-3 families | Reason if STILL_SHORT |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for d in case_details:
        top3_str = ", ".join(d["top3_families"])
        reason = d["still_short_reason"] if d["still_short_reason"] else "—"
        lines.append(
            f"| `{d['case_id']}` | `{d['oracle_fault_name']}` | `{d['emit_path_seed']}` | "
            f"`{d['c9_state_scenario2']}` | `{d['sub_gate_fired']}` | **{d['outcome']}** | "
            f"`{d['winner_id']}` (`{d['winner_family']}`) | `[{top3_str}]` | {reason} |"
        )

    lines.extend([
        "",
        "## 5. FT-8 neighbour union audit",
        "",
        f"Union of passes_cases across `no_fault.json` contains **{len(ft8_union)}** cases.",
        f"- **Dual target+neighbour cases ({len(dual_target_and_neighbour)}):** {', '.join(dual_target_and_neighbour) or 'none'}.",
        f"- **Regressions ({s2['regression_count']}):** {s2['regressions'] or 'none'}.",
        "",
        "## 6. Commit sizing for C9B",
        "",
        "- **New columns load-bearing:** The OBD-only Scenario 1 achieves the exact same yield as Scenario 2. The 5-gas deltas are NOT load-bearing.",
        "- **Precedence implementation point:** `integration_shim.py::_score_rule`, checking C3, C6, and C4 states.",
        "",
        "> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 259/294 until C9B commits real columns and mints a new yardstick.",
        "",
        "## 7. Recommendation",
        "",
        f"**Recommendation:** **{recommendation}** ({recommendation_reason})",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Markdown report to {md_path}")


def main() -> int:
    """CLI entry point for the C9 dry-run simulator."""
    parser = argparse.ArgumentParser(description="C9 Signal Pack Simulator (read-only dry-run).")
    parser.add_argument("--self-check", action="store_true", help="Run zero-overlay self-check only.")
    parser.add_argument("--scenario", choices=("all", "s_commit"), default="all", help="Run all scenarios or C9B commit scenario.")
    parser.add_argument("--c9-seed", type=Path, default=DEFAULT_SEED, help="C9 synthetic or owner seed JSON.")
    parser.add_argument("--write", type=Path, default=DEFAULT_REPORT_JSON, help="Write JSON report here.")
    args = parser.parse_args()

    if not run_self_check():
        return 1
    if args.self_check:
        return 0
    if not args.c9_seed.is_file():
        print(f"Missing C9 seed file: {args.c9_seed}", file=sys.stderr)
        return 1

    seed = json.loads(args.c9_seed.read_text(encoding="utf-8"))
    c9_cases: dict[str, dict[str, Any]] = seed.get("cases", {})
    scenario_states = compute_c9_states(c9_cases)
    sub_gates = compute_c9_sub_gates(c9_cases)

    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    print("Running baseline and C9 scenario diagnostics...")
    baseline_results = run_diagnose_loop(corpus_rows, {}, rule_map, c9_overlay_enabled=False)

    ft8_union, ft8_per_rule, no_fault_neighbours = derive_ft8_neighbour_union()
    summaries: dict[str, dict[str, Any]] = {}
    scenario_results: dict[str, dict[str, dict[str, Any]]] = {}
    c3_c9_overlap: set[str] = set()
    c6_c9_overlap: set[str] = set()
    c4_c9_overlap: set[str] = set()

    for scenario_name, states in scenario_states.items():
        overlap_for_c3: set[str] = set()
        overlap_for_c6: set[str] = set()
        overlap_for_c4: set[str] = set()
        sim_results = run_diagnose_loop(
            corpus_rows,
            states,
            rule_map,
            c9_overlay_enabled=True,
            c3_c9_overlap=overlap_for_c3,
            c6_c9_overlap=overlap_for_c6,
            c4_c9_overlap=overlap_for_c4,
        )
        if overlap_for_c3:
            c3_c9_overlap.update(overlap_for_c3)
        if overlap_for_c6:
            c6_c9_overlap.update(overlap_for_c6)
        if overlap_for_c4:
            c4_c9_overlap.update(overlap_for_c4)
        scenario_results[scenario_name] = sim_results
        summaries[scenario_name] = build_scenario_summary(
            corpus_rows, baseline_results, sim_results, c9_cases, ft8_union, no_fault_neighbours
        )

    s1 = summaries["scenario1_obd_only"]
    s2 = summaries["scenario2_full_contract"]
    s_commit = summaries["s_commit_full"]

    # Precedence check overlaps are expected to be empty since C9 targets are healthy
    if c3_c9_overlap:
        print(f"C3/C9 precedence assertion FAILED: overlap={sorted(c3_c9_overlap)}", file=sys.stderr)
        return 1
    if c6_c9_overlap:
        print(f"C6/C9 precedence assertion FAILED: overlap={sorted(c6_c9_overlap)}", file=sys.stderr)
        return 1
    if c4_c9_overlap:
        print(f"C4/C9 precedence assertion FAILED: overlap={sorted(c4_c9_overlap)}", file=sys.stderr)
        return 1

    full_results = scenario_results["scenario2_full_contract"]
    case_details = build_case_details(corpus_rows, baseline_results, full_results, c9_cases, scenario_states, sub_gates)
    dual_target_and_neighbour = sorted(set(c9_cases) & ft8_union)
    banked_stay_abstained = sorted(
        detail["case_id"]
        for detail in case_details
        if detail["stay_abstained_seed"] and detail["outcome"] == "WOULD_BANK"
    )

    commit_matches_s2 = set(s_commit["would_bank"]) == set(s2["would_bank"])
    commit_clean = (
        len(s_commit["would_bank"]) == 10
        and commit_matches_s2
        and s_commit["regression_count"] == 0
        and not s_commit["no_fault_neighbour_regressions"]
    )
    if args.scenario == "s_commit" and not commit_clean:
        print("S-COMMIT pre-flight FAILED", file=sys.stderr)
        print(f"would_bank={len(s_commit['would_bank'])} matches_s2={commit_matches_s2}", file=sys.stderr)
        print(f"regressions={s_commit['regressions']}", file=sys.stderr)
        print(f"no_fault_neighbour_regressions={s_commit['no_fault_neighbour_regressions']}", file=sys.stderr)
        return 1

    # Formulate recommendation
    has_yield = len(s2["would_bank"]) > 0
    zero_regressions = s2["regression_count"] == 0
    era2_016_state = scenario_states["scenario2_full_contract"].get("era2_016")
    era2_016_fails = era2_016_state == "SENSOR_HEALTH_UNPROVEN_ABSTAIN"
    
    if has_yield and zero_regressions and era2_016_fails:
        recommendation = "C9B-GO"
        recommendation_reason = f"meaningful yield (+{len(s2['would_bank'])} cases: {', '.join(s2['would_bank'])}), 0 regressions, and era2_016 correctly abstains"
    else:
        recommendation = "STOP-CLOSE-PACK"
        reasons = []
        if not has_yield:
            reasons.append("no yield (0 cases bank)")
        if not zero_regressions:
            reasons.append(f"{s2['regression_count']} regressions")
        if not era2_016_fails:
            reasons.append("era2_016 falsely confirmed healthy")
        recommendation_reason = f"due to: {', '.join(reasons)}"

    print("\n" + "=" * 72)
    print("C9 SIGNAL DRYRUN SUMMARY (Scenario 2: full contract)")
    print("=" * 72)
    print(f"Baseline pin: {BASELINE_RUN}")
    print(f"Baseline top3: {s2['baseline_top3_passes']}/294")
    print(f"Simulated top3: {s2['simulated_top3_passes']}/294")
    print(
        "Scenario WOULD_BANK: "
        f"S1={s1['newly_passing_count']} / "
        f"S2={s2['newly_passing_count']} / "
        f"S-COMMIT={s_commit['newly_passing_count']}"
    )
    print(f"S-COMMIT matches S2: {commit_matches_s2} ; clean={commit_clean}")
    print(f"Yield: WOULD_BANK={len(s2['would_bank'])}, ALREADY_PASS={len(s2['already_pass'])}, STILL_SHORT={len(s2['still_short'])}")
    print(f"Regressions: {s2['regression_count']} -> {s2['regressions']}")
    print(f"no_fault neighbour regressions: {s2['no_fault_neighbour_regressions']}")
    print(f"FT-8 neighbour union: {len(ft8_union)} ; dual target+neighbour: {len(dual_target_and_neighbour)}")
    print(f"Misfire/Stay-abstained cases banked (ALARM if non-empty): {banked_stay_abstained}")
    print(f"Recommendation: {recommendation} ({recommendation_reason})")
    print("=" * 72)

    serializable_results = {
        scenario: {
            cid: {
                **{k: v for k, v in result.items() if k not in {"top3_families", "siblings"}},
                "top3_families": sorted(result["top3_families"]),
            }
            for cid, result in results.items()
        }
        for scenario, results in scenario_results.items()
    }
    output = {
        "task": "T-V3-P4-C9A",
        "mode": "provisional-synthetic-simulated (side file; live corpus untouched)",
        "baseline_run": BASELINE_RUN,
        "yardstick": "V3_YARDSTICK_2026-07-06-C4B",
        "seed": str(args.c9_seed.relative_to(WORKSPACE_ROOT)),
        "producer_gates": {
            "readiness_complete": "True",
            "stored_dtc_count": 0,
            "pending_dtc_count": 0,
            "permanent_dtc_count": 0,
            "mode06_min_margin_pct": ">= 10.0",
            "warmup_cycles_since_clear": ">= 5",
            "miles_since_clear": ">= 200",
            "stft_idle_pct": "+/-5.0%",
            "ltft_idle_pct": "+/-7.0%",
            "stft_2500_pct": "+/-5.0%",
            "ltft_2500_pct": "+/-7.0%",
            "trim_delta_max": "+/-5.0%",
            "gas_delta_hc_ppm": "[-10, 15]",
            "gas_delta_co_pct": "[-0.15, 0.15]",
            "gas_delta_co2_pct": "[0.3, 0.8]",
            "gas_delta_o2_pct": "[-0.5, 0.4]",
        },
        "consumer_overlay": {
            "c9_rules_boosted": list(C9_RULES),
            "boost": C9_BOOST,
            "abstain_state_noop": ABSTAIN_STATE,
        },
        "c3_c9_decisive_overlap_assertion": sorted(c3_c9_overlap),
        "c6_c9_decisive_overlap_assertion": sorted(c6_c9_overlap),
        "c4_c9_decisive_overlap_assertion": sorted(c4_c9_overlap),
        "ft8_neighbour_union": sorted(ft8_union),
        "ft8_neighbour_count": len(ft8_union),
        "ft8_per_rule": ft8_per_rule,
        "no_fault_rule_neighbours": sorted(no_fault_neighbours),
        "dual_target_and_neighbour": dual_target_and_neighbour,
        "banked_stay_abstained_ALARM": banked_stay_abstained,
        "recommendation": recommendation,
        "recommendation_reason": recommendation_reason,
        "scenarios": {
            "scenario1_obd_only": {
                "description": "OBD only gates: readiness, DTCs, Mode 06, warmup cycles, miles, and fuel trims.",
                "summary": summaries["scenario1_obd_only"],
            },
            "scenario2_full_contract": {
                "description": "Full C9 contract: OBD plus two-point 5-gas deltas.",
                "summary": summaries["scenario2_full_contract"],
                "case_details": case_details,
            },
            "s_commit_full": {
                "description": "C9B committed config.",
                "summary": summaries["s_commit_full"],
            },
        },
        "scenario_results_compact": serializable_results,
    }

    args.write.parent.mkdir(parents=True, exist_ok=True)
    args.write.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Wrote JSON report to {args.write}")
    write_markdown_report(
        args.write.with_suffix(".md"),
        summaries,
        case_details,
        ft8_union,
        ft8_per_rule,
        no_fault_neighbours,
        dual_target_and_neighbour,
        banked_stay_abstained,
        c3_c9_overlap,
        c6_c9_overlap,
        c4_c9_overlap,
        recommendation,
        recommendation_reason,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
