# gasa — Progress Ledger (GASLab audit fix rows: `audit/FIX_PLAN.md` T-AUD-5)

**Tasks dir:** `labs/gaslab/audit_tasks/` · **Mode:** STRICT · **ID prefix:** `T-GASA-` (ceiling 99)
**Scope:** T-AUD-5 (P2, GASLab ontology and rules back to the wiki: F-C2-1…15; F-D2-22…24).
**Placement ruling 2026-11-13 (Windows Cowork):** a new folder, not `labs/gaslab/tasks/`, which holds older-format task
files. Same ruling as the coma pack. Lost: one task folder per lab.
**Branch rule:** one `fix/<ID>` branch per row. T-GASA-1 is cut from `fix/T-COMA-30` (`7034d64`); each later row from
the previous accepted row. Never `main`.
**Order:** the HIGH findings first (F-C2-1, 2, 5, 6), each measured on the v7 corpus before it is authored.
**Last updated:** 2026-11-13 (Windows Cowork: pack opened; T-GASA-1 inline, difficulty 1).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

**Cap: 25 KB.**

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-GASA-1 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | — | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 99, t=15/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-1.md`.** F-C2-1 (HIGH): low-triangle leak route needs CO + CO2 > 6 % (wiki §4.2); diluted sample is INVALID |
| T-GASA-2 | (inline, Cowork; difficulty 1, no task file: roster 2026-11-13) | done | T-GASA-1 | 2026-11-13 | 1/5 | **ACCEPT 2026-11-13, score 99, t=12/1 — `repo/labs/gaslab/audit_tasks/reviews/REVIEW_T-GASA-2.md`.** F-C2-2 (HIGH): collision rule keeps the triangle gate's validity; 2 pins re-stated; T-GASA-1 docstring nit |
