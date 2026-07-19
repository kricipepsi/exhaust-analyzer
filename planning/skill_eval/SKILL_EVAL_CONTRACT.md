# Skill-Eval Methodology Contract

**Pack:** `planning/skill_eval/` · **Author:** architect · **Date:** 2026-06-09

The question this pack answers: **for each skill a coder session could load, does
loading it measurably improve the produced code — or does it only consume context
and tokens?** This file fixes *how* that is measured so every per-skill verdict is
comparable and defensible. It is the analogue of the rollout pack's
`PROJECTION_CONTRACT.md`.

---

## 1. The central trap (read before designing any trial)

The naive test — "write code with the skill vs without, then check it" — **cannot
work**, for two reasons:

1. **The gate equalizes the output.** Every coder session ends in the inner-loop
   gate (`ruff → pyright → pytest`). The gate forces both arms to converge to the
   same clean final state, so comparing *final* error counts always shows ~no
   difference. This is exactly the "same errors surface either way" observation
   that motivated the pack — it is a measurement artefact, not a finding.
2. **Some skills *are* the gate.** `verification-loop` (and the validate-loop half
   of `python`) re-implement build/lint/type/test. Comparing them against a baseline
   that already runs the gate compares a skill against a copy of itself → no
   difference, by construction.

**Consequences for the design:**
- Never score a skill on the gated final state. Score it on signals the gate does
  **not** hold constant (§3).
- For any skill whose mechanism overlaps the gate, the only honest measurement is
  the **no-gate ablation arm** (§2, arm C): remove the gate, then ask whether the
  skill recovers the quality the gate would have enforced.

## 2. Conditions (arms)

For each evaluated skill, a task is run under matched arms — same task spec, same
model, same temperature, same repo state — differing only in what is loaded:

| Arm | Loads | Purpose |
|---|---|---|
| **A — baseline** | no skill, gate ON | Control. The current default coder session. |
| **B — skill** | the skill under test, gate ON | The skill's claimed contribution *on top of* the gate. |
| **C — no-gate ablation** | skill under test, gate **OFF** (single-shot, no iterate-to-green) | Isolates skill value from gate value. Run **only** for gate-overlapping skills (verification-loop, code-review, the python validate-loop). |

A skill "earns its context" if **B > A** on a gate-invisible metric (§3) by more
than trial variance (§5), **or** (for gate-overlapping skills) if **C-with-skill >
C-without-skill** — i.e. it recovers quality the gate would otherwise have caught.

## 3. Metrics — measured upstream of, or invisible to, the gate

Every trial records all of these; the per-skill task picks which are **primary**
for that skill's claim (assigned in the ledger):

1. **First-pass gate counts** — `ruff` / `pyright` / `pytest` failures on the
   **first** run, before any fix. (Quality of code as first written.)
2. **Iterations-to-green** — edit→check cycles to reach clean. (Convergence cost.)
3. **Token/cost to green** — total tokens for the task. (The "is it worth the
   context" axis directly.)
4. **Hallucinated-API count** — references to nonexistent functions/params/imports
   (objective; grep + import-resolve). The anti-hallucination claim lives here.
5. **Gate-invisible quality score** — a blinded rubric (§4) over the final code:
   readability, structure, naming, cohesion, error-handling, test meaningfulness.
6. **Objective proxies** (no judge needed): cyclomatic complexity, mutation score
   (test suites only), type-coverage %, docstring coverage, diff churn.

Rule: a skill is only credited for metrics tied to **its own claim**. `python-testing`
is judged on test quality (coverage, mutation score, meaningful asserts), not on
production-code readability; `uncle-bob` on structure/naming, not on test coverage.

## 4. The judge (for metric 5)

- **Rubric, not vibes.** A fixed 6-axis rubric, each axis 0–3, defined in T-SE-0's
  deliverable. The judge is an LLM-as-judge instance loaded with `code-reviev` +
  `uncle-bob` as the review standard.
- **Blinded.** The judge never sees which arm produced the code (strip arm labels,
  randomize order). The author-model and judge-model must differ, or at minimum run
  in separate sessions, to limit self-preference bias (this is the very blind-spot
  `ai-regression-testing` warns about — cite it).
- **Variance-aware.** Each artefact judged K times; report mean ± SD per axis.

## 5. Sample size, variance, success bar (FROZEN — T-SE-0)

### 5.1 Sample size

- **N ≥ 5** matched coding tasks (T-SE-2 corpus). One task is anecdote, not evidence.
- **K ≥ 3** independent trials per arm per task. Same task + same arm + different seed.
- **J ≥ 3** blinded judge passes per artefact (rubric.md judge protocol).

### 5.2 Success bar (pinned)

For arms A vs B (both gated), on the skill's **primary metric**:

> **KEEP:** `mean(B) − mean(A) > max(SD(A), SD(B))`
>
> i.e. the effect size must exceed the larger of the two arms' standard deviations.
> A ≥ 1-SD separation is required. This is the **Cohen's d ≥ 1.0** threshold —
> a large effect, intentionally conservative.

For arm C (no-gate ablation, gate-overlapping skills only):

> **KEEP:** `mean(C_skill) − mean(C_no_skill) > max(SD(C_skill), SD(C_no_skill))`
>
> where `C_no_skill` is arm A with the gate removed (control for the no-gate
> condition). The skill must recover quality the gate would have caught, by the
> same ≥ 1-SD margin.

### 5.3 Edge cases

- **SD = 0 on both arms.** If both arms produce identical results with zero
  variance, treat as **null** — no measurable effect. (A skill that never
  changes the output is context cost with zero benefit.)
- **SD = 0 on one arm only.** Use the non-zero SD as the threshold. If both are
  zero, see above.
- **Negative effect.** `mean(B) < mean(A)` → CUT regardless of magnitude
  (the skill actively harms the metric).
- **Multi-metric skills.** A skill with multiple primary metrics (e.g. python
  claims both first-pass quality and rubric axes) must clear the bar on its
  **strongest** metric to earn KEEP. If it clears on a minor metric but not its
  main claim, it is TRIM at best.

### 5.4 Verdicts

| Verdict | Condition |
|---------|-----------|
| **KEEP** | Effect > bar on primary metric; token cost acceptable. |
| **TRIM** | Effect positive but sub-bar, or only on a minor axis, or tokens disproportionate. Keep a slimmer version. |
| **CUT** | Null or negative effect; or pure gate-overlap with no no-gate recovery. |
| **OUT-OF-SCOPE** | Does not touch produced-code quality (assigned at T-SE-1 triage). |
| **DEAD** | Empty / stub / byte-duplicate — cut by inspection, no trial (assigned at T-SE-1 triage). |

### 5.5 Reporting

Every per-skill verdict in T-SE-FINAL must report:
- `mean(A) ± SD(A)` and `mean(B) ± SD(B)` on the primary metric
- Effect size (Cohen's d): `(mean(B) − mean(A)) / pooled_SD`
- Whether the bar was cleared (`d ≥ 1.0 → true/false`)
- Token delta: `mean(tokens_B) − mean(tokens_A)`
- Recommended load-set disposition

## 6. Two tracks

1. **Static triage (T-SE-1) — cheap, no trials.** Inventory every `SKILL.md`; mark
   `DEAD` (empty name, redirect stub, byte-duplicate) and `OUT-OF-SCOPE`
   (output-format/domain skills that never shape code: doc/excel/pdf/graph/firecrawl/
   meta-authoring). These get a verdict by inspection — a duplicate or empty skill
   is provable waste without spending a single trial. Triage outputs the **in-scope
   shortlist** the A/B track consumes.
2. **Empirical A/B (T-SE-3+).** Only the in-scope coding skills get the arm-based
   trials above, grouped into **claim cohorts** so members sharing a metric/method
   are run together.

## 7. Scope boundary (owner-confirmable)

**In scope — could affect produced-code quality:** `python`, `verification-loop`,
`python-testing`, `ai-regression-testing`, `code-review-excellence`, `uncle-bob-craft`,
`improve-codebase-architecture`, and (as borderline) `prompt-engineering-master`,
`eval-harness`.

**Out of scope for *this* eval — do not shape code in the loop:** the `doc/*` PRD/HLD/
md-prep skills, `excel/*`, `pdf-to-markdown`, `firecrawl`, all `graph/*` + `mcpmarket`
skills, `coding-bootstrap` (builds infra, not code), `FolderStruct`. They may have
value on *their* axis; that is a separate question this pack does not adjudicate.

If the owner wants any out-of-scope skill measured, move it to in-scope and assign
it a claim + metric here first — never run a trial without a named metric.

## 8. Hard rules inherited

Inner loop on Windows `.venv-wired` is the gate of record (sandbox can serve
truncated files). No graphify rebuild. No imports from `ARCHIVE/`/`v2/`/`v6/`.
Reports in `.md`. One task per coder session.
