# T-COMA-17 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-17, HEAD 61b6d61 (spec commit), `git status --porcelain` empty; preconditions print `checked`; patch passes `git apply --check`. Base counts match P1 (comlab 510/4 skipped, wired 176, ui 70, probes 2 failed).
(b) The two new tests fail on base by design: R5 stash run records `3 failed, 4 passed` and `2 failed, 1 passed`.
(c) Expected values come from the task's P2/P3 and R5 (7 comlab, 3 ui tests; mutants 3/1/1/1 failed), not from the test files.
(d) No contradiction found; the patch is rehearsed and the task is mechanical.
(e) Deliverable: apply rehearsal.patch, add the two tests, commit once on fix/T-COMA-17. Decisive check: steps 1-5 give P2/P3 counts and R5 base/mutant counts show the tests catch each change.

Assumptions worked past: none yet.

## R5 results (population: the 7 comlab and 3 ui new tests)
- Base (3 patched .py files stashed): comlab `3 failed, 4 passed`; ui `2 failed, 1 passed`. Stash popped, list empty.
- Mutant A: `3 failed, 4 passed`. B: `1 failed, 6 passed`. C: `1 failed, 6 passed`. D: `1 failed, 6 passed`.
- Each mutant was restored; `cmp` against a copy of the patched file printed no difference. `git diff --stat` after restore: `4 files changed, 60 insertions(+), 8 deletions(-)` (the four patched files, before commit).

## VERIFICATION GATE
- Step 1: comlab `517 passed, 4 skipped`; wired `176 passed`; ui `73 passed`.
- Step 2: `7 passed`; `3 passed`.
- Step 3: `INVALID -> LC-002 lean_condition True FULL_FUSION`; `1 failed, 1 passed, 9 deselected`.
- Step 4: `changed 0 of 314`.
- Step 5: ruff `All checks passed!`; `6 files changed, 177 insertions(+), 8 deletions(-)`; log shows the spec commit and 7337c0e; status shows only the note (the RESULT is written next).

## CODE REVIEW
Read the full patch diff before commit. Every changed line is in the write scope and traces to R1-R4. No new field lacks a reader: the two reasons are read by `routing_notices` and `_confidence_for`. No finding.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T14:14:35Z | 2026-11-13T14:17:07Z | 2.5 | ABSENT

Assumptions worked past: none. The commit message carries no co-author trailer, because `bash_guard` refused a commit command whose text held it.
