# vina — Progress Ledger (VINLab audit fix rows: `audit/FIX_PLAN.md` T-AUD-9)

**Tasks dir:** `labs/vinlab/tasks/` · **Mode:** STRICT · **ID prefix:** `T-VINA-` (ceiling 99)
**Scope:** T-AUD-9 of the 2026-10-17 audit: F-C6-1…14 and F-D1-13 (`audit/reports/R1_C6_20261017.md`). The SymptomLab
findings F-C6-11…13 are in this pack too: they are T-AUD-9's, and one kind of work stays in one pack.
**Branch rule:** one `fix/<ID>` branch per row. T-VINA-1 is cut from `fix/T-AUD-7a`; each later row from the previous
accepted row. Never `main`. Ruling 2026-11-03 (Windows Cowork): base on the fix chain, not `main`, because T-AUD-1b
changed the vinlab and symptomlab dist names and `constraints.txt` (the venv matches the chain). Lost: merge
independence; the operator merges the chain in order anyway.
**Order (disclosure first):** the year decode feeds the era, the O₂ type and the scope, so it goes first. Rows 2 and 6
measure before they commit. Later rows stay `deferred` until their blockers are `done`.
**Last updated:** 2026-11-04 (Windows Cowork: T-VINA-10 authored).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

**Cap: 25 KB.**

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-VINA-1 | `repo/labs/vinlab/tasks/T-VINA-1_year_scope_gate(3).md` | done | — | 2026-11-03 | 3/5 | **ACCEPT 2026-11-03, score 95, t=11/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-1.md`.** F-C6-3 (cycle), F-C6-8: model year 1990-2010, `L` = 1990, B-K refused; UI placeholder in scope |
| T-VINA-2 | `repo/labs/vinlab/tasks/T-VINA-2_type_code_year(2).md` | done | — | 2026-11-04 | 2/5 | **ACCEPT 2026-11-04, score 94, t=12/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-2.md`.** F-C6-3 rest: WMIs whose position 10 is not a year (Mercedes `WDB`, `WDD`); measure first |
| T-VINA-3 | `repo/labs/vinlab/tasks/T-VINA-3_vref_year_window(2).md` | done | — | 2026-11-04 | 2/5 | **ACCEPT 2026-11-04, score 88, t=15/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-3.md`.** F-C6-4: vref.db row applied only inside its model-year window (F-C6-1, F-D1-13 moved to T-VINA-10) |
| T-VINA-4 | (not authored) | deferred | T-VINA-3 | — | — | F-C6-6: upstream O₂ type, no wideband by year alone |
| T-VINA-5 | `repo/labs/vinlab/tasks/T-VINA-5_wmi_brand_table(4).md` | done | — | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 91, t=25/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-5.md`.** F-C6-2: WMI brand table (WDB, KMH, JSA, JN1, SAX) and the engine-map keys; plan REQUIRED. `# source: wmi.csv rows WDB/KMH/JSA/JN1/SAX hand-fixed (T-VINA-5); vds_engine_map.csv wrong-brand rows re-keyed, 133 conflicts settled by the Nio 1+2 vote; build_wmi_map.py keeps the last of several vPIC makes per WMI (unfixed -> T-VINA-12)` |
| T-VINA-6 | `repo/labs/vinlab/tasks/T-VINA-6_h1_diesel_map_rows(2).md` | done | T-VINA-5 | 2026-11-07 | 2/5 | **ACCEPT 2026-11-07, score 96, t=2/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-6.md`.** F-C6-5: H1 on the shipped map: 84 rows of 27 TecDoc-diesel keys -> DIESEL (measured, recheck/T-VINA-6/); data + test, no decoder change |
| T-VINA-6b | (not authored) | deferred | T-VINA-6 | — | — | rest of F-C6-5: diesel codes TecDoc does not key (K9K A7, F9Q G7, D4EA-V, D4HE; Mazda WL variants 1WL/PWL to verify) and the electric brands LIVEWIRE/ZEEHO (225 rows); needs a source first |
| T-VINA-7 | (not authored) | deferred | T-VINA-1 | — | — | F-C6-7, F-C6-9, F-C6-10, F-C6-14: checksum by market, grade NONE, Path B docs, closed connections; waits for the operator's merge of the AUD chain (`decoder.py`, `VIN_VOCABULARY.md` are in it; Cowork 2026-11-07) |
| T-VINA-8 | `repo/labs/vinlab/tasks/T-VINA-8_symptomlab_contract_fixes(2).md` | done | — | 2026-11-03 | 2/5 | **ACCEPT 2026-11-03, score 93, t=14/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-8.md`.** F-C6-11, F-C6-12, F-C6-13: SymptomLab pair count 21, `load_state` required, typed tier error |
| T-VINA-9 | (not authored) | deferred | — | — | — | F-C6-3 rest: Renault VF1 position 10 (0-4 only on 103 real VINs) is it a year? Find a source first |
| T-VINA-10 | `repo/labs/vinlab/tasks/T-VINA-10_era_from_year_when_euro_unknown(4).md` | done | — | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 90, t=15/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-10.md`.** F-C6-1, F-D1-13: era from model year when euro unknown (416 real VINs LEGACY to ADAPTIVE); flag; cited wiki §10.8 |
| T-VINA-11 | (not authored) | superseded | T-VINA-5 | 2026-11-04 | — | 97 folded duplicate keys (93 MERCEDES BENZ/-BENZ), 48 differ; files 1+2 vote = today's pick, file-3 matches 623 = 623: no decode effect (recheck/T-VINA-11/vote.out) → T-VINA-11b |
| T-VINA-11b | (not authored) | deferred | T-VINA-12 | — | — | rest of T-VINA-11: one vds key with two WMI populations (12602); RGX weak keys (221RA 0.400, U6UA0 0.833). **Measured 2026-11-07 (Cowork, `C:/4DApp/recheck/T-VINA-11b/heldout.py`, held-out Nio file 3, petrol, map code = P15 code normalised):** share <0.50 411 keys, 39,867 VINs, match 0.336; 0.50-0.70 744 keys, 23,555 VINs, 0.537; 0.70-0.90 716 keys, 19,624 VINs, 0.764; >=0.90 5,976 keys, 114,560 VINs, 0.978. A weak key is wrong more often than right; the fix (no engine below a share floor, or a grade change) is a `decoder.py` ruling → waits for the operator's merge of the AUD chain (decoder.py is in it) |
| T-VINA-12 | `repo/labs/vinlab/tasks/T-VINA-12_wmi_make_by_registry(4).md` | done | — | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 90, t=48/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-12.md`.** F-R3-2: 11 car WMIs take the registry make (JTE/JTM Toyota, KNE Kia); file-3 engine join floors; tool picks by registry |
| T-VINA-13a | `repo/labs/vinlab/tasks/T-VINA-13a_tecdoc_1q2019_extract(4).md` | done | T-VINA-5 | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 89, t=18/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-13a.md`.** F-C6-1 (operator DB task): TecDoc 1Q2019 per-engine extract CSV for the engine map's codes, brand-agreeing tiers, coverage report; plan REQUIRED |
| T-VINA-13b | `repo/labs/vinlab/tasks/T-VINA-13b_vref_tecdoc_merge(5).md` | done | T-VINA-13a | 2026-11-04 | 5/5 | **ACCEPT 2026-11-04, score 92, t=45/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-13b.md`.** F-C6-1: merge the 13a extract into vref.db engine_ref (NULL where TecDoc is silent, collisions skipped, schema change); real-VIN reach measured; plan REQUIRED |
| T-VINA-13c | (not authored) | deleted | T-VINA-13b | 2026-11-04 | — | TecDoc 1Q2018 fallback: not material. Cowork measured (`C:/4DApp/recheck/scratch/vina13c_measure.py`, after 13b): of 550 real VINs without a vref row, 1Q2018 adds 1 brand-agreeing (28 other-brand); 94 are in the 13a extract but skipped by 13b (collisions, no my_start, G1/G2) → T-VINA-14 |
| T-VINA-14 | `repo/labs/vinlab/tasks/T-VINA-14_decoder_banks_induction_remerge(4).md` | done | — | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 93, t=11/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-14.md`.** decoder: map BOXER keeps 2 banks, stated induction beats the heuristic; merge coalesces 35 collisions, +40 rows (B8) |
| T-VINA-15 | `repo/labs/vinlab/tasks/T-VINA-15_zero_zero_sensors_unknown(2).md` | done | T-VINA-13b | 2026-11-04 | 2/5 | **ACCEPT 2026-11-04, score 92, t=9/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-15.md`.** 68 vref rows store has_maf 0/has_map 0 (13 real VINs MAP_ONLY, no sensor); decoder reads 0/0 as unknown |
| T-VINA-16 | `repo/labs/vinlab/tasks/T-VINA-16_engine_ref_cylinder_count(5).md` | done | — | 2026-11-05 | 5/5 | **ACCEPT 2026-11-05, score 95, t=34/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-16.md`.** engine_ref cylinder_count from TecDoc (1,225 backfilled + 34 new rows); decoder prefers it to the map; G2 (i) retired; table digest pinned (F-C6-1, F-R3-1) |
| T-VINA-17 | `repo/labs/vinlab/tasks/T-VINA-17_type_code_wmis_measured(2).md` | done | — | 2026-11-04 | 2/5 | **ACCEPT 2026-11-04, score 91, t=4/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-17.md`.** F-R3-3: add VSA, WDF, WMX, 4JG, VDB to the type-code set (registry-measured); WHE/WDA/WD3/WDZ out |
| T-VINA-18 | `repo/labs/vinlab/tasks/T-VINA-18_catalog_21_pairs_docs(1).md` | done | — | 2026-11-04 | 1/5 | **ACCEPT 2026-11-04, score 97, t=3/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-18.md`.** F-R3-4 (docs): live catalog-size statements say 21 (ADR-0006, DNALab DLD/HLD/PRD) |
| T-VINA-19 | `repo/labs/vinlab/tasks/T-VINA-19_registry_majority_filters(1).md` | done | T-VINA-12 | 2026-11-04 | 1/5 | **ACCEPT 2026-11-04, score 95, t=3/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-19.md`.** T-VINA-12 review: _registry_majority test lets a no-17-char-filter mutant pass (tie); skip U+FFFD brands |
| T-VINA-20 | (not authored) | deferred | T-VINA-16 | — | — | builder writes False for unstated has_maf/has_map (`tools/build_vref_db.py:660-661`, `:1030-1031`); the 68 vref.db 0/0 rows stay pinned by 13b tests; fix builder + repin on a rebuild (035); runs with the first row that needs a rebuild (Cowork 2026-11-05) |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `superseded`

## Unplanned follow-ups

**Cap: 8 KB.**

| ID | Discovered in | One-liner (≤ 120 chars) | Status |
|---|---|---|---|
| — | — | — | — |

## Architect-level out-of-band patches

**Cap: 5 KB.**

| Date | File | Patch (≤ 120 chars) | Reason (≤ 120 chars) |
|---|---|---|---|
| — | — | — | — |
