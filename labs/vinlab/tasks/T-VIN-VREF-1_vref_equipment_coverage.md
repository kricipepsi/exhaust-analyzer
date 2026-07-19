# T-VIN-VREF-1 — Expand `vref.db` equipment coverage for top-traffic petrol codes
**Authored:** 2026-07-07 (architect, Cowork).
**Source:** T-VIN-ENG-1 disclosure §4 + T-VIN-ENG-2 audit correction (2026-07-07);
continues the sourced-tranche method established in `T-VIN-FIX-2`.
**Type:** data-sourcing + reproducible builder rows. Additions to
`tools/vref_manual_overrides.yaml` consumed by `tools/build_vref_db.py`; regenerated
`vinlab/data/vref.db`. **No decoder change. No `VinDNA` schema change.**
**Blocked by:** none (ENG-1 and ENG-2 are done and verified).

### Why this exists ###
After the ENG-1 map rebuild and the ENG-2 normalized join, only **27 of 5,363**
distinct map engine codes (~0.5 %) join `vref.db.engine_ref` — so >99 % of decoded
petrol VINs get no vref tech-mask (equipment output that feeds GasLab/OBDLab through
`VinDNA`). Engine-code recovery itself is already at its structural VDS ceiling
(80.5 % exact on held-out data); the remaining downstream lever is **equipment
coverage**, not code accuracy. The ENG-2 progress note reported this coverage as
"160" — that figure is the map-row count and was mislabelled; the correct distinct-code
figure is 27 (see the audit correction appended to `progress_notes/T-VIN-ENG-2.md`).

### Named signal/noise consumer ###
`engine_ref` rows are read by `vinlab/db/tecdoc_query.py::lookup_engine_ref` (now with
the ENG-2 normalized fallback) and surface as the tech-mask on `VinDNA`. Each new row
must carry the same confidence-critical fields FIX-2 sourced (displacement, induction,
fuel delivery, VVT, Euro class, MAP/MAF presence, upstream O2 type, rated RPM, idle
targets, CoC/type-approval CO/HC/NOx/CO2). Reference-count ranking prioritises **which**
codes to source; it is **not** evidence for the values — every field is sourced per code.

### What to do ###
1. **Source an initial tranche of the highest-traffic real automotive codes** not
   already joining vref. Current recomputed ranking (map-row references, codes already
   in vref excluded, against the shipped map):
   `EJ20` (49), `N55B30A` (45), `B48B20B` (41), `PE` (41), `D4F D7` (41),
   `HN05` (39), `G4FA` (37), `CBZ` (36), `B38A15A` (35). Do **at least the top 3**
   fully-sourced; leave the rest ranked for the next tranche (FIX-2 pattern: quality
   over quantity — a code with unsourced fields is not shipped).
2. **Quarantine non-engine / junk codes from the ranking before sourcing.** Several
   high-count entries are not usable automotive engine codes: bare `4`, `M`, `B`
   (single-char), and powersports codes `139QMB`, `BN139QMB`, `ROTAX 810` (scooter /
   kart — out of scope for the gaslab/obdlab automotive tech-mask). Record them as
   skipped-with-reason in the disclosure; do not invent equipment for them.
3. **Reproducible build path only.** Add rows via `tools/vref_manual_overrides.yaml`
   and the existing `_load_yaml_entries` / `INSERT_ROW` path in
   `tools/build_vref_db.py` (the mechanism FIX-2 established). Preserve all existing
   rows and their CoC enrichment. Archive the old `vref.db` (repo rule: archive,
   don't delete) e.g. `vinlab/data/ARCHIVE/vref_pre_VREF1.db`.
4. **Use lab wiki/docs before the open web**; cite a source URL per field, as FIX-2
   did. Contract enums are locked (`GDI` not `DIRECT_INJECTION`, etc.) — match the
   values the builder validates, not the raw spec sheet wording.

### Success criteria (loop until proven) ###
- At least the top-3 non-quarantined codes each have a complete, per-field-sourced
  `vref.db` row; `distinct map codes joining engine_ref` rises from 27 by the number
  of codes added (report the exact new total).
- A held-out petrol VIN whose VDS maps to a newly-sourced code now receives the vref
  tech-mask on its `VinDNA` (add one regression test with a real VIN per new code).
- `python -m pytest tests -q` green (currently 197 passed / 8 skipped); `ruff check`
  and `pyright` clean.
- `VF7SA5FR8AW511081` still resolves `5FR` with `HIGH` confidence (presentation guard).
- No decoder or `VinDNA` schema change; no fuzzy matching added.

### Disclosure (what the run must surface) ###
Per-code source table (one URL per confidence-critical field, FIX-2 format); codes
skipped-with-reason from step 2; before/after **distinct-code** join count against
`engine_ref` (start = 27); and the updated top-N ranking of still-missing codes to
seed the next tranche.
