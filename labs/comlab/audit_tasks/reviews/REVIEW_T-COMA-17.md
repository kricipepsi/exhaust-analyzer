# REVIEW T-COMA-17 — ACCEPT, score 99 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-17` on `fix/T-COMA-16` `1046999`: spec `61b6d61`; build `7337c0e` (`_gas_sample_reasons`,
`_confidence_for`, the ERR-ABORT-001 tuple, two `LabRoutingDirectiveReason` members, `GAS_SAMPLE_NOTICES`, the
ADR-0007 amendment; two tests). The changed lines are identical to `C:/4DApp/recheck/T-COMA-17/rehearsal.patch`
(`git apply --check -R` passes); both tests `cmp` equal. Porcelain: the note and the RESULT only.

## Gates re-run by Cowork
- comlab `517 passed, 4 skipped` (base 510); wired `176` (equal); ui `73` (base 70). All equal to P2.
- Implementer's note: R5 base `3 failed, 4 passed` and `2 failed, 1 passed`; mutants A `3 failed`, B/C/D `1 failed`
  each; corpus `changed 0 of 314`; probes `1 failed, 1 passed` (F-C1-14 passes; F-C1-13's expectation superseded by
  R1). Equal to the rehearsal.

## Second review
ds-pro APPROVE, no High or Medium finding (`C:/4DApp/recheck/codex/T-COMA-17_review.md`; it cites the embedded
rulings, diff and both `ExecutionMeta` sites). Its Low notes, re-derived:
- `ROUTING_NOTICES[3][1]` in the UI test is coupled to the tuple order. Upheld as cosmetic: T-AUD-10d's test already
  pins that order, so a reorder fails there first.
- `test_no_reasons_attribute_gives_flag_notices_only` passes on base. Upheld, and it is by design: it is a PIN on the
  `getattr(..., None)` default; the other two UI tests are the NEW ones.
- No test drives `gas_lab_output=None` through `_gas_sample_reasons`. Upheld: the branch is untested (mutant D covers
  only the suppression half). Too small for a row: it is one `or` clause, and `process()` already handles `gas is
  None` the same way for the perception detectors.

## Score
100 − 1 (Cowork's rehearsed test leaves the `gas is None` half of the guard unexercised) = 99.

## Follow-up
None new. Residual on the ledger row: 3 `invalid_input` corpus cases raise `DTCFormatError`/`PIDValidationError`
before the shim (input validation, not this policy).
