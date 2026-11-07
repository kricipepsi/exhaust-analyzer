# T-COMA-9 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-9, one spec commit d5875af over 3974488, `git status --porcelain` empty; preconditions all present.
(b) Tests fail for the intended reason: validator raises `TypeError: _run_dtclab() missing 1 required positional argument: 'vin_dna'`; oracle file `8 failed`; build_corpus `5 failed, 24 passed` (P1 reproduced on base).
(c) Decisive values derived from the task: validator 314/314; oracle 8 passed; build_corpus 24 passed, 5 skipped. Call site line 404 lacks `vin_dna`, which is defined at line 391/393 in scope.
(d) No contradiction or missing decision.
(e) Teach-back: apply R1-R3 with apply_fix.py (pass vin_dna to _run_dtclab, make oracle tests path-independent, skip local-data tests when files absent) and commit once. Decisive check: P2 counts in Verification plus R5 mutant giving `1 failed, 7 passed`.

## Assumptions worked past
none

## R5 mutant
Put the call back to `_run_dtclab(_as_dict(dtc_inputs))`; oracle file from apps/wired: `1 failed, 7 passed`. Line restored by hand (sed); `git diff --stat` after: 3 files, 15 insertions, 4 deletions.

## VERIFICATION GATE
Verification steps 1-4 run; all match P2 (see RESULT). CLEAN.

## CODE REVIEW
Diff equals apply_fix.py output (R1-R3), read before commit. Every changed line is in `### Files to touch ###`. No test deleted; no assertion weakened. CLEAN.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-07T18:33:03Z | 2026-11-07T18:36:06Z | 3 | ABSENT
