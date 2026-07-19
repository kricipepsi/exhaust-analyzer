## Plan

Verify that all unit tests in `labs/symptomlab/tests/unit/` run green and assert meaningful validator/model rules. We will execute `python -m ruff check tests`, `python -m pyright tests`, and `python -m pytest -q` from `labs/symptomlab` directory. The task is expected to fold into `T-SYMGRAPH-2` since the existing tests are already robust and green.

## Rule Map

- **`test_drift_guard.py`**: Asserts that allowed symptom combinations in `allowed_combinations.yaml` align with the authoritative triage mapping diagram in `VehicleDNA.md`.
- **`test_models.py`**: Asserts the schema keys, serialization structure, immutability, and string values of enums (`OccursDuring`, `EngineState`, `LoadState`) in `symptomlab.models`.
- **`test_resolve_isolation.py`**: Asserts instance caching and resolution isolation under independent paths in `_get_validator` and `resolve()`.
- **`test_symptomdna_from_json.py`**: Asserts round-trip deserialization, validation of required fields, validation of enum string values, and intentional absence of pair validation in `SymptomDNA.from_json`.
- **`test_validator.py`**: Asserts `SymptomValidator` validation logic, rejection of incorrect catalog sizes, correct validation of all 21 allowed combinations, parameter enum validations, JSON shape, and hashing support.

## Verification

### Commands
```powershell
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\symptomlab
python -m ruff check tests
python -m pyright tests
python -m pytest -q
```

### Results
- **Ruff check**: Passed.
- **Pyright**: Passed (0 errors, 0 warnings).
- **Pytest**: 63 passed in 0.41s.

Note: Since all tests are green and contain meaningful assertions mapped to validator/model rules, execution is folded directly into `T-SYMGRAPH-2`.
