# T-AUD-4b progress note

## Readiness challenge
(a) Start matches: branch `fix/T-AUD-4b`, HEAD `a80d7f0` (spec commit, base), `git status --porcelain` empty; preconditions print `checked`. 2026-11-05T12:19:50Z.
(b) The NEW tests must fail on the base: override applied after the labs (3 override tests) and `ValueError` on SUPERCHARGED (1 test); the PIN passes.
(c) Derived expected values: wideband case + NARROWBAND override -> OBDLab view `NARROWBAND_0_TO_1V`, GASLab view `NARROWBAND`; wideband ratio only -> `OBD_INPUT_INCOMPLETE`; `de_cat` True -> `has_catalyst` False; SUPERCHARGED -> TURBOCHARGED. Match P2/R2.
(d) No contradiction. Step 4 text says the hook re-applies the override so base equals fixed and `{}` prints; consistent with rehearse.py.
(e) Deliverable: move the override block ahead of the labs in `diagnose` and map SUPERCHARGED to TURBOCHARGED in the OBD view, with 5 tests. Decisive check: step 1 `46 passed`, mutants fail named tests, step 4 `changes ... {}` and SUPERCHARGED `ok`.

## Assumptions worked past
- The wideband case is embedded in the test (era2_015 raw inputs) so the test does not depend on the v7 corpus path.
- Mutants ran as copies of `apps/wired/{wired,tests}` under `recheck/T-AUD-4b/mut/m1,m2` with PYTHONPATH at the copy (the printed import path confirmed it).
- The commit message has no attribution trailer: `bash_guard` refuses a command whose text holds the agent's name beyond the identity flags.
- `diagnose` now sets `vin_dna["emissions"]` to `_as_dict(...)`, so the override and the request read one object.

## VERIFICATION GATE
CLEAN. Steps 1-5 ran as written. Step 1 `46 passed`; step 2 equals P3; step 3 `526 passed, 4 skipped, 2 errors` (R0-2 known); step 4 `changes ... {}`, SUPERCHARGED `ok`; step 5 `All checks passed!`. Mutant m1 (override block after the labs) fails the three override tests; m2 (no SUPERCHARGED mapping) fails `test_supercharged_projects_as_turbocharged`. pyright and `ruff --select S` NOT RUN (not in this task's Verification).

## CODE REVIEW
Scope: the block moved and gained consumer comments; one mapping added in `_build_obd_dna_view`; five tests. No new name is read nowhere. Out-of-scope items untouched. No findings.

## Time
phase | start | end | minutes | context at end
build | 2026-11-05T12:19:50Z | 2026-11-05T12:22:54Z | 3.1 | ABSENT
