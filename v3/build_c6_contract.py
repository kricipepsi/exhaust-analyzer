"""Read-only extractor for the C6 signal-pack REVEAL CONTRACT.

Task: T-V3-P4-C6-PRE.  This script instances the frozen signal-pack
reveal contract for C6 (sensor fault under-detection). It writes only the
C6 report pair under ``v3/reports/``; it does not touch corpus, registry,
engine, scorer, run JSON, yardsticks, or synthetic data.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

WS = Path(__file__).resolve().parent.parent
ACQ_JSON = WS / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
SENSOR_RULES = WS / "labs/comlab/registry/rules/sensor_fault.json"
NO_FAULT_RULES = WS / "labs/comlab/registry/rules/no_fault.json"
OUT_JSON = WS / "v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json"
OUT_MD = WS / "v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md"

C6_COLUMNS = [
    "mode06_o2_response_margin_pct",
    "o2_rich_to_lean_ms",
    "o2_lean_to_rich_ms",
    "maf_actual_calc_delta_pct_idle",
    "maf_actual_calc_delta_pct_2500",
    "maf_gps_idle",
    "maf_gps_2500",
    "calc_airflow_gps_idle",
    "calc_airflow_gps_2500",
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

C6_PRODUCER_THRESHOLDS: list[dict[str, str]] = [
    {
        "signal": "Mode $06 oxygen-sensor monitor margin",
        "maneuver": "Warm closed loop; retrieve Mode $06 current result and min/max limits",
        "threshold": (
            "Use the ECU's stored min/max acceptable band; low or exceeded "
            "margin to the vehicle-specific limit emits O2_LAZY_OR_BIASED"
        ),
        "verdict": "O2_LAZY_OR_BIASED",
        "producer_state": "OBDLab SensorDynamicsState",
        "evidence_fields": "mode06_o2_response_margin_pct",
        "cite": (
            "cluster6.md §Question One Answer lines 114-115; "
            "§Question Four Answer line 155; Candidate Signature Table line 171"
        ),
        "grounding": "standardized-transport / manufacturer-specific numeric limit",
        "feasibility_tier": "Tier A: generic OBD-II Mode $06 where exposed",
    },
    {
        "signal": "Forced rich→lean / lean→rich O2 response timing",
        "maneuver": (
            "Stabilize at about 2500 rpm no-load; decel fuel cut for rich→lean; "
            "controlled return/enrichment for lean→rich"
        ),
        "threshold": (
            "Prefer vehicle Mode $06/OEM limit; absent that, longer-than-expected "
            "transition is positive evidence. Research names the direction, not a "
            "fleet-wide millisecond fail line; 849 ms / <150 ms examples must not "
            "be treated as universal."
        ),
        "verdict": "O2_LAZY_OR_BIASED",
        "producer_state": "OBDLab SensorDynamicsState",
        "evidence_fields": "o2_rich_to_lean_ms, o2_lean_to_rich_ms",
        "cite": (
            "cluster6.md §Question Three Answer lines 147-151; "
            "§Question Four Answer line 157; Candidate Signature Table line 172"
        ),
        "grounding": "manufacturer-typical (direction strong, universal ms bound weak)",
        "feasibility_tier": "Tier A if ECU monitor decisive; Tier C if scope timing required",
    },
    {
        "signal": "MAF actual vs calculated airflow plausibility",
        "maneuver": "Warm idle and steady 2500 rpm no-load; compare measured MAF to modeled airflow",
        "threshold": (
            "Sustained measured-MAF shortfall greater than roughly 10-15% versus "
            "modeled airflow at BOTH points emits MAF_UNDERREAD"
        ),
        "verdict": "MAF_UNDERREAD",
        "producer_state": "OBDLab SensorDynamicsState",
        "evidence_fields": (
            "maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, "
            "maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, "
            "calc_airflow_gps_2500"
        ),
        "cite": (
            "cluster6.md §Question One Answer lines 117-118; "
            "§Question Three Answer line 149; §Question Four Answer line 161; "
            "Candidate Signature Table line 174"
        ),
        "grounding": "empirical-inferred (component accuracy anchored; vehicle threshold provisional)",
        "feasibility_tier": "Tier A if PID set available; otherwise Tier C modeled-airflow support",
    },
    {
        "signal": "Static-only O2/MAF evidence",
        "maneuver": "Single static O2 voltage, AFR, or MAF value only",
        "threshold": "Static-only values are rejected as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "verdict": "SENSOR_HEALTH_UNPROVEN_ABSTAIN",
        "producer_state": "OBDLab SensorDynamicsState",
        "evidence_fields": "absence of decisive dynamic Mode $06/O2 timing/MAF plausibility evidence",
        "cite": (
            "cluster6.md §Question One Answer lines 126-129; "
            "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C6.6 line 93"
        ),
        "grounding": "physics/regulatory rationale (dynamic inconsistency required)",
        "feasibility_tier": "Abstain fallback",
    },
]

C6_CONFOUNDERS: list[dict[str, str]] = [
    {
        "confounder": "Upstream exhaust leak or intake tract disconnection",
        "mechanism": (
            "Cluster6 pre-gate requires no obvious upstream exhaust leak or intake "
            "tract disconnection. Either can distort O2 or airflow plausibility and "
            "mimic lazy-O2/MAF-underread behavior."
        ),
        "cite": "cluster6.md §Question Three Answer line 145",
    },
    {
        "confounder": "MAF architecture / speed-density vehicle",
        "mechanism": (
            "If no MAF is fitted, the MAF_UNDERREAD branch is not applicable; the "
            "case needs O2 dynamics or abstain, not an invented MAF comparison."
        ),
        "cite": "cluster6.md §Question Three Answer line 145 and flow lines 215-220",
    },
    {
        "confounder": "Wideband versus switching O2 architecture",
        "mechanism": (
            "If the upstream sensor is wideband, cross-count logic is not applicable; "
            "Mode $06/OEM limits or appropriate active dynamics must drive the decision."
        ),
        "cite": "cluster6.md §Question Three Answer line 145",
    },
    {
        "confounder": "C4 exhaust-leak / true-lean overlap",
        "mechanism": (
            "C4 consumes these same C6 O2/MAF dynamics columns to separate exhaust "
            "leak, true lean, and biased-O2 lookalikes. C6-SYNTH must mark cases "
            "outside sensor/no-fault separability as stay-abstained candidates."
        ),
        "cite": "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md lines 106-112",
    },
]

C3_INTERACTION = {
    "live_c3_state": "ControlPlausibilityState.CONTROL_REFERENCE_FAULT",
    "live_c3_reader": "integration_shim.py::_control_plausibility_state lines 540-557",
    "live_c3_effect": (
        "integration_shim.py::_score_rule lines 562-569 boosts EF-001/002/003 "
        "by +0.10 and prunes SF-001/SF-002 when CONTROL_REFERENCE_FAULT is present."
    ),
    "c6_future_effect": (
        "C6 will boost sensor/no-fault consumers from SensorDynamicsState: "
        "O2_LAZY_OR_BIASED, MAF_UNDERREAD, or SENSOR_HEALTH_UNPROVEN_ABSTAIN."
    ),
    "column_population_today": "C3 columns and C6 columns are disjoint in the current corpus.",
    "required_precedence_for_c6b": (
        "If a future row carries both C3 control-reference columns and C6 sensor-dynamics "
        "columns, C3 control-reference pruning must run first for SF-001/SF-002. "
        "Only a decisive C6 dynamic sensor fault may re-enable/boost sensor rules; "
        "static-only C6 evidence must preserve abstain/prune behavior. This prevents "
        "a control-reference fault from being relabelled as a lazy O2 sensor."
    ),
}


def _load(path: Path) -> Any:
    """Load a JSON file from *path*."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _c6_case_split() -> dict[str, Any]:
    """Return the 14 C6 cases, all scoring-gated until C6 values exist."""
    acq = _load(ACQ_JSON)
    c6_cases = [c for c in acq["case_unlocks"] if c.get("cluster") == "C6"]
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
        for c in sorted(c6_cases, key=lambda row: row["case_id"])
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
            "All 14 C6 rows are SCORING_GATED. The producer/consumer logic is "
            "buildable from research, but the top3_family delta is unknowable "
            "until Mode $06/O2 timing/MAF plausibility values exist."
        ),
    }


def _ft8_neighbours() -> dict[str, Any]:
    """Derive FT-8 neighbour set live from sensor_fault and no_fault rules."""
    rules: list[dict[str, Any]] = []
    passes: set[str] = set()
    for family, path in (("sensor_fault", SENSOR_RULES), ("no_fault", NO_FAULT_RULES)):
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
    return {
        "touched_families": ["sensor_fault", "no_fault"],
        "touched_competition_groups": ["sensor_fault", "no_fault"],
        "rules": rules,
        "passes_cases_union": sorted(passes),
        "passes_cases_count": len(passes),
        "risk_note": (
            "NF rules touch healthy/no-fault cases. A false C6 boost that regresses "
            "NF-001/NF-002 is high-cost because it turns a healthy case into a fault."
        ),
    }


def _mimic_risk(case_split: dict[str, Any]) -> list[dict[str, str | None]]:
    """Classify per-case lookalike risk disclosed for C6-SYNTH."""
    risks: list[dict[str, str | None]] = []
    for case in case_split["scoring_gated"]:
        expected = case["expected_family"]
        predicted = case.get("predicted_family")
        if expected == "sensor_fault" and predicted == "no_fault":
            note = "healthy-vs-under-detected split; NF regression exposure is direct"
        elif expected == "sensor_fault" and predicted in {"misfire", "lean_condition", "catalyst_failure"}:
            note = f"{predicted} lookalike; dynamic C6 data needed or stay abstained"
        elif expected == "misfire" and predicted == "sensor_fault":
            note = "oracle is misfire lookalike; C6 should not back-solve into sensor fault"
        else:
            note = "C6-SYNTH must decide separability from oracle fault, not current rank"
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
    for threshold in C6_PRODUCER_THRESHOLDS:
        grounding = threshold["grounding"]
        if grounding.startswith("standardized-transport"):
            risk = "Strong transport standard; numeric pass/fail limit remains vehicle-specific."
        elif grounding.startswith("manufacturer-typical"):
            risk = "Direction is strong; do not freeze a universal millisecond threshold."
        elif grounding.startswith("empirical-inferred"):
            risk = "Provisional producer-tuning risk; validate 10-15% band on real vehicles."
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


def build_contract() -> dict[str, Any]:
    """Assemble the machine-readable C6 reveal contract."""
    case_split = _c6_case_split()
    ft8 = _ft8_neighbours()
    c6_ids = {case["case_id"] for case in case_split["scoring_gated"]}
    dual_target_neighbour = sorted(c6_ids & set(ft8["passes_cases_union"]))
    return {
        "task": "T-V3-P4-C6-PRE",
        "generated": "2026-07-05",
        "mode": "DISCLOSE only (read-only pre-author; no wiring, no score move)",
        "purpose": (
            "Instance the frozen reveal contract for C6 — sensor fault "
            "under-detection. Surfaces SensorDynamicsState gates, consumer "
            "mapping, C3 interaction, 14-case split, live FT-8 neighbours, "
            "confounders, and baseline pin."
        ),
        "reveal_contract_template": REVEAL_SECTIONS,
        "baseline": {
            "yardstick": "V3_YARDSTICK_2026-07-05-C3B",
            "csv_hash": "9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283",
            "oracle_hash": "3088a7c3",
            "scorer": "apps/wired/v7/run_suite.py (hash-locked, untouched)",
            "named_run": "POST_T_V3_P4_C3B",
            "run_dir": "apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json",
            "note": (
                "All C6 sizing references this current post-C3B baseline. If any "
                "commit lands first, stop and re-pin before C6-SYNTH/C6A."
            ),
        },
        "c6_instance": {
            "cluster": "C6",
            "title": "sensor fault under-detection",
            "research_source": "v3/research/research_answers/cluster6.md",
            "producer": {
                "states": ["OBDLab SensorDynamicsState"],
                "emit_condition": (
                    "Emit O2_LAZY_OR_BIASED from decisive Mode $06 or active O2 "
                    "response evidence; emit MAF_UNDERREAD from sustained 10-15% "
                    "actual-vs-calculated shortfall at idle and 2500; emit "
                    "SENSOR_HEALTH_UNPROVEN_ABSTAIN for static-only evidence."
                ),
                "thresholds": C6_PRODUCER_THRESHOLDS,
                "corpus_columns": C6_COLUMNS,
            },
            "consumer": {
                "sensor_fault": {
                    "file": "labs/comlab/registry/rules/sensor_fault.json",
                    "rules": ["SF-005", "SF-008", "SF-001", "SF-002"],
                    "reads": (
                        "SF-005/SF-008 consume dynamic O2/MAF evidence; SF-001/SF-002 "
                        "consume bias/perception fields and must obey C3 interaction precedence."
                    ),
                    "evidence_fields": C6_COLUMNS,
                },
                "no_fault": {
                    "file": "labs/comlab/registry/rules/no_fault.json",
                    "rules": ["NF-001", "NF-002"],
                    "reads": (
                        "Healthy-vs-under-detected split reads decisive no-fault evidence: "
                        "wide Mode $06 margin, normal response timing, and no sustained MAF shortfall."
                    ),
                    "evidence_fields": C6_COLUMNS,
                },
            },
            "c3_interaction": C3_INTERACTION,
            "case_split": case_split,
            "ft8_neighbours": ft8,
            "dual_target_and_neighbour": dual_target_neighbour,
            "confounder_disclosure": {
                "confounders": C6_CONFOUNDERS,
                "mimic_risk_per_case": _mimic_risk(case_split),
                "c4_dependency": (
                    "C4B consumes the C6 O2/MAF dynamics columns; landing C6 unblocks "
                    "half of C4B's column ask but does not itself decide C4."
                ),
            },
            "grounding_strength": _grounding_strength_table(),
            "code_landed_neq_score_moved": (
                "The C6 producer emit rule + consumer map are BUILDABLE_NOW from "
                "cluster6.md and unit-testable on synthetic SensorDynamicsState "
                "vectors. That is CODE_LANDED. SCORE_MOVED on these 14 cannot be "
                "shown until owner/synthetic C6 values exist; the two must never be conflated."
            ),
            "abstain_fallback": (
                "If only static O2/MAF values are supplied, the case stays abstained "
                "at MARGIN=0.02. Dynamic inconsistency is the separator for C6."
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
    """Render the human-readable C6 reveal report."""
    c6 = contract["c6_instance"]
    base = contract["baseline"]
    case_split = c6["case_split"]
    ft8 = c6["ft8_neighbours"]
    lines: list[str] = [
        "# V3_C6_REVEAL_CONTRACT_2026-07-05",
        "",
        "**Task:** `T-V3-P4-C6-PRE`  **Mode:** DISCLOSE only (read-only pre-author)",
        "**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no",
        "**Machine-readable twin:** `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json`",
        "(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c6_contract.py`).",
        "",
        "This document instances the frozen reveal contract for **C6 — sensor fault under-detection**,",
        "the next pack in the pinned sequence (C2 → C3 → **C6** → C5 → C4 → …).",
        "It builds nothing and scores nothing; it fixes how C6 discloses thresholds, consumers,",
        "C3 interaction, FT-8 exposure, and stay-abstained cases.",
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
            "## 2. C6 producer extraction (cited to `cluster6.md`)",
            "",
            "The C6 producer is **OBDLab `SensorDynamicsState`**. It emits",
            "`O2_LAZY_OR_BIASED`, `MAF_UNDERREAD`, or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.",
            "The emit thresholds, transcribed read-only from the research answer:",
            "",
            "| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for threshold in c6["producer"]["thresholds"]:
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
            "**Producer emit summary:** `O2_LAZY_OR_BIASED` requires decisive dynamic",
            "O2 evidence (Mode $06 margin or active response timing); `MAF_UNDERREAD`",
            "requires sustained >10–15% measured-MAF shortfall versus modeled airflow at",
            "both warm idle and 2500 rpm; static-only O2/MAF values produce",
            "`SENSOR_HEALTH_UNPROVEN_ABSTAIN`, not a guessed pass/fail.",
            "",
            "**Load-bearing subset to size in C6A:** Mode $06 margin + the two MAF delta",
            "columns may be enough for many rows; exact rich↔lean millisecond columns are",
            "stronger when Mode $06 is absent/equivocal. C6A must ladder these scenarios",
            "instead of committing all 9 columns blindly.",
            "",
            "---",
            "",
            "## 3. C6 consumer mapping (named; no edit)",
            "",
            "| Family file | Rules | Field each would read | What the C6 state supplies |",
            "| --- | --- | --- | --- |",
            "| `sensor_fault.json` | **SF-005 / SF-008 / SF-001 / SF-002** | "
            "`mode06_o2_response_margin_pct`, `o2_rich_to_lean_ms`, "
            "`o2_lean_to_rich_ms`, MAF actual-vs-calculated deltas and source g/s columns | "
            "Dynamic sensor under-detection evidence: lazy/biased O2 or under-reading MAF. |",
            "| `no_fault.json` | **NF-001 / NF-002** | Same C6 columns, but healthy margins/response/no-MAF-shortfall | "
            "Healthy-vs-under-detected split; protects clean rows from false sensor-fault boosts. |",
            "",
            "Nothing is edited here. The consumer map is for C6-SYNTH/C6A/C6B inheritance.",
            "",
            "---",
            "",
            "## 4. C3-INTERACTION DISCLOSURE (mandatory)",
            "",
            "The live C3B shim now has a control-reference state and a prune/boost branch:",
            "",
            f"- Producer: `{C3_INTERACTION['live_c3_reader']}` returns "
            "`CONTROL_REFERENCE_FAULT` from KOEO MAP/BARO, ground drop, and loaded-voltage gates.",
            f"- Effect: {C3_INTERACTION['live_c3_effect']}",
            f"- C6 future effect: {C3_INTERACTION['c6_future_effect']}",
            f"- Today: {C3_INTERACTION['column_population_today']}",
            "",
            "**Composition / precedence rule C6B must implement:**",
            C3_INTERACTION["required_precedence_for_c6b"],
            "",
            "This interaction is disclosed now because SF-001/SF-002 are in both surfaces:",
            "C3 prunes them when a control-reference fault is decisive; C6 may later boost",
            "sensor rules when sensor-dynamics evidence is decisive. Static-only C6 evidence",
            "must abstain and must not undo a C3 prune.",
            "",
            "---",
            "",
            "## 5. C6 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 14)",
            "",
            "**BUILDABLE_NOW-reachable by logic alone: 0**. Every C6 row is residual because",
            "its dynamic O2/MAF discriminator is absent from the live corpus; logic without",
            "values cannot move `top3_family`.",
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
            f"All cases require: `{_csv(C6_COLUMNS)}`. **3 + 6 + 5 = 14.** ✔",
            "",
            "**CODE_LANDED != SCORE_MOVED, stated for C6:** the SensorDynamicsState emit",
            "logic and consumer map above are buildable from `cluster6.md`; any top3_family",
            "delta is unobservable until C6-SYNTH/C6A provides values. A pack report must",
            "never present wiring as score movement.",
            "",
            "---",
            "",
            "## 6. REGRESSION / FT-8 neighbour set (derived live)",
            "",
            "A C6 consumer edit touches `sensor_fault.json` and `no_fault.json` — both",
            "competition groups. The commit must re-audit every case those rules currently",
            "pass for a regressed family. Union of `passes_cases` across all SF + NF rules =",
            f"**{ft8['passes_cases_count']} cases**:",
            "",
            "```",
            _csv(ft8["passes_cases_union"]),
            "```",
            "",
            f"**Dual target+neighbour cases ({len(c6['dual_target_and_neighbour'])}):** "
            f"{_csv(c6['dual_target_and_neighbour'])}.",
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
            "## 7. Confounder disclosure (C6)",
            "",
            "**Source:** `cluster6.md` §Question Three/Four Answers + acq-spec §C4.",
            "",
            "| Confounder | Mechanism | Cite |",
            "| --- | --- | --- |",
        ]
    )
    for confounder in c6["confounder_disclosure"]["confounders"]:
        lines.append(
            f"| **{confounder['confounder']}** | {confounder['mechanism']} | "
            f"{confounder['cite']} |"
        )
    lines.extend(
        [
            "",
            "**Per-case mimic risk:** C6-SYNTH must use oracle-fault separability, not",
            "current rank, to decide seed bands. `PDF-4G-05` is an explicit lookalike:",
            "oracle `misfire`, current `sensor_fault`; C6 must not back-solve it into a",
            "sensor pass. Sensor-vs-no_fault rows have high NF regression exposure.",
            "",
            f"**C4 dependency:** {c6['confounder_disclosure']['c4_dependency']}",
            "",
            "---",
            "",
            "## 8. Grounding-strength table per threshold",
            "",
            "| Signal | Threshold | Grounding | Feasibility Tier | Risk note |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in c6["grounding_strength"]:
        lines.append(
            f"| {item['signal']} | {item['threshold']} | **{item['grounding']}** | "
            f"{item['feasibility_tier']} | {item['risk_note']} |"
        )
    lines.extend(
        [
            "",
            "**Weakest-grounded threshold:** the MAF >10–15% actual-vs-calculated shortfall",
            "is empirical-inferred. The O2 monitor framework is stronger, but its numeric",
            "limit is vehicle-specific; do not launder example values such as 849 ms or <150 ms",
            "into a universal fleet threshold.",
            "",
            "---",
            "",
            "## 9. ABSTAIN_FALLBACK (C6)",
            "",
            "If only static O2/MAF values are supplied, the row **stays abstained** at",
            "MARGIN=0.02. C6 separates on dynamic inconsistency: Mode $06 monitor margin,",
            "active O2 response timing, or two-point MAF plausibility. One warm-idle static",
            "sensor value is not a discriminator.",
            "",
            "---",
            "",
            "## Provenance / guardrails",
            "",
            "- Read-only: no corpus column added, no producer/consumer wired, no rule/weight",
            "  edit, no yardstick mint, no synthesized values, no abstain-dial change",
            "  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No",
            "  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.",
            "- Sources: `v3/research/research_answers/cluster6.md`;",
            "  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C6/§C4;",
            "  `labs/comlab/registry/rules/sensor_fault.json`, `no_fault.json`;",
            "  `labs/comlab/registry/integration_shim.py` lines 540-569 for C3 interaction.",
            "- Governs `T-V3-P4-C6-SYNTH` → `C6A` → `C6B`.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    """Build and write the C6 reveal contract JSON + Markdown."""
    contract = build_contract()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(contract, fh, indent=2, sort_keys=False, ensure_ascii=False)
    OUT_MD.write_text(render_markdown(contract), encoding="utf-8")

    c6 = contract["c6_instance"]
    case_split = c6["case_split"]
    ft8 = c6["ft8_neighbours"]
    dual = c6["dual_target_and_neighbour"]
    print(f"C6 reveal contract written to {OUT_JSON} and {OUT_MD}")
    print(f"Total C6 cases: {case_split['total']}")
    print(f"  BUILDABLE_NOW: {case_split['buildable_now_count']}")
    print(f"  SCORING_GATED: {case_split['scoring_gated_count']}")
    print(f"  Bucket breakdown: {case_split['bucket_breakdown']}")
    print(f"  Expected family mix: {case_split['expected_family_mix']}")
    print(f"FT-8 touched families: {ft8['touched_families']}")
    print(f"FT-8 neighbour passes_cases union: {ft8['passes_cases_count']}")
    print(f"Dual target+neighbour: {len(dual)} — {dual}")
    print(f"Grounding-strength entries: {len(c6['grounding_strength'])}")


if __name__ == "__main__":
    main()
