# T-FL-2 — Capture upstream evidence progress

**Task:** [[T-FL-2_capture_upstream_evidence]]  
**Status:** done  
**Date:** 2026-06-30  
**Scope:** read-only FL capture harness + report only. No engine, lab, oracle, wiki, ARCHIVE, graphify, or Vault edits.

## Deliverables

- Added `apps/wired/fl_tasks/capture_upstream_evidence.py`.
- Wrote `apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.md`.
- Wrote `apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json` for [[T-FL-3_classify_failure_modes]].

## Capture-method proof

Method: read-only replay of GASLab/OBDLab on the same sanitized inputs as the v7 composition path: `v7.load_corpus.row_to_raw_inputs()` + wired composition seam helpers `_run_gaslab()` / `_run_obdlab()`. Live-pipeline proof uses in-memory OpenTelemetry, calls public `diagnose()`, and reads COMLab `phase.prune` span events.

Coverage from `FL_UPSTREAM_2026-06-30.md`:

| Metric | Value |
|---|---:|
| Total corpus rows | 314 |
| GASLab chemistry states captured | 314/314 |
| OBDLab O2 mode/status field populated | 314/314 |
| Live `phase.prune` spot checks | 3 |

Spot checks against live `phase.prune` `rule_pruned` events:

| case_id | expected family | expected code | emitted GASLab state | required state | pruned rule | prune reason | failed gating key |
|---|---|---|---|---|---|---|---|
| `era1_002` | `mechanical_wear` | `ERR-MW-002` | `RICH_MISFIRE` | `COOLANT_LEAK_INTERNAL` | `MW-002` | `chemistry` | `gas_lab_state` |
| `era3_019` | `exhaust_leak` | `ERR-EL-002` | `VVT_FAILURE` | `EXHAUST_AIR_LEAK` | `EL-002` | `missing_evidence` | `no_evidence_satisfied` |
| `REAL-001` | `non_starter` | `ERR-NS-001` | `SAMPLE_INVALID` | `IGNITION_MISFIRE` | `NS-001` | `chemistry` | `gas_lab_state` |

Dead-family emitted-vs-required summary:

| Expected family | Emitted GASLab states | Registry-required GASLab states |
|---|---|---|
| `mechanical_wear` | `EGR_STUCK_OPEN=4`, `GDI_HPFP_INTERNAL_SEAL_LEAK=1`, `IGNITION_MISFIRE=1`, `INCOMPLETE_COMBUSTION=1`, `INCOMPLETE_OXIDATION=1`, `POA_SIGNATURE=1`, `RICH_MISFIRE=5` | `COOLANT_LEAK_INTERNAL`, `IGNITION_MISFIRE`, `INCOMPLETE_COMBUSTION`, `POA_SIGNATURE`, `WORN_ENGINE`, `WORN_PISTON_RINGS`, `WORN_VALVE_SEALS` |
| `exhaust_leak` | `LEAN_MIXTURE=1`, `SAMPLE_INVALID=7`, `VVT_FAILURE=2` | `EXHAUST_AIR_LEAK`, `INCOMPLETE_COMBUSTION`, `NORMAL_OPERATION`, `SAMPLE_INVALID` |
| `non_starter` | `SAMPLE_INVALID=5` | `IGNITION_MISFIRE`, `INCOMPLETE_COMBUSTION`, `LEAN_MIXTURE`, `NORMAL_OPERATION`, `SAMPLE_INVALID` |

## VERIFICATION GATE — T-FL-2

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/capture_upstream_evidence.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/capture_upstream_evidence.py` -> OK)
3. Types   : PASS (`cd apps/wired && /agent_workspace/.venv-wired/bin/python -m pyright` -> 0 errors; targeted `pyright fl_tasks/capture_upstream_evidence.py` -> 0 errors)
4. Tests   : PASS (`/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/capture_upstream_evidence.py --no-write` -> `Captured upstream evidence: gas=314/314 obd=314/314 spot_checks=3`)
5. Contract: PASS (`FL_UPSTREAM_2026-06-30.json` contains 314 `records`, `dead_family_records`, and 3 live `phase.prune` spot checks; report includes coverage + dead-family emitted-vs-required tables)
6. Orphan  : N-A (no new COMLab field/consumer; report JSON is the named consumer artifact for T-FL-3)
Result: CLEAN

## CODE REVIEW — T-FL-2

Scope         : PASS (changes are limited to `fl_tasks/`: harness, report JSON/Markdown, progress note, ledger)
Composition   : PASS (no lab/engine/oracle/wiki edits; no cross-lab logic added to labs; no deferred path; no graphify/Vault/ARCHIVE imports)
Consumers     : PASS (`FL_UPSTREAM_2026-06-30.json` is consumed by [[T-FL-3_classify_failure_modes]]; no mapped lab->COMLab field added)
Literals      : PASS (no new boundary numeric thresholds; report counts derive from corpus/run output)
Docstrings    : PASS (new harness functions have docstrings)
Craft (WARN)  : Thin read-only seam; deletion test passes because each captured field is emitted into the report/JSON; trace proof isolated from capture loop; public CLI is the test surface.
Result: CLEAN
