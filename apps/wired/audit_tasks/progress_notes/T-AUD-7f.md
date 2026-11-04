# T-AUD-7f progress note

## Readiness
(a) Starting state matches: branch `fix/T-AUD-7f`, HEAD~1 `41ccddd`, `git status --porcelain` empty; rules.py base `sides not found: 14`, T-GR-10/11 counts 0 and 2, `branch (.fix/` 0 (P1).
(b) The check fails for the intended reason: base prints 14, not 18, and the exception text is absent from `AGENTS.md`.
(c) Expected values come from the spec: 18 not-found, 4 NOT FOUND in X2-X4, counts 1 and 3, then 1 and 0; the diff stat is 7 files, 11 insertions, 8 deletions.
(d) No contradiction found: all seven files exist and the pinned old strings are in `make_rh.py`.
(e) Teach-back: I will make the seven pinned edits R1-R7 by hand and commit them once as `docs(T-AUD-7f):`. The decisive check is `rules.py` printing `sides not found: 18` plus the grep counts.

## Assumptions worked past
- Spec says R7 is at harness/HARNESS_START_HERE.md line 96; the old text is on line 97 (line 96 is blank). The old string is unique, so the edit is unaffected (SOFT, no blocker).
- The commit hook (bash_guard) refused the commit while the message held the co-author trailer, so the commit has no trailer.

## VERIFICATION GATE
CLEAN. Step 1: `sides not found: 18`, X2-X4 `NOT FOUND` count 4. Step 2: `AGENTS.md:1`, pack START_HERE `:3`, `branch (.fix/` 1, `run **by the user**` 0. Step 3: one `docs(T-AUD-7f):` commit `51fdebf`; stat `7 files changed, 11 insertions(+), 8 deletions(-)`; status lists only the note (RESULT written after). My diff matches `rehearsal.diff` on all changed lines. `git diff --check` is clean.

## CODE REVIEW
Docs only, no code. Every changed line traces to R1-R7; no other file touched. No findings.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-04T23:38:43Z | 2026-11-04T23:39:58Z | 1 | ABSENT
