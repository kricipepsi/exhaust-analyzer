# T-V3-D4 — progress note (per-case resolution harness)

**Task:** `T-V3-D4_per_case_resolution_harness.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Code:** `apps/wired/fl_tasks/score_v3_yardstick.py`
**Test:** `apps/wired/v7/tests/test_resolution_diff.py`

## Plan

Add the per-case v3 movement instrument to the existing scoreboard without changing `score` or `compare` output:
1. Add `diff --before <json> --after <json>` to compare stored result rows by `case_id`.
2. Classify each accuracy case on the v3 pass surface: `single_verdict OR top3_family`.
3. Emit `newly_pass`, `newly_fail`, `unchanged`, before→after failure-mode movement, per-family net movement, and an explicit `REGRESSIONS:` line.
4. Add executable coverage for a synthetic passing-before/failing-after regression and a clean no-regression comparison.

Result: implementation and synthetic tests are green. T-V3-2R rebound the active scoreboard hash-lock to `V3_YARDSTICK_2026-06-30`, so the exact self-compare command now passes without `--allow-new-yardstick`: `newly_pass=0`, `newly_fail=0`, `unchanged=294`, `REGRESSIONS: (empty)`.

## VERIFICATION GATE

```
VERIFICATION GATE — T-V3-D4
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_resolution_diff.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_resolution_diff.py` -> OK)
3. Types   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_resolution_diff.py` -> 0 errors; `cd apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright .` -> 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k resolution_diff` -> 2 passed, 25 deselected)
5. Contract: PASS  (after T-V3-2R, the exact task self-compare command without `--allow-new-yardstick` reports `newly_pass=0`, `newly_fail=0`, `unchanged=294`, `REGRESSIONS: (empty)`)
6. Orphan  : N-A  (measurement harness only; no new producer/consumer field mapping)
Result: CLEAN
```

## CODE REVIEW

```
CODE REVIEW — T-V3-D4
Scope         : PASS  (changed only the scoreboard diff surface and the focused regression-diff test; no engine/oracle/lab/Vault/graph edit)
Composition   : PASS  (measurement-only `fl_tasks` harness; no lab edits, no cross-lab imports added, no deferred fusion path)
Consumers     : PASS  (N/A for mapped fields; consumer is the v3 acceptance gate / owner per-fix sign-off named by the task)
Literals      : PASS  (no new diagnostic thresholds or boundary numerics; output counts derive from compared inputs)
Docstrings    : PASS  (new public helpers and command function documented)
Craft (WARN)  : depth: diff logic is isolated in small helpers; deletion: optional artifact writers are tied to the `.md`/`.json` deliverable; seam: no routing/scoring mutation outside the scoreboard; interface: tests exercise the public diff helper/render contract rather than private internals of engine code
Result: CLEAN
```
