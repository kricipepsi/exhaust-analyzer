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
| T-VINA-5 | `repo/labs/vinlab/tasks/T-VINA-5_wmi_brand_table(4).md` | pending | — | 2026-11-04 | 4/5 | F-C6-2: WMI brand table (WDB, KMH, JSA, JN1, SAX) and the engine-map keys; plan REQUIRED |
| T-VINA-6 | (not authored) | deferred | T-VINA-5 | — | — | F-C6-5: petrol guard on real data (diesel and electric engines); measure first; also run H1 before the T-VINA-3 window drop |
| T-VINA-7 | (not authored) | deferred | T-VINA-1 | — | — | F-C6-7, F-C6-9, F-C6-10, F-C6-14: checksum by market, grade NONE, Path B docs, closed connections |
| T-VINA-8 | `repo/labs/vinlab/tasks/T-VINA-8_symptomlab_contract_fixes(2).md` | done | — | 2026-11-03 | 2/5 | **ACCEPT 2026-11-03, score 93, t=14/1 — `repo/labs/vinlab/tasks/reviews/REVIEW_T-VINA-8.md`.** F-C6-11, F-C6-12, F-C6-13: SymptomLab pair count 21, `load_state` required, typed tier error |
| T-VINA-9 | (not authored) | deferred | — | — | — | F-C6-3 rest: Renault VF1 position 10 (0-4 only on 103 real VINs) is it a year? Find a source first |
| T-VINA-10 | (not authored) | deferred | T-VINA-3 | — | — | F-C6-1, F-D1-13: era from year when euro unknown (36 corpus runs change); cited era thresholds; plan |
| T-VINA-11 | (not authored) | deferred | T-VINA-5 | — | — | vds map: same-brand spelling rows that disagree; one key, two WMI populations (12602); measure first |

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
