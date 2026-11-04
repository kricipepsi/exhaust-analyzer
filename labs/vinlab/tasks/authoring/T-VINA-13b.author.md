# T-VINA-13b — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Decoder use of a vref row** (`vinlab/decoder.py::_apply_vref_techmask`, `_derive_air_metering`): displacement,
   induction, fuel, banks (`is_v_engine`), euro (`_normalise_euro`, NULL → EURO_1), O₂ hint (`"NB"` → NARROWBAND,
   `""` → year rule), `has_egr`, `has_maf`/`has_map` (non-NULL is a fact), CoC columns (NULL → `coc_null_*`).
   `era_bucket`, `has_vvt`, `has_gdi`, `has_turbo` have no decoder reader.
2. **Rebuild is not neutral** (P2): Cowork ran `build_vref_db.py` on a scratch copy without MySQL
   (`C:/4DApp/recheck/T-VINA-13b/rebuild/`): 72 rows, 68 equal, 4 differ (hand-edited CoC, rated_rpm).
3. **Measured** (P3, P4) on fix/T-VINA-13a `8592bb3` with `reach.py` and `vina13b_measure.py`.

### Rulings and the tradeoff that lost ###
- Merge into the shipped db. Lost: a builder that reads the extract (a rebuild changes 4 hand-edited rows).
- NULL `has_maf`/`has_map` and `''` O₂ on new rows, so a row adds only what TecDoc states. Lost: the schema as is
  (a `0` default asserts no MAF and no MAP: P3's 13 VINs).
- Collision codes skipped. Lost: 70 real VINs this row (lookup has no brand key).
- Difficulty 5, plan REQUIRED: a schema change, a binary data file and downstream effects across three suites.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `261 passed, 8 skipped` (T-VINA-13a review, 2026-11-04) |
| step 2 | DEFERRED | the test file does not exist |
| step 3 | RAN | `27 passed`, `41 passed`, `30 passed` (T-VINA-13a review) |
| step 4 | RAN | P3 on the base (Cowork, 2026-11-04) |
| step 5 | DEFERRED | the tool does not exist |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-13b: the TecDoc extract becomes vref.db rows (merge, NULL where TecDoc is silent); real-VIN reach measured.

### Cold read ###
own pass 2026-11-04: P1-P5 measured · traceability: criteria 1-4 → steps 1-5 · JUDGEMENT: 0.
cold read 2026-11-04: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
- **01 (2026-11-04, plan review; Plan: APPROVED with C1-C6).** Hand-back B8 (3 soft, COWORK). Second review (ds-pro):
  APPROVE WITH CORRECTIONS, 6 findings. Upheld F1 (migration guard, C1), F6 (era fixture, C5); F3 and F5 as fail-closed
  guards with 0 effect today (C3, C4). Not upheld: F2 (derived from stated induction/GDI: C2 clarifies R4), F4 (all
  readers by name). C6: CoC CSV is on D:, 0 codes enriched (Cowork). T-VINA-14, 15 registered. Record:
  `corrections/T-VINA-13b_plan_correction_20261104.md`.
