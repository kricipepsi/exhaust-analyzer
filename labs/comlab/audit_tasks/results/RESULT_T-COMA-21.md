# Result

## Status
completed

## Summary
Applied Cowork's rehearsal patch (R1-R3) and the new unit test (R4). `degradation_mode` is `GAS_DOMINANT` when OBD data is absent or suppressed. `processing_confidence_rating` is the band of the verdict score, capped under `GAS_DOMINANT`.

## Files changed
- labs/comlab/comlab/core/lab_pipeline_aggregator.py
- labs/comlab/tests/regression/fixtures/case_020_misfire.json
- labs/comlab/docs/COMLab_BDD.md
- labs/comlab/tests/unit/test_t_coma_21_mode_and_rating.py (new)
- labs/comlab/audit_tasks/progress_notes/T-COMA-21.md and this file (new, uncommitted)

## Commands executed
The task's `### Verification ###` steps 1-5 on the base and on the patch; the R5 stash run and five mutants; `git apply`, `cp`, `cmp`; one commit.

## Validation evidence
- Base: comlab `527 passed, 4 skipped`; wired `186 passed`; ui `73 passed`; step 3 `4 failed`.
- After (before correction 1): comlab `538 passed, 4 skipped`; wired `186 passed`; ui `73 passed`; step 2 `11 passed` (base `10 failed, 1 passed`); step 3 `4 passed`; step 4 `changed 0 of 314`.
- ruff `All checks passed!`; diff stat `4 files changed, 110 insertions(+), 23 deletions(-)`.
- R5: five mutants each `1 failed, 10 passed`; restored file identical to the patched one.

## Criteria
1. MET: steps 1-4 and R5 counts as listed above.
2. MET: ruff clean, the P2 diff stat, one new commit 3ed6cb0 on `fix/T-COMA-21` after spec commit c988cb9; `git status --porcelain` listed only the note (the RESULT is the second path).

## Decisions the task did not specify
- The commit has no attribution trailer, because `bash_guard` refuses the command when the trailer is present.

## Pre-existing changes preserved
none present (clean start).

## Rollback
`git revert 3ed6cb0` on `fix/T-COMA-21`.

## Remaining risks or uncertainties
- pyright and `ruff --select S`: NOT RUN (not required by the task).
- P4 (tier accuracy) is Cowork's and was not rerun.

## Correction 1
- R6 applied (`correction1.patch`; test `cmp` identical to the `_c1` copy): the `_map_degradation` docstring and BDD row name the `suppress_gaslab` trigger and "gas and OBD only"; two tests added.
- After: comlab `540 passed, 4 skipped`; wired `186 passed`; ui `73 passed`; step 2 `13 passed`; step 3 `4 passed`; step 4 `changed 0 of 314`; ruff `All checks passed!`; diff stat `4 files changed, 126 insertions(+), 23 deletions(-)`.
- R7: mutant F `1 failed, 12 passed`; mutant G `1 failed, 12 passed`; file restored, `cmp` identical.
- Criteria 1 and 2 (revised): MET, by the figures above; one new commit c176043 on `fix/T-COMA-21`; `git status --porcelain` lists only the note and this file.
- Rollback for correction 1: `git revert c176043`.
- Decision: the commit has no attribution trailer; `bash_guard` refuses it.

Branch: `fix/T-COMA-21`
```
c176043 fix(T-COMA-21): correction 1, name the suppress_gaslab trigger; two tests
9d47a65 coma: spec(T-COMA-21) correction 1: name suppress_gaslab; two tests
3ed6cb0 fix(T-COMA-21): degradation_mode reflects OBD absence; rating is the verdict score band (F-C1-11, F-C1-12)
c988cb9 coma: spec(T-COMA-21): degradation_mode = lab completeness; rating = score band (F-C1-11, F-C1-12)
```
