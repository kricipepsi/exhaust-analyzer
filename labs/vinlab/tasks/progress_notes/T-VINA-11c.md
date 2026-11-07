# T-VINA-11c progress note

## Readiness
(a) Start state matches: branch fix/T-VINA-11c, HEAD 68b86c3 (spec commit) over 0f5f570, `git status --porcelain` empty; preconditions print `checked`; P1 base vinlab `381 passed, 8 skipped`.
(b) The new test and the revised vref test fail on the base decoder for the intended reason (weak row still applied); R4 shows `8 failed, 17 passed` before the fix.
(c) Expected value derived from the task: floor 0.50 strict; AUDI `ZZZ4B` share 0.230 < 0.50, so `WAUZZZ4BZYN125879` loses 1.781 L / 4 cyl and gets `vds_engine_weak`, grade PARTIAL; compared with the test in step 2 (`25 passed`).
(d) No contradiction found; every mandatory command evaluated, no defect.
(e) Deliverable: `_WEAK_SHARE_FLOOR`/`_weak_share` in decoder.py so a row under 0.50 is read by H1 then dropped with `vds_engine_weak` (PARTIAL), plus a vocabulary row and two tests. Decisive check: step 2 `25 passed` (base `8 failed, 17 passed`, mutant `2 failed, 23 passed`) and suites `389/113/70`.

## Assumptions worked past
- Applied the fix and copied the tests before the R4 base run; the base failure was then shown with the stash, as R4 says.
- Mutant line restored with a `cp` of a pre-mutant copy, not a hand edit; `git diff --stat` matched afterwards.
- The commit has no attribution trailer: `bash_guard` refused a chained commit command whose text held the tool-name word, so the commit ran alone with a plain message.

## R4 results
- Base decoder (stash of decoder.py and VIN_VOCABULARY.md), step 2: `8 failed, 17 passed`.
- Fixed: `25 passed`.
- Mutant (`elif "wmi_brand_missing" not in conf_flags:`): `2 failed, 23 passed`. Restored; `git diff --stat 0f5f570 -- decoder.py VIN_VOCABULARY.md`: `2 files changed, 20 insertions(+), 3 deletions(-)`.

## VERIFICATION GATE
- vinlab `389 passed, 8 skipped`; wired `113 passed`; ui `70 passed` (P1 base: 381/8, 113, 70).
- ruff: `All checks passed!` on the three files.
- `git diff --stat 0f5f570 HEAD` over decoder.py and VIN_VOCABULARY.md: `2 files changed, 20 insertions(+), 3 deletions(-)`; `git log 0f5f570..HEAD`: 68b86c3 (spec), f005a0d.
- Anti-orphan: `_weak_share` and `_WEAK_SHARE_FLOOR` are read in `decode_vin_payload`; `vds_engine_weak` is read in the no-row branch and in the tests.

## CODE REVIEW
Scope: four committed paths only; the edit is Cowork's `apply_fix.py`. `_resolve_engine`, the CSV and the 0.70 threshold are untouched. A blank or unparsable share is not weak (ValueError path). The floor is strict `<` and its literal carries the P3 evidence in a comment. No findings.

## Time
phase | start | end | minutes | context at end
all | 2026-11-07T15:51:09Z | 2026-11-07T15:52:37Z | 1.5 | ABSENT
