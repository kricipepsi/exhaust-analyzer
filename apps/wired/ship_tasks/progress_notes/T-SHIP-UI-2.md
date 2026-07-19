# Progress note — T-SHIP-UI-2
**Date:** 2026-07-08 · **Mode:** STRICT · **Runner:** Agy (omp coder)

## Plan
Build the powertrain diagnostic Streamlit UI in `apps/ui/app.py` per the T-SHIP-UI-1 contract and the Field-Placement Map. Untouched widgets must remain absent from the payload. Render ranked top-3 differential candidate cards, first-class abstain outcome, and the calibration caveat footer.

## Implementation
- `apps/ui/ui_payload.py`: Maps flat Streamlit widget values to the structured raw_inputs dict expected by `wired.diagnose()`. Untouched widgets are omitted.
- `apps/ui/app.py`: Streamlit frontend with sidebar module picker, VIN lookup (decoded via `vinlab`), overrides, symptom catalog, and 8 central expanders (including the new Advanced signals expander).
- `apps/ui/tests/test_ui.py`: Unit and E2E tests verifying widget→payload mapping, MW-002 E2E diagnosis, and stoichiometric abstain case.
- `apps/ui/4DLab_UI_FieldMap.md`: Updated provenance note `apps/wiredV2` -> `apps/wired`.

## VERIFICATION GATE — T-SHIP-UI-2
1. Lint    : PASS (ruff clean on app.py, ui_payload.py, and test_ui.py)
2. Tests   : PASS (pytest apps/ui/tests/test_ui.py -> 5 passed)
3. E2E     : PASS (MW-002 fixture returns fault_code=MW-002, perfect stoich case abstains and renders correctly)
4. Types   : PASS (pyright clean on app.py, ui_payload.py, and test_ui.py with appropriate PYTHONPATH)
Result: CLEAN

## CODE REVIEW — T-SHIP-UI-2
1. Scope     : PASS (UI app, helper payload, tests, and FieldMap note only; no lab or composition edits)
2. Consumers : PASS (All 36 advanced columns wired to obd/gas payloads; mapped to named integration shim consumers)
3. Honesty   : PASS (Abstain state is first-class, calibration caveat footer displayed verbatim)
Result: CLEAN
