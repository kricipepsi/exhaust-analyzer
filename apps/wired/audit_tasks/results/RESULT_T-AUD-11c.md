# Result

## Status
completed

## Summary
One drift report for VINLab: 8 sections in P1 order, 20 findings (README 1, PRD 1, HLD 7, LLD 4, DLD 6, VIN_VOCABULARY 1; BDD and ADR: none). Each finding quotes the document line and the code line.

## Files changed
- `repo/audit/drift/2026-11-05_DRIFT_REPORT_vinlab.md` (new, committed `6f0ffc9`)
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-11c.md` (new, uncommitted)
- `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-11c.md` (new, uncommitted)

## Commands executed
- First action and Preconditions (clean tree, `checked`).
- Reads of the 8 documents and of `labs/vinlab/vinlab/**/*.py`, the three callers, the data CSV headers.
- `git ls-files labs/vinlab/mysql_data`, `ls`, `grep -n` for line anchors.
- Verification steps 1 to 3, then the commit by explicit path.

## Validation evidence
- Step 1: `sections 8/8, findings 20, refs ok 38/38`, `REPORT OK`, exit 0.
- Step 2: `audit/drift/2026-11-05_DRIFT_REPORT_vinlab.md` only.
- Step 3: `6f0ffc9`, `fcc2516`, `3e20cf3`; `git status --porcelain` lists only the note (and this RESULT).

## Criteria
1. MET - step 1 output above (both N equal: 38/38).
2. MET - step 2 lists the report only.
3. MET - `6f0ffc9` sits on `fix/T-AUD-11c` after the spec commit `fcc2516`; status lists only the note and the RESULT.

## Decisions the task did not specify
- Doubtful cases kept out of the report and listed in the note: `rated_rpm` provenance (build script reads `P14_rated_rpm` into `vref.db`), dead `H4Bt` entry, unused `open_vref_readonly`, `__init__` docstring 1990-2020, unset `downstream_trim_role`/`has_catalyst`.
- `mysql_data/` reported once, under the README, with `Code: ABSENT`.
- The HLD caller finding is `DIVERGENCE` (the document names COMLab as a caller; no `labs/comlab` file imports `vinlab`).
- The commit has no attribution trailer: `bash_guard` refused the command while the message held it.

## Pre-existing changes preserved
none in `repo/` (clean tree at start). `C:/4DApp` loop-pack changes untouched.

## Rollback
Revert `6f0ffc9` on `fix/T-AUD-11c`, or drop the branch; nothing else changed.

## Remaining risks or uncertainties
- Line numbers are those of the 11b tip plus the spec commits.
- The `vref.db` contents were not queried (task rule), so column-level claims (for example the 13 CoC columns) are checked against the decoder only.
- BDD and ADR have no finding; the ADR-0008 "1990-2020 fleet" wording was judged narrative.

## Branch and log
```
fix/T-AUD-11c
6f0ffc9 docs(T-AUD-11c): VINLab EGM drift report
fcc2516 spec(T-AUD-11c): dispatch index
3e20cf3 spec(T-AUD-11c): VINLab EGM drift report
```
(`git -C repo log --oneline 972f3eb..HEAD`)
