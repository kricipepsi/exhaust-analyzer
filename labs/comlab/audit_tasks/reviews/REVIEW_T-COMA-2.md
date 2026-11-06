# REVIEW T-COMA-2 — ACCEPT, score 98 (Windows Cowork, 2026-11-06 10:08 CET)

Branch `fix/T-COMA-2`: spec `8931b9a`, build `d405b26`. The T-AUD-4e residual is fixed: a non-starter is diagnosed
without exhaust gas readings; the schema keeps gas required for every other session.

## Facts re-derived by Cowork (before the RESULT)
- The build's source diff is line-for-line the rehearsal patch (set compare of changed lines: no difference either
  way); the test file is identical to the rehearsed one; the R5 and R6 rewrites are as ruled.
- Verification on `d405b26`: new file `6 passed`; comlab `531 passed, 4 skipped, 2 errors`; registry
  `5 failed, 502 passed, 4 deselected` (the known set); wired `85 passed`; ui `38 passed`; the 9 probe lines equal P2
  (no gas and empty gas → NS-NO-RULE; partial gas and a running engine without gas → the standard abort; case_006
  without gas → NS-004); corpus 314, equal to T-COMA-1's accepted dump; ruff clean; status only the note and RESULT.
- Mutant counts (RESULT) equal Cowork's rehearsal: M1 2F, M2 1F, M3 3F; base `5 failed, 1 passed`.

## Second review
Codex, APPROVE (`C:/4DApp/recheck/codex/T-COMA-2_review.md`): every ruling and boundary case confirmed. One NIT:
`apps/ui/tests/test_t_aud_1c.py` `test_r2_gas_help_says_required` keeps a docstring saying "required for every run".
Upheld as a spec gap (R6 named the assert, not the docstring); classified too small for a row or a revision.

## Score
100 − 2 (`## Time` is one approximate phase, `~3` minutes, not a table of measured phases per AGENTS § Time; the
missing commit trailer is bash_guard's refusal, recorded, not deducted) = 98. Time: 3 min (09:03:20Z-09:06:00Z).

## Successors
- T-AUD-4e (census remainder) and T-COMA-3 (GASLab cranking validity, NS-004 DTC list, OBD `active_dtcs` not reaching
  the shim, REAL-002's label) stay queued.
