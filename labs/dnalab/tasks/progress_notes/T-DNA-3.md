# T-DNA-3 progress note

Status: done
Date: 2026-06-11

## Scope Confirm

Added `rated_rpm` to `VinDNA` as an optional integer sourced from
`DBS/docs/vehicles_petrol_specimens.csv` column `P14_rated_rpm`, keyed by
`P15_engine_code` through VINLab's existing vref baseline overlay. The bounded
field change is VINLab-only: `VinDNA.rated_rpm` serializes, deserializes, and is
populated when the decoded engine code has a baseline median; unresolved engine
paths leave it `None`. The named live signal/noise consumer is existing COMLab:
`labs/comlab/comlab/projection.py:89` reads `vin.get("rated_rpm")` into
`ObdLabDnaView.rated_rpm` for OBDLab's DNA-relative RPM ceiling. No COMLab code
or proposal was needed.

## Changed Files

- `labs/vinlab/vinlab/models.py`
- `labs/vinlab/vinlab/decoder.py`
- `labs/vinlab/tools/build_vref_db.py`
- `labs/vinlab/tests/test_models.py`
- `labs/vinlab/tests/fixtures/vindna_pre_refactor/*.json`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-3.md`

Local verification artifact:

- `labs/vinlab/vinlab/data/vref.db` was updated locally with a `rated_rpm`
  column and DBS-derived medians. It is ignored by `.gitignore` via `*.db`; the
  tracked reproducible change is `tools/build_vref_db.py`.

## Contract Amendment Draft For COMLab/Semantic Sign-Off

Draft addition to `SEMANTIC_CONTRACT.md` Section 4.1 `VinDNA` fields:

```yaml
rated_rpm:
  type: int | null
  source: DBS/docs/vehicles_petrol_specimens.csv P14_rated_rpm
  key: P15_engine_code
  semantics: Rated engine speed in RPM, emitted when the VIN-resolved engine
    code has a DBS median; null when no engine code or no median is available.
  consumer: COMLab projection.py -> ObdLabDnaView.rated_rpm -> OBDLab
    DNA-relative RPM ceiling.
```

Example JSON shape:

```json
{
  "vin": "WBA4W9C5ZLYYYYYYY",
  "rated_rpm": 5500
}
```

This is draft text only. The contract remains COMLab/semantic-owned and needs
sign-off before `SEMANTIC_CONTRACT.md` is edited.

## VERIFICATION GATE

- RED check before implementation:
  `.venv-wired\Scripts\python.exe -m pytest tests\test_models.py -x -q --tb=short`
  failed on `AttributeError: 'VinDNA' object has no attribute 'rated_rpm'`,
  proving the new tests caught the missing field.
- Targeted GREEN check:
  `.venv-wired\Scripts\python.exe -m pytest tests\test_models.py -x -q --tb=short`:
  passed, 15 tests.
- `.venv-wired\Scripts\python.exe -m ruff check vinlab tests tools\build_vref_db.py`:
  passed.
- `.venv-wired\Scripts\pyright.exe vinlab`: passed with 0 errors, 0 warnings,
  0 informations. Pyright also printed an update notice for 1.1.410.
- `.venv-wired\Scripts\python.exe -m pytest tests\ -x -q --tb=short`: passed,
  169 tests, 3 skipped.
- Build-script syntax check:
  `.venv-wired\Scripts\python.exe -m py_compile tools\build_vref_db.py`: passed.
- Local vref artifact check: `engine_ref` has 24 rows with non-null
  `rated_rpm`; `B58B30` resolves to `5500`.
- Producer check: `rg -n "rated_rpm" vinlab tests tools\build_vref_db.py`
  confirms the field is defined, deserialized, populated from `db_row`, covered
  by tests, and regenerated from DBS `P14_rated_rpm`.
- Consumer check: `rg -n "rated_rpm" labs/comlab/comlab/projection.py` confirms
  line 89 reads `vin.get("rated_rpm")`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `rated_rpm` stays optional and defaults to `None`; unresolved engine
  paths do not fabricate RPM data.
- Confirmed the populated path uses the existing vref baseline overlay, with
  `tools/build_vref_db.py` computing medians by exact `P15_engine_code`.
- Confirmed the live COMLab consumer already exists, so this is not an orphan
  field and no proposal entry is required.
- Confirmed snapshot fixtures were updated because `VinDNA.to_json()` now emits
  the new optional key.
- Confirmed no graph artifacts were modified and no graphify command was run.
