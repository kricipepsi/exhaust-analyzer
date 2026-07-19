### Goal ###
Restore the scoreboard's hash-lock (the guard that refuses to score if the corpus/oracle changed)
so it actively pins the **post-T-V3-2 corpus** instead of the stale pre-re-pin FL hashes. After
T-V3-2 re-pinned the oracle CSV (owner-signed-off Option B), the live corpus hash moved
(`a94a7731…` → `47182b3d…`), but the scoreboard's frozen constants (constant = a fixed value baked
into the code) still expect the old FL hash. So every v3 scoreboard run now refuses unless bypassed
with `--allow-new-yardstick NAME` — and that flag validates **nothing**, it just skips the refusal.
The frozen guard is effectively defeated for all v3 work. Rebind it to the V3 yardstick so routine
v3 runs pass with **no override**, and any *further* accidental corpus drift refuses again.

Done when the exact T-V3-D4 self-compare command runs **without** `--allow-new-yardstick` and
prints an empty `REGRESSIONS:` line — which unblocks T-V3-D4.

### Success criteria ###
- `score_v3_yardstick.py score` (no `--results`, no `--allow-new-yardstick`) runs against the live
  corpus and prints `Hash lock: ok` (not REFUSED, not OVERRIDDEN). The frozen single-verdict block
  is unchanged (family+state 133/294 = 45.24 %).
- The T-V3-D4 self-compare passes with **no override**:
  ```
  score_v3_yardstick.py diff \
    --before apps/wired/v7/runs/20260630_163900/results.json \
    --after  apps/wired/v7/runs/20260630_163900/results.json | grep -iE 'REGRESSIONS'
  ```
  → `REGRESSIONS: (empty)` and zero movement (newly_pass=0, newly_fail=0, unchanged=294).
- A regression test pins the active V3 hash tuple (tuple = the fixed group of csv/oracle/scorer
  hashes) so a future silent corpus edit fails CI: assert `check_hash_lock` PASSES on the current
  corpus with no override, and RAISES `YardstickRefusalError` on a mutated-corpus fixture with no
  override.
- Inner loop clean on the changed file(s): `py_compile`, `ruff`, `pyright`, `pytest -x -q`.

### Context ###
Unplanned follow-up discovered while verifying T-V3-D4 (per-case resolution harness). D4's code is
already implemented and green; it is blocked *only* because its spec's self-compare re-runs the
scoreboard without the bypass and hits this pre-existing refusal. Root cause is upstream of D4.

The intended design is already documented — the FL scoreboard README says:
"first create a new explicitly named yardstick report that freezes the changed corpus/oracle/scorer,
then rerun with the new yardstick name." T-V3-2 did the **report** half
(`v3/reports/V3_ORACLE_REPIN_2026-06-30.md` records the new hash `47182b3d…`) but the **code** half
never happened: the scoreboard never got a new active frozen tuple, so `--allow-new-yardstick` is
the only way through, and it pins nothing. This task does the code half.

Post-re-pin hashes (already verified against the live corpus — do not recompute-and-trust blindly,
but these are the expected values):
| Artefact | Value |
|---|---|
| Corpus CSV `apps/wired/v7/data/cases_petrol_v7.csv` | `47182b3d9c4d4cb9e08645746a07fbae0d09b5db3d913fe00e1567965dd86dc9` |
| Oracle subset | `192d7be1a339ce45afa7682d710ccfca7b1a0102bff447d037a63a64a73879f5` |
| Scorer `apps/wired/v7/run_suite.py` | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` (UNCHANGED — T-V3-2 was zero-engine) |

Also reconcile two stale artefacts left by the naming drift:
- `v3/reports/V3_YARDSTICK_2026-06-30.md` (T-V3-1) still records the **pre-re-pin** CSV hash
  `a94a7731…` in its "Frozen artefacts" table — now wrong. Update that table to the post-re-pin
  hashes above and cross-reference `V3_ORACLE_REPIN_2026-06-30.md` as the change-record.
- The scoreboard already defines `V3_YARDSTICK_NAME = "V3_YARDSTICK_2026-06-30"`. Make that the
  single canonical active yardstick name reported by the hash-lock. (T-V3-2's note used the label
  `V3_ORACLE_REPIN`; converge on one name — `V3_YARDSTICK_2026-06-30` — and note the alias.)

### Consumer (signal/noise) ###
- **Consumer:** every v3 scoreboard invocation and the v3 acceptance gate; directly unblocks T-V3-D4.
- **Code path:** `apps/wired/fl_tasks/score_v3_yardstick.py::check_hash_lock` — bind its `expected`
  tuple and `yardstick` name to the V3 values. Measurement-surface only; no engine/oracle/schema
  change. Keep the FL constants defined as the historical BEFORE (its frozen data lives in
  `runs/20260630_163900/results.json`), but the FL tuple is no longer the active gate.

### Deliverables ###
1. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY. Add V3 frozen hash constants; make
   `check_hash_lock` validate the live corpus against the V3 tuple and report yardstick
   `V3_YARDSTICK_2026-06-30`. Preserve `--allow-new-yardstick` as the escape hatch for the *next*
   intentional re-pin. Do not weaken the refusal for genuine drift.
2. `apps/wired/v7/tests/test_yardstick_rebind.py` — CREATE. Pins: PASS on current corpus with no
   override; RAISES on a mutated-corpus fixture with no override.
3. `v3/reports/V3_YARDSTICK_2026-06-30.md` — MODIFY. Correct the "Frozen artefacts" hash table to
   the post-re-pin values; cross-reference `V3_ORACLE_REPIN_2026-06-30.md`.
4. `apps/wired/fl_tasks/reports/FL_SCOREBOARD_README_2026-06-30.md` — MODIFY (optional but
   preferred). Note that the active v3 yardstick is `V3_YARDSTICK_2026-06-30` with the post-re-pin
   hashes; the FL table remains the frozen historical baseline.

### Files to touch ###
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY)
- `apps/wired/v7/tests/test_yardstick_rebind.py` (CREATE)
- `v3/reports/V3_YARDSTICK_2026-06-30.md` (MODIFY — hash table only)
- `apps/wired/fl_tasks/reports/FL_SCOREBOARD_README_2026-06-30.md` (MODIFY — note only)

### Out of scope ###
No engine/oracle/scorer edit — this rebinds the *guard*, it does not touch what is scored. Do NOT
edit `apps/wired/v7/data/cases_petrol_v7.csv` or `run_suite.py`. Do NOT overwrite or re-hash the
frozen `FL_YARDSTICK_2026-06-30` (leave its immutable historical hashes intact). Do NOT weaken or
delete the refusal path — genuine drift (a hash matching neither FL nor V3) must still refuse
without an override. No `Vault/` edits. GRAPH GUARDRAIL: no `graphify`/graph rebuild. No changes to
the `score`/`compare`/`diff` output formats. Surgical change only.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py
/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py
/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/v7/tests/test_yardstick_rebind.py
/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k yardstick_rebind
# Guard now passes with NO override:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score | grep -iE 'Hash lock'
# The exact T-V3-D4 self-compare — must pass with NO --allow-new-yardstick:
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after  apps/wired/v7/runs/20260630_163900/results.json | grep -iE 'REGRESSIONS'
```
All steps must pass; `Hash lock: ok` (no OVERRIDDEN); self-compare `REGRESSIONS: (empty)`.

### Progress hook ###
PROGRESS.md `T-V3-2R`: Status=done, Files changed=3-4, Verification="hash-lock rebound to
V3_YARDSTICK_2026-06-30 (csv 47182b3d/oracle 192d7be1/scorer unchanged); score + D4 self-compare
pass with no override; drift still refuses". Then flip `T-V3-D4` from blocked→done (its self-compare
now passes unmodified) and re-run its progress hook.
