# T-AUD-18a progress note

## Readiness
(a) Start matches: branch fix/T-AUD-18a, HEAD 20216ca (descendant of 3b7197f), status clean, census `stale 9`, `notes 0`.
(b) Docs-only row; the census is the failing check: `stale 9` before, must reach `stale 0`.
(c) Expected after: `stale 0`, `notes 7` (pinned P1). Facts re-read in code: the four router functions, `_P030X_RE` `^P030[0-8]$`, `fault_name=sibling_id`, mask yaml lines 45-46, `o2_failure_mode` at ingestion.py:399.
(d) No contradiction: all 3 docs are in Files to touch; no code change.
(e) Deliverable: 3 COMLab docs corrected to match the code by running apply_fix.py. Decisive check: census prints stale 0 / notes 7, the diff lists exactly the 3 docs, comlab suite 503 passed, 4 skipped, 2 errors.

## Assumptions worked past
The commit message has no Co-Authored-By trailer: `bash_guard` refused the commit command that held it, and nothing ran.

## VERIFICATION GATE
- census: `stale 0`, `notes 7` (base: `stale 9`, `notes 0`).
- `git diff --name-only 20216ca HEAD`: the 3 COMLab docs only.
- comlab suite: `503 passed, 4 skipped, 2 errors in 9.40s` (P3). Before-count NOT RUN: docs-only diff.
- `git status --porcelain`: only the note (the RESULT was not yet written at that point).

## CODE REVIEW
Diff read in full (13 insertions, 11 deletions, 3 files). Every changed line is an edit pinned in apply_fix.py. One wording point: DEP-9 now reads "...`T-COMV2-ECU-HW-1`; the fuel-system gate is **shipped**: ...; `pending`)". The trailing `pending` applies to the ECU-HW-1 part, as pinned. No code, config or test change.

## Time
phase | start | end | minutes | context at end
all | 2026-11-07T00:29:49Z | 2026-11-07T00:30:33Z (verification run) | under 2 | ABSENT
