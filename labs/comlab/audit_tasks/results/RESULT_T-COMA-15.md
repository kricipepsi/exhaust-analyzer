# Result

## Status
completed

## Summary
The O2 bias label now follows the lean/rich direction: delta > tolerance gives `O2_SENSOR_BIASED_LOW`, delta < -tolerance gives `O2_SENSOR_BIASED_HIGH`. SF-001 now fires on `lt -0.03` and SF-002 on `gt 0.03`. The three pins that encoded the inversion were swapped and a new test was added.

## Files changed
labs/comlab/comlab/core/perception_contradiction.py; labs/comlab/registry/rules/sensor_fault.json; labs/comlab/tests/unit/test_perception_contradiction.py; labs/comlab/tests/e2e/test_real_routing.py; apps/wired/tests/test_oil_cases.py; apps/wired/tests/test_t_coma_15_o2_bias_direction.py (new); the progress note; this RESULT.

## Commands executed
Task First action and Preconditions; `rehearse.py` from `repo`; `cp` and `cmp` of the test; Verification steps 1-5; R5 base run and mutants A and B; the commit.

## Validation evidence
- Base P1: comlab `510 passed, 4 skipped`; wired `170 passed`; ui `70 passed`.
- After: comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`; new test `6 passed`.
- Step 3: line 222 `O2_SENSOR_BIASED_LOW`, line 231 `O2_SENSOR_BIASED_HIGH`.
- Step 4: `vs before 18 of 314`, `vs expected 0 of 314`.
- Step 5: `All checks passed!`; `6 files changed, 76 insertions(+), 35 deletions(-)` (e8f1e84).
- Correction 1 (R6, R7): base `2 failed, 4 passed` with the corrected test; after: comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`; new test `6 passed`; corpus `vs before 18 of 314`, `vs expected 0 of 314`; ruff `All checks passed!`; `git diff --stat e8f1e84 HEAD` `2 files changed, 10 insertions(+), 7 deletions(-)`.
- Previous decisive failure absent: the new test was `4 failed, 2 passed` on base and is `6 passed` now.
- R5: base `4 failed, 2 passed`; mutant A `2 failed, 4 passed`; mutant B `2 failed, 4 passed`. Restored, diff stat `5 files changed, 36 insertions(+), 35 deletions(-)` before the commit.

## Criteria
1. MET: steps 1-4 counts as pinned; R5 results as pinned.
2. MET: ruff clean, P2 diff stat, one new commit c2212f5 after the correction spec commit c651f31 (R1-R5 in e8f1e84); correction 1 R6 and R7 MET as in Validation evidence, `git status --porcelain` showed only the note before this RESULT was written.

## Decisions the task did not specify
- R5 base run: I ran the new test on the unedited base before `rehearse.py` instead of using `git stash`; the code state is identical and the repo was clean.
- Mutants were restored by copy from `C:/4DApp/recheck/T-COMA-15/pt/*.bak` (a scratch location), then `cmp` checked.
- The commit message has no co-author trailer: `bash_guard` refused the command when the trailer text was present (AGENTS.md § git).

## Pre-existing changes preserved
none present in `repo` (status was empty at start).

## Rollback
`git -C repo reset` is not allowed here; Cowork reverts with `git revert e8f1e84` on `fix/T-COMA-15`, or discards the branch.

## Remaining risks or uncertainties
- e2e mock names `sensor_biased_high()` and `sensor_biased_low()` now disagree with their labels (out of scope, recorded).
- Rule descriptions' remaining wording (SF-001 "slow/lazy response"), KG and UI copy are later rows.

Branch: fix/T-COMA-15
Log `68dd691..HEAD`:
c2212f5 fix(T-COMA-15): SF-001/SF-002 descriptions state the corrected lean/rich direction (correction 1)
c651f31 coma: spec(T-COMA-15): correction 1 - SF-001/SF-002 descriptions state the corrected direction (second review)
e8f1e84 fix(T-COMA-15): O2 bias label and SF-001/SF-002 delta rows follow the lean/rich direction (F-D2-1)
4de9540 coma: spec(T-COMA-15): O2 bias direction in the perception label and SF-001/SF-002 rows (F-D2-1)
