# REVIEW T-COMA-6 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-6` on `fix/T-COMA-11` `49214a9`: spec `8f1690b`; build `9e0df5d` (`_strict_support`, the
`_score_rule_raw`/`_prune_attribution` checks, the COMLab no-fire abstain, two reversed pins, one test); correction
spec `118f675`; correction build `c086c3e`. Both builds have hunks identical to Cowork's rehearsals
(`C:/4DApp/recheck/T-COMA-6/rehearsal.patch`, `correction1.patch`), and both tests are `cmp` equal. Porcelain: the
note and the RESULT only.

## Gates re-run by Cowork
- On `9e0df5d`: comlab `510 passed, 4 skipped` (equal); wired `140` (base 127); ui `70`; probes `3 passed, 13
  deselected`, verdict `OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH` (base `LC-002`/`MF-005`); v7 corpus
  `changed 0 of 314`; ruff clean.
- On `c086c3e`: wired `143`; comlab `510 passed, 4 skipped`. The rehearsal on the same tree: new test `16 passed`
  (`3 failed, 13 passed` on `9e0df5d`), ui 70, probes, corpus 0 of 314 and ruff all equal.
- Note: R5 base `9 failed, 4 passed`; mutant A `1 failed`; mutant B `2 failed`; R7 `3 failed, 13 passed`. All equal
  to the pins.

## Second review
- `9e0df5d`: ds-flash APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-COMA-6_review.md`). **High upheld as
  latent:** NORMAL rows were filtered out before the "no non-GATING row" test, so a rule whose only support is the
  NORMAL row would fire on healthy gas. This departs from R1. No current rule has the shape (registry scan: 0).
  **Medium upheld:** there was no test. The defect was in Cowork's rehearsal script, not the build. It went to
  correction 1 (R6, R7), extended to a GATING NORMAL row used as the anchor.
- `c086c3e`: ds-flash APPROVE (`C:/4DApp/recheck/codex/T-COMA-6_c1_review.md`); it cites the embedded diff.

## Score
100 − 2 (one return for a latent defect in Cowork's spec and rehearsal) − 1 (step 1 named an untracked
`case_library.html` path; harmless pathspec error, removed in correction 1) = 97. The implementer followed the
spec exactly, both times.

## Follow-up
- No new row. The ledger already names the open neighbours of F-C1-1: F-C1-2 (12 chemical states with no rule; 13
  `test_unrouted_state_*` probes fail before and after) and rule coverage outside NORMAL_OPERATION (for example RM-001
  has no CO or λ row). See `C:/4DApp/recheck/T-COMA-6/candidates4.out` and the sidecar.
- Commits `9e0df5d` and `c086c3e` have no Co-Authored-By trailer (the note says `bash_guard` refused it). This
  matches earlier COMA builds, so it is not scored.
