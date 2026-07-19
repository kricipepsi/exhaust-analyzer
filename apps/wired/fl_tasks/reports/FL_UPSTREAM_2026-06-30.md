# FL_UPSTREAM_2026-06-30 — per-case upstream GASLab/OBDLab evidence

**Task:** [[T-FL-2_capture_upstream_evidence]]  
**Mode:** read-only measurement; no engine/lab/oracle/wiki/source edits.  
**Consumer:** [[T-FL-3_classify_failure_modes]].

## Method

This harness replays the exact per-row sanitized inputs produced by `apps/wired/v7/load_corpus.py::row_to_raw_inputs()` through the same wired composition seam helpers used by `diagnose()`: `_run_gaslab()` and `_run_obdlab()`. It does not change the final engine schema; it captures the upstream lab states that the final `OrchestratorFinalUIOutput` omits. The live-pipeline proof uses in-memory OpenTelemetry, calls public `diagnose()`, and reads the COMLab `phase.prune` span events.

## Coverage

| Metric | Value |
|---|---|
| Total corpus rows | 314 |
| GASLab chemistry states captured | 314/314 |
| OBDLab O2 mode/status field populated | 314/314 |

## Live-pipeline spot checks

| case_id | expected family | expected code | emitted GASLab state | required state | phase.prune spans | pruned rule | prune reason | failed gating key |
|---|---|---|---|---|---|---|---|---|
| era1_002 | mechanical_wear | ERR-MW-002 | RICH_MISFIRE | COOLANT_LEAK_INTERNAL | 1 | MW-002 | chemistry | gas_lab_state |
| era3_019 | exhaust_leak | ERR-EL-002 | VVT_FAILURE | EXHAUST_AIR_LEAK | 1 | EL-002 | missing_evidence | no_evidence_satisfied |
| REAL-001 | non_starter | ERR-NS-001 | SAMPLE_INVALID | IGNITION_MISFIRE | 1 | NS-001 | chemistry | gas_lab_state |

## Dead-family emitted-vs-required summary

| Expected family | Emitted GASLab states | Registry-required GASLab states |
|---|---|---|
| mechanical_wear | EGR_STUCK_OPEN=4, GDI_HPFP_INTERNAL_SEAL_LEAK=1, IGNITION_MISFIRE=1, INCOMPLETE_COMBUSTION=1, INCOMPLETE_OXIDATION=1, POA_SIGNATURE=1, RICH_MISFIRE=5 | COOLANT_LEAK_INTERNAL, IGNITION_MISFIRE, INCOMPLETE_COMBUSTION, POA_SIGNATURE, WORN_ENGINE, WORN_PISTON_RINGS, WORN_VALVE_SEALS |
| exhaust_leak | LEAN_MIXTURE=1, SAMPLE_INVALID=7, VVT_FAILURE=2 | EXHAUST_AIR_LEAK, INCOMPLETE_COMBUSTION, NORMAL_OPERATION, SAMPLE_INVALID |
| non_starter | SAMPLE_INVALID=5 | IGNITION_MISFIRE, INCOMPLETE_COMBUSTION, LEAN_MIXTURE, NORMAL_OPERATION, SAMPLE_INVALID |

## Dead-family case rows

| case_id | expected family | expected code | predicted family | emitted GASLab state | required state for expected code | OBDLab O2 mode |
|---|---|---|---|---|---|---|
| era1_002 | mechanical_wear | ERR-MW-002 | misfire | RICH_MISFIRE | COOLANT_LEAK_INTERNAL | NO_FAULT |
| era1_015 | mechanical_wear | ERR-MW-003 | misfire | INCOMPLETE_OXIDATION | WORN_PISTON_RINGS | NO_FAULT |
| era1_016 | exhaust_leak | ERR-EL-001 | lean_condition | VVT_FAILURE | EXHAUST_AIR_LEAK | NO_FAULT |
| era3_019 | exhaust_leak | ERR-EL-002 | lean_condition | VVT_FAILURE | EXHAUST_AIR_LEAK | NO_FAULT |
| CSV-095 | exhaust_leak | ERR-EL-001 | lean_condition | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| CSV-117 | mechanical_wear | ERR-MW-004 | sensor_fault | EGR_STUCK_OPEN | WORN_VALVE_SEALS | NO_FAULT |
| CSV-118 | mechanical_wear | ERR-MW-004 | misfire | EGR_STUCK_OPEN | WORN_VALVE_SEALS | NO_FAULT |
| CSV-119 | mechanical_wear | ERR-MW-002 | misfire | RICH_MISFIRE | COOLANT_LEAK_INTERNAL | WIDEBAND_OFFSET_CANDIDATE |
| CSV-120 | mechanical_wear | ERR-MW-002 | misfire | IGNITION_MISFIRE | COOLANT_LEAK_INTERNAL | WIDEBAND_OFFSET_CANDIDATE |
| CSV-129 | exhaust_leak | ERR-EL-005 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| CSV-130 | exhaust_leak | ERR-EL-005 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| EXP-N030 | mechanical_wear | ERR-MW-002 | lean_condition | GDI_HPFP_INTERNAL_SEAL_LEAK | COOLANT_LEAK_INTERNAL | WIDEBAND_OFFSET_CANDIDATE |
| EXT-222 | mechanical_wear | ERR-MW-005 | misfire | INCOMPLETE_COMBUSTION | INCOMPLETE_COMBUSTION | WIDEBAND_OFFSET_CANDIDATE |
| EXT-223 | mechanical_wear | ERR-MW-003 | misfire | EGR_STUCK_OPEN | WORN_PISTON_RINGS | NO_FAULT |
| EXT-224 | mechanical_wear | ERR-MW-002 | misfire | RICH_MISFIRE | COOLANT_LEAK_INTERNAL | WIDEBAND_OFFSET_CANDIDATE |
| EXT-238 | exhaust_leak | ERR-EL-005 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| EXT-239 | exhaust_leak | ERR-EL-005 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| MECH-001 | mechanical_wear | ERR-MW-003 | sensor_fault | EGR_STUCK_OPEN | WORN_PISTON_RINGS | NO_FAULT |
| MECH-002 | mechanical_wear | ERR-MW-002 | misfire | RICH_MISFIRE | COOLANT_LEAK_INTERNAL | WIDEBAND_OFFSET_CANDIDATE |
| MECH-006 | mechanical_wear | ERR-MW-005 | misfire | RICH_MISFIRE | INCOMPLETE_COMBUSTION | WIDEBAND_OFFSET_CANDIDATE |
| PDF-HI-007 | exhaust_leak | ERR-EL-001 | lean_condition | LEAN_MIXTURE | EXHAUST_AIR_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| REAL-001 | non_starter | ERR-NS-001 | misfire | SAMPLE_INVALID | IGNITION_MISFIRE | NO_FAULT |
| REAL-003 | non_starter | ERR-NS-003 | misfire | SAMPLE_INVALID | LEAN_MIXTURE | NO_FAULT |
| TC-048 | exhaust_leak | ERR-EL-001 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| YAML-CSV95 | exhaust_leak | ERR-EL-001 | sensor_fault | SAMPLE_INVALID | EXHAUST_AIR_LEAK | NO_FAULT |
| case_006 | non_starter | ERR-NS-003 | invalid_input | SAMPLE_INVALID | LEAN_MIXTURE | NO_FAULT |
| case_007 | non_starter | ERR-NS-004 | misfire | SAMPLE_INVALID | INCOMPLETE_COMBUSTION | NO_FAULT |
| case_040 | non_starter | ERR-NS-001 | invalid_input | SAMPLE_INVALID | IGNITION_MISFIRE | NO_FAULT |
| case_044 | mechanical_wear | ERR-MW-007 | sensor_fault | POA_SIGNATURE | POA_SIGNATURE | NO_FAULT |

## Per-case upstream evidence

| case_id | tag | expected family | expected code | predicted family | predicted code | gas_chemistry_states[] | obd_o2_failure_mode |
|---|---|---|---|---|---|---|---|
| era1_001 | viable | lean_condition | ERR-LC-005 | misfire | MF-001 | INCOMPLETE_OXIDATION | NO_FAULT |
| era1_002 | viable | mechanical_wear | ERR-MW-002 | misfire | MF-001 | RICH_MISFIRE | NO_FAULT |
| era1_003 | viable | rich_mixture | ERR-RM-007 | rich_mixture | RM-001 | INCOMPLETE_OXIDATION | NO_FAULT |
| era1_004 | viable | misfire | ERR-MF-002 | misfire | MF-001 | VVT_FAILURE | NO_FAULT |
| era1_005 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | VVT_FAILURE | NO_FAULT |
| era1_006 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| era1_007 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | NO_FAULT |
| era1_008 | viable | catalyst_failure | ERR-CF-004 | catalyst_failure | CF-001 | SAMPLE_INVALID | NO_FAULT |
| era1_009 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | EVAP_CANISTER_SATURATED | NO_FAULT |
| era1_011 | viable | cam_timing | ERR-CT-001 | misfire | MF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era1_012 | viable | misfire | ERR-MF-002 | misfire | MF-001 | IGNITION_MISFIRE | NO_FAULT |
| era1_013 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | EVAP_CANISTER_SATURATED | NO_FAULT |
| era1_014 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | VVT_FAILURE | NO_FAULT |
| era1_015 | viable | mechanical_wear | ERR-MW-003 | misfire | MF-001 | INCOMPLETE_OXIDATION | NO_FAULT |
| era1_016 | viable | exhaust_leak | ERR-EL-001 | lean_condition | LC-001 | VVT_FAILURE | NO_FAULT |
| era1_017 | viable | sensor_fault | ERR-SF-005 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| era1_018 | viable | lean_condition | ERR-LC-002 | lean_condition | LC-001 | VVT_FAILURE | NO_FAULT |
| era1_019 | viable | lean_condition | ERR-LC-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| era1_020 | viable | misfire | ERR-MF-004 | misfire | MF-001 | RICH_MISFIRE | NO_FAULT |
| era2_001 | viable | catalyst_failure | ERR-CF-004 | catalyst_failure | CF-001 | SAMPLE_INVALID | NO_FAULT |
| era2_002 | viable | rich_mixture | ERR-RM-004 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| era2_003 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | VVT_FAILURE | NO_FAULT |
| era2_004 | viable | misfire | ERR-MF-002 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| era2_005 | viable | sensor_fault | ERR-SF-001 | rich_mixture | RM-001 | EVAP_CANISTER_SATURATED | NO_FAULT |
| era2_006 | viable | lean_condition | ERR-LC-005 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| era2_008 | viable | cam_timing | ERR-CT-004 | sensor_fault | SF-001 | SAMPLE_INVALID | NO_FAULT |
| era2_009 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| era2_010 | viable | sensor_fault | ERR-SF-004 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| era2_011 | viable | lean_condition | ERR-LC-001 | cam_timing | CT-008 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era2_012 | viable | sensor_fault | ERR-SF-005 | catalyst_failure | CF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era2_013 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| era2_014 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| era2_015 | viable | lean_condition | ERR-LC-001 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| era2_016 | viable | misfire | ERR-MF-008 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| era2_017 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| era2_019 | viable | rich_mixture | ERR-RM-004 | misfire | MF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era2_020 | viable | misfire | ERR-MF-001 | misfire | MF-001 | POA_SIGNATURE | WIDEBAND_OFFSET_CANDIDATE |
| era3_001 | viable | rich_mixture | ERR-RM-005 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| era3_002 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| era3_003 | viable | ignition_fault | ERR-IF-005 | ignition_fault | IF-002 | POA_SIGNATURE | NO_FAULT |
| era3_004 | viable | sensor_fault | ERR-SF-002 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| era3_005 | viable | rich_mixture | ERR-RM-004 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| era3_006 | viable | misfire | ERR-MF-006 | misfire | MF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era3_007 | viable | lean_condition | ERR-LC-005 | catalyst_failure | CF-001 | SAMPLE_INVALID | NO_FAULT |
| era3_008 | viable | lean_condition | ERR-LC-004 | misfire | MF-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| era3_009 | viable | lean_condition | ERR-LC-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| era3_011 | viable | misfire | ERR-MF-006 | misfire | MF-001 | VVT_FAILURE | NO_FAULT |
| era3_013 | viable | lean_condition | ERR-LC-002 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| era3_014 | viable | no_fault | OPTIMAL_HEALTH | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| era3_015 | viable | lean_condition | ERR-LC-001 | misfire | MF-001 | VVT_FAILURE | NO_FAULT |
| era3_016 | viable | lean_condition | ERR-LC-006 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| era3_017 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | EVAP_CANISTER_SATURATED | WIDEBAND_OFFSET_CANDIDATE |
| era3_018 | viable | cam_timing | ERR-CT-002 | cam_timing | CT-008 | INCOMPLETE_COMBUSTION | NO_FAULT |
| era3_019 | viable | exhaust_leak | ERR-EL-002 | lean_condition | LC-001 | VVT_FAILURE | NO_FAULT |
| era3_020 | viable | ecu_fault | ERR-ECU-001 | ecu_fault | EF-004 | TIMING_RETARDED | NO_FAULT |
| CASE-009 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-010 | viable | sensor_fault | ERR-SF-002 | sensor_fault | SF-001 | SAMPLE_INVALID | WIDEBAND_OFFSET_CANDIDATE |
| CASE-011 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-012 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| CASE-013 | viable | catalyst_failure | ERR-CF-003 | lean_condition | LC-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| CASE-014 | viable | sensor_fault | ERR-SF-001 | lean_condition | LC-001 | WORN_PISTON_RINGS | NO_FAULT |
| CASE-015 | viable | catalyst_failure | ERR-CF-005 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-016 | viable | catalyst_failure | ERR-CF-004 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| CASE-017 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-018 | viable | cam_timing | ERR-CT-004 | cam_timing | CT-007 | SAMPLE_INVALID | NO_FAULT |
| CASE-019 | viable | lean_condition | ERR-LC-002 | lean_condition | LC-001 | FLAT_CAMSHAFT | WIDEBAND_OFFSET_CANDIDATE |
| CASE-020 | viable | lean_condition | ERR-LC-005 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CASE-021 | viable | misfire | ERR-MF-009 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| CASE-022 | viable | sensor_fault | ERR-SF-004 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-023 | viable | rich_mixture | ERR-RM-006 | catalyst_failure | CF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| CASE-024 | viable | misfire | ERR-MF-001 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| CASE-025 | viable | rich_mixture | ERR-RM-004 | rich_mixture | RM-001 | TIMING_RETARDED | NO_FAULT |
| CASE-026 | viable | catalyst_failure | ERR-CF-007 | catalyst_failure | CF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-027 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-028 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-029 | viable | rich_mixture | ERR-RM-003 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-030 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | VVT_FAILURE | NO_FAULT |
| CASE-031 | viable | rich_mixture | ERR-RM-005 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-032 | viable | lean_condition | ERR-LC-008 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-033 | viable | misfire | ERR-MF-007 | misfire | MF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CASE-034 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| CASE-035 | viable | ignition_fault | ERR-IF-005 | sensor_fault | SF-001 | SAMPLE_INVALID | NO_FAULT |
| CASE-036 | viable | lean_condition | ERR-LC-004 | lean_condition | LC-001 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| CASE-037 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CASE-038 | viable | misfire | ERR-MF-005 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| CASE-039 | viable | ecu_fault | ERR-EF-002 | sensor_fault | SF-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| CASE-040 | viable | rich_mixture | ERR-RM-003 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CASE-041 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | LEAN_MIXTURE | NOT_RUN_NO_OBD_INPUT |
| CASE-043 | invalid | invalid_input |  | ecu_fault | EF-004 | TIMING_RETARDED | NOT_RUN_NO_OBD_INPUT |
| CASE-045 | viable | sensor_fault | ERR-SF-005 | misfire | MF-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| CASE-046 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| CASE-047 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| CASE-048 | viable | sensor_fault | ERR-SF-005 | misfire | MF-001 | EGR_STUCK_OPEN | NOT_RUN_NO_OBD_INPUT |
| CSV-001 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-005 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-016 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-018 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-022 | viable | misfire | ERR-MF-002 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-025 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-041 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-043 | viable | ecu_fault | ERR-ECU-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| CSV-045 | viable | ecu_fault | ERR-ECU-001 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| CSV-052 | viable | misfire | ERR-MF-008 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| CSV-066 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-068 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| CSV-072 | viable | ecu_fault | ERR-ECU-001 | ecu_fault | EF-004 | NORMAL_OPERATION | NO_FAULT |
| CSV-081 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NO_FAULT |
| CSV-083 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NO_FAULT |
| CSV-095 | viable | exhaust_leak | ERR-EL-001 | lean_condition | LC-001 | SAMPLE_INVALID | NO_FAULT |
| CSV-100 | viable | lean_condition | ERR-LC-001 | rich_mixture | RM-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| CSV-101 | viable | misfire | ERR-MF-002 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| CSV-102 | viable | misfire | ERR-MF-002 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| CSV-103 | viable | misfire | ERR-MF-001 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-104 | viable | misfire | ERR-MF-001 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-105 | viable | misfire | ERR-MF-008 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | NO_FAULT |
| CSV-106 | viable | misfire | ERR-MF-008 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | NO_FAULT |
| CSV-107 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-108 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| CSV-109 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-110 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-111 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-112 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-113 | viable | lean_condition | ERR-LC-005 | misfire | MF-001 | RICH_MISFIRE | NO_FAULT |
| CSV-114 | viable | lean_condition | ERR-LC-005 | misfire | MF-001 | RICH_MISFIRE | NO_FAULT |
| CSV-115 | viable | cam_timing | ERR-CT-001 | cam_timing | CT-007 | INCOMPLETE_COMBUSTION | NO_FAULT |
| CSV-116 | viable | cam_timing | ERR-CT-001 | cam_timing | CT-007 | INCOMPLETE_COMBUSTION | NO_FAULT |
| CSV-117 | viable | mechanical_wear | ERR-MW-004 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CSV-118 | viable | mechanical_wear | ERR-MW-004 | misfire | MF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CSV-119 | viable | mechanical_wear | ERR-MW-002 | misfire | MF-001 | RICH_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-120 | viable | mechanical_wear | ERR-MW-002 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-121 | viable | catalyst_failure | ERR-CF-005 | lean_condition | LC-001 | WORN_PISTON_RINGS | NO_FAULT |
| CSV-122 | viable | catalyst_failure | ERR-CF-005 | lean_condition | LC-001 | FLAT_CAMSHAFT | NO_FAULT |
| CSV-123 | viable | ecu_fault | ERR-EF-007 | rich_mixture | RM-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-124 | viable | ecu_fault | ERR-EF-007 | rich_mixture | RM-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| CSV-125 | viable | ecu_fault | ERR-ECU-001 | catalyst_failure | CF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CSV-126 | viable | ecu_fault | ERR-ECU-001 | misfire | MF-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| CSV-127 | viable | no_fault | OPTIMAL_HEALTH | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| CSV-128 | viable | no_fault | OPTIMAL_HEALTH | catalyst_failure | CF-001 | EGR_STUCK_OPEN | NO_FAULT |
| CSV-129 | viable | exhaust_leak | ERR-EL-005 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| CSV-130 | viable | exhaust_leak | ERR-EL-005 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| ECU-001 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| ECU-002 | viable | ecu_fault | ERR-ECU-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| ECU-003 | viable | ecu_fault | ERR-ECU-001 | catalyst_failure | CF-001 | EGR_STUCK_OPEN | NO_FAULT |
| ECU-007 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| ECU-008 | viable | misfire | ERR-MF-008 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| ECU-009 | viable | ecu_fault | ERR-EF-002 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| EXP-N001 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N002 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N003 | viable | rich_mixture | ERR-RM-007 | rich_mixture | RM-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N004 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | INCOMPLETE_COMBUSTION | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N005 | viable | ecu_fault | ERR-EF-008 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| EXP-N006 | viable | sensor_fault | ERR-SF-004 | sensor_fault | SF-002 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N007 | viable | cam_timing | ERR-CT-004 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXP-N008 | viable | catalyst_failure | ERR-CF-006 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| EXP-N009 | viable | lean_condition | ERR-LC-002 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N010 | viable | rich_mixture | ERR-RM-004 | catalyst_failure | CF-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N011 | viable | lean_condition | ERR-LC-001 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| EXP-N012 | viable | catalyst_failure | ERR-CF-003 | catalyst_failure | CF-001 | SAMPLE_INVALID | NO_FAULT |
| EXP-N013 | viable | rich_mixture | ERR-RM-005 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N014 | viable | misfire | ERR-MF-007 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXP-N015 | viable | sensor_fault | ERR-SF-002 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| EXP-N016 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| EXP-N017 | viable | lean_condition | ERR-LC-001 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N018 | viable | ecu_fault | ERR-EF-002 | sensor_fault | SF-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N019 | viable | ecu_fault | ERR-ECU-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| EXP-N020 | viable | sensor_fault | ERR-SF-004 | rich_mixture | RM-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N021 | viable | misfire | ERR-MF-003 | lean_condition | LC-001 | RICH_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| EXP-N022 | viable | lean_condition | ERR-LC-001 | catalyst_failure | CF-001 | SAMPLE_INVALID | NO_FAULT |
| EXP-N023 | viable | cam_timing | ERR-CT-005 | sensor_fault | SF-001 | SAMPLE_INVALID | NO_FAULT |
| EXP-N025 | viable | catalyst_failure | ERR-CF-003 | lean_condition | LC-002 | FLAT_CAMSHAFT | NO_FAULT |
| EXP-N026 | viable | ignition_fault | ERR-IF-005 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXP-N027 | viable | rich_mixture | ERR-RM-006 | misfire | MF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| EXP-N028 | viable | sensor_fault | ERR-SF-002 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| EXP-N029 | viable | lean_condition | ERR-LC-001 | mechanical_wear | MW-002 | WORN_VALVE_SEALS | NO_FAULT |
| EXP-N030 | viable | mechanical_wear | ERR-MW-002 | lean_condition | LC-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| EXT-201 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-202 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-203 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | FLAT_CAMSHAFT | WIDEBAND_OFFSET_CANDIDATE |
| EXT-204 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| EXT-205 | viable | lean_condition | ERR-LC-003 | lean_condition | LC-001 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| EXT-206 | viable | rich_mixture | ERR-RM-004 | rich_mixture | RM-001 | SAMPLE_INVALID | WIDEBAND_OFFSET_CANDIDATE |
| EXT-207 | viable | catalyst_failure | ERR-CF-003 | lean_condition | LC-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| EXT-208 | viable | catalyst_failure | ERR-CF-002 | lean_condition | LC-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| EXT-209 | viable | cam_timing | ERR-CT-001 | cam_timing | CT-007 | INCOMPLETE_COMBUSTION | NO_FAULT |
| EXT-210 | viable | cam_timing | ERR-CT-002 | cam_timing | CT-007 | SAMPLE_INVALID | NO_FAULT |
| EXT-211 | viable | lean_condition | ERR-LC-005 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXT-212 | viable | lean_condition | ERR-LC-005 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXT-213 | viable | catalyst_failure | ERR-CF-004 | lean_condition | LC-002 | TIMING_RETARDED | WIDEBAND_OFFSET_CANDIDATE |
| EXT-214 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-215 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-216 | viable | no_fault | OPTIMAL_HEALTH | rich_mixture | RM-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| EXT-217 | viable | rich_mixture | ERR-RM-006 | catalyst_failure | CF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| EXT-218 | viable | lean_condition | ERR-LC-002 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-219 | viable | sensor_fault | ERR-SF-003 | rich_mixture | RM-001 | EGR_STUCK_OPEN | WIDEBAND_OFFSET_CANDIDATE |
| EXT-220 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | NORMAL_OPERATION | NO_FAULT |
| EXT-221 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-222 | viable | mechanical_wear | ERR-MW-005 | misfire | MF-001 | INCOMPLETE_COMBUSTION | WIDEBAND_OFFSET_CANDIDATE |
| EXT-223 | viable | mechanical_wear | ERR-MW-003 | misfire | MF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXT-224 | viable | mechanical_wear | ERR-MW-002 | misfire | MF-001 | RICH_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-225 | viable | misfire | ERR-MF-008 | misfire | MF-001 | EGR_STUCK_OPEN | NO_FAULT |
| EXT-226 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-227 | viable | rich_mixture | ERR-RM-007 | rich_mixture | RM-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| EXT-228 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-229 | viable | sensor_fault | ERR-SF-001 | lean_condition | LC-001 | WORN_PISTON_RINGS | NO_FAULT |
| EXT-230 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-231 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-232 | viable | catalyst_failure | ERR-CF-005 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-233 | viable | catalyst_failure | ERR-CF-006 | lean_condition | LC-001 | TIMING_RETARDED | NO_FAULT |
| EXT-234 | viable | misfire | ERR-MF-002 | misfire | MF-001 | VVT_FAILURE | NO_FAULT |
| EXT-235 | viable | misfire | ERR-MF-004 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| EXT-236 | viable | misfire | ERR-MF-004 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| EXT-237 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| EXT-238 | viable | exhaust_leak | ERR-EL-005 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| EXT-239 | viable | exhaust_leak | ERR-EL-005 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| EXT-240 | viable | rich_mixture | ERR-RM-004 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| MECH-001 | viable | mechanical_wear | ERR-MW-003 | sensor_fault | SF-001 | EGR_STUCK_OPEN | NO_FAULT |
| MECH-002 | viable | mechanical_wear | ERR-MW-002 | misfire | MF-001 | RICH_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| MECH-003 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| MECH-004 | viable | cam_timing | ERR-CT-001 | cam_timing | CT-008 | INCOMPLETE_COMBUSTION | NO_FAULT |
| MECH-005 | viable | misfire | ERR-MF-007 | sensor_fault | SF-001 | POA_SIGNATURE | NO_FAULT |
| MECH-006 | viable | mechanical_wear | ERR-MW-005 | misfire | MF-001 | RICH_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| PDF-4G-01 | viable | catalyst_failure | ERR-CF-007 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| PDF-4G-02 | viable | misfire | ERR-MF-002 | sensor_fault | SF-002 | EGR_STUCK_OPEN | NO_FAULT |
| PDF-4G-03 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| PDF-4G-04 | viable | ignition_fault | ERR-IF-004 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | NO_FAULT |
| PDF-4G-05 | viable | misfire | ERR-MF-005 | sensor_fault | SF-002 | WORN_VALVE_SEALS | NO_FAULT |
| PDF-HI-001 | viable | rich_mixture | ERR-RM-003 | sensor_fault | SF-002 | GDI_HPFP_INTERNAL_SEAL_LEAK | NO_FAULT |
| PDF-HI-002 | viable | misfire | ERR-MF-003 | misfire | MF-001 | IGNITION_MISFIRE | NO_FAULT |
| PDF-HI-005 | viable | no_fault | OPTIMAL_HEALTH | sensor_fault | SF-002 | TIMING_RETARDED | NO_FAULT |
| PDF-HI-006 | viable | catalyst_failure | ERR-CF-001 | sensor_fault | SF-002 | WORN_PISTON_RINGS | NO_FAULT |
| PDF-HI-007 | viable | exhaust_leak | ERR-EL-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| PDF-HI-008 | viable | misfire | ERR-MF-002 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| PDF-HI-010 | viable | no_fault | OPTIMAL_HEALTH | sensor_fault | SF-002 | TIMING_RETARDED | NO_FAULT |
| REAL-001 | viable | non_starter | ERR-NS-001 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| REAL-002 | viable | lean_condition | ERR-LC-003 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| REAL-003 | viable | non_starter | ERR-NS-003 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| REAL-004 | viable | lean_condition | ERR-LC-005 | misfire | MF-001 | RICH_MISFIRE | NO_FAULT |
| REAL-005 | viable | catalyst_failure | ERR-CF-004 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| RULE-CO-1 | viable | rich_mixture | ERR-RM-003 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| RULE-NOx-1 | invalid | invalid_input |  | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| TC-011 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| TC-021 | viable | ecu_fault | ERR-EF-006 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| TC-046 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| TC-048 | viable | exhaust_leak | ERR-EL-001 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| YAML-CSV1 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV100 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | WIDEBAND_OFFSET_CANDIDATE |
| YAML-CSV16 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| YAML-CSV18 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| YAML-CSV22 | viable | misfire | ERR-MF-002 | misfire | MF-001 | IGNITION_MISFIRE | WIDEBAND_OFFSET_CANDIDATE |
| YAML-CSV25 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV41 | viable | ecu_fault | ERR-EF-006 | rich_mixture | RM-001 | RICH_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| YAML-CSV43 | viable | ecu_fault | ERR-ECU-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV45 | viable | ecu_fault | ERR-ECU-001 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| YAML-CSV5 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV52 | viable | misfire | ERR-MF-008 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| YAML-CSV66 | viable | misfire | ERR-MF-008 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV68 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| YAML-CSV72 | viable | ecu_fault | ERR-ECU-001 | ecu_fault | EF-004 | NORMAL_OPERATION | NO_FAULT |
| YAML-CSV81 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| YAML-CSV83 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| YAML-CSV95 | viable | exhaust_leak | ERR-EL-001 | sensor_fault | SF-002 | SAMPLE_INVALID | NO_FAULT |
| YAML-PDF_4G_01 | viable | catalyst_failure | ERR-CF-001 | cam_timing | CT-002 | VVT_FAILURE | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_4G_02 | viable | misfire | ERR-MF-002 | misfire | MF-001 | RICH_MISFIRE | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_4G_03 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_4G_04 | viable | misfire | ERR-MF-002 | misfire | MF-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_4G_05 | viable | misfire | ERR-MF-002 | ecu_fault | EF-004 | TIMING_RETARDED | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_001 | viable | rich_mixture | ERR-RM-003 | sensor_fault | SF-001 | GDI_HPFP_INTERNAL_SEAL_LEAK | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_002 | viable | misfire | ERR-MF-002 | misfire | MF-001 | GDI_INTAKE_VALVE_CARBON | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_005 | viable | no_fault | OPTIMAL_HEALTH | ecu_fault | EF-004 | TIMING_RETARDED | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_006 | viable | catalyst_failure | ERR-CF-001 | sensor_fault | SF-002 | VVT_FAILURE | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_007 | invalid | invalid_input |  | lean_condition | LC-001 | LEAN_MIXTURE | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_008 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| YAML-PDF_HI_010 | viable | no_fault | OPTIMAL_HEALTH | catalyst_failure | CF-001 | VVT_FAILURE | NOT_RUN_NO_OBD_INPUT |
| YAML-RULE_CO2_1 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NOT_RUN_NO_OBD_INPUT |
| YAML-RULE_CO_1 | viable | misfire | ERR-MF-002 | catalyst_failure | CF-001 | VVT_FAILURE | NOT_RUN_NO_OBD_INPUT |
| YAML-RULE_NOx_1 | viable | ecu_fault | ERR-ECU-001 | catalyst_failure | CF-001 | VVT_FAILURE | NOT_RUN_NO_OBD_INPUT |
| YAML-TC1 | viable | no_fault | OPTIMAL_HEALTH | ecu_fault | EF-004 | TIMING_RETARDED | NOT_RUN_NO_OBD_INPUT |
| YAML-TC11 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | LEAN_MIXTURE | NO_FAULT |
| YAML-TC12 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| YAML-TC21 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | RICH_MIXTURE | NO_FAULT |
| YAML-TC22 | viable | ecu_fault | ERR-ECU-001 | lean_condition | LC-002 | TIMING_RETARDED | NO_FAULT |
| YAML-TC36 | viable | misfire | ERR-MF-002 | misfire | MF-001 | TIMING_RETARDED | NO_FAULT |
| YAML-TC37 | viable | misfire | ERR-MF-002 | misfire | MF-001 | IGNITION_MISFIRE | NO_FAULT |
| YAML-TC46 | viable | sensor_fault | ERR-SF-001 | misfire | MF-005 | NORMAL_OPERATION | NOT_RUN_NO_OBD_INPUT |
| YAML-TC47 | viable | ecu_fault | ERR-ECU-001 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| YAML-TC48 | invalid | invalid_input |  | invalid_input | ERR-ABORT-001 | SAMPLE_INVALID | NO_FAULT |
| case_001 | viable | ecu_fault | ERR-EF-006 | lean_condition | LC-001 | INCOMPLETE_OXIDATION | WIDEBAND_OFFSET_CANDIDATE |
| case_002 | viable | rich_mixture | ERR-RM-003 | sensor_fault | SF-001 | SAMPLE_INVALID | NO_FAULT |
| case_003 | viable | lean_condition | ERR-LC-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| case_004 | viable | sensor_fault | ERR-SF-001 | catalyst_failure | CF-001 | TIMING_RETARDED | NO_FAULT |
| case_005 | viable | misfire | ERR-MF-002 | misfire | MF-001 | POA_SIGNATURE | NO_FAULT |
| case_006 | viable | non_starter | ERR-NS-003 | invalid_input | II-002 | SAMPLE_INVALID | NO_FAULT |
| case_007 | viable | non_starter | ERR-NS-004 | misfire | MF-001 | SAMPLE_INVALID | NO_FAULT |
| case_008 | viable | lean_condition | ERR-LC-001 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| case_009 | viable | sensor_fault | ERR-SF-002 | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| case_010 | viable | catalyst_failure | ERR-CF-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| case_011 | invalid | invalid_input |  |  |  | VVT_FAILURE | NO_FAULT |
| case_013 | viable | ecu_fault | ERR-EF-007 | rich_mixture | RM-001 | VVT_FAILURE | WIDEBAND_OFFSET_CANDIDATE |
| case_014 | viable | no_fault | OPTIMAL_HEALTH | sensor_fault | SF-002 | VVT_FAILURE | NO_FAULT |
| case_015 | viable | rich_mixture | ERR-RM-003 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| case_016 | viable | lean_condition | ERR-LC-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| case_017 | viable | rich_mixture | ERR-RM-003 | catalyst_failure | CF-001 | INCOMPLETE_COMBUSTION | NO_FAULT |
| case_018 | viable | lean_condition | ERR-LC-001 | lean_condition | LC-001 | GDI_INTAKE_VALVE_CARBON | WIDEBAND_OFFSET_CANDIDATE |
| case_019 | viable | lean_condition | ERR-LC-005 | lean_condition | LC-001 | LEAN_MIXTURE | WIDEBAND_OFFSET_CANDIDATE |
| case_020 | invalid | invalid_input |  |  |  | VVT_FAILURE | OBDLAB_ERROR:PIDValidationError |
| case_021 | invalid | invalid_input |  |  |  | TIMING_RETARDED | OBDLAB_ERROR:PIDValidationError |
| case_022 | viable | misfire | ERR-MF-002 | misfire | MF-002 | VVT_FAILURE | NO_FAULT |
| case_023 | viable | rich_mixture | ERR-RM-003 | rich_mixture | RM-001 | RICH_MIXTURE | NO_FAULT |
| case_027 | viable | ecu_fault | ERR-ECU-001 | ecu_fault | EF-004 | TIMING_RETARDED | NO_FAULT |
| case_028 | viable | no_fault | OPTIMAL_HEALTH | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |
| case_034 | viable | catalyst_failure | ERR-CF-001 | catalyst_failure | CF-001 | VVT_FAILURE | NO_FAULT |
| case_040 | viable | non_starter | ERR-NS-001 | invalid_input | II-002 | SAMPLE_INVALID | NO_FAULT |
| case_044 | viable | mechanical_wear | ERR-MW-007 | sensor_fault | SF-001 | POA_SIGNATURE | NO_FAULT |
| case_046 | viable | sensor_fault | ERR-SF-001 | no_fault | NF-001 | TIMING_RETARDED | NO_FAULT |

