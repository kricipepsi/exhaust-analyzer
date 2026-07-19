# SHIP FINAL VERIFY — 2026-07-08

**Task:** T-SHIP-6 — final full-suite verification before GitHub push  
**Mode:** READ-ONLY disclose. No source, test, corpus, rule, yardstick, graph, or `Vault/` file was edited by this task.  
**Interpreter:** `/agent_workspace/.venv-wired/bin/python` from repo root.  
**Verdict:** PASS with one dirty-tree finding: `apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md` is untracked and outside the task file's expected dirty-set wording. All suites, guards, score lock, synthetic split, and UI smoke checks are green.

---

## 1. Suite table

Baseline = `apps/wired/ship_tasks/reports/SHIP_VERIFY_2026-07-07.md` §1, except `apps/ui/tests` is new in T-SHIP-6.

| Surface | Command | Baseline | Result | Delta | Status |
|---|---|---:|---:|---:|---|
| `labs/gaslab` | `.venv-wired/bin/python -m pytest -q labs/gaslab` | 208 passed / 2 skipped | 208 passed / 2 skipped / 4 deselected | no shrink | PASS |
| `labs/obdlab` | `.venv-wired/bin/python -m pytest -q labs/obdlab` | 388 passed / 2 skipped | 388 passed / 2 skipped | no shrink | PASS |
| `labs/dtclab` | `.venv-wired/bin/python -m pytest -q labs/dtclab` | 590 passed | 590 passed | no shrink | PASS |
| `labs/dnalab` | `.venv-wired/bin/python -m pytest -q labs/dnalab` | 27 passed | 27 passed | no shrink | PASS |
| `labs/vinlab` | `.venv-wired/bin/python -m pytest -q labs/vinlab` | 200 passed / 8 skipped | 203 passed / 8 skipped | +3 passed | PASS |
| `labs/comlab` | `.venv-wired/bin/python -m pytest -q labs/comlab` | 527 passed / 4 skipped | 1021 passed / 4 skipped | +494 passed | PASS |
| `labs/comlab/registry` | `.venv-wired/bin/python -m pytest -q labs/comlab/registry` | 494 passed | 494 passed | no shrink | PASS |
| `apps/wired/tests` | `.venv-wired/bin/python -m pytest -q apps/wired/tests` | 11 passed | 11 passed | no shrink | PASS |
| `apps/wired/v7/tests` | `.venv-wired/bin/python -m pytest -q apps/wired/v7/tests` | 48 passed | 49 passed | +1 passed | PASS |
| `apps/ui/tests` | `PYTHONPATH=apps/ui:labs/comlab .venv-wired/bin/python -m pytest -q apps/ui/tests` | new: 8 passed expected | 8 passed | matches expected | PASS |

No suite failed. No suite shrank relative to baseline. The `labs/gaslab` run reports 4 deselected tests in the current test configuration; passed/skipped counts match the baseline.

---

## 2. Guards

| Guard | Command / check | Result | Status |
|---|---|---|---|
| Wired registry guard count | Python JSON count over `labs/comlab/registry/rules/*.json` + read `apps/wired/wired/registry_guard.py` | 16 files, 73 rules; guard line `_EXPECTED_RULE_COUNT = 73` | PASS |
| Registry manifest equals rules directory | `.venv-wired/bin/python -m pytest -q labs/comlab/registry/tests/test_integration_shim.py::test_production_manifest_matches_rules_directory` | 1 passed | PASS |
| Vocabulary drift guard | `.venv-wired/bin/python -m pytest -q labs/comlab/tests/unit/test_vocabulary.py` | 27 passed | PASS |
| Scoreboard hash and score lock | `.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score` | `Hash lock: ok`; `top3_family: 269/294 = 91.50 %` | PASS |
| Synthetic-vs-real split | same scoreboard command | `191/294` real-only banked; `78` synthetic banked (`C2 19, C3 16, C4 10, C5 10, C6 13, C9 10`) | PASS |

Scoreboard identity held exactly: `269/294`, `191 real + 78 synthetic`. No score-chasing change was made.

---

## 3. UI smoke

| Smoke | Command / check | Result | Status |
|---|---|---|---|
| UI MW-002 fixture | `PYTHONPATH=apps/ui:labs/comlab .venv-wired/bin/python -m pytest -q apps/ui/tests/test_ui.py::test_e2e_mw002_fixture apps/ui/tests/test_ui.py::test_e2e_abstain_case apps/wired/tests/test_oil_cases.py::test_run_case_cli_prints_fault_code apps/wired/tests/test_oil_cases.py::test_oil_cases_route_to_expected_faults` | 4 passed | PASS |
| UI abstain fixture | same command | `test_e2e_abstain_case` passed; asserts abstained verdict with `floor`/`margin` reason | PASS |
| CLI oil fixture cross-check | same command | `MW-002` CLI prints `fault_code=MW-002`; routed oil fixtures pass | PASS |
| Streamlit import smoke | `PYTHONPATH=apps/ui:labs/comlab .venv-wired/bin/python -c "import app"` executed via tool subprocess | exit 0; Streamlit emitted expected bare-mode warnings only | PASS |

One attempted smoke command used a nonexistent test node (`apps/wired/tests/test_oil_cases.py::test_run_case_routes_expected_faults`) and returned no collected tests. It was corrected to the real test nodes above; the corrected command passed.

---

## 4. Pre-push tree audit

Command:

```bash
git status --porcelain
```

Verbatim output before writing this report/progress note:

```text
 M apps/ui/app.py
 M apps/ui/tests/test_ui.py
 M apps/ui/ui_payload.py
 M apps/wired/ship_tasks/SHIP_PROGRESS.md
?? apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md
?? apps/wired/ship_tasks/progress_notes/T-SHIP-UI-3.md
?? pyrightconfig.json
```

Final `git status --porcelain` after writing this report/progress note:

```text
 M apps/ui/app.py
 M apps/ui/tests/test_ui.py
 M apps/ui/ui_payload.py
 M apps/wired/ship_tasks/SHIP_PROGRESS.md
?? apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md
?? apps/wired/ship_tasks/progress_notes/T-SHIP-6.md
?? apps/wired/ship_tasks/progress_notes/T-SHIP-UI-3.md
?? apps/wired/ship_tasks/reports/SHIP_FINAL_VERIFY_2026-07-08.md
?? pyrightconfig.json
```

Expected dirty set per task: T-SHIP-UI-3 files, ledger, progress note, this task's report/progress note, and untracked `pyrightconfig.json`.

**Finding F-1 — unexpected untracked task spec:** `apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md` is untracked and outside the task file's expected dirty-set wording. It is the spec being executed, so the owner should either include it in the explicit-path commit for ship records or tell the architect/coder why it should remain untracked.

**Disposition question for `pyrightconfig.json`:** commit it or gitignore it? This task does not decide.

---

## 5. Secrets sweep

Dirty files checked after this report/note existed:

```text
apps/ui/app.py
apps/ui/tests/test_ui.py
apps/ui/ui_payload.py
apps/wired/ship_tasks/SHIP_PROGRESS.md
apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md
apps/wired/ship_tasks/progress_notes/T-SHIP-UI-3.md
apps/wired/ship_tasks/progress_notes/T-SHIP-6.md
apps/wired/ship_tasks/reports/SHIP_FINAL_VERIFY_2026-07-08.md
pyrightconfig.json
```

Pattern set: `AKIA[0-9A-Z]{16}`, AWS access/secret forms, `(api_key|api-key|secret|token|password) =/ : quoted value`, and private-key PEM markers.  
Result: **0 hits**.

---

## 6. Findings

| ID | Severity | Evidence | Required owner/architect action |
|---|---|---|---|
| F-1 | Dirty-tree disclosure | `?? apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md` in `git status --porcelain`; not named in expected dirty-set wording | Decide/commit explicit path with the ship records, or leave untracked intentionally. |
| Q-1 | Owner disposition | `?? pyrightconfig.json` | Owner decides commit vs gitignore. |

No test, guard, scoreboard, UI smoke, hash-lock, or secrets finding.

---

## 7. Owner explicit-path commit list

If the owner chooses to commit all ship/UI-3/T-SHIP-6 records currently visible, use explicit paths only; do not use `git add -A` or `git add .`.

```bash
git add \
  apps/ui/app.py \
  apps/ui/tests/test_ui.py \
  apps/ui/ui_payload.py \
  apps/wired/ship_tasks/SHIP_PROGRESS.md \
  apps/wired/ship_tasks/T-SHIP-6_final_full_suite_pre_push.md \
  apps/wired/ship_tasks/progress_notes/T-SHIP-UI-3.md \
  apps/wired/ship_tasks/progress_notes/T-SHIP-6.md \
  apps/wired/ship_tasks/reports/SHIP_FINAL_VERIFY_2026-07-08.md
```

Add `pyrightconfig.json` only if the owner decides to commit it:

```bash
git add pyrightconfig.json
```

Commit/push/merge remain owner-run actions.
