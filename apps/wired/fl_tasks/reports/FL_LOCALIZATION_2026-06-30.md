# FL_LOCALIZATION_2026-06-30 — per-case failure localization

**Task:** [[T-FL-3_classify_failure_modes]]  
**Date:** 2026-06-30  
**Mode:** STRICT, measure-only. No engine/oracle/lab/wiki/CSV edits.  
**Consumer:** [[T-FL-4_v3_scoreboard]] and v3 rebuild coders.  
**Inputs:** untraced run `apps/wired/v7/runs/20260630_163900/results.json`; traced run `apps/wired/v7/runs/20260630_190651/results.json`; upstream capture `apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json`; Jaeger case trace index `apps/wired/trace/runs/V7_TRACE_20260630/case_trace_index.json`; raw Jaeger spans `apps/wired/trace/runs/V7_TRACE_20260630/traces-raw.json`.

## Scope confirmation

T-FL-3 classifies the existing v7 failures only. It writes this report and the T-FL-3 progress note, then marks the ledger row done. It does not tune routing, edit the oracle, change lab code, change the corpus, import `ARCHIVE/`, run `graphify`, or commit raw run/trace JSON.

## Method

The classifier joins each accuracy row to three observable sources:

1. `run.results[].dimensions` from `20260630_163900/results.json` for `fault_family` and `state` pass/fail.
2. `FL_UPSTREAM_2026-06-30.json` for `gas_chemistry_states[]`, `obd_o2_failure_mode`, and the required GASLab state for the expected code where available.
3. Jaeger `phase.prune` / `phase.rank` logs from `traces-raw.json`, keyed by `case_trace_index.json`: `rule_pruned{rule_id, prune_reason, failed_gating_key}`, `rule_scored{rule_id, score}`, `router.winner_id`, `router.winner_score`, `router.candidates_in/out`, and `router.threshold_miss`.

One mode is assigned per accuracy case using the task precedence: `SURFACE_DEFECT` → `ORACLE_SUSPECT` → `PRODUCER_GAP` → `PRUNED_OTHER` → `OUTRANKED` → `DATA_GAP`.

Implementation details for repeatability:

- `SURFACE_DEFECT`: `fault_family=PASS` and `state=PASS`; remaining failures are non-routing dimensions (`fault_code`, `confidence`, `perception_gap`, or `demotion_note_contains`).
- `ORACLE_SUSPECT`: the 10 `mechanical_wear → misfire` rows carried forward from [[FL_YARDSTICK_2026-06-30]] / `FL-V3-ORACLE-MW-MISFIRE`.
- `PRODUCER_GAP`: the expected rule was pruned on `gas_lab_state` / chemistry and the upstream GASLab states do not contain the required state for the expected code.
- `OUTRANKED`: the expected rule, or another rule from the expected family when the expected-code mapping is ambiguous, appears in `phase.rank rule_scored`, but `router.winner_id` belongs to another family.
- `DATA_GAP`: no expected-family rule scored and the observed prune reason is missing input evidence (`obd:*`, `no_evidence_satisfied`, missing DTC/input), or no expected-family prune/score event exists.
- `PRUNED_OTHER`: reserved for non-producer prune/contract failures. This run produced none after precedence.

## Verification summary

- Accuracy denominator classified: **294 / 294**.
- Unique case IDs: **294 / 294**.
- Blank modes: **0**.
- Primary-routing surface rows: **133**; all have `fault_family=PASS,state=PASS`.

### Per-mode totals

| Mode | Cases |
| --- | --- |
| SURFACE_DEFECT | 133 |
| ORACLE_SUSPECT | 10 |
| PRODUCER_GAP | 25 |
| PRUNED_OTHER | 0 |
| OUTRANKED | 107 |
| DATA_GAP | 19 |

### Stage-of-first-divergence totals

| Stage | Cases |
| --- | --- |
| surface | 133 |
| gaslab | 25 |
| obdlab | 10 |
| dtc | 9 |
| rank | 117 |

## Per-family × mode matrix

| Expected family | Total | SURFACE_DEFECT | ORACLE_SUSPECT | PRODUCER_GAP | PRUNED_OTHER | OUTRANKED | DATA_GAP | Dominant mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cam_timing | 11 | 7 | 0 | 3 | 0 | 1 | 0 | SURFACE_DEFECT |
| catalyst_failure | 23 | 9 | 0 | 0 | 0 | 14 | 0 | OUTRANKED |
| ecu_fault | 31 | 4 | 0 | 4 | 0 | 23 | 0 | OUTRANKED |
| exhaust_leak | 10 | 0 | 0 | 0 | 0 | 10 | 0 | OUTRANKED |
| ignition_fault | 4 | 1 | 0 | 0 | 0 | 3 | 0 | OUTRANKED |
| lean_condition | 62 | 37 | 0 | 0 | 0 | 19 | 6 | SURFACE_DEFECT |
| mechanical_wear | 14 | 0 | 10 | 3 | 0 | 1 | 0 | ORACLE_SUSPECT |
| misfire | 54 | 46 | 0 | 0 | 0 | 8 | 0 | SURFACE_DEFECT |
| no_fault | 18 | 0 | 0 | 0 | 0 | 8 | 10 | DATA_GAP |
| non_starter | 5 | 0 | 0 | 4 | 0 | 1 | 0 | PRODUCER_GAP |
| rich_mixture | 37 | 23 | 0 | 11 | 0 | 3 | 0 | SURFACE_DEFECT |
| sensor_fault | 25 | 6 | 0 | 0 | 0 | 16 | 3 | OUTRANKED |

## Per-family × stage matrix

| Expected family | Total | surface | gaslab | obdlab | dtc | prune | rank | Dominant stage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| cam_timing | 11 | 7 | 3 | 0 | 0 | 0 | 1 | surface |
| catalyst_failure | 23 | 9 | 0 | 0 | 0 | 0 | 14 | rank |
| ecu_fault | 31 | 4 | 4 | 0 | 0 | 0 | 23 | rank |
| exhaust_leak | 10 | 0 | 0 | 0 | 0 | 0 | 10 | rank |
| ignition_fault | 4 | 1 | 0 | 0 | 0 | 0 | 3 | rank |
| lean_condition | 62 | 37 | 0 | 0 | 6 | 0 | 19 | surface |
| mechanical_wear | 14 | 0 | 3 | 0 | 0 | 0 | 11 | rank |
| misfire | 54 | 46 | 0 | 0 | 0 | 0 | 8 | surface |
| no_fault | 18 | 0 | 0 | 10 | 0 | 0 | 8 | obdlab |
| non_starter | 5 | 0 | 4 | 0 | 0 | 0 | 1 | gaslab |
| rich_mixture | 37 | 23 | 11 | 0 | 0 | 0 | 3 | surface |
| sensor_fault | 25 | 6 | 0 | 0 | 3 | 0 | 16 | rank |

## Dead-family calls

- `mechanical_wear`: 14 rows → `ORACLE_SUSPECT` 10, `PRODUCER_GAP` 3, `OUTRANKED` 1. The dominant actionable planning item remains the oracle/product-definition issue from `FL-V3-ORACLE-MW-MISFIRE`; the non-suspect rows split between upstream GASLab producer gaps and rank outrank.
- `exhaust_leak`: 10 rows → `OUTRANKED` 10. The expected `EL-*` rule scored, but `phase.rank` picked `LC-*` or `SF-*` winners. This is rank/scoring-term work, not a producer gap.
- `non_starter`: 5 rows → `PRODUCER_GAP` 4, `OUTRANKED` 1. The dominant failure is upstream GASLab not producing the required starter/misfire/incomplete-combustion state for the expected non-starter rule.

## Required fully-cited examples

| case_id | expected | predicted | stage | mode | evidence_ref |
| --- | --- | --- | --- | --- | --- |
| era1_011 | cam_timing | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned CT-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=CAM_TIMING_RETARDED_MAP; rank winner_id=MF-001 |
| era1_016 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.9000000000000001 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| CASE-045 | sensor_fault | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |

## Mechanical-wear cross-check

The audit claim is **partly confirmed and refined** by the spans:

- Confirmed: all 10 `mechanical_wear → misfire` oracle-suspect rows are decided at `phase.rank` with `winner_id=MF-001`; `router.threshold_miss=False` in each row. Mechanical-wear expected rules are frequently pruned on `gas_lab_state` chemistry.
- Refined: the missing required GASLab state is not uniformly `WORN_*`. The 10 rows require `COOLANT_LEAK_INTERNAL` (5), `WORN_PISTON_RINGS` (2), `WORN_VALVE_SEALS` (1), or `INCOMPLETE_COMBUSTION` (2), with some rows having multiple expected-rule candidates. Only 3/10 carry active `P0300`; all 10 have high HC (`450–1100 ppm`) and rank to `MF-001`.
- Classification consequence: T-FL-3 keeps the 10-row T-FL-1 precedence as `ORACLE_SUSPECT`, not `PRODUCER_GAP`, because the engine's misfire-family answer is wiki-defensible for a single-snapshot yardstick even when the exact winner code remains `MF-001` rather than `ERR-MF-006`.

| case_id | expected_code | required | emitted | dtc | hc | winner | winner_score | expected_trace | mode |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CSV-118 | ERR-MW-004 | WORN_VALVE_SEALS | EGR_STUCK_OPEN | [] | 1100 | MF-001 | 0.9500000000000001 | pruned MW-002:chemistry/gas_lab_state; pruned MW-004:chemistry/gas_lab_state | ORACLE_SUSPECT |
| CSV-119 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | RICH_MISFIRE | [] | 950 | MF-001 | 0.9500000000000001 | pruned MW-002:chemistry/gas_lab_state; pruned MW-003:chemistry/gas_lab_state | ORACLE_SUSPECT |
| CSV-120 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | IGNITION_MISFIRE | [] | 1100 | MF-001 | 1 | pruned MW-002:chemistry/gas_lab_state; pruned MW-003:chemistry/gas_lab_state; scored MW-007=1 | ORACLE_SUSPECT |
| EXT-222 | ERR-MW-005 | INCOMPLETE_COMBUSTION | INCOMPLETE_COMBUSTION | [] | 450 | MF-001 | 0.9500000000000001 | pruned MW-004:chemistry/gas_lab_state; pruned MW-005:missing_evidence/obd:rpm; scored MW-006=0.7 | ORACLE_SUSPECT |
| EXT-223 | ERR-MW-003 | WORN_PISTON_RINGS | EGR_STUCK_OPEN | [] | 800 | MF-001 | 0.9500000000000001 | pruned MW-001:chemistry/gas_lab_state; pruned MW-003:chemistry/gas_lab_state | ORACLE_SUSPECT |
| EXT-224 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | RICH_MISFIRE | P0300 | 950 | MF-001 | 1 | pruned MW-002:chemistry/gas_lab_state; pruned MW-003:chemistry/gas_lab_state | ORACLE_SUSPECT |
| MECH-002 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | RICH_MISFIRE | [] | 800 | MF-001 | 0.9500000000000001 | pruned MW-002:chemistry/gas_lab_state; pruned MW-003:chemistry/gas_lab_state | ORACLE_SUSPECT |
| MECH-006 | ERR-MW-005 | INCOMPLETE_COMBUSTION | RICH_MISFIRE | [] | 550 | MF-001 | 0.9500000000000001 | pruned MW-004:chemistry/gas_lab_state; pruned MW-005:chemistry/gas_lab_state; scored MW-006=0.7 | ORACLE_SUSPECT |
| era1_002 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | RICH_MISFIRE | P0300 | 950 | MF-001 | 1 | pruned MW-002:chemistry/gas_lab_state | ORACLE_SUSPECT |
| era1_015 | ERR-MW-003 | WORN_PISTON_RINGS | INCOMPLETE_OXIDATION | P0300 | 850 | MF-001 | 1 | pruned MW-003:chemistry/gas_lab_state | ORACLE_SUSPECT |

## Per-case localization table

| case_id | expected | predicted | stage_of_first_divergence | mode | evidence_ref |
| --- | --- | --- | --- | --- | --- |
| CASE-018 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-115 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-116 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXP-N007 | cam_timing | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored CT-007=0.9000000000000001 but winner_id=SF-001 score=0.95; candidates_in=19,threshold_miss=False |
| EXP-N023 | cam_timing | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned CT-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks expected required=NORMAL_OPERATION; rank winner_id=SF-001 |
| EXT-209 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-210 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| MECH-004 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| era1_011 | cam_timing | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned CT-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=CAM_TIMING_RETARDED_MAP; rank winner_id=MF-001 |
| era2_008 | cam_timing | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned CT-004 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=VVT_FAILURE; rank winner_id=SF-001 |
| era3_018 | cam_timing | cam_timing | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-013 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-003=0.8500000000000001 but winner_id=LC-002 score=0.9500000000000002; candidates_in=21,threshold_miss=False |
| CASE-015 | catalyst_failure | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored CF-002=0.8 but winner_id=NF-001 score=0.93; candidates_in=17,threshold_miss=False |
| CASE-016 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-026 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-121 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-002=0.8 but winner_id=LC-001 score=0.9500000000000001; candidates_in=13,threshold_miss=False |
| CSV-122 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-002=0.8 but winner_id=LC-001 score=0.9500000000000001; candidates_in=12,threshold_miss=False |
| EXP-N008 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N012 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N025 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank expected_family rule_scored CF-001=0.9 but winner_id=LC-002 score=0.9000000000000001; candidates_in=11,threshold_miss=False |
| EXT-207 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-003=0.8500000000000001 but winner_id=LC-002 score=0.9500000000000002; candidates_in=23,threshold_miss=False |
| EXT-208 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-003=0.8500000000000001 but winner_id=LC-002 score=0.9500000000000002; candidates_in=22,threshold_miss=False |
| EXT-213 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-003=0.8500000000000001 but winner_id=LC-002 score=0.9500000000000002; candidates_in=22,threshold_miss=False |
| EXT-232 | catalyst_failure | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored CF-002=0.8 but winner_id=NF-001 score=0.93; candidates_in=17,threshold_miss=False |
| EXT-233 | catalyst_failure | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored CF-002=0.8 but winner_id=LC-001 score=0.9500000000000001; candidates_in=17,threshold_miss=False |
| PDF-4G-01 | catalyst_failure | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored CF-001=0.9 but winner_id=SF-002 score=0.95; candidates_in=15,threshold_miss=False |
| PDF-HI-006 | catalyst_failure | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored CF-002=0.75 but winner_id=SF-002 score=0.95; candidates_in=12,threshold_miss=False |
| REAL-005 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-PDF_4G_01 | catalyst_failure | cam_timing | rank | OUTRANKED | trace.phase.rank expected_family rule_scored CF-002=0.75 but winner_id=CT-002 score=0.8; candidates_in=7,threshold_miss=False |
| YAML-PDF_HI_006 | catalyst_failure | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored CF-001=0.9 but winner_id=SF-002 score=0.95; candidates_in=11,threshold_miss=False |
| case_010 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,demotion_note_contains |
| case_034 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_008 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_001 | catalyst_failure | catalyst_failure | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-039 | ecu_fault | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned EF-005 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=EGR_STUCK_OPEN lacks expected required=POA_SIGNATURE; rank winner_id=SF-001 |
| CSV-041 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| CSV-043 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.8 but winner_id=LC-002 score=0.9000000000000001; candidates_in=13,threshold_miss=False |
| CSV-045 | ecu_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=SF-002 score=0.95; candidates_in=18,threshold_miss=False |
| CSV-072 | ecu_fault | ecu_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-123 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored EF-002=0.9 but winner_id=RM-001 score=1; candidates_in=23,threshold_miss=False |
| CSV-124 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored EF-002=0.9 but winner_id=RM-001 score=1; candidates_in=22,threshold_miss=False |
| CSV-125 | ecu_fault | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned EF-005 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=EGR_STUCK_OPEN lacks expected required=NORMAL_OPERATION; rank winner_id=CF-001 |
| CSV-126 | ecu_fault | misfire | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned EF-005 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=EGR_STUCK_OPEN lacks expected required=NORMAL_OPERATION; rank winner_id=MF-001 |
| ECU-001 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| ECU-002 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.8 but winner_id=LC-002 score=0.9000000000000001; candidates_in=13,threshold_miss=False |
| ECU-003 | ecu_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.8 but winner_id=CF-001 score=0.9; candidates_in=10,threshold_miss=False |
| ECU-009 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=RM-001 score=0.95; candidates_in=14,threshold_miss=False |
| EXP-N002 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=23,threshold_miss=False |
| EXP-N004 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| EXP-N005 | ecu_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=CF-001 score=0.9500000000000001; candidates_in=16,threshold_miss=False |
| EXP-N018 | ecu_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EF-003=0.85 but winner_id=SF-001 score=0.95; candidates_in=13,threshold_miss=False |
| EXP-N019 | ecu_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EF-003=0.85 but winner_id=CF-001 score=0.9500000000000001; candidates_in=16,threshold_miss=False |
| EXT-221 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| TC-021 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=RM-001 score=0.95; candidates_in=22,threshold_miss=False |
| YAML-CSV41 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EF-003=0.85 but winner_id=RM-001 score=0.95; candidates_in=22,threshold_miss=False |
| YAML-CSV43 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.8 but winner_id=LC-002 score=0.9000000000000001; candidates_in=13,threshold_miss=False |
| YAML-CSV45 | ecu_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=SF-002 score=0.95; candidates_in=18,threshold_miss=False |
| YAML-CSV72 | ecu_fault | ecu_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-RULE_NOx_1 | ecu_fault | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned EF-005 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=VVT_FAILURE lacks expected required=NORMAL_OPERATION; rank winner_id=CF-001 |
| YAML-TC22 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.8 but winner_id=LC-002 score=0.9000000000000001; candidates_in=13,threshold_miss=False |
| YAML-TC47 | ecu_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored EF-003=0.85 but winner_id=SF-002 score=0.95; candidates_in=18,threshold_miss=False |
| case_001 | ecu_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EF-001=0.9 but winner_id=LC-001 score=1; candidates_in=22,threshold_miss=False |
| case_013 | ecu_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored EF-002=0.9 but winner_id=RM-001 score=1; candidates_in=24,threshold_miss=False |
| case_027 | ecu_fault | ecu_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_020 | ecu_fault | ecu_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-095 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.9000000000000001 but winner_id=LC-001 score=1; candidates_in=21,threshold_miss=False |
| CSV-129 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EL-003=0.7000000000000001 but winner_id=SF-002 score=0.95; candidates_in=17,threshold_miss=False |
| CSV-130 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EL-003=0.7000000000000001 but winner_id=SF-002 score=0.95; candidates_in=17,threshold_miss=False |
| EXT-238 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EL-003=0.7000000000000001 but winner_id=SF-002 score=0.95; candidates_in=16,threshold_miss=False |
| EXT-239 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EL-003=0.7000000000000001 but winner_id=SF-002 score=0.95; candidates_in=16,threshold_miss=False |
| PDF-HI-007 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EL-003=0.7000000000000001 but winner_id=LC-001 score=0.95; candidates_in=18,threshold_miss=False |
| TC-048 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.8500000000000001 but winner_id=SF-002 score=0.95; candidates_in=21,threshold_miss=False |
| YAML-CSV95 | exhaust_leak | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.8500000000000001 but winner_id=SF-002 score=0.95; candidates_in=21,threshold_miss=False |
| era1_016 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored EL-001=0.9000000000000001 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| era3_019 | exhaust_leak | lean_condition | rank | OUTRANKED | trace.phase.rank expected_family rule_scored EL-001=0.9000000000000001 but winner_id=LC-001 score=1; candidates_in=24,threshold_miss=False |
| CASE-035 | ignition_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored IF-002=0.91 but winner_id=SF-001 score=0.95; candidates_in=18,threshold_miss=False |
| EXP-N026 | ignition_fault | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored IF-002=0.91 but winner_id=SF-001 score=0.95; candidates_in=17,threshold_miss=False |
| PDF-4G-04 | ignition_fault | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored IF-003=0.47 but winner_id=MF-001 score=0.9500000000000001; candidates_in=14,threshold_miss=False |
| era3_003 | ignition_fault | ignition_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-011 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-012 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-017 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-019 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-020 | lean_condition | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=SF-001 score=0.95; candidates_in=15,threshold_miss=False |
| CASE-027 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-030 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-032 | lean_condition | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| CASE-034 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-036 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-016 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-068 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-100 | lean_condition | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=RM-001 score=1; candidates_in=21,threshold_miss=False |
| CSV-109 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-110 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-111 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-112 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-113 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=MF-001 score=0.9500000000000001; candidates_in=18,threshold_miss=False |
| CSV-114 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=MF-001 score=0.9500000000000001; candidates_in=18,threshold_miss=False |
| EXP-N001 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N009 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N011 | lean_condition | sensor_fault | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| EXP-N017 | lean_condition | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=RM-001 score=1; candidates_in=17,threshold_miss=False |
| EXP-N022 | lean_condition | catalyst_failure | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| EXP-N029 | lean_condition | mechanical_wear | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=MW-002 |
| EXT-201 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-202 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-204 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-205 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-211 | lean_condition | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=SF-001 score=0.95; candidates_in=16,threshold_miss=False |
| EXT-212 | lean_condition | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=SF-001 score=0.95; candidates_in=16,threshold_miss=False |
| EXT-214 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-215 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-218 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| MECH-003 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| REAL-002 | lean_condition | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-002 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| REAL-004 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=MF-001 score=0.9500000000000001; candidates_in=18,threshold_miss=False |
| TC-011 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-CSV68 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_003 | lean_condition | catalyst_failure | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| case_008 | lean_condition | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored LC-001=0.9 but winner_id=SF-002 score=0.95; candidates_in=23,threshold_miss=False |
| case_016 | lean_condition | catalyst_failure | dtc | DATA_GAP | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| case_018 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_019 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_001 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=MF-001 score=0.9500000000000001; candidates_in=16,threshold_miss=False |
| era1_005 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_007 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_018 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_019 | lean_condition | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=CF-001 score=0.9; candidates_in=13,threshold_miss=False |
| era2_003 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_006 | lean_condition | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.9000000000000001 but winner_id=CF-001 score=0.9500000000000001; candidates_in=13,threshold_miss=False |
| era2_011 | lean_condition | cam_timing | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=CT-008 score=1; candidates_in=14,threshold_miss=False |
| era2_014 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_015 | lean_condition | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=RM-001 score=1; candidates_in=17,threshold_miss=False |
| era2_017 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_002 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_007 | lean_condition | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=CF-001 score=0.9500000000000001; candidates_in=16,threshold_miss=False |
| era3_008 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.9500000000000002 but winner_id=MF-002 score=0.9500000000000002; candidates_in=20,threshold_miss=False |
| era3_009 | lean_condition | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.9000000000000001 but winner_id=NF-001 score=0.93; candidates_in=14,threshold_miss=False |
| era3_013 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_015 | lean_condition | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored LC-002=0.8500000000000001 but winner_id=MF-001 score=0.9; candidates_in=15,threshold_miss=False |
| era3_016 | lean_condition | lean_condition | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-117 | mechanical_wear | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned MW-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=EGR_STUCK_OPEN lacks required=WORN_VALVE_SEALS; rank winner_id=SF-001 |
| CSV-118 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=EGR_STUCK_OPEN |
| CSV-119 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=RICH_MISFIRE |
| CSV-120 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=IGNITION_MISFIRE |
| EXP-N030 | mechanical_wear | lean_condition | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned MW-002 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=GDI_HPFP_INTERNAL_SEAL_LEAK lacks required=COOLANT_LEAK_INTERNAL; rank winner_id=LC-001 |
| EXT-222 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=INCOMPLETE_COMBUSTION |
| EXT-223 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=EGR_STUCK_OPEN |
| EXT-224 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=RICH_MISFIRE |
| MECH-001 | mechanical_wear | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned MW-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=EGR_STUCK_OPEN lacks required=WORN_PISTON_RINGS; rank winner_id=SF-001 |
| MECH-002 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=RICH_MISFIRE |
| MECH-006 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=RICH_MISFIRE |
| case_044 | mechanical_wear | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MW-006=0.7 but winner_id=SF-001 score=0.95; candidates_in=16,threshold_miss=False |
| era1_002 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=RICH_MISFIRE |
| era1_015 | mechanical_wear | misfire | rank | ORACLE_SUSPECT | T-FL-1 FL-V3-ORACLE-MW-MISFIRE; trace.phase.rank winner_id=MF-001, threshold_miss=False; upstream gas=INCOMPLETE_OXIDATION |
| CASE-021 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-024 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-028 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-033 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-038 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-022 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-052 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-066 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-101 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-102 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-103 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-104 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-105 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-106 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CSV-107 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CSV-108 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| ECU-007 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| ECU-008 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXP-N014 | misfire | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-001=0.9 but winner_id=SF-001 score=0.95; candidates_in=16,threshold_miss=False |
| EXP-N016 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N021 | misfire | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored MF-002=0.9500000000000002 but winner_id=LC-001 score=1; candidates_in=25,threshold_miss=False |
| EXT-225 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-226 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-228 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-234 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-235 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-236 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-237 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| MECH-005 | misfire | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-001=0.9 but winner_id=SF-001 score=0.95; candidates_in=15,threshold_miss=False |
| PDF-4G-02 | misfire | sensor_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-001=0.9 but winner_id=SF-002 score=0.95; candidates_in=13,threshold_miss=False |
| PDF-4G-05 | misfire | sensor_fault | rank | OUTRANKED | trace.phase.rank rule_scored MF-005=0.8 but winner_id=SF-002 score=0.95; candidates_in=11,threshold_miss=False |
| PDF-HI-002 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| PDF-HI-008 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-CSV22 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-CSV52 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-CSV66 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-PDF_4G_02 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-PDF_4G_04 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-PDF_4G_05 | misfire | ecu_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-005=0.8 but winner_id=EF-004 score=0.9; candidates_in=10,threshold_miss=False |
| YAML-PDF_HI_002 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| YAML-RULE_CO_1 | misfire | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-005=0.8 but winner_id=CF-001 score=0.9500000000000001; candidates_in=8,threshold_miss=False |
| YAML-TC36 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-TC37 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_005 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_022 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_004 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_012 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_020 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_004 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_013 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_016 | misfire | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored MF-005=0.8 but winner_id=NF-001 score=0.93; candidates_in=14,threshold_miss=False |
| era2_020 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_006 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_011 | misfire | misfire | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-009 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| CSV-001 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| CSV-005 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| CSV-127 | no_fault | catalyst_failure | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| CSV-128 | no_fault | catalyst_failure | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| EXT-216 | no_fault | rich_mixture | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=WIDEBAND_OFFSET_CANDIDATE,dtc=['P0172']; no expected rule scored; rank winner_id=RM-001 |
| EXT-220 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=7,threshold_miss=False |
| EXT-231 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| PDF-HI-005 | no_fault | sensor_fault | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| PDF-HI-010 | no_fault | sensor_fault | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| YAML-CSV1 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| YAML-CSV5 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| YAML-PDF_HI_005 | no_fault | ecu_fault | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=EF-004 |
| YAML-PDF_HI_010 | no_fault | catalyst_failure | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:co2; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| YAML-TC1 | no_fault | ecu_fault | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=EF-004 |
| case_014 | no_fault | sensor_fault | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| case_028 | no_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored NF-001=0.93 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| era3_014 | no_fault | catalyst_failure | obdlab | DATA_GAP | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=['P0507']; no expected rule scored; rank winner_id=CF-001 |
| REAL-001 | non_starter | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned NS-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=IGNITION_MISFIRE; rank winner_id=MF-001 |
| REAL-003 | non_starter | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned NS-002 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=LEAN_MIXTURE; rank winner_id=MF-001 |
| case_006 | non_starter | invalid_input | rank | OUTRANKED | trace.phase.rank rule_scored NS-004=0.75 but winner_id=II-002 score=0.95; candidates_in=19,threshold_miss=False |
| case_007 | non_starter | misfire | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned NS-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=INCOMPLETE_COMBUSTION; rank winner_id=MF-001 |
| case_040 | non_starter | invalid_input | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned NS-001 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=IGNITION_MISFIRE; rank winner_id=II-002 |
| CASE-023 | rich_mixture | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=RICH_MIXTURE; rank winner_id=CF-001 |
| CASE-025 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-029 | rich_mixture | lean_condition | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=LEAN_MIXTURE lacks required=RICH_MIXTURE; rank winner_id=LC-001 |
| CASE-031 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-037 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| CASE-040 | rich_mixture | no_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=TIMING_RETARDED lacks required=RICH_MIXTURE; rank winner_id=NF-001 |
| CSV-018 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N003 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N010 | rich_mixture | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored RM-001=0.9 but winner_id=CF-001 score=0.9; candidates_in=16,threshold_miss=False |
| EXP-N013 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXP-N027 | rich_mixture | misfire | rank | OUTRANKED | trace.phase.rank expected_family rule_scored RM-001=0.9 but winner_id=MF-001 score=0.9500000000000001; candidates_in=20,threshold_miss=False |
| EXT-203 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXT-206 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-217 | rich_mixture | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=RICH_MIXTURE; rank winner_id=CF-001 |
| EXT-227 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-240 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| PDF-4G-03 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| PDF-HI-001 | rich_mixture | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=GDI_HPFP_INTERNAL_SEAL_LEAK lacks required=RICH_MIXTURE; rank winner_id=SF-002 |
| RULE-CO-1 | rich_mixture | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=VVT_FAILURE lacks required=RICH_MIXTURE; rank winner_id=CF-001 |
| YAML-CSV18 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-PDF_4G_03 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| YAML-PDF_HI_001 | rich_mixture | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=GDI_HPFP_INTERNAL_SEAL_LEAK lacks required=RICH_MIXTURE; rank winner_id=SF-001 |
| YAML-TC12 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_002 | rich_mixture | sensor_fault | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=SAMPLE_INVALID lacks required=RICH_MIXTURE; rank winner_id=SF-001 |
| case_015 | rich_mixture | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=VVT_FAILURE lacks required=RICH_MIXTURE; rank winner_id=CF-001 |
| case_017 | rich_mixture | catalyst_failure | gaslab | PRODUCER_GAP | trace.phase.prune rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks required=RICH_MIXTURE; rank winner_id=CF-001 |
| case_023 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,demotion_note_contains |
| era1_003 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_009 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_013 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era1_014 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_002 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_009 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_019 | rich_mixture | misfire | gaslab | PRODUCER_GAP | trace.phase.prune expected_family rule_pruned RM-003 reason=chemistry failed_gating_key=gas_lab_state; upstream gas=INCOMPLETE_COMBUSTION lacks expected required=RICH_MIXTURE; rank winner_id=MF-001 |
| era3_001 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era3_005 | rich_mixture | catalyst_failure | rank | OUTRANKED | trace.phase.rank expected_family rule_scored RM-001=0.9 but winner_id=CF-001 score=0.9; candidates_in=15,threshold_miss=False |
| era3_017 | rich_mixture | rich_mixture | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-010 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| CASE-014 | sensor_fault | lean_condition | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-008=0.81 but winner_id=LC-001 score=0.9; candidates_in=13,threshold_miss=False |
| CASE-022 | sensor_fault | lean_condition | rank | OUTRANKED | trace.phase.rank rule_scored SF-004=0.77 but winner_id=LC-001 score=1; candidates_in=19,threshold_miss=False |
| CASE-045 | sensor_fault | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| CASE-048 | sensor_fault | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| CSV-025 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored SF-008=0.8600000000000001 but winner_id=NF-001 score=0.93; candidates_in=18,threshold_miss=False |
| EXP-N006 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |
| EXP-N015 | sensor_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored SF-002=0.95 but winner_id=CF-001 score=0.9500000000000001; candidates_in=16,threshold_miss=False |
| EXP-N020 | sensor_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-008=0.8600000000000001 but winner_id=RM-001 score=0.9500000000000001; candidates_in=13,threshold_miss=False |
| EXP-N028 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| EXT-219 | sensor_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank rule_scored SF-004=0.8 but winner_id=RM-001 score=1; candidates_in=18,threshold_miss=False |
| EXT-229 | sensor_fault | lean_condition | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-008=0.81 but winner_id=LC-001 score=0.9; candidates_in=13,threshold_miss=False |
| EXT-230 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-005=0.7000000000000001 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| TC-046 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank rule_scored SF-008=0.8600000000000001 but winner_id=NF-001 score=0.93; candidates_in=18,threshold_miss=False |
| YAML-CSV25 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-005=0.7000000000000001 but winner_id=NF-001 score=0.93; candidates_in=12,threshold_miss=False |
| YAML-TC46 | sensor_fault | misfire | dtc | DATA_GAP | trace.phase.prune rule_pruned SF-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-005 |
| case_004 | sensor_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored SF-006=0.65 but winner_id=CF-001 score=0.9; candidates_in=17,threshold_miss=False |
| case_009 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| case_046 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-005=0.7500000000000001 but winner_id=NF-001 score=0.93; candidates_in=15,threshold_miss=False |
| era1_006 | sensor_fault | no_fault | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-005=0.7500000000000001 but winner_id=NF-001 score=0.93; candidates_in=14,threshold_miss=False |
| era1_017 | sensor_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored SF-005=0.7000000000000001 but winner_id=CF-001 score=0.9; candidates_in=12,threshold_miss=False |
| era2_005 | sensor_fault | rich_mixture | rank | OUTRANKED | trace.phase.rank expected_family rule_scored SF-008=0.8600000000000001 but winner_id=RM-001 score=0.9500000000000001; candidates_in=15,threshold_miss=False |
| era2_010 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence |
| era2_012 | sensor_fault | catalyst_failure | rank | OUTRANKED | trace.phase.rank rule_scored SF-005=0.7000000000000001 but winner_id=CF-001 score=0.9; candidates_in=19,threshold_miss=False |
| era3_004 | sensor_fault | sensor_fault | surface | SURFACE_DEFECT | run.dimensions fault_family=PASS,state=PASS; non-routing fails=fault_code,confidence,perception_gap |

## Bottom line for v3

The dominant measured failure mode is not one thing:

- **133/294** rows are not routing failures at all; they are surface/accounting failures after family+state passed.
- **107/294** rows are `OUTRANKED`; the expected family reached rank but lost to a louder neighbor.
- **25/294** rows are `PRODUCER_GAP`; GASLab did not emit the required state for the expected rule.
- **19/294** rows are `DATA_GAP`; the necessary discriminating OBD/DTC/input evidence is absent from the row.
- **10/294** rows are `ORACLE_SUSPECT`; v3 should repin them or require new mechanical discriminators before treating them as engine misses.
