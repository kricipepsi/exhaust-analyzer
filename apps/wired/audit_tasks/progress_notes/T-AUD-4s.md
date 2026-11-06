# T-AUD-4s progress note

## Readiness challenge
(a) Start matched: branch `fix/T-AUD-4s`, HEAD a9507a7 (descendant of 8c28352, base), `git status --porcelain` empty.
(b) Red: new wired file `9 failed, 3 passed`, new ui file `3 failed` on base (P3).
(c) Decisive values taken from P3/P4 (12 passed, 3 passed, 101, 52, 525/4/2, differ 0, 3 passed f7).
(d) No contradiction found; preconditions printed `checked`.
(e) Deliverable: 31 raw OBD channels range-checked in composition.py; bad values abort with OBD_INPUT_OUT_OF_RANGE. Decisive check: `12 passed` + `3 passed`, corpus `differ 0`, M1 fails exactly 2 named tests.
Order slip: I ran the red gate and applied apply_fix.py before writing this note (no guard refused it). No effect on the result.

## Assumptions worked past
- Commit made without the Co-Authored-By trailer: bash_guard refused the command text holding the trailer.

## Mutant M1 (R2 abort block disabled: `if False and out_of_range is not None:`)
`2 failed, 10 passed`: `test_diagnose_aborts_out_of_range`, `test_diagnose_aborts_instead_of_crashing`. Restored with `git restore`.

## VERIFICATION GATE
step 1: 12 passed; 3 passed; 101 passed; 52 passed. step 2: 525 passed, 4 skipped, 2 errors.
step 3: corpus 314; differ 0; 3 passed, 9 deselected. step 4: ruff All checks passed!
Not run: pyright, `--select S` (task Verification does not list them).

## CODE REVIEW
Diff of composition.py equals `composition.fix.py` byte for byte (cmp). Only the 31 P1 lines, import math, table, two helpers, one abort block changed. Scope holds; no drive-by edits. Anti-orphan: `_raw_obd_value` read in `_run_obdlab` and `_out_of_range_input`; `_out_of_range_input` read in `diagnose`.

## Time
phase | start | end | minutes | context at end
all | 2026-11-06T14:10:37Z | 2026-11-06T14:12:43Z | 2 | ABSENT
