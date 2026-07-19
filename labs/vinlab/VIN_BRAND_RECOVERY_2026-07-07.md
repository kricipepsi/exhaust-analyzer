# VIN brand-join recovery — T-SHIP-3 report
**Date:** 2026-07-07 · **Runner:** Cowork architect (owner-authorized impl) · **Pack:** ship

## 1. Audit-figure correction (good news first)
The ship audit carried the 2026-07-06 figure "blank-brand WMIs = 11.6% of petrol traffic".
**Measured today on all 170,185 petrol rows of `docs/Nio_vozila_3.csv`: blank-brand = 4 rows
(0.00%), absent-WMI = 37 rows (0.02%).** The blank-brand backfill had already landed via the
T-VIN-FIX-1/ENG-1 line; the audit figure was stale. B-4 as stated is CLOSED by measurement.

## 2. The real residue: corrupted brand spellings (fixed)
What actually remained was a dead **fold-join** (spelling-normalizing lookup) for two brands:
- `wmi.csv`: TMB/TNB brand stored as `\x8aKODA` (latin-1 misdecode of cp1250 `Š`) — displays
  as "KODA"; folds to `KODA` ≠ map `SKODA` → **every Škoda petrol VIN decoded with make
  "KODA", confidence NONE, engine unresolved**.
- `vds_engine_map.csv`: 445 `\x8aKODA` rows + 30 `�KODA` (U+FFFD) rows + 1 `CITRO�N` row —
  unreachable from any correctly-spelled brand key.

**Fix:** `labs/vinlab/tools/repair_brand_spellings.py` — explicit spelling table applied after
stripping control/replacement chars (no guessing); duplicate brand+vds keys after rename
deduped preferring rows with ENG-1 `majority_share` provenance (28 dropped). Idempotent
(second run: 0/0/0). Repaired: wmi.csv 2 rows; map 476 rows.

## 3. Held-out verification (file 3, seed 42)
| Sample | Before | After |
|---|---|---|
| TMB (Škoda), 200 VINs | make "KODA", conf NONE, engine 0% | make SKODA; conf > NONE **198/200**; engine resolved **128/200** |
| VF7 (Citroën), 100 VINs | (control — already working) | conf > NONE 99/100; engine resolved 96/100 |
| Blank-brand share (all petrol) | 4/170,185 = 0.00% | unchanged (not the defect) |

## 4. Tests
`labs/vinlab/tests/unit/test_decoder.py::TestBrandSpellingRepair` (3 tests): no corrupt brand
cell in either CSV; TMB/TNB → SKODA; real-shape TMB VIN decodes make SKODA.
Full vinlab suite: **203 passed, 8 skipped**; ruff clean.

## 5. Left open (registered, not blocking)
- 245 blank-brand `wmi.csv` rows remain but carry ≈0% file-3 traffic — leave (majority-vote
  backfill would be guessing on no evidence).
- TMB engine resolution 64% reflects the ENG-1 map's per-VDS coverage, not the brand join —
  the ~78% structural ceiling from `planning/AUDIT_2026-07-06_vin_engine_number.md` §1 applies.
