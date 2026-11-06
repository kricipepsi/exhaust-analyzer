# REVIEW T-AUD-4n — ACCEPT, score 98 (Windows Cowork, 2026-11-06 10:21 CET)

Branch `fix/T-AUD-4n`: spec `dd6aa13`, build `4b9d0e1`. F-C4-6 and the Fuel blend / Mileage part of F-C5-10 fixed:
the UI no longer offers Fuel blend, Mileage or the high-idle measured lambda, which no code read.

## Facts re-derived by Cowork (before the RESULT)
- The build's changed lines in `app.py`, `ui_payload.py` and `test_ui.py` equal the rehearsal patch exactly; the
  test file is identical to the rehearsed one.
- Verification on `4b9d0e1`: new file `4 passed`; ui `45 passed`; wired `85 passed`; leftover references `0`; ruff
  clean; status only the note and RESULT. Rehearsal: base `4 failed`; the tuple mutant fails
  `test_payload_sends_no_lambda_2500`.

## Second review
Codex, APPROVE (`C:/4DApp/recheck/codex/T-AUD-4n_review.md`). One NIT: the rehearsed test's docstring says "the four
high-idle gases" while it asserts five keys. Upheld (Cowork's text); too small for a revision or a row.

## Score
100 − 2 (`## Time` is a single `all` phase, not a pipe table) = 98. Time: 1 min (09:18:27Z-09:19:37Z).

## Successors
T-AUD-4o, 4p, 4q, 4r and T-COMA-3 stay queued.
