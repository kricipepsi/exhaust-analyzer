# T-AUD-7a progress note

## Readiness
- (a) Starting state matches: branch `fix/T-AUD-7a`, base HEAD `d97d92e`, `git status --porcelain` empty. Preconditions: checked, no MISSING.
- (b) Probe fails for the intended reason: the baseline probe prints `sides not found: 0`, so all 4 "never branch / work on main" quotes are still present.
- (c) Expected value derived from the spec: R1 removes the quotes at 4DLab_CLAUDE.md:137, :138, :128 and R2 removes v3/CLAUDE.md:40. That is 4 lost sides, so the last line must read `sides not found: 4`.
- (d) No contradiction: cited lines 127-160 and 40-41 are where the task says; both files are LF.
- (e) Teach-back: replace the old git section in 4DLab_CLAUDE.md and the git bullet in v3/CLAUDE.md with the pinned text, in one docs commit. The decisive check is the D3 probe: `sides not found: 4` with the two AUDIT_START_HERE sides still found.

## Assumptions worked past
- none

## VERIFICATION GATE
CLEAN. Step 1: 4 `NOT FOUND` lines (4DLab_CLAUDE.md x3, v3/CLAUDE.md x1); both AUDIT_START_HERE.md sides (:62, :59) still found. Step 2: `sides not found: 4` (probe exit 1, the expected fixed state). Step 3: one `docs(T-AUD-7a):` commit after the spec commit; diff stat names only the two files; status shows only the note and the RESULT.

## CODE REVIEW
CLEAN. No code changed. Every changed line is R1 or R2 text from the task. LF endings kept. No other file touched.

## Assumptions worked past
- The commit has no attribution trailer. bash_guard refused the first commit attempt because the command text held the trailer; the retry without it passed.

## Time
phase | start | end | minutes | context at end
all | 2026-11-03T19:51:55Z | 2026-11-03T19:52:46Z | 1 | ABSENT
