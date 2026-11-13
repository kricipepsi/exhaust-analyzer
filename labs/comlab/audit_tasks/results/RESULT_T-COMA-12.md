# Result

## Status
completed

## Summary
R1-R3 applied in `fault_atlas_router.py`: one discriminator lift per family (`_discriminator_families`), float-safe abstain margin (`_MARGIN_EPSILON`, `_within_abstain_margin`, both sites), override regex `^P030[0-9]$`. New test added.

## Files changed
- `labs/comlab/comlab/core/fault_atlas_router.py` (modified)
- `apps/wired/tests/test_t_coma_12_lift_margin_p030x.py` (created, `cmp`-identical to Cowork's copy)
- `labs/comlab/audit_tasks/progress_notes/T-COMA-12.md`, this RESULT (created)

## Commands executed
`rehearse.py` (printed `applied`), Verification steps 1-5, and R5 (stash base run, two mutants), all as the task states.

## Validation evidence
- P1 on base: comlab `510 passed, 4 skipped`; wired `143 passed`; ui `70 passed`; probes `2 failed, 1 passed`.
- After: comlab `510 passed, 4 skipped`; wired `156 passed`; ui `70 passed`; new test `13 passed`; probes `3 passed`; corpus `changed 0 of 314`; ruff `All checks passed!`; diff stat `2 files changed, 72 insertions(+), 13 deletions(-)`.
- R5: base `9 failed, 4 passed`; mutant A `4 failed, 9 passed`; mutant B `1 failed, 12 passed`.

## Criteria
1. MET: steps 1-4 and R5 counts as above.
2. MET: ruff clean, diff stat, one new commit 35f5230 after spec commit 55c92f9, porcelain lists only the note and this RESULT.

## Decisions the task did not specify
- The commit message has no co-author trailer: `bash_guard` refused any command whose text held the assistant's name.

## Pre-existing changes preserved
none (porcelain was empty at start).

## Rollback
On the task branch: `git revert 35f5230`.

## Remaining risks or uncertainties
The F-C1-18 audit probe passes without exercising the lift (task Context); the new test pins it.

Branch: `fix/T-COMA-12`
Log (`101f042..HEAD`):
```
35f5230 fix(T-COMA-12): one discriminator lift per family; float-safe abstain margin; P0309 (F-C1-18/19/20)
55c92f9 coma: spec(T-COMA-12): one discriminator lift per family; float-safe abstain margin; P0309 (F-C1-18/19/20)
```
