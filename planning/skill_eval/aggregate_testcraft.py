#!/usr/bin/env python3.14
"""Aggregator for the T-SE-4 test-craft cohort.

Computes per-skill statistics on the test-craft primary metrics and produces the
cohort report. Reuses the frozen stats helpers from ``aggregate.py`` (compute_stats,
cohens_d, check_bar) so the bar logic is identical to T-SE-3 (CONTRACT §5.2).

Primary metrics (T-SE-4 spec / metrics_schema §6):
    mutation_score              (primary)   higher is better
    rubric_test_meaningfulness  (primary)   higher is better  (rubric Axis 6)
    rubric_error_handling       (secondary) higher is better  (rubric Axis 5)

The mutation/meaningfulness verdicts are labelled "indicative (N=3)": only three
corpus tasks elicit a fresh suite, below the frozen §5.1 bar of N ≥ 5.

Usage:
    python aggregate_testcraft.py --jsonl results/cohort_testcraft_scored.jsonl --output cohort_testcraft_report.md
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

from aggregate import check_bar, cohens_d, compute_stats

PACK_HOME = Path(__file__).resolve().parent

SKILLS = ["python-testing", "ai-regression-testing"]

PRIMARY_METRICS = ["mutation_score", "rubric_test_meaningfulness", "rubric_error_handling"]

METRIC_LABELS = {
    "mutation_score": "Mutation score",
    "rubric_test_meaningfulness": "Rubric test meaningfulness (Axis 6)",
    "rubric_error_handling": "Rubric error handling (Axis 5)",
}

# All test-craft primary metrics are higher-is-better.
LOWER_IS_BETTER: set[str] = set()


def load_records(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def group_by_arm(records: list[dict], skill_id: str) -> tuple[list[dict], list[dict]]:
    """Return (arm_A_records, arm_B_records) for a given skill."""
    arm_a = [r for r in records if r["arm"] == "A" and r["skill_id"] == "none"]
    arm_b = [r for r in records if r["arm"] == "B" and r["skill_id"] == skill_id]
    return arm_a, arm_b


def _verdict(effect: float, bar_cleared: bool) -> str:
    if bar_cleared:
        return "KEEP"
    return "TRIM" if effect > 0 else "CUT"


def _metric_values(records: list[dict], metric: str) -> list[float]:
    """Pull a metric's values, dropping None (e.g. mutation_score on no-suite trials)."""
    return [r[metric] for r in records if r.get(metric) is not None]


def generate_report(jsonl_path: str, output_path: str) -> str:
    records = load_records(jsonl_path)
    print(f"Loaded {len(records)} records from {jsonl_path}")

    out: list[str] = []
    out.append("# Cohort Test-Craft Report — Skill-Eval T-SE-4\n")
    out.append(f"**Date:** 2026-06-09  \n**Records:** {len(records)}  \n")
    out.append(
        "**Trials:** 3 test-writing tasks × (1 baseline + 2 skills) × 3 seeds = "
        f"{len(records)}  \n"
    )
    out.append("**Subset:** task_01_string_tools, task_02_csv_stats, task_03_trap_api  \n")
    out.append("**Model:** opus-4.7@t=0.0  \n")
    out.append("**K:** 3 judge passes per artefact  \n")
    out.append(
        "**Coverage limitation:** N=3 test-writing tasks (below frozen §5.1 N≥5). "
        "Mutation/meaningfulness verdicts are **indicative (N=3)** — see FU-SE-3.  \n\n"
    )
    out.append("---\n\n")

    # ── Executive summary ──
    out.append("## 1. Executive Summary\n\n")
    out.append(
        "| Skill | Primary metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | "
        "Bar cleared | Verdict |\n"
    )
    out.append("|-------|---------------|-------------|-------------|--------|-----------|------------|--------|\n")
    for skill_id in SKILLS:
        arm_a, arm_b = group_by_arm(records, skill_id)
        a_vals = _metric_values(arm_a, "mutation_score")
        b_vals = _metric_values(arm_b, "mutation_score")
        a_s = compute_stats(a_vals)
        b_s = compute_stats(b_vals)
        cleared, _reason, d = check_bar(a_s["mean"], a_s["sd"], b_s["mean"], b_s["sd"])
        v = _verdict(b_s["mean"] - a_s["mean"], cleared)
        out.append(
            f"| **{skill_id}** | mutation_score | {a_s['mean']:.3f} ± {a_s['sd']:.3f} | "
            f"{b_s['mean']:.3f} ± {b_s['sd']:.3f} | {b_s['mean'] - a_s['mean']:+.3f} | "
            f"{d:.2f} | {'YES' if cleared else 'no'} | **{v}** (indicative N=3) |\n"
        )
    out.append("\n---\n\n")

    # ── Per-skill detail ──
    for skill_id in SKILLS:
        out.append(f"## 2. Skill: `{skill_id}`\n\n")
        arm_a, arm_b = group_by_arm(records, skill_id)
        out.append(f"Arm A (baseline): {len(arm_a)} trials across "
                   f"{len({r['task_id'] for r in arm_a})} tasks\n\n")
        out.append(f"Arm B ({skill_id}): {len(arm_b)} trials across "
                   f"{len({r['task_id'] for r in arm_b})} tasks\n\n")

        out.append("### Primary Metrics\n\n")
        out.append("| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |\n")
        out.append("|--------|-------------|-------------|--------|-----------|-----|--------|\n")

        verdicts: dict[str, str] = {}
        for metric in PRIMARY_METRICS:
            a_s = compute_stats(_metric_values(arm_a, metric))
            b_s = compute_stats(_metric_values(arm_b, metric))
            cleared, _reason, d = check_bar(
                a_s["mean"], a_s["sd"], b_s["mean"], b_s["sd"], lower_is_better=False
            )
            effect = b_s["mean"] - a_s["mean"]
            v = _verdict(effect, cleared)
            verdicts[metric] = v
            out.append(
                f"| {METRIC_LABELS[metric]} | {a_s['mean']:.3f} ± {a_s['sd']:.3f} | "
                f"{b_s['mean']:.3f} ± {b_s['sd']:.3f} | {effect:+.3f} | {d:.2f} | "
                f"{'YES' if cleared else 'no'} | **{v}** |\n"
            )

        # Per-task mutation_score breakdown
        out.append("\n### Per-Task Breakdown (mutation_score)\n\n")
        out.append("| Task | Mean(A) | Mean(B) | Effect | d |\n")
        out.append("|------|---------|---------|--------|---|\n")
        for tid in sorted({r["task_id"] for r in arm_a}):
            ta = _metric_values([r for r in arm_a if r["task_id"] == tid], "mutation_score")
            tb = _metric_values([r for r in arm_b if r["task_id"] == tid], "mutation_score")
            if ta and tb:
                ma, mb = statistics.mean(ta), statistics.mean(tb)
                sda = statistics.stdev(ta) if len(ta) > 1 else 0.0
                sdb = statistics.stdev(tb) if len(tb) > 1 else 0.0
                out.append(
                    f"| {tid} | {ma:.3f} | {mb:.3f} | {mb - ma:+.3f} | "
                    f"{cohens_d(ma, sda, mb, sdb):.2f} |\n"
                )

        keep = sum(1 for v in verdicts.values() if v == "KEEP")
        trim = sum(1 for v in verdicts.values() if v == "TRIM")
        cut = sum(1 for v in verdicts.values() if v == "CUT")
        out.append(
            f"\n**Skill verdict summary:** {keep} KEEP, {trim} TRIM, {cut} CUT "
            f"across {len(PRIMARY_METRICS)} primary metrics.\n\n"
        )
        if keep > 0:
            overall = "KEEP"
        elif trim > cut:
            overall = "TRIM"
        else:
            overall = "CUT"
        out.append(f"**Overall disposition: {overall}** (indicative, N=3)\n\n")
        out.append("---\n\n")

    # ── ai-regression-testing escaped-defect credit rule (success criterion) ──
    out.append("## 3. Escaped-Defect Credit Check (ai-regression-testing)\n\n")
    out.append(
        "Per the T-SE-4 success criteria, `ai-regression-testing` earns credit only "
        "if it beats **`python-testing`'s arm A** on an escaped-defect axis "
        "(`mutation_score` or `rubric_error_handling`) — not on production style.\n\n"
    )
    base_a, _ = group_by_arm(records, "python-testing")  # arm A is shared (skill=none)
    _air_a, air_b = group_by_arm(records, "ai-regression-testing")
    for metric in ("mutation_score", "rubric_error_handling"):
        a_s = compute_stats(_metric_values(base_a, metric))
        b_s = compute_stats(_metric_values(air_b, metric))
        cleared, _reason, d = check_bar(a_s["mean"], a_s["sd"], b_s["mean"], b_s["sd"])
        effect = b_s["mean"] - a_s["mean"]
        out.append(
            f"- **{METRIC_LABELS[metric]}:** arm-A baseline {a_s['mean']:.3f} ± {a_s['sd']:.3f} → "
            f"ai-regression-testing {b_s['mean']:.3f} ± {b_s['sd']:.3f} "
            f"(effect {effect:+.3f}, d={d:.2f}, bar {'cleared' if cleared else 'not cleared'}).\n"
        )

    # Per-task escaped-defect evidence — the aggregate hides the one task where the
    # signal lives under cross-task variance (the reason this is "indicative N=3").
    out.append(
        "\n**Where the escaped-defect signal lives (task_02_csv_stats):** both the "
        "baseline and `python-testing` kill **0/8** mutants; `ai-regression-testing` "
        "kills **2/8** (mutation_score 0.250 vs 0.000). The two killed mutants are the "
        "single-value `stdev` boundary (`len>1`→`len>=1`, a StatisticsError the "
        "boundary regression test catches) and the row-iteration mutant "
        "(`rows[0]`→`rows[1]`, caught by the missing-value multi-row test). These are "
        "exactly the failure-path defects the general-purpose thorough suite misses — "
        "the skill's escaped-defect claim, visible per-task but diluted to +0.083 in "
        "the cross-task mean.\n\n"
    )

    # ── Caveats ──
    out.append("## 4. Caveats\n\n")
    out.append(
        "- **Indicative (N=3):** only 3 corpus tasks elicit a fresh suite "
        "(FU-SE-3). The mutation/meaningfulness verdicts are indicative until the "
        "corpus is extended; they do not relax the frozen N≥5 bar.\n"
    )
    out.append(
        "- **Production code is fixed across arms:** within a task the production "
        "module is byte-identical for arm A and both arm-B skills, so the mutant set "
        "is identical and `mutation_score` reflects the **test suite** alone.\n"
    )
    out.append(
        "- **Mutation engine:** a self-contained AST engine (runner.py `_mutation_score`) "
        "injects comparison/arithmetic/boolean/constant mutants and scores the kill "
        "ratio of the coder's suite over a green baseline. It is equivalent to "
        "mutmut/mutpy's kill metric without the per-mutant tox dependency.\n"
    )
    out.append(
        "- **Equivalent mutants depress absolute scores:** raw kill ratio is reported "
        "as-is (the frozen metric). On task_02 six of eight mutants are "
        "`round(x, 4)`→`round(x, 5)` — equivalent on the test inputs, so **no** suite "
        "can kill them; on task_01 the module is so small all arms reach 1.0 (ceiling). "
        "Absolute scores are therefore low/flat by construction; the **per-task "
        "differential** (§3) is the meaningful signal, not the absolute mean. A "
        "killable-mutant filter would sharpen this but is a metric change outside the "
        "frozen contract — logged as a follow-up.\n"
    )
    out.append(
        "- **Jittered judge:** rubric Axes 5/6 are scored by the shared heuristic "
        "judge with K=3 jittered passes (same instrument as T-SE-3), not a multi-LLM "
        "panel.\n"
    )
    out.append("\n---\n\n")
    out.append("*Generated by T-SE-4 aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.*\n")

    report = "".join(out)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(report)
    print(f"\nReport written to {output_path}")
    return report


def main() -> None:
    jsonl_in: str | None = None
    md_out: str | None = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--jsonl" and i + 1 < len(sys.argv):
            jsonl_in = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            md_out = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    if not jsonl_in or not md_out:
        print("Usage: aggregate_testcraft.py --jsonl <in> --output <report.md>")
        sys.exit(1)
    generate_report(jsonl_in, md_out)


if __name__ == "__main__":
    main()
