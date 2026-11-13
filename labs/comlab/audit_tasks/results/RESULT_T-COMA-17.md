# Result

## Status
completed

## Summary
An INVALID gas sample stays scored on the default path, with `LOW_CERTAINTY` and reason `GAS_SAMPLE_INVALID`. EXTERNAL_O2_SUSPECT carries `GAS_SAMPLE_O2_SUSPECT` and no longer aborts with fatal gates on. The UI shows one notice per reason. ADR-0007 has the amendment.

## Files changed
`lab_pipeline_aggregator.py`, `vocabulary.py`, `apps/ui/ui_payload.py`, ADR-0007, two new tests (commit 7337c0e); the note and this RESULT.

## Commands executed
`git apply rehearsal.patch`; `cp` and `cmp` of the two tests; Verification steps 1-5; R5 stash run and four mutants (see the note).

## Validation evidence
- Base (P1): comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`; probes `2 failed`.
- After: comlab `517 passed, 4 skipped`; wired `176 passed`; ui `73 passed`; new tests `7 passed` and `3 passed`.
- Probes: `INVALID -> LC-002 lean_condition True FULL_FUSION`, `1 failed, 1 passed, 9 deselected`.
- v7 corpus: `changed 0 of 314`.
- ruff `All checks passed!`; diff stat `6 files changed, 177 insertions(+), 8 deletions(-)`.
- R5: base `3 failed, 4 passed` and `2 failed, 1 passed`; mutants A `3 failed, 4 passed`, B, C, D each `1 failed, 6 passed`.

## Criteria
1. MET: steps 1-4 and R5 counts as named.
2. MET: ruff clean, P2 diff stat, one new commit 7337c0e after spec commit 61b6d61, `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- The commit has no co-author trailer: `bash_guard` refused the commit command with it.

## Pre-existing changes preserved
none (clean start).

## Rollback
`git -C repo revert 7337c0e` on `fix/T-COMA-17`, or reset the branch to 61b6d61 (task branch only).

## Remaining risks or uncertainties
The F-C1-13 audit probe still fails by R1 design. pyright was not run: the task did not require it (`NOT RUN`).

Branch: fix/T-COMA-17
Log (`git log --oneline 1046999..HEAD`):
7337c0e fix(T-COMA-17): INVALID gas sample scored at LOW_CERTAINTY with a notice; O2-suspect continues (F-C1-13, F-C1-14)
61b6d61 coma: spec(T-COMA-17): INVALID gas sample scored at LOW_CERTAINTY with a notice; O2-suspect continues (F-C1-13, F-C1-14)
