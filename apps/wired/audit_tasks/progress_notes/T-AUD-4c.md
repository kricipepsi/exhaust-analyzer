# T-AUD-4c progress note

## Readiness challenge
(a) Start state matches: branch fix/T-AUD-4c, HEAD 6dc64fc (spec commit, base), `git status --porcelain` empty; preconditions print `checked` with no MISSING.
(b) The new test cases (None, key absent -> VALID) fail on base: base returns CODES_RECENTLY_CLEARED for both (gate 5 line 88-89). Confirmed by red run below.
(c) Expected: corpus shape VALID 289, UI shape VALID 293 (P2), derived from P1 by CODES_RECENTLY_CLEARED -> VALID with other gates unchanged; step 1 count 81 - 1 + 2 = 82.
(d) No contradiction or missing decision found.
(e) Gate 5 blocks only a stated count below 1; absent or None passes. Decisive check: step 1 gives 82 passed, both R2 mutants fail, step 3 prints P2.

## Assumptions worked past
none. The commit has no attribution trailer, because bash_guard refuses a command whose text names the assistant; the commit ran as its own command.

## Red gate
Before the gate change: `2 failed, 29 passed` (both `test_gate5_drive_cycles_unknown_passes` cases), assertion CODES_RECENTLY_CLEARED != VALID.

## VERIFICATION GATE
CLEAN. Step 1 `82 passed`; obdlab `389 passed, 2 skipped`; wired `46 passed`; ui `30 passed`; ruff `All checks passed!`.
Mutant A (base default, None blocks): 2 failed (`unknown_passes[none]`, `[absent]`). Mutant B (gate 5 removed): 1 failed (`test_gate5_codes_cleared_fails`).
Step 3: UI-shape VALID 293, ENGINE_COLD 2, exceptions 2; corpus VALID 289 and other gates unchanged; `ui-shape verdict changes 0 []`.
Not run: pyright, `--select S` (task names ruff only). Repo-wide gates are Cowork's.

## CODE REVIEW
Scope: two files in Files to touch; each changed line traces to R1/R2. No new field or enum (anti-orphan n/a). Gates 1-4, 6-8 unchanged. Added `import pytest` for the parametrisation.

## Time
phase | start | end | minutes | context at end
all | 2026-11-05T12:43:41Z | 2026-11-05T12:47:20Z | 3.6 | ABSENT

## Revision 02
Start 2026-11-05T12:59:05Z. Branch fix/T-AUD-4c, HEAD 52af440 above 87c366e; `git status --porcelain` printed only the note and the RESULT.
(a) Starting state matches the revision-02 First action.
(b) Test: `test_gate5_codes_not_cleared_pass[1]` passes on the current code, so it is a PIN, not a red test. It kills the boundary mutant `drive_cycles < 2`, which I run below.
(c) Expected: step 1 `83 passed` (82 + 1 case); obdlab `390 passed, 2 skipped`.
(d) No contradiction found.
(e) Parametrise the pass test over 1 and 5 so a count of 1 pins the gate-5 boundary; the production file does not change. Decisive check: the mutant `< 2` fails case `[1]`, and step 1 prints `83 passed`.

Mutant C (boundary, `drive_cycles < 2`, copy under `C:/4DApp/recheck/T-AUD-4c/mut/obdlab`): `1 failed, 31 passed`, `test_gate5_codes_not_cleared_pass[1]`. It survived the suite before this revision.
Step 1 `83 passed`; obdlab `390 passed, 2 skipped`; wired `46 passed`; ui `30 passed`; ruff `All checks passed!`. Production file unchanged. Commit 1750bc8 `test(T-AUD-4c): ...`, no attribution trailer (bash_guard refuses the command text that names the assistant).
Step 3 BASE and FIX blocks as printed (BASE equals FIX because the script imports the patched code):
```
cases with OBD 297
corpus keys present: drive_cycles 0 active_dtcs 207
BASE corpus-shape gates {'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2, 'CKP_CMP_FAULT_ACTIVE': 1}
BASE ui-shape gates     {'VALID': 293, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2}
FIX  corpus-shape gates {'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2, 'CKP_CMP_FAULT_ACTIVE': 1}
FIX  ui-shape gates     {'VALID': 293, 'ENGINE_COLD': 2, 'EXC:PIDValidationError': 2}
ui-shape verdict changes 0 []
```
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| revision 02 | 2026-11-05T12:59:05Z | 2026-11-05T13:05:04Z | 6.0 | ABSENT |
