# T-COMA-7 progress note

## Readiness
(a) Start matches: branch `fix/T-COMA-7`, `git log 42cf560..HEAD` = spec commit 993109f, `git status --porcelain` empty. P1 base counts reproduced: comlab 508 passed 4 skipped; wired 115 passed; ui 70 passed; probe prints WARNING_DEGRADED_PERFORMANCE and fails.
(b) The new test must fail on base code: R3 shows `3 failed, 3 passed` (run before commit).
(c) Expected value derived from the wiki rule: flashing MIL plus confirmed P030x gives CRITICAL_IMMEDIATE_STOP; the other 3 cases (one condition only) stay unchanged. Test: 6 cases, 3 forced, 3 not.
(d) No contradiction found; all preconditions exist.
(e) Teach-back: run apply_fix.py to route the v2 return through apply_catalyst_damage_override, and add the 6-case test. Decisive check: the new test goes 3 failed -> 6 passed and the C1 probe prints CRITICAL_IMMEDIATE_STOP.

## Assumptions worked past
none yet
Assumption: R3 base failure was run with the new test copied in and the fix not yet applied (same code as the stash route); result `3 failed, 3 passed`.
Assumption: the v7 corpus check in P2 is not in `### Verification ###`; NOT RUN.

## R3
- Base (fix not applied): `3 failed, 3 passed`.
- Mutant (`isinstance(_req, str)`): `3 failed, 3 passed`. Line restored by hand; `git diff --stat`: `1 file changed, 12 insertions(+), 1 deletion(-)`.

## VERIFICATION GATE
Step 1: comlab `508 passed, 4 skipped`; wired `121 passed`; ui `70 passed`. Step 2: `6 passed`. Step 3: `verdict: MF-001 misfire severity: CRITICAL_IMMEDIATE_STOP`, `1 passed, 6 deselected`. Step 4: ruff `All checks passed!`; diff stat `1 file changed, 12 insertions(+), 1 deletion(-)`; one new commit c697f9a; status lists only the note (and RESULT).

## CODE REVIEW
Diff is the apply_fix.py output only; every line traces to R1. Scope clean. No new field. Test file is a byte copy (cmp ok).

## Time
phase | start | end | minutes | context at end
all | 2026-11-07T17:16:34Z | 2026-11-07T17:18:17Z | 1.7 | ABSENT
