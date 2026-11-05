# Result

## Status
completed

## Summary
One drift report lists 44 findings for the DTCLab design documents: 7 documents have findings, the README has none. The main classes: stale counts in the v2.0 reconciliation notes (18 tags, 3 `DtcEmissionsView` flags, 5 DNA-gated entries, 32 YAML entries, 6 symptom flags, 3 Mode $06 states, 3 named gates), the no-start state documented as a proposal but shipped, and the Wired adapter for the Phase-2 scorer that no `.py` file under `apps` or `labs/comlab` calls.

## Files changed
- `audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md` (created, committed `b103252`)
- `apps/wired/audit_tasks/progress_notes/T-AUD-11d.md` (created, uncommitted)
- `apps/wired/audit_tasks/results/RESULT_T-AUD-11d.md` (created, uncommitted)

## Commands executed
- First action and Preconditions commands from the task.
- `check_report.py` before the report existed (`FileNotFoundError`), then after (`REPORT OK`).
- `grep -n`, `grep -c`, `sed -n` and one `$PY -c` one-liner on the P1 documents and P2 code.
- `git add`, `git commit`, `git diff --name-only HEAD~1 HEAD`, `git log`, `git status --porcelain`.

## Validation evidence
- Step 1: `sections 8/8, findings 44, refs ok 77/77` / `REPORT OK`, exit 0.
- Step 2: `audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md` only.
- Step 3: `b103252`, `a4db998`, `759653a`; `git status --porcelain` shows the note and this RESULT only.
- The previous decisive failure (report missing, `FileNotFoundError`) is gone.

## Criteria
1. MET: step 1 printed `sections 8/8`, `refs ok 77/77`, `REPORT OK`.
2. MET: step 2 listed the report only.
3. MET: commit `b103252` is on `fix/T-AUD-11d` after spec commit `a4db998`; `git status --porcelain` lists the note and this RESULT only.

## Decisions the task did not specify
- Where a document contradicts itself, only the line that disagrees with the code is reported.
- A count claim with no single code line to quote uses the `Code: ABSENT (command -> output)` form with a `grep -c` command.
- Doubtful cases are in the note under `Assumptions worked past`, not in the report.
- The commit has no co-author trailer: `bash_guard` refused the commit command while the trailer text was in it.

## Pre-existing changes preserved
`git status --porcelain` printed nothing at the start. No tracked file outside the report changed.

## Rollback
Cowork drops the report with `git rm audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md` on `fix/T-AUD-11d`, or discards the branch before any push.

## Remaining risks or uncertainties
- Doubtful items were left out on purpose (see the note): the README `multi-DTC patterns` role line, the manufacturer-MID overlay wording, the `DTCState` exposure wording.
- The "no caller" claims show only that `classify_top3` and `rank_candidates` appear in no `.py` file under `apps` and `labs/comlab`; they say nothing about other places.

## Git
Branch: `fix/T-AUD-11d`

`git log --oneline 759653a..HEAD`:
```
b103252 docs(T-AUD-11d): DTCLab drift report, 44 findings in 7 documents
a4db998 spec(T-AUD-11d): DTCLab EGM drift report
```
