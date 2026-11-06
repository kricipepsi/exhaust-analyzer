# REVIEW T-COMA-3b — ACCEPT, score 99 (Windows Cowork, 2026-11-06)

Branch `fix/T-COMA-3b`: spec `57c6b04`, build `42ebcdc`. A `will_not_start` session's gas sample is a cranking sample:
GASLab's new `CRANKING` bucket skips the running-engine triangle and dilution gates and classifies `RICH_MISFIRE`,
`LEAN_MISFIRE` or `INCOMPLETE_COMBUSTION`, so NS-001..NS-003 can name the no-start. NS-004 and NS-005 outrank NS-001.

## Facts re-derived by Cowork (before the RESULT)
- The build's diff equals the rehearsal patch exactly; both new test files equal the rehearsed copies.
- On `42ebcdc`: gaslab `215 passed, 2 skipped, 4 deselected` (base 208); wired `106 passed` (base 104); registry
  `5 failed, 504 passed, 4 deselected` (the 5 are `test_build_corpus`, inputs absent); comlab `503 passed, 4 skipped,
  2 errors`; ui 57; obdlab 391, dtclab 590, vinlab 376, dnalab 27, symptomlab 72 (baselines).
- Corpus `differ 5`: REAL-002 and case_007 → NS-001, REAL-003 → NS-002, case_006 NS-004 and case_040 NS-005 kept
  (confidence 0.85 → 1.0).

## Second review
Three routes, all with a verdict line; the wrapper parsed none (`C:/4DApp/recheck/codex/T-COMA-3b_review.md` assembles
them). ds-flash and Codex APPROVE WITH CORRECTIONS, ds-pro REJECT.
- ds-pro BLOCKER (NS-004 ties NS-001 at 0.85 and loses on rule_id): not upheld. NS-004 also carries rpm < 600
  SUGGESTIVE (outside the embedded hunk); measured case_006 NS-004 0.9 vs NS-001 0.85.
- Codex/ds-flash CONCERN (precedence is conditional on the rpm bonus; the registry test checks config only): probed
  end to end. A freeze frame without rpm aborts `FREEZE_FRAME_INCOMPLETE` before scoring; with rpm 700 (no bonus)
  P0230 → NS-004 and P0335 → NS-005 on `42ebcdc`. A trial with base 0.85 gave the same verdicts and was reverted. No
  correction; the extra scoring test is too small for a revision.
- ds-pro CONCERN (confidence 1.0 above the 0.9 ceiling): the non_starter symptom prior adds +0.10 after the shim;
  203 of 314 corpus verdicts already show 1.0. Not upheld.
- ds-pro CONCERN (NS-005 now fires without rpm): a satisfied GATING DTC row already sets `any_satisfied` in
  `_score_rule_raw`; the firing set is unchanged. Not upheld.
- ds-pro CONCERN (the abstain test has no gas): `_raw` defaults `gas` to CO2 14.8 % (`test_t_aud_1a_inputs.py`). Not
  upheld; the docstring's "not a cranking sample" means the CO2 ≥ 8 branch, wording only.
- Codex CONCERN (CRANKING exclusivity rests on triage) and NITs (triage `cranking` untested, the < 600 band is
  descriptive, REAL-002 unpinned pending T-COMA-3c): the row's recorded rulings; too small.

## Score
99. Time: 2 min. One point: the registry precedence test asserts configuration, not a scored contest.

## Successors
T-COMA-3c (REAL-002 label) waits on channel 046; with this row REAL-002 names NS-001, the recommended relabel.
