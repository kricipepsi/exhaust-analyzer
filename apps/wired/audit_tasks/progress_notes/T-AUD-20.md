# T-AUD-20 progress note

## Readiness
(a) Start matches: branch fix/T-AUD-20, base 5aa3528 (spec commit, descendant of 167b2d6), porcelain clean, preconditions print `checked`.
(b) Test fails for the intended reason: base run `3 failed, 1 passed`; the cold bucket reaches bound matching.
(c) Expected value derived from GAS_VOCABULARY §7 and R1: `(SAMPLE_INVALID, INVALID)`; base lab suite without the new file `215 passed, 2 skipped, 4 deselected` matches P2.
(d) No contradiction or missing decision.
(e) Deliverable: classify() returns SAMPLE_INVALID/INVALID for the cold bucket after the CRANKING step, with the vocab text updated and a 4-test file. Decisive check: new tests `4 passed`, lab suite `219 passed`, corpus `differ 0`.

## Assumptions worked past
none

## VERIFICATION GATE
CLEAN. Step 1: `4 passed`; `219 passed, 2 skipped, 4 deselected`; ruff `All checks passed!`. Step 2: `corpus 314`, `differ 0`, wired `106 passed`, `notimpl 8`.

## CODE REVIEW
Diff is the rehearsed edit: 3 lines in rule_engine.py (step 0b after CRANKING), one sentence in GAS_VOCABULARY.md §7, one new test file. No scope drift. Anti-orphan: no new name.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-06T23:57:56Z | 2026-11-07T00:00Z | ~2 (clock) | ABSENT
