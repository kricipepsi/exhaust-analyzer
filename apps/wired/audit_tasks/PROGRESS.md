# audit — Progress Ledger (app-scoped fix rows from `audit/FIX_PLAN.md`)
**Pack goal:** land the app-scoped rows of the 2026-10-17 audit (T-AUD-1a, T-AUD-1b, later T-AUD-10). Lab-scoped rows
(T-AUD-2, 3, 5, 8, 9) get specs in their lab's own `tasks/`. Source of every row: `audit/FIX_PLAN.md`; evidence:
`audit/FINDINGS.md` + `audit/scratch/<target>/` probes (a finding's probe is its acceptance test).
**Tasks dir:** `apps/wired/audit_tasks/` · **Mode:** STRICT (dual-gate) · **Branch rule:** one `fix/<id>` branch per
row, cut from `audit-r2`; never `main` (`main` redeploys Render).
**Last updated:** 2026-11-02 (Windows builder: T-AUD-1a spec authored, awaiting architect review + Fork F-1 ruling).

Gate blocks go in `audit_tasks/progress_notes/<id>.md`.

## Task log
| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-AUD-1a | `T-AUD-1a_app_usable.md` | deferred | architect review of the spec + Fork F-1 ruling | 2026-11-02 | | | P0. Registry importable; no crash on blank/unticked input; field-level validation. |
| T-AUD-1b | (not authored) | deferred | T-AUD-1a (`labs/comlab/pyproject.toml` shared) | | | | Deploy manifests + constraints: F-P5-1, F-P5-2, F-P5-4. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `void`
**Runnability:** `pending` = runnable now (spec authored, reviewed, blockers `done`). Unreviewed or unauthored rows stay
`deferred`.
