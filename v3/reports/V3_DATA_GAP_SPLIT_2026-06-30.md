# V3_DATA_GAP_SPLIT_2026-06-30 — T-V3-D3

## Summary

- Total DATA_GAP cases: **19 / 19**.
- `CORPUS_FILL`: **0**.
- `ACQUISITION_GAP`: **19**.
- Method: compare the frozen DATA_GAP list against the current corpus row and the v7 owner-fill queue.
- Source lock: frozen `FL_LOCALIZATION_2026-06-30` + `FL_UPSTREAM_2026-06-30`; no corpus, lab, engine, oracle, graph, or Vault edits.
- Owner-fill cross-check: no exact DATA_GAP case id is already present in the v7 owner action queue; all 19 are acquisition-scope until the owner confirms an out-of-tree source row has the missing signal.

## Research-cluster demand

| Research cluster | ACQUISITION_GAP cases |
| --- | --- |
| Cluster 5 — lean-condition root cause | 5 |
| Cluster 6 — sensor fault under-detection | 3 |
| Cluster 8 — non-starter | 1 |
| Cluster 9 — confirming no-fault reliably | 10 |

## Per-case split

| case_id | expected_code | expected_family | predicted_family | failed gating key | verdict | missing input | source ref | action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-N011 | ERR-LC-001 | lean_condition | sensor_fault | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:EXP-N011 | Phase-4 acquisition: Cluster 5 — lean-condition root cause. |
| EXP-N022 | ERR-LC-001 | lean_condition | catalyst_failure | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:EXP-N022 | Phase-4 acquisition: Cluster 5 — lean-condition root cause. |
| EXP-N029 | ERR-LC-001 | lean_condition | mechanical_wear | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:EXP-N029 | Phase-4 acquisition: Cluster 5 — lean-condition root cause. |
| REAL-002 | ERR-LC-003 | lean_condition | misfire | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:REAL-002 | Phase-4 acquisition: Cluster 8 — non-starter. |
| case_003 | ERR-LC-001 | lean_condition | catalyst_failure | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:case_003 | Phase-4 acquisition: Cluster 5 — lean-condition root cause. |
| case_016 | ERR-LC-001 | lean_condition | catalyst_failure | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:case_016 | Phase-4 acquisition: Cluster 5 — lean-condition root cause. |
| CSV-127 | OPTIMAL_HEALTH | no_fault | catalyst_failure | obd:hc | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases/cases_petrol_master_v5.csv:CSV-127 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| CSV-128 | OPTIMAL_HEALTH | no_fault | catalyst_failure | obd:hc | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases/cases_petrol_master_v5.csv:CSV-128 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| EXT-216 | OPTIMAL_HEALTH | no_fault | rich_mixture | obd:hc | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases/cases_petrol_master_v5.csv:EXT-216 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| PDF-HI-005 | OPTIMAL_HEALTH | no_fault | sensor_fault | obd:obd_lambda | ACQUISITION_GAP | OBD lambda / sensor-dynamics evidence bundle | cases/cases_petrol_master_v5.csv:PDF-HI-005 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| PDF-HI-010 | OPTIMAL_HEALTH | no_fault | sensor_fault | obd:obd_lambda | ACQUISITION_GAP | OBD lambda / sensor-dynamics evidence bundle | cases/cases_petrol_master_v5.csv:PDF-HI-010 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| YAML-PDF_HI_005 | OPTIMAL_HEALTH | no_fault | ecu_fault | obd:obd_lambda | ACQUISITION_GAP | OBD lambda / sensor-dynamics evidence bundle | cases/cases_petrol_master_v5.csv:YAML-PDF_HI_005 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| YAML-PDF_HI_010 | OPTIMAL_HEALTH | no_fault | catalyst_failure | obd:co2 | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases/cases_petrol_master_v5.csv:YAML-PDF_HI_010 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| YAML-TC1 | OPTIMAL_HEALTH | no_fault | ecu_fault | obd:obd_lambda | ACQUISITION_GAP | OBD lambda / sensor-dynamics evidence bundle | cases/cases_petrol_master_v5.csv:YAML-TC1 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| case_014 | OPTIMAL_HEALTH | no_fault | sensor_fault | obd:hc | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases/cases_petrol_master_v5.csv:case_014 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| era3_014 | OPTIMAL_HEALTH | no_fault | catalyst_failure | obd:hc | ACQUISITION_GAP | OBD no-fault evidence bundle (not a current v7 CSV scalar column) | cases_petrol_era_v1.csv:era3_014 | Phase-4 acquisition: Cluster 9 — confirming no-fault reliably. |
| CASE-045 | ERR-SF-005 | sensor_fault | misfire | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:CASE-045 | Phase-4 acquisition: Cluster 6 — sensor fault under-detection. |
| CASE-048 | ERR-SF-005 | sensor_fault | misfire | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:CASE-048 | Phase-4 acquisition: Cluster 6 — sensor fault under-detection. |
| YAML-TC46 | ERR-SF-001 | sensor_fault | misfire | no_evidence_satisfied | ACQUISITION_GAP | rule-specific corroborating OBD/DTC evidence | cases/cases_petrol_master_v5.csv:YAML-TC46 | Phase-4 acquisition: Cluster 6 — sensor fault under-detection. |

## CORPUS_FILL cases

No `CORPUS_FILL` cases. Exact DATA_GAP case ids do not appear in the v7 owner-fill queue; do not file duplicate owner-fill rows from this task.

## ACQUISITION_GAP cases

| case_id | missing physical quantity | research cluster | source confirmation |
| --- | --- | --- | --- |
| EXP-N011 | live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load | Cluster 5 — lean-condition root cause | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| EXP-N022 | live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load | Cluster 5 — lean-condition root cause | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| EXP-N029 | live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load | Cluster 5 — lean-condition root cause | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| REAL-002 | cranking fuel-pressure / injector-pulse / spark evidence; a warm-idle gas row cannot separate no-start roots | Cluster 8 — non-starter | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| case_003 | live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load | Cluster 5 — lean-condition root cause | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| case_016 | live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load | Cluster 5 — lean-condition root cause | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| CSV-127 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| CSV-128 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| EXT-216 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| PDF-HI-005 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| PDF-HI-010 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| YAML-PDF_HI_005 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| YAML-PDF_HI_010 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| YAML-TC1 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| case_014 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| era3_014 | OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, sensor dynamics nominal | Cluster 9 — confirming no-fault reliably | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| CASE-045 | O2/MAF sensor dynamics or plausibility evidence: switch rate, forced rich-lean response, heater/circuit DTC, or Mode 06 sensor monitor | Cluster 6 — sensor fault under-detection | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| CASE-048 | O2/MAF sensor dynamics or plausibility evidence: switch rate, forced rich-lean response, heater/circuit DTC, or Mode 06 sensor monitor | Cluster 6 — sensor fault under-detection | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |
| YAML-TC46 | O2/MAF sensor dynamics or plausibility evidence: switch rate, forced rich-lean response, heater/circuit DTC, or Mode 06 sensor monitor | Cluster 6 — sensor fault under-detection | owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports confirm only the populated inputs used here |

## Evidence detail

| case_id | populated evidence | localization evidence |
| --- | --- | --- |
| EXP-N011 | gas hc=180, co=0.15, co2=13.5, o2=1.5, nox=90, lambda=1.02; shrtft1=0.0, longft1=0.0, o2_pid=1.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| EXP-N022 | gas hc=110, co=0.2, co2=11.5, o2=0.5, nox=70, lambda=1.0; shrtft1=0.0, longft1=0.0, o2_pid=1.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| EXP-N029 | gas hc=200, co=0.4, co2=13.5, o2=0.5, nox=65, lambda=1.01; shrtft1=1.0, longft1=0.0, o2_pid=1.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=MW-002 |
| REAL-002 | gas hc=2937, co=0.025, co2=2.98, o2=16.75, nox=141, lambda=2.0; shrtft1=0.0, longft1=0.0, o2_pid=0.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-002 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| case_003 | gas hc=80, co=0.05, co2=13.5, o2=2.8, nox=350, lambda=1.06; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| case_016 | gas hc=30, co=0.05, co2=14.0, o2=0.8, nox=1200, lambda=1.03; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned LC-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| CSV-127 | gas hc=180, co=0.45, co2=13.8, o2=0.55, nox=45, lambda=0.99; shrtft1=8.0, longft1=0.0, o2_pid=0.99, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| CSV-128 | gas hc=220, co=0.5, co2=13.5, o2=0.6, nox=50, lambda=0.98; shrtft1=10.0, longft1=0.0, o2_pid=0.98, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| EXT-216 | gas hc=650, co=5.5, co2=11.0, o2=0.2, nox=15, lambda=0.82; shrtft1=-25.0, longft1=-25.0, o2_pid=0.78, dtc=["P0172"], obd_o2=WIDEBAND_OFFSET_CANDIDATE | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=WIDEBAND_OFFSET_CANDIDATE,dtc=['P0172']; no expected rule scored; rank winner_id=RM-001 |
| PDF-HI-005 | gas hc=15, co=0.1, co2=15.2, o2=0.3, nox=30, lambda=1.001; shrtft1=0.0, longft1=0.0, o2_pid=0.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| PDF-HI-010 | gas hc=12, co=0.08, co2=15.3, o2=0.25, nox=20, lambda=1.01; shrtft1=0.0, longft1=0.0, o2_pid=0.0, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| YAML-PDF_HI_005 | gas hc=15, co=0.01, co2=14.8, o2=0.3, nox=0, lambda=1.001; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=EF-004 |
| YAML-PDF_HI_010 | gas hc=30, co=0.12, co2=14.0, o2=0.5, nox=300, lambda=1.01; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:co2; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=CF-001 |
| YAML-TC1 | gas hc=12, co=0.1, co2=15.2, o2=0.3, nox=0, lambda=1.0; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:obd_lambda; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=EF-004 |
| case_014 | gas hc=55, co=0.3, co2=12.0, o2=2.0, nox=150, lambda=1.0; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=[]; no expected rule scored; rank winner_id=SF-002 |
| era3_014 | gas hc=180, co=0.3, co2=13.5, o2=0.6, nox=45, lambda=1.01; shrtft1=0.0, longft1=0.0, o2_pid=1.0, dtc=["P0507"], obd_o2=NO_FAULT | trace.phase.prune rule_pruned NF-001 reason=missing_evidence failed_gating_key=obd:hc; upstream obd_o2=NO_FAULT,dtc=['P0507']; no expected rule scored; rank winner_id=CF-001 |
| CASE-045 | gas hc=1200, co=4.5, co2=12.5, o2=3.5, nox=20, lambda=; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| CASE-048 | gas hc=200, co=0.5, co2=14.0, o2=1.5, nox=40, lambda=; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned SF-005 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-001 |
| YAML-TC46 | gas hc=20, co=0.1, co2=15.0, o2=0.2, nox=0, lambda=1.0056; shrtft1=blank, longft1=blank, o2_pid=blank, dtc=[], obd_o2=NOT_RUN_NO_OBD_INPUT | trace.phase.prune rule_pruned SF-001 reason=missing_evidence failed_gating_key=no_evidence_satisfied; upstream obd_o2=NOT_RUN_NO_OBD_INPUT,dtc=[]; no expected rule scored; rank winner_id=MF-005 |

