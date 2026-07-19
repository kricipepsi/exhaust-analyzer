# T-DNA-TH-2 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-TH-2 adds a VINLab-local isolation test harness using controlled mini
fixture data plugged into the existing `decode(vin, data_dir=...)` and
`lookup_engine_ref(db_path, ...)` seams. No production code, schema fields, enum
values, vocabulary strings, graph files, DNALab code, SymptomLab code, or COMLab
code were edited. The named anti-orphan consumers are
`tests/unit/test_decode_isolation.py`, `tests/unit/test_horizon.py`,
`tests/unit/test_stress_rpm.py`, and `tests/unit/test_switches.py`.

## Changed Files

- `labs/vinlab/tests/conftest.py`
- `labs/vinlab/tests/fixtures/__init__.py`
- `labs/vinlab/tests/fixtures/mini_data/README.md`
- `labs/vinlab/tests/fixtures/mini_data/seed.sql`
- `labs/vinlab/tests/fixtures/mini_data/vds_engine_map.csv`
- `labs/vinlab/tests/fixtures/mini_data/wmi.csv`
- `labs/vinlab/tests/fixtures/mini_data/years.csv`
- `labs/vinlab/tests/unit/__init__.py`
- `labs/vinlab/tests/unit/test_decode_isolation.py`
- `labs/vinlab/tests/unit/test_horizon.py`
- `labs/vinlab/tests/unit/test_stress_rpm.py`
- `labs/vinlab/tests/unit/test_switches.py`
- `labs/vinlab/tests/unit/` moved flat legacy test modules
- `labs/vinlab/tasks/progress_notes/T-DNA-TH-2.md`
- `labs/dnalab/tasks/PROGRESS.md`

## Decision

The slim `tests/unit/` layout is now in place. Existing flat test modules were
moved into `tests/unit/`; the superseded root `test_overlay.py` horizon cases
were migrated into dedicated `tests/unit/test_horizon.py`, and the old
production-data-coupled root `test_decode_isolation.py` was replaced by a mini
data-dir version under `tests/unit/`.

The fixture source in `tests/fixtures/mini_data/` contains tiny CSV files and a
reviewable `seed.sql`. Tests build `vref.db` from the seed at runtime under
`tmp_path`, so no binary database blob is committed.

One pre-existing pyright annotation issue in `tests/unit/test_csv_suite.py` was
fixed after the move: `_build_vds_engine_code_index` returns two dict indexes,
not one dict. This is a test-only type correction.

## VERIFICATION GATE

- Environment:
  `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Red test:
  `python -m pytest tests/unit -q --tb=short -k "horizon or stress_rpm or switches or decode_isolation"`
  failed with missing fixtures `mini_data_dir`, `make_stress_profile`, and
  `make_switch_profile`.
- Ruff:
  `ruff check vinlab/ tests/` passed: `All checks passed!`.
- Pyright:
  `pyright vinlab/ tests/` passed: `0 errors, 0 warnings, 0 informations`.
- Focused overlay isolation:
  `python -m pytest tests/unit -q --tb=short -k "horizon or stress_rpm or switches"`
  passed: `30 passed, 158 deselected`.
- Focused decode isolation:
  `python -m pytest tests/unit/test_decode_isolation.py -q --tb=short`
  passed: `3 passed`.
- Full VINLab tests:
  `python -m pytest tests/ -q --tb=short` passed:
  `177 passed, 11 skipped`.
- Corpus-independent unit subset:
  `python -m pytest tests/unit -q --tb=short -k "not (csv or specimen or integration)"`
  passed: `172 passed, 8 skipped, 8 deselected`.
- Anti-orphan helper check:
  `rg -n "mini_data_dir|make_mini_data_dir|make_stress_profile|make_switch_profile|D4F|VF1CB05CF25935016" tests`
  showed each new builder and mini fixture row consumed by named tests.
- Mini fixture binary check:
  `tests/fixtures/mini_data/` contains `README.md`, `seed.sql`,
  `vds_engine_map.csv`, `wmi.csv`, and `years.csv`; no `vref.db` binary.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed new isolated tests pass data through existing path seams only; no
  production dependency-injection seam was added.
- Confirmed `test_decode_isolation.py` decodes through the mini data dir and
  exercises `tecdoc_query.lookup_engine_ref` via generated SQLite.
- Confirmed `test_horizon.py`, `test_stress_rpm.py`, and `test_switches.py`
  directly cover the previously missing overlay modules.
- Confirmed corpus-dependent tests retain their skip guards and are no longer
  the only way to exercise the target modules.
- Confirmed fixture builders are consumed in the same diff.
- Confirmed no production files, `graph/`, or `.sandbox-py/` files were touched.
