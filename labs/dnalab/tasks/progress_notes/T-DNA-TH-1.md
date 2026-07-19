# T-DNA-TH-1 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-TH-1 adds a DNALab-local isolation test harness for
`assembly.build_vehicle_dna` and `models.VehicleDNA`, using test-only doubles
plugged into the existing `dnalab.assembly._decode_vin` and `_resolve_symptom`
module seams. No production code, schema fields, enum values, vocabulary strings,
or sibling lab code were edited. The named anti-orphan consumers are
`tests/unit/test_assembly.py`, `tests/unit/test_models.py`, and
`tests/unit/test_vehicledna_roundtrip.py`.

## Changed Files

- `labs/dnalab/pyproject.toml`
- `labs/dnalab/tests/conftest.py`
- `labs/dnalab/tests/fixtures/__init__.py`
- `labs/dnalab/tests/unit/__init__.py`
- `labs/dnalab/tests/unit/test_assembly.py`
- `labs/dnalab/tests/unit/test_assembly_integration.py`
- `labs/dnalab/tests/unit/test_models.py`
- `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-TH-1.md`

## Decision

The flat DNALab tests were moved into `tests/unit/`, and the slim
`tests/fixtures/` package was added per `DNA_ISOLATION_HARNESS.md`. The new
`make_vin_dna` and `make_symptom_dna` builders construct sibling dataclasses
directly, so the default DNALab tests no longer run `vinlab.decode`,
`symptomlab.resolve`, or read SymptomLab YAML. `fake_decode_returning` and
`fake_resolve_returning` are consumed by assembly isolation tests that cover the
happy compose path, missing-triage-key guard, and sibling error propagation.

One real-pipeline smoke test remains in
`tests/unit/test_assembly_integration.py`, marked `integration`, so DNALab still
checks the sibling wiring contract without making the real pipeline the default
fixture path.

## VERIFICATION GATE

- Environment:
  `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Baseline before edits:
  `python -m pytest tests\ -q --tb=short` passed: `26 passed`.
- Red test:
  `python -m pytest tests\unit\test_assembly.py -q --tb=short` failed during
  collection because `fake_decode_returning` was not yet present in
  `tests.conftest`.
- Ruff:
  `python -m ruff check dnalab\ tests\` passed: `All checks passed!`.
- Pyright:
  `PYRIGHT_PYTHON_FORCE_VERSION=latest python -m pyright dnalab\ tests\`
  passed: `0 errors, 0 warnings, 0 informations`.
- Catalog-unavailable isolation proof:
  temporarily renamed
  `labs/symptomlab/symptomlab/data/allowed_combinations.yaml`, then ran
  `python -m pytest tests\unit\ -x -q --tb=short -k "not integration"`:
  `26 passed, 1 deselected`; the file was restored afterward.
- Full DNALab tests:
  `python -m pytest tests\ -q --tb=short` passed: `27 passed`.
- Anti-orphan helper check:
  `rg -n "make_vin_dna|make_symptom_dna|fake_decode|fake_resolve" tests\unit\`
  showed every added builder/fake consumed by unit tests.
- Catalog restore check:
  `allowed_combinations.yaml` exists and
  `allowed_combinations.yaml.unavailable_for_dnalab_test` does not exist.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `tests/conftest.py` no longer builds `sample_dna` through the real
  assembly pipeline.
- Confirmed `tests/unit/test_assembly.py` monkeypatches both sibling seams for
  isolated assembly cases.
- Confirmed the missing-triage-key guard raises before `_resolve_symptom` is
  called.
- Confirmed VIN and symptom exceptions propagate from fake sibling callables.
- Confirmed model and round-trip tests build `VehicleDNA` from test builders, not
  real sibling data files.
- Confirmed the only real sibling pipeline call is the marked integration smoke
  test.
- Confirmed no production files, `graph/`, or `.sandbox-py/` files were touched.
