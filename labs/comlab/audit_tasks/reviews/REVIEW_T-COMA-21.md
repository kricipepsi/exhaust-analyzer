# REVIEW T-COMA-21 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-21` on `fix/T-COMA-20` `8dc0b43`: spec `c988cb9`; build `3ed6cb0` (`_map_degradation`
reads OBD absence and suppression; `_confidence_for` is the verdict score band with the GAS_DOMINANT cap and the
abstained/INVALID floor; `_confidence_from_horizon` deleted; the `case_020_misfire` pin and the BDD §0 rows; one
test); correction spec `9d47a65`; correction `c176043` (docstring and BDD wording; two tests). Each build's changed
lines are identical to `rehearsal.patch` / `correction1.patch`; the test `cmp` equals the `_c1` copy. Porcelain: the
note and the RESULT only.

## Gates re-run by Cowork
- comlab `540 passed, 4 skipped` (base 527); wired `186`; ui `73`.
- Implementer's note: R5 base `10 failed, 1 passed`; mutants A-E `1 failed` each; R7 mutants F and G `1 failed,
  12 passed`; step 3 `4 passed`; verdicts `changed 0 of 314`. Equal to the rehearsal.
- Measured effect (P4): the rating now orders family accuracy (HIGH 157/199, DEGRADED 8/11, LOW 51/101); before it
  was the era (HIGH 5/8, DEGRADED 1/1, LOW 210/302). Mode changed on 17 of 311 cases.

## Second review
- Build: APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-COMA-21_review.md`). Upheld: the docstring and BDD row
  dropped `suppress_gaslab` (M); the `suppress_gaslab` branch and the `process()`-level cap were untested (L, L);
  "lab completeness" overclaimed (L). Not upheld: porcelain evidence (Cowork ran `git status`), phase timings and
  the mutant-revert method.
- Correction: APPROVE WITH CORRECTIONS (`..._review_c1.md`), two Low. The `SimpleNamespace` directive stub would
  fail pyright: not upheld (pyright is not a gate here; T-AUD-10d's test uses the same stub). The docstring says
  "The test reads gas and OBD only" where "gate" is meant: upheld, cosmetic, left as a recorded nit (no third
  dispatch for one word).

## Score
100 − 2 (Cowork's rehearsed docs and tests needed a correction round) − 1 (the "test"/"gate" wording nit) = 97.

## Follow-up
None new. Calibration (wiki 09) and a GAS_DOMINANT score ceiling stay out of scope; the two audit probes
`test_no_second_frame_is_single_point` and `test_invalid_sample_does_not_produce_fault_verdict_by_default` stay
failing by ruling.
