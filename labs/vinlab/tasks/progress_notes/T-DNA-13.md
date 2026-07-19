# T-DNA-13 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

Implemented all three clarity/correctness fixes defined in the task spec:
1. **Part A (D1):** Unified `to_json_payload()` (dict) and `to_json()` (str) naming conventions across the three models (`VinDNA`, `SymptomDNA` / `EnvironmentalConditions`, and `VehicleDNA`).
2. **Part B (V2):** Clarified the checksum bypass comment in `decoder.py` to state that `0` is intentionally treated as a dummy/bypass marker.
3. **Part C (V3):** Replaced bare-string enum comparisons in `decoder.py` with proper enum members (`FuelDeliveryType.CARBURETOR`, `FuelDeliveryType.GDI`, `InductionType.TURBOCHARGED`, and `InductionType.SUPERCHARGED`).

No JSON wire format modifications were made.

## Changed Files

- `labs/vinlab/vinlab/models.py` (updated `VinDNA` serialization methods)
- `labs/symptomlab/symptomlab/models.py` (updated `SymptomDNA` / `EnvironmentalConditions` serialization methods)
- `labs/dnalab/dnalab/models.py` (updated `VehicleDNA` to call `.to_json_payload()`)
- `labs/vinlab/vinlab/decoder.py` (aligned V2 comments and resolved V3 bare-string enum comparisons)
- `labs/symptomlab/tests/unit/test_models.py` (updated caller assertions)
- `labs/symptomlab/tests/unit/test_symptomdna_from_json.py` (updated caller assertions)
- `labs/symptomlab/tests/unit/test_validator.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_air_metering.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_contract_conformance.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_csv_suite.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_models.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_vindna_from_json.py` (updated caller assertions)
- `labs/vinlab/tests/unit/test_vindna_roundtrip.py` (updated round-trip to assert dictionary shape)

## VERIFICATION GATE

1. **Ruff check:** passed cleanly for all touched labs.
2. **Pyright check:** passed cleanly with 0 errors/warnings on `vinlab`, `symptomlab`, and `dnalab` packages and tests.
3. **Pytest runs:**
   - `vinlab` tests: 177 passed.
   - `symptomlab` tests: 63 passed.
   - `dnalab` tests: 27 passed.
   - `comlab` tests: 337 passed.
4. **Negative proof / grep:** verified no bare-string comparisons remain in `decoder.py` for `CARBURETOR`, `TURBOCHARGED`, `SUPERCHARGED`, or `GDI`.

## CODE REVIEW

All success criteria met:
- Method signatures are unified.
- Checksum comments match logic.
- Type safety improved on comparisons without modifying runtime output.
