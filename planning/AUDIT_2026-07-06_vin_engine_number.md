# AUDIT — VIN → engine-number accuracy (follow-up to VIN_engine_number_test_report.md)

**Authored:** 2026-07-06 (architect, Cowork).
**Trigger:** `labs/vinlab/VIN_engine_number_test_report.md` (2026-07-06): exact+near
match only **14.5 %** on 200 held-out petrol VINs.
**Scope:** `vds_engine_map.csv` content + its builder, the `_resolve_engine` join,
and the report's own conclusion.

---

## 1. Headline: the report's "structural limit" conclusion is wrong

The report claims VDS granularity (`vin[3:8]` → one code per brand) caps accuracy
and that fixing map corruption "cannot overcome the structural limit." Measured
against the same data, that is false:

| Experiment (this audit, in-sandbox) | Resolved | Exact match |
|---|---|---|
| Shipped map, report's sample (N=200, seed 42) | 47.5 % | 8.0 % |
| Majority-vote map, train = `docs/Nio_vozila_1+2.csv`, test = **all 167,778** petrol rows of `Nio_vozila_3.csv` (held-out) | **99.3 %** | **78.2 %** |
| Same, upper bound if trained on file 3 itself | — | 79.5 % |
| 6-char key `vin[3:9]` instead of 5-char | — | 81.2 % (marginal gain) |

So ~78 % exact is reachable **with the existing 5-char VDS design** and data already
in the repo. The structural ceiling is real but sits near 80 %, not 15 %.

## 2. Why the shipped map scores 8 %

1. **Wrong/stale source.** `tools/build_vds_map.py` builds from
   `$VEHICLE_DATA_ROOT/petrol_vin/vehicles_petrol_specimens.csv` — a host-only file
   (`C:\Users\muto\...`), **not in the repo**. The shipped map has 5,807 rows vs
   8,163 brand+VDS groups in `Nio_vozila_3` alone → the 52.5 % no-resolution rate.
2. **Last-row-wins collapse.** `_pass_b_petrol_csv` does `brand_vds[key] = {...}` —
   the *last* CSV row silently overwrites, so multi-engine VDS groups (1,700 of
   8,163 in file 3) get an arbitrary code, not the majority one. This produces the
   report's "resolved but wrong" bucket (Z12XE→Z21XEP etc.).
3. **Corrupted codes in the map.** 203 rows carry junk prefixes
   (`TIP`/`TRI`/`TUP`/`UNK-`, decypher-era enrichment artifacts); 16 rows are
   mojibake (`�AWY`). Mojibake origin: `tools/extract_opsi_engine_codes.py:97`
   reads with `errors="replace"`. These rows also **kill the vref.db equipment
   join** (exact `engine_code = ?` in `vinlab/db/tecdoc_query.py`): only 20/3,343
   map codes match `engine_ref`; +5 recover with normalize+junk-strip.
4. **No normalization at compare/join.** `188A5000` vs `TIP188A4000`, `K4M G8`
   spacing, dots — all compared raw.

## 3. The "offset database columns" recollection

Checked: the 2026-06-21 audit contains **no offset-columns finding** — its defects
were D1 blank brands, D2 brand-string/encoding mismatch, D3 vref coverage 0.6 %,
D4 missing VDS rows. Closest real artifacts to the recollection:

- **Builder schema drift** — `build_vds_map.py` `FIELD_NAMES` emits **7 columns**,
  but the shipped CSV has **8** (`engine_configuration` added later by hand/enrichment).
  A naive rebuild silently drops that column. Must be fixed before any rebuild.
- **D2 encoding mismatch + mojibake** (§2.3 above).

No evidence of misaligned/shifted columns in `vref.db` (schema inspected, sane) or
in the map rows sampled.

## 4. Residue from prior fixes (noted, not re-tasked)

- `wmi.csv` still has **313 blank-brand rows** (D1 was 324; T-VIN-FIX-1 tracked).
- `vref.db` has 69 `engine_ref` rows (all with induction) — D3 work is
  `T-VIN-FIX-2`, unchanged by this audit; a rebuilt map with clean codes raises its
  join hit-rate for free.

## 5. Actions

Task pack (progressive disclosure — run 1, read numbers, then decide on 2):

1. `labs/vinlab/tasks/T-VIN-ENG-1_engine_map_rebuild.md` — rebuild the map from
   in-repo Nio files with majority vote + clean codes; held-out eval. **Discloses**
   real per-brand accuracy, ambiguity counts, vref join coverage.
2. `labs/vinlab/tasks/T-VIN-ENG-2_normalized_join_ambiguity.md` — normalized vref
   join + ambiguity confidence flag. **Gated** behind ENG-1's numbers.

---

## 6. Addendum (2026-07-06, later): status of the 2026-06-21 audit's sibling cases

Verified against live decoder + file-3 traffic (167,804 petrol rows):

| Case (from D1/D2 lists) | Status | Evidence |
|---|---|---|
| VF7 Citroën (presentation) | **fixed** | decodes HIGH, engine `5FR` |
| Mercedes-Benz (D2) | **fixed** | `WDD2452321J708365` joins via folded brand → `266920` |
| Škoda TMB (D1) | **still broken** | `wmi.csv` brand blank **and** map brand is mojibake `�KODA` — both sides dead; 6,239 rows in file 3 |
| Dacia UU1 (D1) | **still broken** | blank brand; map `DACIA` rows exist but unreachable; 1,795 rows |
| Blank-brand WMIs overall | **11.6 % of petrol traffic** (TMB, VSS, TSM, UU1, TMA, NLH top) |
| WMIs absent from `wmi.csv` | 1.1 % of traffic |

**Consequence for §1:** the 78.2 % held-out figure assumed brand known from the Nio
row itself; at runtime the decoder gets brand from `wmi.csv`, so ~12.7 % of traffic
can't even form a lookup key today. T-VIN-ENG-1 amended (new step 3): backfill blank
`wmi.csv` brands + missing WMIs by majority `D1-Znamka` from the train files;
success criteria now include blank-brand traffic < 1 % and Škoda/Dacia regression
VINs. Map-side `�KODA` rows regenerate cleanly as part of the rebuild.
