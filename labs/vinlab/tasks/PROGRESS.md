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
**Last updated:** 2026-11-03 (Windows Cowork: pack opened, T-VINA-1 authored).

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
| T-VINA-6 | (not authored) | deferred | T-VINA-5 | — | — | F-C6-5: petrol guard on real data (diesel and electric engines); measure first; also run H1 before the T-VINA-3 window drop |
| T-VINA-7 | (not authored) | deferred | T-VINA-1 | — | — | F-C6-7, F-C6-9, F-C6-10, F-C6-14: checksum by market, grade NONE, Path B docs, closed connections |
| T-VINA-8 | `repo/labs/vinlab/tasks/T-VINA-8_symptomlab_contract_fixes(2).md` | done | — | 2026-11-03 | 2/5 | **ACCEPT 2026-11-03, score 93, t=14/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-8.md`.** F-C6-11, F-C6-12, F-C6-13: SymptomLab pair count 21, `load_state` required, typed tier error |
| T-VINA-9 | (not authored) | deferred | — | — | — | F-C6-3 rest: Renault VF1 position 10 (0-4 only on 103 real VINs) is it a year? Find a source first |
| T-VINA-10 | (not authored) | deferred | T-VINA-3 | — | — | F-C6-1, F-D1-13: era from year when euro unknown (36 corpus runs change); cited era thresholds; plan |
| T-VINA-11 | (not authored) | deferred | T-VINA-5 | — | — | vds map: same-brand spelling rows that disagree (123 folded duplicate keys, 119 `MERCEDES BENZ`/`MERCEDES-BENZ`, B7); one key, two WMI populations (12602); measure first |
| T-VINA-12 | (not authored) | deferred | T-VINA-5 | — | — | build_wmi_map.py: pick among vPIC makes by Nio D1-Znamka majority; 5NM; vPIC E:/agent_workspace/vpic |
| T-VINA-13a | `repo/labs/vinlab/tasks/T-VINA-13a_tecdoc_1q2019_extract(4).md` | done | T-VINA-5 | 2026-11-04 | 4/5 | **ACCEPT 2026-11-04, score 89, t=18/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-13a.md`.** F-C6-1 (operator DB task): TecDoc 1Q2019 per-engine extract CSV for the engine map's codes, brand-agreeing tiers, coverage report; plan REQUIRED |
| T-VINA-13b | `repo/labs/vinlab/tasks/T-VINA-13b_vref_tecdoc_merge(5).md` | pending | T-VINA-13a | 2026-11-04 | 5/5 | F-C6-1: merge the 13a extract into vref.db engine_ref (NULL where TecDoc is silent, collisions skipped, schema change); real-VIN reach measured; plan REQUIRED |
| T-VINA-13c | (not authored) | deferred | T-VINA-13b | — | — | TecDoc 1Q2018 (`DBS/tecdoc`) fallback, REA first, only if misses stay material |
| T-VINA-14 | (not authored) | deferred | T-VINA-13b | — | — | decoder: banks from a BOXER fact (not is_v_engine 0) and keep a vref-stated induction over the cylinder heuristic; then rerun the merge for the 41 guarded codes (B8) |
| T-VINA-15 | (not authored) | deferred | T-VINA-13b | — | — | the 13 shipped vref rows with has_maf 0 and has_map 0 decode with neither sensor (MAP_ONLY); measure and correct |

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
