# T-OIL-3 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

Added the five oil-consumption fault-atlas nodes `P_NEW_09` through `P_NEW_13` to
`comlab/config/kg/mechanical_wear.json`. They remain in COMLab's canonical
`mechanical_wear` KG family; the three new oil fault-family labels are registered as
human-facing proposal targets:

- `Engine Mechanical (Piston Rings)`
- `Engine Mechanical (PCV/Crankcase)`
- `Engine Mechanical (Turbo Oil Seal)`

Registered `COMLab-OIL-KG` in `comlab/config/proposals/entries.yaml` so the nodes and
family labels are proposal-bounded until T-OIL-4 adds routing rules. No routing behavior
was changed in this task.

## Changed Files

- `labs/comlab/comlab/config/kg/mechanical_wear.json`
- `labs/comlab/comlab/config/proposals/entries.yaml`
- `labs/comlab/tests/unit/test_oil_consumption_kg.py`
- `labs/comlab/tests/unit/test_kg_population.py`
- `labs/comlab/tests/unit/test_fault_atlas_kg.py`
- `labs/comlab/tests/e2e/test_kg_registry_consistency.py`
- `planning/oil_consumption/PROGRESS.md`
- `Vault/tasks/T-GAS-VAULT-OIL_refresh_gaslab_vault_oil.md`

## Verification Gate

- RED: `python -m pytest tests/unit/test_oil_consumption_kg.py -q --tb=short` failed
  because `P_NEW_09` and `COMLab-OIL-KG` were missing.
- GREEN: `python -m pytest tests/unit/test_oil_consumption_kg.py tests/unit/test_kg_population.py tests/unit/test_fault_atlas_kg.py tests/e2e/test_kg_registry_consistency.py -q --tb=short`
  passed: 31 tests.
- `python -m ruff check comlab tests` passed.
- `python -m pyright tests/unit/test_oil_consumption_kg.py tests/unit/test_kg_population.py tests/unit/test_fault_atlas_kg.py tests/e2e/test_kg_registry_consistency.py`
  passed with 0 errors.
- `python -m pytest tests -q --tb=short` passed: 339 passed, 6 skipped.
- Full `python -m pyright comlab tests` remains blocked by existing optional/member
  and fixture typing debt in `fault_atlas_router.py`, `test_fault_atlas_router*.py`,
  `test_power_loss_analytics.py`, `test_symptom_prior.py`, and `test_tag_discriminator.py`;
  no errors were reported in the files touched for T-OIL-3.

## Next

T-OIL-4 is now the next pending row in `planning/oil_consumption/PROGRESS.md`.
