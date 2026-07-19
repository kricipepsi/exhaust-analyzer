# Meta / Borderline Disposition Report

**Pack:** `planning/skill_eval/` **Task:** T-SE-6 **Date:** 2026-06-10
**Status:** COMPLETE

This report dispositions the two skills the CONTRACT flags as borderline/meta:
`grey-haven-prompt-engineering` and `eval-harness`. Both are OUT-OF-SCOPE, confirmed by inspection and (for prompt-engineering) one confirmatory A/B.

---

## 1. grey-haven-prompt-engineering — OUT-OF-SCOPE

**Path:** `_skills/prompt-engineering-master/SKILL.md`
**Track:** Static triage (inspection) + 1 confirmatory A/B

### 1.1 Inspection argument

The skill teaches users how to craft better LLM prompts (26 principles, templates, checklists, anti-patterns). Its stated purpose is: "Master 26 documented prompt engineering principles for crafting effective LLM prompts with 400%+ quality improvement."

In the skill-eval harness, the coder implements **fixed, pre-authored corpus prompts** (e.g. `corpus/task_01_string_tools/prompt.md`). The coder does **not author prompts** — it reads a spec and writes code. A prompt-engineering skill has **no lever** on produced-code quality because the prompt is already fixed.

Per CONTRACT §7, an OUT-OF-SCOPE skill gets a code-quality metric only if one can be named. The named effect is "better prompts" — which the fixed-prompt harness does not exercise. The inspection prediction is sub-variance (null).

### 1.2 Confirmatory A/B

| Parameter | Value |
|-----------|-------|
| Task | `task_01_string_tools` (lowest-variance corpus task) |
| Arms | A (baseline, gate ON) vs B (`grey-haven-prompt-engineering`, gate ON) |
| K | 3 per arm (seeds 42/43/44 arm A; 52/53/54 arm B) |
| Primary metrics | `rubric_total`, `first_ruff_errors`, `first_pyright_errors` |

**First-pass gate counts:**

| Metric | Arm A (mean ± SD) | Arm B (mean ± SD) | Effect | Bar |
|--------|-------------------|-------------------|--------|-----|
| `first_ruff_errors` | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 | null (SD=0 both arms) |
| `first_pyright_errors` | 0.0 ± 0.0 | 0.0 ± 0.0 | 0.0 | null (SD=0 both arms) |

**Rubric scores (blinded, J=1 pass, 6-axis rubric 0-3 per axis):**

| Artefact (seed) | Read. | Struct. | Naming | Cohesion | Err.Hand. | Test.Mean. | Total |
|-----------------|-------|---------|--------|----------|-----------|------------|-------|
| A-42 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |
| A-43 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |
| A-44 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |
| B-52 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |
| B-53 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |
| B-54 | 2 | 2 | 2 | 2 | 2 | 2 | 12 |

| Arm | mean(`rubric_total`) | SD |
|-----|----------------------|----|
| A | 12.0 | 0.0 |
| B | 12.0 | 0.0 |

- Effect (Cohen's d): undefined (SD=0 both arms)
- Bar: per CONTRACT §5.3, SD=0 on both arms → treat as **null** — no measurable effect

### 1.3 Overturn rule evaluation

The overturn rule was: "if the confirmatory A/B clears the §5.2 bar (effect > max(SD_A, SD_B), Cohen's d ≥ 1.0) on `rubric_total`, the inspection verdict is wrong."

- Effect: 0.0, max(SD_A, SD_B): 0.0
- 0.0 > 0.0 → **false**
- Bar **not cleared** → OUT-OF-SCOPE **confirmed**

### 1.4 Verdict

**OUT-OF-SCOPE.** The skill's claim is "better prompts" which the fixed-prompt eval harness does not exercise. The confirmatory A/B shows zero measurable effect on `rubric_total` (null by §5.3) and zero effect on first-pass gate counts (all zero both arms). No overturn triggered.

Consumer: T-SE-FINAL coverage table, recommended default load-set (excludes OUT-OF-SCOPE skills).

---

## 2. eval-harness — OUT-OF-SCOPE

**Path:** `_skills/codingskills/ecc-subset/eval-harness/SKILL.md`
**Track:** Static triage (inspection), no trial

### 2.1 Inspection argument

`eval-harness` is the measurement instrument this skill-eval pack *uses* to run trials. Its stated purpose is: "Formal evaluation framework implementing eval-driven development (EDD) — define pass/fail criteria before implementation, measure agent reliability with pass@k metrics."

Subjecting the eval-harness to its own harness as a code-quality subject is **circular** — it does not produce diagnostic-engine code in the loop; it measures the quality of other code. A measurement instrument cannot measure itself on the axis it defines.

Per CONTRACT §7, OUT-OF-SCOPE for *this* eval (which measures code-quality impact of loaded skills). Already settled in T-SE-1 triage and ledger.

### 2.2 Verdict

**OUT-OF-SCOPE, no trial.** Circular — the instrument cannot measure itself. Consumer: T-SE-FINAL coverage table (counts toward the "all skills" set with OUT-OF-SCOPE disposition).

---

## Evidence record

- `results/meta_confirmatory.jsonl` — 6 trial records (3 arm A + 3 arm B)
- `tasks/progress_notes/T-SE-6.md` — Plan + dual gate blocks
- `_skills/prompt-engineering-master/SKILL.md` — confirms skill purpose is prompt authoring, not code production
- `_skills/codingskills/ecc-subset/eval-harness/SKILL.md` — confirms skill purpose is evaluation framework, not code production

## Dispositions summary

| Skill | Disposition | Backing |
|-------|-------------|---------|
| `grey-haven-prompt-engineering` | OUT-OF-SCOPE | Inspection + confirmatory A/B (null, sub-variance) |
| `eval-harness` | OUT-OF-SCOPE | Inspection (circular — measurement instrument) |
