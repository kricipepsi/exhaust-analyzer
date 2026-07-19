# V3_PRODUCER_GAP_SPLIT_2026-06-30 — T-V3-D2

## Summary

- Total PRODUCER_GAP cases: **25 / 25**.
- `CLASSIFIER_FIXABLE`: **2**.
- `SIGNAL_REQUIRED`: **23**.
- Method: replay each raw v7 row through GASLab/OBDLab query mode, then compare the required GASLab gating state against the row's actual chemistry thresholds.
- Source lock: frozen `FL_LOCALIZATION_2026-06-30` + `FL_UPSTREAM_2026-06-30`; no lab, engine, oracle, CSV, graph, or Vault edits.

## Research-cluster demand

| Research cluster | SIGNAL_REQUIRED cases |
| --- | --- |
| Cluster 1 — mechanical vs misfire | 3 |
| Cluster 2 — rich vs catalyst | 11 |
| Cluster 3 — ECU/control fault | 3 |
| Cluster 7 — cam timing / VVT | 2 |
| Cluster 8 — no-start root cause | 4 |

## Per-case split

| case_id | expected_code | expected_family | required_state | emitted_state | verdict | state / threshold evidence | missing quantity | research cluster |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXP-N023 | ERR-CT-005 | cam_timing | NORMAL_OPERATION | SAMPLE_INVALID | SIGNAL_REQUIRED | fails hc=420 in [0,35]; co=0.4 in [0.1,0.2]; co2=13 in [14.5,16]; o2=0.4 in [0,0.35]; lambda=0.941 in [0.998,1.008] (passes nox=75 in [0,100]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | cam/VVT evidence that can separate a real timing fault from chemically non-normal exhaust | Cluster 7 — cam timing / VVT |
| era1_011 | ERR-CT-001 | cam_timing | CAM_TIMING_RETARDED_MAP | INCOMPLETE_COMBUSTION | SIGNAL_REQUIRED | fails co=0.8 in [3.5,7]; co2=11.5 in [8,10.5]; o2=2 in [0,0.5]; nox=40 in [0,10]; lambda=0.998 in [0.75,0.88] (passes hc=650 in [400,1200]); sample_validity=VALID; high-idle present; required state not reachable from row inputs | idle→2500 cam/VVT discriminator satisfying the retarded-MAP rich-normalising vector | Cluster 7 — cam timing / VVT |
| era2_008 | ERR-CT-004 | cam_timing | VVT_FAILURE | SAMPLE_INVALID | CLASSIFIER_FIXABLE | passes required bound signature: hc=420 in [0,20000]; co=0.4 in [0,15]; co2=13 in [0,16]; o2=0.4 in [0,22]; nox=75 in [0,5000]; lambda=0.941 in [0.5,2.5]; sample_validity=INVALID; required state reachable from row inputs | — | — |
| CASE-039 | ERR-EF-002 | ecu_fault | POA_SIGNATURE | EGR_STUCK_OPEN | CLASSIFIER_FIXABLE | passes required bound signature: hc=600 in [500,20000]; co=2.5 in [0,15]; co2=11.5 in [0,14.5]; o2=0.5 in [0,22]; nox=45 in [0,5000]; lambda=0.855 in [0.5,2.5]; sample_validity=VALID; required state reachable from row inputs | — | — |
| CSV-125 | ERR-ECU-001 | ecu_fault | NORMAL_OPERATION | EGR_STUCK_OPEN | SIGNAL_REQUIRED | fails hc=420 in [0,35]; co=1.8 in [0.1,0.2]; co2=13.2 in [14.5,16]; o2=1.3 in [0,0.35]; lambda=0.96 in [0.998,1.008] (passes nox=38 in [0,100]); sample_validity=EXTERNAL_O2_SUSPECT; high-idle absent; required state not reachable from row inputs | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| CSV-126 | ERR-ECU-001 | ecu_fault | NORMAL_OPERATION | EGR_STUCK_OPEN | SIGNAL_REQUIRED | fails hc=450 in [0,35]; co=2 in [0.1,0.2]; co2=13 in [14.5,16]; o2=1.5 in [0,0.35]; lambda=0.961 in [0.998,1.008] (passes nox=35 in [0,100]); sample_validity=EXTERNAL_O2_SUSPECT; high-idle absent; required state not reachable from row inputs | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| YAML-RULE_NOx_1 | ERR-ECU-001 | ecu_fault | NORMAL_OPERATION | VVT_FAILURE | SIGNAL_REQUIRED | fails hc=100 in [0,35]; co=0.5 in [0.1,0.2]; co2=13 in [14.5,16]; o2=1 in [0,0.35]; nox=500 in [0,100]; lambda=1.04 in [0.998,1.008]; sample_validity=VALID; high-idle absent; required state not reachable from row inputs | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| CSV-117 | ERR-MW-004 | mechanical_wear | WORN_VALVE_SEALS | EGR_STUCK_OPEN | SIGNAL_REQUIRED | fails hc=950 in [75,250]; co=0.6 in [0,0.5]; o2=1.4 in [0,0.5]; lambda=0.918 in [0.97,1.03] (passes co2=12.5 in [11,14.5]; nox=70 in [0,100]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | mechanical-wear high-idle/transient HC discriminator | Cluster 1 — mechanical vs misfire |
| EXP-N030 | ERR-MW-002 | mechanical_wear | COOLANT_LEAK_INTERNAL | GDI_HPFP_INTERNAL_SEAL_LEAK | SIGNAL_REQUIRED | fails co=4.5 in [0,0.5]; lambda=0.774 in [1,2.5] (passes hc=800 in [300,20000]; co2=11 in [0,12]; o2=0.3 in [0,22]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | positive block-test / coolant-combustion marker | Cluster 1 — mechanical vs misfire |
| MECH-001 | ERR-MW-003 | mechanical_wear | WORN_PISTON_RINGS | EGR_STUCK_OPEN | SIGNAL_REQUIRED | fails hc=1.2e+03 in [0,100]; co=0.8 in [0,0.5]; co2=13.5 in [14.5,16]; o2=1.2 in [0,0.5]; lambda=0.873 in [0.97,1.03] (passes nox=80 in [0,100]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | mechanical-wear high-idle/load HC discriminator | Cluster 1 — mechanical vs misfire |
| REAL-001 | ERR-NS-001 | non_starter | IGNITION_MISFIRE | SAMPLE_INVALID | SIGNAL_REQUIRED | fails lambda=0.397 in [1,2.5] (passes hc=2e+04 in [1000,20000]; co=0.006 in [0,0.5]; co2=0.16 in [0,10]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | non-starter cranking/misfire evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| REAL-003 | ERR-NS-003 | non_starter | LEAN_MIXTURE | SAMPLE_INVALID | SIGNAL_REQUIRED | fails hc=2e+04 in [0,300]; co=3.24 in [0,0.1]; lambda=0.318 in [1.05,2.5] (passes co2=1.16 in [0,13]; o2=14.5 in [2.5,22]; nox=30 in [0,5000]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | non-starter live OBD/fuel-air evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| case_007 | ERR-NS-004 | non_starter | INCOMPLETE_COMBUSTION | SAMPLE_INVALID | SIGNAL_REQUIRED | fails co=0.02 in [0.5,5]; lambda=4.19 in [0.97,1.5] (passes hc=300 in [200,20000]; co2=4 in [0,13]; o2=16 in [0,22]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | non-starter combustion/no-combustion evidence beyond invalid sample | Cluster 8 — no-start root cause |
| case_040 | ERR-NS-001 | non_starter | IGNITION_MISFIRE | SAMPLE_INVALID | SIGNAL_REQUIRED | fails hc=0 in [1000,20000]; lambda=523 in [1,2.5] (passes co=0 in [0,0.5]; co2=0.04 in [0,10]; o2=20.9 in [3,22]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | non-starter cranking/misfire evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| CASE-023 | ERR-RM-006 | rich_mixture | RICH_MIXTURE | INCOMPLETE_COMBUSTION | SIGNAL_REQUIRED | fails lambda=0.975 in [0.5,0.97] (passes hc=220 in [0,300]; co=0.6 in [0.5,15]; co2=13 in [0,13]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| CASE-029 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | LEAN_MIXTURE | SIGNAL_REQUIRED | fails co=0.03 in [0.5,15]; o2=4 in [0,1]; nox=280 in [0,100]; lambda=1.32 in [0.5,0.97] (passes hc=80 in [0,300]; co2=11.5 in [0,13]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| CASE-040 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | TIMING_RETARDED | SIGNAL_REQUIRED | fails co=0.06 in [0.5,15]; co2=15.2 in [0,13]; lambda=1.01 in [0.5,0.97] (passes hc=12 in [0,300]; o2=0.2 in [0,1]; nox=22 in [0,100]); sample_validity=VALID; high-idle present; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| EXT-217 | ERR-RM-006 | rich_mixture | RICH_MIXTURE | INCOMPLETE_COMBUSTION | SIGNAL_REQUIRED | fails lambda=0.975 in [0.5,0.97] (passes hc=220 in [0,300]; co=0.6 in [0.5,15]; co2=13 in [0,13]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| PDF-HI-001 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | GDI_HPFP_INTERNAL_SEAL_LEAK | SIGNAL_REQUIRED | fails hc=650 in [0,300] (passes co=4 in [0.5,15]; co2=11 in [0,13]; o2=0.3 in [0,1]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| RULE-CO-1 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | VVT_FAILURE | SIGNAL_REQUIRED | fails nox=500 in [0,100]; lambda=1.02 in [0.5,0.97] (passes hc=100 in [0,300]; co=1 in [0.5,15]; co2=13 in [0,13]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| YAML-PDF_HI_001 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | GDI_HPFP_INTERNAL_SEAL_LEAK | SIGNAL_REQUIRED | fails hc=650 in [0,300] (passes co=4 in [0.5,15]; co2=11 in [0,13]; o2=0.3 in [0,1]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_002 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | SAMPLE_INVALID | SIGNAL_REQUIRED | fails hc=450 in [0,300]; o2=1.2 in [0,1] (passes co=2.1 in [0.5,15]; co2=10.5 in [0,13]; nox=80 in [0,100]); sample_validity=INVALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_015 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | VVT_FAILURE | SIGNAL_REQUIRED | fails co2=13.5 in [0,13]; nox=300 in [0,100]; lambda=1.04 in [0.5,0.97] (passes hc=80 in [0,300]; co=0.5 in [0.5,15]; o2=1 in [0,1]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_017 | ERR-RM-003 | rich_mixture | RICH_MIXTURE | INCOMPLETE_COMBUSTION | SIGNAL_REQUIRED | fails lambda=0.982 in [0.5,0.97] (passes hc=200 in [0,300]; co=1.5 in [0.5,15]; co2=12 in [0,13]); sample_validity=VALID; high-idle absent; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| era2_019 | ERR-RM-004 | rich_mixture | RICH_MIXTURE | INCOMPLETE_COMBUSTION | SIGNAL_REQUIRED | fails lambda=0.991 in [0.5,0.97] (passes hc=250 in [0,300]; co=0.6 in [0.5,15]; co2=13 in [0,13]); sample_validity=VALID; high-idle present; required state not reachable from row inputs | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |

## Classifier-fixable cases

| case_id | required_state | emitted_state | bound candidates | resolved candidates | evidence |
| --- | --- | --- | --- | --- | --- |
| era2_008 | VVT_FAILURE | SAMPLE_INVALID | VVT_FAILURE | VVT_FAILURE | passes required bound signature: hc=420 in [0,20000]; co=0.4 in [0,15]; co2=13 in [0,16]; o2=0.4 in [0,22]; nox=75 in [0,5000]; lambda=0.941 in [0.5,2.5]; sample_validity=INVALID; required state reachable from row inputs |
| CASE-039 | POA_SIGNATURE | EGR_STUCK_OPEN | POA_SIGNATURE, EGR_STUCK_OPEN, VVT_FAILURE, INCOMPLETE_OXIDATION | POA_SIGNATURE, EGR_STUCK_OPEN, VVT_FAILURE, INCOMPLETE_OXIDATION | passes required bound signature: hc=600 in [500,20000]; co=2.5 in [0,15]; co2=11.5 in [0,14.5]; o2=0.5 in [0,22]; nox=45 in [0,5000]; lambda=0.855 in [0.5,2.5]; sample_validity=VALID; required state reachable from row inputs |

## Signal-required cases

| case_id | required_state | missing physical quantity | research cluster |
| --- | --- | --- | --- |
| EXP-N023 | NORMAL_OPERATION | cam/VVT evidence that can separate a real timing fault from chemically non-normal exhaust | Cluster 7 — cam timing / VVT |
| era1_011 | CAM_TIMING_RETARDED_MAP | idle→2500 cam/VVT discriminator satisfying the retarded-MAP rich-normalising vector | Cluster 7 — cam timing / VVT |
| CSV-125 | NORMAL_OPERATION | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| CSV-126 | NORMAL_OPERATION | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| YAML-RULE_NOx_1 | NORMAL_OPERATION | ECU/control evidence with chemically normal exhaust | Cluster 3 — ECU/control fault |
| CSV-117 | WORN_VALVE_SEALS | mechanical-wear high-idle/transient HC discriminator | Cluster 1 — mechanical vs misfire |
| EXP-N030 | COOLANT_LEAK_INTERNAL | positive block-test / coolant-combustion marker | Cluster 1 — mechanical vs misfire |
| MECH-001 | WORN_PISTON_RINGS | mechanical-wear high-idle/load HC discriminator | Cluster 1 — mechanical vs misfire |
| REAL-001 | IGNITION_MISFIRE | non-starter cranking/misfire evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| REAL-003 | LEAN_MIXTURE | non-starter live OBD/fuel-air evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| case_007 | INCOMPLETE_COMBUSTION | non-starter combustion/no-combustion evidence beyond invalid sample | Cluster 8 — no-start root cause |
| case_040 | IGNITION_MISFIRE | non-starter cranking/misfire evidence beyond ambient-air sample | Cluster 8 — no-start root cause |
| CASE-023 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| CASE-029 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| CASE-040 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| EXT-217 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| PDF-HI-001 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| RULE-CO-1 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| YAML-PDF_HI_001 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_002 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_015 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| case_017 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
| era2_019 | RICH_MIXTURE | rich-mixture discriminator not present in the single idle chemistry row | Cluster 2 — rich vs catalyst |
