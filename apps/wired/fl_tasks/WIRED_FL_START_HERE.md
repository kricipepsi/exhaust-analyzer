# WIRED-FL — START HERE (failure-localization pack bootstrap)
Paste this as message 1 of a fresh coder session. This file is a **procedure**, not
documentation — execute it before any other output.

## What this pack is
Build the instrument that **pinpoints the exact failure point of every failing v7 case**
(pipeline stage + failure mode) and a **frozen before/after yardstick**, so the planned
**v3** engine rebuild is judged on *real* per-family / per-mode movement — not another
incomparable headline. **Read-only on the engine.** This pack measures and localizes; it
does not fix the engine.

## Boot (every session)
1. Read `apps/wired/fl_tasks/FL_PROGRESS.md` (ledger) — find the first `pending` row whose
   `Blocked by` are all `done`. That is your task. One task per session.
2. Read the named task spec `apps/wired/fl_tasks/T-FL-<n>_*.md` in full.
3. Read the load-bearing context, in order:
   - `apps/wired/v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md` (the proven mechanism).
   - `apps/wired/v7_tasks/reports/V7_ACCURACY_2026-06-30.md` (the run this pack dissects).
   - The driver/scorer `apps/wired/v7/run_suite.py` and corpus `apps/wired/v7/data/cases_petrol_v7.csv`.
   - The trace tooling `apps/wired/trace/` (+ `T-V7-6` for the prune/rank spans).
4. Load the skills the spec names (wired-python, wired-verification-loop, wired-code-review).
5. Post a one-paragraph scope confirmation (which task, what you will touch, what you will
   NOT touch) **before** any code.

## Hard rules (this pack)
- **No engine/oracle/lab/wiki edits.** If a finding implies a fix, it is logged for v3, not
  applied here. Touch only `fl_tasks/` and (where a spec says) additive read-only helpers
  under `apps/wired/v7/` or `apps/wired/trace/`.
- **No ARCHIVE imports, no `graphify`, no `Vault/`** (AGENTS canon).
- **Reuse, don't rebuild:** the v7 driver, corpus, oracle, and trace tooling are inputs.
- **Verified vs inferred:** every per-case attribution must cite the field/span it rests on.
  Mark anything not directly observed as inferred.
- Run/trace JSON stays untracked (git-excluded), like the v7 runs.

## Pack map
| Task | Does | Blocked by |
|---|---|---|
| T-FL-1 | honest current routing baseline + frozen v3 yardstick | — |
| T-FL-2 | capture per-case GASLab/OBDLab upstream states | — |
| T-FL-3 | classify each failing case → mode + stage of first divergence | T-V7-6, T-FL-2 |
| T-FL-4 | one-command v3 before/after scoreboard | T-FL-1, T-FL-3 |

## Definition of done (pack)
A coder building v3 can read **one report** that says, per failing case: expected vs
predicted, the upstream states, whether the correct rule was pruned or outranked (with the
deciding evidence/span), and the failure **mode** — plus per-family/per-mode totals. And a
**single command** that re-scores v3 against the frozen yardstick and prints the per-mode
delta. That is the whole point: v3 gets a target list and an honest scoreboard.
