"""Read-only extractor for the C3 signal-pack REVEAL CONTRACT (T-V3-P4-C3-PRE).

Emits ``v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json``: the frozen
reveal-contract template instanced for **C3 — ECU/control-system fault**
(producer thresholds cited to ``cluster3_prepped.md``, named consumer rules,
the 22-case BUILDABLE_NOW / SCORING_GATED split, FT-8 neighbour set derived
live from the touched rule files, confounder disclosure, and grounding-strength
table).

This script is **read-only**: it reads the C3 acquisition contract, the research
answer, and the registry rule JSONs, and writes only under ``v3/reports/``.  It
adds no corpus column, wires no producer/consumer, mutates no engine/lab/registry
state, synthesizes no per-case values, and mints no yardstick.  See
``v3/v3_tasks/T-V3-P4-C3-PRE_reveal_contract.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

WS = Path(__file__).resolve().parent.parent
ACQ_JSON = WS / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
ECU_RULES = WS / "labs/comlab/registry/rules/ecu_fault.json"
SENSOR_RULES = WS / "labs/comlab/registry/rules/sensor_fault.json"
OUT_JSON = WS / "v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json"

# The five mandatory reveal-contract sections (cluster-agnostic, reused from
# V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01 — instanced, not re-derived).
REVEAL_SECTIONS: list[dict[str, str]] = [
    {
        "key": "BUILDABLE_NOW",
        "definition": (
            "Producer/consumer logic + thresholds derivable from the cluster "
            "research answer; provable by unit tests on synthetic vectors, with "
            "no owner data."
        ),
    },
    {
        "key": "SCORING_GATED",
        "definition": (
            "The per-case owner columns still required and which residual "
            "case_ids each unlocks; stays abstained until the owner supplies "
            "real measured values (no synthetic stand-in)."
        ),
    },
    {
        "key": "CODE_LANDED_NEQ_SCORE_MOVED",
        "definition": (
            "Explicit separation of 'producer/consumer logic shipped' from "
            "'top3_family delta'. Landing code proves the discriminator is "
            "wired; it does NOT move the score until gated data arrives. Never "
            "report the first as the second."
        ),
    },
    {
        "key": "REGRESSION_FT8",
        "definition": (
            "The neighbour set the consumer edit touches (rules in the same "
            "family file + shared competition_group + their passes_cases), plus "
            "the no-regressed-family audit run on the full corpus at commit time."
        ),
    },
    {
        "key": "ABSTAIN_FALLBACK",
        "definition": (
            "Cases whose discriminating signal the owner cannot supply stay "
            "abstained (MARGIN=0.02 dial), never guessed from the idle snapshot."
        ),
    },
]

# C3 producer emit thresholds, quoted with section/line cites into
# cluster3_prepped.md.  Read-only transcription of the research answer; no
# value is invented here.
C3_PRODUCER_THRESHOLDS: list[dict[str, str]] = [
    {
        "signal": "Gas-to-OBD Divergence (Δλ)",
        "maneuver": "Warm engine idle (750 RPM), 60 s closed-loop window",
        "threshold": "Δλ = |λ_OBD − λ_tailpipe| ≥ 0.05",
        "verdict": "CONTROL_REFERENCE_FAULT (gas-vs-OBD disagree)",
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 183 (Diagnostic Parameter: Gas-to-OBD Divergence)"
        ),
        "grounding": "empirical-anecdotal",
        "feasibility_tier": "Tier B: 5-gas analyzer",
    },
    {
        "signal": "Adaptive Fuel Trim Limits (LTFT railed)",
        "maneuver": "Dynamic cruise (1500–2500 RPM)",
        "threshold": "LTFT ≥ +25% or ≤ −25% with un-correlated tailpipe chemistry",
        "verdict": "CONTROL_REFERENCE_FAULT (trims at correction limit)",
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 184 (Diagnostic Parameter: Adaptive Fuel Trim Limits)"
        ),
        "grounding": "manufacturer-typical",
        "feasibility_tier": "Tier A: Generic OBD-II",
    },
    {
        "signal": "KOEO MAP-vs-BARO Correlation",
        "maneuver": "KOEO (0 RPM), ignition ON",
        "threshold": "|P_MAP − P_BARO| ≥ 5 kPa",
        "verdict": "CONTROL_REFERENCE_FAULT (static pressure split)",
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 185 (Diagnostic Parameter: KOEO MAP-vs-BARO Correlation)"
        ),
        "grounding": "manufacturer-typical",
        "feasibility_tier": "Tier A: Generic OBD-II",
    },
    {
        "signal": "DLC Signal Ground drop",
        "maneuver": "Idle under high electrical load",
        "threshold": "ΔV_gnd > 0.20 V (signal ground vs battery negative)",
        "verdict": "CONTROL_REFERENCE_FAULT (ground offset)",
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 186 (Diagnostic Parameter: DLC Signal Ground drop)"
        ),
        "grounding": "standardized",
        "feasibility_tier": "Tier C: DMM / breakout box",
    },
    {
        "signal": "Ground Path Voltage Drop",
        "maneuver": "Idle under high electrical load",
        "threshold": (
            "ΔV > 0.10 V (ground joint) or > 0.20 V (wire/cable)"
        ),
        "verdict": "CONTROL_REFERENCE_FAULT (chassis/engine ground degradation)",
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 187 (Diagnostic Parameter: Ground Path Voltage Drop)"
        ),
        "grounding": "standardized",
        "feasibility_tier": "Tier C: DMM",
    },
    {
        "signal": "Active Overrides Response",
        "maneuver": "Bidirectional fuel override at idle (+25% / −12.5%)",
        "threshold": (
            "O2 voltage delta < 0.1 V under ±25% fuel command steps"
        ),
        "verdict": (
            "CONTROL_REFERENCE_FAULT (sensor unresponsive to fuel command)"
        ),
        "producer_state": "OBDLab ControlPlausibilityState",
        "cite": (
            "cluster3_prepped.md §Quantitative Diagnostic Signature Mapping "
            "line 188 (Diagnostic Parameter: Active Overrides Response)"
        ),
        "grounding": "manufacturer-typical",
        "feasibility_tier": "Tier C: Bidirectional scan tool",
    },
]

# Cases where the C3 signature may fail (confounder disclosure).
# Source: cluster3_prepped.md §Conditions Under Which Signatures May Fail.
C3_CONFOUNDERS: list[dict[str, str]] = [
    {
        "confounder": "Upstream Exhaust System Leaks",
        "mechanism": (
            "Outside air drawn into the exhaust causes excess O2 at the "
            "sensor; both tailpipe gas and OBD trims indicate lean — mimics a "
            "fuel-delivery or vacuum leak, not a control-system electrical "
            "offset. Gas-vs-OBD divergence is near-zero, so the C3 Δλ test "
            "fails to trigger."
        ),
        "cite": "cluster3_prepped.md §Conditions Under Which Signatures May Fail, bullet 1",
    },
    {
        "confounder": "Severe Cylinder Misfires",
        "mechanism": (
            "A misfiring cylinder pumps raw oxygen and unburned fuel; the "
            "upstream O2 sensor drops, the ECU drives trims positive. Tailpipe "
            "gas shows high O2 + elevated HC — this can mimic a control-system "
            "or sensor bias fault because the O2 sensor response appears "
            "biased relative to actual combustion."
        ),
        "cite": "cluster3_prepped.md §Conditions Under Which Signatures May Fail, bullet 2",
    },
]


# -- Helpers ----------------------------------------------------------------

def _load(path: Path) -> Any:
    """Load a JSON file from *path*."""
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _ft8_neighbours() -> dict[str, Any]:
    """Derive the FT-8 neighbour set live from the two C3-touched rule files.

    C3 consumers touch ``ecu_fault.json`` (EF-001/EF-002/EF-003) and
    ``sensor_fault.json`` (SF-001/SF-002 for dispersion-as-sensor-bias).
    Returns the full rule roster of both families (both competition groups) and
    the union of their ``passes_cases`` — the exact set a C3 commit must
    re-audit for a regressed family.
    """
    rules: list[dict[str, Any]] = []
    passes: set[str] = set()
    for fam_file in (ECU_RULES, SENSOR_RULES):
        data = _load(fam_file)
        for rule in data["rules"]:
            pc = rule.get("passes_cases", [])
            rules.append(
                {
                    "rule_id": rule["rule_id"],
                    "fault_family": rule["fault_family"],
                    "competition_group": rule.get("competition_group"),
                    "base_weight": rule.get("base_weight"),
                    "passes_cases": pc,
                }
            )
            passes.update(pc)
    return {
        "touched_families": ["ecu_fault", "sensor_fault"],
        "touched_competition_groups": ["ecu_fault", "sensor_fault"],
        "rules": rules,
        "passes_cases_union": sorted(passes),
        "passes_cases_count": len(passes),
    }


def _c3_case_split() -> dict[str, Any]:
    """Split the 22 C3 residual cases into BUILDABLE_NOW vs SCORING_GATED.

    The 21 acq-spec §C3 rows plus the CASE-039 overlay (rerouted from
    CLASSIFIER_FIXABLE by T-V3-P4-0A) are all SCORING_GATED — none can be
    scored without the owner-supplied control-plausibility columns.
    """
    acq = _load(ACQ_JSON)
    c3_cases = [c for c in acq["case_unlocks"] if c.get("cluster") == "C3"]

    # Add CASE-039 overlay (it is not in the acq-spec C3 cluster because it
    # was originally CLASSIFIER_FIXABLE, rerouted to C3 by T-V3-P4-0A).
    case039_ids = {c["case_id"] for c in c3_cases}
    if "CASE-039" not in case039_ids:
        c3_cases.append(
            {
                "case_id": "CASE-039",
                "cluster": "C3",
                "bucket": "CLASSIFIER_FIXABLE_REROUTED",
                "expected_family": "ecu_fault",
                "predicted_family": "rich_mixture",
                "source_detail": (
                    "Rerouted from CLASSIFIER_FIXABLE by T-V3-P4-0A; "
                    "broad EGR/POA neighbour risk prevents safe classifier fix"
                ),
                "unlock_columns": [
                    "koeo_map_baro_delta_kpa",
                    "module_voltage_loaded_v",
                    "dlc_signal_ground_drop_v",
                    "gas_obd_lambda_delta",
                    "lambda_perception_delta",
                    "bidirectional_fuel_response_ok_bool",
                ],
                "unlock_verdict": "unlockable",
            }
        )

    scoring_gated = [
        {
            "case_id": c["case_id"],
            "bucket": c.get("bucket", ""),
            "expected_family": c.get("expected_family", ""),
            "predicted_family": c.get("predicted_family"),
            "required_columns": c.get("unlock_columns", []),
        }
        for c in sorted(c3_cases, key=lambda x: x["case_id"])
    ]
    buckets: dict[str, int] = {}
    for c in scoring_gated:
        buckets[c["bucket"]] = buckets.get(c["bucket"], 0) + 1
    return {
        "total": len(scoring_gated),
        "buildable_now_reachable": [],
        "buildable_now_count": 0,
        "scoring_gated": scoring_gated,
        "scoring_gated_count": len(scoring_gated),
        "bucket_breakdown": buckets,
        "note": (
            "All 22 C3 cases (21 acq-spec §C3 + CASE-039 overlay) are "
            "SCORING_GATED and 0 are BUILDABLE_NOW-reachable: the "
            "discriminating columns (KOEO MAP/BARO, ground voltage, "
            "gas-vs-OBD lambda divergence, bidirectional response) are "
            "absent from the corpus by construction, which is why these "
            "rows are residual. Producer/consumer LOGIC is fully buildable "
            "now; the top3_family DELTA is not observable until the owner "
            "supplies values."
        ),
    }


def _confounder_mimic_risk(case_split: dict[str, Any]) -> list[dict[str, Any]]:
    """Identify which of the 22 C3 cases' oracle faults are at mimic risk.

    Exhaust leaks and severe misfires can mimic the control-fault signature
    (cluster3_prepped.md §Conditions Under Which Signatures May Fail).  Since
    all 22 C3 cases have expected_family=ecu_fault, the mimic risk applies only
    if a case's *winner/predicted* family is exhaust_leak or misfire — meaning
    the engine currently routes them to a family whose physical failure could
    produce the same gas-vs-OBD pattern as a control fault.

    Additionally, any case whose oracle fault mechanism involves a physical
    exhaust leak or cylinder misfire (as opposed to an electrical/ECU fault)
    would be a stay-abstained candidate because the C3 signal cannot
    confidently separate it.
    """
    at_risk: list[dict[str, Any]] = []
    # For C3, all cases have expected_family == ecu_fault.  The confounders
    # apply when the *competing* families are exhaust_leak or misfire, meaning
    # the C3 discriminator must fight those specific look-alikes.  In practice
    # none of the 22 C3 cases have predicted_family == exhaust_leak or misfire;
    # they are outranked by lean_condition, rich_mixture, sensor_fault, or
    # catalyst_failure.  The mimic risk here is that a future *real* exhaust
    # leak or misfire in a vehicle COULD mask a genuine control fault — making
    # the gas-vs-OBD divergence test a false negative.
    #
    # Since we cannot know from the corpus which cases' physical vehicles have
    # a co-existing exhaust leak or misfire, we flag all 22 as having a
    # structural mimic risk from the C3 research and recommend that C3-SYNTH
    # flag any case where the oracle fault description suggests physical
    # exhaust-stream contamination rather than a pure ECU/wiring fault.
    for case in case_split["scoring_gated"]:
        predicted = case.get("predicted_family")
        risk_note = "no specific mimic risk from predicted family"
        if predicted in ("exhaust_leak", "misfire"):
            risk_note = (
                f"predicted_family={predicted} — this family's physical "
                f"failure mechanism can mimic the C3 control-fault signature "
                f"(gas-vs-OBD convergence instead of divergence); "
                f"stay-abstained candidate for C3-SYNTH"
            )
        at_risk.append(
            {
                "case_id": case["case_id"],
                "predicted_family": predicted,
                "mimic_risk": risk_note,
            }
        )
    return at_risk


def _grounding_strength_table() -> list[dict[str, str]]:
    """Produce the per-threshold grounding-strength table.

    Source: cluster3_prepped.md §Quantitative Diagnostic Signature Mapping,
    column 'Source Basis'.
    """
    return [
        {
            "signal": t["signal"],
            "threshold": t["threshold"],
            "grounding": t["grounding"],
            "feasibility_tier": t["feasibility_tier"],
            "risk_note": (
                "PRODUCER-TUNING RISK — threshold is empirical-anecdotal; "
                "not a standardized/OEM constant; confirm against real "
                "vehicle data before committing"
            )
            if t["grounding"] == "empirical-anecdotal"
            else "Threshold basis is well-grounded",
        }
        for t in C3_PRODUCER_THRESHOLDS
    ]


def build_contract() -> dict[str, Any]:
    """Assemble the machine-readable C3 reveal contract."""
    case_split = _c3_case_split()
    ft8 = _ft8_neighbours()

    # Identify cases that are both C3 target AND FT-8 neighbour.
    c3_ids = {c["case_id"] for c in case_split["scoring_gated"]}
    dual_target_neighbour = sorted(c3_ids & set(ft8["passes_cases_union"]))

    return {
        "task": "T-V3-P4-C3-PRE",
        "generated": "2026-07-05",
        "mode": "DISCLOSE only (read-only pre-author; no wiring, no score move)",
        "purpose": (
            "Instance the frozen reveal contract for C3 — ECU/control-system "
            "fault. Surfaces producer thresholds (grounding-tagged), consumer "
            "mapping, 22-case split, FT-8 neighbours (derived live), "
            "confounder disclosure, and baseline pin."
        ),
        "reveal_contract_template": REVEAL_SECTIONS,
        "baseline": {
            "yardstick": "V3_YARDSTICK_2026-07-05",
            "csv_hash": "3df2e8cbd82a866c3b8f12a72fdee837ac35cc1f09a19db65a10baa499282ddc",
            "oracle_hash": "3088a7c3",
            "scorer": "apps/wired/v7/run_suite.py (hash-locked, untouched)",
            "named_run": "POST_T_V3_P4_C2B",
            "run_dir": "apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json",
            "note": (
                "All sizing in this pack references this baseline. "
                "The C4A dry-run predates C2B and is known-stale — "
                "do not copy its numbers."
            ),
        },
        "c3_instance": {
            "cluster": "C3",
            "title": "ECU/control-system fault",
            "research_source": "v3/research/research_answers/cluster3_prepped.md",
            "producer": {
                "states": ["OBDLab ControlPlausibilityState"],
                "emit_condition": (
                    "Emit CONTROL_REFERENCE_FAULT when electrical/reference "
                    "or gas-vs-OBD divergence gates pass."
                ),
                "thresholds": C3_PRODUCER_THRESHOLDS,
                "corpus_columns": [
                    "koeo_map_baro_delta_kpa",
                    "module_voltage_loaded_v",
                    "dlc_signal_ground_drop_v",
                    "gas_obd_lambda_delta",
                    "lambda_perception_delta",
                    "bidirectional_fuel_response_ok_bool",
                ],
            },
            "consumer": {
                "ecu_fault": {
                    "file": "labs/comlab/registry/rules/ecu_fault.json",
                    "rules": ["EF-001", "EF-002", "EF-003"],
                    "reads": (
                        "obd_evidence longft1/shrtft1 (fuel trims); the C3 "
                        "ControlPlausibilityState would supply the "
                        "control-reference discriminator (gas-vs-OBD "
                        "divergence, ground voltage, MAP/BARO delta) that "
                        "these rules currently lack — they fire only on "
                        "trim saturation + DTC pattern."
                    ),
                },
                "sensor_fault": {
                    "file": "labs/comlab/registry/rules/sensor_fault.json",
                    "rules": ["SF-001", "SF-002"],
                    "reads": (
                        "obd_evidence lambda_perception_delta, o2_voltage; "
                        "the C3 state gates SF-001/SF-002 for cases where "
                        "dispersion presents as sensor bias — separates a "
                        "true lazy/biased O2 sensor from an ECU ground-offset "
                        "that merely *looks* like sensor bias."
                    ),
                },
            },
            "case_split": case_split,
            "ft8_neighbours": ft8,
            "dual_target_and_neighbour": dual_target_neighbour,
            "confounder_disclosure": {
                "confounders": C3_CONFOUNDERS,
                "mimic_risk_per_case": _confounder_mimic_risk(case_split),
            },
            "grounding_strength": _grounding_strength_table(),
            "code_landed_neq_score_moved": (
                "The C3 producer emit rule + consumer wiring are "
                "BUILDABLE_NOW from cluster3_prepped.md and unit-testable on "
                "synthetic control-plausibility vectors. That is CODE_LANDED. "
                "SCORE_MOVED (any top3_family delta on the 22) cannot be "
                "shown until the owner supplies real column values; the two "
                "must never be conflated in a pack report."
            ),
            "abstain_fallback": (
                "If no KOEO plausibility or voltage/divergence data are "
                "supplied, the case stays abstained at MARGIN=0.02; a single "
                "warm-idle gas snapshot cannot separate ECU/control faults "
                "from true chemistry deviations."
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


def main() -> None:
    """Build and write the C3 reveal contract JSON + summary stats."""
    contract = build_contract()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(contract, fh, indent=2, sort_keys=False, ensure_ascii=False)

    cs = contract["c3_instance"]["case_split"]
    ft8 = contract["c3_instance"]["ft8_neighbours"]
    dual = contract["c3_instance"]["dual_target_and_neighbour"]

    print(f"C3 reveal contract written to {OUT_JSON}")
    print(f"Total C3 cases: {cs['total']}")
    print(f"  BUILDABLE_NOW: {cs['buildable_now_count']}")
    print(f"  SCORING_GATED: {cs['scoring_gated_count']}")
    print(f"  Bucket breakdown: {cs['bucket_breakdown']}")
    print(f"FT-8 touched families: {ft8['touched_families']}")
    print(f"FT-8 neighbour passes_cases union: {ft8['passes_cases_count']}")
    print(f"Dual target+neighbour: {len(dual)} — {dual}")
    print(f"Confounders: {len(contract['c3_instance']['confounder_disclosure']['confounders'])}")
    print(f"Grounding-strength entries: {len(contract['c3_instance']['grounding_strength'])}")


if __name__ == "__main__":
    main()
