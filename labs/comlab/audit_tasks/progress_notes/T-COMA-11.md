# T-COMA-11 progress note

## Readiness
(a) Start matches: branch fix/T-COMA-11, `d319e8c..HEAD` = spec commit 9febb21, `git status --porcelain` empty, preconditions print `checked` with no MISSING.
(b) Test fails for the intended reason: shown in R3 below (new test on base code, expected 4 failed).
(c) Decisive expected value: P1 probe shows reported 0.95 vs own raw score 0.9; after the fix the verdict reports the named rule's own score (0.9). The test pins this.
(d) No contradiction or missing decision found; every pinned file and literal exists (two `new_top_score = float(scored_rules[0]...)` lines at 2057 and 2104).
(e) Teach-back: after both re-sorts the verdict confidence must be the score of the rule named by fault_code, via `_reported_fault_score`. The decisive check is the new test (4 passed; 4 failed on base) plus the C1 probe printing 0.9.

Assumptions worked past: none.

## R3 results
- Base code (router stashed, new test present): `4 failed`.
- Mutant (discriminator line, 2116, back to `float(scored_rules[0]...)`): `2 failed, 2 passed`. Line restored by hand; `cmp` against a saved copy: identical.

## VERIFICATION GATE
- comlab `510 passed, 4 skipped`; wired `127 passed`; ui `70 passed`.
- New test `4 passed`. C1 probe: `reported: 0.9 own raw score: 0.9`, `1 passed, 6 deselected`.
- ruff: `All checks passed!`. Diff stat d319e8c..HEAD on labs/comlab/comlab: `1 file changed, 14 insertions(+), 2 deletions(-)`.
- v7 corpus 17/314 count: NOT RUN (not in `### Verification ###`; the corpus test cases in the new test pass).

## CODE REVIEW
Scope: only the two pinned edits plus the helper (output of `git diff` read before commit). Anti-orphan: `_reported_fault_score` is read at two call sites. No new field. CLEAN.

## Time
phase | start | end | minutes | context at end
all | 2026-11-07T18:44:58Z | 2026-11-07T18:46:08Z | ~1 | ABSENT
