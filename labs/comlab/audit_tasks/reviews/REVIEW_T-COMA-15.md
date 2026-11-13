# REVIEW T-COMA-15 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-15` on `fix/T-COMA-14` `68dd691`: spec `4de9540`; build `e8f1e84` (perception labels,
SF-001/SF-002 delta rows, 13 comlab + 2 wired pins re-stated, one test); correction spec `c651f31`; correction build
`c2212f5` (SF-001/SF-002 description parentheticals; the test pins value, tier and description). Both builds have
hunks identical to Cowork's rehearsals (`rehearsal.patch`, `correction1.patch`), and both tests are identical up to
line endings. Porcelain: the note and the RESULT only.

## Gates re-run by Cowork
- On `e8f1e84`: comlab `510 passed, 4 skipped`; wired `176` (base 170); ui `70`; corpus `vs before 18`,
  `vs expected 0` of 314 (SF-001↔SF-002 swaps plus EXP-N005 CF-001 → SF-001); family accuracy 216 equal.
- On `c2212f5`: comlab `510 passed, 4 skipped`; wired `176`; ui `70`.
- Note: R5 base `4 failed, 2 passed`; mutants A and B `2 failed` each; R7 `2 failed, 4 passed`. All equal to the
  pins.
- Domain referee (`C:/4DApp/recheck/T-COMA-15/referee.py`): all 5 corpus cases GASLab classifies
  `O2_SENSOR_BIASED_HIGH` with an out-of-band delta read rich (−0.09 to −0.11).

## Second review
- `e8f1e84`: ds-flash APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-COMA-15_review.md`). It confirmed the
  direction and R1-R3. **Medium upheld:** SF-001/SF-002 descriptions, which are the user-facing `fault_name` and
  headline, still stated the old direction. **Low upheld:** the test pinned only the operator. Both went to
  correction 1. The note on the e2e mock names is not counted (out of scope by the spec).
- `c2212f5`: ds-flash APPROVE (`C:/4DApp/recheck/codex/T-COMA-15_c1_review.md`). The first run of this review
  failed before any call: the prompt held a cp1252 byte from Python's stdout. It was rebuilt with
  `PYTHONIOENCODING=utf-8`.

## Score
100 − 2 (one return: Cowork's rehearsal missed the user-facing description text) − 1 (the first test pinned the
operator only) = 97. The implementer followed the spec exactly, both times.

## Follow-up
None new. The e2e mocks `sensor_biased_high()`/`sensor_biased_low()` keep λ-direction names (recorded in the note).
F-D2-2, 3, 4 stay open in T-AUD-2/T-AUD-4.
