# T-OIL-1 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

We added the `oil_consumption` tier_1 category with its 3 tier_2 markers to [allowed_combinations.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/data/allowed_combinations.yaml). We updated the invariant limit from 18 to 21 in [validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/validator.py). We renamed the test fixture [allowed_combinations.good18.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/fixtures/allowed_combinations.good18.yaml) to [allowed_combinations.good21.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/fixtures/allowed_combinations.good21.yaml) and added the 3 new pairs. We updated [test_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_validator.py) and [test_drift_guard.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_drift_guard.py) to assert 21 pairs instead of 18, and updated the fixture path in [conftest.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/conftest.py).

To prevent orphan markers, we registered the 3 new markers as proposed mappings under `COMLab-A` in [entries.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/entries.yaml). The `symptom_prior.yaml` updates have been deferred to `T-OIL-4` because the new fault families (e.g. PCV/Crankcase, Piston Rings) do not exist in the active COMLab schemas yet.

## Changed Files

- [labs/symptomlab/symptomlab/data/allowed_combinations.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/data/allowed_combinations.yaml)
- [labs/symptomlab/symptomlab/validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/validator.py)
- [labs/symptomlab/tests/conftest.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/conftest.py)
- [labs/symptomlab/tests/fixtures/allowed_combinations.good21.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/fixtures/allowed_combinations.good21.yaml)
- [labs/symptomlab/tests/unit/test_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_validator.py)
- [labs/symptomlab/tests/unit/test_drift_guard.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_drift_guard.py)
- [labs/comlab/comlab/config/proposals/entries.yaml](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/config/proposals/entries.yaml)

## VERIFICATION GATE

- **symptomlab**: `ruff check symptomlab/` and `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m pyright symptomlab/` passed with 0 errors/warnings.
- **pytest**: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m pytest tests -x -q --tb=short` in `labs/symptomlab` passed all 63 tests.
- **dnalab (transitive)**: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m pytest tests -x -q --tb=short` in `labs/dnalab` passed all 27 tests.
- **21-pair invariant check**: Confirmed with command line test. YAML holds 21 pairs.
- **Anti-orphan check**: Each new marker appears in `labs/comlab/comlab/config/proposals/entries.yaml`.

## CODE REVIEW

- Catalog size increased from 18 to 21 pairs with the addition of the `oil_consumption` tier_1 category and its three markers.
- Validator class strictly validates the new size constraint.
- No schema or model field changes introduced.
- Tests updated to match new reference data, including drift guard and validator assertions.
