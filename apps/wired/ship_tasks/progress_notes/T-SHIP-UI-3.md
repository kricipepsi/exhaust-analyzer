# Progress note — T-SHIP-UI-3
**Date:** 2026-07-08 · **Mode:** STRICT · **Runner:** Antigravity (omp coder)

## Plan
Implement per-field `?` hover tooltips for all input fields (sidebar, 8 expanders, DTC/FF/$06 rows) displaying lay-readable explanations and allowed ranges/options from a unified `FIELD_HELP` dict in `ui_payload.py` to prevent help-and-enforcement drift. App inputs share constants for min/max limits. Write unit tests to check coverage, format, and constant identity check.

## Implementation
- `apps/ui/ui_payload.py`: Defined the `FieldHelp` dataclass, shared range constants for numeric inputs, and the `FIELD_HELP` dictionary containing explanations and ranges/options for all flat widget keys consumed by the payload mapping.
- `apps/ui/app.py`: Updated all module checkboxes, text inputs, selectboxes, sliders, and number inputs to use `FIELD_HELP[key].get_tooltip()` for help hovers, and the shared range constants for min/max limits. Updated `_check_radio` to accept `help_str` and forward it to individual checkboxes.
- `apps/ui/tests/test_ui.py`: Added unit tests verifying help tooltips format, coverage of all widget keys queried in `ui_payload.py`, and range constants bounds equality.

## VERIFICATION GATE — T-SHIP-UI-3
1. Compile : PASS  (apps/ui/app.py, apps/ui/ui_payload.py, apps/ui/tests/test_ui.py)
2. Lint    : PASS  (ruff)
3. Types   : PASS  (pyright, 0 errors)
4. Tests   : PASS  (PYTHONPATH=apps/ui:labs/comlab pytest apps/ui/tests/test_ui.py -> 8 passed)
5. Contract: PASS  (tooltip constants match widget constraints)
6. Orphan  : N-A  (UI task only, no custom COMLab consumer mapped)
Result: CLEAN

## CODE REVIEW — T-SHIP-UI-3
Scope         : PASS  (only files under apps/ui touched)
Composition   : PASS  (no engine or lab edits)
Consumers     : PASS  (no new fields mapped)
Literals      : PASS  (limits cited and shared as constants)
Docstrings    : PASS  (module-level and helpers documented)
Craft (WARN)  : depth ok (thin UI layer), deletion check clean (no unused variables/imports), seam is UI-only, interface works
Result: CLEAN
