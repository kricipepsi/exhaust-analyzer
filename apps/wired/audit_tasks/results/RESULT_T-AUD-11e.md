# Result

## Status
completed

## Summary
One drift report lists 47 findings for the GASLab design documents: all 8 documents are covered and 7 have findings, the BDD has 1. The main classes: stale counts (3 catch-all faults against 4 in the ontology, a 9-field `GasLabPayload` against 15), vocabulary entries with no code (`LambdaBand` discretiser, `GasBehavior`, `CatalystStatus`, `COLD_OPEN_LOOP_INVALID` handling, per-vehicle type-approval fields, `chemical_efficiency`, the logging and warning-string promises), thresholds that are literals where the documents say the YAML supplies them, and `confidence` read in `ranking.py` where the documents say it has one use.

## Files changed
- `audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md` (created, committed `499714a`)
- `apps/wired/audit_tasks/progress_notes/T-AUD-11e.md` (created, uncommitted)
- `apps/wired/audit_tasks/results/RESULT_T-AUD-11e.md` (created, uncommitted)

## Commands executed
- First action and Preconditions commands from the task.
- `check_report.py` before the report existed (`FileNotFoundError`), then after (`REPORT OK`).
- `cat -n`, `grep -n`, `grep -c`, `sed -n`, `awk` and `wc -l` on the P1 documents and P2 code.
- Each `Code: ABSENT` command, re-run one by one.
- `git add`, `git commit`, `git diff --name-only HEAD~1 HEAD`, `git log`, `git status --porcelain`.

## Validation evidence
- Step 1: `sections 8/8, findings 47, refs ok 80/80` / `REPORT OK`, exit 0.
- Step 2: `audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md` only.
- Step 3: `499714a`, `49ab697`, `ecf3c75`; `git status --porcelain` shows the note and this RESULT only.
- The previous decisive failure (report missing, `FileNotFoundError`) is gone.

## Criteria
1. MET: step 1 printed `sections 8/8`, `refs ok 80/80`, `REPORT OK`.
2. MET: step 2 listed the report only.
3. MET: commit `499714a` is on `fix/T-AUD-11e` after spec commit `49ab697`; `git status --porcelain` lists the note and this RESULT only.

## Decisions the task did not specify
- Where a document contradicts itself, only the line that disagrees with the code is reported.
- A count or absence claim with no single code line to quote uses the `Code: ABSENT (command -> output)` form, and the sentence states only what the command shows.
- The same stale count in several documents gives one finding for each document line, so a fix row can change each line.
- Doubtful cases are in the note under `Assumptions worked past`, not in the report.
- The commit has no co-author trailer: `bash_guard` refused the commit command while the trailer text was in it.

## Pre-existing changes preserved
`git status --porcelain` printed nothing at the start. No tracked file outside the report changed.

## Rollback
`git -C C:/4DApp/repo reset --hard 49ab697` is not allowed for an implementer. Cowork can drop the report with `git -C C:/4DApp/repo revert 499714a` on `fix/T-AUD-11e`, or delete the branch before the push.

## Remaining risks or uncertainties
- The report holds drift between documents and code only. A reviewer must confirm each finding before Cowork writes a fix row.
- Three findings depend on a reading of the document line: README:8 (mirror claim), HLD:37 (COMLab as the builder of the DNA view) and VOC:564 (invariant 7). The note records why.
- Several ontology comments cite GAS_VOCABULARY §10 tiers with values that differ from the tier. Only the NOx case is reported.

## Git
- `git -C repo branch --show-current`: `fix/T-AUD-11e`
- `git -C repo log --oneline 49ab697..HEAD`: `499714a docs(T-AUD-11e): GASLab drift report, 47 findings in 8 documents`
