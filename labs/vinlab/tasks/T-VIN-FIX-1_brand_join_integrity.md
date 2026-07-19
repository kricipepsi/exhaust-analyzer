# T-VIN-FIX-1 — Brand-join integrity (blank brands + brand-string match + VDS coverage + fail-loud)

**Authored:** 2026-06-21 (architect, Cowork).
**Source:** `planning/AUDIT_2026-06-21_vin_engine_resolution.md` §3 (D1), §4 (D2), §6 (D4).
**Type:** data fix (`wmi.csv`, `vds_engine_map.csv`) + small resolver change (`decoder.py`).
No schema change.

### Goal ###

Make VIN → engine resolution reach the engine data that already exists. Today a VIN
fails to resolve its engine when its manufacturer's brand is **blank** in `wmi.csv`
(D1), **spelled differently** than `vds_engine_map.csv` expects (D2), or when the
**specific VDS row is missing** from the map (D4). The lookup key is
`"{BRAND}_{VDS}"`; if the brand half is empty or non-matching, or no row exists for
that brand+VDS, the join silently misses and the decode returns `confidence = NONE`
with `cylinder_count = 0`.

Proven done when the presentation VIN **`VF7SA5FR8AW511081`** (Citroën, engine `5FR`)
and a Mercedes-Benz VIN both resolve their engine (displacement + cylinders
populated, confidence ≥ PARTIAL), and the empty-brand path no longer fails silently.

### Named signal/noise consumer ###

The brand value in `wmi.csv` is consumed by `decoder.py::_resolve_engine` to build
the `vds_full_index` / `vds_pos8_index` key. New confidence flag `wmi_brand_missing`
is consumed by `_compute_confidence` (and surfaces in `VinDNA.confidence`) so a
missing brand is **visible**, not silent. No new schema field on `VinDNA`.

### What to do ###

1. **Fill blank brand cells in `wmi.csv`** (D1 — 324 rows, 2.5 %). Prioritise the
   mainstream European set; **VF7 → CITROEN is the must-have for the presentation.**
   French blanks to resolve: `S24, VF7, VF8, VFA, VNV, VR1, VR3, VR7`. Also the
   German (17), Italian (17), Slovenian (27), UK (8) blanks. Use the brand spelling
   that **matches `vds_engine_map.csv`** (see step 2). Cite the WMI source for each
   filled value (ISO 3780 / SAE J853 / NHTSA vPIC) in the commit message or a
   sidecar note — do not invent assignments.

2. **Normalize the brand join on both sides** (D2). In `_resolve_engine` (and the
   index build in `__init__`), compare brands after folding **case + hyphen/space +
   diacritics** so `"MERCEDES-BENZ"` (wmi.csv) matches `"MERCEDES BENZ"`
   (vds_engine_map.csv) and `"Škoda"` matches `"SKODA"`. Keep the raw brand string
   for display; use the folded form only as the join key.

3. **Add the missing VDS row(s)** (D4). The presentation VIN's `CITROEN_SA5FR` row is
   absent from `vds_engine_map.csv` even though siblings `SA5FD/SA5FF/SA5FS` exist and
   the engine code `5FR` exists (under `PEUGEOT,WB5FR`). Add
   `CITROEN,SA5FR,,5FR,1.6,4,I4,DIRECT_INJECTION` (note: EP6CDT THP is **GDI**, not the
   `PORT_INJECTION` the existing `5FR` row carries — use GDI here and flag the Peugeot
   row for review). Spot-audit sibling VDS coverage for the same engine family while
   here; cite the VDS→engine source for each added row.

4. **Make the empty-brand path fail loud** (D1 hardening). When `brand` is empty,
   append a `wmi_brand_missing` confidence flag instead of silently returning `None`
   with no explanation. `_compute_confidence` should treat it like the other
   downgrade flags (→ at most PARTIAL), so a future blank can be spotted from the
   output rather than mistaken for an un-decodable VIN.

### Success criteria ###

- `decode_vin_payload("VF7SA5FR8AW511081")` → `make=CITROEN`, `engine=5FR`,
  `displacement=1.6`, `cylinder_count=4`, `confidence ≥ PARTIAL`.
- A Mercedes-Benz VIN whose VDS is in `vds_engine_map.csv` resolves its engine
  (displacement + cylinders populated) — no longer `NONE`.
- A VIN with a still-blank brand returns a result carrying the `wmi_brand_missing`
  flag (not a silent empty engine).
- Existing vin tests stay green (no regression to the 94 already-joinable brands);
  add tests for: VF7/SA5FR resolves, Mercedes resolves via normalized join,
  blank-brand flag is set.
- Inner loop clean in vinlab (`ruff` / `pyright` / `pytest -x -q`).

### Files to touch ###

- `labs/vinlab/vinlab/data/wmi.csv` (MODIFY — fill blank brand cells)
- `labs/vinlab/vinlab/data/vds_engine_map.csv` (MODIFY — add `CITROEN_SA5FR` row +
  any sibling gaps found)
- `labs/vinlab/vinlab/decoder.py` (MODIFY — brand-fold join key in `__init__` +
  `_resolve_engine`; add `wmi_brand_missing` flag; `_compute_confidence` handling)
- `labs/vinlab/tests/` (ADD — VF7/SA5FR, Mercedes-normalized, blank-brand-flag tests)

### Out of scope ###

`vref.db` equipment coverage / induction-type correctness — that is **T-VIN-FIX-2**
(D3). Do not change existing displacement/cylinder values in `vds_engine_map.csv`
(only ADD the missing rows). Do not touch the checksum logic or the two-path VDS
resolver structure. No "while I'm here" fixes. GRAPH GUARDRAIL: never run `graphify`.

### Verification ###

```bash
cd C:\Workspace\labs\vinlab
ruff check vinlab && pyright vinlab
pytest tests -x -q                      # existing suite stays green
# the money checks:
python -c "from pathlib import Path; from vinlab.decoder import RobustVINDecoder; \
d=RobustVINDecoder(Path('vinlab/data')); r=d.decode_vin_payload('VF7SA5FR8AW511081'); \
print(r.make, r.engine_displacement_liters, r.cylinder_count, r.confidence)"
# expect: CITROEN 1.6 4 PARTIAL (or HIGH once T-VIN-FIX-2 lands)
```

### Progress hook ###

PROGRESS: `T-VIN-FIX-1` Status=done, Verification="VF7/SA5FR + Mercedes resolve engine
via filled/normalized brand join + added CITROEN_SA5FR row; blank-brand now flagged
not silent".
