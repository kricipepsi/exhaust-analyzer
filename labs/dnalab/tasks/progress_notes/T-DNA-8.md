# T-DNA-8 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-8 reconciles the SymptomLab catalog to the revised 18-pair set, with the
visible-exhaust block fixed to `black_smoke`, `blue_oily_smell`, and
`white_sweet_smell`. The named signal/noise consumer is COMLab proposal
COMLab-A, consumed by `fault_atlas_router`. COMLab routing code remains out of
scope.

## Changed Files

- `labs/symptomlab/tests/test_validator.py`
- `labs/symptomlab/tests/test_models.py`
- `labs/vinlab/VehicleDNA.md`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-8.md`

## Decision

The catalog itself was already reconciled when this session started:
`allowed_combinations.yaml` contained 18 pairs and the target
`visible_exhaust_smoke` block already used `blue_oily_smell` plus
`white_sweet_smell`. COMLab-A also already registered the same 18 keys.

The historical discrepancy remains recorded here for ledger integrity: T-DNA-1
was marked `done` while the audit found the live file at 17 pairs
(`visible_exhaust_smoke = {black_smoke, blue_oily}`), which would trip the
validator construction invariant. T-DNA-8 certifies the now-live 18-pair state
instead of retro-editing the T-DNA-1 note.

Because the live catalog and COMLab-A proposal were already aligned, no
production catalog or COMLab proposal edit was needed. This task added explicit
test coverage for the dropped legacy `blue_oily` string, added model JSON
coverage for the two revised visible-exhaust strings, and tightened
`VehicleDNA.md` so the triage diagram shows the exact enum keys.

## VERIFICATION GATE

- Environment: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Initial catalog count: PowerShell `Select-String` count for `^    - ` in
  `symptomlab/data/allowed_combinations.yaml` printed `18`.
- Initial invariant probe:
  `python -c "from pathlib import Path; from symptomlab.validator import SymptomValidator; SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml')); print('18-pair invariant OK')"`
  printed `18-pair invariant OK`.
- Focused tests after adding coverage:
  `python -m pytest tests/test_validator.py tests/test_models.py -q --tb=short`
  passed: `44 passed`.
- Anti-orphan set equality: YAML pairs and COMLab-A proposal mappings both
  counted `18`; set equality printed `True`; no missing keys on either side.
- Scoped legacy grep:
  `rg --pcre2 "blue_oily(?!_smell)|white_sweet_smell|blue_oily_smell"` across
  the live YAML, COMLab proposal, and `VehicleDNA.md` found only the revised
  `blue_oily_smell` / `white_sweet_smell` strings.
- Ruff: `python -m ruff check symptomlab tests` passed.
- Pyright: `python -m pyright symptomlab tests` passed with `0 errors,
  0 warnings, 0 informations`.
- Final invariant probe printed `18-pair invariant OK`.
- Pair count printed `18`.
- Full SymptomLab tests:
  `python -m pytest tests -x -q --tb=short` passed: `63 passed`.
- DNALab transitive suite:
  `python -m pytest tests -x -q --tb=short` from `labs/dnalab` passed:
  `26 passed`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `allowed_combinations.yaml` defines exactly the revised 18
  `(tier_1, tier_2)` pairs.
- Confirmed `SymptomValidator` constructs from the live catalog and validates
  the revised visible-exhaust strings with the T-DNA-2 `load_state` argument.
- Confirmed the dropped legacy pair
  `("visible_exhaust_smoke", "blue_oily")` now has explicit rejection coverage.
- Confirmed COMLab-A proposal keys exactly match the live YAML pair set.
- Confirmed `VehicleDNA.md` uses the exact revised enum keys in the visible
  exhaust triage diagram.
- Confirmed no `graph/` or `.sandbox-py/` artifacts were touched.
