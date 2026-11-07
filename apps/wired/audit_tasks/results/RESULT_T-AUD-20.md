# Result

## Status
completed

## Summary
`classify()` returns `(SAMPLE_INVALID, INVALID)` for `COLD_OPEN_LOOP_INVALID` right after the CRANKING step. `GAS_VOCABULARY.md` §7 states the shipped behaviour. New test file added.

## Files changed
- labs/gaslab/gaslab/rule_engine.py
- labs/gaslab/docs/GAS_VOCABULARY.md
- labs/gaslab/tests/unit/test_cold_open_loop.py (new)
- apps/wired/audit_tasks/progress_notes/T-AUD-20.md, results/RESULT_T-AUD-20.md (new)

## Commands executed
The task's `### Verification ###` steps 1-3, plus `apply_fix.py`, plus a red run of the new tests before the fix.

## Validation evidence
- Red (before fix): `3 failed, 1 passed`; lab suite without new file `215 passed, 2 skipped, 4 deselected`.
- New tests: `4 passed`. Lab suite: `219 passed, 2 skipped, 4 deselected`. ruff: `All checks passed!`.
- Corpus: `corpus 314`, `differ 0`. Wired: `106 passed`. Census: `notimpl 8`.

## Criteria
1. MET: step 1 outputs above.
2. MET: step 2 outputs above.
3. MET: commit on fix/T-AUD-20 after 5aa3528; porcelain shows only the note and RESULT (checked at finish line).

## Decisions the task did not specify
- The commit has no Co-Authored-By trailer: `bash_guard` refused the command that carried it, so I committed with the AGENTS.md form only.

## Pre-existing changes preserved
none (clean start).

## Rollback
`git revert` of the commit on fix/T-AUD-20, or reset the branch to 5aa3528 by the operator.

## Remaining risks or uncertainties
Repo-wide gates (ui, registry) NOT RUN; Cowork runs them at review.

Branch: fix/T-AUD-20
Log (5aa3528..HEAD): see below.
dcd910f fix(T-AUD-20): GASLab rejects a COLD_OPEN_LOOP_INVALID sample (GAS_VOCABULARY §7)
