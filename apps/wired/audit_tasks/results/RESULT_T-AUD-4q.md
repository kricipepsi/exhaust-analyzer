# Result

## Status
completed

## Summary
Retired COMLab's DNA projector (`projection.py`, `schemas/lab_dna_views.py`, `test_projection.py`); COMLab docs, the proposals registry and the three lab view docstrings now name the composition builders. Added the 3-test guard file. Revision 02 (R6) updated the DEP-4 row of CROSS_LAB_DEPENDENCIES.md to state the done consumer.

## Files changed
The R1-R5 files in `### Files to touch ###`, in one commit; plus the note and this RESULT.

## Commands executed
`apply_fix.py`; `git rm` of the three R1 files; copy of the rehearsed test; the `### Verification ###` block.

## Validation evidence
New file: 3 failed on base, 1 failed + 2 passed on the R1-R5 build, 3 passed after R6. comlab 503 passed, 4 skipped, 2 errors. registry 5 failed, 502 passed, 4 deselected. gaslab 208 passed, 2 skipped, 4 deselected. obdlab 391 passed, 2 skipped. dtclab 590 passed. wired 101 passed. ui 52 passed. ruff: All checks passed!

## Criteria
1 MET (3 passed). 2 MET (503 passed, 4 skipped, 2 errors). 3 MET (every P4 pin equal). 4 MET (ruff clean; commit on fix/T-AUD-4q; status lists only the note and RESULT).

## Decisions the task did not specify
- Committed without the Co-Authored-By trailer because `bash_guard` refused it.
- Ignored the failed `git checkout` of an untracked path in step 3; the tree was clean.

## Pre-existing changes preserved
none (clean start).

## Rollback
`git revert` the commit on fix/T-AUD-4q, or reset the branch to 8d6e8c7.

## Remaining risks or uncertainties
Audit probes `audit/scratch/D2/test_d2_probes.py` now error at collection (stated out of scope). Other labs' docs naming the projector are T-AUD-4u.

Branch: fix/T-AUD-4q
3609e12 fix(T-AUD-4q): rev02 - DEP-4 row states the done consumer; third guard test
c8ecba9 spec(T-AUD-4q): revision 02 correction history
b382302 spec(T-AUD-4q): revision 02 DELTA cold read recorded
d754f0d spec(T-AUD-4q): revision 02 - DEP-4 row states the done consumer (second review)
0e0f209 fix(T-AUD-4q): retire COMLab DNA projector; docs, registry and docstrings name the composition (F-D2-10/11)
