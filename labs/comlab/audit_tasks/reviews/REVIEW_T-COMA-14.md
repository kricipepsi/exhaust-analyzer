# REVIEW T-COMA-14 — ACCEPT, score 99 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-14` on `fix/T-COMA-13` `e531528`: spec `d8f3cfb`; build `55d55d6` (the `fuel_pressure`
dispatch line and RM-004's row on it removed; one test). Hunks identical to `C:/4DApp/recheck/T-COMA-14/rehearsal.patch`.
The test is identical up to line endings: git stores LF, and the worktree copy is `cmp` equal. Porcelain: the note
and the RESULT only.

## Gates re-run by Cowork
- comlab `510 passed, 4 skipped` (equal); wired `170` (base 167); ui `70`; `grep -hc '"fuel_pressure"'` `0`, `0`;
  v7 corpus `changed 0 of 314`.
- Note: R3 base `2 failed, 1 passed`; mutant `1 failed, 2 passed`. Both equal to the pins.

## Second review
ds-flash APPROVE, no defect (`C:/4DApp/recheck/codex/T-COMA-14_review.md`). Its non-blocking note is upheld:
RM-004's `source_wiki_refs` still lists `OBD_VOCABULARY §3` after the only row that cited it was removed. This is
stale metadata left by Cowork's scripted edit, with no effect on behaviour.

## Score
100 − 1 (stale `source_wiki_refs` entry left by Cowork's scripted edit) = 99.

## Follow-up
None new. F-C1-6 (horizon and `gdi_equipped` preconditions) can add a GDI rail-pressure row behind that gate, and
drop or reuse the `§3` reference.
