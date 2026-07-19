# T-VIN-FIX-3 progress note

Status: done
Date: 2026-06-21

## Scope completed

- Consolidated the partial working-tree patch into one class-level
  `RobustVINDecoder._resolve_engine` implementation.
- Preserved exact-brand priority, then folded-brand fallback, for both the
  five-character VDS path and the position-8 path.
- Blank brands now append `wmi_brand_missing` once and return `None` without
  crashing or being converted into `engine_not_in_csv`.
- Made the `wmi.csv` `brand`, `country`, and `era_hint` loads safe when
  `csv.DictReader` supplies `None` for missing columns.
- Confirmed the production `YTD` row is the valid four-column
  `YTD,Toyota,CZECH REPUBLIC,modern` record.
- Added regressions for the presentation VIN, folded Mercedes join, blank-brand
  confidence, position-8 fallback, and short WMI rows missing one or all optional
  columns.

## Verification gate

- `python -c "import py_compile; py_compile.compile('vinlab/decoder.py', doraise=True); import vinlab"` — passed.
- `python -m ruff check vinlab tests` — passed.
- `python -m pyright vinlab` — 0 errors, 0 warnings.
- `python -m pytest tests -x -q` — 194 passed, 8 skipped.
- `VF7SA5FR8AW511081` — `CITROEN`, 1.598 L, 4 cylinders,
  `TURBOCHARGED`, `GDI`, `EURO_5`, `HIGH`.
- `1MB010010A1234567` — `Mercedes-Benz`, 1.8 L, 4 cylinders; resolved
  through the folded brand join.
- Blank-brand resolver call — `None`, `["wmi_brand_missing"]`, public
  confidence `PARTIAL`.
- Temporary malformed `wmi.csv` rows — decoder constructed; missing fields
  degraded to empty brand/country and `modern` era.

## Code review gate

- Exactly one `_resolve_engine` definition remains on `RobustVINDecoder`.
- Lookup order is Path A exact → Path A folded → Path B exact → Path B folded.
- The resolver result remains consumed by `decode_vin_payload` engine and
  `VinDNA` assembly paths.
- `wmi_brand_missing` remains consumed by `_compute_confidence`; no schema field
  or cross-lab import was added.
- No checksum logic, graph output, or unrelated data rows were changed for this
  task.
- `git diff --check` passed for the modified decoder and test files.

No `labs/vinlab/tasks/PROGRESS.md` ledger exists in this checkout, so there was no
ledger row to flip.
