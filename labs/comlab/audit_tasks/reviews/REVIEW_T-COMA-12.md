# REVIEW T-COMA-12 — ACCEPT, score 100 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-12` on `fix/T-COMA-6` `101f042`: spec `55c92f9`; build `35f5230` (`_discriminator_families`,
`_within_abstain_margin` with `_MARGIN_EPSILON`, `_P030X_RE` `^P030[0-9]$`; one test). Hunks identical to
`C:/4DApp/recheck/T-COMA-12/rehearsal.patch`; the test `cmp` equal. Porcelain: the note and the RESULT only.

## Gates re-run by Cowork
- comlab `510 passed, 4 skipped` (equal); wired `156` (base 143); ui `70`; audit probes `3 passed` (base `2 failed,
  1 passed`); v7 corpus `changed 0 of 314`; ruff clean.
- Note: R5 base `9 failed, 4 passed`; mutant A (list, no dedupe) `4 failed`; mutant B (epsilon 0) `1 failed`. All
  equal to the pins.

## Second review
ds-flash APPROVE, no defect (`C:/4DApp/recheck/codex/T-COMA-12_review.md`); it cites the embedded lines for R1-R3.

## Score
100.

## Follow-up
None new. The F-C1-18 audit probe passes without exercising the lift since T-COMA-6 (tags-only NORMAL input
no-fires). The new unit test pins the lift instead.
