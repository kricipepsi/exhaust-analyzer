# T-FL-3 — progress note

**Task:** [[T-FL-3_classify_failure_modes]]  
**Date:** 2026-06-30  
**Report:** [[FL_LOCALIZATION_2026-06-30]]  
**Mode:** STRICT, measure-only.

## Work completed

- Joined `20260630_163900/results.json`, `FL_UPSTREAM_2026-06-30.json`, `case_trace_index.json`, and `traces-raw.json`.
- Classified all 294 accuracy cases with exactly one T-FL-3 mode.
- Wrote per-case localization table, per-family × mode matrix, per-family × stage matrix, and mechanical-wear cross-check in `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md`.
- No engine, oracle, lab, wiki, CSV, trace, or v7 run JSON edits.

## VERIFICATION GATE — T-FL-3

1. Compile : N-A (no Python source files written; report/progress/ledger markdown only)
2. Lint    : N-A (no Python source files written)
3. Types   : N-A (no Python source files written)
4. Tests   : PASS (deterministic join/classifier assertions in analysis: 294/294 accuracy rows classified, 294 unique case IDs, 0 blank modes)
5. Contract: PASS (report contains `case_id`, expected, predicted, `stage_of_first_divergence`, mode, and evidence_ref for every accuracy case)
6. Orphan  : N-A (no mapped fields or named COMLab consumers added)
Result: CLEAN

### Per-mode totals

| Mode | Cases |
| --- | --- |
| SURFACE_DEFECT | 133 |
| ORACLE_SUSPECT | 10 |
| PRODUCER_GAP | 25 |
| PRUNED_OTHER | 0 |
| OUTRANKED | 107 |
| DATA_GAP | 19 |

### Required cited examples

| case_id | expected | predicted | stage | mode | evidence_ref |
| --- | --- | --- | --- | --- | --- |
| era1_011 | cam_timing | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned CT-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=CAM_TIMING_RETARDED_MAP; rank winner_id=MF-001 |
| era1_016 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.9000000000000001 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| CASE-045 | sensor_fault | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |

### Mechanical-wear cross-check

All 10 `mechanical_wear → misfire` oracle-suspect rows rank to `MF-001` with `threshold_miss=False`. The broad audit link is confirmed at rank but refined at producer detail: required expected-rule states are mixed (`COOLANT_LEAK_INTERNAL`, `WORN_PISTON_RINGS`, `WORN_VALVE_SEALS`, `INCOMPLETE_COMBUSTION`), only 3/10 rows carry active `P0300`, and all 10 carry high HC (`450–1100 ppm`). T-FL-3 therefore keeps the T-FL-1 precedence as `ORACLE_SUSPECT` while recording the span evidence in [[FL_LOCALIZATION_2026-06-30]].

## CODE REVIEW — T-FL-3

Scope         : PASS (touched only `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md`, this progress note, and the T-FL-3 ledger row)
Composition   : PASS (no engine/lab/oracle/wiki/CSV edits; no cross-lab source imports; no deferred path)
Consumers     : PASS (no mapped fields added; report consumer is [[T-FL-4_v3_scoreboard]] / v3 planning)
Literals      : PASS (no source boundary literals added)
Docstrings    : N-A (no public functions added)
Craft (WARN)  : Depth N-A; deletion test clean for report-only artifact; seam discipline preserved; interface=test surface N-A.
Result: CLEAN
