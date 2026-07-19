# T-FL-1 — progress note

**Task:** [[T-FL-1_lock_true_baseline]]  
**Report:** [[FL_YARDSTICK_2026-06-30]] (`apps/wired/fl_tasks/reports/FL_YARDSTICK_2026-06-30.md`)  
**Mode:** read-only measurement; no engine/oracle/CSV/wiki/scorer edits.

## Result

Frozen v3 yardstick created from existing run `apps/wired/v7/runs/20260630_163900/results.json` joined to `apps/wired/v7/data/cases_petrol_v7.csv`; no suite rerun was needed.

| Metric | Value |
|---|---:|
| Accuracy denominator | 294 |
| As-pinned family-only routing | 141 / 294 = 47.96 % |
| As-pinned state-only routing | 275 / 294 = 93.54 % |
| **As-pinned primary family+state routing** | **133 / 294 = 45.24 %** |
| `fault_code` surface dimension | 0 / 294 PASS; 294 / 294 FAIL |
| `confidence` surface dimension | 21 / 294 PASS; 273 / 294 FAIL |
| **Adjudicated primary family+state routing** | **143 / 294 = 48.64 %** |
| Adjudication delta | +10 / 294 = +3.40 pp |

## ORACLE_SUSPECT adjudication

| Cluster | Cases | Decision | Primary-yardstick effect | Evidence |
|---|---:|---|---:|---|
| `mechanical_wear → misfire` | 10 | `oracle-correct` for family+state | +10 | COMWIKI-06 says `misfire` includes mechanical/compression dropout (`labs/comlab/wiki/06_fault_atlas_families.md:73-76`); COMWIKI-06 says `mechanical_wear` has no distinct single-snapshot chemistry (`:101-104`); COMWIKI-05 maps low-compression mechanical misfire to `misfire` (`labs/comlab/wiki/05_fault_taxonomy.md:82-88`); KG says gas alone cannot distinguish compression loss from ignition failure (`labs/comlab/comlab/config/kg/mechanical_wear.json:155-171`). |

Pending-for-v3 row logged in `FL_PROGRESS.md`: `FL-V3-ORACLE-MW-MISFIRE`.

## Frozen hashes

| Artefact | SHA-256 |
|---|---|
| `apps/wired/v7/data/cases_petrol_v7.csv` | `a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae` |
| Oracle subset (`case_id`, `tag`, all `expected_*`, `accuracy_excluded`) | `a4de411098eb3c08d23d4881f4863fa1bd0a204cbb4041acb595474a1cecad7d` |
| `apps/wired/v7/run_suite.py` | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| `apps/wired/v7/runs/20260630_163900/results.json` | `d9069f8dea738de91654320b4f431b4345364ff27571f39cce2fd5b7fb210ee3` |

Workspace commit at measurement: `fe3b827cfa4c80b099873a6c3c4b17833b50ae98`.

Run command frozen for v2 default:

```bash
cd /agent_workspace && /agent_workspace/.venv-wired/bin/python apps/wired/v7/run_suite.py
```

Environment: `USE_V2_REGISTRY` unset; COMLab default resolves unset to v2 (`labs/comlab/comlab/core/lab_pipeline_aggregator.py:116-121`). `WIRED_OTEL` unset; `--trace` not used.

## VERIFICATION GATE — T-FL-1

1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/v7/run_suite.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/v7/run_suite.py`)
3. Types   : PASS  (`cd apps/wired; /agent_workspace/.venv-wired/bin/python -m pyright` -> 0 errors)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pytest -q apps/wired/v7/tests/test_run_suite.py` -> 6 passed; Python yardstick assertions -> PASS: metrics, hashes, oracle row present)
5. Contract: PASS  (`FL_YARDSTICK_2026-06-30.md` contains corpus/oracle/scorer/run hashes, as-pinned and adjudicated routing numbers, surface dims separated, ORACLE_SUSPECT decision table, and run command/env; `FL_PROGRESS.md` has T-FL-1 done and pending-for-v3 oracle row)
6. Orphan  : N-A   (no domain field/fault/consumer mapping added; named consumer is [[T-FL-4_v3_scoreboard]] and v3 coders)
Result: CLEAN

## CODE REVIEW — T-FL-1

Scope         : PASS  (changed files are limited to `apps/wired/fl_tasks/reports/FL_YARDSTICK_2026-06-30.md`, `apps/wired/fl_tasks/progress_notes/T-FL-1.md`, and the T-FL-1/follow-up rows in `apps/wired/fl_tasks/FL_PROGRESS.md`)  
Composition   : PASS  (no lab edits, no engine/scorer/oracle/wiki edits, no `ARCHIVE` import, no deferred path, no `graphify`)  
Consumers     : PASS  (no mapped lab field added; report consumer is [[T-FL-4_v3_scoreboard]] / v3 coders per task spec)  
Literals      : PASS  (hashes and routing counts are measured artefact values; wiki citations included for adjudication; no boundary literals added)  
Docstrings    : N-A   (no Python public function/mapper added)  
Craft (WARN)  : depth=report-only measurement, no logic seam added; deletion=no redundant helper/scaffold; seam=yardstick isolated under `fl_tasks/`; interface=test surface is existing public v7 scorer plus frozen JSON/CSV, not private helpers.  
Result: CLEAN
