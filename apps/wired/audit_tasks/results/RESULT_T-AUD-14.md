# Result

## Status
completed

## Summary
Ran `recheck/T-AUD-14/apply_fix.py` from `repo`: VINLab HLD, LLD, DLD and VOCABULARY now state the decoder as it is; the two `model_year >= 1996` lines in `decoder.py` carry `# source: OBD-II mandate`; the `_resolve_wmi` docstring and LLD:109 say 12-14.

## Files changed
decoder.py, HLD_VINLab.md, LLD_VINLab.md, DLD_VINLab.md, VIN_VOCABULARY.md (all under `repo/labs/vinlab/`), plus the note and this RESULT. Commit 9de179d.

## Commands executed
First action; preconditions; census.sh (before and after); apply_fix.py; the `### Verification ###` steps 1-3; git add and commit.

## Validation evidence
- Before: `stale 7`, `cited 0`, flags `0 0 1`, `0 0 1`, `0 0 0`, `0 0 0` (the previous decisive failure).
- After: `stale 0`, `cited 2`, four flags `1 1 1`; `ast same labs/vinlab/vinlab/decoder.py`.
- `376 passed, 8 skipped in 7.81s`; ruff `All checks passed!`.

## Criteria
1. MET: step 1 output above.
2. MET: step 2 equals P3.
3. MET: ruff passes; commit 9de179d on fix/T-AUD-14 after spec e95c1fc; porcelain lists only the note and RESULT.

## Decisions the task did not specify
none

## Pre-existing changes preserved
none present (porcelain empty at start).

## Rollback
`git -C repo revert 9de179d` on fix/T-AUD-14, or reset the branch to e95c1fc.

## Remaining risks or uncertainties
Repo-wide gates (wired, ui, registry) NOT RUN; report-only, Cowork runs them.

Branch: fix/T-AUD-14
Log e95c1fc..HEAD: 9de179d docs(T-AUD-14): VINLab docs state the decoder as it is; KR6 citations on the 1996 literals
