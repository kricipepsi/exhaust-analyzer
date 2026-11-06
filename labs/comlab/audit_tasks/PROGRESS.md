# coma — Progress Ledger (COMLab audit fix rows: `audit/FIX_PLAN.md` T-AUD-2, T-AUD-3)

**Tasks dir:** `labs/comlab/audit_tasks/` · **Mode:** STRICT · **ID prefix:** `T-COMA-` (ceiling 99)
**Scope:** T-AUD-2 (P1, COMLab REG-V2 verdict correctness: F-C1-1…4, 6…8, 10, 18…21; F-D2-1, 3, 4; F-D1-12) and T-AUD-3
(P2, COMLab output: F-C1-9, 11…16; F-C5-6; F-D2-6, 7, 14). Also takes the T-AUD-4e residual (gas readings optional for
a non-starter), which is the same fix as F-C1-7.
**Placement ruling 2026-11-05 (Windows Cowork):** a new folder, not `labs/comlab/tasks/`. That folder's ledger uses
6- and 8-column tables for the old T-COMV2/T-COMTST rows, and `gen_dispatch.py` checks 7 columns. Lost: one task
folder per lab (VINLab reused its own).
**Branch rule:** one `fix/<ID>` branch per row. T-COMA-1 is cut from `fix/T-AUD-11h` (`2e07e9c`); each later row from
the previous accepted row. Never `main`.
**Order:** F-C1-7 first (HIGH; a non-starter verdict is decided by gas readings a non-running engine cannot give).
**Last updated:** 2026-11-06 (Windows Cowork: T-COMA-1 authored; T-COMA-2/3 registered).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

**Cap: 25 KB.**

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-COMA-1 | `labs/comlab/audit_tasks/T-COMA-1_non_starter_family_gate(4).md` | done | — | 2026-11-06 | 4/5 | **ACCEPT 2026-11-06, score 98, t=14/1 — `repo/labs/comlab/audit_tasks/reviews/REVIEW_T-COMA-1.md`.** F-C1-7 (HIGH): non_starter family gate + NS-NO-RULE abstain; ruling B (sidecar); wiki 07 amended |
| T-COMA-2 | `labs/comlab/audit_tasks/T-COMA-2_non_starter_without_gas(3).md` | done | — | 2026-11-06 | 3/5 | **ACCEPT 2026-11-06, score 98, t=3/1 — `repo/labs/comlab/audit_tasks/reviews/REVIEW_T-COMA-2.md`.** T-AUD-4e residual: a non-starter is diagnosed without gas; schema keeps gas for running sessions |
| T-COMA-3 | (split: `authoring/T-COMA-3.design.md`) | done-superseded | — | 2026-11-06 | — | split into 3a (NS-005 P0335/P0336), 3b (GASLab cranking validity), 3c (REAL-002 label, channel question); OBD-only DTCs: no row |
| T-COMA-3a | `labs/comlab/audit_tasks/T-COMA-3a_crank_sync_no_start(2).md` | done | — | 2026-11-06 | 2/5 | **ACCEPT 2026-11-06, score 100, t=2/1 — `repo/labs/comlab/audit_tasks/reviews/REVIEW_T-COMA-3a.md`.** NS-005 crank-sync no-start (P0335/P0336); only case_040 moves (NS-NO-RULE -> NS-005) |
| T-COMA-3b | `labs/comlab/audit_tasks/T-COMA-3b_cranking_gas_sample(3).md` | done | — | 2026-11-06 | 3/5 | **ACCEPT 2026-11-06, score 99, t=2/1 — `repo/labs/comlab/audit_tasks/reviews/REVIEW_T-COMA-3b.md`.** GASLab CRANKING bucket for will_not_start (no triangle/dilution; RICH/LEAN_MISFIRE, INCOMPLETE_COMBUSTION); NS-004/005 outrank NS-001; corpus differ 5 |
| T-COMA-3c | `labs/comlab/audit_tasks/T-COMA-3c_real002_non_starter_label(1).md` | pending | T-COMA-3 | 2026-11-06 | 1/5 | REAL-002 lean_condition label on a will_not_start case vs T-COMA-1 ruling B; label owner's answer first |
