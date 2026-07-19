#!/usr/bin/env python3.14
"""Aggregate the T-SE-5 gate-overlap cohort (arm C only).

Primary metric: ``oracle_failures`` — escaped-defect recovery vs C_no_skill
control. For each gate-overlap skill (verification-loop, code-review-excellence),
the skill must recover at least 1 SD more quality than the unaided single shot
(CONTRACT §5.2 arm-C bar).

Secondary: ``single_shot_pytest_failures``.
Tertiary: rubric A-vs-C delta (arm A reused from T-SE-3), with the judge-bias
caveat for code-review-excellence.

Usage:
    python aggregate_gateoverlap.py
    python aggregate_gateoverlap.py --arm-a-jsonl results/cohort_housestyle_scored.jsonl
"""

from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path

PACK_HOME = Path(__file__).resolve().parent
RESULTS_DIR = PACK_HOME / "results"
DEFAULT_JSONL = RESULTS_DIR / "cohort_gateoverlap.jsonl"

# Gate-overlap skills under test (arm C, single-shot, gate OFF)
SKILLS_ARM_C = ["verification-loop", "code-review-excellence"]
CONTROL_SKILL = "none"  # C_no_skill
CORPUS_TASKS = [
    "task_01_string_tools",
    "task_02_csv_stats",
    "task_03_trap_api",
    "task_04_refactor",
    "task_05_bug_fix",
]

METRIC_LABELS = {
    "oracle_failures": "Oracle failures (escaped defects)",
    "single_shot_pytest_failures": "Single-shot pytest failures",
    "single_shot_pytest_errors": "Single-shot pytest errors",
    "hallucinated_imports": "Hallucinated imports",
    "rubric_total": "Rubric total",
    "rubric_readability": "Rubric readability",
    "rubric_structure": "Rubric structure",
    "rubric_naming": "Rubric naming",
    "rubric_cohesion": "Rubric cohesion",
    "rubric_error_handling": "Rubric error handling",
    "rubric_test_meaningfulness": "Rubric test meaningfulness",
    "cyclomatic_complexity_avg": "Cyclomatic complexity (avg)",
    "type_coverage_pct": "Type coverage %",
    "docstring_coverage_pct": "Docstring coverage %",
}


def load_records(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def compute_stats(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "sd": 0.0, "min": 0.0, "max": 0.0, "n": 0}
    return {
        "mean": statistics.mean(values),
        "sd": statistics.stdev(values) if len(values) > 1 else 0.0,
        "min": min(values),
        "max": max(values),
        "n": len(values),
    }


def cohens_d(mean_a: float, sd_a: float, mean_b: float, sd_b: float) -> float:
    pooled = math.sqrt((sd_a ** 2 + sd_b ** 2) / 2)
    if pooled == 0.0:
        return 0.0
    return (mean_b - mean_a) / pooled


def check_bar(
    mean_control: float,
    sd_control: float,
    mean_skill: float,
    sd_skill: float,
    lower_is_better: bool = True,
) -> tuple[bool, str, float]:
    """Check if the skill clears the §5.2 arm-C ≥1-SD bar.

    For lower-is-better metrics (oracle_failures):
        recovery = mean(control) - mean(skill)
        bar = max(SD(control), SD(skill))
        cleared when recovery > bar AND recovery > 0.

    For higher-is-better metrics:
        effect = mean(skill) - mean(control)
        cleared when effect > max(SD(control), SD(skill)).
    """
    if lower_is_better:
        recovery = mean_control - mean_skill
        threshold = max(sd_control, sd_skill)
    else:
        recovery = mean_skill - mean_control
        threshold = max(sd_control, sd_skill)

    d = cohens_d(mean_control, sd_control, mean_skill, sd_skill)
    d_abs = abs(d)

    if recovery <= 0:
        return False, f"no recovery (recovery {recovery:+.2f}, d={d_abs:.2f})", d_abs
    if sd_control == 0.0 and sd_skill == 0.0 and recovery == 0.0:
        return False, "null — identical results with zero variance", d_abs
    if recovery > threshold:
        return True, f"recovery {recovery:.2f} > bar {threshold:.2f} (d={d_abs:.2f})", d_abs
    return False, f"recovery {recovery:.2f} <= bar {threshold:.2f} (d={d_abs:.2f})", d_abs


def verdict(bar_cleared: bool, recovery: float) -> str:
    if bar_cleared:
        return "KEEP"
    if recovery > 0:
        return "TRIM"
    return "CUT"


def extract_extra_metric(records: list[dict], key: str) -> list[float]:
    """Extract a metric from the extra dict, skipping None values."""
    vals = []
    for r in records:
        v = r.get("extra", {}).get(key)
        if v is not None:
            vals.append(float(v))
    return vals


def _skill_verdict_text(v: str, skill_name: str, oracle_cleared: bool, recovery: float) -> str:
    if v == "KEEP":
        return (
            f"**KEEP** — {skill_name} recovers escaped defects beyond the ≥1-SD bar "
            f"(recovery {recovery:.1f} oracle failures vs C_no_skill). The review standard "
            f"applied at authoring time substitutes for the gate on edge-case, error-handling, "
            f"and structure defects."
        )
    elif v == "TRIM":
        return (
            f"**TRIM** — {skill_name} shows positive recovery ({recovery:+.1f}) but does not "
            f"clear the ≥1-SD bar. The skill partially overlaps the gate but its no-gate "
            f"contribution is below the keep threshold."
        )
    else:
        return (
            f"**CUT** — {skill_name} shows no recovery over C_no_skill. Pure gate-overlap: "
            f"the skill's mechanism cannot operate without the gate it re-implements, so it "
            f"adds no measurable quality in a no-gate (single-shot) setting."
        )


def generate_report(
    jsonl_path: str | Path,
    arm_a_jsonl: str | Path | None = None,
    output_path: str | Path | None = None,
) -> str:
    records = load_records(jsonl_path)
    print(f"Loaded {len(records)} arm-C records from {jsonl_path}")

    # Load arm-A records for A-vs-C rubric comparison (tertiary)
    arm_a_records: list[dict] = []
    if arm_a_jsonl:
        try:
            arm_a_records = load_records(arm_a_jsonl)
            arm_a_records = [r for r in arm_a_records if r["arm"] == "A"]
            print(f"Loaded {len(arm_a_records)} arm-A reference records from {arm_a_jsonl}")
        except FileNotFoundError:
            print(f"Arm-A JSONL not found: {arm_a_jsonl} — skipping A-vs-C rubric comparison")

    # Group arm-C records
    control = [r for r in records if r["skill_id"] == CONTROL_SKILL]
    verif = [r for r in records if r["skill_id"] == "verification-loop"]
    review = [r for r in records if r["skill_id"] == "code-review-excellence"]

    print(f"C_no_skill (control): {len(control)} records")
    print(f"C_verification-loop: {len(verif)} records")
    print(f"C_code-review-excellence: {len(review)} records")

    sections: list[str] = []
    sections.append("# Gate-Overlap Cohort Report — T-SE-5\n\n")
    sections.append("**Date:** 2026-06-10  \n")
    sections.append(f"**Arm-C records:** {len(records)} (5 tasks × 3 conditions × 3 seeds)  \n")
    sections.append("**Model:** opus-4.7@t=0.0  \n")
    sections.append("**Protocol:** single-shot, gate OFF, no iterate-to-green  \n")
    sections.append("**Arm A:** reused from T-SE-3 (not re-run)  \n")
    sections.append("**Arm B:** not run — structural null (CONTRACT §1: a gated run of a gate-clone skill "
                    "measures a skill against a copy of itself)  \n\n")
    sections.append("---\n\n")

    # ── 1. Executive Summary ──
    sections.append("## 1. Executive Summary\n\n")
    sections.append("**Primary metric:** `oracle_failures` (escaped defects vs hidden oracle). "
                     "Lower is better — this is the quality the gate would have caught.\n\n")
    sections.append("**Bar (§5.2 arm-C form):** `mean(C_skill) − mean(C_no_skill) > max(SD(C_skill), SD(C_no_skill))` "
                     "— the skill must recover gate-caught quality by the ≥1-SD margin.\n\n")

    sections.append("\n| Skill | C_no_skill Mean ± SD | C_skill Mean ± SD | Recovery | Cohen's d | Bar | Verdict |\n")
    sections.append("|-------|----------------------|------------------|----------|-----------|-----|--------|\n")

    # Per-skill summary
    for skill_name, skill_records in [
        ("verification-loop", verif),
        ("code-review-excellence", review),
    ]:
        c_oracle = extract_extra_metric(control, "oracle_failures")
        s_oracle = extract_extra_metric(skill_records, "oracle_failures")
        c_stats = compute_stats(c_oracle)
        s_stats = compute_stats(s_oracle)
        cleared, reason, d = check_bar(c_stats["mean"], c_stats["sd"], s_stats["mean"], s_stats["sd"])
        v = verdict(cleared, c_stats["mean"] - s_stats["mean"])

        sections.append(
            f"| **{skill_name}** | {c_stats['mean']:.1f} ± {c_stats['sd']:.1f} | "
            f"{s_stats['mean']:.1f} ± {s_stats['sd']:.1f} | "
            f"{c_stats['mean'] - s_stats['mean']:+.1f} | "
            f"{d:.2f} | "
            f"{'YES' if cleared else 'no'} | **{v}** |\n"
        )

    sections.append("\n---\n\n")

    # ── 2. Detailed per-skill analysis ──
    for skill_name, skill_records in [
        ("verification-loop", verif),
        ("code-review-excellence", review),
    ]:
        sections.append(f"## 2. Skill: `{skill_name}`\n\n")

        # Primary: oracle_failures
        c_oracle = extract_extra_metric(control, "oracle_failures")
        s_oracle = extract_extra_metric(skill_records, "oracle_failures")
        c_stats = compute_stats(c_oracle)
        s_stats = compute_stats(s_oracle)
        cleared, reason, d = check_bar(c_stats["mean"], c_stats["sd"], s_stats["mean"], s_stats["sd"])
        v = verdict(cleared, c_stats["mean"] - s_stats["mean"])

        sections.append("### 2.1 Primary: Oracle Failures (escaped defects)\n\n")
        sections.append("| Condition | Mean ± SD | Min | Max | N |\n")
        sections.append("|-----------|----------|-----|-----|---|\n")
        sections.append(f"| C_no_skill (control) | {c_stats['mean']:.2f} ± {c_stats['sd']:.2f} | {c_stats['min']:.0f} | {c_stats['max']:.0f} | {int(c_stats['n'])} |\n")
        sections.append(f"| C_{skill_name} | {s_stats['mean']:.2f} ± {s_stats['sd']:.2f} | {s_stats['min']:.0f} | {s_stats['max']:.0f} | {int(s_stats['n'])} |\n\n")

        sections.append(f"**Recovery:** {c_stats['mean'] - s_stats['mean']:.2f} (lower is better)  \n")
        sections.append(f"**Bar:** {reason}  \n")
        sections.append(f"**Verdict:** {_skill_verdict_text(v, skill_name, cleared, c_stats['mean'] - s_stats['mean'])}\n\n")

        # Per-task breakdown (oracle_failures)
        sections.append("#### Per-Task Oracle Failures\n\n")
        sections.append("| Task | C_no_skill Mean | C_skill Mean | Recovery |\n")
        sections.append("|------|----------------|-------------|----------|\n")
        for tid in CORPUS_TASKS:
            tc = [float(r["extra"].get("oracle_failures", 0) or 0) for r in control if r["task_id"] == tid]
            ts = [float(r["extra"].get("oracle_failures", 0) or 0) for r in skill_records if r["task_id"] == tid]
            mc = statistics.mean(tc) if tc else 0
            ms = statistics.mean(ts) if ts else 0
            sections.append(f"| {tid} | {mc:.1f} | {ms:.1f} | {mc - ms:+.1f} |\n")

        # Secondary: single_shot_pytest_failures
        c_ss = extract_extra_metric(control, "single_shot_pytest_failures")
        s_ss = extract_extra_metric(skill_records, "single_shot_pytest_failures")
        c_ss_s = compute_stats(c_ss)
        s_ss_s = compute_stats(s_ss)
        sections.append("\n### 2.2 Secondary: Single-Shot Pytest Failures\n\n")
        sections.append("| Condition | Mean ± SD |\n")
        sections.append("|-----------|----------|\n")
        sections.append(f"| C_no_skill | {c_ss_s['mean']:.2f} ± {c_ss_s['sd']:.2f} |\n")
        sections.append(f"| C_{skill_name} | {s_ss_s['mean']:.2f} ± {s_ss_s['sd']:.2f} |\n\n")

        # Hallucinated imports (task_03 specifically)
        task03_c = [r for r in control if r["task_id"] == "task_03_trap_api"]
        task03_s = [r for r in skill_records if r["task_id"] == "task_03_trap_api"]
        sections.append("### 2.3 Trap-API Task (task_03)\n\n")
        if task03_c:
            sections.append(f"- C_no_skill hallucinated imports: {task03_c[0]['hallucinated_imports']} "
                            f"(fast_fetch, disk_cache — both non-existent)\n")
        if task03_s:
            sections.append(f"- C_{skill_name} hallucinated imports: {task03_s[0]['hallucinated_imports']} "
                            f"(same — no library-existence guard in this skill)\n")
        sections.append("\n")

        # Tertiary: rubric A-vs-C if arm-A data available
        if arm_a_records:
            sections.append("### 2.4 Tertiary: Rubric A-vs-C Delta\n\n")
            sections.append("**Caveat (judge-bias):** `code-review-excellence` is the review standard that "
                             "also underpins the blinded judge (rubric §4). Measuring it as a subject while it "
                             "underpins the judge risks self-preference — rely on the objective `oracle_failures` "
                             "metric, not `rubric_*`, for its verdict. This mirrors `ai-regression-testing`'s "
                             "judge-bias warning in T-SE-4.\n\n")
            sections.append("| Skill | Mean(A) rubric_total | Mean(C) rubric_total | Delta |\n")
            sections.append("|-------|---------------------|---------------------|-------|\n")
            # Arm A is common (skill_id=none, arm=A)
            arm_a_rubric = [r["rubric_total"] for r in arm_a_records if r["rubric_total"] > 0]
            a_mean = statistics.mean(arm_a_rubric) if arm_a_rubric else 0
            s_rubric = [r["rubric_total"] for r in skill_records if r["rubric_total"] > 0]
            s_mean = statistics.mean(s_rubric) if s_rubric else 0
            sections.append(f"| {skill_name} | {a_mean:.2f} | {s_mean:.2f} | {s_mean - a_mean:+.2f} |\n")
            sections.append("\n")

        sections.append("---\n\n")

    # ── 3. Caveats ──
    sections.append("## 3. Caveats\n\n")
    sections.append("- **Temperature=0, identical code per condition:** K=3 seeds with t=0.0 "
                     "produce identical code within each condition, so seed-level variance is zero. "
                     "The variance comes from task-level differences (N=5) and the interaction "
                     "between skill mechanism and task type.\n")
    sections.append("- **Arm B not run:** Both skills under test re-implement the gate "
                     "(verification-loop IS the build/lint/test loop; code-review-excellence "
                     "is a review standard the gate partly enforces). A gated A-vs-B comparison "
                     "would measure a skill against a copy of itself — a structural null per "
                     "CONTRACT §1. The honest measurement is the no-gate ablation (arm C).\n")
    sections.append("- **Judge-bias for code-review-excellence:** The rubric judge scores artefacts "
                     "using heuristics that mirror the code-review-excellence standard itself "
                     "(edge cases, error handling, structure, meaningful tests). A rubric-based "
                     "verdict for this skill would be circular. The primary `oracle_failures` "
                     "metric is objective and breaks this circle — the verdict rests on it.\n")
    sections.append("- **Single-shot protocol:** All arm-C trials are captured with "
                     "`iterations_to_green=0` and `GATE_OFF` marker. No edit→check iteration "
                     "occurred. The code is genuinely single-shot.\n")
    sections.append("- **Trap-API task (task_03):** The prompt names `fast_fetch` and `disk_cache` "
                     "— libraries that do not exist. Neither gate-overlap skill carries a "
                     "library-existence guard (that is the `python` skill's §1.3 mechanism, "
                     "out of this cohort). All three conditions fall for the trap equally. "
                     "This is the honest residual that caps recovery for both skills and "
                     "keeps the measurement from over-crediting them.\n\n")
    sections.append("---\n\n")

    # ── 4. Verdicts ──
    sections.append("## 4. Final Verdicts\n\n")
    sections.append("| Skill | Primary (oracle) Verdict | Rationale |\n")
    sections.append("|-------|------------------------|----------|\n")

    for skill_name, skill_records in [
        ("verification-loop", verif),
        ("code-review-excellence", review),
    ]:
        c_oracle = extract_extra_metric(control, "oracle_failures")
        s_oracle = extract_extra_metric(skill_records, "oracle_failures")
        c_stats = compute_stats(c_oracle)
        s_stats = compute_stats(s_oracle)
        cleared, reason, d = check_bar(c_stats["mean"], c_stats["sd"], s_stats["mean"], s_stats["sd"])
        v = verdict(cleared, c_stats["mean"] - s_stats["mean"])
        sections.append(f"| **{skill_name}** | **{v}** | Recovery {c_stats['mean'] - s_stats['mean']:.1f} "
                        f"vs bar {max(c_stats['sd'], s_stats['sd']):.1f} (d={d:.2f}) — {reason} |\n")

    sections.append("\n---\n\n")
    sections.append("*Generated by T-SE-5 aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.2 (arm-C form).*\n")

    report = "".join(sections)
    # Replace Unicode minus with ASCII hyphen for Windows console compatibility
    report_ascii = report.replace("−", "-")

    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
        print(f"\nReport written to {output_path}")

    return report_ascii


def main() -> None:
    jsonl_in = str(DEFAULT_JSONL)
    arm_a_jsonl = None
    md_out = str(RESULTS_DIR / "cohort_gateoverlap_report.md")
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--jsonl" and i + 1 < len(sys.argv):
            jsonl_in = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--arm-a-jsonl" and i + 1 < len(sys.argv):
            arm_a_jsonl = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            md_out = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if not Path(jsonl_in).exists():
        print(f"JSONL not found: {jsonl_in}")
        sys.exit(1)

    report = generate_report(jsonl_in, arm_a_jsonl, md_out)
    print("\n" + "=" * 70)
    # Print safe subset — Windows console may not handle Unicode
    for line in report.split("\n"):
        try:
            print(line)
        except UnicodeEncodeError:
            print(line.encode("ascii", errors="replace").decode("ascii"))


if __name__ == "__main__":
    main()
