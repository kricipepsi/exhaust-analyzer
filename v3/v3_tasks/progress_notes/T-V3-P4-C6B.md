# Progress note — T-V3-P4-C6B

**Task:** [[T-V3-P4-C6B_c6_signal_commit]]  
**Date:** 2026-07-05  
**Mode:** STRICT C6 signal-pack COMMIT

## Scope confirmation

Implemented the C6 sensor-under-detection commit only: pre-flighted `S-COMMIT` (Mode $06 margin + six MAF/airflow columns, no O2 timing), populated the 7 committed C6 columns for the 14 seeded rows, mapped them through the wired OBD payload chain, added `SensorDynamicsState` in the registry shim, applied SF boost / NF prune under the C3 precedence rule, added focused v7 shim tests, minted `[[V3_YARDSTICK_2026-07-05-C6B]]`, and rebound the active scorer to it. Out of scope remained untouched: O2 timing columns, registry JSON, `run_suite.py`, C3 thresholds, abstain margin, `Vault/`, and graphify.

## Implementation notes

- `v3/c6_signal_sim.py`: added `s_commit_mode06_plus_maf_no_timing` plus CLI `--scenario s_commit`; the simulator now blanks live C6 columns before building its baseline rows so it remains pinned to `POST_T_V3_P4_C3B` even after C6B lands.
- `apps/wired/v7/data/cases_petrol_v7.csv`: added 7 columns and populated exactly 14 C6 rows from `v3/data/c6_synthetic_seed_2026-07-05.json`; all non-C6 rows remain blank.
- `labs/comlab/comlab/schemas/ingestion.py`, `apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py`: added/mapped the C6 Mode $06 + MAF/airflow columns with named `SensorDynamicsState` consumers.
- `labs/comlab/registry/integration_shim.py`: added `SensorDynamicsState`; decisive states are `O2_LAZY_OR_BIASED` (`mode06_o2_response_margin_pct <= 10`) and `MAF_UNDERREAD` (both MAF deltas `<= -15`). Decisive C6 boosts `SF-005/SF-008/SF-001/SF-002` by `+0.10` and prunes `NF-001/NF-002`; `SENSOR_HEALTH_UNPROVEN_ABSTAIN` is a no-op. C3 precedence is preserved: C3 prunes `SF-001/SF-002` unless decisive C6 evidence is present.
- `apps/wired/v7/tests/test_c6_sensor_dynamics.py`: covers Mode $06 emit, MAF both-point gate, None-MAF abstain/no-op, PDF-4G-05-style healthy no-op, C3 precedence, and no-C6-columns no-op.
- `apps/wired/fl_tasks/score_v3_yardstick.py`: active yardstick rebound to `V3_YARDSTICK_2026-07-05-C6B` with CSV hash `bf7393688230caf7f15054cc2473343e26351aa72c4615ca83044c7eb12fc0de`; oracle hash remains `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127`; scorer hash unchanged.

## Pre-flight result

Command:

```bash
/agent_workspace/.venv-wired/bin/python v3/c6_signal_sim.py --scenario s_commit
```

Observed:

- Zero-overlay self-check: `OK (all 294 cases matched, drift = 0)`
- `S-COMMIT` WOULD_BANK = **13**
- `S-COMMIT` bank set equals S3 = **True**
- regressions = **0**
- no_fault-neighbour regressions = **0**
- `PDF-4G-05` banked alarm = `[]`

## Score result

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
```

Observed:

- Yardstick: `V3_YARDSTICK_2026-07-05-C6B`
- Hash lock: `ok`
- `top3_family` = **241/294 = 81.97%**
- coverage = **211/294 = 0.72**
- `top3_on_covered` = **177/211 = 83.89%**
- total abstained = **83**
- single-verdict family+state = **146/294 = 49.66%**

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
```

Observed:

- newly_pass = **13**
- newly_fail = **0**
- `REGRESSIONS: (empty)`
- per-family movement: `sensor_fault +13`, all other families `+0`

## VERIFICATION GATE — T-V3-P4-C6B

1. Compile : PASS  (`py_compile apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py v3/c6_signal_sim.py apps/wired/v7/tests/test_c6_sensor_dynamics.py`)
2. Lint    : PASS  (`ruff check apps/wired/fl_tasks/score_v3_yardstick.py apps/wired/wired/composition.py apps/wired/v7/load_corpus.py labs/comlab/comlab/schemas/ingestion.py labs/comlab/registry/integration_shim.py v3/c6_signal_sim.py apps/wired/v7/tests/test_c6_sensor_dynamics.py` -> OK)
3. Types   : PASS  (`cd apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright .` -> 0 errors; root per-file invocation hit the known import-resolution gotcha from `wired-verification-loop`)
4. Tests   : PASS  (`/agent_workspace/.venv-wired/bin/python v3/c6_signal_sim.py --scenario s_commit` -> 13 banked, set==S3, 0/0 regressions; `/agent_workspace/.venv-wired/bin/python -m pytest apps/wired/v7/tests/` -> 31 passed; score+diff commands above -> Hash lock ok, 13 newly_pass, 0 newly_fail)
5. Contract: PASS  (7 committed columns only; no O2 timing columns; 14/14 C6 rows populated; non-C6 rows blank; `run_suite.py` untouched; registry JSON untouched; `V3_YARDSTICK_2026-07-05-C6B` minted)
6. Orphan  : PASS  (`SensorDynamicsState` fields grep-confirmed through `load_corpus.py` -> `composition.py` -> `ingestion.py` -> `integration_shim.py::_sensor_dynamics_state` -> `_score_rule` SF/NF branch)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C6B

Scope         : PASS  (changed lines trace to C6B deliverables: pre-flight sim, CSV columns, payload mapping, shim producer/consumer, tests, yardstick, progress ledger)
Composition   : PASS  (`wired/` remains a composition seam; diagnostic scoring stays in COMLab shim; no cross-lab imports added; no deferred path; no `Vault/`; no graphify)
Consumers     : PASS  (every mapped field carries a named `registry integration_shim SensorDynamicsState` consumer; live reads are in `_sensor_dynamics_state` and `_score_rule`)
Literals      : PASS  (`10.0`, `-15.0`, and `+0.10` are the task-pinned C6B/C6-PRE thresholds; the report ties them to `[[V3_C6_REVEAL_CONTRACT_2026-07-05]]` and `[[V3_C6_SIGNAL_DRYRUN_2026-07-05]]`)
Docstrings    : PASS  (new enum/helper/test helpers carry docstrings)
Craft (WARN)  : Depth: shim branch stays a thin producer/consumer override beside C2/C3; no rule JSON mutation. Deletion test: all new fields are consumed today by the C6 branch; the six MAF columns also serve the live `MAF_UNDERREAD` branch and unblock later C5/C4 reuse. Seam discipline: CSV -> loader -> composition -> ingestion -> shim is single-path; no duplicate mapping in runner/tests. Interface=test surface: public score/diff and v7 tests exercise the committed path; private shim tests pin branch edge cases.
Result: CLEAN

## Follow-on

C6B unblocks the C5 pack in the pinned sequence. The abstain-cal thread remains parked: C6B deliberately left `MARGIN=0.02` untouched, so 5 of the 13 C6 top-3 flips can still be hidden by abstain behavior.
