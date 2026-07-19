# T-SE-4 — Cohort A/B: test-craft

**Status:** authored · runnable · **Blocked by:** T-SE-0, T-SE-1, T-SE-2 (all done) ·
**Pack:** `planning/skill_eval/` · **Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `eval-harness`. **Do not hand-load the skills under test** — the
runner's arm logic loads them (CONTRACT §2 / START_HERE §0).

Clones the T-SE-3 template (gated A/B, no arm C). The only structural difference is
the **subset of corpus tasks** that exercise this cohort's claim and the **primary
metrics** (test quality, not production-code style).

## Cohort under test

`python-testing` (`codingskills/ecc-subset/python-testing`) and
`ai-regression-testing` (`codingskills/ecc-subset/ai-regression-testing`). Both
claim to improve the **test suite the coder writes** — coverage, defect-catching
power, meaningful (behavioural, not implementation-coupled) assertions.
`ai-regression-testing` additionally claims an escaped-defect / judge-bias guard.

## Corpus subset (READ — this bounds N)

A test-craft skill is only observable where the coder **authors a fresh test
suite**. In the T-SE-2 corpus that is exactly three tasks:

| Task | Writes a `test_*.py`? | In subset |
|---|---|---|
| `task_01_string_tools` | yes (`test_string_tools.py`) | IN |
| `task_02_csv_stats` | yes (`test_csv_stats.py`) | IN |
| `task_03_trap_api` | yes (`test_data_fetcher.py`) | IN |
| `task_04_refactor` | no — preserves behaviour against the existing oracle | OUT |
| `task_05_bug_fix` | no — surgical fix against an existing visible test | OUT |

**N = 3** for the mutation/test-meaningfulness metric. This is **below the frozen
§5.1 bar of N ≥ 5**, because only three corpus tasks elicit a suite. This does not
relax the bar; it is a stated coverage limitation. The cohort verdict for these
metrics is **"indicative"** until the corpus is extended (see *Unplanned
follow-up FU-SE-3* in the ledger). The secondary axis `rubric_error_handling`
(error-path test coverage) is observable on all three subset tasks too.

## Method (per skill in the cohort)

Arms **A (baseline, gate ON)** vs **B (skill, gate ON)**; arm C **not** used (no
gate overlap — these skills sit upstream of the gate, like T-SE-3). **K ≥ 3**
trials per arm per task, on the 3-task subset. Both skills run the same subset so
their per-task records are matched.

Primary metrics (metrics_schema §3–4, credited per CONTRACT §3 — a test skill is
judged on **test quality**, never on production-code readability):

| Metric | Field(s) | Why it is the claim's metric |
|---|---|---|
| Mutation score (primary) | `mutation_score` | Directly measures whether the coder's tests *catch* injected defects — the core test-craft claim. `mutmut`/`mutpy` over the production module, scored by the coder's suite. |
| Test meaningfulness (primary) | `rubric_test_meaningfulness` | Blinded rubric Axis 6 — behavioural vs implementation-coupled asserts, edge/error-path coverage. |
| Error-path coverage (secondary) | `rubric_error_handling` | Rubric Axis 5 — does the suite exercise failure paths (the `ai-regression-testing` escaped-defect claim). |

Token/cost (`total_tokens`) is recorded for the §5.5 token-delta line but is not a
primary metric here.

## Runner gap to close (IN SCOPE for this task)

`runner.py` defines `mutation_score` in `TrialRecord` (schema §5) but **never
computes it** — `capture_metrics` sets the objective proxies (`cyclomatic_*`,
`type_coverage_pct`, `docstring_coverage_pct`, `diff_churn_*`) and leaves
`mutation_score` at its `None` default. Since `mutation_score` is this cohort's
**primary** metric, the coder must add the producer:

1. A `_mutation_score(work_dir)` helper running `mutmut` (or `mutpy`) over the
   production module, scored by the coder-authored suite, returning the kill ratio.
2. Call it from `capture_metrics` for the test-writing subset, setting
   `rec.mutation_score`. Tasks with no suite still return `None` (unchanged).

This populates an **existing** schema field (no new field ships); it only supplies
the missing code path. Logged as **FU-SE-5** in the ledger so the runner change is
tracked. Line/branch coverage is **not** added as a separate field — `mutation_score`
subsumes it (an unkilled mutant in uncovered code already counts against the score),
so the schema gains nothing it cannot already read.

## Deliverables

1. `results/cohort_testcraft.jsonl` — every trial's `TrialRecord` (metrics_schema §5),
   `mutation_score` populated (not `null`) for every subset trial.
2. `cohort_testcraft_report.md` — per skill: `mean ± SD` on each primary metric,
   the effect `mean(B) − mean(A)`, whether it clears the §5.2 bar
   (`effect > max(SD_A, SD_B)`, i.e. Cohen's d ≥ 1.0), and the verdict
   (`KEEP`/`TRIM`/`CUT`) with the one-line evidence. The report must label the
   mutation/test-meaningfulness verdict **"indicative (N=3)"**.

## Success criteria

- `mutation_score` is a real number (not `null`) for all 3 subset tasks × both
  arms × K trials, for both skills. A `null` mutation score on a subset task is a
  failed run, not a result.
- Each verdict states the **effect size and the variance it must beat**;
  sub-variance effects are reported `null`, not rounded up to a win (CONTRACT §5.3).
- `ai-regression-testing` is credited only if it beats `python-testing`'s arm A on
  an escaped-defect axis (`mutation_score` or `rubric_error_handling`) — not on
  production-code style.
- Verdicts written back to the ledger's per-skill table.

## Out of scope

Other cohorts; production-code-quality axes (those are T-SE-3's, and a test skill
gets no credit there); editing the rubric/contract (frozen in T-SE-0); **extending
the corpus** (logged as FU-SE-3 — a separate task, not this diff).

## Signal/noise consumer

Every field this task reads already exists in `metrics_schema.md` and is captured
by `runner.py` (`mutation_score`, `rubric_*` via the blinded judge). The verdicts
are consumed by **T-SE-FINAL**'s KEEP/TRIM/CUT table and the recommended default
coder load-set. No new schema field is introduced.

## Verification

- Re-score one suite blind and reproduce its Axis 5/6 scores within the K-pass SD.
- Recompute one mutation score by hand-injecting one mutant and confirming the
  coder's suite fails on it (spot-check that `mutation_score` is real, not stubbed).
- Recompute one effect-vs-bar decision by hand.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-4.md`, opening with `## Plan`.)
