# T-OBDV2-ARCH-1 — progress note

## Plan

We implemented the ratified Option B to excise `ranking.py`, `family_map.py`, and their corresponding unit tests.
- **Ratified Option:** Option B (excise).
- **Rationale:** Consistent with simple variants dead (the named consumer `OBDLabSimple -> COMLabSimple` is archived and not a live port). No live modules imported `classify_top3` or `rank_candidates`.
- **Files touched (deleted):**
  - `obdlab/obdlab/ranking.py`
  - `obdlab/obdlab/family_map.py`
  - `obdlab/tests/unit/test_ranking.py`
  - `obdlab/tests/unit/test_classify_top3.py`
  - `obdlab/tests/unit/test_family_map.py`

## Verification Gate

- [x] All 379 remaining unit tests in the test suite passed cleanly.
- [x] Verified that no imports or references to the excised modules or functions remain under `labs/obdlab/`.
- [x] Verification run commands:
  - `pytest -q`: Passed (379 passed, 6 skipped).
  - `Get-ChildItem -Recurse -Filter *.py | Select-String "ranking|family_map|classify_top3|rank_candidates|signature_to_family"`: Returned zero external imports/calls under `labs/obdlab/`.

## Code Review

- **Verdicts check:** Removing the unused ranking logic keeps OBDLab aligned strictly with its role as a perception-channel emitter (which should not make internal verdict rankings).
- **Linter and Type check:**
  - `ruff check obdlab/ tests/`: All checks passed.
  - `pyright obdlab/`: 0 errors, 0 warnings.
- **Anti-orphan check / follow-ups:**
  - `O2FailureMode.DEAD` was previously read inside `ranking.py`. With `ranking.py` excised, `O2FailureMode.DEAD` is now read by no live path and is fully orphaned.
  - This has been recorded as coupling for `T-OBDV2-ARCH-2` progress note.
