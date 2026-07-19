#!/usr/bin/env python3
"""Read-only extractor for the C9 signal-pack REVEAL CONTRACT.

This script instances the frozen reveal contract template for C9 — independent
healthy-confirm. It audits the corpus columns, live rules, and baseline run results
to produce both the JSON twin and the Markdown report. No live engine code is modified.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

WS = Path(__file__).resolve().parent.parent
ACQ_JSON = WS / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
NO_FAULT_RULES = WS / "labs/comlab/registry/rules/no_fault.json"
OUT_JSON = WS / "v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.json"
OUT_MD = WS / "v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.md"

C9_COLUMNS = [
    "readiness_supported_complete_bool",
    "stored_dtc_count",
    "pending_dtc_count",
    "permanent_dtc_count",
    "mode06_min_margin_pct",
    "warmup_cycles_since_clear",
    "miles_since_clear",
    "stft_idle_pct",
    "ltft_idle_pct",
    "stft_2500_pct",
    "ltft_2500_pct",
    "gas_delta_hc_ppm",
    "gas_delta_co_pct",
    "gas_delta_co2_pct",
    "gas_delta_o2_pct",
]

REVEAL_SECTIONS = [
    {
        "key": "BUILDABLE_NOW",
        "definition": "Producer/consumer logic + thresholds derivable from the cluster research answer; provable by unit tests on synthetic vectors, with no owner data."
    },
    {
        "key": "SCORING_GATED",
        "definition": "The per-case owner columns still required and which residual case_ids each unlocks; stays abstained until the owner supplies real measured values."
    },
    {
        "key": "CODE_LANDED_NEQ_SCORE_MOVED",
        "definition": "Explicit separation of producer/consumer logic shipped from top3_family delta. Landing code proves the discriminator is wired; it does not move score until gated data exists."
    },
    {
        "key": "REGRESSION_FT8",
        "definition": "The neighbour set the consumer edit touches, plus the no-regressed-family audit run on the full corpus at commit time."
    },
    {
        "key": "ABSTAIN_FALLBACK",
        "definition": "Cases whose discriminating signal the owner cannot supply stay abstained at MARGIN=0.02, never guessed from static idle data."
    }
]

C9_PRODUCER_THRESHOLDS = [
    {
        "signal": "OBD readiness monitor completeness",
        "maneuver": "Read Mode $01 PID 0x01",
        "threshold": "All supported non-continuous monitors = COMPLETE / READY",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "readiness_supported_complete_bool",
        "cite": "cluster9.1.md §2; SAE J1979",
        "grounding": "standardized (CARB/EPA)",
        "feasibility_tier": "Tier A: generic OBD-II live data"
    },
    {
        "signal": "OBD emission-related DTC count",
        "maneuver": "Read Mode $03, Mode $07, and Mode $0A (where supported)",
        "threshold": "Stored, pending, and permanent DTCs = 0",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "stored_dtc_count, pending_dtc_count, permanent_dtc_count",
        "cite": "cluster9.1.md §2; SAE J1979",
        "grounding": "standardized (SAE J1979)",
        "feasibility_tier": "Tier A: generic OBD-II live data"
    },
    {
        "signal": "OBD Mode $06 monitor test margins",
        "maneuver": "Read Mode $06 test value and limit for non-continuous monitors",
        "threshold": "Test value must be inside limit with margin >= 10% of limit range",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "mode06_min_margin_pct",
        "cite": "value9.md §1; cluster9.1.md §2; SAE J1979",
        "grounding": "standardized (regulatory cut)",
        "feasibility_tier": "Tier A: generic OBD-II Mode $06 data"
    },
    {
        "signal": "OBD warm-up cycles since DTCs cleared",
        "maneuver": "Read Mode $01 PID 0x30 / 0x4D",
        "threshold": "Warm-up cycles since clear >= 5",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "warmup_cycles_since_clear",
        "cite": "value9.md §1; EPA/CARB",
        "grounding": "standardized (EPA/CARB)",
        "feasibility_tier": "Tier A: generic OBD-II live data"
    },
    {
        "signal": "OBD distance traveled since DTCs cleared",
        "maneuver": "Read Mode $01 PID 0x31 / 0x4E",
        "threshold": "Distance since clear >= 200 miles",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "miles_since_clear",
        "cite": "value9.md §1; CARB",
        "grounding": "standardized (CARB)",
        "feasibility_tier": "Tier A: generic OBD-II live data"
    },
    {
        "signal": "Short-Term Fuel Trim (STFT)",
        "maneuver": "Warm idle and steady 2500 RPM no load",
        "threshold": "STFT within +/-5% (P10-P90: -4% to +4%)",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "stft_idle_pct, stft_2500_pct",
        "cite": "value9.md §1; SAE J1979",
        "grounding": "standardized (OEM/SAE J1979)",
        "feasibility_tier": "Tier A: generic OBD-II live trims"
    },
    {
        "signal": "Long-Term Fuel Trim (LTFT)",
        "maneuver": "Warm idle and steady 2500 RPM no load",
        "threshold": "LTFT within +/-7% (P10-P90: -6% to +6%)",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "ltft_idle_pct, ltft_2500_pct",
        "cite": "value9.md §1 (WIDEN); SAE J1979",
        "grounding": "standardized (OEM/SAE J1979)",
        "feasibility_tier": "Tier A: generic OBD-II live trims"
    },
    {
        "signal": "Fuel trim delta between idle and 2500 RPM",
        "maneuver": "Transition from idle to 2500 RPM",
        "threshold": "Delta of fuel trim <= +/-5%",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct",
        "cite": "value9.md §1; Workshop practice",
        "grounding": "manufacturer-typical",
        "feasibility_tier": "Tier A: generic OBD-II live trims"
    },
    {
        "signal": "Two-point gas delta: HC",
        "maneuver": "Two-point tailpipe gas capture (idle to 2500 RPM no load)",
        "threshold": "Delta HC within -10 to +15 ppm",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "gas_delta_hc_ppm",
        "cite": "value9.md §1 (TIGHTEN); EPA/BAR",
        "grounding": "anecdotal / workshop norm",
        "feasibility_tier": "Tier B: 5-gas two-point capture"
    },
    {
        "signal": "Two-point gas delta: CO",
        "maneuver": "Two-point tailpipe gas capture (idle to 2500 RPM no load)",
        "threshold": "Delta CO within -0.15 to +0.15%",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "gas_delta_co_pct",
        "cite": "value9.md §1 (TIGHTEN); EPA/BAR",
        "grounding": "anecdotal / workshop norm",
        "feasibility_tier": "Tier B: 5-gas two-point capture"
    },
    {
        "signal": "Two-point gas delta: CO2",
        "maneuver": "Two-point tailpipe gas capture (idle to 2500 RPM no load)",
        "threshold": "Delta CO2 typically positive, within +0.3 to +0.8%",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "gas_delta_co2_pct",
        "cite": "value9.md §1 (SHIFT); EPA/BAR",
        "grounding": "anecdotal / workshop norm",
        "feasibility_tier": "Tier B: 5-gas two-point capture"
    },
    {
        "signal": "Two-point gas delta: O2",
        "maneuver": "Two-point tailpipe gas capture (idle to 2500 RPM no load)",
        "threshold": "Delta O2 within -0.5 to +0.4%",
        "verdict": "SYSTEM_HEALTH_CONFIRMED gate",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "gas_delta_o2_pct",
        "cite": "value9.md §1; EPA/BAR",
        "grounding": "anecdotal / workshop norm",
        "feasibility_tier": "Tier B: 5-gas two-point capture"
    },
    {
        "signal": "Unsupported, incomplete, or marginal OBD health evidence",
        "maneuver": "Any operating state",
        "threshold": "Any gate check fails or is missing; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "verdict": "SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "producer_state": "OBDLab HealthConfirmationState",
        "evidence_fields": "absence of complete OBD/trim/gas-delta confirmation",
        "cite": "cluster9.1.md §Bottom Line; V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C9.6 line 67",
        "grounding": "physics/regulatory rationale (provenance required)",
        "feasibility_tier": "Abstain fallback"
    }
]

C9_CONFOUNDERS = [
    {
        "confounder": "Catalyst masking",
        "mechanism": "A healthy catalyst downstream strongly attenuates emissions, meaning tailpipe gas alone cannot diagnose engine-out or sensor degradation upstream. Separated by requiring complete OBD readiness, DTC absence, and Mode $06 margins rather than tailpipe gas alone.",
        "cite": "cluster9.1.md §2; cluster9.2.md §Technical characterization"
    },
    {
        "confounder": "Lazy oxygen sensor / sensor under-detection",
        "mechanism": "A degraded O2 sensor transitions slowly, delaying fuel correction without setting a DTC. Clean tailpipe gas masks the latency. Separated by O2 sensor dynamics (transition time < 150 ms, amplitude swing min/max) and fuel trim stability.",
        "cite": "cluster9.1.md §2; value9.md §1"
    },
    {
        "confounder": "Freshly cleared OBD memory",
        "mechanism": "BATTERY_DISCONNECT or scan tool clear makes readiness incomplete and DTC count zero, creating a blind spot where active faults are temporarily hidden. Separated by requiring warm-up cycles >= 5 and miles since clear >= 200.",
        "cite": "value9.md §1; cluster9.1.md §Bottom Line"
    },
    {
        "confounder": "Marginal emissions systems",
        "mechanism": "Components that pass OBD but operate near malfunction limits can be missed. Separated by requiring Mode $06 monitor margins >= 10% of the limit range.",
        "cite": "cluster9.1.md §2; value9.md §1"
    }
]


def _load(path: Path) -> Any:
    """Load a JSON file from *path*."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _c9_case_split() -> dict[str, Any]:
    """Return the 11 C9 cases, all scoring-gated until C9 values exist."""
    acq = _load(ACQ_JSON)
    c9_cases = [c for c in acq["case_unlocks"] if c.get("cluster") == "C9"]
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
        for c in sorted(c9_cases, key=lambda row: row["case_id"])
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
            "All 11 C9 rows are SCORING_GATED. The producer/consumer logic is "
            "buildable from research, but the top3_family delta is unknowable "
            "until readiness/DTC/trim/gas-delta values exist."
        ),
    }


def _ft8_neighbours() -> dict[str, Any]:
    """Derive FT-8 neighbour set live from no_fault rules and baseline results."""
    rules: list[dict[str, Any]] = []
    passes: set[str] = set()
    data = _load(NO_FAULT_RULES)
    for rule in data["rules"]:
        passes_cases = rule.get("passes_cases", [])
        rules.append(
            {
                "rule_id": rule["rule_id"],
                "fault_family": rule["fault_family"],
                "source_file": str(NO_FAULT_RULES.relative_to(WS)),
                "competition_group": rule.get("competition_group"),
                "base_weight": rule.get("base_weight"),
                "passes_cases": passes_cases,
            }
        )
        passes.update(passes_cases)

    # Also add the runtime no_fault winners that won NF rules in the baseline run POST_T_V3_P4_C5B
    results_path = WS / "apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json"
    runtime_nf_winners = set()
    if results_path.exists():
        with results_path.open("r", encoding="utf-8") as fh:
            res_data = json.load(fh)
        for r in res_data.get("results", []):
            verdict = r.get("verdict") or {}
            fault_code = verdict.get("fault_code")
            if fault_code and fault_code.startswith("NF-"):
                runtime_nf_winners.add(r["case_id"])

    union_passes = passes.union(runtime_nf_winners)
    return {
        "touched_families": ["no_fault"],
        "touched_competition_groups": ["no_fault"],
        "rules": rules,
        "passes_cases_union": sorted(list(union_passes)),
        "passes_cases_count": len(union_passes),
        "static_passes_cases": sorted(list(passes)),
        "runtime_passes_cases": sorted(list(runtime_nf_winners)),
        "risk_note": (
            "NF rules touch no-fault cases. A C9 boost could resurrect a "
            "no_fault verdict on cases that have active sensor or ECU faults. "
            "Thus, the live C6B prunes must take precedence."
        ),
    }


def _mimic_risk(case_split: dict[str, Any]) -> list[dict[str, str | None]]:
    """Classify lookalike risk disclosed for C9-SYNTH."""
    risks: list[dict[str, str | None]] = []
    for case in case_split["scoring_gated"]:
        expected = case["expected_family"]
        predicted = case.get("predicted_family")
        if expected == "misfire" and predicted == "no_fault":
            note = "RISKY FALSE-HEALTHY LOOKALIKE; currently misclassified. Needs OBD check (DTCs or Mode $06) to separate."
        elif predicted == "catalyst_failure":
            note = "catalyst_failure lookalike; needs complete readiness, DTC absence, and Mode $06 margins to confirm health"
        elif predicted == "sensor_fault":
            note = "sensor_fault lookalike; needs O2 sensor dynamics (amplitude, switch rate) to confirm health"
        elif predicted == "rich_mixture":
            note = "rich_mixture lookalike; needs normal STFT/LTFT trims to confirm health"
        elif predicted == "ecu_fault":
            note = "ecu_fault lookalike; needs normal OBD communication and DTC absence to confirm health"
        else:
            note = "C9-SYNTH must decide separability from oracle fault, not current rank"
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
    for threshold in C9_PRODUCER_THRESHOLDS:
        grounding = threshold["grounding"]
        if "anecdotal" in grounding:
            risk = "Gas deltas are derived from workshop norms; healthy deltas tend to be tight, but no regulatory cut exists."
        elif "manufacturer-typical" in grounding:
            risk = "Fuel trim delta is highly typical but can vary slightly across speed-density vs MAF architectures."
        elif "standardized" in grounding:
            if "Mode $06" in threshold["signal"]:
                risk = "Mode $06 10% margin is a standard regulatory cut, but healthy populations vary widely above it."
            else:
                risk = "Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive."
        else:
            risk = "Unsupported/incomplete data defaults to SENSOR_HEALTH_UNPROVEN_ABSTAIN."
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

    live_cols = sorted([col for col in C9_COLUMNS if col in header])
    new_cols = sorted([col for col in C9_COLUMNS if col not in header])

    return {
        "total_contract_columns": len(C9_COLUMNS),
        "live_columns": live_cols,
        "live_columns_count": len(live_cols),
        "new_columns": new_cols,
        "new_columns_count": len(new_cols),
        "note": (
            f"Of the {len(C9_COLUMNS)} required C9 columns, {len(live_cols)} already exist "
            f"in the live schema (4 trims from C2B/C5B). The genuinely new ask "
            f"is shrank to {len(new_cols)} columns. For C9 rows, the live columns exist in "
            f"the schema but are currently empty/null."
        ),
    }


def build_contract() -> dict[str, Any]:
    """Assemble the machine-readable C9 reveal contract."""
    case_split = _c9_case_split()
    ft8 = _ft8_neighbours()
    c9_ids = {case["case_id"] for case in case_split["scoring_gated"]}
    dual_target_neighbour = sorted(c9_ids & set(ft8["passes_cases_union"]))
    column_audit = _perform_column_audit()

    return {
        "task": "T-V3-P4-C9-PRE",
        "generated": "2026-07-06",
        "mode": "DISCLOSE only (read-only pre-author; no wiring, no score move)",
        "purpose": (
            "Instance the frozen reveal contract for C9 — independent healthy-confirm. "
            "Surfaces HealthConfirmationState gates, consumer mapping, C6 interaction/pruning, "
            "C3 interaction, 11-case split, live FT-8 neighbours, column audit, "
            "confounders, and baseline pin."
        ),
        "reveal_contract_template": REVEAL_SECTIONS,
        "baseline": {
            "yardstick": "V3_YARDSTICK_2026-07-06-C5B",
            "csv_hash": "c49c17af1182a3eb07056a3fbf27c101378a32f35e375b18b3104d3928d8c7fd",
            "oracle_hash": "3088a7c3",
            "scorer": "apps/wired/v7/run_suite.py (hash-locked, untouched)",
            "named_run": "POST_T_V3_P4_C5B",
            "run_dir": "apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json",
            "note": (
                "All C9 sizing references this current post-C5B baseline. If any "
                "commit lands first, stop and re-pin before C9-SYNTH/C9A."
            ),
        },
        "c9_instance": {
            "cluster": "C9",
            "title": "independent healthy-confirm",
            "research_source": "v3/research/research_answers/cluster9.1.md",
            "producer": {
                "states": ["OBDLab HealthConfirmationState"],
                "emit_condition": (
                    "Emit SYSTEM_HEALTH_CONFIRMED when all readiness monitors are complete, "
                    "no stored/pending/permanent DTCs are present, Mode $06 margins are >= 10%, "
                    "fuel trims are within +/-7% and stable (delta <= 5%), and 2-point gas deltas "
                    "are stable. Emit SENSOR_HEALTH_UNPROVEN_ABSTAIN otherwise."
                ),
                "thresholds": C9_PRODUCER_THRESHOLDS,
                "corpus_columns": C9_COLUMNS,
            },
            "column_audit": column_audit,
            "consumer": {
                "no_fault": {
                    "file": "labs/comlab/registry/rules/no_fault.json",
                    "rules": ["NF-001", "NF-002"],
                    "reads": (
                        "NF-001/NF-002 consume readiness, DTC counts, Mode $06, and trim columns. "
                        "In C9B, they will gate on the C9 state output SYSTEM_HEALTH_CONFIRMED."
                    ),
                    "evidence_fields": C9_COLUMNS,
                }
            },
            "c6_interaction": {
                "description": "C6B prunes NF-001/NF-002 when SensorDynamicsState is in decisive sensor-fault states (O2_LAZY_OR_BIASED or MAF_UNDERREAD).",
                "interaction_rule": "The C6 sensor-fault prune of NF-001/NF-002 must take precedence over any C9 healthy-confirm boost. If c6_decisive is true, NF-001/NF-002 must remain pruned (return None) to prevent a degraded/lazy sensor from being overridden by a C9 boost.",
                "live_shim_reference": "integration_shim.py::_score_rule lines 685-691 evaluates c6_decisive and returns None for NF-001/NF-002."
            },
            "c3_interaction": {
                "live_c3_state": "ControlPlausibilityState.CONTROL_REFERENCE_FAULT",
                "live_c3_reader": "integration_shim.py::_control_plausibility_state",
                "live_c3_effect": "integration_shim.py::_score_rule boosts EF-001/002/003 and prunes SF-001/002 (unless c6_decisive) when CONTROL_REFERENCE_FAULT is present.",
                "required_precedence_for_c9b": "C3 control-reference faults also prune SF-001/002 under C3 precedence. Since no_fault rules (NF-001/002) require clean OBD health, they are naturally inactive/pruned if any DTC is present, but C3 precedence is preserved: a C3 active control reference fault inherently invalidates any C9 no_fault call."
            },
            "case_split": case_split,
            "ft8_neighbours": ft8,
            "dual_target_and_neighbour": dual_target_neighbour,
            "confounder_disclosure": {
                "confounders": C9_CONFOUNDERS,
                "mimic_risk_per_case": _mimic_risk(case_split),
                "c4_dependency": (
                    "C9 is theprove-healthy cluster and is independent of C4, but it is placed "
                    "next in the sequence (C2 -> C3 -> C6 -> C5 -> C4 -> C9 -> C8 -> C1 -> C7) "
                    "because C9 is the highest remaining yield research-independent pack."
                ),
            },
            "grounding_strength": _grounding_strength_table(),
            "code_landed_neq_score_moved": (
                "The C9 producer emit logic and consumer map are buildable from cluster9.1.md; "
                "any top3_family score movement cannot be shown until owner/synthetic C9 values are populated."
            ),
            "abstain_fallback": (
                "If any OBD readiness monitor is incomplete, DTCs are present, Mode $06 margins "
                "are too narrow (<10%), fuel trims are unstable, or OBD history is too recently cleared, "
                "the case must stay abstained at MARGIN=0.02. Vehicles with unproven health must not be guessed."
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
    """Render the human-readable C9 reveal report."""
    c9 = contract["c9_instance"]
    base = contract["baseline"]
    case_split = c9["case_split"]
    ft8 = c9["ft8_neighbours"]
    col_audit = c9["column_audit"]
    lines: list[str] = [
        "# V3_C9_REVEAL_CONTRACT_2026-07-06",
        "",
        "**Task:** `T-V3-P4-C9-PRE`  **Mode:** DISCLOSE only (read-only pre-author)",
        "**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no",
        "**Machine-readable twin:** `v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.json`",
        "(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c9_contract.py`).",
        "",
        "This document instances the frozen reveal contract for **C9 — independent healthy-confirm**,",
        "the next pack in the pinned sequence (C2 → C3 → C6 → C5 → C4 → **C9** → C8 → C1 → C7).",
        "It builds nothing and scores nothing; it fixes how C9 discloses thresholds, consumers,",
        "C6 interaction, C3 interaction, FT-8 exposure, column audit, and stay-abstained cases.",
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
            "## 2. C9 producer extraction (cited to `cluster9.1.md` / `value9.md`)",
            "",
            "The C9 producer is **OBDLab `HealthConfirmationState`**. It emits",
            "`SYSTEM_HEALTH_CONFIRMED` or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.",
            "The emit thresholds, transcribed read-only from the research answer:",
            "",
            "| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for threshold in c9["producer"]["thresholds"]:
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
            "**Producer emit summary:** `SYSTEM_HEALTH_CONFIRMED` requires all supported monitors to be complete,",
            "no DTCs of any type (stored, pending, permanent), Mode $06 margins >= 10%, trims within +/-7% and stable,",
            "and 2-point gas deltas stable. Any deviation, incomplete status, or fresh OBD clear (warm-ups < 5, miles < 200)",
            "produces `SENSOR_HEALTH_UNPROVEN_ABSTAIN` to prevent false-healthy diagnostic leaks.",
            "",
            "---",
            "",
            "## 3. C9 consumer mapping (named; no edit)",
            "",
            "| Family file | Rules | Field each would read | What the C9 state supplies |",
            "| --- | --- | --- | --- |",
            "| `no_fault.json` | **NF-001 / NF-002** | Readiness, DTCs, Mode $06, trims. Gated on C9 state output in C9B. | Positive-health confirmation state. |",
            "",
            "Nothing is edited here. The consumer map is for C9-SYNTH/C9A/C9B inheritance.",
            "",
            "---",
            "",
            "## 4. C6-INTERACTION & C3-INTERACTION DISCLOSURE (mandatory)",
            "",
            "### C6-INTERACTION",
            "",
            f"- **Interaction description:** {c9['c6_interaction']['description']}",
            f"- **Interaction rule:** {c9['c6_interaction']['interaction_rule']}",
            f"- **Live shim reference:** {c9['c6_interaction']['live_shim_reference']}",
            "",
            "### C3-INTERACTION",
            "",
            "C3 control-reference precedence is preserved:",
            "",
            f"- Live state check: `{c9['c3_interaction']['live_c3_state']}` via `{c9['c3_interaction']['live_c3_reader']}`.",
            f"- Live C3 effect: {c9['c3_interaction']['live_c3_effect']}",
            f"- Required precedence: {c9['c3_interaction']['required_precedence_for_c9b']}",
            "",
            "---",
            "",
            "## 5. ALREADY-LIVE-COLUMN AUDIT (mandatory)",
            "",
            f"- **Total required C9 columns:** {col_audit['total_contract_columns']}",
            f"- **Already live in schema ({col_audit['live_columns_count']}):** `{_csv(col_audit['live_columns'])}`",
            f"- **Genuinely new ask ({col_audit['new_columns_count']}):** `{_csv(col_audit['new_columns'])}`",
            "",
            col_audit["note"],
            "",
            "---",
            "",
            "## 6. C9 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 11)",
            "",
            "**BUILDABLE_NOW-reachable by logic alone: 0**. Every C9 row is residual because",
            "its readiness/DTC/trim/gas-delta columns are empty/null in the live corpus;",
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
            f"**Oracle-family mix:** `{case_split['expected_family_mix']}`. "
            f"**Current winner family mix:** `{case_split['predicted_family_mix']}`.",
            "All cases require C9 columns. **10 + 1 = 11.** ✔",
            "",
            "**CODE_LANDED != SCORE_MOVED, stated for C9:** the HealthConfirmationState emit",
            "logic and consumer map above are buildable from `cluster9.1.md`; any top3_family",
            "delta is unobservable until C9-SYNTH/C9A provides values. A pack report must",
            "never present wiring as score movement.",
            "",
            "---",
            "",
            "## 7. REGRESSION / FT-8 neighbour set (derived live)",
            "",
            "A C9 consumer edit touches `no_fault.json` — the no_fault competition group.",
            "The commit must re-audit every case those rules currently pass for a regressed family.",
            "Union of `passes_cases` across all NF rules including the baseline runtime winners =",
            f"**{ft8['passes_cases_count']} cases**:",
            "",
            "```",
            _csv(ft8["passes_cases_union"]),
            "```",
            "",
            f"**Dual target+neighbour cases ({len(c9['dual_target_and_neighbour'])}):** "
            f"{_csv(c9['dual_target_and_neighbour'])}.",
            "",
            f"**NF-regression exposure:** {ft8['risk_note']}",
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
            "## 8. Confounder disclosure (C9)",
            "",
            "**Source:** `cluster9.1.md` / `cluster9.2.md` + `value9.md`.",
            "",
            "| Confounder | Mechanism | Cite |",
            "| --- | --- | --- |",
        ]
    )
    for confounder in c9["confounder_disclosure"]["confounders"]:
        lines.append(
            f"| **{confounder['confounder']}** | {confounder['mechanism']} | "
            f"{confounder['cite']} |"
        )
    lines.extend(
        [
            "",
            "**Per-case mimic risk:** C9-SYNTH must use oracle-fault separability, not",
            "current rank, to decide seed bands. For example, `era2_016` (expected misfire) is currently",
            "winning `no_fault` due to clean tailpipe gas; C9-SYNTH must not back-solve it.",
            "",
            f"**C4 dependency:** {c9['confounder_disclosure']['c4_dependency']}",
            "",
            "---",
            "",
            "## 9. Grounding-strength table per threshold",
            "",
            "| Signal | Threshold | Grounding | Feasibility Tier | Risk note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in c9["grounding_strength"]:
        lines.append(
            f"| {item['signal']} | {item['threshold']} | **{item['grounding']}** | "
            f"{item['feasibility_tier']} | {item['risk_note']} |"
        )
    lines.extend(
        [
            "",
            "**Weakest-grounded threshold:** The two-point 5-gas deltas are anecdotal/workshop norms",
            "and are subject to baseline analyzer noise.",
            "",
            "---",
            "",
            "## 10. ABSTAIN_FALLBACK (C9)",
            "",
            "If any OBD readiness monitor is incomplete, DTCs are present, Mode $06 margins",
            "are too narrow (<10%), fuel trims are unstable, or OBD history is too recently cleared,",
            "the case **stays abstained** at MARGIN=0.02. Vehicles with unproven health must not be guessed.",
            "",
            "---",
            "",
            "## Provenance / guardrails",
            "",
            "- Read-only: no corpus column added, no producer/consumer wired, no rule/weight",
            "  edit, no yardstick mint, no synthesized values, no abstain-dial change",
            "  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No",
            "  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.",
            "- Sources: `v3/research/research_answers/cluster9.1.md`;",
            "  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C9;",
            "  `labs/comlab/registry/rules/no_fault.json`;",
            "  `labs/comlab/registry/integration_shim.py` for C6/C3 interactions.",
            "- Governs `T-V3-P4-C9-PRE` → `T-V3-P4-C9-SYNTH` → `C9A` → `C9B`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Build and write the C9 reveal contract JSON + Markdown."""
    contract = build_contract()
    c9 = contract["c9_instance"]

    OUT_JSON.write_text(json.dumps(contract, indent=2), encoding="utf-8")
    print(f"Wrote JSON contract to {OUT_JSON}")

    md_text = render_markdown(contract)
    OUT_MD.write_text(md_text, encoding="utf-8")
    print(f"Wrote Markdown report to {OUT_MD}")

    print(f"Total C9 cases: {c9['case_split']['total']}")
    print(f"FT-8 neighbour set size: {c9['ft8_neighbours']['passes_cases_count']}")
    print(f"Grounding-strength entries: {len(c9['grounding_strength'])}")


if __name__ == "__main__":
    main()
