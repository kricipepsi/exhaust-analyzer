# T-VINA-17 progress note

## Readiness
(a) Starting state matches: branch `fix/T-VINA-17`, `HEAD~1` = `e4ad961`, `git status --porcelain` empty (First action run 2026-11-04T19:44:05Z). Loop-pack HEAD `C:/4DApp` = de7e8c41436dd2b94a1b0325b14bc1e24a3f13f1 (repo-row, no loop commit).
(b) The new rows in `TYPE_CODE_VINS` and the 11-WMI set test fail on the base (WMIs VSA, WDF, WMX, 4JG, VDB not in the set); confirmed by running step 2 after the test edit, before the decoder edit.
(c) Decisive expected value from the spec: `VSA63823413020157` today decodes 2001, must give `None`; `4JGBF71EX7A107518` keeps 2007 (letters at 4-9). P2: step 2 `15 passed` (9 base + 5 + 1).
(d) No contradiction: precheck commands from Preconditions and First action pass; step 5 grep matches the glossary bullet and the `# source:` line (2).
(e) Deliverable: add the five Mercedes WMIs to `_TYPE_CODE_WMIS` with tests and wiki, as `make_rh.py` does. Decisive check: step 2 `15 passed`, vinlab `319 passed, 8 skipped`, M1 `6 failed`, M2 `4 failed`.

## Assumptions worked past
none. Edits made by hand with the Edit tool from the `make_rh.py` strings (that script was read, not run); the Edit result was not diffed against a rehearsal copy.

## Red gate
Step 2 after the test edit, before the decoder edit: `6 failed, 9 passed` (5 `test_type_code_vin_has_no_year` new cases + `test_type_code_set_is_the_measured_one`).

## Mutants (R4)
Copy of `decoder.py` in `C:/4DApp/recheck/T-VINA-17/mut/decoder.py`; each restore confirmed with `cmp`.
- M1 set written back to the 6 T-VINA-2 WMIs: `6 failed, 9 passed`.
- M2 ` and vin[3:9].isdigit()` removed from `_resolve_year`: `4 failed, 11 passed`.

## VERIFICATION GATE
CLEAN. Step 1 `319 passed, 8 skipped`; step 2 `15 passed`; step 3 `27 passed`, `41 passed`, `30 passed`; step 4 `8 passed, 43 deselected`; step 5 `2`; step 6 `All checks passed!`. pyright, `--select S` and import sanity: NOT RUN (the task's Verification lists none).

## CODE REVIEW
Scope: three files only, every line from R1-R3. Provenance: the new `# source:` comment cites the registry measurement. Anti-orphan: no new name; the set is read at `_resolve_year`. Findings: none.

## Time
phase | start | end | minutes | context at end
implement + verify | 2026-11-04T19:44:05Z | 2026-11-04T19:45:59Z | 1.9 | ABSENT

## Round 2
Start 2026-11-04T19:56:22Z, end 2026-11-04T19:57:52Z. Branch `fix/T-VINA-17`, HEAD before = bfa6af8 (Cowork correction commit), round-1 commit 193dc69 kept. Applied the R5 edits of `make_rh2.py` by hand (script read, not run): code comment (5 lines), 6 test comments, new test `test_type_code_vin_with_other_position_10_has_no_year`, wiki paragraph (4 lines).
- Verification: step 1 `320 passed, 8 skipped`; step 2 `16 passed`; step 3 `27`, `41`, `30 passed`; step 4 `8 passed, 43 deselected`; step 5 `2`; ruff `All checks passed!`.
- M3 (`and vin[9] == "1"` added in `_resolve_year`): `1 failed, 15 passed` (the new test). Copy `mut/decoder_r2.py`, restored, `cmp` equal.
- M1 re-run on the round-2 tree: `7 failed, 9 passed`, not 6. The new test also fails when the set is the 6 WMIs, because `WDF` is out. This is the expected effect of R5.3; round-1 M1 stays `6 failed`. M2 re-run: `4 failed, 12 passed`.
- Time: round 2 about 3 min.
