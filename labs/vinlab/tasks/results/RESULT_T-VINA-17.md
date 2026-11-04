# Result

## Status
completed

## Summary
Added `VSA`, `WDF`, `WMX`, `4JG` and `VDB` to `_TYPE_CODE_WMIS`, with the registry `# source:` comment, 6 test rows, the set test and the wiki §10.6 paragraph and glossary bullet. `VSA63823413020157` now decodes `model_year = None`.

## Files changed
- `labs/vinlab/vinlab/decoder.py`
- `labs/vinlab/tests/unit/test_type_code_year.py`
- `labs/vinlab/wiki/10_decode_scope_rules.md`
- `labs/vinlab/tasks/progress_notes/T-VINA-17.md`, this file (new)

## Commands executed
First action and Preconditions; Verification steps 1-6; R4 mutants M1 and M2 (see the note).

## Validation evidence
- Step 1 `319 passed, 8 skipped`; step 2 `15 passed`; step 3 `27 passed`, `41 passed`, `30 passed`; step 4 `8 passed, 43 deselected`; step 5 `2`; step 6 `All checks passed!`.
- Red gate before the decoder edit: step 2 `6 failed, 9 passed`.
- M1 `6 failed, 9 passed`; M2 `4 failed, 11 passed`.

## Criteria
1. MET: step 1 `319 passed, 8 skipped`, step 2 `15 passed`, M1 6 failed, M2 4 failed.
2. MET: dnalab 27, wired 41, ui 30.
3. MET: probes `8 passed, 43 deselected`.
4. MET: step 5 prints `2`.
5. MET: ruff clean; one commit `193dc69` after the spec commit `c9a2c0d`; `git status --porcelain` shows only the note and this RESULT.

## Decisions the task did not specify
none. The commit message carries the attribution trailer the session required.

## Pre-existing changes preserved
None existed in `repo/` (clean at start).

## Rollback
`git -C repo reset` is not needed; revert commit `193dc69` on `fix/T-VINA-17`.

## Remaining risks or uncertainties
P3 counts were taken from Cowork's measurement and were not re-run. WHE, WDA, WD3, WDZ stay out of the set by task scope.

## Git
```
fix/T-VINA-17
193dc69 fix(T-VINA-17): add VSA, WDF, WMX, 4JG, VDB to the type-code WMIs
c9a2c0d vina: T-VINA-17 spec (F-R3-3: five more type-code WMIs, registry-measured)
```

## Round 2
Status: completed. Commit on `fix/T-VINA-17` after correction commit bfa6af8; round-1 commit 193dc69 kept.
- Changed: `decoder.py` source comment, `test_type_code_year.py` comments and one new test, wiki §10.6 paragraph (R5.1-R5.3).
- Evidence: vinlab `320 passed, 8 skipped`; `test_type_code_year.py` `16 passed`; dnalab 27, wired 41, ui 30; probes `8 passed, 43 deselected`; step 5 `2`; ruff clean. M3 `1 failed`. M1 on the round-2 tree `7 failed` (the new WDF test also fails with the 6-WMI set); M2 `4 failed`.
- Criteria 1-5: MET (criterion 1 with the M1 count noted above).
- Decisions the task did not specify: none beyond the M1 re-run count.
- Rollback: revert the round-2 commit.
- Git:
```
fix/T-VINA-17
44670bc fix(T-VINA-17): round 2, exact counts in comment and wiki, non-1 position-10 test
bfa6af8 vina: T-VINA-17 correction 01 (second review: wording, labels, non-1 position-10 test)
193dc69 fix(T-VINA-17): add VSA, WDF, WMX, 4JG, VDB to the type-code WMIs
c9a2c0d vina: T-VINA-17 spec (F-R3-3: five more type-code WMIs, registry-measured)
```
