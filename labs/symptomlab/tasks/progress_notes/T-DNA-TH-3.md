# T-DNA-TH-3 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-TH-3 adds a SymptomLab-local isolation test harness using controlled
good-18 and bad-17 YAML catalogs plugged into the existing `resolve(...,
allowed_path=...)` and `SymptomValidator(allowed_path)` seams. No production
code, schema fields, enum values, vocabulary strings, graph files, DNALab code,
VINLab code, or COMLab code were edited. The named anti-orphan consumers are
`tests/unit/test_validator.py`, `tests/unit/test_resolve_isolation.py`, and
`tests/unit/test_models.py`.

## Changed Files

- `labs/symptomlab/tests/conftest.py`
- `labs/symptomlab/tests/fixtures/__init__.py`
- `labs/symptomlab/tests/fixtures/allowed_combinations.good18.yaml`
- `labs/symptomlab/tests/fixtures/allowed_combinations.bad17.yaml`
- `labs/symptomlab/tests/unit/__init__.py`
- `labs/symptomlab/tests/unit/test_validator.py`
- `labs/symptomlab/tests/unit/test_resolve_isolation.py`
- `labs/symptomlab/tests/unit/test_models.py`
- `labs/symptomlab/tests/unit/test_symptomdna_from_json.py`
- `labs/symptomlab/tests/unit/test_drift_guard.py`
- `labs/symptomlab/tasks/progress_notes/T-DNA-TH-3.md`
- `labs/dnalab/tasks/PROGRESS.md`

## Decision

The slim `tests/unit/` layout is now in place. Existing flat test modules were
moved into `tests/unit/`, and `tests/fixtures/` now contains a frozen
contract-valid 18-pair catalog plus a deliberately invalid 17-pair catalog.

`tests/conftest.py` exposes `good_allowed_path`, `bad_allowed_path`, and
`make_symptom_dna`. Validator and resolver tests now read the injected fixture
catalogs instead of the packaged production YAML. The drift guard remains as the
single intentional live-catalog check, so the isolated subset can prove
independence from the live file while the full suite still checks production
catalog drift.

## VERIFICATION GATE

- Environment:
  `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Red test:
  `python -m pytest tests/unit -q --tb=short` failed before edits because
  `tests/unit` did not exist: `ERROR: file or directory not found: tests/unit`.
- Syntax:
  `python -m py_compile tests\conftest.py tests\unit\test_validator.py
  tests\unit\test_resolve_isolation.py tests\unit\test_models.py
  tests\unit\test_symptomdna_from_json.py tests\unit\test_drift_guard.py`
  passed.
- Imports:
  `python -c "import importlib; importlib.import_module('symptomlab');
  importlib.import_module('symptomlab.validator');
  importlib.import_module('symptomlab.models')"` passed: `IMPORTS OK`.
- Ruff:
  `ruff check symptomlab tests --fix` passed: `All checks passed!`.
- Pyright:
  `pyright symptomlab tests` passed: `0 errors, 0 warnings, 0 informations`.
- Unit suite:
  `python -m pytest tests/unit -q --tb=short` passed: `63 passed`.
- Live-catalog isolation proof:
  temporarily renamed
  `labs/symptomlab/symptomlab/data/allowed_combinations.yaml`, then ran
  `python -m pytest tests/unit -q --tb=short -k "validator or resolve or models"`:
  `48 passed, 15 deselected`; the file was restored afterward.
- Full SymptomLab tests:
  `python -m pytest tests -q --tb=short` passed: `63 passed`.
- Anti-orphan helper check:
  `Get-ChildItem -Path tests -Recurse -File -Include *.py,*.yaml |
  Select-String -Pattern 'good18|bad17|good_allowed_path|bad_allowed_path|make_symptom_dna'`
  showed both catalog path fixtures and `make_symptom_dna` consumed by named unit
  tests.
- Catalog restore check:
  `allowed_combinations.yaml` exists and
  `allowed_combinations.yaml.t-dna-th-3.tmp` does not exist.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

Pythonskill checklist items applied: type hints, no mutable defaults, no bare
except, pathlib paths, context managers for YAML reads, `is None` assertions
where applicable, sorted imports, and focused test fixture reuse. No production
functions/classes/docstrings were added.

## CODE REVIEW

- Confirmed validator tests construct `SymptomValidator` from the injected
  good-18 fixture and assert the injected bad-17 fixture raises the 18-pair
  invariant error.
- Confirmed resolver isolation tests use `allowed_path=good_allowed_path` and no
  longer call the live default YAML path.
- Confirmed `make_symptom_dna` is consumed by model tests and does not create an
  unused test helper.
- Confirmed `tests/unit/test_drift_guard.py` is the only remaining test module
  that intentionally reads the production catalog.
- Confirmed no production files, `graph/`, or `.sandbox-py/` files were touched.
