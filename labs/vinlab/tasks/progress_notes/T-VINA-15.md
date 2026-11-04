# T-VINA-15 progress note

## Readiness
(a) Starting state matches: branch fix/T-VINA-15, HEAD~1 = 5307de4, `git status --porcelain` empty. Loop-pack HEAD n/a (repo row).
(b) Test fails for intended reason: to be shown by running test_sensor_unknown.py before R1 (expect 3 failed: the 0/0 cases).
(c) Decisive expected value: step 5 `changed 13 {('MAP_ONLY_SPEED_DENSITY','DUAL_MAF_MAP_CROSSCHECK'): 13}`; derived from P1/Context (13 VINs, has_egr=1 gives the heuristic DUAL).
(d) No contradiction found; preconditions printed `checked` with no MISSING/EXISTS.
(e) Deliverable: in `_derive_air_metering`, a stored has_maf=0 and has_map=0 becomes None/None so the heuristic runs, plus 9 tests. Decisive check: vinlab suite 353 passed and effect.py shows exactly 13 VINs moving to DUAL_MAF_MAP_CROSSCHECK.

## Assumptions worked past
none. The commit carries no co-author trailer: the shell guard refused a command containing that trailer text.

## Red gate
Before R1: test_sensor_unknown.py 3 failed, 6 passed (the two real-VIN cases and test_zero_zero_equals_unknown[stored0]).

## Mutants (R3)
Final decoder kept in recheck/T-VINA-15/mut/decoder.final.py; restored with cmp (identical).
- final: 9 passed
- M1 base decoder (git show HEAD~1): 3 failed, 6 passed
- M2 rule `if False:`: 3 failed, 6 passed
- M3 `if not db_maf and not db_map:`: 1 failed, 8 passed

## VERIFICATION GATE
CLEAN. Steps 1-6 as expected: 353 passed 8 skipped; 9 passed; 27/41/30 passed; 14 passed 37 deselected; decoded 1131 changed 13 {(MAP_ONLY_SPEED_DENSITY, DUAL_MAF_MAP_CROSSCHECK): 13}; ruff All checks passed.

## CODE REVIEW
CLEAN. Diff is the 5 R1 lines in _derive_air_metering plus the new test file. No new field or public name.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-04T21:26:54Z | 2026-11-04T21:28:36Z | 1.7 | ABSENT

## Round 2
Clock at start 2026-11-04T21:34:19Z; Cowork correction 01 (commit 511ffbd). Starting state: branch fix/T-VINA-15, round-1 commit 32d3d1c, tree clean apart from the note and RESULT.
Edits made by hand as make_rh2.py makes them: carburettor scope on the rule (4 lines), exact-strategy assert in the real-VIN test, new test_carburettor_zero_zero_is_kept.
- test_sensor_unknown.py: 10 passed. M4 (only db_maf reset): 2 failed, 8 passed. M5 (carburettor line deleted): 1 failed, 9 passed. Final decoder restored, cmp identical (mut/decoder.r2.py).
- vinlab 354 passed, 8 skipped; dnalab 27; wired 41; ui 30; probes 14 passed, 37 deselected.
- effect.py against 51566ca: changed 13 (MAP_ONLY_SPEED_DENSITY to DUAL_MAF_MAP_CROSSCHECK). Against round 1 (32d3d1c): changed 0.
- ruff: All checks passed. Commit 18b60a1.
Assumptions worked past: none.
VERIFICATION GATE: CLEAN. CODE REVIEW: CLEAN (diff is the R5 edits only).

## Time (round 2)
round 2 | 2026-11-04T21:34:19Z | 2026-11-04T21:35:31Z | 1.2 | ABSENT
