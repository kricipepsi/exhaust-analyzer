# Result

## Status
completed

## Summary
Both `ExecutionMeta` builders in `LabPipelineAggregator.process` now set `vin_confidence=request.metadata.vin_confidence.value`. Two new tests pin it.

## Files changed
- labs/comlab/comlab/core/lab_pipeline_aggregator.py (2 lines)
- apps/wired/tests/test_t_coma_8_vin_confidence_echo.py (new)
- labs/comlab/tests/unit/test_t_coma_8_vin_confidence_paths.py (new)
- the progress note and this RESULT

## Commands executed
`apply_fix.py` (`$PY -I`), `cp` + `cmp` of the two tests, `### Verification ###` steps 1-4, R3 stash and mutant runs, `git commit` by explicit path.

## Validation evidence
Base: comlab 508 passed 4 skipped; wired 121; ui 70; probe `in: PARTIAL  out: HIGH`, 1 failed.
After: comlab `510 passed, 4 skipped`; wired `123 passed`; ui `70 passed`; new tests `2 passed` each (`2 failed` each on base); probe `in: PARTIAL  out: PARTIAL`, `1 passed, 6 deselected`; ruff `All checks passed!`; diff stat `1 file changed, 2 insertions(+), 2 deletions(-)`.
Mutant (second site reverted): comlab paths test `1 failed, 1 passed`.

## Criteria
1. MET: steps 1-3 and R3 as above.
2. MET: step 4 output as above; one new commit 40dc1cc; `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- Used apply_fix.py's replacement line, which adds a trailing comment to the bare line R1 shows.
- Committed without the co-author trailer because `bash_guard` refused it.
- P2's v7 corpus check (314 of 314) is not in `### Verification ###`: NOT RUN.

## Pre-existing changes preserved
None in `repo/`; status was clean at start.

## Rollback
`git revert 40dc1cc` on `fix/T-COMA-8`.

## Remaining risks or uncertainties
PARTIAL-decode degradation and the verdict confidence cap stay out of scope (T-AUD-2).

Branch: fix/T-COMA-8
```
40dc1cc fix(T-COMA-8): execution_meta.vin_confidence echoes the decode grade (F-C1-9)
26d27fd coma: spec(T-COMA-8): execution_meta.vin_confidence echoes the decode grade (F-C1-9)
```
