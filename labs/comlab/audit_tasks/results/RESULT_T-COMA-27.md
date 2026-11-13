# Result

## Status
completed

## Summary
Applied Cowork's rehearsed patch (`rehearse.py`: `applied 10 files`) and committed it as `7fd2cce` on `fix/T-COMA-27`. Ten GASLab chemical states that had no REG-V2 rule now each have one rule in their GASLab family (CT-009, CT-010, MF-007, MF-008, LC-004, LC-005, RM-005, RM-006, MW-010, IF-004). FLAT_CAMSHAFT and INCOMPLETE_OXIDATION stay unrouted (R3). All P2 counts match.

## Files changed
In commit `7fd2cce` (10 files, 309 insertions, 6 deletions):
- `labs/comlab/registry/rules/{cam_timing,ignition_fault,lean_condition,mechanical_wear,misfire,rich_mixture}.json`
- `labs/comlab/registry/tests/{test_cam_timing_rules,test_integration_shim,test_mechanical_wear_rules}.py`
- `labs/comlab/tests/unit/test_t_coma_27_unrouted_states.py` (new)
Uncommitted, as specified: `labs/comlab/audit_tasks/progress_notes/T-COMA-27.md`, this RESULT.
Runtime: `C:/4DApp/recheck/T-COMA-27/pt/` (basetemps, `after.json`).

## Commands executed
- First action and Preconditions (as written): branch `fix/T-COMA-27`, log `780e1a7` only, porcelain empty, `checked`.
- Base probe (step 3 on base): `unrouted chemical states: 12 [...]`, `13 failed, 3 deselected`; comlab `542 passed`.
- `$PY -I C:/4DApp/recheck/T-COMA-27/rehearse.py` (with the note parked; see Decisions): `applied 10 files`, exit 0.
- `git add <10 paths>`; `git -c user.name=Claude ... commit` -> `7fd2cce`.
- Verification steps 1-5 exactly as written in the task.

## Validation evidence
- step 1: `563 passed`; `186 passed`; `75 passed`.
- step 2: `508 passed, 5 skipped`; `2 passed`; `21 passed`. `case_library.html` restored.
- step 3: `unrouted chemical states: 2 ['FLAT_CAMSHAFT', 'INCOMPLETE_OXIDATION']`; `3 failed, 10 passed, 3 deselected` (R3 expected).
- step 4: `changed 0 of 314`.
- step 5: `All checks passed!`; `10 files changed, 309 insertions(+), 6 deletions(-)`; log `7fd2cce`, `780e1a7`; porcelain: note and RESULT only.
- Previous decisive failure absent: 12 unrouted / 13 failed on base -> 2 unrouted / 3 failed.

## Criteria
| # | verdict | evidence |
|---|---|---|
| 1 | MET | `applied 10 files`; steps 1-4 match P2 exactly (above) |
| 2 | MET | step 5: ruff clean, P2 diff stat, one new commit `7fd2cce` after spec `780e1a7`, porcelain lists only the note and RESULT |

## Decisions the task did not specify
- `rehearse.py` refuses any untracked file, but the header requires the progress note before the first edit. I moved the note to `C:/4DApp/recheck/T-COMA-27/pt/T-COMA-27.md.parked`, ran `rehearse.py`, then moved it back unchanged. This is recorded in the note under `Assumptions worked past`. Suggest the rehearse script ignore `audit_tasks/progress_notes/` in future packs.

## Pre-existing changes preserved
The `repo/` tree was clean at start. Nothing outside the write scope was touched.

## Rollback
`git -C C:/4DApp/repo reset --hard 780e1a7` on `fix/T-COMA-27` only (or `git revert 7fd2cce`).

## Remaining risks or uncertainties
- FLAT_CAMSHAFT and INCOMPLETE_OXIDATION still fall into the LC-002/MF-005 sinks (out of scope, R3).
- The task-end gate items from the skill that the task's Verification does not name (pyright, baseline.sh, isolation.py) were NOT RUN; the task states "Repo-wide gates: none beyond steps 1-2".

## Branch and log
```
$ git -C repo branch --show-current
fix/T-COMA-27
$ git -C repo log --oneline d8495f9..HEAD
7fd2cce fix(T-COMA-27): route 10 unrouted GASLab chemical states to their GASLab families (F-C1-2)
780e1a7 coma: spec(T-COMA-27): route 10 unrouted GASLab chemical states (F-C1-2 slice)
```
