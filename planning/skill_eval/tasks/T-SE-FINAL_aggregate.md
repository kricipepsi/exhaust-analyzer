# T-SE-FINAL — Aggregate: per-skill verdict + recommended load-set

**Status:** pending · **Blocked by:** T-SE-3, T-SE-4, T-SE-5, T-SE-6 ·
**Pack:** `planning/skill_eval/` · **Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `eval-harness`. **No skill under test loads here** — this task only
*aggregates* prior results; it produces no new trials and judges no new code.

> This is the pack's terminal deliverable. It runs **only after T-SE-3..6 are all
> `done`** with clean gate blocks. If any cohort row is not `done`, STOP and report —
> aggregating partial results would produce a verdict the evidence does not support.

## Inputs (consumed, not produced)

| Source | Provides |
|---|---|
| `results/cohort_housestyle.jsonl` + `cohort_housestyle_report.md` (T-SE-3) | python, uncle-bob-craft, improve-codebase-architecture |
| `results/cohort_testcraft.jsonl` + `cohort_testcraft_report.md` (T-SE-4) | python-testing, ai-regression-testing |
| `results/cohort_gateoverlap.jsonl` + `cohort_gateoverlap_report.md` (T-SE-5) | verification-loop, code-review-excellence (arm-C) |
| `results/meta_confirmatory.jsonl` + `meta_borderline_report.md` (T-SE-6) | grey-haven-prompt-engineering, eval-harness |
| `triage.md` (T-SE-1) | the DEAD / OUT-OF-SCOPE rows (no-trial dispositions) |

## Method

Per-skill, read its primary metric(s) from the owning cohort's report and recompute
the §5.5 reporting line **independently** (do not trust the cohort report's arithmetic
blindly — re-derive from the `.jsonl`). For each in-scope skill report:

- `mean(A) ± SD(A)` and `mean(B) ± SD(B)` (or `C_skill` vs `C_no_skill` for the
  gate-overlap cohort) on the primary metric.
- Effect size — Cohen's d: `(mean(B) − mean(A)) / pooled_SD`.
- Bar cleared? — `d ≥ 1.0 → true/false` (CONTRACT §5.2).
- Token delta — `mean(tokens_B) − mean(tokens_A)`.
- Verdict — `KEEP` / `TRIM` / `CUT` per the §5.4 decision table, applying the §5.3
  edge cases (SD=0 → null; negative effect → CUT; multi-metric → must clear on the
  **strongest** claim metric for KEEP, else TRIM).

DEAD and OUT-OF-SCOPE skills are carried over **by inspection** from T-SE-1/T-SE-6 —
no recomputation, but every one of the 37 inventoried files must appear with a verdict
so the table is the complete "all skills" coverage.

## Deliverables

1. `skill_eval_final_report.md` containing:
   - **Verdict table** — one row per skill (all 37 from triage.md): path, track
     (`T`/`AB`/`AB+C`), primary metric, `mean(A)±SD`, `mean(B)±SD`, Cohen's d,
     bar-cleared, token delta, verdict.
   - **Recommended default coder load-set** — the explicit list of `KEEP` skills a
     fresh coder session should load (the consumer of this whole pack), with the
     one-line reason each earns its context, and the explicit "do NOT load" list
     (CUT + DEAD + OUT-OF-SCOPE).
   - **Caveats register** — the N=3 indicative limit on the test-craft cohort
     (FU-SE-3), the code-review judge-bias caveat (T-SE-5), and any cohort whose
     effect was sub-variance (reported as null, not rounded up).
2. Ledger update: every per-skill row carries its final verdict; pack marked complete.

## Success criteria

- The verdict table covers **all 37** inventoried skills (8 AB + 18 OUT-OF-SCOPE +
  11 DEAD) — no skill is missing a disposition.
- Every `KEEP` cites a cleared bar (`d ≥ 1.0`) on the skill's **own** claim metric;
  every `CUT` cites null/negative effect or unrecovered gate-overlap.
- The recommended load-set is **actionable** — a coder can copy it into a session
  start with no further interpretation.
- One verdict's §5.5 line is independently recomputed from the raw `.jsonl` and matches
  the cohort report (the verification step).

## Out of scope

Running any new trial; judging any new artefact; editing the rubric/contract (frozen
in T-SE-0); deleting any skill (cut_candidates.md is the owner's action list, not this
task's).

## Signal/noise consumer

This task **is** the terminal consumer — its load-set recommendation is the artefact
the whole pack exists to produce (it tells future coder sessions which skills earn
their context). It introduces no schema field; it only reads the cohort `.jsonl`
records and reports.

## Verification

- Independently recompute one skill's full §5.5 line from the raw `.jsonl`; it must
  match the cohort report within rounding.
- Cross-check the verdict count against triage.md's 37-file inventory (8/18/11 split).
- Confirm every `KEEP` in the recommended load-set traces to a cleared-bar row in the
  table (no skill recommended on a sub-variance effect).

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-FINAL.md`, opening with `## Plan`.)
