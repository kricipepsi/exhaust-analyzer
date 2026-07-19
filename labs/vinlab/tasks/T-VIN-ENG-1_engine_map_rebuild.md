# T-VIN-ENG-1 — Rebuild `vds_engine_map.csv` from in-repo Nio data (majority vote, clean codes)

**Authored:** 2026-07-06 (architect, Cowork).
**Source:** `planning/AUDIT_2026-07-06_vin_engine_number.md` §2; test report
`VIN_engine_number_test_report.md`.
**Type:** builder fix + data rebuild. One schema-preserving change to
`tools/build_vds_map.py` (or a sibling builder), regenerated
`vinlab/data/vds_engine_map.csv`. **No decoder change. No `VinDNA` schema change.**
**Blocks:** T-VIN-ENG-2.

### Why this exists ###
The shipped map scores **8 % exact** engine-code recovery on held-out petrol VINs.
Audit proved **78.2 % exact / 99.3 % resolved** is reachable with the same 5-char
VDS design by (a) building from the in-repo Nio CSVs instead of the host-only
specimens file, (b) majority vote instead of last-row-wins, (c) normalized, junk-free
codes. The claimed "structural VDS limit" is ~80 %, not 15 %.

### Named signal/noise consumer ###
`vds_engine_map.csv` rows are consumed by `decoder.py::_resolve_engine` (keys) and
`_engine_attrs_from_csv` (columns `engine_displacement`, `cylinder_count`,
`engine_configuration`, `fuel_system_type`). `engine_code` is additionally the join
key into `vref.db.engine_ref` (`vinlab/db/tecdoc_query.py::lookup_engine_ref`), whose
equipment output feeds GasLab/OBDLab via VinDNA. **All 8 existing columns must
survive the rebuild** — note: the current builder's `FIELD_NAMES` lists only 7
(`engine_configuration` missing); fix that first or the column is silently dropped.

### What to do ###
1. **Fix builder schema drift.** `FIELD_NAMES` in `tools/build_vds_map.py` must
   match the shipped 8-column header exactly:
   `brand,vds_full,pos_8_only,engine_code,engine_displacement,cylinder_count,engine_configuration,fuel_system_type`.
2. **New Pass B source = in-repo Nio files.** Train on
   `/agent_workspace/docs/Nio_vozila_1.csv` + `Nio_vozila_2.csv` (`;`-delimited).
   Filter: `P13-Vrsta goriva (oznaka) == "P"`, 17-char `E-VIN`, non-empty
   `P15-Oznaka motorja` and `D1-Znamka`. **Never read `Nio_vozila_3.csv` during the
   build — it is the held-out eval set.**
3. **Backfill `wmi.csv` brands from the same train set (D1 residue).** 11.6 % of
   file-3 petrol traffic sits on WMIs whose `wmi.csv` brand is blank (TMB=Škoda
   6,239 rows, VSS=SEAT, TSM, UU1=Dacia, TMA, NLH…) and 1.1 % on WMIs absent from
   `wmi.csv` entirely. Without this step the map rebuild cannot reach its target —
   the decoder forms lookup keys from `wmi.csv`, not from Nio. Fill **blank** brands
   (and add missing WMIs) with the majority `D1-Znamka` per WMI from files 1+2;
   never overwrite a non-blank brand (spelling drift is handled by the existing
   folded fallback). Archive the old `wmi.csv` alongside the old map.
4. **Majority vote per (brand, vin[3:8]).** Normalize codes before counting:
   uppercase, strip all non-alphanumerics. Ties: higher raw count of the raw
   spelling, then lexicographic — deterministic either way. Store the most frequent
   *raw* spelling (normalized form only for counting), so vref join keys stay
   human-readable.
5. **No `errors="replace"` anywhere.** Read with the file's actual encoding
   (verify; expect UTF-8). A row that fails to decode is counted and reported, never
   emitted with `�`. Quarantine list (code starts with `TIP`/`TRI`/`TUP`/`UNK-` or
   contains `�`) applies to *carried-over* attribute joins too (step 5).
6. **Attribute columns.** `engine_displacement` = median `P11-Delovna prostornina`
   of the winning group ÷ 1000, 1 decimal. `cylinder_count` /
   `engine_configuration` / `fuel_system_type`: carry over from the *current* map by
   normalized `engine_code` match where available (the decypher enrichment is worth
   keeping); else leave blank — `overlay/cylinder_heuristic.py` covers gaps. Do not
   invent values.
7. **Keep Pass C (`pos_8_only` legacy rows) unchanged.**
8. Archive the old map (repo rule: archive, don't delete), e.g.
   `vinlab/data/ARCHIVE/vds_engine_map_pre_ENG1.csv`.

### Success criteria (loop until proven) ###
- `python3 tools/vin_engine_number_report.py` (petrol, seed 42, N=200, file 3):
  **exact ≥ 70 %**, resolved ≥ 95 % (audit measured 78.2 %/99.3 % full-population;
  a 200-sample run has noise — if below target, check the build, don't lower the bar).
- New map contains **zero** codes matching `^(TIP|TRI|TUP|UNK-)` or containing `�`.
- All 8 columns present; decoder constructs; existing `pytest` suite green.
- Blank-brand share of file-3 petrol traffic (by WMI lookup) drops from 11.6 % to < 1 %;
  `TMBDY16Y033784910` (Škoda, P15 `AZQ`) and `UU1B5220562764666` (Dacia, P15 `H4B B4`)
  both resolve an engine code.
- `VF7SA5FR8AW511081` still resolves `5FR` (presentation VIN regression guard).

### Disclosure (what the run must surface, not hide) ###
Append a results section to the test report (or a sibling `_ENG1.md`) with:
per-brand exact rates (top 15 brands by volume), count + share of ambiguous
groups (>1 distinct normalized code) and the majority share distribution,
quarantined/undecodable row counts, and **how many distinct map codes now join
`vref.db.engine_ref`** (feeds T-VIN-FIX-2 prioritisation). These numbers gate
T-VIN-ENG-2 — report them even where they look bad.
