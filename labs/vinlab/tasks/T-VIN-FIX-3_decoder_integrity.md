# T-VIN-FIX-3 — Decoder integrity: complete & harden `decoder.py` (T-VIN-FIX-1 follow-up)

**Authored:** 2026-06-21 (architect, Cowork).
**Source:** verification of T-VIN-FIX-1 against VIN `VF7SA5FR8AW511081`.
**Type:** bugfix — the decoder does not currently import/decode. **Blocks** the oil-burn
presentation test run (no VIN can be decoded until this lands).

### Why this exists ###

T-VIN-FIX-1 shipped the data fixes (VF7→Citroën, `CITROEN_SA5FR` map row, `5FR` in
vref.db) but left `decoder.py` in a non-running state. Three concrete defects, found
while verifying the presentation VIN:

1. **Missing method.** `decode_vin_payload()` calls
   `self._resolve_engine(vin, brand, conf_flags)` (a method = a function attached to
   the decoder class), but **there is no `def _resolve_engine` on the class.** Any VIN
   that reaches engine resolution raises `AttributeError`. The brand-folding helper
   `_fold_brand()` and the four `vds_*_index` lookup tables it built in `__init__`
   exist — only the method that *uses* them to look up an engine is absent.

2. **Loader crashes on one malformed row.** `__init__` does
   `row.get("era_hint", "modern").strip()` while loading `wmi.csv`. A short/malformed
   row makes `csv.DictReader` return `None` for the missing field, so `.strip()` raises
   `AttributeError` and **the whole decoder fails to construct** — one bad row takes
   down every VIN. (Same brittleness on `brand` / `country`.)

3. **Corrupted data row.** `wmi.csv` line for `YTD` is `YTD,Toyota,CZEC` — truncated
   (3 columns, should be 4) and semantically wrong (Toyota WMIs are Japan / UK /
   Turkey, **not** Czech Republic). The committed value was
   `YTD,Toyota,CZECH REPUBLIC,modern`; the working-tree edit broke it.

> A candidate patch for (1) and (2) was sketched in the host working tree during
> verification (a `_resolve_engine` two-path method + None-safe `.get(...) or default`
> loader). **Do not assume it is correct or complete** — re-implement or validate it
> properly and run the gates; the sandbox could not execute it to confirm.

### Named signal/noise consumer ###

`_resolve_engine` output (the engine CSV row) is consumed by `decode_vin_payload`
steps 4–6 → `VinDNA` engine fields. The `wmi_brand_missing` confidence flag is
consumed by `_compute_confidence`. No new schema field.

### What to do ###

1. **Define `_resolve_engine(self, vin, brand, conf_flags) -> dict | None`.** Two-path
   lookup matching the indexes `__init__` already builds: Path A = 5-char VDS
   (`vin[3:8]`), Path B = position-8 (`vin[7]`). For each path try the **exact** brand
   key first (`vds_full_exact_index` / `vds_pos8_exact_index`), then the **folded**
   brand key (`vds_full_index` / `vds_pos8_index`, via `_fold_brand`) so
   `Mercedes-Benz` joins `MERCEDES BENZ`. Empty brand → append `wmi_brand_missing` and
   return `None` (fail loud, don't crash).

2. **Make the `wmi.csv` loader None-safe.** `(row.get("era_hint") or "modern").strip()`
   and the same pattern for `brand` / `country`, so a malformed row degrades that one
   row instead of killing the decoder. Optionally skip rows whose column count ≠ header
   and log them.

3. **Restore the `YTD` row** to a valid 4-column value. Minimal: revert to the
   committed `YTD,Toyota,CZECH REPUBLIC,modern`. Better: assign a correct Toyota market
   — but **do not hand-curate the whole table here**; the broader `wmi.csv` rebuild is
   tracked separately (see `planning/AUDIT_2026-06-21_vin_engine_resolution.md`).

### Success criteria ###

- `python -c "import vinlab"` succeeds; `py_compile` clean.
- `decode_vin_payload("VF7SA5FR8AW511081")` → `make=CITROEN`, engine `5FR`,
  `displacement=1.6`, `cylinder_count=4`, `induction=TURBOCHARGED`,
  `fuel=GDI`, `euro≈EURO_5`, `confidence=HIGH`.
- A constructed Mercedes-Benz VIN resolves its engine via the folded join (no `NONE`).
- A VIN whose brand is blank returns the `wmi_brand_missing` flag (not a crash, not a
  silent empty engine).
- A deliberately malformed `wmi.csv` row does not prevent the decoder from constructing.
- Existing vinlab tests green; inner loop clean (`ruff` / `pyright` / `pytest -x -q`).

### Files to touch ###

- `labs/vinlab/vinlab/decoder.py` (MODIFY — add `_resolve_engine`; None-safe loader)
- `labs/vinlab/vinlab/data/wmi.csv` (MODIFY — restore the single `YTD` row only)
- `labs/vinlab/tests/` (ADD — `_resolve_engine` happy/empty-brand/folded-join tests;
  malformed-row loader test)

### Out of scope ###

Full `wmi.csv` data-quality rebuild (separate effort). `vref.db` coverage beyond `5FR`
(that is T-VIN-FIX-2). No changes to checksum logic or the index-building structure in
`__init__` beyond None-safety. GRAPH GUARDRAIL: never run `graphify`.

### Verification ###

```powershell
cd C:\Workspace\labs\vinlab
python -c "import py_compile; py_compile.compile('vinlab/decoder.py', doraise=True); print('SYNTAX OK')"
python -c "from pathlib import Path; from vinlab.decoder import RobustVINDecoder; \
d=RobustVINDecoder(Path('vinlab/data')); r=d.decode_vin_payload('VF7SA5FR8AW511081'); \
print(r.make, r.engine_displacement_liters, r.cylinder_count, r.induction_type, r.fuel_delivery_type, r.euro_emission_category, r.confidence)"
# expect: CITROEN 1.6 4 TURBOCHARGED GDI EURO_5 HIGH
ruff check vinlab && pyright vinlab && pytest tests -x -q
```

### Progress hook ###

PROGRESS: `T-VIN-FIX-3` Status=done, Verification="decoder imports + decodes
VF7SA5FR8AW511081 to HIGH turbo/GDI; _resolve_engine restored; loader None-safe; YTD
row repaired".
