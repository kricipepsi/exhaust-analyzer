# REVIEW T-COMA-18 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-18` on `fix/T-COMA-17` `24d265b`: spec `206f21b`; build `2a3ccd1` (`_hardware_gate`, the
prune record, `SessionMetadata.fuel_delivery_type`, wired `_build_metadata`, the sanitized metadata; one test);
correction spec `15cc332`; correction `a556cb6` (two test changes, docstring). Each build's changed lines are
identical to `rehearsal.patch` / `correction1.patch`; the test `cmp` equals the `_c1` copy. Porcelain: the note and
the RESULT only.

## Gates re-run by Cowork
- comlab `517 passed, 4 skipped` (equal); wired `186` (base 176); ui `73` (equal); `5 files changed, 121
  insertions(+)` from `24d265b`.
- Implementer's note: R4 base `5 failed, 4 passed`; mutants A `3 failed`, B/C/D `1 failed` each; R6 mutant E
  `1 failed, 9 passed`; probes `3 passed`; corpus `changed 0 of 314`. Equal to the rehearsal.
- Corpus differential: RM-004 is a sibling in 1 case (era3_001, MODERN), down from 32 (31 LEGACY).

## Second review
- Build: ds-pro APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-COMA-18_review.md`). Upheld: the GDI-chemistry
  test checked only the winner (M); no test asserted the prune record (M); docstring wording (L). Not upheld: the
  criteria evidence was not in the prompt (Cowork re-ran the gates); module-level `logging.disable` (house pattern).
- Correction: APPROVE, no finding (`C:/4DApp/recheck/codex/T-COMA-18_review_c1.md`).

## Score
100 − 2 (two weak assertions in Cowork's rehearsed test, caught by review) − 1 (docstring wording) = 97.

## Follow-up
None new. Residual on the ledger row: per-rule horizon scopes for the other REG-V2 rules (rule-data authoring) and
CT-001's `vvt_equipped` precondition (no VVT field reaches COMLab).
