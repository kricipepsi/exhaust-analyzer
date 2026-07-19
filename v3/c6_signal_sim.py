#!/usr/bin/env python3
"""Read-only overlay simulator for the C6 SensorDynamicsState signal pack.

The simulator consumes the provisional C6 seed side file and sizes the future C6B
commit without mutating live corpus, registry rules, engine code, scorer, or
yardstick. It runs a zero-overlay self-check against POST_T_V3_P4_C3B first,
then compares three acquisition-cost scenarios:

1. Mode $06 O2 monitor margin only.
2. Mode $06 plus active rich->lean / lean->rich O2 timing.
3. Full contract: O2 dynamics plus two-point MAF actual-vs-calculated airflow.
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

BASELINE_RUN = "POST_T_V3_P4_C3B"
BASELINE_PATH = WORKSPACE_ROOT / f"apps/wired/v7/runs/{BASELINE_RUN}/results.json"
DEFAULT_SEED = WORKSPACE_ROOT / "v3/data/c6_synthetic_seed_2026-07-05.json"
DEFAULT_REPORT_JSON = WORKSPACE_ROOT / "v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.json"

MODE06_MARGIN_GATE_PCT = 10.0  # C6-PRE §2: low margin to vehicle-specific limit fires.
O2_RESPONSE_SLOW_MS = 600.0  # C6-SYNTH §3: wide provisional slow-response lower corner.
MAF_UNDERREAD_GATE_PCT = -15.0  # C6-PRE §2: sustained >10–15% under-read at both points.
C6_BOOST = 0.10  # Mirrors existing C2/C3/C4 dry-run/commit boost pattern.

SENSOR_RULES = ("SF-005", "SF-008", "SF-001", "SF-002")
NO_FAULT_RULES = ("NF-001", "NF-002")
DECISIVE_STATES = ("O2_LAZY_OR_BIASED", "MAF_UNDERREAD")
ABSTAIN_STATE = "SENSOR_HEALTH_UNPROVEN_ABSTAIN"
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
    """Return a float for populated seed values; preserve missing/None as not applicable."""
    if value is None or value == "":
        return None
    return float(value)


def compute_c6_states(c6_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, dict[str, str]]:
    """Compute SensorDynamicsState for each C6 case under the three scenario ladder."""
    scen1: dict[str, str] = {}
    scen2: dict[str, str] = {}
    scen3: dict[str, str] = {}

    for cid, cdata in c6_cases.items():
        mode06 = _as_float(cdata.get("mode06_o2_response_margin_pct"))
        rich_to_lean = _as_float(cdata.get("o2_rich_to_lean_ms"))
        lean_to_rich = _as_float(cdata.get("o2_lean_to_rich_ms"))
        maf_idle = _as_float(cdata.get("maf_actual_calc_delta_pct_idle"))
        maf_2500 = _as_float(cdata.get("maf_actual_calc_delta_pct_2500"))

        mode06_fires = mode06 is not None and mode06 <= MODE06_MARGIN_GATE_PCT
        o2_timing_fires = (
            (rich_to_lean is not None and rich_to_lean >= O2_RESPONSE_SLOW_MS)
            or (lean_to_rich is not None and lean_to_rich >= O2_RESPONSE_SLOW_MS)
        )
        maf_fires = (
            maf_idle is not None
            and maf_2500 is not None
            and maf_idle <= MAF_UNDERREAD_GATE_PCT
            and maf_2500 <= MAF_UNDERREAD_GATE_PCT
        )

        scen1[cid] = "O2_LAZY_OR_BIASED" if mode06_fires else ABSTAIN_STATE
        scen2[cid] = "O2_LAZY_OR_BIASED" if mode06_fires or o2_timing_fires else ABSTAIN_STATE
        if mode06_fires or o2_timing_fires:
            scen3[cid] = "O2_LAZY_OR_BIASED"
        elif maf_fires:
            scen3[cid] = "MAF_UNDERREAD"
        else:
            scen3[cid] = ABSTAIN_STATE

    return {
        "scenario1_mode06_only": scen1,
        "scenario2_mode06_plus_o2_timing": scen2,
        "scenario3_full_contract": scen3,
    }


def compute_c6_sub_gates(c6_cases: Mapping[str, Mapping[str, Any]]) -> dict[str, str]:
    """Record every producer sub-gate fired under the full C6 contract."""
    gates: dict[str, str] = {}
    for cid, cdata in c6_cases.items():
        fired: list[str] = []
        mode06 = _as_float(cdata.get("mode06_o2_response_margin_pct"))
        rich_to_lean = _as_float(cdata.get("o2_rich_to_lean_ms"))
        lean_to_rich = _as_float(cdata.get("o2_lean_to_rich_ms"))
        maf_idle = _as_float(cdata.get("maf_actual_calc_delta_pct_idle"))
        maf_2500 = _as_float(cdata.get("maf_actual_calc_delta_pct_2500"))

        if mode06 is not None and mode06 <= MODE06_MARGIN_GATE_PCT:
            fired.append(f"mode06_margin<={MODE06_MARGIN_GATE_PCT:g}%")
        if rich_to_lean is not None and rich_to_lean >= O2_RESPONSE_SLOW_MS:
            fired.append(f"rich_to_lean>={O2_RESPONSE_SLOW_MS:g}ms")
        if lean_to_rich is not None and lean_to_rich >= O2_RESPONSE_SLOW_MS:
            fired.append(f"lean_to_rich>={O2_RESPONSE_SLOW_MS:g}ms")
        if (
            maf_idle is not None
            and maf_2500 is not None
            and maf_idle <= MAF_UNDERREAD_GATE_PCT
            and maf_2500 <= MAF_UNDERREAD_GATE_PCT
        ):
            fired.append(f"maf_delta_both<={MAF_UNDERREAD_GATE_PCT:g}%")
        gates[cid] = " ; ".join(fired) if fired else "(none — abstain/healthy)"
    return gates


def run_diagnose_loop(
    corpus_rows: Sequence[Mapping[str, Any]],
    c6_states: Mapping[str, str],
    rule_map: Mapping[str, str],
    c6_overlay_enabled: bool,
    c3_c6_overlap: set[str] | None = None,
) -> dict[str, dict[str, Any]]:
    """Run all cases through diagnose() with a read-only C6 scoring overlay."""
    original_score_rule = shim._score_rule

    def c6_score_rule(rule: Any, obs: Any) -> float | None:
        cid = CURRENT_CASE_ID[0]

        base_score = original_score_rule(rule, obs)

        if not (c6_overlay_enabled and cid in c6_states):
            return base_score

        c6_state = c6_states[str(cid)]
        c3_state = shim._control_plausibility_state(obs)
        if c3_state is not None and c6_state in DECISIVE_STATES and c3_c6_overlap is not None:
            c3_c6_overlap.add(str(cid))
        if c6_state in DECISIVE_STATES:
            if rule.rule_id in SENSOR_RULES:
                score_to_boost = base_score if base_score is not None else rule.base_weight
                return min(score_to_boost + C6_BOOST, 1.0)
            if rule.rule_id in NO_FAULT_RULES:
                return None
        # SENSOR_HEALTH_UNPROVEN_ABSTAIN: no boost, no NF prune, no C3-prune reversal.

        return base_score

    shim._score_rule = c6_score_rule
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
    """Zero-overlay self-check: reproduce POST_T_V3_P4_C3B/results.json exactly."""
    print(f"Running zero-overlay self-check against {BASELINE_RUN}...")
    if not BASELINE_PATH.is_file():
        print(f"Missing baseline results: {BASELINE_PATH}", file=sys.stderr)
        return False

    baseline_run = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))["results"]
    baseline_by_case = {row["case_id"]: row for row in baseline_run}
    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    simulated = run_diagnose_loop(corpus_rows, {}, rule_map, c6_overlay_enabled=False)

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
    """Re-derive the C6 FT-8 union from sensor_fault.json and no_fault.json passes_cases."""
    rules_dir = WORKSPACE_ROOT / "labs/comlab/registry/rules"
    union: set[str] = set()
    no_fault_union: set[str] = set()
    per_rule: dict[str, list[str]] = {}
    for filename in ("sensor_fault.json", "no_fault.json"):
        data = json.loads((rules_dir / filename).read_text(encoding="utf-8"))
        for rule in data.get("rules", []):
            rule_id = str(rule.get("rule_id", ""))
            passes = list(rule.get("passes_cases", []))
            per_rule[rule_id] = passes
            union.update(passes)
            if rule_id in NO_FAULT_RULES:
                no_fault_union.update(passes)
    return union, per_rule, no_fault_union


def build_scenario_summary(
    corpus_rows: Sequence[Mapping[str, Any]],
    baseline_results: Mapping[str, Mapping[str, Any]],
    sim_results: Mapping[str, Mapping[str, Any]],
    c6_cases: Mapping[str, Mapping[str, Any]],
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

        if cid in c6_cases:
            cdata = c6_cases[cid]
            has_data = any(
                cdata.get(field) is not None
                for field in (
                    "mode06_o2_response_margin_pct",
                    "o2_rich_to_lean_ms",
                    "o2_lean_to_rich_ms",
                    "maf_actual_calc_delta_pct_idle",
                    "maf_actual_calc_delta_pct_2500",
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
    corpus_rows: Sequence[Mapping[str, Any]],
    baseline_results: Mapping[str, Mapping[str, Any]],
    sim_results: Mapping[str, Mapping[str, Any]],
    c6_cases: Mapping[str, Mapping[str, Any]],
    scenario_states: Mapping[str, Mapping[str, str]],
    sub_gates: Mapping[str, str],
) -> list[dict[str, Any]]:
    """Return per-C6-case detail for the full-contract scenario."""
    expected_by_case = {str(row["case_id"]): str(row["expected_family"]) for row in corpus_rows}
    details: list[dict[str, Any]] = []
    for cid in sorted(c6_cases):
        cdata = c6_cases[cid]
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
                reason = "seed stay-abstained: healthy C6 dynamics; PDF-4G-05 banking would be a back-solve alarm"
            elif scenario_states["scenario3_full_contract"][cid] == ABSTAIN_STATE:
                reason = "producer emitted SENSOR_HEALTH_UNPROVEN_ABSTAIN; no C6 boost/prune applied"
            else:
                current_no_fault = base["winner_family"] == "no_fault"
                no_fault_note = " current winner is no_fault;" if current_no_fault else ""
                reason = (
                    f"producer fired {scenario_states['scenario3_full_contract'][cid]};{no_fault_note} "
                    f"+{C6_BOOST} SF boost and NF prune still left expected family outside top-3 "
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
            "c6_state_scenario1": scenario_states["scenario1_mode06_only"][cid],
            "c6_state_scenario2": scenario_states["scenario2_mode06_plus_o2_timing"][cid],
            "c6_state_scenario3": scenario_states["scenario3_full_contract"][cid],
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
    c3_c6_overlap: set[str],
) -> None:
    """Write the essential-first C6 dry-run Markdown report."""
    s1 = summaries["scenario1_mode06_only"]
    s2 = summaries["scenario2_mode06_plus_o2_timing"]
    s3 = summaries["scenario3_full_contract"]
    lines: list[str] = [
        "---",
        "node_type: report",
        "lab: apps/wired",
        "module: v3/c6_signal_sim.py",
        "implements: T-V3-P4-C6A",
        "consumers: [owner acceptance read, next-decision C6B commit sizing]",
        "tags: [v3, phase4, c6, signal, dryrun, synthetic]",
        "source: v3/v3_tasks/T-V3-P4-C6A_c6_signal_dryrun.md",
        "---",
        "",
        "# V3 C6 SIGNAL DRYRUN — Sensor fault under-detection (read-only sim)",
        "",
        "**Task:** [[T-V3-P4-C6A_c6_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)",
        "**Baseline pin:** `POST_T_V3_P4_C3B` / `V3_YARDSTICK_2026-07-05-C3B` "
        "(csv `9f530695…`, oracle `3088a7c3…`, `run_suite.py` untouched)",
        "**C6 Seed:** `v3/data/c6_synthetic_seed_2026-07-05.json` (`synthetic=true`; "
        "13 separable + `PDF-4G-05` stay-abstained)",
        "**Live engine status:** untouched (no corpus / rule / registry / yardstick edit)",
        "",
        "## Headline",
        f"- **Baseline `top3_family`:** {s3['baseline_top3_passes']}/294 → "
        f"**Scenario 3: {s3['simulated_top3_passes']}/294** "
        f"(+{s3['simulated_top3_passes'] - s3['baseline_top3_passes']}).",
        f"- **Yield split (Scenario 3, 14 C6 cases):** {len(s3['would_bank'])} WOULD_BANK / "
        f"{len(s3['already_pass'])} ALREADY_PASS / {len(s3['still_short'])} STILL_SHORT / "
        f"{len(s3['abstain_no_data'])} ABSTAIN_NO_DATA.",
        f"- **Covered-vs-masked at MARGIN=0.02:** {len(s3['would_bank_covered'])} covered / "
        f"{len(s3['would_bank_still_abstained'])} still-abstained among WOULD_BANK.",
        f"- **Scenario ladder WOULD_BANK:** S1 Mode$06={len(s1['would_bank'])}; "
        f"S2 +O2 timing={len(s2['would_bank'])}; S3 +MAF={len(s3['would_bank'])}.",
        f"- **Zero-overlay self-check:** drift = 0 across 294 vs `{BASELINE_RUN}`.",
        f"- **FT-8 regressions:** {s3['regression_count']} full-corpus regressions; "
        f"{len(s3['no_fault_neighbour_regressions'])} no_fault-neighbour regressions.",
        f"- **`PDF-4G-05` back-solve alarm:** banked = "
        f"`{list(banked_stay_abstained) or '(none)'}` — "
        f"{'ALARM' if banked_stay_abstained else 'honoured'}.",
        f"- **C3 precedence assertion:** dual C3+C6 decisive state cases = "
        f"`{sorted(c3_c6_overlap) or '(none)'}`.",
        "",
        "`WOULD_BANK` means the expected family flips into the 3-distinct-family top-3 window. "
        "A flipped case may still be hidden by the abstain dial; that split is disclosed above.",
        "",
        "## 1. Producer simulation (`SensorDynamicsState`)",
        "Per C6-PRE §2: decisive dynamic evidence emits `O2_LAZY_OR_BIASED` or `MAF_UNDERREAD`; "
        "static-only / healthy dynamics emit `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.",
        f"- `O2_LAZY_OR_BIASED`: Mode $06 margin ≤ {MODE06_MARGIN_GATE_PCT:g}% OR "
        f"rich→lean / lean→rich response ≥ {O2_RESPONSE_SLOW_MS:g} ms.",
        f"- `MAF_UNDERREAD`: measured-vs-calculated MAF delta ≤ {MAF_UNDERREAD_GATE_PCT:g}% "
        "at BOTH idle and 2500 rpm; `None` MAF columns make the MAF gate not applicable.",
        "- `SENSOR_HEALTH_UNPROVEN_ABSTAIN`: neither dynamic O2 nor two-point MAF gate fires.",
        "",
        "## 2. Column-subset scenario ladder",
        "| Metric | S1 Mode$06 only | S2 + O2 timing | S3 full (+ MAF) |",
        "| --- | ---: | ---: | ---: |",
        f"| Top-3 family hits | {s1['simulated_top3_passes']}/294 | "
        f"{s2['simulated_top3_passes']}/294 | {s3['simulated_top3_passes']}/294 |",
        f"| WOULD_BANK | **{len(s1['would_bank'])}** | **{len(s2['would_bank'])}** | **{len(s3['would_bank'])}** |",
        f"| Already pass | {len(s1['already_pass'])} | {len(s2['already_pass'])} | {len(s3['already_pass'])} |",
        f"| Still short | {len(s1['still_short'])} | {len(s2['still_short'])} | {len(s3['still_short'])} |",
        f"| Covered WOULD_BANK | {len(s1['would_bank_covered'])} | {len(s2['would_bank_covered'])} | {len(s3['would_bank_covered'])} |",
        f"| Still-abstained WOULD_BANK | {len(s1['would_bank_still_abstained'])} | "
        f"{len(s2['would_bank_still_abstained'])} | {len(s3['would_bank_still_abstained'])} |",
        f"| Regressions | {s1['regression_count']} | {s2['regression_count']} | {s3['regression_count']} |",
        "",
        f"- S2-only banks over S1: `{sorted(set(s2['would_bank']) - set(s1['would_bank'])) or '(none)'}`.",
        f"- S3-only banks over S2: `{sorted(set(s3['would_bank']) - set(s2['would_bank'])) or '(none)'}`.",
        f"- Full S3 bank set: `{s3['would_bank'] or '(none)'}`.",
        "",
        "## 3. Consumer simulation with C3 precedence",
        f"On decisive C6 states (`O2_LAZY_OR_BIASED` / `MAF_UNDERREAD`), the overlay boosts "
        f"{', '.join(SENSOR_RULES)} by +{C6_BOOST} and prunes {', '.join(NO_FAULT_RULES)}. "
        "On `SENSOR_HEALTH_UNPROVEN_ABSTAIN`, it applies no boost and no NF prune.",
        "",
        "C3 precedence is asserted in-sim: live C3 control-reference state and decisive C6 dynamic "
        "state are disjoint today. If any future row carries both, C6B must implement the precedence "
        "inside `integration_shim.py::_score_rule`: C3 prune first; only decisive C6 dynamics may "
        "re-enable/boost SF-001/SF-002; static-only C6 must preserve the C3 prune.",
        "",
        "## 4. Yield disclosure (14 C6 cases, Scenario 3)",
        "| Outcome | Count | Case IDs |",
        "| --- | ---: | --- |",
        f"| **WOULD_BANK** | {len(s3['would_bank'])} | `{', '.join(s3['would_bank']) or '(none)'}` |",
        f"| **ALREADY_PASS** | {len(s3['already_pass'])} | `{', '.join(s3['already_pass']) or '(none)'}` |",
        f"| **STILL_SHORT** | {len(s3['still_short'])} | `{', '.join(s3['still_short']) or '(none)'}` |",
        f"| **ABSTAIN_NO_DATA** | {len(s3['abstain_no_data'])} | `{', '.join(s3['abstain_no_data']) or '(none)'}` |",
        "",
        "### Per-case detail (Scenario 3 full contract)",
        "| Case | Expected | Oracle code | Band | Seed emit | S1 | S2 | S3 | Gate fired | Base hit | Base winner | Sim hit | Sim abst | Winner | Winner fam | Outcome |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for detail in case_details:
        lines.append(
            f"| {detail['case_id']} | {detail['expected_family']} | {detail['oracle_fault_code']} | "
            f"{detail['band_id']} | {detail['emit_path_seed']} | `{detail['c6_state_scenario1']}` | "
            f"`{detail['c6_state_scenario2']}` | `{detail['c6_state_scenario3']}` | "
            f"{detail['sub_gate_fired']} | {detail['baseline_hit']} | "
            f"{detail['baseline_winner_id']}/{detail['baseline_winner_family']} | {detail['top3_hit']} | "
            f"{detail['abstained']} | {detail['winner_id']} | {detail['winner_family']} | **{detail['outcome']}** |"
        )
    lines.extend([
        "",
        "### Why each STILL_SHORT case fell short",
    ])
    for detail in case_details:
        if detail["outcome"] == "STILL_SHORT":
            lines.append(f"- `{detail['case_id']}` ({detail['band_id']}): {detail['still_short_reason']}")
    lines.extend([
        "",
        "## 5. FT-8 neighbour audit",
        f"Neighbour union re-derived live from `sensor_fault.json` + `no_fault.json` `passes_cases`: **{len(ft8_union)}** cases.",
        f"- Dual target+neighbour: **{len(dual_target_and_neighbour)}** — `{list(dual_target_and_neighbour)}`.",
        f"- Full-corpus regressions (Scenario 3): **{s3['regression_count']}** — `{s3['regressions'] or '(empty)'}`.",
        f"- FT-8 neighbour regressions: `{s3['ft8_neighbour_regressions'] or '(empty)'}`.",
        f"- no_fault rule neighbours ({len(no_fault_neighbours)}): `{sorted(no_fault_neighbours)}`.",
        f"- no_fault neighbours currently passing at baseline: `{s3['no_fault_currently_passing_neighbours'] or '(empty)'}`.",
        f"- no_fault-neighbour regressions: `{s3['no_fault_neighbour_regressions'] or '(empty)'}`.",
        f"- Healthy no_fault cases regressed to a fault winner: `{s3['healthy_no_fault_to_fault_winner'] or '(empty)'}`.",
        "",
        "Per-rule live `passes_cases` counts:",
        "",
        "| Rule | Count |",
        "| --- | ---: |",
    ])
    for rule_id in sorted(ft8_per_rule):
        lines.append(f"| {rule_id} | {len(ft8_per_rule[rule_id])} |")
    lines.extend([
        "",
        "## 6. Commit scope for `T-V3-P4-C6B` (sized, not guessed)",
        f"- **Producer gates simulated:** Mode $06 margin ≤ {MODE06_MARGIN_GATE_PCT:g}%; "
        f"O2 response ≥ {O2_RESPONSE_SLOW_MS:g} ms; two-point MAF delta ≤ {MAF_UNDERREAD_GATE_PCT:g}% at both points.",
        f"- **Consumer deltas simulated:** boost {', '.join(SENSOR_RULES)} by +{C6_BOOST}; "
        f"prune {', '.join(NO_FAULT_RULES)} only on decisive dynamic C6 evidence; abstain state is no-op.",
        "- **Column-set pricing:**",
        f"  - Scenario 1 banked {len(s1['would_bank'])}; Scenario 2 banked {len(s2['would_bank'])}; Scenario 3 banked {len(s3['would_bank'])}.",
        f"  - MAF columns are load-bearing for: `{sorted(set(s3['would_bank']) - set(s2['would_bank'])) or '(none)'}`.",
        "  - If C6B wants the MAF-underread row, it needs the six MAF/airflow columns; otherwise Mode $06 + O2 timing carries the O2-lazy rows.",
        "- **Precedence implementation point:** `integration_shim.py::_score_rule`, after the live C3 branch has computed/pruned and before any C6 SF/NF overlay returns a score.",
        "",
        "> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 228/294 until C6B commits real/accepted columns and mints a new yardstick.",
    ])
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote Markdown report to {md_path}")


def main() -> int:
    """CLI entry point for the C6 dry-run simulator."""
    parser = argparse.ArgumentParser(description="C6 Signal Pack Simulator (read-only dry-run).")
    parser.add_argument("--self-check", action="store_true", help="Run zero-overlay self-check only.")
    parser.add_argument("--c6-seed", type=Path, default=DEFAULT_SEED, help="C6 synthetic or owner seed JSON.")
    parser.add_argument("--write", type=Path, default=DEFAULT_REPORT_JSON, help="Write JSON report here.")
    args = parser.parse_args()

    if not run_self_check():
        return 1
    if args.self_check:
        return 0
    if not args.c6_seed.is_file():
        print(f"Missing C6 seed file: {args.c6_seed}", file=sys.stderr)
        return 1

    seed = json.loads(args.c6_seed.read_text(encoding="utf-8"))
    c6_cases: dict[str, dict[str, Any]] = seed.get("cases", {})
    scenario_states = compute_c6_states(c6_cases)
    sub_gates = compute_c6_sub_gates(c6_cases)

    corpus_rows = build_corpus_rows()
    rule_map = load_rule_family_map()
    print("Running baseline and C6 scenario diagnostics...")
    baseline_results = run_diagnose_loop(corpus_rows, {}, rule_map, c6_overlay_enabled=False)

    ft8_union, ft8_per_rule, no_fault_neighbours = derive_ft8_neighbour_union()
    summaries: dict[str, dict[str, Any]] = {}
    scenario_results: dict[str, dict[str, dict[str, Any]]] = {}
    c3_c6_overlap: set[str] = set()
    for scenario_name, states in scenario_states.items():
        overlap_for_scenario: set[str] = set()
        sim_results = run_diagnose_loop(
            corpus_rows,
            states,
            rule_map,
            c6_overlay_enabled=True,
            c3_c6_overlap=overlap_for_scenario,
        )
        if overlap_for_scenario:
            c3_c6_overlap.update(overlap_for_scenario)
        scenario_results[scenario_name] = sim_results
        summaries[scenario_name] = build_scenario_summary(
            corpus_rows, baseline_results, sim_results, c6_cases, ft8_union, no_fault_neighbours
        )

    if c3_c6_overlap:
        print(f"C3/C6 precedence assertion FAILED: overlap={sorted(c3_c6_overlap)}", file=sys.stderr)
        return 1

    full_results = scenario_results["scenario3_full_contract"]
    case_details = build_case_details(corpus_rows, baseline_results, full_results, c6_cases, scenario_states, sub_gates)
    dual_target_and_neighbour = sorted(set(c6_cases) & ft8_union)
    banked_stay_abstained = sorted(
        detail["case_id"]
        for detail in case_details
        if detail["stay_abstained_seed"] and detail["outcome"] == "WOULD_BANK"
    )

    s3 = summaries["scenario3_full_contract"]
    print("\n" + "=" * 72)
    print("C6 SIGNAL DRYRUN SUMMARY (Scenario 3: full contract)")
    print("=" * 72)
    print(f"Baseline pin: {BASELINE_RUN}")
    print(f"Baseline top3: {s3['baseline_top3_passes']}/294")
    print(f"Simulated top3: {s3['simulated_top3_passes']}/294")
    print(
        "Scenario WOULD_BANK: "
        f"S1={summaries['scenario1_mode06_only']['newly_passing_count']} / "
        f"S2={summaries['scenario2_mode06_plus_o2_timing']['newly_passing_count']} / "
        f"S3={s3['newly_passing_count']}"
    )
    print(f"Yield: WOULD_BANK={len(s3['would_bank'])}, ALREADY_PASS={len(s3['already_pass'])}, STILL_SHORT={len(s3['still_short'])}")
    print(f"Regressions: {s3['regression_count']} -> {s3['regressions']}")
    print(f"no_fault neighbour regressions: {s3['no_fault_neighbour_regressions']}")
    print(f"FT-8 neighbour union: {len(ft8_union)} ; dual target+neighbour: {len(dual_target_and_neighbour)}")
    print(f"PDF-4G-05 banked (ALARM if non-empty): {banked_stay_abstained}")
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
        "task": "T-V3-P4-C6A",
        "mode": "provisional-synthetic-simulated (side file; live corpus untouched)",
        "baseline_run": BASELINE_RUN,
        "yardstick": "V3_YARDSTICK_2026-07-05-C3B",
        "seed": str(args.c6_seed.relative_to(WORKSPACE_ROOT)),
        "producer_gates": {
            "mode06_o2_response_margin_pct": f"<= {MODE06_MARGIN_GATE_PCT:g}",
            "o2_response_ms": f">= {O2_RESPONSE_SLOW_MS:g}",
            "maf_actual_calc_delta_pct_both_points": f"<= {MAF_UNDERREAD_GATE_PCT:g}",
        },
        "consumer_overlay": {
            "sensor_rules_boosted": list(SENSOR_RULES),
            "no_fault_rules_pruned_on_decisive_dynamic_evidence": list(NO_FAULT_RULES),
            "boost": C6_BOOST,
            "abstain_state_noop": ABSTAIN_STATE,
        },
        "c3_c6_decisive_overlap_assertion": sorted(c3_c6_overlap),
        "ft8_neighbour_union": sorted(ft8_union),
        "ft8_neighbour_count": len(ft8_union),
        "ft8_per_rule": ft8_per_rule,
        "no_fault_rule_neighbours": sorted(no_fault_neighbours),
        "dual_target_and_neighbour": dual_target_and_neighbour,
        "banked_stay_abstained_ALARM": banked_stay_abstained,
        "scenarios": {
            "scenario1_mode06_only": {
                "description": "Mode $06 O2 response margin only (cheapest Tier-a scan read).",
                "summary": summaries["scenario1_mode06_only"],
            },
            "scenario2_mode06_plus_o2_timing": {
                "description": "Mode $06 plus active rich->lean / lean->rich O2 response timing.",
                "summary": summaries["scenario2_mode06_plus_o2_timing"],
            },
            "scenario3_full_contract": {
                "description": "Full C6 contract: O2 dynamics plus two-point MAF actual-vs-calculated airflow.",
                "summary": summaries["scenario3_full_contract"],
                "case_details": case_details,
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
        c3_c6_overlap,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
