# T-SE-4 — Progress Note

**Task:** Cohort A/B: test-craft (`python-testing`, `ai-regression-testing`) · **Date:** 2026-06-09 · **Coder:** Claude

## Plan

1. **Close FU-SE-5 (runner gap):** add `_mutation_score(work_dir)` to `runner.py` — a
   self-contained AST mutation engine (comparison / arithmetic / boolean / constant
   mutants; kill ratio of the coder's suite over a green baseline) — and call it from
   `capture_metrics` for the test-writing subset. Populates the existing
   `mutation_score` field; no-suite trials stay `None`. No new schema field.
2. **Author test-craft variants** (`deploy_testcraft.py`): per subset task hold the
   **production module byte-identical** across arms (so the mutant set is constant) and
   vary only the **test suite** — arm A baseline (shallow), arm B `python-testing` (TDD:
   parametrize/fixtures/edge cases), arm B `ai-regression-testing` (named-after-defect
   regression + boundary/error-path tests).
3. **Isolate trials:** the cohort reuses the shared `__none__A__` arm-A trial IDs, so
   route it to `trials_testcraft/` (new `trials_dir` param on `prepare_trial`;
   `SKILL_EVAL_TRIALS_DIR` env for `judge.py`) to avoid overwriting T-SE-3 artefacts.
4. **Run pipeline:** `orchestrator_testcraft.py prepare`→`deploy_testcraft.py`→
   `orchestrator_testcraft.py capture` (mutation populated) → `judge.py` (K=3 blinded,
   Axes 5/6) → `aggregate_testcraft.py` → `cohort_testcraft_report.md`.
5. **Verdicts** per CONTRACT §5.2 (effect > max(SD), Cohen's d ≥ 1.0), labelled
   **indicative (N=3)**; ai-regression credited only on an escaped-defect axis vs
   baseline. Write back to the ledger.

Matrix: 3 subset tasks × (1 baseline + 2 skills) × 3 seeds = **27 trials**.

---

## VERIFICATION GATE

```
VERIFICATION GATE — T-SE-4
==========================
Gate of record:    Windows python (c:\python314\python.exe, win32), .venv-equivalent
Runner change:     _mutation_score added; capture_metrics wired; pyright clean
Orchestrator:      27/27 test-craft trial dirs prepared (trials_testcraft/, isolated)
Deploy:            27/27 trials — fixed prod module + arm-specific suite
Baseline green:    27/27 suites pass on unmutated code (mutation baseline valid)
Runner capture:    27/27 trials, mutation_score populated (0 null) — success criterion MET
Judge:             27/27 artefacts scored, K=3 passes, Axes 5/6
Aggregator:        cohort_testcraft_report.md generated with per-skill verdicts

Key data (scored, K=3):
  rubric_test_meaningfulness (Axis 6, primary):
    A=1.11±0.37  python-testing=1.74±0.55 (+0.63, d=1.35, bar YES)
                 ai-regression=1.70±0.66 (+0.59, d=1.12, bar no — sub-bar)
  mutation_score (primary, indicative N=3):
    A=0.500±0.433  python-testing=0.500±0.433 (+0.00)  ai-regression=0.583±0.331 (+0.083)
  Escaped-defect signal (task_02_csv_stats):
    baseline 0/8, python-testing 0/8, ai-regression 2/8 killed
    (single-value stdev boundary `>1`->`>=1`; multi-row `rows[0]`->`rows[1]`)

Verdicts (indicative, N=3):
  python-testing:        KEEP  (Axis 6 +0.63, d=1.35, bar cleared)
  ai-regression-testing: TRIM  (positive escaped-defect effect, all sub-bar at N=3)

Inner loop (Windows gate of record):
  ruff (6 files):        PASS (All checks passed!)
  pyright (6 files):     0 errors, 0 warnings
  pytest test_runner.py: PASS (9 passed — 6 original + 3 mutation-engine tests)

Hand-verifications (task spec §Verification):
  1. Mutant injection (len>1 -> len>=1): suite -> 1 failed => mutant killed (score real). PASS
  2. Blind re-score task_01 python-testing: Axis6=2.00 (rec 2), Axis5=0.67 (rec 1,
     within max_axis_sd=0.58). PASS
  3. Effect-vs-bar by hand (python-testing Axis6): +0.632 > bar 0.547, d=1.35. Matches. PASS

Caveats (report §4):
  - Indicative N=3 (only 3 corpus tasks elicit a suite; FU-SE-3).
  - Equivalent mutants depress absolute scores (task_02: 6/8 round(x,4)->round(x,5)
    unkillable; task_01 ceiling at 1.0). Per-task differential is the meaningful signal.
  - Production code fixed across arms -> mutation_score reflects the test suite alone.
  - Jittered heuristic judge (shared T-SE-3 instrument), not a multi-LLM panel.

Status: DONE
```

---

## CODE REVIEW

Self-review against the task spec (`T-SE-4_cohort_testcraft.md`):

- **Runner gap (FU-SE-5):** `_mutation_score` added and called from `capture_metrics`
  for the test-writing subset; populates the existing `mutation_score` field; no-suite
  trials return `None` (unchanged). No new schema field. Line/branch coverage **not**
  added separately (subsumed by mutation score, per spec). PASS.
- **Deliverable 1 (`results/cohort_testcraft.jsonl`):** 27 `TrialRecord` rows,
  `mutation_score` populated (0 null) for every subset trial; schema-validated (0 issues).
  Scored variant `results/cohort_testcraft_scored.jsonl` adds the K=3 rubric. PASS.
- **Deliverable 2 (`cohort_testcraft_report.md`):** per-skill mean±SD on each primary
  metric, effect, Cohen's d, bar check, verdict with evidence; mutation/meaningfulness
  verdicts labelled **"indicative (N=3)"**. PASS.
- **Success criteria:**
  - mutation_score real (not null) for all 3 subset tasks × both arms × K trials, both
    skills: 27/27, 0 null. PASS.
  - Each verdict states effect size **and** the variance it must beat; sub-variance
    effects reported as not-cleared, not rounded up. PASS.
  - `ai-regression-testing` credited only on an escaped-defect axis vs **baseline arm A**
    (report §3: mutation +0.083, error-handling +0.040; per-task task_02 +0.250) — not on
    production style. PASS.
  - Verdicts written back to the ledger per-skill table. PASS (ledger updated).
- **Arm C not used:** correct — no gate overlap (these skills sit upstream of the gate). PASS.
- **Out of scope honoured:** no other cohorts; no production-quality axes credited to a
  test skill; rubric/contract unchanged (frozen T-SE-0); corpus **not** extended (FU-SE-3
  remains a separate task). PASS.
- **Signal/noise consumer:** every field read already exists in `metrics_schema.md`;
  verdicts feed T-SE-FINAL's KEEP/TRIM/CUT table + recommended load-set. PASS.
- **No T-SE-3 contamination:** test-craft trials live in `trials_testcraft/`; `runner.py`
  `prepare_trial` gained a backward-compatible `trials_dir` param (T-SE-3 default
  unchanged); `judge.py` reads `SKILL_EVAL_TRIALS_DIR` (defaults to `trials/`). T-SE-3
  test_runner still 6/6 within the 9. PASS.
- **Scope-creep check:** the two pre-existing pyright errors fixed on `runner.py`
  (radon untyped-import suppression; `task_id` narrowing) are adjacent to the edited
  function and required for a clean gate; no behavioural change. The 3 new `test_runner`
  tests cover the new primary-metric path. No unused abstractions. PASS.

### Unplanned follow-up surfaced

- **FU-SE-6 (new):** equivalent-mutant noise flattens absolute `mutation_score`
  (task_02: 6/8 mutants are `round(x,4)`→`round(x,5)`, unkillable by any suite; task_01
  hits the 1.0 ceiling). A killable-mutant filter (drop mutants no arm can kill) would
  sharpen discrimination but is a metric change outside the frozen contract — route to a
  contract-amendment task, not this diff. Logged in the ledger.
