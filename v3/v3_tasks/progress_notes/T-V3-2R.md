# T-V3-2R — progress note (V3 yardstick hash-lock rebind)

**Task:** `T-V3-2R_v3_yardstick_hashlock_rebind.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Code:** `apps/wired/fl_tasks/score_v3_yardstick.py`
**Test:** `apps/wired/v7/tests/test_yardstick_rebind.py`

## Plan

Rebind the scoreboard's active hash-lock from the stale pre-repin FL tuple to the post-T-V3-2 V3 tuple without weakening drift refusal:
1. Preserve the FL hashes as historical BEFORE constants.
2. Add V3 active constants: CSV `47182b3d...`, oracle subset `192d7be1...`, scorer `dc47eb4...`.
3. Make `check_hash_lock()` validate against `V3_YARDSTICK_2026-06-30` by default and report `Hash lock: ok` on the live corpus.
4. Add regression tests proving the live corpus passes and a mutated corpus refuses without override.
5. Correct the V3 yardstick report and scoreboard README to distinguish active V3 hashes from historical FL hashes.

Result: active V3 hash-lock passes with no override, drift still refuses, and the exact T-V3-D4 self-compare is unblocked.

## VERIFICATION GATE

```
VERIFICATION GATE — T-V3-2R
1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py` -> OK)
3. Types   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py` -> 0 errors; `cd apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright .` -> 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k yardstick_rebind` -> 2 passed, 27 deselected; combined `yardstick_rebind or resolution_diff` -> 4 passed, 25 deselected)
5. Contract: PASS  (`score_v3_yardstick.py score | grep -iE 'Hash lock|family\+state'` -> `Hash lock: ok`, `family+state: 133/294 = 45.24 %`; exact D4 self-compare without override -> `newly_pass=0`, `newly_fail=0`, `unchanged=294`, `REGRESSIONS: (empty)`)
6. Orphan  : N-A  (measurement guard only; no new producer/consumer field mapping)
Result: CLEAN
```

## CODE REVIEW

```
CODE REVIEW — T-V3-2R
Scope         : PASS  (changed only the scoreboard guard constants/active yardstick, one focused test, and two contracted docs)
Composition   : PASS  (no lab edits, no engine/oracle/scorer edit, no graphify, no Vault edit, no deferred path)
Consumers     : PASS  (N/A for mapped fields; consumer is every v3 scoreboard invocation and the v3 acceptance gate)
Literals      : PASS  (hash literals are the task-pinned post-T-V3-2 tuple; no diagnostic thresholds added)
Docstrings    : PASS  (`check_hash_lock` docstring now names the active V3 yardstick; new tests document the guard behavior)
Craft (WARN)  : depth: one guard seam; deletion: no bypass or fallback path added; seam: FL constants remain historical while ACTIVE_* drives the guard; interface: tests exercise public `check_hash_lock()` behavior
Result: CLEAN
```
