# T-AUD-4h progress note

## Readiness
- (a) Starting state matches: branch fix/T-AUD-4h, HEAD dd24964 (spec commit, descendant of b4c6495, = base), `git status --porcelain` empty; preconditions printed `checked` only.
- (b) Tests are written before the code; they must fail on the base (helper missing -> ImportError; ECT 40.0/69.9 return 3.0 not None). Confirmed by running them before the edit.
- (c) Independent expected values: codes `{"$03":["P0131","P0300"],"$07":["P0131","P0340"]}` -> ordered dedupe `["P0131","P0300","P0340"]`; ECT < 70.0 -> None, ECT >= 70.0 -> 3.0 (the fixture trim).
- (d) No contradiction found: R1-R5, Files to touch and Verification agree; FF test fixture in the existing T-AUD-4g test has no coolant_temp_c so it is unchanged by R2.
- (e) Teach-back: add `_with_user_dtcs` so user DTC codes reach OBDLab as `active_dtcs` (explicit non-empty wins), and make the registry shim skip ff trims when FF coolant < 70.0. Decisive check: step 4 prints 0 verdict/gate changes for ff and UI=1 dtc, and each R4 mutant fails its named test.

## Time

phase | start | end | minutes | context at end
implement+verify | 2026-11-05T16:30:16Z | 2026-11-05T16:36:37Z | 6.3 | ABSENT

## Assumptions worked past
- `_with_user_dtcs` takes `dtc_inputs: Any` (the raw argument of `diagnose`) and reads it through `_as_dict`, so a non-dict raises the same TypeError as `_run_dtclab` does.
- A non-numeric `coolant_temp_c` in the FF counts as absent (no cold gate), matching the "present" wording of R2.
- A stray no-op shell command ran early (a heredoc mix-up) and was backgrounded; `git status` showed it changed no file.

## VERIFICATION GATE
CLEAN. Steps 1-5 as in the RESULT; ruff `All checks passed!`; no baseline or pyright run beyond the task's list (pyright NOT RUN, not in Verification).

## CODE REVIEW
Scope: 3 modified files + 1 new test, all in Files to touch. Consumer comment present on the new key. Threshold 70.0 is a named constant citing OBDLab §9. No cross-lab import added. No findings.
