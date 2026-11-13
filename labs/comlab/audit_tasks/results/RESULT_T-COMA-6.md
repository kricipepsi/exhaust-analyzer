# Result

## Status
completed

## Summary
On NORMAL_OPERATION gas a registry rule now fires only with strict support (R1). A verdict where no rule fired abstains with `no_rule` (R2). Two old pins updated (R3). Applied with `rehearse.py`; test copied (R4).

## Files changed
integration_shim.py, fault_atlas_router.py, test_abstain_emit.py, apps/ui/tests/test_ui.py, apps/wired/tests/test_t_coma_6_firing_predicate.py (new); the note and this RESULT.

## Commands executed
Verification steps 1-5 as in the task; the base baseline run; `rehearse.py`; R5 base stash and mutants A and B.

## Validation evidence
Base: comlab `510 passed, 4 skipped`; wired `127 passed`; ui `70 passed`; probes `3 failed, 13 deselected` (first verdict `LC-002`).
After: comlab `510 passed, 4 skipped`; wired `140 passed`; ui `70 passed`; new test `13 passed`; probes `3 passed, 13 deselected`, first verdict `verdict: OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH`; corpus `changed 0 of 314`; ruff `All checks passed!`; diff stat `5 files changed, 114 insertions(+), 4 deletions(-)`.

## Criteria
1. MET: steps 1-4 as above; R5 base `9 failed, 4 passed`, mutant A `1 failed, 12 passed`, mutant B `2 failed, 11 passed`.
2. MET: ruff clean, P2 diff stat, one new commit `9e0df5d` after the spec commit, `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- Step 1 restore path: used `labs/comlab/registry/docs/case_library.html`; the task's `labs/comlab/registry/case_library.html` does not exist.
- The commit has no Co-Authored-By trailer: `bash_guard` refused every commit command that held that line.
- Mutants restored by copying a saved good shim (in `recheck/T-COMA-6/pt/`), because `git restore` would drop the uncommitted edit; `cmp` confirmed identical.

## Pre-existing changes preserved
None existed (`git status --porcelain` was empty at start).

## Rollback
`git revert 9e0df5d` on `fix/T-COMA-6` (or reset the branch to `8f1690b`).

## Remaining risks or uncertainties
Out-of-scope F-C1-2 (13 `test_unrouted_state_*` probes) unchanged. Context percentage ABSENT.

Branch: `fix/T-COMA-6`
Log (`49214a9..HEAD`):
```
9e0df5d fix(T-COMA-6): strict support on NORMAL_OPERATION gas; no-fire verdict abstains no_rule
8f1690b coma: spec(T-COMA-6): on NORMAL_OPERATION gas a rule needs strict support; no-fire abstains (F-C1-1)
```

## Correction 1 (R6, R7)
Status: completed. R6 changes `_strict_support`: a NORMAL_OPERATION chemistry row stays a row but is never satisfied support, and a GATING NORMAL row is not the chemistry anchor. Applied with `correct1.py`; the test file was replaced by the `_c1` copy (`cmp` ok).
- R7 base: `3 failed, 13 passed` before `correct1.py`.
- After: comlab `510 passed, 4 skipped`; wired `143 passed`; ui `70 passed`; new test `16 passed`; probes `3 passed, 13 deselected`, first verdict `verdict: OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH`; corpus `changed 0 of 314`; ruff `All checks passed!`; `git diff --stat 9e0df5d HEAD -- labs/comlab/registry labs/comlab/comlab labs/comlab/tests apps` is `2 files changed, 26 insertions(+), 6 deletions(-)`.
- Criteria: 1 MET (steps 1-4, R7). 2 MET (ruff, diff stat, one new commit `c086c3e`, status lists only the note and RESULT).
- Decision: the commit has no Co-Authored-By trailer (`bash_guard` refused it).
- Files changed: `integration_shim.py`, `test_t_coma_6_firing_predicate.py`; the note and this RESULT.

Branch: `fix/T-COMA-6`
```
c086c3e fix(T-COMA-6): correction 1 - a NORMAL chemistry row is never strict support nor the chemistry anchor
118f675 coma: spec(T-COMA-6): correction 1 - a NORMAL chemistry row stays a row but is never support (second review)
9e0df5d fix(T-COMA-6): strict support on NORMAL_OPERATION gas; no-fire verdict abstains no_rule
8f1690b coma: spec(T-COMA-6): on NORMAL_OPERATION gas a rule needs strict support; no-fire abstains (F-C1-1)
```
