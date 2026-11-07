# REVIEW T-COMA-8 — ACCEPT, score 99 (Windows Cowork, 2026-11-07)

Facts first: `fix/T-COMA-8` on `fix/T-COMA-7` `e65c2d0`: spec `26d27fd`; build `40dc1cc` (both `ExecutionMeta`
builders in `process` echo `request.metadata.vin_confidence.value`; two tests). Source hunks identical to
`C:/4DApp/recheck/T-COMA-8/rehearsal.patch`; both tests `cmp` equal. Porcelain: note and RESULT only.

## Gates re-run by Cowork
- comlab `510 passed, 4 skipped` (base 508); wired `123 passed` (base 121); ui `70`; ruff clean; audit probe
  `in: PARTIAL  out: PARTIAL`, `1 passed` (base `out: HIGH`); v7 corpus 0 of 314 changed (rehearsal).
- R3 (note): base `2 failed` each; mutant (second site HIGH) comlab test `1 failed, 1 passed`; restored, `cmp` equal.

## Second review
ds-flash APPROVE WITH CORRECTIONS, 1 LOW (`C:/4DApp/recheck/codex/T-COMA-8_review.md`): both lines keep a trailing
comment (`# lld: §3.3; F-C1-9 (T-COMA-8): echoed`), while R1 names only the expression. Re-derived: not a defect of
the build. The comment is in Cowork's `apply_fix.py`, which R2 makes the binding route; R1's text abbreviated the
line. The slip is Cowork's spec wording.

## Score
100 − 1 (R1 wording did not quote the scripted line in full) = 99.

## Follow-up
GAS_DOMINANT and the confidence cap for a PARTIAL decode stay T-AUD-2 (wiki 03 §CONCEPT_DNA_CONFIDENCE).
