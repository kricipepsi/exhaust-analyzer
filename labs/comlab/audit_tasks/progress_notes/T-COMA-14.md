# T-COMA-14 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-14, one spec commit d8f3cfb over e531528, `git status --porcelain` empty; P1 baseline reproduced (comlab 510 passed 4 skipped; wired 167 passed; ui 70 passed).
(b) The new test is expected to fail on the base (ff dispatch field + RM-004 evidence); confirmed in R3 below.
(c) Decisive values: base `2 failed, 1 passed`, after `3 passed`; derived from the test: fuel_pressure_kpa is absent from FreezeFrameRecord, RM-004 has two obd rows on base.
(d) No contradiction found; preconditions all present.
(e) Deliverable: remove the dead fuel_pressure dispatch entry and RM-004 row, add the schema-field test. Decisive check: new test `3 passed` (`2 failed, 1 passed` on base) and v7 corpus `changed 0 of 314`.
Assumptions worked past: none.

## R3
- Base (`git stash push labs/comlab/registry`): new test `2 failed, 1 passed`; stash popped.
- Mutant (deleted line restored after `o2_downstream`): `1 failed, 2 passed`; line deleted again by hand, `git diff --stat` back to 2 files, 9 deletions.
- After: `3 passed`.

## VERIFICATION GATE
step 1 comlab `510 passed, 4 skipped`; wired `170 passed`; ui `70 passed`. step 2 `3 passed`. step 3 `0`, `0`. step 4 `changed 0 of 314`. step 5 ruff `All checks passed!`; diff stat `3 files changed, 39 insertions(+), 9 deletions(-)`; one new commit 55d55d6 after spec d8f3cfb.

## CODE REVIEW
Diff: one dispatch line and one RM-004 row removed, plus the new test (copied, `cmp` identical). Nothing else changed. Audit probe `test_fuel_pressure_pid_resolvable` now raises KeyError by design (R4); not edited.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T11:15:55Z | 2026-11-13T11:18:03Z | 2 | ABSENT
