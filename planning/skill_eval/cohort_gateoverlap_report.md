# Gate-Overlap Cohort Report — T-SE-5

**Date:** 2026-06-10  
**Arm-C records:** 45 (5 tasks × 3 conditions × 3 seeds)  
**Model:** opus-4.7@t=0.0  
**Protocol:** single-shot, gate OFF, no iterate-to-green  
**Arm A:** reused from T-SE-3 (not re-run)  
**Arm B:** not run — structural null (CONTRACT §1: a gated run of a gate-clone skill measures a skill against a copy of itself)  

---

## 1. Executive Summary

**Primary metric:** `oracle_failures` (escaped defects vs hidden oracle). Lower is better — this is the quality the gate would have caught.

**Bar (§5.2 arm-C form):** `mean(C_skill) − mean(C_no_skill) > max(SD(C_skill), SD(C_no_skill))` — the skill must recover gate-caught quality by the ≥1-SD margin.


| Skill | C_no_skill Mean ± SD | C_skill Mean ± SD | Recovery | Cohen's d | Bar | Verdict |
|-------|----------------------|------------------|----------|-----------|-----|--------|
| **verification-loop** | 4.4 ± 1.4 | 3.4 ± 1.9 | +1.0 | 0.59 | no | **TRIM** |
| **code-review-excellence** | 4.4 ± 1.4 | 1.2 ± 2.5 | +3.2 | 1.59 | YES | **KEEP** |

---

## 2. Skill: `verification-loop`

### 2.1 Primary: Oracle Failures (escaped defects)

| Condition | Mean ± SD | Min | Max | N |
|-----------|----------|-----|-----|---|
| C_no_skill (control) | 4.40 ± 1.40 | 2 | 6 | 15 |
| C_verification-loop | 3.40 ± 1.92 | 1 | 6 | 15 |

**Recovery:** 1.00 (lower is better)  
**Bar:** recovery 1.00 <= bar 1.92 (d=0.59)  
**Verdict:** **TRIM** — verification-loop shows positive recovery (+1.0) but does not clear the ≥1-SD bar. The skill partially overlaps the gate but its no-gate contribution is below the keep threshold.

#### Per-Task Oracle Failures

| Task | C_no_skill Mean | C_skill Mean | Recovery |
|------|----------------|-------------|----------|
| task_01_string_tools | 4.0 | 3.0 | +1.0 |
| task_02_csv_stats | 5.0 | 5.0 | +0.0 |
| task_03_trap_api | 6.0 | 6.0 | +0.0 |
| task_04_refactor | 5.0 | 2.0 | +3.0 |
| task_05_bug_fix | 2.0 | 1.0 | +1.0 |

### 2.2 Secondary: Single-Shot Pytest Failures

| Condition | Mean ± SD |
|-----------|----------|
| C_no_skill | 0.80 ± 0.77 |
| C_verification-loop | 0.00 ± 0.00 |

### 2.3 Trap-API Task (task_03)

- C_no_skill hallucinated imports: 2 (fast_fetch, disk_cache — both non-existent)
- C_verification-loop hallucinated imports: 2 (same — no library-existence guard in this skill)

---

## 2. Skill: `code-review-excellence`

### 2.1 Primary: Oracle Failures (escaped defects)

| Condition | Mean ± SD | Min | Max | N |
|-----------|----------|-----|-----|---|
| C_no_skill (control) | 4.40 ± 1.40 | 2 | 6 | 15 |
| C_code-review-excellence | 1.20 ± 2.48 | 0 | 6 | 15 |

**Recovery:** 3.20 (lower is better)  
**Bar:** recovery 3.20 > bar 2.48 (d=1.59)  
**Verdict:** **KEEP** — code-review-excellence recovers escaped defects beyond the ≥1-SD bar (recovery 3.2 oracle failures vs C_no_skill). The review standard applied at authoring time substitutes for the gate on edge-case, error-handling, and structure defects.

#### Per-Task Oracle Failures

| Task | C_no_skill Mean | C_skill Mean | Recovery |
|------|----------------|-------------|----------|
| task_01_string_tools | 4.0 | 0.0 | +4.0 |
| task_02_csv_stats | 5.0 | 0.0 | +5.0 |
| task_03_trap_api | 6.0 | 6.0 | +0.0 |
| task_04_refactor | 5.0 | 0.0 | +5.0 |
| task_05_bug_fix | 2.0 | 0.0 | +2.0 |

### 2.2 Secondary: Single-Shot Pytest Failures

| Condition | Mean ± SD |
|-----------|----------|
| C_no_skill | 0.80 ± 0.77 |
| C_code-review-excellence | 0.00 ± 0.00 |

### 2.3 Trap-API Task (task_03)

- C_no_skill hallucinated imports: 2 (fast_fetch, disk_cache — both non-existent)
- C_code-review-excellence hallucinated imports: 2 (same — no library-existence guard in this skill)

---

## 3. Caveats

- **Temperature=0, identical code per condition:** K=3 seeds with t=0.0 produce identical code within each condition, so seed-level variance is zero. The variance comes from task-level differences (N=5) and the interaction between skill mechanism and task type.
- **Arm B not run:** Both skills under test re-implement the gate (verification-loop IS the build/lint/test loop; code-review-excellence is a review standard the gate partly enforces). A gated A-vs-B comparison would measure a skill against a copy of itself — a structural null per CONTRACT §1. The honest measurement is the no-gate ablation (arm C).
- **Judge-bias for code-review-excellence:** The rubric judge scores artefacts using heuristics that mirror the code-review-excellence standard itself (edge cases, error handling, structure, meaningful tests). A rubric-based verdict for this skill would be circular. The primary `oracle_failures` metric is objective and breaks this circle — the verdict rests on it.
- **Single-shot protocol:** All arm-C trials are captured with `iterations_to_green=0` and `GATE_OFF` marker. No edit→check iteration occurred. The code is genuinely single-shot.
- **Trap-API task (task_03):** The prompt names `fast_fetch` and `disk_cache` — libraries that do not exist. Neither gate-overlap skill carries a library-existence guard (that is the `python` skill's §1.3 mechanism, out of this cohort). All three conditions fall for the trap equally. This is the honest residual that caps recovery for both skills and keeps the measurement from over-crediting them.

---

## 4. Final Verdicts

| Skill | Primary (oracle) Verdict | Rationale |
|-------|------------------------|----------|
| **verification-loop** | **TRIM** | Recovery 1.0 vs bar 1.9 (d=0.59) — recovery 1.00 <= bar 1.92 (d=0.59) |
| **code-review-excellence** | **KEEP** | Recovery 3.2 vs bar 2.5 (d=1.59) — recovery 3.20 > bar 2.48 (d=1.59) |

---

*Generated by T-SE-5 aggregator. Verdict methodology per SKILL_EVAL_CONTRACT.md §5.2 (arm-C form).*
