# audit — Progress Ledger (app-scoped fix rows from `audit/FIX_PLAN.md`)

**Tasks dir:** `apps/wired/audit_tasks/` · **Mode:** STRICT · **ID prefix:** `T-AUD-` (ceiling 99)
**Scope:** the app-scoped rows of the 2026-10-17 audit (T-AUD-1a, T-AUD-1b, later T-AUD-10). Lab-scoped rows
(T-AUD-2, 3, 5, 8, 9) get packs in their lab's own `tasks/`. Source of every row: `audit/FIX_PLAN.md`.
**Branch rule:** one `fix/<ID>` branch per row, cut from `audit-r2`; never `main` (`main` redeploys Render).
**Last updated:** 2026-11-02 (Windows Cowork: rewritten to the loop column contract; T-AUD-1a re-authored).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-AUD-1a | `repo/apps/wired/audit_tasks/T-AUD-1a_app_usable(4).md` | pending | — | 2026-11-02 | 4/5 | P0 app usable; plan REQUIRED; 2 commits (Cowork 006/008) |
| T-AUD-1b | (not authored) | deferred | T-AUD-1a | 2026-11-02 | — | deploy manifests F-P5-1/2/4; shares labs/comlab/pyproject.toml |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `superseded`
**Score** (column 6, checked by `ops/gen_dispatch.py`): the routing score `N/5`, the same `N` as the file name's `(N)`.
**Runnability:** `pending` = runnable now (the spec exists and every Blocked-by is `done`); otherwise `deferred`.
