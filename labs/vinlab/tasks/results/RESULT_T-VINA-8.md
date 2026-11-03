# Result

## Status
completed

## Summary
`SymptomDNA.from_json` requires `load_state` (F-C6-12). `SymptomValidator.validate` raises `SymptomValidationError` ("must be strings") for a non-string tier (F-C6-13). Code docstrings and six docs state 21 pairs (7 x 3), the oil sub-filters are in the three catalog docs, and ADR-0008 supersedes ADR-0003 (F-C6-11).

## Files changed
models.py, validator.py, tests/unit/test_symptomdna_from_json.py (PIN rename), tests/test_t_vina_8.py (new, 5 cases), docs ADR/BDD/DLD/HLD/LLD/PRD/SYMPTOM_VOCABULARY (all under `repo/labs/symptomlab/`); plus the note and this RESULT.

## Commands executed
`### Verification ###` steps 0-6 as written; mutant runs MR1 and MR2 (below).

## Validation evidence
- step 1 `68 passed`; step 2 `5 passed`
- step 3 dnalab `27 passed`; wired `41 passed`; ui `30 passed`; comlab `526 passed, 4 skipped, 2 errors`
- step 4 `3 passed, 48 deselected` (base: `3 failed`)
- step 5 `0`, `0`, `1`, `1`
- step 6 `All checks passed!`; `git status --porcelain` shows only the note (and this RESULT)
- MR1 `1 failed` (`test_missing_load_state_raises_validation_error`); MR2 `4 failed` (the 4 non-string-tier cases); both files restored, `cmp` identical.

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | steps 1, 2: `68 passed`, `5 passed`; MR1 and MR2 fail the named tests |
| 2 | MET | step 3 counts equal P1 |
| 3 | MET | step 4 `3 passed` |
| 4 | MET | step 5 `0 0 1 1` |
| 5 | MET | ruff clean; one commit `4d6ee41` on `fix/T-VINA-8`; status lists only the note and RESULT |

## Decisions the task did not specify
- "6"/"six"/"6x3" wording changed to 7 where it described the tier_1 count (BDD, HLD, LLD, PRD, SYMPTOM_VOCABULARY).
- `SYMPTOM_VOCABULARY.md` §5 lead sentence reworded: the oil pairs are in the live catalog; only their routing is proposal-only.
- `PRD_SymptomLab.md` T-DNA-8 "Landed" bullet: dropped the size ("full 18 pairs") instead of writing 21, so the history stays in ADR-0008.
- LLD §6 literal block lists `oil_consumption` and its three tier_2 values.

## Pre-existing changes preserved
none (clean tree at start; comlab `case_library.html` restored after the comlab run).

## Rollback
`git revert 4d6ee41` on `fix/T-VINA-8`, or `git restore` per path before push. Not pushed.

## Remaining risks or uncertainties
- Probe `test_f11_combination_count_consistent` stays red by design (ADR keeps its record); not run here.
- pyright NOT RUN (not in Verification).

## Git
```
fix/T-VINA-8
4d6ee41 fix(T-VINA-8): SymptomLab requires load_state, refuses non-string tiers, states the 21-pair catalog
eeeeaa9 spec(T-VINA-8): SymptomLab contract fixes (F-C6-11..13)
```

## Round 2
Status: completed. Correction 01 (R7) applied in one more commit on `fix/T-VINA-8`; round-1 commit unchanged.

- Files changed: `models.py` (R7.4 object checks), `tests/test_t_vina_8.py` (+4 cases), `docs/DLD_SymptomLab.md`, `docs/LLD_SymptomLab.md`, `docs/ADR_SymptomLab.md` (R7.1-R7.3).
- Validation: symptomlab `72 passed`; `test_t_vina_8.py` `9 passed`; dnalab `27`, wired `41`, ui `30`, comlab `526 passed, 4 skipped, 2 errors`; probes `3 passed, 48 deselected`; step 5 `0 0 1 1 0 0 0 0`; ruff clean.
- MR3 (`env` check `if False:`): `3 failed` (the 3 non-object-env cases); file restored, `cmp` identical.
- Criteria 1-5: MET (commands above; criterion 5 shows two implementer commits plus the two spec commits).
- Decisions: reworded the ADR-0008 sentence so the string "Its rejection of" is gone, as the step 5 count requires.
- Pre-existing changes preserved: none; comlab `case_library.html` restored.
- Rollback: `git revert` the round-2 commit.

```
fix/T-VINA-8
597173f fix(T-VINA-8): R7 correction 01 (load_state docs, LLD counts, ADR-0008 attribution, from_json object check)
3f72ac1 spec(T-VINA-8): correction 01 (R7: DLD/LLD load_state, LLD counts, ADR-0008 attribution, from_json object check)
4d6ee41 fix(T-VINA-8): SymptomLab requires load_state, refuses non-string tiers, states the 21-pair catalog
eeeeaa9 spec(T-VINA-8): SymptomLab contract fixes (F-C6-11..13)
```
