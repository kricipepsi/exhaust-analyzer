# T-AUD-18c progress note

## Readiness
- (a) Start matches: branch `fix/T-AUD-18c`, base (spec commit) `74adb2d`, descendant of `f7c7c64`; `git status --porcelain` empty; census on base `notimpl 0`, `measured 0`, `orjson_claim 1`.
- (b) The census is the test: it prints the P1 before-values on the base (0/0/1), so it fails for the intended reason (no marks, orjson claim present).
- (c) Independent expected value: `wc -c` registry = 110240, `cat kg/*.json | wc -c` = 191093 (match R2). Five absent operations confirmed: no `scripts/build_validate.py`, no `.github/workflows`, no `KGConsistencyError`/`run_orchestrator`/`orjson`/`stage_latency_ms` in `labs/comlab/comlab`. So after: notimpl 5, measured 2, orjson_claim 0.
- (d) No contradiction. File is LF, so `apply_fix.py` (read_text/write_bytes) makes no line-ending churn.
- (e) Deliverable: run `apply_fix.py` to add five `Not implemented (T-AUD-18c):` marks, two measured sizes and the orjson correction to `COMLab_DLD.md`, one docs-only commit on `fix/T-AUD-18c`. Decisive check: census prints 5/2/0, `git diff --name-only` shows only that file, comlab suite stays `503 passed, 4 skipped, 2 errors`.

## Assumptions worked past
- The KG mark lands between "exits with code 78" and its parenthetical "(configuration error, per sysexits.h convention)" because `apply_fix.py` pins that spot. Kept as pinned; cosmetic only.
- The commit has no trailer. `bash_guard` refused the first commit attempt, which carried a `Co-Authored-By` line; AGENTS.md says a trailer trips it.

## VERIFICATION GATE
- Step 1: `notimpl 5`, `measured 2`, `orjson_claim 0`; `git diff --name-only 74adb2d HEAD` = `labs/comlab/docs/COMLab_DLD.md`.
- Step 2: `503 passed, 4 skipped, 2 errors in 10.60s` (comlab, `--continue-on-collection-errors`).
- Step 3: log shows spec commit `74adb2d` and `741ae51`; `git status --porcelain` lists the note (and the RESULT once written) only.
- Repo-wide gates (wired, ui, registry): NOT RUN, report-only and Cowork runs them. No executable line changed.

## CODE REVIEW
Docs-only diff, 14 insertions and 6 deletions in one file. Each change traces to R1 or R2. No `.py` file touched, so ruff and pyright do not apply (NOT RUN). No findings.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-07T00:33:43Z | 2026-11-07T00:34:28Z | 0.75 | ABSENT
