# T-COMA-2 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-2, base (spec commit) 8931b9a (descendant of b81c50e), `git status --porcelain` empty, preconditions print `checked`.
(b) The new test file on the base: `5 failed, 1 passed` (P3 base). The 5 NEW tests fail for the intended reason (gas_lab_output "Field required", old abort message).
(c) Decisive expected values come from P2/P3/P4/P5 of the task, not from the code under test: fix `6 passed`; wired `85 passed`; corpus dump equals T-COMA-1 `corpus_fix.json`.
(d) No contradiction found: R1-R6 are literal and match the files; rehearsal.patch is the shape reference.
(e) Deliverable: a non-starter with no gas key is diagnosed by the T-COMA-1 family gate (schema, aggregator, composition accept no gas); a running engine still aborts. Decisive check: the new file `6 passed`, wired `85 passed`, and the 9 probe lines plus `corpus equal: True`.

## Assumptions worked past
- The new test file was copied from `recheck/T-COMA-2/tests/` (R4 says "the 6 tests of the rehearsed file") and run red before the source edits.
- First corpus dump run failed because `impl/` did not exist yet; I created it and reran (no code change).
- A commit trailer was refused by `bash_guard`; the commit has no trailer.

## Mutants (R4)
- M1 (`_gasless_non_starter` returns False): `2 failed, 4 passed`: test_non_starter_without_gas_abstains_no_rule, test_non_starter_without_gas_keeps_the_dtc_rule.
- M2 (schema check never raises): `1 failed, 5 passed`: test_request_without_gas_is_refused_for_a_running_engine.
- M3 (aggregator calls the perception detector with no gas): `3 failed, 3 passed`: test_non_starter_without_gas_abstains_no_rule, test_non_starter_without_gas_keeps_the_dtc_rule, test_request_without_gas_runs_for_a_non_starter.
Each mutant was reverted with `git restore <path>`.

## VERIFICATION GATE
CLEAN. Step 1: new file `6 passed`; comlab `531 passed, 4 skipped, 2 errors`. Step 2: registry `5 failed, 502 passed, 4 deselected`; wired `85 passed`; ui `38 passed`. Step 3: probe lines as P2; `corpus 314`; `corpus equal: True`. Step 4: ruff `All checks passed!`.

## CODE REVIEW
Diff equals rehearsal.patch (applied with `git apply`); every changed line is in R1-R6. `_gasless_non_starter` is read in `_diagnose` and `_incomplete_input`. Out-of-scope paths (v1 router, OBD active_dtcs) untouched.

## Time
phase | start | end | minutes | context at end
all | 2026-11-06T09:03:20Z | 2026-11-06T09:06:00Z | ~3 | ABSENT
