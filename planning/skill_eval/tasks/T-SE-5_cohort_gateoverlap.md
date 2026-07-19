# T-SE-5 — Cohort A/B/C: gate-overlap

**Status:** authored · runnable · **Blocked by:** T-SE-0, T-SE-1, T-SE-2 (all done) ·
**Pack:** `planning/skill_eval/` · **Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `eval-harness`. **Do not hand-load the skills under test** — the
runner's arm logic loads them (CONTRACT §2 / START_HERE §0).
**Special case:** the skill under test here *is* the verification loop. Per
START_HERE §0, the **arm** loads it for arms B/C; your own session still loads the
mandatory pair (which includes `verification-loop`) to run *your* inner loop. The
measurement is not contaminated because the metric is read from the **trial's**
single-shot output, not your session.

This is the only cohort that uses **arm C**. It exists because of CONTRACT §1: these
skills *re-implement the gate*, so a gated A-vs-B comparison measures a skill against
a copy of itself and is null by construction. The honest measurement is the **no-gate
ablation**.

## Cohort under test

`verification-loop` (`codingskills/ecc-subset/verification-loop`) and
`code-review-excellence` (`codingskills/code-reviev`). Both overlap the gate:
verification-loop is the build/lint/type/test loop itself; code-review-excellence
is a review standard that the gate (and the blinded judge) partly enforce already.

## Method — arm C is primary

For each skill, run the **full 5-task corpus**, **K ≥ 3** trials per condition:

| Condition | Loads | Gate | Purpose |
|---|---|---|---|
| `C_no_skill` | nothing | **OFF** (single-shot, no iterate-to-green) | Control for the no-gate condition — what a coder produces in one shot with no help and no gate. |
| `C_skill` | the skill under test | **OFF** (single-shot) | Does the skill recover the quality the gate would otherwise have enforced? |
| `A` (reference only) | nothing | ON | The gated baseline — reference for "what the gate already guarantees". Reused from T-SE-3's arm-A records; **do not re-run**. |

**No arm B is run for `verification-loop`** — a gated run of the verification skill
is a copy of the gate (CONTRACT §1) and would be reported as a structural null, not
measured. For `code-review-excellence`, arm B is also skipped for the same overlap
reason; its value, if any, is a single-shot review effect captured by arm C.

### Success bar (CONTRACT §5.2, arm-C form)

> **KEEP:** `mean(C_skill) − mean(C_no_skill) > max(SD(C_skill), SD(C_no_skill))`

i.e. the skill must **recover gate-caught quality** by the ≥ 1-SD margin. A skill
that only matches `C_no_skill` is pure gate-overlap → **CUT** (CONTRACT §5.4: "pure
gate-overlap with no no-gate recovery").

## Primary metrics

| Metric | Field | Read on |
|---|---|---|
| Escaped-defect count (primary) | `extra["oracle_failures"]` | single-shot output vs the hidden oracle — *lower is better*; this is the quality the gate would have caught. |
| Single-shot test failures | `extra["single_shot_pytest_failures"]` | the coder's own visible tests, measured once (not fixed). |
| Gate-invisible quality (secondary) | `rubric_*` total | blinded judge over the single-shot artefact (A-vs-C delta). |

## Runner gap to close (IN SCOPE for this task)

`runner.py:capture_metrics` currently **skips all first-pass gate counts when
`no_gate=True`** (the `if not no_gate:` guard, ~line 571), and never calls the
already-defined `_run_oracle`. For arm C the single-shot result *is* the
measurement, so the coder must, **for `no_gate` trials only**:

1. Run the hidden oracle once via the existing `_run_oracle(task_dir, work_dir)`
   and record its failure count in `rec.extra["oracle_failures"]`.
2. Run `pytest` once in **measure-only** mode (no fix loop) and record
   `rec.extra["single_shot_pytest_failures"]`.

This is a measurement wiring change inside `capture_metrics`'s `no_gate` branch —
it adds **no new schema field** (both live in the existing `extra` dict, which
metrics_schema §5 already defines for extensibility). Gated arms A/B are untouched.
Logged as **FU-SE-4** in the ledger so the change is tracked, not silent.

## Deliverables

1. `results/cohort_gateoverlap.jsonl` — `C_no_skill` and `C_skill` records for both
   skills across the 5-task corpus, with `extra["oracle_failures"]` and
   `extra["single_shot_pytest_failures"]` populated.
2. `cohort_gateoverlap_report.md` — per skill: `mean ± SD` of escaped-defect count
   for `C_skill` vs `C_no_skill`, the recovery effect, whether it clears the §5.2
   arm-C bar, and the verdict. Must state explicitly that arm B was not run and why
   (gate-overlap → structural null).

## Success criteria

- Arm C trials are genuinely single-shot: the working dir is captured **before** any
  edit→check iteration. An arm-C record with `iterations_to_green > 0` is invalid.
- The escaped-defect recovery effect is reported against the variance it must beat;
  a skill that matches `C_no_skill` within variance is `CUT`, not "no harm".
- The **judge-bias caveat is stated**: `code-review-excellence` is *also* the judge's
  review standard (rubric §4). Measuring it as a subject while it underpins the judge
  risks self-preference — cite `ai-regression-testing`'s judge-bias warning and rely
  on the objective `oracle_failures` metric, not `rubric_*`, for its verdict.
- Verdicts written back to the ledger's per-skill table.

## Out of scope

Other cohorts; re-running arm A (reuse T-SE-3 records); adding new schema fields
(use `extra`); editing the rubric/contract (frozen in T-SE-0).

## Signal/noise consumer

`oracle_failures` and `single_shot_pytest_failures` are read by **this report's**
recovery computation and consumed by **T-SE-FINAL**'s arm-C verdict line; they live
in the existing `extra` dict (metrics_schema §5), so no new top-level field ships.
The verdicts feed T-SE-FINAL's KEEP/TRIM/CUT table.

## Verification

- For one arm-C trial, hand-confirm the recorded `oracle_failures` by running the
  oracle against the captured single-shot dir.
- Confirm `C_no_skill` and `C_skill` used the **same** corpus task, seed set, and
  single-shot protocol (matched arms).
- Recompute one recovery-vs-bar decision by hand.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-5.md`, opening with `## Plan`.)
