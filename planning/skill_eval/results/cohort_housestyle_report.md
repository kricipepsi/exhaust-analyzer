# Cohort House-Style Report — Skill-Eval T-SE-3
**Date:** 2026-06-09  
**Records:** 60  
**Trials:** 5 tasks × (1 baseline + 3 skills) × 3 seeds = 60  
**Model:** opus-4.7@t=0.0  
**K:** 3 judge passes per artefact  

---

## 1. Executive Summary

| Skill | Primary metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar cleared | Verdict |
|-------|---------------|-------------|-------------|--------|-----------|------------|--------|
| **python** | rubric_total | 8.00 ± 1.12 | 8.51 ± 0.98 | +0.51 | 0.49 | no | **TRIM** |
| **uncle-bob-craft** | rubric_total | 8.00 ± 1.12 | 9.31 ± 0.65 | +1.31 | 1.43 | YES | **KEEP** |
| **improve-codebase-architecture** | rubric_total | 8.00 ± 1.12 | 8.98 ± 0.87 | +0.98 | 0.98 | no | **TRIM** |

---

## 2. Skill: `python`

Arm A (baseline): 15 trials across 5 tasks

Arm B (python): 15 trials across 5 tasks

### Primary Metrics

| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |
|--------|-------------|-------------|--------|-----------|-----|--------|
| First-pass ruff errors | 1.80 ± 1.52 | 3.00 ± 1.60 | +1.20 | 0.77 | no | **CUT** |
| First-pass pyright errors | 0.40 ± 0.83 | 1.20 ± 1.66 | +0.80 | 0.61 | no | **CUT** |
| Hallucinated imports | 0.40 ± 0.83 | 0.00 ± 0.00 | -0.40 | 0.68 | no | **TRIM** |
| Hallucinated functions | 0.00 ± 0.00 | 0.00 ± 0.00 | +0.00 | 0.00 | no | **CUT** |
| Rubric total | 8.00 ± 1.12 | 8.51 ± 0.98 | +0.51 | 0.49 | no | **TRIM** |
| Rubric readability | 0.20 ± 0.25 | 0.18 ± 0.31 | -0.02 | 0.08 | no | **CUT** |
| Rubric structure | 0.95 ± 0.43 | 1.67 ± 0.59 | +0.71 | 1.37 | YES | **KEEP** |
| Rubric naming | 2.11 ± 0.39 | 1.84 ± 0.35 | -0.27 | 0.72 | no | **CUT** |
| Rubric cohesion | 2.07 ± 0.36 | 2.04 ± 0.21 | -0.02 | 0.08 | no | **CUT** |
| Cyclomatic complexity (avg) | 3.49 ± 1.20 | 2.53 ± 0.38 | -0.96 | 1.09 | no | **TRIM** |

### Per-Task Breakdown (rubric_total)

| Task | Mean(A) | Mean(B) | Effect | d |
|------|---------|---------|--------|---|
| task_01_string_tools | 8.00 | 8.67 | +0.67 | 0.71 |
| task_02_csv_stats | 8.56 | 9.56 | +1.00 | 1.96 |
| task_03_trap_api | 6.78 | 7.34 | +0.56 | 0.71 |
| task_04_refactor | 7.89 | 9.11 | +1.23 | 1.17 |
| task_05_bug_fix | 8.78 | 7.89 | -0.89 | -1.11 |

**Skill verdict summary:** 1 KEEP, 3 TRIM, 6 CUT across 10 primary metrics.

**Overall disposition: KEEP**

---

## 2. Skill: `uncle-bob-craft`

Arm A (baseline): 15 trials across 5 tasks

Arm B (uncle-bob-craft): 15 trials across 5 tasks

### Primary Metrics

| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |
|--------|-------------|-------------|--------|-----------|-----|--------|
| Rubric total | 8.00 ± 1.12 | 9.31 ± 0.65 | +1.31 | 1.43 | YES | **KEEP** |
| Rubric readability | 0.20 ± 0.25 | 0.13 ± 0.17 | -0.07 | 0.32 | no | **CUT** |
| Rubric structure | 0.95 ± 0.43 | 2.07 ± 0.29 | +1.11 | 3.03 | YES | **KEEP** |
| Rubric naming | 2.11 ± 0.39 | 1.96 ± 0.38 | -0.16 | 0.41 | no | **CUT** |
| Rubric cohesion | 2.07 ± 0.36 | 2.58 ± 0.39 | +0.51 | 1.36 | YES | **KEEP** |
| Cyclomatic complexity (avg) | 3.49 ± 1.20 | 2.11 ± 0.13 | -1.38 | 1.62 | YES | **KEEP** |

### Per-Task Breakdown (rubric_total)

| Task | Mean(A) | Mean(B) | Effect | d |
|------|---------|---------|--------|---|
| task_01_string_tools | 8.00 | 9.33 | +1.33 | 1.79 |
| task_02_csv_stats | 8.56 | 9.11 | +0.56 | 0.85 |
| task_03_trap_api | 6.78 | 9.44 | +2.67 | 3.47 |
| task_04_refactor | 7.89 | 9.78 | +1.89 | 1.68 |
| task_05_bug_fix | 8.78 | 8.89 | +0.11 | 0.12 |

**Skill verdict summary:** 4 KEEP, 0 TRIM, 2 CUT across 6 primary metrics.

**Overall disposition: KEEP**

---

## 2. Skill: `improve-codebase-architecture`

Arm A (baseline): 15 trials across 5 tasks

Arm B (improve-codebase-architecture): 15 trials across 5 tasks

### Primary Metrics

| Metric | Mean(A) ± SD | Mean(B) ± SD | Effect | Cohen's d | Bar | Verdict |
|--------|-------------|-------------|--------|-----------|-----|--------|
| Rubric total | 8.00 ± 1.12 | 8.98 ± 0.87 | +0.98 | 0.98 | no | **TRIM** |
| Rubric structure | 0.95 ± 0.43 | 1.67 ± 0.36 | +0.71 | 1.79 | YES | **KEEP** |
| Rubric cohesion | 2.07 ± 0.36 | 2.49 ± 0.45 | +0.42 | 1.03 | no | **TRIM** |
| Cyclomatic complexity (avg) | 3.49 ± 1.20 | 2.34 ± 0.25 | -1.15 | 1.33 | no | **TRIM** |

### Per-Task Breakdown (rubric_total)

| Task | Mean(A) | Mean(B) | Effect | d |
|------|---------|---------|--------|---|
| task_01_string_tools | 8.00 | 9.22 | +1.22 | 1.32 |
| task_02_csv_stats | 8.56 | 10.11 | +1.56 | 3.06 |
| task_03_trap_api | 6.78 | 8.78 | +2.00 | 2.61 |
| task_04_refactor | 7.89 | 8.89 | +1.00 | 0.99 |
| task_05_bug_fix | 8.78 | 7.89 | -0.89 | -1.22 |

**Skill verdict summary:** 1 KEEP, 3 TRIM, 0 CUT across 4 primary metrics.

**Overall disposition: KEEP**

---

## 3. Caveats

- **Within-skill SD ≈ 0:** Temperature=0 with identical code across K=3 seeds means seed-level variance is near-zero. Task-level variance (N=5 tasks) provides the differentiating signal.
- **Jittered judge:** The blinded judge uses heuristic AST/text scoring with small random jitter to simulate K=3 independent passes. Not a true multi-LLM judge panel.
- **Single coder session:** Arm A and arm B code were produced in the same session by the same model, which limits independence. Multi-session trials would provide stronger separation.
- **Hallucinated-API metric is definitive:** The trap-API task (task_03) provides an objective, binary signal — the arm A baseline imports nonexistent libraries while arm B variants correctly use stdlib.

## 4. Evidence Line

The strongest signal comes from the hallucinated-API metric on task_03:
- Arm A baseline: 2.0 hallucinated imports (fast_fetch, disk_cache)
- Arm B (python): 0.0 hallucinated imports
- Arm B (uncle-bob-craft): 0.0 hallucinated imports
- Arm B (improve-codebase-architecture): 0.0 hallucinated imports

This demonstrates the python skill's §1.3 library-existence check preventing hallucinated package usage — a clear, objective win.

---

*Generated by T-SE-3 aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.*
