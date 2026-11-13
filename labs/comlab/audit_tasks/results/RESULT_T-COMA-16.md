# Result

## Status
completed

## Summary
Wiki 09 now has `## Abstain thresholds {#CONCEPT_ABSTAIN}` (floor 0.80, margin 0.02, margin epsilon, no_rule abstention, each with its source), one graph-relation line and one core-entity line. `ABSTAIN_FLOOR` and `ABSTAIN_MARGIN` cite it. No behaviour change.

## Files changed
- labs/comlab/wiki/09_calibration_confidence.md
- labs/comlab/comlab/core/fault_atlas_router.py (comments only)
- the progress note and this RESULT

## Commands executed
`cd repo && python -I C:/4DApp/recheck/T-COMA-16/rehearse.py` (read first); the three pytest suites, the greps, ruff and git checks from `### Verification ###`, run before and after the edit; `git add` of the two paths, then the commit.

## Validation evidence
Before (P1): comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`; CONCEPT_ABSTAIN count 0.
After (P2): the same three counts; CONCEPT_ABSTAIN count 3; constant-line grep 2; ruff `All checks passed!`; diff stat `2 files changed, 21 insertions(+), 3 deletions(-)`.

## Criteria
1. MET: step 1-2 output above.
2. MET: ruff clean, the P2 diff stat, one new commit 7041573 after spec commit 6181853. `git status --porcelain` lists only the note and RESULT (checked after writing them).

## Decisions the task did not specify
- The commit message has no co-author trailer: bash_guard refuses a command whose text holds the agent's name, and AGENTS.md says a trailer counts.
- Readiness lines were written after the edit but before the commit (see the note).

## Pre-existing changes preserved
none (clean start state).

## Rollback
`git revert 7041573` on fix/T-COMA-16, or reset that branch to 6181853. Nothing touched `main`.

## Remaining risks or uncertainties
- The floor's inertness (0/297) is documented, not fixed: out of scope.
- The §6 heading of the TOPK report was not checked, only the quoted line.

branch: fix/T-COMA-16
log (127c19e..HEAD):
7041573 docs(T-COMA-16): abstain thresholds get wiki 09 CONCEPT_ABSTAIN and the constants cite it (F-D1-12)
6181853 coma: spec(T-COMA-16): abstain thresholds documented in wiki 09 and cited (F-D1-12)
