# T-COMA-12 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-12, log 101f042..HEAD = 55c92f9 (spec commit), porcelain empty. Base P1 reproduced: comlab 510 passed, 4 skipped; wired 143 passed; ui 70 passed; three probes 2 failed, 1 passed.
(b) The new test is Cowork's; it must fail on base code (9 failed, 4 passed) - checked in R5 below.
(c) Decisive values from the task: new test 13 passed after edit; probes 3 passed; v7 corpus changed 0 of 314.
(d) No contradiction or missing decision found; preconditions print `checked`.
(e) Teach-back: apply R1-R3 to fault_atlas_router.py with rehearse.py and add the Cowork test, so each family is lifted once, a nominal 0.02 gap abstains and the override regex is ^P030[0-9]$. Decisive check: step 2 gives 13 passed (9 failed on base), probes 3 passed and corpus changed 0 of 314.

## R5 results
- Base (stash of router): `9 failed, 4 passed`.
- Mutant A (set -> list in `_discriminator_families`): `4 failed, 9 passed`.
- Mutant B (`_MARGIN_EPSILON = 0.0`): `1 failed, 12 passed`.
- Both lines restored by hand; router byte-identical to the pre-mutant copy (`cmp`); `git diff --stat` `1 file changed, 22 insertions(+), 13 deletions(-)` (router only; test file untracked then).

## VERIFICATION GATE
1 comlab `510 passed, 4 skipped`; wired `156 passed`; ui `70 passed`. 2 new test `13 passed`. 3 probes `3 passed`. 4 `changed 0 of 314`. 5 ruff `All checks passed!`; `git diff --stat 101f042 HEAD -- labs/comlab/comlab apps` `2 files changed, 72 insertions(+), 13 deletions(-)`; log: 35f5230 plus spec commit 55c92f9; porcelain: the note and the RESULT only.

## CODE REVIEW
Diff read: only R1-R3 lines in the router; test file `cmp`-identical to Cowork's. Anti-orphan: `_discriminator_families`, `_within_abstain_margin` (2 sites) and `_MARGIN_EPSILON` are all read in the router. No out-of-scope edit.

## Assumptions worked past
- The commit message has no co-author trailer: `bash_guard` refused every command whose text held the assistant's name. The identity flags alone passed.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T10:58:00Z | 2026-11-13T11:00:03Z | 2 (clock) | ABSENT
