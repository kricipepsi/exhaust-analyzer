# T-VINA-2 progress note

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to finish | 2026-11-04T08:46:26Z | 2026-11-04T08:48:20Z | 1.9 | ABSENT |

## Readiness
(a) Starting state matches: branch `fix/T-VINA-2`, base (spec commit) `0f8dc05`, child of `02ebfba`; `git status --porcelain` empty. Preconditions: `checked`, no MISSING/EXISTS. P1 reproduced: vinlab `216 passed, 8 skipped`; probes `3 failed, 5 passed` (WDB1240261A102470, WDD1770441J098476, WBA4W9C5ZLYYYYYYY).
(b) The new test is run before R1/R2 and must fail on the 3 type-code VINs only (the decoder returns 1990-2010 years there today).
(c) Expected values derived from the spec: type-code VINs -> `model_year None` (position 10 = plant code `1`); North American form WDBED30DXLB097097 -> L=1990, WDBSK74F75F093354 -> 5=2005, WME01MC011H080963 -> 1=2001; VF1CB05CF25935016 -> 2=2002. Anchors all found at the cited strings (decoder.py:117, :817; test_decoder.py:338; wiki §10.6 line 157).
(d) No contradiction: R1-R5 files are all in Files to touch; steps 1-6 do not conflict.
(e) Deliverable: a `_TYPE_CODE_WMIS` set and a rule in `_resolve_year` that returns `(None, None)` for those WMIs when positions 4-9 are digits, plus tests, one updated expectation and the wiki paragraph. Decisive check: step 1 `224 passed, 8 skipped`, step 2 `8 passed`, probes `1 failed, 7 passed`, and mutants M1/M2 each fail 3.

## Assumptions worked past
none. The note and RESULT stay uncommitted: step 6 expects them as the only entries in `git status --porcelain`.

## Mutants
M1 (` and vin[3:9].isdigit()` removed): `test_north_american_form_keeps_the_year` 3 failed, 5 passed. M2 (`if False:`): `test_type_code_vin_has_no_year` 3 failed, 5 passed. Both restored from `C:/4DApp/recheck/T-VINA-2/mut/decoder.py`; `cmp` clean.
Red gate: before R1/R2 the new file gave `4 failed, 4 passed` (3 type-code VINs plus the set import).

## VERIFICATION GATE
CLEAN. Step 1 `224 passed, 8 skipped`; step 2 `8 passed`; step 3 dnalab `27 passed`, wired `41 passed`, ui `30 passed`; step 4 `1 failed, 7 passed` (only WBA4W9C5ZLYYYYYYY, T-VINA-3); step 5 `3`; step 6 ruff `All checks passed!`, commit `069e188` after spec commit `0f8dc05`. Previous decisive failures (WDB1240261A102470, WDD1770441J098476) now pass. pyright and `ruff --select S` were not named by the task: NOT RUN.

## CODE REVIEW
Scope: the diff is the four code and wiki paths, each line traced to R1-R5. Provenance: the set carries a `# source:` comment. Anti-orphan: `_TYPE_CODE_WMIS` is read in `_resolve_year` and in the new test. No finding.

## Round 2
Correction 01 (spec commit 2257cc9). R6.1: "plant code" replaced by "a code that is not a model year" in decoder.py comment, the test_decoder.py row comment and wiki §10.6 (grep -c "plant code" = 0 in all three). R6.2: added `test_numeric_positions_outside_the_set_keep_the_year` (`_resolve_year("VF11234562A123456", {})[0] == 2002`).
M3 (`vin[:3] in _TYPE_CODE_WMIS and ` removed): that test fails (1 failed, 8 passed); decoder.py restored, `cmp` clean.
Verification: vinlab `225 passed, 8 skipped`; new file `9 passed`; dnalab `27 passed`; wired `41 passed`; ui `30 passed`; probes `1 failed, 7 passed` (WBA4W9C5ZLYYYYYYY, T-VINA-3); doc grep `3`; ruff `All checks passed!`. Round 2 ended 2026-11-04T08:53:22Z. Commit below.
