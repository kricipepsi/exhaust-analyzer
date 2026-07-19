# T-OBDV2-PURGE-1 — progress note

> Coder: open this with the confirmed `## Plan` (written at task start, before any code),
> then add the `VERIFICATION GATE` and `CODE REVIEW` blocks at task end. STRICT mode:
> the PROGRESS.md row does not flip to `done` until both blocks below are clean.

## Plan

We will perform the following actions:
1. Delete the files [obdlab/ranking.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/ranking.py), [obdlab/family_map.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/family_map.py), [tests/unit/test_ranking.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_ranking.py), [tests/unit/test_classify_top3.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_classify_top3.py), and [tests/unit/test_family_map.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/tests/unit/test_family_map.py).
2. Verify that no live imports/references to `obdlab.ranking`, `obdlab.family_map`, `classify_top3`, `rank_candidates`, or `signature_to_family` exist in the remaining modules or tests using a grep gate.
3. Confirm that the public API surface in [obdlab/__init__.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/__init__.py) imports clean and is unaffected.
4. Run the inner loop validation: `ruff check obdlab/ tests/`, `pyright obdlab/`, and `pytest -x -q` to ensure all tests pass.
5. Run `graphify update .` to keep the knowledge graph current.

## VERIFICATION GATE

1. **File Deletion Verification**:
   - `obdlab/ranking.py` -> Deleted
   - `obdlab/family_map.py` -> Deleted
   - `tests/unit/test_ranking.py` -> Deleted
   - `tests/unit/test_classify_top3.py` -> Deleted
   - `tests/unit/test_family_map.py` -> Deleted
   - Verified that all 5 files no longer exist on disk.

2. **Grep Reference Check**:
   - Run `git grep -E 'obdlab\.(ranking|family_map)|classify_top3|rank_candidates|signature_to_family' -- 'obdlab/' 'tests/'`
   - Result: 0 matches found, confirming no live code/test references remain.

3. **Public Surface Import Validation**:
   - Run `python.exe -c "import obdlab; obdlab.SensorSignalTranslator; obdlab.OBDLivePayload; print('surface OK')"`
   - Result: Output `surface OK` (import is clean).

4. **Inner Loop Validation**:
   - Ruff: `ruff check obdlab/ tests/` -> All checks passed!
   - Pyright: `pyright obdlab/` -> 0 errors, 0 warnings, 0 informations.
   - Pytest: `pytest -x -q` -> 294 passed, 6 skipped (25 tests corresponding to the deleted modules were removed).

5. **Knowledge Graph Update**:
   - Run `graphify update .` -> Graph updated successfully with 81,860 nodes.

## CODE REVIEW

- **API Preservation**: The public API exports in [obdlab/__init__.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/obdlab/obdlab/__init__.py) only expose `SensorSignalTranslator` and `OBDLivePayload`. Both are fully intact and functional.
- **Dead Code Purge**: All 5 removed files were verified to be entirely unused dead code that fed the archived/deprecated simple classifier paths. No functionality or active logic was impacted.
- **No Unrelated Changes**: Only the target files and the progress ledger were modified. The changes strictly conform to the surgical-change rule.
