"""Read-only extractor for the signal-pack REVEAL CONTRACT (T-V3-P4-C2-PRE).

Emits ``v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json``: the
cluster-agnostic reveal-contract template plus the worked **C2** instance
(producer thresholds cited to ``cluster2.md``, named consumer rules, the 22-case
BUILDABLE_NOW/SCORING_GATED split, and the FT-8 neighbour set derived live from
the two touched rule files).

This script is **read-only**: it reads the C2 acquisition contract, the research
answer, and the registry rule JSONs, and writes only under ``v3/reports/``. It
adds no corpus column, wires no producer/consumer, mutates no engine/lab/registry
state, synthesizes no per-case values, and mints no yardstick. See
``v3/v3_tasks/T-V3-P4-C2-PRE_reveal_contract.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

WS = Path(__file__).resolve().parent.parent
ACQ_JSON = WS / "v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
RICH_RULES = WS / "labs/comlab/registry/rules/rich_mixture.json"
CAT_RULES = WS / "labs/comlab/registry/rules/catalyst_failure.json"
OUT_JSON = WS / "v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json"

# The five mandatory reveal-contract sections every signal-pack task (C*A/C*B)
# must surface. Cluster-agnostic; one-line definition each.
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

# C2 producer emit thresholds, quoted with section/line cites into cluster2.md.
# Read-only transcription of the research answer; no value is invented here.
C2_PRODUCER_THRESHOLDS: list[dict[str, str]] = [
    {
        "signal": "Total Fuel Trim (STFT+LTFT)",
        "maneuver": "Curb idle, 60 s, 100 points",
        "threshold": "<= -10%",
        "verdict": "TRUE_RICH (rich fueling malfunction active)",
        "producer_state": "GASLab CatalystConversionState / rich producer",
        "cite": "cluster2.md Protocol step 4 + Quantitative Signatures (Fuel Trim, +/-10% Normal)",
    },
    {
        "signal": "Mode $06 O2 index ratio",
        "maneuver": "Steady-state downstream O2 switching",
        "threshold": "<= 0.20",
        "verdict": "catalyst PASS (healthy); high ratio => LOW_OSC_OR_HIGH_INDEX (deteriorated)",
        "producer_state": "OBDLab CatalystMonitorState",
        "cite": "cluster2.md Quantitative Signatures (Index Ratio <= 0.20 Pass)",
    },
    {
        "signal": "OSC lag dt_osc",
        "maneuver": "Fuel step-change (lean +6% 4.0 s -> rich -10% 3.0 s), transition at 0.45 V",
        "threshold": "dt_osc < 0.5 s",
        "verdict": "catalyst FAIL (low OSC / minimal delay)",
        "producer_state": "OBDLab CatalystMonitorState",
        "cite": "cluster2.md Quantitative Signatures (OSC/Lag dt_osc < 0.5 s Fail) + Protocol step 5",
    },
    {
        "signal": "Decel 5-gas sweep CO",
        "maneuver": "Deceleration 2500 rpm -> curb idle, continuous tailpipe CO",
        "threshold": "CO > 0.8%",
        "verdict": "catalyst FAIL (lazy/low conversion at idle enthalpy)",
        "producer_state": "GASLab CatalystConversionState",
        "cite": "cluster2.md Quantitative Signatures (5-Gas Sweep CO > 0.8% Fail) + Protocol step 6",
    },
    {
        "signal": "Pre-gate: misfire (MID $A2/$A7) or pending heater (P0135) codes",
        "maneuver": "Query DTCs before any catalyst read",
        "threshold": "present => INVALID read",
        "verdict": "ABSTAIN / repair-first (readings invalidated)",
        "producer_state": "pre-gate on both producers",
        "cite": "cluster2.md Diagnostic Acquisition Protocol step 1 (Architectural Pre-Gate)",
    },
]


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _ft8_neighbours() -> dict[str, Any]:
    """Derive the FT-8 neighbour set live from the two touched rule files.

    Returns the full rule roster of the ``rich_mixture`` and ``catalyst_failure``
    families (both competition groups the C2 consumer edit would touch) and the
    union of their ``passes_cases`` — the exact set a C2 commit must re-audit for
    a regressed family.
    """
    rules: list[dict[str, Any]] = []
    passes: set[str] = set()
    for fam_file in (RICH_RULES, CAT_RULES):
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
        "touched_families": ["rich_mixture", "catalyst_failure"],
        "touched_competition_groups": ["rich_mixture", "catalyst_failure"],
        "rules": rules,
        "passes_cases_union": sorted(passes),
        "passes_cases_count": len(passes),
    }


def _c2_case_split() -> dict[str, Any]:
    """Split the 22 C2 residual cases into BUILDABLE_NOW vs SCORING_GATED.

    Every C2 case is residual precisely because the discriminating column is
    absent from the corpus (that is why it could not be answered) — so all 22 are
    SCORING_GATED and 0 are code-reachable now. This function reads that split
    from the acquisition contract's per-case unlock table; it does not decide it.
    """
    acq = _load(ACQ_JSON)
    c2_cases = [c for c in acq["case_unlocks"] if c.get("cluster") == "C2"]
    scoring_gated = [
        {
            "case_id": c["case_id"],
            "bucket": c["bucket"],
            "expected_family": c["expected_family"],
            "predicted_family": c["predicted_family"],
            "required_columns": c["unlock_columns"],
        }
        for c in c2_cases
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
            "All 22 C2 cases are SCORING_GATED and 0 are BUILDABLE_NOW-reachable: "
            "the discriminating columns (fuel trims + Mode $06 catalyst) are "
            "absent from the corpus by construction, which is why these rows are "
            "residual. Producer/consumer LOGIC is fully buildable now; the "
            "top3_family DELTA is not observable until the owner supplies values."
        ),
    }


def build_contract() -> dict[str, Any]:
    """Assemble the machine-readable reveal contract + C2 worked instance."""
    return {
        "task": "T-V3-P4-C2-PRE",
        "generated": "2026-07-01",
        "mode": "DISCLOSE only (read-only pre-author; no wiring, no score move)",
        "purpose": (
            "Freeze the cluster-agnostic reveal contract every signal-pack task "
            "(T-V3-P4-C*A / C*B) inherits, and resolve research(=logic)-vs-"
            "data(=per-case values) on the worked C2 instance."
        ),
        "reveal_contract_template": REVEAL_SECTIONS,
        "c2_instance": {
            "cluster": "C2",
            "title": "rich_mixture vs catalyst_failure",
            "research_source": "v3/research/research_answers/cluster2.md",
            "producer": {
                "states": ["GASLab CatalystConversionState", "OBDLab CatalystMonitorState"],
                "thresholds": C2_PRODUCER_THRESHOLDS,
            },
            "consumer": {
                "rich_mixture": {
                    "file": "labs/comlab/registry/rules/rich_mixture.json",
                    "rules": ["RM-001", "RM-003", "RM-004"],
                    "reads": "obd_evidence longft1/shrtft1 (fuel trims); the C2 TRUE_RICH "
                    "producer state would gate/confirm these negative-trim rules.",
                },
                "catalyst_failure": {
                    "file": "labs/comlab/registry/rules/catalyst_failure.json",
                    "rules": ["CF-001", "CF-002", "CF-006", "CF-007"],
                    "reads": "chemistry_evidence CATALYST_OVERWHELMED/NORMAL_OPERATION + "
                    "obd_evidence; the C2 LOW_OSC_OR_HIGH_INDEX producer state would "
                    "supply the catalyst-health discriminator these rules currently "
                    "infer from tailpipe chemistry alone.",
                },
            },
            "case_split": _c2_case_split(),
            "ft8_neighbours": _ft8_neighbours(),
            "code_landed_neq_score_moved": (
                "The C2 producer emit rule + consumer wiring are BUILDABLE_NOW from "
                "cluster2.md and unit-testable on synthetic trim/Mode-$06 vectors. "
                "That is CODE_LANDED. SCORE_MOVED (any top3_family delta on the 22) "
                "cannot be shown until the owner supplies real column values; the two "
                "must never be conflated in a pack report."
            ),
            "abstain_fallback": (
                "If Mode $06 catalyst data and fuel trims are absent for a case, it "
                "stays abstained at MARGIN=0.02; a single downstream tailpipe snapshot "
                "is not a discriminator."
            ),
        },
        "owner_next_task_fork": {
            "option_i": {
                "label": "Build C2 producer/consumer code now (scoring deferred)",
                "does": "Author + unit-test the C2 producer emit rule and consumer wiring "
                "on synthetic vectors; land BUILDABLE_NOW logic; leave all 22 cases "
                "abstained until data arrives.",
                "cost": "Engine/registry code churn now that moves no score yet; risk of "
                "the logic drifting from the eventual real-data thresholds.",
                "benefit": "Commit path is pre-validated; when C2 data lands only the "
                "scoring/FT-8 step remains.",
            },
            "option_ii": {
                "label": "Hold all pack code until C2 data lands",
                "does": "Write no producer/consumer code until the owner supplies the 22 "
                "cases' trim + Mode $06 values; then run C2A dry-run -> C2B commit.",
                "cost": "No forward progress on C2 until the owner-data wall clears.",
                "benefit": "Thresholds are calibrated against real values, not research "
                "defaults; zero speculative code.",
            },
            "decision": "OWNER DECIDES — not chosen here.",
        },
    }


def main() -> None:
    contract = build_contract()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as fh:
        json.dump(contract, fh, indent=2)
        fh.write("\n")
    split = contract["c2_instance"]["case_split"]
    ft8 = contract["c2_instance"]["ft8_neighbours"]
    print(f"wrote {OUT_JSON.relative_to(WS)}")
    print(
        f"C2: {split['total']} cases -> "
        f"{split['buildable_now_count']} BUILDABLE_NOW / "
        f"{split['scoring_gated_count']} SCORING_GATED "
        f"({split['bucket_breakdown']})"
    )
    print(f"FT-8 neighbour passes_cases union: {ft8['passes_cases_count']}")


if __name__ == "__main__":
    main()
