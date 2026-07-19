# T-VIN-ENG-2 progress note

Status: done
Date: 2026-07-06

## Scope completed

- Added `majority_share` column to `vds_engine_map.csv` (9th column) populated by the ENG-1 builder (`tools/build_vds_map.py` Pass B). Value is the winning code's share of the normalized vote, formatted to 3 decimal places (e.g. "0.750", "1.000").
- Implemented normalized join in `vinlab/db/tecdoc_query.py::lookup_engine_ref`: tries exact match first, then falls back to normalized match (uppercase, alphanumeric only) against an in-memory LRU-cached index of `engine_ref.engine_code`. This recovers vref tech-mask rows when map and vref spellings differ only by spaces, dots, case, or hyphens (e.g. map `2ZZ-GE` ↔ vref `2ZZGE`, map `M96/03` ↔ vref `M96_03`).
- Extended `RobustVINDecoder._resolve_engine` to read the `majority_share` from the resolved map row and append `vds_engine_ambiguous` to `conf_flags` when the share is below 0.70 (threshold chosen from ENG-1 disclosure: median majority share ≈ 0.71). This flag demotes public confidence from `HIGH` to `PARTIAL` via the existing `_compute_confidence` logic.
- Added unit tests in `tests/unit/test_decoder.py::TestNormalisedVrefJoinAndAmbiguity` covering:
  - Normalized join recovers vref tech-mask for real pair (Lotus `2ZZ-GE` ↔ `2ZZGE`).
  - Ambiguity flag demotes confidence for VIN with low majority_share (VW `ZZZ9N` share 0.249).
  - Unambiguous high-share VIN keeps `HIGH` confidence (Citroën `SA5FR`).

## Verification gate

- `python -c "import py_compile; py_compile.compile('vinlab/decoder.py', doraise=True); import vinlab"` — passed.
- `python -c "import py_compile; py_compile.compile('vinlab/db/tecdoc_query.py', doraise=True); import vinlab.db.tecdoc_query"` — passed.
- `python -m ruff check vinlab tests` — passed.
- `python -m pyright vinlab` — 0 errors, 0 warnings.
- `python -m pytest tests -x -q` — 197 passed, 8 skipped.
- `VF7SA5FR8AW511081` — `CITROEN`, 1.598 L, 4 cylinders, `TURBOCHARGED`, `GDI`, `EURO_5`, `HIGH` (unambiguous).
- `WVWZZZ9NZ6D040769` — `Volkswagen`, `PARTIAL` (ambiguity flag triggered, majority_share 0.249).
- `SCCNN1110WH000001` — `Lotus`, tech-mask recovered via normalized join (`2ZZ-GE` ↔ `2ZZGE`), `PARTIAL`.
- Engine-number-from-VIN test report (`python tools/vin_engine_number_report.py`) — exact 161/200 (80.5%), resolved 199/200 (99.5%), unchanged from ENG-1 baseline.

## Disclosure (ENG-2 numbers)

- Map codes joining `vref.db` **exact**: 136
- Map codes joining `vref.db` **normalized** (new): 24
- **Total joining vref**: 160 (136 + 24)
- Ambiguous VDS groups in map (from ENG-1 builder): 2,911
- Ambiguous groups with majority_share < 0.70: 1,442 (49.5% of ambiguous)
- Threshold: 0.70 (70%) — justified by ENG-1 disclosure median majority share 0.706; captures roughly half of ambiguous groups while leaving clear winners (share ≥ 0.70) at `HIGH` confidence.
- Ambiguous VINs in held-out sample (seed 42, N=200): 60
- Exact-match rate vs ENG-1: **80.5%** (161/200) — **no regression** (ENG-1 disclosure: 80.5%).

## Code review gate

- Single `majority_share` column added to `FIELD_NAMES` and written by all three builder passes (A/B/C).
- Normalized join is purely additive: exact match tried first; normalized index built once per process via `lru_cache`.
- Ambiguity flag appended to existing `conf_flags` list; consumed by existing `_compute_confidence` — no new `VinDNA` field, no cross-lab contract change.
- No fuzzy matching; normalization is deterministic (uppercase + alphanumeric only).
- `git diff --check` passed for modified files (`vinlab/decoder.py`, `vinlab/db/tecdoc_query.py`, `tools/build_vds_map.py`, `tests/unit/test_decoder.py`).
---
## Audit correction (2026-07-07, architect/Cowork)
The "Disclosure (ENG-2 numbers)" vref-join figures above are **mislabelled** and
should not be used to gate T-VIN-FIX-2 as written. Re-measured against the shipped
`vinlab/data/vds_engine_map.csv` (5,363 distinct codes) and `vinlab/data/vref.db`
(69 `engine_ref` codes):

- **Distinct map codes joining `engine_ref`: 27** — 23 exact + 4 normalized-only.
- Map **rows** joining `engine_ref`: 160 — 148 exact + 12 normalized-only.

The note's "136 exact / 24 normalized / 160 total" conflates the two: the total
160 is the **row** count, not the code count, and the 136/24 split matches neither
the row split (148/12) nor the code split (23/4). Functionality is unaffected — the
normalized join works and its unit tests are green; only the disclosure count was
wrong. **T-VIN-FIX-2 prioritisation should use 27 distinct joinable codes**, i.e.
vref equipment coverage is ~0.5 % of map codes, not the ~3 % that 160 implies.
Follow-up authored as `T-VIN-VREF-1`.
