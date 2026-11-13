# REVIEW T-COMA-19 — ACCEPT, score 100 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-19` on `fix/T-COMA-18` `59f3e41`: spec `7635132`; build `c436a8b` (`_known_horizon`
validator; the re-stated `test_abort_incomplete` pin; one new test). Changed lines identical to
`C:/4DApp/recheck/T-COMA-19/rehearsal.patch`; the test `cmp` equal. Porcelain: the note and the RESULT only.

## Gates re-run by Cowork
- comlab `524 passed, 4 skipped` (base 517); wired `186`; ui `73`. Equal to P2.
- Implementer's note: R4 base `6 failed, 5 passed`; mutants A `2 failed`, B `5 failed`; probe `1 passed, 2
  skipped`; corpus `changed 0 of 314`. Equal to the rehearsal.

## Second review
APPROVE, no defect (`C:/4DApp/recheck/codex/T-COMA-19_review.md`; it cites the embedded rulings, diff, producer
and note). Its observation, re-derived: the `None` case fails on type validation alone, and `match=` would name the
origin. True; not a defect: the `''`, `HORIZON_FOO` and `MODERN` cases and mutant B are decisive.

## Score
100.

## Follow-up
None new. F-C1-16 (the v1 path with no DTC output) stays open in T-AUD-3.
