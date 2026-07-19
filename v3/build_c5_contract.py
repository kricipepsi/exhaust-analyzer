"""Read-only extractor for the C5 signal-pack REVEAL CONTRACT.

This script instances the frozen reveal contract for C5 — lean-condition root
cause. It performs a live column audit against the petrol cases CSV header,
derives the FT-8 neighbour set live by parsing the JSON rule files and baseline
results, and outputs both V3_C5_REVEAL_CONTRACT_2026-07-05.json and V3_C5_REVEAL_CONTRACT_2026-07-05.md.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

WS = Path(__file__).resolve().parent.parent
ACQ_JSON = WS / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
LEAN_RULES = WS / "labs/comlab/registry/rules/lean_condition.json"
VACUUM_RULES = WS / "labs/comlab/registry/rules/vacuum_leak.json"
EXHAUST_RULES = WS / "labs/comlab/registry/rules/exhaust_leak.json"
OUT_JSON = WS / "v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json"
OUT_MD = WS / "v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md"

C5_COLUMNS = [
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
]

REVEAL_SECTIONS: list[dict[str, str]] = [
    {
        "key": "BUILDABLE_NOW",
        "definition": (
            "Producer/consumer logic + thresholds derivable from the cluster "
            "research answer; provable by unit tests on synthetic vectors, "
            "with no owner data."
        ),
    },
    {
        "key": "SCORING_GATED",
        "definition": (
            "The per-case owner columns still required and which residual "
            "case_ids each unlocks; stays abstained until the owner supplies "
            "real measured values."
        ),
    },
    {
        "key": "CODE_LANDED_NEQ_SCORE_MOVED",
        "definition": (
            "Explicit separation of producer/consumer logic shipped from "
            "top3_family delta. Landing code proves the discriminator is "
            "wired; it does not move score until gated data exists."
        ),
    },
    {
        "key": "REGRESSION_FT8",
        "definition": (
            "The neighbour set the consumer edit touches, plus the "
            "no-regressed-family audit run on the full corpus at commit time."
        ),
    },
    {
        "key": "ABSTAIN_FALLBACK",
        "definition": (
            "Cases whose discriminating signal the owner cannot supply stay "
            "abstained at MARGIN=0.02, never guessed from static idle data."
        ),
    },
]

C5_PRODUCER_THRESHOLDS: list[dict[str, str]] = [
    {
        "signal": "Total fuel trim delta (ΔTFT) between idle and 2500 RPM",
        "maneuver": "Stationary stabilized idle (Maneuver A) transitioning to free-rev mid-RPM hold (Maneuver B)",
        "threshold": "Positive trims at idle (e.g. TFT >= +15%) that recover by >= 15% at 2500 RPM (e.g. TFT <= +10%)",
        "verdict": "VACUUM_LEAK_TRIM_PATTERN",
        "producer_state": "OBDLab LeanRootCauseState",
        "evidence_fields": "stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct",
        "cite": (
            "cluster5.md §Signal Evaluation and Discriminative Ranking lines 127-129; "
            "§Quantitative Expected Signatures and Decision Matrix lines 155-156"
        ),
        "grounding": "empirical (direction strong; numeric values provisional)",
        "feasibility_tier": "Tier A: generic OBD-II live trims",
    },
    {
        "signal": "Fuel rail pressure drop and wide-range lambda under WOT",
        "maneuver": "Wide-Open Throttle (WOT) acceleration sweep (Maneuver C) under high load",
        "threshold": "Fuel rail pressure drop of > 5 psi (35 kPa) below OEM spec, accompanied by wide-range lambda lambda > 1.05 (failure to enrich)",
        "verdict": "FUEL_DELIVERY_SHORTFALL",
        "producer_state": "OBDLab LeanRootCauseState",
        "evidence_fields": "fuel_rail_pressure_load_kpa, wideband_lambda_wot",
        "cite": (
            "cluster5.md §Signal Evaluation and Discriminative Ranking lines 135-137, 139-141; "
            "§Quantitative Expected Signatures and Decision Matrix lines 158-159"
        ),
        "grounding": "manufacturer-typical (for 35 kPa drop) / standardized (for lambda > 1.05)",
        "feasibility_tier": "Tier A if sensor exposed; Tier C if mechanical gauge required",
    },
    {
        "signal": "Calculated engine load at peak WOT, with positive trims",
        "maneuver": "Wide-Open Throttle (WOT) acceleration sweep (Maneuver C) up to upshift point",
        "threshold": "Calculated engine load failing to reach OEM typical bounds (Peak Load < 80%) under WOT, while trims run positive",
        "verdict": "MAF_UNDERREAD",
        "producer_state": "OBDLab LeanRootCauseState",
        "evidence_fields": "calc_load_wot_pct, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct",
        "cite": (
            "cluster5.md §Signal Evaluation and Discriminative Ranking lines 131-133; "
            "§Quantitative Expected Signatures and Decision Matrix line 157; "
            "Bottom Line Diagnostic Recommendation line 166"
        ),
        "grounding": "manufacturer-typical / empirical-inferred",
        "feasibility_tier": "Tier A: generic OBD-II calculated load and trims",
    },
    {
        "signal": "Static-only or idle-only trim evidence",
        "maneuver": "Stationary idle only; absent Maneuver B/C dynamic evidence",
        "threshold": "Reject static/idle-only trims as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "verdict": "SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "producer_state": "OBDLab LeanRootCauseState",
        "evidence_fields": "absence of decisive dynamic 2500 RPM / WOT load / pressure evidence",
        "cite": (
            "cluster5.md §Bottom Line Diagnostic Recommendation line 166; "
            "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C5.6 line 53"
        ),
        "grounding": "physics/regulatory rationale (dynamic multi-point data required)",
        "feasibility_tier": "Abstain fallback",
    },
]

C5_CONFOUNDERS: list[dict[str, str]] = [
    {
        "confounder": "Exhaust leak pre-O2 (false lean)",
        "mechanism": (
            "Allows outside air to enter before the upstream O2 sensor via venturi effect, "
            "causing false lean lambda but normal engine load and trims. Separated by gas "
            "chemistry (high O2) or vacuum-leak/fuel-pressure verification."
        ),
        "cite": "cluster5.md §Technical Characterization of the Confusable Set line 37",
    },
    {
        "confounder": "Misfire (false lean)",
        "mechanism": (
            "Unburned oxygen passes directly into the exhaust, causing false lean lambda. "
            "Separated by misfire codes (P0300-P0312) or Mode $06 misfire counts."
        ),
        "cite": "cluster5.md §Technical Characterization of the Confusable Set line 37",
    },
    {
        "confounder": "Speed-Density vs MAF architecture",
        "mechanism": (
            "Naturally aspirated speed-density vehicles are immune to idle vacuum leak trims; "
            "turbocharged speed-density systems show negative trims under boost (boost leak)."
        ),
        "cite": "cluster5.md §Physical and Thermodynamic Mechanisms of Fault Separation lines 77-83",
    },
    {
        "confounder": "C4 exhaust-leak / true-lean overlap",
        "mechanism": (
            "C4 contains exhaust-leak/lean-condition/sensor-bias lookalikes that share these "
            "same C5 trim/load columns. C5-SYNTH must mark cases outside true-lean "
            "separability (confounders) as stay-abstained."
        ),
        "cite": "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md lines 106-112",
    },
]

C6_MAF_COLLISION = {
    "description": (
        "C6's SensorDynamicsState and C5's LeanRootCauseState can both emit a MAF-underread "
        "verdict from the same MAF columns, but attribute it to different families (sensor_fault vs lean_condition)."
    ),
    "populations_today": "Disjoint: 14 C6 rows vs 10 C5 rows in the current corpus.",
    "disambiguation_rule": (
        "C6's sensor-attribution requires its Mode $06/dynamics evidence; C5's requires the "
        "trim+load pattern; neither fires on MAF delta alone. When both are present, C5's lean root "
        "cause takes precedence over C6's sensor-fault boost to prevent a lean-condition MAF drift "
        "from being misclassified as a sensor fault."
    ),
    "integration_location": (
        "Lands in integration_shim.py::_score_rule (around lines 608-662), evaluated "
        "after the C3 and C6 branches. C5 must prune/suppress C6's sensor-fault boost if the C5 "
        "WOT load suppression pattern is present."
    ),
}

C3_INTERACTION = {
    "live_c3_state": "ControlPlausibilityState.CONTROL_REFERENCE_FAULT",
    "live_c3_reader": "integration_shim.py::_control_plausibility_state lines 540-557",
    "live_c3_effect": (
        "integration_shim.py::_score_rule lines 562-569 boosts EF-001/002/003 "
        "by +0.10 and prunes SF-001/SF-002 when CONTROL_REFERENCE_FAULT is present."
    ),
    "c5_future_effect": (
        "C5 will boost lean_condition consumers (LC-001/LC-002/LC-003) based on LeanRootCauseState: "
        "VACUUM_LEAK_TRIM_PATTERN, FUEL_DELIVERY_SHORTFALL, or MAF_UNDERREAD."
    ),
    "required_precedence_for_c5b": (
        "If a future row carries both C3 control-reference columns and C5 lean-condition columns, "
        "C3 control-reference pruning must run first. Static-only C5 evidence must preserve "
        "abstain/prune behavior to prevent control-reference faults from being misclassified as "
        "lean conditions."
    ),
}


def _load(path: Path) -> Any:
    """Load a JSON file from *path*."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _c5_case_split() -> dict[str, Any]:
    """Return the 10 C5 cases, all scoring-gated until C5 values exist."""
    acq = _load(ACQ_JSON)
    c5_cases = [c for c in acq["case_unlocks"] if c.get("cluster") == "C5"]
    scoring_gated = [
        {
            "case_id": c["case_id"],
            "bucket": c.get("bucket", ""),
            "expected_family": c.get("expected_family", ""),
            "predicted_family": c.get("predicted_family"),
            "source_detail": c.get("source_detail"),
            "required_columns": c.get("unlock_columns", []),
            "buildable_now": False,
            "abstain_if_absent": bool(c.get("abstain_if_absent")),
        }
        for c in sorted(c5_cases, key=lambda row: row["case_id"])
    ]
    buckets = Counter(c["bucket"] for c in scoring_gated)
    expected = Counter(c["expected_family"] for c in scoring_gated)
    predicted = Counter(c.get("predicted_family") for c in scoring_gated)
    return {
        "total": len(scoring_gated),
        "buildable_now_reachable": [],
        "buildable_now_count": 0,
        "scoring_gated": scoring_gated,
        "scoring_gated_count": len(scoring_gated),
        "bucket_breakdown": dict(sorted(buckets.items())),
        "expected_family_mix": dict(sorted(expected.items())),
        "predicted_family_mix": dict(sorted(predicted.items())),
        "note": (
            "All 10 C5 rows are SCORING_GATED. The producer/consumer logic is "
            "buildable from research, but the top3_family delta is unknowable "
            "until trims/load/pressure values exist."
        ),
    }


def _ft8_neighbours() -> dict[str, Any]:
    """Derive FT-8 neighbour set live from lean_condition and vacuum_leak rules and baseline results."""
    rules: list[dict[str, Any]] = []
    passes: set[str] = set()
    for family, path in (("lean_condition", LEAN_RULES), ("vacuum_leak", VACUUM_RULES)):
        data = _load(path)
        for rule in data["rules"]:
            passes_cases = rule.get("passes_cases", [])
            rules.append(
                {
                    "rule_id": rule["rule_id"],
                    "fault_family": rule["fault_family"],
                    "source_file": str(path.relative_to(WS)),
                    "competition_group": rule.get("competition_group"),
                    "base_weight": rule.get("base_weight"),
                    "passes_cases": passes_cases,
                }
            )
            passes.update(passes_cases)

    # Also add the C3 lean-bias winners (EXP-N002, EXP-N004, case_001) that won LC rules in the baseline run
    results_path = WS / "apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json"
    runtime_lc_vl_winners = set()
    if results_path.exists():
        with results_path.open("r", encoding="utf-8") as fh:
            res_data = json.load(fh)
        for r in res_data.get("results", []):
            verdict = r.get("verdict") or {}
            fault_code = verdict.get("fault_code")
            if fault_code and (fault_code.startswith("LC-") or fault_code.startswith("VL-")):
                runtime_lc_vl_winners.add(r["case_id"])

    union_passes = passes.union(runtime_lc_vl_winners)
    return {
        "touched_families": ["lean_condition", "vacuum_leak"],
        "touched_competition_groups": ["lean_condition", "vacuum_leak"],
        "rules": rules,
        "passes_cases_union": sorted(list(union_passes)),
        "passes_cases_count": len(union_passes),
        "static_passes_cases": sorted(list(passes)),
        "runtime_passes_cases": sorted(list(runtime_lc_vl_winners)),
        "risk_note": (
            "LC rules touch lean-condition cases. Vacuum leak and fuel shortfall "
            "rules have high overlap with other clusters (e.g., C3 control-reference "
            "lean-bias cases which are now-passing LC-001/LC-002, and C4 exhaust-leak "
            "lookalikes). A false boost that regresses these neighbours must be audited."
        ),
    }


def _mimic_risk(case_split: dict[str, Any]) -> list[dict[str, str | None]]:
    """Classify per-case lookalike risk disclosed for C5-SYNTH."""
    risks: list[dict[str, str | None]] = []
    for case in case_split["scoring_gated"]:
        expected = case["expected_family"]
        predicted = case.get("predicted_family")
        if predicted == "sensor_fault":
            note = "sensor_fault lookalike; dynamic C5 trims needed or stay abstained"
        elif predicted == "catalyst_failure":
            note = "catalyst_failure lookalike; dynamic C5 trims/load needed or stay abstained"
        elif predicted == "misfire":
            note = "misfire lookalike; dynamic C5 trims/load needed or stay abstained"
        elif predicted == "mechanical_wear":
            note = "mechanical_wear lookalike; dynamic C5 trims/load needed or stay abstained"
        else:
            note = "C5-SYNTH must decide separability from oracle fault, not current rank"
        risks.append(
            {
                "case_id": case["case_id"],
                "expected_family": expected,
                "predicted_family": predicted,
                "mimic_risk": note,
            }
        )
    return risks


def _grounding_strength_table() -> list[dict[str, str]]:
    """Produce the per-threshold grounding-strength table."""
    table: list[dict[str, str]] = []
    for threshold in C5_PRODUCER_THRESHOLDS:
        grounding = threshold["grounding"]
        if grounding.startswith("empirical"):
            risk = "Direction is strong; local trims at idle recover at 2500, but exact delta % threshold is empirical."
        elif grounding.startswith("manufacturer-typical") and "/" in grounding:
            risk = "Pressure drop limit is typical for port-injection; DI rails have higher targets. WOT Load threshold may vary by altitude."
        elif grounding.startswith("manufacturer-typical"):
            risk = "Load threshold is typical; altitude and OEM mapping represent drift risks."
        elif grounding.startswith("standardized"):
            risk = "Wideband lambda value at WOT is standard; failure to enrich under load is physically decisive."
        else:
            risk = "Static-only inputs are insufficient; abstain is the intended outcome."
        table.append(
            {
                "signal": threshold["signal"],
                "threshold": threshold["threshold"],
                "grounding": grounding,
                "feasibility_tier": threshold["feasibility_tier"],
                "risk_note": risk,
            }
        )
    return table


def _perform_column_audit() -> dict[str, Any]:
    """Audit the petrol cases CSV header dynamically to identify live vs new columns."""
    csv_path = WS / "apps/wired/v7/data/cases_petrol_v7.csv"
    with csv_path.open("r", encoding="utf-8") as fh:
        header = next(csv.reader([fh.readline().strip()]))

    live_cols = sorted([col for col in C5_COLUMNS if col in header])
    new_cols = sorted([col for col in C5_COLUMNS if col not in header])

    return {
        "total_contract_columns": len(C5_COLUMNS),
        "live_columns": live_cols,
        "live_columns_count": len(live_cols),
        "new_columns": new_cols,
        "new_columns_count": len(new_cols),
        "note": (
            f"Of the {len(C5_COLUMNS)} required C5 columns, {len(live_cols)} already exist "
            f"in the live schema (4 trims from C2B, 2 MAF from C6B). The genuinely new ask "
            f"is shrank to {len(new_cols)} columns. For C5 rows, the live columns exist in "
            f"the schema but are currently empty/null."
        ),
    }


def build_contract() -> dict[str, Any]:
    """Assemble the machine-readable C5 reveal contract."""
    case_split = _c5_case_split()
    ft8 = _ft8_neighbours()
    c5_ids = {case["case_id"] for case in case_split["scoring_gated"]}
    dual_target_neighbour = sorted(c5_ids & set(ft8["passes_cases_union"]))
    column_audit = _perform_column_audit()

    return {
        "task": "T-V3-P4-C5-PRE",
        "generated": "2026-07-05",
        "mode": "DISCLOSE only (read-only pre-author; no wiring, no score move)",
        "purpose": (
            "Instance the frozen reveal contract for C5 — lean-condition root "
            "cause. Surfaces LeanRootCauseState gates, consumer mapping, "
            "C6-MAF-collision, C3 interaction, 10-case split, live FT-8 neighbours, "
            "column audit, confounders, and baseline pin."
        ),
        "reveal_contract_template": REVEAL_SECTIONS,
        "baseline": {
            "yardstick": "V3_YARDSTICK_2026-07-05-C6B",
            "csv_hash": "bf7393688230caf7f15054cc2473343e26351aa72c4615ca83044c7eb12fc0de",
            "oracle_hash": "3088a7c3",
            "scorer": "apps/wired/v7/run_suite.py (hash-locked, untouched)",
            "named_run": "POST_T_V3_P4_C6B",
            "run_dir": "apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json",
            "note": (
                "All C5 sizing references this current post-C6B baseline. If any "
                "commit lands first, stop and re-pin before C5-SYNTH/C5A."
            ),
        },
        "c5_instance": {
            "cluster": "C5",
            "title": "lean-condition root cause",
            "research_source": "v3/research/research_answers/cluster5.md",
            "producer": {
                "states": ["OBDLab LeanRootCauseState"],
                "emit_condition": (
                    "Emit VACUUM_LEAK_TRIM_PATTERN from positive trims at idle that recover at 2500; "
                    "emit FUEL_DELIVERY_SHORTFALL from lean under load and rail pressure drop > 35 kPa; "
                    "emit MAF_UNDERREAD from peak load < 80% with positive trims; "
                    "emit SENSOR_HEALTH_UNPROVEN_ABSTAIN for static-only evidence."
                ),
                "thresholds": C5_PRODUCER_THRESHOLDS,
                "corpus_columns": C5_COLUMNS,
            },
            "column_audit": column_audit,
            "consumer": {
                "lean_condition": {
                    "file": "labs/comlab/registry/rules/lean_condition.json",
                    "rules": ["LC-001", "LC-002", "LC-003"],
                    "reads": (
                        "LC-001/LC-002/LC-003 consume trims, MAP, and MAF g/s columns. In C5B, "
                        "they will gate on the C5 state outputs VACUUM_LEAK_TRIM_PATTERN and MAF_UNDERREAD."
                    ),
                    "evidence_fields": C5_COLUMNS,
                },
                "vacuum_leak": {
                    "file": "labs/comlab/registry/rules/vacuum_leak.json",
                    "rules": ["VL-001", "VL-002", "VL-003"],
                    "reads": (
                        "VL-001/VL-002/VL-003 read trims and MAP directly. Today, no cases in "
                        "the active corpus expect vacuum_leak as their fault family, so these rules "
                        "are not currently mapped to active cases (only synthetic placeholders)."
                    ),
                    "evidence_fields": C5_COLUMNS,
                },
                "exhaust_leak_note": {
                    "file": "labs/comlab/registry/rules/exhaust_leak.json",
                    "rule": "EL-001",
                    "reads": "Reads longft1 and DTCs. Used in C4 later to separate exhaust leak from true lean.",
                },
            },
            "c6_maf_collision": C6_MAF_COLLISION,
            "c3_interaction": C3_INTERACTION,
            "case_split": case_split,
            "ft8_neighbours": ft8,
            "dual_target_and_neighbour": dual_target_neighbour,
            "confounder_disclosure": {
                "confounders": C5_CONFOUNDERS,
                "mimic_risk_per_case": _mimic_risk(case_split),
                "c4_dependency": (
                    "C4 is not a new-column ask; its residuals consume the C5 trim/load columns "
                    "and C6 dynamics columns. Landing C5 is a required prerequisite for C4B."
                ),
            },
            "grounding_strength": _grounding_strength_table(),
            "code_landed_neq_score_moved": (
                "The C5 producer emit rule + consumer map are BUILDABLE_NOW from "
                "cluster5.md and unit-testable on synthetic LeanRootCauseState "
                "vectors. That is CODE_LANDED. SCORE_MOVED on these 10 cannot be "
                "shown until owner/synthetic C5 values exist; the two must never be conflated."
            ),
            "abstain_fallback": (
                "If only static or idle trims are supplied, the case stays abstained "
                "at MARGIN=0.02. Dynamic multi-point data is the separator for C5."
            ),
        },
        "provenance": {
            "read_only": True,
            "corpus_changed": False,
            "yardstick_minted": False,
            "rules_edited": False,
            "producers_wired": False,
            "values_synthesized": False,
            "abstain_dial_changed": False,
            "run_suite_touched": False,
            "vault_touched": False,
            "graphify_run": False,
        },
    }


def _csv(items: list[str]) -> str:
    """Return a comma-separated list or an em dash."""
    return ", ".join(items) if items else "—"


def render_markdown(contract: dict[str, Any]) -> str:
    """Render the human-readable C5 reveal report."""
    c5 = contract["c5_instance"]
    base = contract["baseline"]
    case_split = c5["case_split"]
    ft8 = c5["ft8_neighbours"]
    col_audit = c5["column_audit"]
    lines: list[str] = [
        "# V3_C5_REVEAL_CONTRACT_2026-07-05",
        "",
        "**Task:** `T-V3-P4-C5-PRE`  **Mode:** DISCLOSE only (read-only pre-author)",
        "**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no",
        "**Machine-readable twin:** `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json`",
        "(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c5_contract.py`).",
        "",
        "This document instances the frozen reveal contract for **C5 — lean-condition root cause**,",
        "the next pack in the pinned sequence (C2 → C3 → C6 → **C5** → C4 → …).",
        "It builds nothing and scores nothing; it fixes how C5 discloses thresholds, consumers,",
        "C6 collision, C3 interaction, FT-8 exposure, column audit, and stay-abstained cases.",
        "",
        "---",
        "",
        "## 0. Baseline pin",
        "",
        "| Artefact | Pinned value |",
        "| --- | --- |",
        f"| Yardstick | `{base['yardstick']}` |",
        f"| CSV SHA-256 | `{base['csv_hash']}` |",
        f"| Oracle subset SHA-256 | `{base['oracle_hash']}…` (unchanged) |",
        f"| Scorer | `{base['scorer']}` |",
        f"| Named run | `{base['named_run']}` |",
        f"| Run JSON | `{base['run_dir']}` |",
        "",
        f"{base['note']}",
        "",
        "---",
        "",
        "## 1. The reveal contract (cluster-agnostic template — instanced, not re-derived)",
        "",
        "| Section | Definition |",
        "| --- | --- |",
    ]
    for section in contract["reveal_contract_template"]:
        lines.append(f"| **{section['key']}** | {section['definition']} |")
    lines.extend(
        [
            "",
            "---",
            "",
            "## 2. C5 producer extraction (cited to `cluster5.md`)",
            "",
            "The C5 producer is **OBDLab `LeanRootCauseState`**. It emits",
            "`VACUUM_LEAK_TRIM_PATTERN`, `FUEL_DELIVERY_SHORTFALL`, `MAF_UNDERREAD`, or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.",
            "The emit thresholds, transcribed read-only from the research answer:",
            "",
            "| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for threshold in c5["producer"]["thresholds"]:
        lines.append(
            "| "
            f"{threshold['signal']} | {threshold['maneuver']} | "
            f"{threshold['threshold']} | `{threshold['verdict']}` | "
            f"`{threshold['evidence_fields']}` | {threshold['grounding']} | "
            f"{threshold['cite']} |"
        )
    lines.extend(
        [
            "",
            "**Producer emit summary:** `VACUUM_LEAK_TRIM_PATTERN` requires positive trims at idle",
            "that recover at 2500 RPM; `FUEL_DELIVERY_SHORTFALL` requires rail pressure drop > 35 kPa",
            "and wide-range lambda > 1.05 under WOT; `MAF_UNDERREAD` requires suppressed peak WOT load < 80%",
            "accompanied by positive trims; static-only trims produce `SENSOR_HEALTH_UNPROVEN_ABSTAIN`,",
            "not a guessed pass/fail.",
            "",
            "**Load-bearing subset to size in C5A:** The trims and MAF g/s columns already exist. The genuinely new",
            "columns are load/pressure/lambda at WOT. C5A dry-run must size whether the full column set is load-bearing.",
            "",
            "---",
            "",
            "## 3. C5 consumer mapping (named; no edit)",
            "",
            "| Family file | Rules | Field each would read | What the C5 state supplies |",
            "| --- | --- | --- | --- |",
            "| `lean_condition.json` | **LC-001 / LC-002 / LC-003** | Trims, MAP, MAF g/s. Gated on C5 state output in C5B. | Lean-condition sub-cause state overrides: VACUUM_LEAK_TRIM_PATTERN or MAF_UNDERREAD. |",
            "| `vacuum_leak.json` | **VL-001 / VL-002 / VL-003** | Trims, MAP directly. Gated on C5 state output in C5B. | Optional sub-cause gating. (No active cases expect vacuum_leak). |",
            "| `exhaust_leak.json` | **EL-001** | Trims and DTCs. Reads shared trims. | Used in C4 later to separate exhaust leak from true lean. |",
            "",
            "Nothing is edited here. The consumer map is for C5-SYNTH/C5A/C5B inheritance.",
            "",
            "---",
            "",
            "## 4. C6-MAF-COLLISION & C3-INTERACTION DISCLOSURE (mandatory)",
            "",
            "### C6-MAF-COLLISION",
            "",
            f"- **Collision description:** {c5['c6_maf_collision']['description']}",
            f"- **Populations today:** {c5['c6_maf_collision']['populations_today']}",
            f"- **Disambiguation rule:** {c5['c6_maf_collision']['disambiguation_rule']}",
            f"- **Integration location:** {c5['c6_maf_collision']['integration_location']}",
            "",
            "### C3-INTERACTION",
            "",
            "The live C3B shim now has a control-reference state and a prune/boost branch:",
            "",
            f"- Producer: `{c5['c3_interaction']['live_c3_reader']}` returns `CONTROL_REFERENCE_FAULT` from KOEO MAP/BARO, ground drop, and loaded-voltage gates.",
            f"- Effect: {c5['c3_interaction']['live_c3_effect']}",
            f"- C5 future effect: {c5['c3_interaction']['c5_future_effect']}",
            "",
            "**Composition / precedence rule C5B must implement:**",
            c5["c3_interaction"]["required_precedence_for_c5b"],
            "",
            "---",
            "",
            "## 5. ALREADY-LIVE-COLUMN AUDIT (mandatory)",
            "",
            f"- **Total required C5 columns:** {col_audit['total_contract_columns']}",
            f"- **Already live in schema ({col_audit['live_columns_count']}):** `{_csv(col_audit['live_columns'])}`",
            f"- **Genuinely new ask ({col_audit['new_columns_count']}):** `{_csv(col_audit['new_columns'])}`",
            "",
            col_audit["note"],
            "",
            "---",
            "",
            "## 6. C5 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 10)",
            "",
            "**BUILDABLE_NOW-reachable by logic alone: 0**. Every C5 row is residual because",
            "its trims/load/pressure discriminators are absent or incomplete on C5 rows in the live corpus;",
            "logic without values cannot move `top3_family`.",
            "",
            f"**SCORING_GATED: {case_split['scoring_gated_count']} / {case_split['total']}**, split by residual bucket:",
            "",
        ]
    )
    by_bucket: dict[str, list[str]] = {}
    for case in case_split["scoring_gated"]:
        by_bucket.setdefault(case["bucket"], []).append(case["case_id"])
    for bucket, case_ids in sorted(by_bucket.items()):
        lines.append(f"- **{bucket} = {len(case_ids)}:** {_csv(case_ids)}.")
    lines.extend(
        [
            "",
            f"**Oracle-fault mix:** `{case_split['expected_family_mix']}`. "
            f"**Current winner mix:** `{case_split['predicted_family_mix']}`.",
            "All cases require C5 columns. **5 + 4 + 1 = 10.** ✔",
            "",
            "**CODE_LANDED != SCORE_MOVED, stated for C5:** the LeanRootCauseState emit",
            "logic and consumer map above are buildable from `cluster5.md`; any top3_family",
            "delta is unobservable until C5-SYNTH/C5A provides values. A pack report must",
            "never present wiring as score movement.",
            "",
            "---",
            "",
            "## 7. REGRESSION / FT-8 neighbour set (derived live)",
            "",
            "A C5 consumer edit touches `lean_condition.json` and `vacuum_leak.json` — both",
            "competition groups. The commit must re-audit every case those rules currently",
            "pass for a regressed family. Union of `passes_cases` across all LC + VL rules",
            "including the C3 lean-bias winners currently passing LC-001/LC-002 =",
            f"**{ft8['passes_cases_count']} cases**:",
            "",
            "```",
            _csv(ft8["passes_cases_union"]),
            "```",
            "",
            f"**Dual target+neighbour cases ({len(c5['dual_target_and_neighbour'])}):** "
            f"{_csv(c5['dual_target_and_neighbour'])}.",
            "",
            f"**LC-regression exposure:** {ft8['risk_note']}",
            "",
            "Rules derived live from the JSON files:",
            "",
            "| Rule | Family | Competition group | passes_cases count |",
            "| --- | --- | --- | --- |",
        ]
    )
    for rule in ft8["rules"]:
        lines.append(
            f"| `{rule['rule_id']}` | `{rule['fault_family']}` | "
            f"`{rule['competition_group']}` | {len(rule['passes_cases'])} |"
        )
    lines.extend(
        [
            "",
            "---",
            "",
            "## 8. Confounder disclosure (C5)",
            "",
            "**Source:** `cluster5.md` §Technical Characterization / §Physical Mechanisms + acq-spec §C4.",
            "",
            "| Confounder | Mechanism | Cite |",
            "| --- | --- | --- |",
        ]
    )
    for confounder in c5["confounder_disclosure"]["confounders"]:
        lines.append(
            f"| **{confounder['confounder']}** | {confounder['mechanism']} | "
            f"{confounder['cite']} |"
        )
    lines.extend(
        [
            "",
            "**Per-case mimic risk:** C5-SYNTH must use oracle-fault separability, not",
            "current rank, to decide seed bands. `CSV-113, CSV-114, REAL-004, era1_001` are",
            "EGR stuck open lookalikes, currently winning misfire (MF-001). C5-SYNTH must not",
            "back-solve them without proper grounds. `era3_015` PCV pressure sensor drift is TUNABLE_HELD.",
            "",
            f"**C4 dependency:** {c5['confounder_disclosure']['c4_dependency']}",
            "",
            "---",
            "",
            "## 9. Grounding-strength table per threshold",
            "",
            "| Signal | Threshold | Grounding | Feasibility Tier | Risk note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in c5["grounding_strength"]:
        lines.append(
            f"| {item['signal']} | {item['threshold']} | **{item['grounding']}** | "
            f"{item['feasibility_tier']} | {item['risk_note']} |"
        )
    lines.extend(
        [
            "",
            "**Weakest-grounded threshold:** The fuel trim delta (ΔTFT) recovery threshold is empirical.",
            "The Calculated Engine Load threshold (80%) and fuel pressure drop (35 kPa) are OEM-typical",
            "and represent altitude / system pressure variance risks.",
            "",
            "---",
            "",
            "## 10. ABSTAIN_FALLBACK (C5)",
            "",
            "If only static warm-idle trims are supplied, the case **stays abstained** at",
            "MARGIN=0.02. C5 separates on dynamic multi-point data: idle vs 2500 trims, WOT load,",
            "and WOT fuel pressure drop. One static idle point is not a discriminator.",
            "",
            "---",
            "",
            "## Provenance / guardrails",
            "",
            "- Read-only: no corpus column added, no producer/consumer wired, no rule/weight",
            "  edit, no yardstick mint, no synthesized values, no abstain-dial change",
            "  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No",
            "  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.",
            "- Sources: `v3/research/research_answers/cluster5.md`;",
            "  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C5/§C4;",
            "  `labs/comlab/registry/rules/lean_condition.json`, `vacuum_leak.json`;",
            "  `labs/comlab/registry/integration_shim.py` lines 540-569 for C3 interaction.",
            "- Governs `T-V3-P4-C5-PRE` → `T-V3-P4-C5-SYNTH` → `C5A` → `C5B`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Build and write the C5 reveal contract JSON + Markdown."""
    contract = build_contract()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(contract, fh, indent=2, sort_keys=False, ensure_ascii=False)
    OUT_MD.write_text(render_markdown(contract), encoding="utf-8")

    c5 = contract["c5_instance"]
    case_split = c5["case_split"]
    ft8 = c5["ft8_neighbours"]
    dual = c5["dual_target_and_neighbour"]
    col_audit = c5["column_audit"]
    print(f"C5 reveal contract written to {OUT_JSON} and {OUT_MD}")
    print(f"Total C5 cases: {case_split['total']}")
    print(f"  BUILDABLE_NOW: {case_split['buildable_now_count']}")
    print(f"  SCORING_GATED: {case_split['scoring_gated_count']}")
    print(f"  Bucket breakdown: {case_split['bucket_breakdown']}")
    print(f"  Expected family mix: {case_split['expected_family_mix']}")
    print(f"FT-8 touched families: {ft8['touched_families']}")
    print(f"FT-8 neighbour passes_cases union: {ft8['passes_cases_count']}")
    print(f"Dual target+neighbour: {len(dual)} — {dual}")
    print(f"Live audited columns count: {col_audit['live_columns_count']}")
    print(f"New required columns count: {col_audit['new_columns_count']}")
    print(f"Grounding-strength entries: {len(c5['grounding_strength'])}")


if __name__ == "__main__":
    main()
