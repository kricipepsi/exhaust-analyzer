# REVIEW T-COMA-3a — ACCEPT, score 100 (Windows Cowork, 2026-11-06 16:26 CET)

Branch `fix/T-COMA-3a`: spec `f388565`, build `c596788`. A `will_not_start` session with P0335 or P0336
(crankshaft position sensor) names the new `non_starter` rule NS-005 instead of the `NS-NO-RULE` abstain.

## Facts re-derived by Cowork (before the RESULT)
- The build's changed lines equal the rehearsal patch exactly (111 of 111).
- On `c596788`: new file `3 passed` (base `2 failed, 1 passed`); wired 104 (base 101); ui 57; registry 5F/503P
  (base 5F/502P; the 5 are `test_build_corpus`, inputs absent); comlab 503/4/2; gaslab 208, obdlab 391, dtclab 590;
  corpus: exactly case_040 moves, `NS-NO-RULE` abstain → `non_starter` `NS-005` 0.85; ruff clean.

## Second review
ds-flash, APPROVE (`C:/4DApp/recheck/codex/T-COMA-3a_review.md`).
- CONCERN (a running engine with P0335 could reach NS-005): not upheld. Cowork probe on `c596788`, running session
  with `[P0335]` → `lean_condition` LC-002 0.91, identical to the same session with no DTCs; with `[P0335, P0300]` →
  `misfire` MF-001. The family gate keeps `non_starter` rules to `will_not_start` sessions.
- CONCERN (outcompeting chemistry rules not tested directly): the ceiling 0.8 equals NS-004's; corpus moves only
  case_040. No correction.
- CONCERN (the `passes_cases` resolver widened to v7): the row's recorded ruling; kept.
- NITs (EOF newline, pin coverage, P0336 synthetic): too small.

## Score
100. Time: 2 min. The RESULT discloses the trailing newline `json.dumps` adds to `non_starter.json`.

## Successors
Queue: T-COMA-3b (GASLab cranking validity, plan REQUIRED). T-COMA-3c waits on channel 046.
