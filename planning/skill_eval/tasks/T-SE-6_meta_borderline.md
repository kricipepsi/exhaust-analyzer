# T-SE-6 — Meta / borderline disposition

**Status:** authored · runnable · **Blocked by:** T-SE-0, T-SE-1 (both done) ·
**Pack:** `planning/skill_eval/` · **Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `eval-harness`. **Do not hand-load the skills under test** — for the
one confirmatory A/B below, the runner's arm logic loads `grey-haven-prompt-engineering`.

This task dispositions the two skills that the contract flags as borderline/meta. It
is mostly **inspection** (CONTRACT §6 track 1) with **one** confirmatory A/B attached
to the prompt-engineering verdict (owner decision Q-SE-1).

## Subjects & dispositions

| Skill | Path (under `_skills/`) | Disposition | Backing |
|---|---|---|---|
| `grey-haven-prompt-engineering` | `prompt-engineering-master` | **OUT-OF-SCOPE** (by inspection) | + 1 confirmatory A/B (below) |
| `eval-harness` | `codingskills/ecc-subset/eval-harness` | **OUT-OF-SCOPE** (by inspection, no trial) | circular — it is the measurement instrument |

### Inspection argument — `grey-haven-prompt-engineering`

The eval arms differ **only** by which skill loads; the coding-task prompt is fixed
(T-SE-2 corpus). A prompt-engineering skill shapes how *a user prompts a model* — but
in this harness the coder is **implementing a fixed spec**, not authoring prompts, so
the skill has **no lever** on the produced code. Per CONTRACT §7, an OUT-OF-SCOPE skill
gets a code-quality metric only if one can be named; here the named effect is "better
prompts," which the fixed-prompt harness does not exercise. Disposition: **OUT-OF-SCOPE**.

### Inspection argument — `eval-harness`

`eval-harness` is the instrument this pack *uses* to run trials. Subjecting it to its
own harness as a code-quality subject is circular (it does not produce diagnostic-
engine code in the loop). Already settled OUT-OF-SCOPE in the ledger and T-SE-1 triage.
Disposition: **OUT-OF-SCOPE, no trial.**

## Confirmatory A/B (the "+ confirm" half — `grey-haven-prompt-engineering` only)

A single small trial that **backs** the inspection verdict with evidence rather than
overturning the methodology:

- **Task:** `task_01_string_tools` only (simplest corpus task → lowest variance, so a
  real effect would surface most cleanly here).
- **Arms:** A (baseline, gate ON) vs B (`grey-haven-prompt-engineering`, gate ON).
- **Trials:** K ≥ 3 per arm.
- **Primary metrics (resolves metrics_schema §6 "TBD"):** `rubric_total` and the
  first-pass counts `first_ruff_errors + first_pyright_errors`. These are the general
  "did loading it make the coder write better code at all" axes — the only axes a
  prompt skill could plausibly move, and the ones the inspection predicts it will not.
- **Expectation:** sub-variance (null) — confirming OUT-OF-SCOPE.
- **Overturn rule:** if the confirmatory A/B **clears the §5.2 bar** (effect >
  `max(SD_A, SD_B)`, Cohen's d ≥ 1.0) on `rubric_total`, the inspection verdict is
  **wrong** → do **not** silently keep OUT-OF-SCOPE; log it as an overturn and route
  a full-cohort A/B as a new follow-up task. (This is the guard that keeps "inspection"
  honest — one task can falsify it but not, by itself, confirm a KEEP.)

## Deliverables

1. `results/meta_confirmatory.jsonl` — the `task_01 × {A,B} × K` records for
   `grey-haven-prompt-engineering`.
2. `meta_borderline_report.md` — the two inspection arguments above, the confirmatory
   A/B result (`mean ± SD` on `rubric_total` and first-pass counts, effect vs bar),
   and the final disposition for each skill with its evidence line.

## Success criteria

- Both inspection verdicts state *why the harness gives the skill no lever*, not just
  "it's a doc/meta skill".
- The confirmatory A/B reports effect vs the variance it must beat; a sub-variance
  result is reported `null` and read as **confirming** OUT-OF-SCOPE.
- The overturn rule is evaluated explicitly (bar cleared: yes/no) — not skipped.
- Dispositions written back to the ledger's per-skill table.

## Out of scope

A full prompt-engineering cohort (only triggered by an overturn, as a new task);
other cohorts; editing the rubric/contract (frozen in T-SE-0); re-opening
`eval-harness` as a subject.

## Signal/noise consumer

The confirmatory A/B reads only existing fields (`rubric_total`, `first_ruff_errors`,
`first_pyright_errors`) already captured by `runner.py`. No new schema field. The two
dispositions are consumed by **T-SE-FINAL**'s coverage table (the "all skills" row set)
and the recommended default load-set (which excludes OUT-OF-SCOPE skills).

## Verification

- Re-read both SKILL.md files and confirm the inspection argument matches their
  actual stated purpose (no straw-manning).
- Re-score the confirmatory artefact blind once and reproduce `rubric_total` within
  the K-pass SD.
- Recompute the effect-vs-bar (overturn) decision by hand.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-6.md`, opening with `## Plan`.)
