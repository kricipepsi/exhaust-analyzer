# T-VINA-6 progress note

## Readiness
(a) Start matches: branch `fix/T-VINA-6`, `HEAD~1` = `8b4d343`, `git status --porcelain` empty, map has 0 `DIESEL` rows, preconditions printed `checked`.
(b) The new test fails on the base map: `test_diesel_keys_carry_diesel` finds 0 DIESEL rows, and the BMW N47D20C VIN decodes instead of raising. Shown after the edit by the stash step.
(c) Expected value derived independently: 84 rows (P2, `git diff --numstat` `84 84`); 27 keys in `DIESEL_KEYS`; `apply_fix.py` exits on any other count.
(d) No contradiction found. `decoder.py` lines 594/620 already call `_is_non_petrol` on the fuel value, so data alone is enough (R1).
(e) Deliverable: 84 map rows change `PORT_INJECTION` to `DIESEL` and a new test pins them. Decisive check: step 2 gives `2 passed` with the edit and `2 failed` with the base map.

## Assumptions worked past
- The bash guard refused the commit command when its message held an attribution trailer. I committed with the AGENTS.md form and no trailer.

## VERIFICATION GATE
Run from `C:/4DApp/repo`, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, `--basetemp` under `C:/4DApp/recheck/T-VINA-6/pt/`.
- Step 1 (vinlab, all): `378 passed, 8 skipped`. No failed or error.
- Step 2 (new test): `2 passed`. With the base map (`git stash push` of the map, then `git stash pop`): `2 failed` (`test_diesel_keys_carry_diesel`, `test_diesel_vin_rejected_by_h1`).
- Step 3: wired `85 passed`; ui `49 passed`.
- Step 4: ruff `All checks passed!`; map numstat `84 84`; test `41 0`; log shows spec commit `302a954` and my commit `ee538f8`; `git status --porcelain` shows only this note (before the RESULT).
- `cmp` of the new test with `C:/4DApp/recheck/T-VINA-6/test_h1_diesel_map_rows.py`: identical.
VERDICT: CLEAN

## CODE REVIEW
- Scope: changed paths are the map and the new test, plus the note and RESULT. `decoder.py` is untouched.
- Map diff: 84 lines changed, each `PORT_INJECTION` to `DIESEL` in the fuel field only (`apply_fix.py` asserts one match per line, exits on a count other than 84, keeps LF endings).
- Anti-orphan: no new name in production code. The test reads the map and `decode`.
- Provenance: the test docstring cites TecDoc 1Q2019 and wiki section 10.4.
- Not run: pyright and `ruff --select S` (the task names only ruff). NOT RUN.
No findings.

## Time
phase | start | end | minutes | context at end
implement and verify | 2026-11-07T07:21:34Z | 2026-11-07T07:22:41Z | 1 (clock; later writes after this) | ABSENT

## Revision 02

### Readiness (revision 02)
- (a) Start state matches: branch `fix/T-VINA-6`, HEAD `3ee93cd` (spec revision 02) over `ee538f8`; untracked only this note and the RESULT; preconditions print `checked`. The current test differs from `test_h1_diesel_map_rows_r02.py` (`cmp` exit 1), as expected.
- (b) The test fails for the intended reason: with the base map (`302a954`) the DIESEL-row checks and both H1 VINs must fail; the 2 petrol controls pass (P2: `3 failed, 2 passed`).
- (c) Decisive expected value, derived from the spec: 27 keys, rows per key sum to 84 (`ROWS_PER_KEY` values); with the shipped map step 2 gives `5 passed` (2 H1 VINs + 2 petrol VINs + 1 row test... P2 states 5).
- (d) No contradiction: R3 is a `cp` and `cmp`; the base-map check is authorised in Files to touch (RUNTIME, restored).
- (e) Teach-back: the deliverable is the test file made byte-identical to the r02 file in one new commit on `fix/T-VINA-6`. The decisive check is step 2 giving `5 passed` on the shipped map and `3 failed, 2 passed` on the base map.

### Revision 02 work
- R3: `cp` of `test_h1_diesel_map_rows_r02.py` over the test; `cmp` exit 0. Commit `9e51f6d` on `fix/T-VINA-6`.
- Step 1: `381 passed, 8 skipped`. Step 2: `5 passed`. Step 3: wired `85 passed`; ui `49 passed`.
- Base-map result (`git checkout 302a954 -- <map>`, step 2, `git checkout HEAD -- <map>`): `3 failed, 2 passed`. The failures are `test_diesel_keys_carry_diesel` and both `test_diesel_vin_rejected_by_h1` cases (BMW and Toyota 1KZ-TE). The 2 petrol controls pass. The map was restored (`git status --porcelain` showed no map change).
- Step 4: ruff `All checks passed!`; map numstat `84 84`; log shows `302a954`, `ee538f8`, `3ee93cd`, `9e51f6d`; `git status --porcelain` lists only this note and the RESULT.

### Assumptions worked past (revision 02)
- The commit has no attribution trailer: the bash guard refused the commit command that held one.

VERDICT (revision 02): CLEAN

CODE REVIEW (revision 02): scope is one test file, byte-identical to the r02 file. `decoder.py` and the map are untouched in this run. No findings. pyright and `ruff --select S` NOT RUN (the task names only ruff).

### Time (revision 02)
phase | start | end | minutes | context at end
revision 02 | 2026-11-07T07:30:30Z | 2026-11-07T07:31:29Z | 1 (clock; note writes after this) | ABSENT
