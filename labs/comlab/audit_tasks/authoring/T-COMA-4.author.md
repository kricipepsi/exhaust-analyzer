# T-COMA-4 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: Linux Cowork `C:/Cowork/channel/050-cowork.md` §1 (optional row: the 4 dev-only test failures).
Rehearsal: `C:/4DApp/recheck/T-COMA-4/` (`apply_fix.py`, `rehearsal.patch`).

### Verified context ###
1. **Root cause:** both files set `WORKSPACE_ROOT = Path("/agent_workspace")` and import `fl_tasks` / `v7` from
   `apps/wired` below it; both packages exist in the repo (`apps/wired/fl_tasks/score_v3_yardstick.py`,
   `apps/wired/v7/load_corpus.py`). On this host: `ModuleNotFoundError` at collection. Observed.
2. **test_tracing:** `_install_in_memory_exporter` already calls `pytest.skip` when the SDK is absent; the SDK is
   installed here, so the Linux failure does not reproduce. Out of this row. Observed.
3. **Rehearsal** (restored): comlab `503 passed, 4 skipped, 2 errors` (flag) → `508 passed, 4 skipped` (no flag); the
   two files `5 passed`; ruff clean; 2 lines changed. Observed.
4. **Base:** the coma ledger is in the unmerged AUD chain, so the row stacks on `fix/T-AUD-18e` (Linux 050 accepted
   stacking 18d/18e on the chain). Observed.

### Rulings and the tradeoff that lost ###
- **R1 path from the file.** Lost: Linux's skip-when-absent option (the modules are not absent; a skip would hide 5
  real tests).
- Code (test) row: second-model review at acceptance. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `508 passed, 4 skipped` |
| step 2 | SIMULATED | `5 passed` |
| step 3 | SIMULATED | ruff clean; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-4: two COMLab tests resolve the repo root from their own path; the 2 collection errors become 5 passes.

### Cold read ###
own pass 2026-11-07: P1-P2 measured (fact 3) · `apply_fix.py` exits on any count other than 1 · traceability:
criteria 1-2 → steps 1-3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
