# Result

## Status
completed

## Summary
`integration_shim.py` no longer scores a trim whose own source reports an open fuel loop (`OL`, `OL_DRIVE`, `OL_FAULT`), live or freeze-frame. The edit is `rehearse.py` (R1-R3); the new test is copied from Cowork's file.

## Files changed
- `labs/comlab/registry/integration_shim.py` (+14 -3)
- `apps/wired/tests/test_t_coma_13_open_loop_trims.py` (new, 52 lines)
- `labs/comlab/audit_tasks/progress_notes/T-COMA-13.md`, this RESULT (new)

## Commands executed
First action and preconditions; `cp` + `cmp` of the test; `rehearse.py` (`applied`); R4 stash and mutants; Verification steps 1-5; one commit by explicit path.

## Validation evidence
- comlab `510 passed, 4 skipped`; wired `167 passed`; ui `70 passed`.
- New test: base `7 failed, 4 passed`; mutant A and B `4 failed, 7 passed`; final `11 passed`.
- Probe: `CL -> LC-001 lean_condition 0.95`, `OL_FAULT -> OPTIMAL_HEALTH no_fault 0.0`, `1 passed` (base: `OL_FAULT -> LC-001 lean_condition 0.95`, `1 failed`).
- v7 corpus `changed 0 of 314`. ruff `All checks passed!`. Diff stat `2 files changed, 66 insertions(+), 3 deletions(-)`.

## Criteria
1. MET: steps 1-4 and R4 counts above.
2. MET: step 5 output above; one new commit fc7a3a2 after spec commit 798e079; status listed only the note before this RESULT.

## Decisions the task did not specify
- The commit message has no co-author trailer: `bash_guard` refused a command that held the trailer text.

## Pre-existing changes preserved
None existed (`git status --porcelain` empty at start).

## Rollback
`git revert fc7a3a2` on `fix/T-COMA-13`, or reset that branch to 798e079 (Cowork's call).

## Remaining risks or uncertainties
pyright and `ruff --select S` NOT RUN (not in the task's Verification).

## Git
```
fix/T-COMA-13
fc7a3a2 fix(T-COMA-13): trims reported in an open fuel loop are not scored (F-C1-8)
798e079 coma: spec(T-COMA-13): trims reported in an open fuel loop are not scored (F-C1-8)
```
