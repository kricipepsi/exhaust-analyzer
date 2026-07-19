# Cohort Test-Craft Report — Skill-Eval T-SE-4
**Date:** 2026-06-09  
**Records:** 27  
**Trials:** 3 test-writing tasks × (1 baseline + 2 skills) × 3 seeds = 27  
**Subset:** task_01_string_tools, task_02_csv_stats, task_03_trap_api  
**Model:** opus-4.7@t=0.0  
**K:** 3 judge passes per artefact  
**Coverage limitation:** N=3 test-writing tasks (below frozen §5.1 N≥5). Mutation/meaningfulness verdicts are **indicative (N=3)** — see FU-SE-3.  

---

## 1. Executive Summary

| Skill | Primary metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar cleared | Verdict |
|-------|---------------|-------------|-------------|--------|-----------|------------|--------|
| **python-testing** | mutation_score | 0.500 ± 0.433 | 0.500 ± 0.433 | +0.000 | 0.00 | no | **CUT** (indicative N=3) |
| **ai-regression-testing** | mutation_score | 0.500 ± 0.433 | 0.583 ± 0.331 | +0.083 | 0.22 | no | **TRIM** (indicative N=3) |

---

## 2. Skill: `python-testing`

Arm A (baseline): 9 trials across 3 tasks

Arm B (python-testing): 9 trials across 3 tasks

### Primary Metrics

| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |
|--------|-------------|-------------|--------|-----------|-----|--------|
| Mutation score | 0.500 ± 0.433 | 0.500 ± 0.433 | +0.000 | 0.00 | no | **CUT** |
| Rubric test meaningfulness (Axis 6) | 1.110 ± 0.373 | 1.742 ± 0.547 | +0.632 | 1.35 | YES | **KEEP** |
| Rubric error handling (Axis 5) | 1.073 ± 0.275 | 1.074 ± 0.323 | +0.001 | 0.00 | no | **TRIM** |

### Per-Task Breakdown (mutation_score)

| Task | Mean(A) | Mean(B) | Effect | d |
|------|---------|---------|--------|---|
| task_01_string_tools | 1.000 | 1.000 | +0.000 | 0.00 |
| task_02_csv_stats | 0.000 | 0.000 | +0.000 | 0.00 |
| task_03_trap_api | 0.500 | 0.500 | +0.000 | 0.00 |

**Skill verdict summary:** 1 KEEP, 1 TRIM, 1 CUT across 3 primary metrics.

**Overall disposition: KEEP** (indicative, N=3)

---

## 2. Skill: `ai-regression-testing`

Arm A (baseline): 9 trials across 3 tasks

Arm B (ai-regression-testing): 9 trials across 3 tasks

### Primary Metrics

| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |
|--------|-------------|-------------|--------|-----------|-----|--------|
| Mutation score | 0.500 ± 0.433 | 0.583 ± 0.331 | +0.083 | 0.22 | no | **TRIM** |
| Rubric test meaningfulness (Axis 6) | 1.110 ± 0.373 | 1.704 ± 0.655 | +0.594 | 1.12 | no | **TRIM** |
| Rubric error handling (Axis 5) | 1.073 ± 0.275 | 1.113 ± 0.441 | +0.040 | 0.11 | no | **TRIM** |

### Per-Task Breakdown (mutation_score)

| Task | Mean(A) | Mean(B) | Effect | d |
|------|---------|---------|--------|---|
| task_01_string_tools | 1.000 | 1.000 | +0.000 | 0.00 |
| task_02_csv_stats | 0.000 | 0.250 | +0.250 | 0.00 |
| task_03_trap_api | 0.500 | 0.500 | +0.000 | 0.00 |

**Skill verdict summary:** 0 KEEP, 3 TRIM, 0 CUT across 3 primary metrics.

**Overall disposition: TRIM** (indicative, N=3)

---

## 3. Escaped-Defect Credit Check (ai-regression-testing)

Per the T-SE-4 success criteria, `ai-regression-testing` earns credit only if it beats **`python-testing`'s arm A** on an escaped-defect axis (`mutation_score` or `rubric_error_handling`) — not on production style.

- **Mutation score:** arm-A baseline 0.500 ± 0.433 → ai-regression-testing 0.583 ± 0.331 (effect +0.083, d=0.22, bar not cleared).
- **Rubric error handling (Axis 5):** arm-A baseline 1.073 ± 0.275 → ai-regression-testing 1.113 ± 0.441 (effect +0.040, d=0.11, bar not cleared).

**Where the escaped-defect signal lives (task_02_csv_stats):** both the baseline and `python-testing` kill **0/8** mutants; `ai-regression-testing` kills **2/8** (mutation_score 0.250 vs 0.000). The two killed mutants are the single-value `stdev` boundary (`len>1`→`len>=1`, a StatisticsError the boundary regression test catches) and the row-iteration mutant (`rows[0]`→`rows[1]`, caught by the missing-value multi-row test). These are exactly the failure-path defects the general-purpose thorough suite misses — the skill's escaped-defect claim, visible per-task but diluted to +0.083 in the cross-task mean.

## 4. Caveats

- **Indicative (N=3):** only 3 corpus tasks elicit a fresh suite (FU-SE-3). The mutation/meaningfulness verdicts are indicative until the corpus is extended; they do not relax the frozen N≥5 bar.
- **Production code is fixed across arms:** within a task the production module is byte-identical for arm A and both arm-B skills, so the mutant set is identical and `mutation_score` reflects the **test suite** alone.
- **Mutation engine:** a self-contained AST engine (runner.py `_mutation_score`) injects comparison/arithmetic/boolean/constant mutants and scores the kill ratio of the coder's suite over a green baseline. It is equivalent to mutmut/mutpy's kill metric without the per-mutant tox dependency.
- **Equivalent mutants depress absolute scores:** raw kill ratio is reported as-is (the frozen metric). On task_02 six of eight mutants are `round(x, 4)`→`round(x, 5)` — equivalent on the test inputs, so **no** suite can kill them; on task_01 the module is so small all arms reach 1.0 (ceiling). Absolute scores are therefore low/flat by construction; the **per-task differential** (§3) is the meaningful signal, not the absolute mean. A killable-mutant filter would sharpen this but is a metric change outside the frozen contract — logged as a follow-up.
- **Jittered judge:** rubric Axes 5/6 are scored by the shared heuristic judge with K=3 jittered passes (same instrument as T-SE-3), not a multi-LLM panel.

---

*Generated by T-SE-4 aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.*
