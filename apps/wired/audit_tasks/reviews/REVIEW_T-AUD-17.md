# REVIEW T-AUD-17 — ACCEPT, score 96 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-AUD-17` carries spec `343d490`, build `3c2327f` (equal to `recheck/T-AUD-17/rehearsal.patch`),
spec revision 02 `d3e6b7b`, build `4f30910` (equal to `rehearsal_r02.patch`). Porcelain: note and RESULT only. Both
headless runs exit 0; revision 02 ran as a fresh session.

## Gates re-run by Cowork
- Census `stale 0`, `notes 20`, `highidle 0`; `ast same` for `payload.py` against the first spec.
- obdlab `394 passed, 2 skipped`; ruff clean; corpus `differ 0` of 314; wired `106 passed`; comlab
  `503 passed, 4 skipped, 2 errors` (equal on the base, at revision 01); ui `57 passed` (revision 01).

## Second review
`recheck/codex/T-AUD-17_review.md` (ds-flash, APPROVE WITH CORRECTIONS). Upheld into revision 02: the stale
`STRESS_IDLE` note (the census matched code tokens only), the DLD table split by Cowork's inserted paragraph, the
exact-class test, the `ObdEmissionsView` wording. Not upheld after re-derivation: the six `except ValueError` scopes
(none encloses `compute_ve`) and the `notes:` NIT (no reader).

## Criteria
1-4 MET.

## Score
100 − 4 (a revision for defects in Cowork's own rehearsal; the implementer's work equals the spec both times) = 96.
