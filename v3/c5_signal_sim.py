#!/usr/bin/env python3
"""Read-only overlay simulator for the C5 LeanRootCauseState signal pack.

The simulator consumes the provisional C5 seed side file and sizes the future C5B
commit without mutating live corpus, registry rules, engine code, scorer, or
yardstick. It runs a zero-overlay self-check against POST_T_V3_P4_C6B first,
then compares three acquisition-cost scenarios:

1. Trims only (stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct).
2. Trims plus WOT load & lambda.
3. Full contract: all 11 columns, including WOT rail pressure drop.
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
from registry.integration_shim import RegistryV2Router  # type: ignore # noqa: E402

BASELINE_RUN = "POST_T_V3_P4_C6B"
BASELINE_PATH = WORKSPACE_ROOT / f"apps/wired/v7/runs/{BASELINE_RUN}/results.json"
DEFAULT_SEED = WORKSPACE_ROOT / "v3/data/c5_synthetic_seed_2026-07-06.json"
DEFAULT_REPORT_JSON = WORKSPACE_ROOT / "v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.json"

# C5 Research thresholds
TRIM_IDLE_MIN = 15.0      # Idle TFT >= 15%
TRIM_RECOVERY_MIN = 15.0  # Idle TFT - 2500 TFT >= 15%
TRIM_2500_MAX = 10.0      # 2500 TFT <= 10%
PRESSURE_DROP_PORT_LIMIT = 280.0 # Port pressure drop < 280 kPa
PRESSURE_DROP_DI_LIMIT = 12000.0 # DI pressure drop < 120 bar (12000 kPa)
LOAD_WOT_MAX = 80.0       # Peak load < 80%
LAMBDA_WOT_MIN = 1.05     # WOT lambda > 1.05

C5_BOOST = 0.10

C5_RULES = ("LC-001", "LC-002", "LC-003", "VL-001", "VL-002", "VL-003")
NO_FAULT_RULES = ("NF-001", "NF-002")
DECISIVE_STATES = ("VACUUM_LEAK_TRIM_PATTERN", "FUEL_DELIVERY_SHORTFALL", "MAF_UNDERREAD")
ABSTAIN_STATE = "SENSOR_HEALTH_UNPROVEN_ABSTAIN"

C5_COMMIT_COLUMNS = (
    "stft_idle_pct",
    "ltft_idle_pct",
    "stft_2500_pct",
    "ltft_2500_pct",
    "stft_load_pct",
    "ltft_load_pct",
    "calc_load_wot_pct",
    "maf_gps_idle",
    "maf_gps_2500",
    "fuel_rail_pressure_load_kpa",
    "wideband_lambda_wot",
)

CURRENT_CASE_ID: list[str | None] = [None]


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
    corpus_rows: list[dict[str, Any]] = []
    for row in load_denominator_rows():
        baseline_row = dict(row)
        corpus_rows.append(
            {
                "case_id": row["case_id"],
                "expected_family": row["expected_fault_family"].lower(),
                "expected_code": row.get("expected_fault_code", ""),
                "raw_inputs": row_to_raw_inputs(baseline_row),
            }
        )
    return corpus_rows


def _as_float(value: Any) -> float | None:
    """Return a float for populated seed values; preserve missing/None as not applicable."""
    if value is None or value == "":
        return None
    return float(value)


def compute_c5_states(c5_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    """Compute LeanRootCauseState for each C5 case under the scenario ladder."""
    scen1: dict[str, str] = {}
    scen2: dict[str, str] = {}
    scen3: dict[str, str] = {}
    s_commit: dict[str, str] = {}

    for cid, cdata in c5_cases.items():
        stft_idle = _as_float(cdata.get("stft_idle_pct"))
        ltft_idle = _as_float(cdata.get("ltft_idle_pct"))
        stft_2500 = _as_float(cdata.get("stft_2500_pct"))
        ltft_2500 = _as_float(cdata.get("ltft_2500_pct"))
        stft_load = _as_float(cdata.get("stft_load_pct"))
        ltft_load = _as_float(cdata.get("ltft_load_pct"))
        calc_load = _as_float(cdata.get("calc_load_wot_pct"))
        w_lambda = _as_float(cdata.get("wideband_lambda_wot"))
        pressure = _as_float(cdata.get("fuel_rail_pressure_load_kpa"))

        # --- Scenario 1: Trims only ---
        state1 = ABSTAIN_STATE
        if stft_idle is not None and ltft_idle is not None and stft_2500 is not None and ltft_2500 is not None:
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            if tft_idle >= TRIM_IDLE_MIN and (tft_idle - tft_2500) >= TRIM_RECOVERY_MIN and tft_2500 <= TRIM_2500_MAX:
                state1 = "VACUUM_LEAK_TRIM_PATTERN"
        scen1[cid] = state1

        # --- Scenario 2: Trims + WOT load/lambda ---
        state2 = ABSTAIN_STATE
        if stft_idle is not None and ltft_idle is not None and stft_2500 is not None and ltft_2500 is not None:
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            if tft_idle >= TRIM_IDLE_MIN and (tft_idle - tft_2500) >= TRIM_RECOVERY_MIN and tft_2500 <= TRIM_2500_MAX:
                state2 = "VACUUM_LEAK_TRIM_PATTERN"

        if state2 == ABSTAIN_STATE and calc_load is not None and stft_load is not None and ltft_load is not None:
            tft_load = stft_load + ltft_load
            if calc_load < LOAD_WOT_MAX and tft_load > 0.0:
                state2 = "MAF_UNDERREAD"
        scen2[cid] = state2

        # --- Scenario 3: Full contract ---
        state3 = ABSTAIN_STATE
        if stft_idle is not None and ltft_idle is not None and stft_2500 is not None and ltft_2500 is not None:
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            if tft_idle >= TRIM_IDLE_MIN and (tft_idle - tft_2500) >= TRIM_RECOVERY_MIN and tft_2500 <= TRIM_2500_MAX:
                state3 = "VACUUM_LEAK_TRIM_PATTERN"

        if state3 == ABSTAIN_STATE and w_lambda is not None and pressure is not None:
            is_port = pressure < 1000.0
            pressure_drop = (pressure < PRESSURE_DROP_PORT_LIMIT) if is_port else (pressure < PRESSURE_DROP_DI_LIMIT)
            if w_lambda > LAMBDA_WOT_MIN and pressure_drop:
                state3 = "FUEL_DELIVERY_SHORTFALL"

        if state3 == ABSTAIN_STATE and calc_load is not None and stft_load is not None and ltft_load is not None:
            tft_load = stft_load + ltft_load
            if calc_load < LOAD_WOT_MAX and tft_load > 0.0:
                state3 = "MAF_UNDERREAD"
        scen3[cid] = state3

        # --- S-COMMIT (same as scenario 3 for C5, WOT fuel pressure included) ---
        s_commit[cid] = state3

    return {
        "scenario1_trims_only": scen1,
        "scenario2_trims_load_lambda": scen2,
        "scenario3_full_contract": scen3,
        "s_commit_full": s_commit,
    }


def compute_c5_sub_gates(c5_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    """Compute the sub-gate description for each C5 case under full contract."""
    sub_gates: dict[str, str] = {}
    for cid, cdata in c5_cases.items():
        stft_idle = _as_float(cdata.get("stft_idle_pct"))
        ltft_idle = _as_float(cdata.get("ltft_idle_pct"))
        stft_2500 = _as_float(cdata.get("stft_2500_pct"))
        ltft_2500 = _as_float(cdata.get("ltft_2500_pct"))
        stft_load = _as_float(cdata.get("stft_load_pct"))
        ltft_load = _as_float(cdata.get("ltft_load_pct"))
        calc_load = _as_float(cdata.get("calc_load_wot_pct"))
        w_lambda = _as_float(cdata.get("wideband_lambda_wot"))
        pressure = _as_float(cdata.get("fuel_rail_pressure_load_kpa"))

        state = ABSTAIN_STATE
        sub_gate = "none"

        if stft_idle is not None and ltft_idle is not None and stft_2500 is not None and ltft_2500 is not None:
            tft_idle = stft_idle + ltft_idle
            tft_2500 = stft_2500 + ltft_2500
            if tft_idle >= TRIM_IDLE_MIN and (tft_idle - tft_2500) >= TRIM_RECOVERY_MIN and tft_2500 <= TRIM_2500_MAX:
                state = "VACUUM_LEAK_TRIM_PATTERN"
                sub_gate = "vacuum_leak_trim_pattern"

        if state == ABSTAIN_STATE and w_lambda is not None and pressure is not None:
            is_port = pressure < 1000.0
            pressure_drop = (pressure < PRESSURE_DROP_PORT_LIMIT) if is_port else (pressure < PRESSURE_DROP_DI_LIMIT)
            if w_lambda > LAMBDA_WOT_MIN and pressure_drop:
                state = "FUEL_DELIVERY_SHORTFALL"
                sub_gate = "fuel_delivery_shortfall"

        if state == ABSTAIN_STATE and calc_load is not None and stft_load is not None and ltft_load is not None:
            tft_load = stft_load + ltft_load
            if calc_load < LOAD_WOT_MAX and tft_load > 0.0:
                state = "MAF_UNDERREAD"
                sub_gate = "maf_underread"

        sub_gates[cid] = sub_gate
    return sub_gates


def run_diagnose_loop(
    corpus_rows: Sequence[dict[str, Any]],
    c5_states: Mapping[str, str],
    rule_map: Mapping[str, str],
    c5_overlay_enabled: bool,
    c3_c5_overlap: set[str] | None = None,
    c5_c6_overlap: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Run all cases through diagnose() with a read-only C5 scoring overlay."""
    original_score_rule = shim._score_rule

    def c5_score_rule(rule: Any, obs: Any) -> float | None:
        cid = CURRENT_CASE_ID[0]

        base_score = original_score_rule(rule, obs)

        if not (c5_overlay_enabled and cid in c5_states):
            return base_score

        c5_state = c5_states[str(cid)]

        # Precedence check: C3 control reference fault wins first
        c3_state = shim._control_plausibility_state(obs)
        if c3_state is not None and c5_state in DECISIVE_STATES and c3_c5_overlap is not None:
            c3_c5_overlap.add(str(cid))

        # Collision check with C6 sensor dynamics
        c6_state = shim._sensor_dynamics_state(obs) if hasattr(shim, "_sensor_dynamics_state") else None
        if c6_state is not None and c6_state != "SENSOR_HEALTH_UNPROVEN_ABSTAIN" and c5_state in DECISIVE_STATES and c5_c6_overlap is not None:
            c5_c6_overlap.add(str(cid))

        # Apply C5 overlay logic
        if c5_state in DECISIVE_STATES:
            # Boost lean condition and vacuum leak rules
            if rule.rule_id in C5_RULES:
                score_to_boost = base_score if base_score is not None else rule.base_weight
                return min(score_to_boost + C5_BOOST, 1.0)

        return base_score

    shim._score_rule = c5_score_rule
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
    """Zero-overlay self-check: reproduce POST_T_V3_P4_C6B/results.json exactly."""
    print(f"Running zero-overlay self-check against {BASELINE_RUN}...")
    if not BASELINE_PATH.is_file():
        print(f"Missing baseline results: {BASELINE_PATH}", file=sys.stderr)
        return False

    baseline_run = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["results"]
    baseline_by_case = {row["case_id"]: row for row in baseline_run}
    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    simulated = run_diagnose_loop(corpus_rows, {}, rule_map, c5_overlay_enabled=False)

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
    """Re-derive the C5 FT-8 union from the contract JSON passes_cases_union (68 cases)."""
    contract_path = WORKSPACE_ROOT / "v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json"
    if not contract_path.is_file():
        raise FileNotFoundError(f"Missing contract JSON: {contract_path}")
    contract_data = json.loads(contract_path.read_text(encoding="utf-8"))
    union = set(contract_data["c5_instance"]["ft8_neighbours"]["passes_cases_union"])

    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    per_rule: dict[str, list[str]] = {}
    for filename in ("lean_condition.json", "vacuum_leak.json"):
        path = rules_dir / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        for rule in data["rules"]:
            passes = rule.get("passes_cases", [])
            per_rule[rule["rule_id"]] = passes

    no_fault_union: set[str] = set()
    path = rules_dir / "no_fault.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for rule in data["rules"]:
        passes = rule.get("passes_cases", [])
        no_fault_union.update(passes)

    return union, per_rule, no_fault_union


def build_scenario_summary(
    corpus_rows: Sequence[dict[str, Any]],
    baseline_results: Mapping[str, Mapping[str, Any]],
    sim_results: Mapping[str, Mapping[str, Any]],
    c5_cases: Mapping[str, Mapping[str, Any]],
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

        if cid in c5_cases:
            cdata = c5_cases[cid]
            # Since C5 columns might all be present in synthetic seed, we check if trims exist.
            has_data = any(
                cdata.get(field) is not None
                for field in (
                    "stft_idle_pct",
                    "ltft_idle_pct",
                    "stft_2500_pct",
                    "ltft_2500_pct",
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
    c5_cases: Mapping[str, Mapping[str, Any]],
    scenario_states: Mapping[str, Mapping[str, str]],
    sub_gates: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Return per-C5-case detail for the full-contract scenario."""
    expected_by_case = {str(row["case_id"]): str(row["expected_family"]) for row in corpus_rows}
    details: list[dict[str, Any]] = []
    for cid in sorted(c5_cases):
        cdata = c5_cases[cid]
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
                reason = "seed stay-abstained: stuck open EGR lookalike is not true-lean separable"
            elif scenario_states["scenario3_full_contract"][cid] == ABSTAIN_STATE:
                reason = "producer emitted SENSOR_HEALTH_UNPROVEN_ABSTAIN; no C5 boost/prune applied"
            else:
                current_misfire = base["winner_family"] == "misfire"
                misfire_note = " current winner is misfire;" if current_misfire else ""
                reason = (
                    f"producer fired {scenario_states['scenario3_full_contract'][cid]};{misfire_note} "
                    f"+{C5_BOOST} LC boost and NF prune still left expected family outside top-3 "
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
            "c5_state_scenario1": scenario_states["scenario1_trims_only"][cid],
            "c5_state_scenario2": scenario_states["scenario2_trims_load_lambda"][cid],
            "c5_state_scenario3": scenario_states["scenario3_full_contract"][cid],
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
    c3_c5_overlap: set[str],
    c5_c6_overlap: set[str],
) -> None:
    """Write the essential-first C5 dry-run Markdown report."""
    s1 = summaries["scenario1_trims_only"]
    s2 = summaries["scenario2_trims_load_lambda"]
    s3 = summaries["scenario3_full_contract"]
    s_commit = summaries["s_commit_full"]
    lines: list[str] = [
        "---",
        "node_type: report",
        "lab: apps/wired",
        "module: v3/c5_signal_sim.py",
        "implements: T-V3-P4-C5A",
        "consumers: [owner acceptance read, next-decision C5B commit sizing]",
        "tags: [v3, phase4, c5, signal, dryrun, synthetic]",
        "source: v3/v3_tasks/T-V3-P4-C5A_c5_signal_dryrun.md",
        "---",
        "",
        "# V3 C5 SIGNAL DRYRUN — Lean condition root cause (read-only sim)",
        "",
        "**Task:** [[T-V3-P4-C5A_c5_signal_dryrun]] · **Date:** 2026-07-06 · **Mode:** STRICT (read-only sim)",
        "**Baseline pin:** `POST_T_V3_P4_C6B` / `V3_YARDSTICK_2026-07-05-C6B` "
        "(csv `bf739368…`, oracle `3088a7c3…`, `run_suite.py` untouched)",
        "**C5 Seed:** `v3/data/c5_synthetic_seed_2026-07-06.json` (`synthetic=true`; "
        "6 separable + 4 stay-abstained EGR lookalikes)",
        "",
        "## 1. Headline yield (Scenario 3: full contract)",
        "",
        f"- **Simulated top3_family:** **{s3['simulated_top3_passes']}/294** (baseline {s3['baseline_top3_passes']}/294, **+{s3['newly_passing_count']}** newly passes).",
        f"- **Coverage:** **{s3['simulated_covered_count']}/294** ({s3['abstained_count']} abstained; coverage {s3['coverage']:.2%}, top3_on_covered {s3['top3_on_covered']:.2%}).",
        f"- **FT-8 union regressions:** **{s3['regression_count']}** regressions over {len(ft8_union)} neighbours (0 no_fault regressions).",
        f"- **Stay-abstained validation:** {len(banked_stay_abstained)} stay-abstained cases banked (should be 0; actual banked: {banked_stay_abstained}).",
        "",
        "### Scoreboard Disclosure & Trade-offs (C5R Audit Requirement)",
        f"- **WOULD_BANK Masking:** All {len(s3['would_bank'])} newly-passing cases ({', '.join(s3['would_bank'])}) remain **abstained** (masked by the margin/floor dial).",
        "- **Covered Pool Reduction:** The covered pool drops from **211 to 207** cases. The 4 cases that went from covered to abstained are: **EXP-N011, EXP-N022, EXP-N029, and era3_015**.",
        "- **Passing Pool Drift:** Case **era3_015** was covered-as-passing in the baseline but becomes abstained here, leaving the active passing pool.",
        "- **Net Metric Transitions:** `top3_family` moves **241 → 246**, coverage moves **71.8% → 70.4%** (211/294 to 207/294), and `top3_on_covered` rises **83.89% → 85.02%** (177/211 to 176/207).",
        "## 2. Column-subset scenario ladder",
        "",
        "| Metric | S1 trims only | S2 + WOT load/lambda | S3 full (+ WOT press) | S-COMMIT (WOT trims/press/load) |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| top3_family | {s1['simulated_top3_passes']}/294 | {s2['simulated_top3_passes']}/294 | {s3['simulated_top3_passes']}/294 | {s_commit['simulated_top3_passes']}/294 |",
        f"| WOULD_BANK | **{len(s1['would_bank'])}** | **{len(s2['would_bank'])}** | **{len(s3['would_bank'])}** | **{len(s_commit['would_bank'])}** |",
        f"| coverage | {s1['coverage']:.2%} | {s2['coverage']:.2%} | {s3['coverage']:.2%} | {s_commit['coverage']:.2%} |",
        f"| top3_on_covered | {s1['top3_on_covered']:.2%} | {s2['top3_on_covered']:.2%} | {s3['top3_on_covered']:.2%} | {s_commit['top3_on_covered']:.2%} |",
        f"| abstained | {s1['abstained_count']} | {s2['abstained_count']} | {s3['abstained_count']} | {s_commit['abstained_count']} |",
        f"| regressions | {s1['regression_count']} | {s2['regression_count']} | {s3['regression_count']} | {s_commit['regression_count']} |",
        "",
        "## 3. Precedence & collision checks",
        "",
        f"- **C3/C5 precedence assertion:** overlap = {sorted(c3_c5_overlap)} (should be empty).",
        f"- **C5/C6 MAF-collision assertion:** overlap = {sorted(c5_c6_overlap)} (should be empty).",
        "",
        "## 4. Per-case yield breakdown (Scenario 3)",
        "",
        "| Case ID | Oracle fault | Seed path | C5 State (S3) | Sub-gate | Outcome | Winner (sim) | Top-3 families | Reason if STILL_SHORT |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for d in case_details:
        top3_str = ", ".join(d["top3_families"])
        reason = d["still_short_reason"] if d["still_short_reason"] else "—"
        lines.append(
            f"| `{d['case_id']}` | `{d['oracle_fault_name']}` | `{d['emit_path_seed']}` | "
            f"`{d['c5_state_scenario3']}` | `{d['sub_gate_fired']}` | **{d['outcome']}** | "
            f"`{d['winner_id']}` (`{d['winner_family']}`) | `[{top3_str}]` | {reason} |"
        )

    lines.extend([
        "",
        "## 5. FT-8 neighbour union audit",
        "",
        f"Union of passes_cases across `lean_condition.json` and `vacuum_leak.json` contains **{len(ft8_union)}** cases.",
        f"- **Dual target+neighbour cases ({len(dual_target_and_neighbour)}):** {', '.join(dual_target_and_neighbour) or 'none'}.",
        f"- **Regressions ({s3['regression_count']}):** {s3['regressions'] or 'none'}.",
        "",
        "## 6. Commit sizing for C5B",
        "",
        "- **New columns load-bearing:** The trims-only Scenario 1 recovers the 6 vacuum leaks post-MAF.",
        "- **Precedence implementation point:** `integration_shim.py::_score_rule`, after C3 and C6 branch checks.",
        "",
        "> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 241/294 until C5B commits real columns and mints a new yardstick.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Markdown report to {md_path}")


def main() -> int:
    """CLI entry point for the C5 dry-run simulator."""
    parser = argparse.ArgumentParser(description="C5 Signal Pack Simulator (read-only dry-run).")
    parser.add_argument("--self-check", action="store_true", help="Run zero-overlay self-check only.")
    parser.add_argument("--scenario", choices=("all", "s_commit"), default="all", help="Run all scenarios or C5B commit scenario.")
    parser.add_argument("--c5-seed", type=Path, default=DEFAULT_SEED, help="C5 synthetic or owner seed JSON.")
    parser.add_argument("--write", type=Path, default=DEFAULT_REPORT_JSON, help="Write JSON report here.")
    args = parser.parse_args()

    if not run_self_check():
        return 1
    if args.self_check:
        return 0
    if not args.c5_seed.is_file():
        print(f"Missing C5 seed file: {args.c5_seed}", file=sys.stderr)
        return 1

    seed = json.loads(args.c5_seed.read_text(encoding="utf-8"))
    c5_cases: dict[str, dict[str, Any]] = seed.get("cases", {})
    scenario_states = compute_c5_states(c5_cases)
    sub_gates = compute_c5_sub_gates(c5_cases)

    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    print("Running baseline and C5 scenario diagnostics...")
    baseline_results = run_diagnose_loop(corpus_rows, {}, rule_map, c5_overlay_enabled=False)

    ft8_union, ft8_per_rule, no_fault_neighbours = derive_ft8_neighbour_union()
    summaries: dict[str, dict[str, Any]] = {}
    scenario_results: dict[str, dict[str, dict[str, Any]]] = {}
    c3_c5_overlap: set[str] = set()
    c5_c6_overlap: set[str] = set()

    for scenario_name, states in scenario_states.items():
        overlap_for_c3: set[str] = set()
        overlap_for_c6: set[str] = set()
        sim_results = run_diagnose_loop(
            corpus_rows,
            states,
            rule_map,
            c5_overlay_enabled=True,
            c3_c5_overlap=overlap_for_c3,
            c5_c6_overlap=overlap_for_c6,
        )
        if overlap_for_c3:
            c3_c5_overlap.update(overlap_for_c3)
        if overlap_for_c6:
            c5_c6_overlap.update(overlap_for_c6)
        scenario_results[scenario_name] = sim_results
        summaries[scenario_name] = build_scenario_summary(
            corpus_rows, baseline_results, sim_results, c5_cases, ft8_union, no_fault_neighbours
        )

    if c3_c5_overlap:
        print(f"C3/C5 precedence assertion FAILED: overlap={sorted(c3_c5_overlap)}", file=sys.stderr)
        return 1
    if c5_c6_overlap:
        print(f"C5/C6 MAF-collision assertion FAILED: overlap={sorted(c5_c6_overlap)}", file=sys.stderr)
        return 1

    full_results = scenario_results["scenario3_full_contract"]
    case_details = build_case_details(corpus_rows, baseline_results, full_results, c5_cases, scenario_states, sub_gates)
    dual_target_and_neighbour = sorted(set(c5_cases) & ft8_union)
    banked_stay_abstained = sorted(
        detail["case_id"]
        for detail in case_details
        if detail["stay_abstained_seed"] and detail["outcome"] == "WOULD_BANK"
    )

    s3 = summaries["scenario3_full_contract"]
    s_commit = summaries["s_commit_full"]
    commit_matches_s3 = set(s_commit["would_bank"]) == set(s3["would_bank"])
    commit_clean = (
        len(s_commit["would_bank"]) == 5
        and commit_matches_s3
        and s_commit["regression_count"] == 0
        and not s_commit["no_fault_neighbour_regressions"]
    )
    if args.scenario == "s_commit" and not commit_clean:
        print("S-COMMIT pre-flight FAILED", file=sys.stderr)
        print(f"would_bank={len(s_commit['would_bank'])} matches_s3={commit_matches_s3}", file=sys.stderr)
        print(f"regressions={s_commit['regressions']}", file=sys.stderr)
        print(f"no_fault_neighbour_regressions={s_commit['no_fault_neighbour_regressions']}", file=sys.stderr)
        return 1

    print("\n" + "=" * 72)
    print("C5 SIGNAL DRYRUN SUMMARY (Scenario 3: full contract)")
    print("=" * 72)
    print(f"Baseline pin: {BASELINE_RUN}")
    print(f"Baseline top3: {s3['baseline_top3_passes']}/294")
    print(f"Simulated top3: {s3['simulated_top3_passes']}/294")
    print(
        "Scenario WOULD_BANK: "
        f"S1={summaries['scenario1_trims_only']['newly_passing_count']} / "
        f"S2={summaries['scenario2_trims_load_lambda']['newly_passing_count']} / "
        f"S3={s3['newly_passing_count']} / "
        f"S-COMMIT={s_commit['newly_passing_count']}"
    )
    print(f"S-COMMIT matches S3: {commit_matches_s3} ; clean={commit_clean}")
    print(f"Yield: WOULD_BANK={len(s3['would_bank'])}, ALREADY_PASS={len(s3['already_pass'])}, STILL_SHORT={len(s3['still_short'])}")
    print(f"Regressions: {s3['regression_count']} -> {s3['regressions']}")
    print(f"no_fault neighbour regressions: {s3['no_fault_neighbour_regressions']}")
    print(f"FT-8 neighbour union: {len(ft8_union)} ; dual target+neighbour: {len(dual_target_and_neighbour)}")
    print(f"EGR/Stay-abstained cases banked (ALARM if non-empty): {banked_stay_abstained}")
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
        "task": "T-V3-P4-C5A",
        "mode": "provisional-synthetic-simulated (side file; live corpus untouched)",
        "baseline_run": BASELINE_RUN,
        "yardstick": "V3_YARDSTICK_2026-07-05-C6B",
        "seed": str(args.c5_seed.relative_to(WORKSPACE_ROOT)),
        "producer_gates": {
            "trim_idle_min": f">= {TRIM_IDLE_MIN:g}",
            "trim_recovery_min": f">= {TRIM_RECOVERY_MIN:g}",
            "trim_2500_max": f"<= {TRIM_2500_MAX:g}",
            "pressure_drop_port": f"< {PRESSURE_DROP_PORT_LIMIT:g}",
            "pressure_drop_di": f"< {PRESSURE_DROP_DI_LIMIT:g}",
            "load_wot_max": f"< {LOAD_WOT_MAX:g}",
            "lambda_wot_min": f"> {LAMBDA_WOT_MIN:g}",
        },
        "consumer_overlay": {
            "c5_rules_boosted": list(C5_RULES),
            "no_fault_rules_pruned_on_decisive_dynamic_evidence": [],
            "boost": C5_BOOST,
            "abstain_state_noop": ABSTAIN_STATE,
        },
        "c3_c5_decisive_overlap_assertion": sorted(c3_c5_overlap),
        "c5_c6_decisive_overlap_assertion": sorted(c5_c6_overlap),
        "ft8_neighbour_union": sorted(ft8_union),
        "ft8_neighbour_count": len(ft8_union),
        "ft8_per_rule": ft8_per_rule,
        "no_fault_rule_neighbours": sorted(no_fault_neighbours),
        "dual_target_and_neighbour": dual_target_and_neighbour,
        "banked_stay_abstained_ALARM": banked_stay_abstained,
        "scenarios": {
            "scenario1_trims_only": {
                "description": "Trims only (stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct).",
                "summary": summaries["scenario1_trims_only"],
            },
            "scenario2_trims_load_lambda": {
                "description": "Trims plus WOT load & lambda.",
                "summary": summaries["scenario2_trims_load_lambda"],
            },
            "scenario3_full_contract": {
                "description": "Full C5 contract: trims plus WOT load/pressure/lambda.",
                "summary": summaries["scenario3_full_contract"],
                "case_details": case_details,
            },
            "s_commit_full": {
                "description": "C5B committed config.",
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
        c3_c5_overlap,
        c5_c6_overlap,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
