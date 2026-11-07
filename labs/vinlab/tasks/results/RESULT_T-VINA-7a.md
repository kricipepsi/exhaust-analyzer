# Result

## Status
completed

## Summary
`lookup_engine_ref` now closes both sqlite connections it opens (`contextlib.closing`), and `_compute_confidence` returns `NONE` for `wmi_brand_missing`. The vocabulary, the HLD and the one old `PARTIAL` test follow. A new test file pins both.

## Files changed
- `labs/vinlab/vinlab/db/tecdoc_query.py`, `labs/vinlab/vinlab/decoder.py`, `labs/vinlab/docs/VIN_VOCABULARY.md`, `labs/vinlab/docs/HLD_VINLab.md`, `labs/vinlab/tests/unit/test_decoder.py` (modified)
- `labs/vinlab/tests/unit/test_t_vina_7a_connections_and_grade.py` (created, copied from Cowork's file, `cmp` identical)
- `labs/vinlab/tasks/progress_notes/T-VINA-7a.md`, this file (created)

## Commands executed
`apply_fix.py` (`-I`, from `repo`); `cp` + `cmp` of the test; Verification steps 1-4; the R4 stash and mutant runs; one `git commit` by explicit path.

## Validation evidence
- Base (new test present): vinlab `4 failed, 389 passed, 8 skipped`; probes `2 failed, 1 passed, 48 deselected` (3 `unclosed database` warnings).
- After: vinlab `393 passed, 8 skipped`; wired `113 passed`; ui `70 passed`; step 2 `61 passed, 2 skipped`; step 3 `3 passed, 48 deselected`; ruff `All checks passed!`.
- R4 base `4 failed, 57 passed, 2 skipped`; R4 mutant `1 failed, 60 passed, 2 skipped`, restored, `git diff --stat` unchanged.
- `git diff --stat 0552976 HEAD -- labs/vinlab/vinlab labs/vinlab/docs`: `4 files changed, 10 insertions(+), 7 deletions(-)`.

## Criteria
1. MET: steps 1-3 and R4 counts above match P2, P3 and R4.
2. MET: ruff clean; P2 diff stat; one new commit fba4eb4 after the spec commit f621680; `git status --porcelain` showed only the note before this RESULT was written.

## Decisions the task did not specify
- The commit has no `Co-Authored-By` trailer: the first attempt, chained with the trailer, was refused by `bash_guard`.
- pyright and `ruff --select S` not run: Verification does not name them.

## Pre-existing changes preserved
None existed: `git status --porcelain` was empty at the start.

## Rollback
Cowork drops fba4eb4 from `fix/T-VINA-7a`, or `git revert fba4eb4`.

## Remaining risks or uncertainties
None found. Repo-wide gates (comlab, dnalab): NOT RUN, report-only, Cowork runs them.

Branch: `fix/T-VINA-7a`
```
fba4eb4 fix(T-VINA-7a): lookup_engine_ref closes its connections; a blank-brand WMI grades NONE (F-C6-14, F-C6-9)
f621680 vina: spec(T-VINA-7a): vref.db connections close; a blank-brand WMI grades NONE; T-VINA-7 split 7a-7c
```
