# T-VIN-FIX-2 — `vref.db` engine-equipment coverage (induction / Euro / O₂ / CoC)

**Authored:** 2026-06-21 (architect, Cowork).
**Source:** `planning/AUDIT_2026-06-21_vin_engine_resolution.md` §5 (D3).
**Type:** data sourcing into `vref.db`. No code change required (the read path
`_apply_vref_techmask` already consumes these columns).
**Depends on:** `T-VIN-FIX-1` (a VIN must first reach STEP 2 before STEP 3 matters).

### Goal ###

Stop the decoder from **guessing engine equipment.** `vds_engine_map.csv` supplies
only dimensions (displacement, cylinders, config, fuel). The equipment — **induction
type, Euro class, O₂ sensor type, CoC chemistry targets** — lives only in `vref.db`.
When an engine code is absent there, the decoder falls back to hard defaults
(`induction = NATURALLY_ASPIRATED`, `euro = EURO_1`), which is **why the presentation
vehicle's turbo engine reports as naturally-aspirated.** Today `vref.db` covers
**19 of 3,343 engine codes (0.6 %)**; the other 99.4 % decode at `PARTIAL` confidence
with defaulted, untrustworthy equipment.

Proven done when `5FR` (and the next priority tranche) resolve from `vref.db` with
authoritative equipment, lifting the presentation VIN `VF7SA5FR8AW511081` to `HIGH`
confidence with the **correct induction flag (turbo)**.

### Named signal/noise consumer ###

`vref.db.engine_ref` columns are consumed by
`decoder.py::_apply_vref_techmask` → `VinDNA.induction_type`,
`euro_emission_category`, `emissions.upstream_o2_type`, `target_lambda_v112`,
`co_low_idle`, `co_high_idle`, etc. Those `VinDNA` fields are in turn consumed
downstream by GASLab (CoC bounds) and OBDLab (O₂/air-metering) via the wiredV2
composition layer — so equipment accuracy here propagates into every diagnostic
verdict. No new column unless a consumer needs it.

### What to do ###

1. **Seed `5FR` first** (Citroën/PSA **EP6CDT, 1.6 THP turbo, GDI** — owner-confirmed
   forced induction; this is the presentation engine). Populate `engine_ref` row:
   `displacement_cc=1600`, `euro_norm` (MY2010 ≈ EURO_5 — confirm against
   type-approval), `has_turbo=1`, `has_gdi=1`, `induction_type=TURBOCHARGED`,
   `fuel_delivery_type=DIRECT_INJECTION`, `o2_type`, and CoC targets
   (`target_lambda_v112`, `co_low_idle`, `co_high_idle`). Cite each value's source.
   (Depends on `T-VIN-FIX-1` adding the `CITROEN_SA5FR → 5FR` map row first.)

2. **Prioritise by VIN traffic, not alphabetically.** Do **not** attempt all 3,324
   missing codes at once. Rank the missing engine codes by how many `vds_engine_map`
   rows / real WMIs reference them, and fill the top tranche (propose a batch size
   with the manager). Every numeric literal carries a source citation per repo rule.

3. **Each filled engine must carry an authoritative `induction_type`** — this is the
   field the audit flagged. No engine may inherit the NA default once it has a
   `vref.db` row.

### Success criteria ###

- `decode_vin_payload("VF7SA5FR8AW511081")` → `confidence = HIGH`,
  `induction_type = TURBOCHARGED`, `fuel_delivery_type = DIRECT_INJECTION`, `euro`
  from the engine's real class — **not** the `EURO_1` default.
- For the seeded tranche, no decode returns the NA/EURO_1 fallback when the engine
  code is present in `vref.db`.
- Add a coverage test: assert the seeded codes are present in `vref.db` and that a
  representative VIN per code decodes to `HIGH` with non-default equipment.
- Existing vin tests stay green; inner loop clean (`ruff` / `pyright` / `pytest`).

### Files to touch ###

- `labs/vinlab/vinlab/data/vref.db` (MODIFY — insert engine_ref rows; via the
  project's existing seed/build path, not ad-hoc SQL if a builder exists)
- `labs/vinlab/tests/` (ADD — vref coverage + HIGH-confidence decode tests)
- A short provenance note for the inserted rows (sources per value)

### Out of scope ###

The brand-join layer (D1/D2) — that is `T-VIN-FIX-1`. Decoder logic changes (the read
path already handles populated rows). Bulk-filling all 3,324 codes in one pass.
GRAPH GUARDRAIL: never run `graphify`.

### Verification ###

```bash
cd C:\Workspace\labs\vinlab
python -c "import sqlite3; c=sqlite3.connect('vinlab/data/vref.db'); \
print('5FR present:', bool(c.execute(\"select 1 from engine_ref where engine_code='5FR'\").fetchone()))"
python -c "from pathlib import Path; from vinlab.decoder import RobustVINDecoder; \
d=RobustVINDecoder(Path('vinlab/data')); r=d.decode_vin_payload('VF7SA5FR8AW511081'); \
print(r.make, r.induction_type, r.fuel_delivery_type, r.euro_emission_category, r.confidence)"
# expect: CITROEN TURBOCHARGED DIRECT_INJECTION EURO_5 HIGH
pytest tests -x -q
```

### Progress hook ###

PROGRESS: `T-VIN-FIX-2` Status=done, Verification="5FR + priority tranche carry
authoritative equipment in vref.db; presentation VIN decodes HIGH with correct
turbo/GDI induction".
