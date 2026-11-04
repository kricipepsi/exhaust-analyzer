# Result

## Status
completed

## Summary
R1-R6 applied with `make_rh.py`. The COMLab, registry and vault-live ledgers no longer offer finished rows as `pending`.

## Files changed
- `labs/comlab/tasks/PROGRESS.md`, `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`, `apps/vault/VAULT_LIVE_PROGRESS.md`
- Note and this RESULT.

## Commands executed
- First action and Preconditions (clean).
- `make_rh.py .` (R1-R6), the D3 probe before and after (`PYTHONUTF8=1`), `git checkout -- audit/scratch/D3/out/` after each run.
- `git add` by path, then the commit.

## Validation evidence
- Step 1: `(no pending row)` 52, `'pending': 2`, both ledgers `(no pending row)`.
- Step 2: `:NOT-FOUND` 3, `FAIL` for the two ledgers 0.
- Step 3: diff stat `3 files changed, 6 insertions(+), 6 deletions(-)`; `git status --porcelain` lists only the note and this RESULT.
- Branch: `fix/T-AUD-7c`
- `git log --oneline 6ce31ba..HEAD`:
  - `b163201 docs(T-AUD-7c): mark finished COMLab, registry and vault-live ledger rows done`
  - `80d5f1f audit: T-AUD-7c spec (F-D3-2, F-D3-3 stale pending rows); vina: T-VINA-11 closed by measurement, T-VINA-11b registered`

## Criteria
1. MET with offset: both ledgers print `(no pending row)`; `'pending': 2`, not 1 (see Decisions).
2. MET: 3 `:NOT-FOUND`, 0 `FAIL` for the two ledgers.
3. MET: one `docs(T-AUD-7c):` commit, 3 ledgers, P2 diff stat; status lists only note and RESULT.

## Decisions the task did not specify
- The spec numbers (`pending` 1, count 53) are one off from the probe (2, 52). The spec commit added the `T-AUD-7c` row (`apps/wired/audit_tasks/PROGRESS.md:21`), which the probe counts as pending. I accepted the offset and did not edit that ledger.
- The commit has no attribution trailer, because `bash_guard` refused the command that held it.
- I wrote the edits before the readiness lines. The edits are in scope and reversible.

## Pre-existing changes preserved
None existed. The tree was clean.

## Rollback
`git revert b163201` on `fix/T-AUD-7c`, or reset the branch to `80d5f1f`.

## Remaining risks or uncertainties
None beyond the count offset. The ledger row stays `pending` for Cowork.
