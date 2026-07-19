### Goal ###
Build the per-case verification instrument that proves each v3 fix resolved its target case
**without regressing a neighbour** (the per-case form of the audit's FT-8 guard). Extend the
scoreboard with a `diff` mode that compares a BEFORE result JSON and an AFTER result JSON and
emits, per case: `newly_pass` / `newly_fail` / `unchanged`, the before→after failure-mode change,
and a **REGRESSIONS** list (cases that passed before and fail after). Output a per-case movement
table (`.md` + `.json`). The acceptance rule for any v3 fix: the REGRESSIONS list is **empty**.

### Success criteria ###
- `apps/wired/fl_tasks/score_v3_yardstick.py diff --before <json> --after <json>` prints a per-case
  movement summary, the per-family net movement, and an explicit `REGRESSIONS:` line (empty or the
  offending case_ids). (The harness already exposes a `compare` subcommand for aggregate before/after
  — extend to true per-case granularity, do not duplicate it.)
- `test_resolution_diff.py::test_regression_detected`: a synthetic AFTER where one passing case
  flips to fail is reported in REGRESSIONS; a clean AFTER reports empty. Both pass.
- Running `diff` with the frozen run as both before and after reports zero movement and empty
  REGRESSIONS (self-compare sanity, mirroring the existing scoreboard self-compare).
- Inner loop clean (`py_compile`, `ruff`, `pyright`, `pytest -x -q` on the new test).

### Context ###
Phase verification for `v3/V3_PLAN.md` (sections 5-6; the FT-8 no-regressed-family rule, applied
per case). The scoreboard already loads the frozen yardstick, scores runs, and reports per-mode
buckets; it has `score` and `compare` subcommands
(`apps/wired/fl_tasks/score_v3_yardstick.py`; see `--before/--after` in its arg parser and the
self-compare-all-zero behaviour noted in `FL_SCOREBOARD_README_2026-06-30.md`). This task adds the
**per-case** diff that lets the owner confirm, case by case, that a fix (T-V3-2 re-pin, T-V3-3
differential, a future T-V3-4 rank change, a Phase-4 signal) moved exactly the intended cases and
broke none. Join on `case_id`; classify movement on the v3 metric set from T-V3-1
(`single_verdict` + `top3_family`), so a case "passing" is unambiguous.

### Consumer (signal/noise) ###
- **Consumer:** the v3 acceptance gate and the owner's per-fix sign-off.
- **Code path:** `apps/wired/fl_tasks/score_v3_yardstick.py::diff` prints it; `test_resolution_diff.py`
  is the executable contract. Measurement surface only — no engine/schema change.

### Deliverables ###
1. `apps/wired/fl_tasks/score_v3_yardstick.py` — MODIFY. Add the `diff` per-case subcommand.
2. `apps/wired/.../tests/test_resolution_diff.py` — CREATE.

### Files to touch ###
- `apps/wired/fl_tasks/score_v3_yardstick.py` (MODIFY)
- `apps/wired/.../tests/test_resolution_diff.py` (CREATE)

### Out of scope ###
No change to the existing `score`/`compare` subcommands' output. No engine/oracle edits. Do not
re-hash or mutate the frozen yardstick. GRAPH GUARDRAIL: no `graphify`/graph rebuild. No `Vault/`
edits. Surgical change only.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py
ruff check apps/wired/fl_tasks/score_v3_yardstick.py
/agent_workspace/.venv-wired/bin/python -m pytest -x -q apps/wired -k resolution_diff
# Self-compare sanity: same run before and after -> zero movement, empty REGRESSIONS
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after  apps/wired/v7/runs/20260630_163900/results.json | grep -iE 'REGRESSIONS'
```
All steps must pass; self-compare must report empty REGRESSIONS.

### Progress hook ###
PROGRESS.md `T-V3-D4`: Status=done, Files changed=2, Verification="per-case diff subcommand + REGRESSIONS guard; self-compare empty; synthetic regression detected"
