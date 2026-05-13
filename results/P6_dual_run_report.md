# P6 Dual-Run Report — V1 vs V2

**Date:** 2026-05-13 16:04
**Corpus:** `cases/csv/cases_petrol_master_v6.csv`
**Cases processed:** 400
**Elapsed:** 0.9s

## Summary

| Classification | Count | % |
|---|---|---|
| schema_gap | 0 | 0.0% |
| threshold_tweak | 334 | 83.5% |
| expected_drift | 54 | 13.5% |
| blocker | 12 | 3.0% |

## Per-Case Diff

| case_id | expected | V1 top | V2 top | classification |
|---|---|---|---|---|
| CSV-001 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| CSV-005 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| CSV-016 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CSV-018 | rich_mixture | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| CSV-022 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| CSV-025 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| CSV-041 | ecu_fault | pcv_fault | Leaking_Injector | threshold_tweak |
| CSV-043 | ecu_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| CSV-045 | ecu_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| CSV-052 | misfire | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| CSV-066 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| CSV-068 | lean_condition | ecu_fault | Lean_Condition | threshold_tweak |
| CSV-072 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| CSV-081 | invalid_input | invalid_input | Catalyst_Failure | expected_drift |
| CSV-083 | invalid_input | invalid_input | Fuel_Delivery_Low | expected_drift |
| CSV-095 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | blocker |
| CSV-100 | lean_condition | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| REAL-001 | non_starter | misfire | Fuel_Delivery_Low | threshold_tweak |
| REAL-002 | lean_condition | ns_lean_no_start | Fuel_Delivery_Low | threshold_tweak |
| REAL-003 | non_starter | ns_flooded | Fuel_Delivery_Low | threshold_tweak |
| REAL-004 | lean_condition | stuck_egr_open | Fuel_Delivery_Low | blocker |
| REAL-005 | catalyst_failure | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| MECH-001 | mechanical_wear | egr_fault | GDI_Carbon_Buildup | threshold_tweak |
| MECH-002 | mechanical_wear | head_gasket | Fuel_Delivery_Low | blocker |
| MECH-003 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| MECH-004 | cam_timing | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| MECH-005 | lean_condition | valve_seal_wear | Vacuum_Leak_Intake | threshold_tweak |
| MECH-006 | mechanical_wear | head_gasket | Fuel_Delivery_Low | threshold_tweak |
| ECU-001 | ecu_fault | pcv_fault | Leaking_Injector | threshold_tweak |
| ECU-002 | ecu_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| ECU-003 | ecu_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| ECU-007 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| ECU-008 | misfire | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| ECU-009 | ecu_fault | sensor_fault | Leaking_Injector | threshold_tweak |
| TC-011 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| TC-021 | ecu_fault | valve_timing_mechanical | Leaking_Injector | threshold_tweak |
| TC-046 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| TC-048 | exhaust_leak | sensor_fault | Fuel_Delivery_Low | threshold_tweak |
| PDF-HI-001 | rich_mixture | rich_mixture | Leaking_Injector | threshold_tweak |
| PDF-HI-002 | misfire | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| PDF-HI-005 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| PDF-HI-006 | catalyst_failure | sensor_fault | Catalyst_Failure | threshold_tweak |
| PDF-HI-007 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| PDF-HI-008 | misfire | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| PDF-HI-010 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| PDF-4G-01 | catalyst_failure | egr_fault | Catalyst_Failure | threshold_tweak |
| PDF-4G-02 | misfire | rich_mixture | Leaking_Injector | threshold_tweak |
| PDF-4G-03 | rich_mixture | rich_mixture | Leaking_Injector | blocker |
| PDF-4G-04 | misfire | sensor_fault | Fuel_Delivery_Low | threshold_tweak |
| PDF-4G-05 | misfire | catalyst_failure | Catalyst_Failure | expected_drift |
| RULE-CO-1 | rich_mixture | catalyst_failure | Catalyst_Failure | expected_drift |
| RULE-NOx-1 | invalid_input | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| YAML-TC1 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-TC11 | invalid_input | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| YAML-TC12 | rich_mixture | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| YAML-TC21 | invalid_input | ecu_fault | Leaking_Injector | threshold_tweak |
| YAML-TC22 | ecu_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| YAML-TC36 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| YAML-TC37 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| YAML-TC46 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-TC47 | ecu_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| YAML-TC48 | invalid_input | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| YAML-CSV1 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-CSV5 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-CSV16 | invalid_input | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| YAML-CSV18 | rich_mixture | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| YAML-CSV22 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| YAML-CSV25 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-CSV41 | ecu_fault | sensor_fault | Leaking_Injector | threshold_tweak |
| YAML-CSV43 | ecu_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| YAML-CSV45 | ecu_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| YAML-CSV52 | misfire | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| YAML-CSV66 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| YAML-CSV68 | lean_condition | ecu_fault | Lean_Condition | threshold_tweak |
| YAML-CSV72 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| YAML-CSV81 | invalid_input | invalid_input | Catalyst_Failure | expected_drift |
| YAML-CSV83 | invalid_input | invalid_input | Fuel_Delivery_Low | expected_drift |
| YAML-CSV95 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | blocker |
| YAML-CSV100 | invalid_input | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| YAML-RULE_CO_1 | misfire | catalyst_failure | Catalyst_Failure | expected_drift |
| YAML-RULE_CO2_1 | invalid_input | catalyst_failure | Fuel_Delivery_Low | threshold_tweak |
| YAML-RULE_NOx_1 | ecu_fault | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| YAML-PDF_HI_001 | rich_mixture | rich_mixture | Leaking_Injector | threshold_tweak |
| YAML-PDF_HI_002 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| YAML-PDF_HI_005 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| YAML-PDF_HI_006 | catalyst_failure | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| YAML-PDF_HI_007 | invalid_input | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| YAML-PDF_HI_008 | invalid_input | head_gasket | Fuel_Delivery_Low | threshold_tweak |
| YAML-PDF_HI_010 | no_fault | catalyst_failure | Catalyst_Failure | expected_drift |
| YAML-PDF_4G_01 | catalyst_failure | catalyst_failure | Catalyst_Failure | expected_drift |
| YAML-PDF_4G_02 | misfire | rich_mixture | Leaking_Injector | threshold_tweak |
| YAML-PDF_4G_03 | rich_mixture | rich_mixture | Leaking_Injector | threshold_tweak |
| YAML-PDF_4G_04 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| YAML-PDF_4G_05 | misfire | sensor_fault | Catalyst_Failure | threshold_tweak |
| CSV-101 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CSV-102 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CSV-103 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| CSV-104 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| CSV-105 | misfire | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| CSV-106 | misfire | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| CSV-107 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| CSV-108 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| CSV-109 | lean_condition | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| CSV-110 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CSV-111 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CSV-112 | lean_condition | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| CSV-113 | lean_condition | stuck_egr_open | Fuel_Delivery_Low | blocker |
| CSV-114 | lean_condition | stuck_egr_open | Fuel_Delivery_Low | blocker |
| CSV-115 | cam_timing | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CSV-116 | cam_timing | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CSV-117 | mechanical_wear | Cam_Timing_Retard_Late | Fuel_Delivery_Low | threshold_tweak |
| CSV-118 | mechanical_wear | Cam_Timing_Retard_Late | Fuel_Delivery_Low | threshold_tweak |
| CSV-119 | mechanical_wear | misfire | Fuel_Delivery_Low | threshold_tweak |
| CSV-120 | mechanical_wear | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| CSV-121 | catalyst_failure | lean_condition | Lean_Condition | expected_drift |
| CSV-122 | catalyst_failure | lean_condition | Lean_Condition | expected_drift |
| CSV-123 | ecu_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| CSV-124 | ecu_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| CSV-125 | ecu_fault | late_ignition_timing | Rich_Mixture | threshold_tweak |
| CSV-126 | ecu_fault | rich_mixture | Rich_Mixture | expected_drift |
| CSV-127 | no_fault | Cam_Timing_Retard_Late | Catalyst_Failure | threshold_tweak |
| CSV-128 | no_fault | Cam_Timing_Retard_Late | Catalyst_Failure | threshold_tweak |
| CSV-129 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| CSV-130 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| EXP-N001 | lean_condition | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| EXP-N002 | ecu_fault | mechanical_wear | Leaking_Injector | threshold_tweak |
| EXP-N003 | rich_mixture | high_fuel_pressure | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXP-N004 | ecu_fault | sensor_fault | Lean_Condition | threshold_tweak |
| EXP-N005 | ecu_fault | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| EXP-N006 | sensor_fault | late_ignition_timing | Catalyst_Failure | threshold_tweak |
| EXP-N007 | cam_timing | catalyst_failure | Catalyst_Failure | expected_drift |
| EXP-N008 | catalyst_failure | egr_fault | Lean_Condition | threshold_tweak |
| EXP-N009 | lean_condition | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| EXP-N010 | lean_condition | late_ignition_timing | Rich_Mixture | threshold_tweak |
| EXP-N011 | lean_condition | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| EXP-N012 | catalyst_failure | rich_mixture | Lean_Condition | threshold_tweak |
| EXP-N013 | rich_mixture | high_fuel_pressure | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXP-N014 | lean_condition | late_ignition_timing | Lean_Condition | threshold_tweak |
| EXP-N015 | sensor_fault | sensor_fault | Vacuum_Leak_Intake | threshold_tweak |
| EXP-N016 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| EXP-N017 | lean_condition | turbo_fault | Turbo_Fault | expected_drift |
| EXP-N018 | ecu_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| EXP-N019 | ecu_fault | sensor_fault | Fuel_Delivery_Low | threshold_tweak |
| EXP-N020 | sensor_fault | high_fuel_pressure | High_Fuel_Pressure | expected_drift |
| EXP-N021 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| EXP-N022 | lean_condition | rich_mixture | Lean_Condition | threshold_tweak |
| EXP-N023 | cam_timing | late_ignition_timing | Catalyst_Failure | threshold_tweak |
| EXP-N025 | catalyst_failure | rich_mixture | Catalyst_Failure | threshold_tweak |
| EXP-N026 | ignition_fault | late_ignition_timing | Catalyst_Failure | threshold_tweak |
| EXP-N027 | ecu_fault | late_ignition_timing | ECT_Sensor_Bias | threshold_tweak |
| EXP-N028 | sensor_fault | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| EXP-N029 | lean_condition | catalyst_failure | Catalyst_Failure | expected_drift |
| EXP-N030 | ecu_fault | mechanical_wear | Leaking_Injector | threshold_tweak |
| EXT-201 | lean_condition | intake_gasket_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-202 | lean_condition | intake_gasket_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-203 | rich_mixture | rich_mixture | GDI_HPFP_Internal_Leak | threshold_tweak |
| EXT-204 | lean_condition | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| EXT-205 | lean_condition | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| EXT-206 | lean_condition | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXT-207 | catalyst_failure | catalyst_failure | Fuel_Delivery_Low | threshold_tweak |
| EXT-208 | catalyst_failure | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| EXT-209 | cam_timing | late_ignition_timing | Vacuum_Leak_Intake | threshold_tweak |
| EXT-210 | cam_timing | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EXT-211 | lean_condition | stuck_egr_open | EGR_Stuck_Open | expected_drift |
| EXT-212 | lean_condition | stuck_egr_open | EGR_Stuck_Open | expected_drift |
| EXT-213 | catalyst_failure | catalyst_failure | Fuel_Delivery_Low | threshold_tweak |
| EXT-214 | lean_condition | intake_gasket_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-215 | lean_condition | intake_gasket_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-216 | no_fault | high_fuel_pressure | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXT-217 | rich_mixture | late_ignition_timing | ECT_Sensor_Bias | threshold_tweak |
| EXT-218 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| EXT-219 | sensor_fault | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXT-220 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| EXT-221 | ecu_fault | pcv_fault | Leaking_Injector | threshold_tweak |
| EXT-222 | mechanical_wear | Cam_Timing_Retard_Late | Vacuum_Leak_Intake | threshold_tweak |
| EXT-223 | mechanical_wear | Cam_Timing_Retard_Late | Fuel_Delivery_Low | threshold_tweak |
| EXT-224 | mechanical_wear | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| EXT-225 | misfire | misfire | Spark_Plug_Worn | threshold_tweak |
| EXT-226 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| EXT-227 | rich_mixture | high_fuel_pressure | EVAP_Purge_Stuck_Open | threshold_tweak |
| EXT-228 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| EXT-229 | sensor_fault | lean_condition | Lean_Condition | expected_drift |
| EXT-230 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| EXT-231 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| EXT-232 | catalyst_failure | sensor_fault | Lean_Condition | threshold_tweak |
| EXT-233 | catalyst_failure | sensor_fault | Lean_Condition | threshold_tweak |
| EXT-234 | misfire | misfire | Spark_Plug_Worn | threshold_tweak |
| EXT-235 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| EXT-236 | misfire | misfire | Fuel_Delivery_Low | threshold_tweak |
| EXT-237 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| EXT-238 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-239 | exhaust_leak | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| EXT-240 | lean_condition | late_ignition_timing | Rich_Mixture | threshold_tweak |
| CASE-009 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| CASE-010 | sensor_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| CASE-011 | lean_condition | intake_gasket_leak | Fuel_Delivery_Low | threshold_tweak |
| CASE-012 | lean_condition | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| CASE-013 | catalyst_failure | catalyst_failure | Fuel_Delivery_Low | threshold_tweak |
| CASE-014 | sensor_fault | sensor_fault | Lean_Condition | threshold_tweak |
| CASE-015 | catalyst_failure | sensor_fault | Lean_Condition | threshold_tweak |
| CASE-016 | catalyst_failure | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| CASE-017 | lean_condition | Mechanical_Lean_Vacuum_Leak | Fuel_Delivery_Low | threshold_tweak |
| CASE-018 | cam_timing | catalyst_failure | Lean_Condition | threshold_tweak |
| CASE-019 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-020 | lean_condition | stuck_egr_open | EGR_Stuck_Open | expected_drift |
| CASE-021 | misfire | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CASE-022 | sensor_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-023 | rich_mixture | late_ignition_timing | ECT_Sensor_Bias | threshold_tweak |
| CASE-024 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-025 | lean_condition | rich_mixture | GDI_HPFP_Internal_Leak | threshold_tweak |
| CASE-026 | catalyst_failure | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| CASE-027 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-028 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| CASE-029 | rich_mixture | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| CASE-030 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-031 | rich_mixture | high_fuel_pressure | High_Fuel_Pressure | expected_drift |
| CASE-032 | lean_condition | sensor_fault | Catalyst_Failure | threshold_tweak |
| CASE-033 | misfire | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CASE-034 | lean_condition | turbo_fault | Turbo_Fault | expected_drift |
| CASE-035 | ignition_fault | valve_seal_wear | Catalyst_Failure | threshold_tweak |
| CASE-036 | lean_condition | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| CASE-037 | rich_mixture | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| CASE-038 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CASE-039 | ecu_fault | mechanical_wear | Leaking_Injector | threshold_tweak |
| CASE-040 | rich_mixture | turbo_fault | Turbo_Fault | expected_drift |
| CASE-041 | invalid_input | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| CASE-043 | invalid_input | sensor_fault | Catalyst_Failure | threshold_tweak |
| CASE-045 | sensor_fault | misfire | GDI_Carbon_Buildup | threshold_tweak |
| CASE-046 | invalid_input | invalid_input | Catalyst_Failure | expected_drift |
| CASE-047 | invalid_input | invalid_input | Fuel_Delivery_Low | expected_drift |
| CASE-048 | sensor_fault | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| case_001 | ecu_fault | sensor_fault | Leaking_Injector | threshold_tweak |
| case_002 | rich_mixture | ns_mechanical_partial | Lean_Condition | threshold_tweak |
| case_003 |  | exhaust_leak | Fuel_Delivery_Low | threshold_tweak |
| case_004 | sensor_fault | ecu_fault | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| case_005 | misfire | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| case_006 | non_starter | ns_no_fuel | Fuel_Delivery_Low | threshold_tweak |
| case_007 | non_starter | ns_mechanical_partial | Fuel_Delivery_Low | threshold_tweak |
| case_008 | lean_condition | catalyst_failure | Fuel_Delivery_Low | threshold_tweak |
| case_009 | sensor_fault | ecu_fault | Vacuum_Leak_Intake | threshold_tweak |
| case_010 | catalyst_failure | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| case_011 |  | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| case_012 |  | sensor_fault | Catalyst_Failure | threshold_tweak |
| case_013 | ecu_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| case_014 |  | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| case_015 | rich_mixture | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| case_016 |  | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| case_017 | rich_mixture | rich_mixture | Lean_Condition | threshold_tweak |
| case_018 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| case_019 | lean_condition | pcv_fault | Fuel_Delivery_Low | threshold_tweak |
| case_020 |  | catalyst_failure | Vacuum_Leak_Intake | threshold_tweak |
| case_021 |  | sensor_fault | Catalyst_Failure | threshold_tweak |
| case_022 | misfire | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| case_023 | rich_mixture | rich_mixture | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| case_024 | catalyst_failure | ecu_fault | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| case_025 | sensor_fault | catalyst_failure | ECT_Sensor_Bias | threshold_tweak |
| case_026 | sensor_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| case_027 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| case_028 |  | sensor_fault | Catalyst_Failure | threshold_tweak |
| case_029 | rich_mixture | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| case_030 | rich_mixture | late_ignition_timing | Rich_Mixture | threshold_tweak |
| case_031 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| case_032 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| case_033 | ecu_fault | sensor_fault | Leaking_Injector | threshold_tweak |
| case_034 | catalyst_failure | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| case_035 | misfire | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| case_036 | ignition_fault | late_ignition_timing | GDI_Carbon_Buildup | threshold_tweak |
| case_037 | sensor_fault | ns_mechanical_partial | Catalyst_Failure | threshold_tweak |
| case_038 | ecu_fault | rich_mixture | Vacuum_Leak_Intake | threshold_tweak |
| case_039 | sensor_fault | ecu_fault | GDI_HPFP_Failure | threshold_tweak |
| case_040 | non_starter | ns_no_fuel | Fuel_Delivery_Low | threshold_tweak |
| case_041 | sensor_fault | sensor_fault | GDI_HPFP_Failure | threshold_tweak |
| case_042 | cam_timing | rich_mixture | Rich_Mixture | expected_drift |
| case_043 | lean_condition | sensor_fault | Fuel_Delivery_Low | threshold_tweak |
| case_044 | mechanical_wear | late_ignition_timing | GDI_Carbon_Buildup | threshold_tweak |
| case_045 | exhaust_leak | sensor_fault | Lean_Condition | threshold_tweak |
| case_046 | sensor_fault | ecu_fault | ECT_Sensor_Bias | threshold_tweak |
| case_047 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| case_048 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| case_049 |  | ecu_fault | Lean_Condition | threshold_tweak |
| case_050 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| GAP-001 | ecu_fault | ecu_fault | Leaking_Injector | threshold_tweak |
| GAP-002 | ecu_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| GAP-003 | ecu_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| GAP-004 | ecu_fault | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| GAP-005 | sensor_fault | rich_mixture | Rich_Mixture | expected_drift |
| GAP-006 | sensor_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| GAP-007 | sensor_fault | rich_mixture | Rich_Mixture | expected_drift |
| GAP-008 | sensor_fault | catalyst_failure | Catalyst_Failure | expected_drift |
| GAP-009 | sensor_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| GAP-010 | ecu_fault | rich_mixture | Rich_Mixture | expected_drift |
| GAP-011 | ecu_fault | lean_condition | Lean_Condition | expected_drift |
| GAP-012 | ecu_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| GAP-013 | sensor_fault | rich_mixture | Rich_Mixture | expected_drift |
| GAP-014 | sensor_fault | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| GAP-015 | ecu_fault | ecu_fault | Lean_Condition | threshold_tweak |
| GAP-016 | ecu_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| GAP-017 | ecu_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| GAP-018 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| GAP-019 | sensor_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| GAP-020 | sensor_fault | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| GAP-021 | sensor_fault | ecu_fault | Fuel_Delivery_Low | threshold_tweak |
| GAP-022 | ecu_fault | rich_mixture | Fuel_Delivery_Low | threshold_tweak |
| GAP-023 | ecu_fault | ecu_fault | Leaking_Injector | threshold_tweak |
| GAP-024 | sensor_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| GAP-025 | ecu_fault | induction_issue | Fuel_Delivery_Low | threshold_tweak |
| GAP-026 | ecu_fault | ecu_fault | Spark_Plug_Worn | threshold_tweak |
| GAP-027 | ecu_fault | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| GAP-028 | sensor_fault | sensor_fault | Fuel_Delivery_Low | threshold_tweak |
| GAP-029 | ecu_fault | rich_mixture | ECT_Sensor_Bias | threshold_tweak |
| GAP-030 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| EGR-001 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | blocker |
| EGR-002 | egr_fault | misfire | Fuel_Delivery_Low | threshold_tweak |
| EGR-003 | egr_fault | catalyst_failure | Catalyst_Failure | expected_drift |
| EGR-004 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | blocker |
| EGR-005 | egr_fault | misfire | Fuel_Delivery_Low | threshold_tweak |
| EGR-006 | egr_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EGR-007 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | blocker |
| EGR-008 | egr_fault | egr_fault | Catalyst_Failure | threshold_tweak |
| EGR-009 | egr_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EGR-010 | egr_fault | rich_mixture | Fuel_Delivery_Low | threshold_tweak |
| EGR-011 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | blocker |
| EGR-012 | egr_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| EGR-013 | egr_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EGR-014 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | threshold_tweak |
| EGR-015 | egr_fault | egr_fault | Catalyst_Failure | threshold_tweak |
| EGR-016 | egr_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EGR-017 | egr_fault | stuck_egr_open | Fuel_Delivery_Low | blocker |
| EGR-018 | egr_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| EGR-019 | egr_fault | egr_fault | Catalyst_Failure | threshold_tweak |
| EGR-020 | egr_fault | misfire | Fuel_Delivery_Low | threshold_tweak |
| TURBO-001 | turbo_fault | rich_mixture | Turbo_Fault | threshold_tweak |
| TURBO-002 | turbo_fault | ecu_fault | Turbo_Fault | threshold_tweak |
| TURBO-003 | turbo_fault | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| TURBO-004 | turbo_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| TURBO-005 | turbo_fault | rich_mixture | Rich_Mixture | expected_drift |
| TURBO-006 | turbo_fault | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| TURBO-007 | turbo_fault | ecu_fault | Turbo_Fault | threshold_tweak |
| TURBO-008 | turbo_fault | rich_mixture | Catalyst_Failure | threshold_tweak |
| TURBO-009 | turbo_fault | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| TURBO-010 | turbo_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| FF-001 | ignition_fault | late_ignition_timing | Misfire | threshold_tweak |
| FF-002 | catalyst_fault | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| FF-003 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| FF-004 | ignition_fault | misfire | Misfire | expected_drift |
| FF-005 | rich_mixture | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| FF-006 | catalyst_fault | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| FF-007 | ignition_fault | late_ignition_timing | Spark_Plug_Worn | threshold_tweak |
| FF-008 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| FF-009 | fuel_fault | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| FF-010 | ignition_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| FF-011 | fuel_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| FF-012 | sensor_fault | late_ignition_timing | ECT_Sensor_Bias | threshold_tweak |
| FF-013 | egr_fault | egr_fault | EGR_Stuck_Open | threshold_tweak |
| FF-014 | ignition_fault | late_ignition_timing | Spark_Plug_Worn | threshold_tweak |
| FF-015 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| CS-001 | no_fault | Cam_Timing_Retard_Late | Leaking_Injector | threshold_tweak |
| CS-002 | no_fault | late_ignition_timing | Lean_Condition | threshold_tweak |
| CS-003 | lean_condition | late_ignition_timing | Lean_Condition | threshold_tweak |
| CS-004 | no_fault | catalyst_failure | Catalyst_Failure | expected_drift |
| CS-005 | rich_mixture | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| CS-006 | ignition_fault | invalid_input | Fuel_Delivery_Low | expected_drift |
| CS-007 | ignition_fault | misfire | GDI_Carbon_Buildup | threshold_tweak |
| CS-008 | mechanical_fault | mechanical_wear | Fuel_Delivery_Low | threshold_tweak |
| CS-009 | ignition_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CS-010 | ecu_fault | invalid_input | Fuel_Delivery_Low | expected_drift |
| CS-011 | no_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| CS-012 | sensor_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CS-013 | no_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| CS-014 | mechanical_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| CS-015 | ignition_fault | invalid_input | Fuel_Delivery_Low | expected_drift |
| ERA-001 | ignition_fault | misfire | Fuel_Delivery_Low | threshold_tweak |
| ERA-002 | fuel_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| ERA-003 | catalyst_fault | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| ERA-004 | fuel_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| ERA-005 | mechanical_fault | late_ignition_timing | Vacuum_Leak_Intake | threshold_tweak |
| ERA-006 | fuel_fault | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| ERA-007 | exhaust_fault | ecu_fault | Catalyst_Failure | threshold_tweak |
| ERA-008 | sensor_fault | rich_mixture | Catalyst_Failure | threshold_tweak |
| ERA-009 | no_fault | rich_mixture | Leaking_Injector | threshold_tweak |
| ERA-010 | ecu_fault | ecu_fault | ECU_Internal_Checksum_Error | threshold_tweak |
| DB-001 | lean_condition | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| DB-002 | rich_mixture | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| DB-003 | lean_condition | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| DB-004 | ignition_fault | late_ignition_timing | Fuel_Delivery_Low | threshold_tweak |
| DB-005 | fuel_fault | rich_mixture | EVAP_Purge_Stuck_Open | threshold_tweak |
| DB-006 | catalyst_fault | catalyst_failure | Aftermarket_Catalyst_Inefficient | threshold_tweak |
| DB-007 | sensor_fault | ecu_fault | Lean_Condition | threshold_tweak |
| DB-008 | no_fault | sensor_fault | Catalyst_Failure | threshold_tweak |
| DB-009 | fuel_fault | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| DB-010 | exhaust_fault | lean_condition | Lean_Condition | expected_drift |
| MIX-001 | fuel_fault | ecu_fault | Lean_Condition | threshold_tweak |
| MIX-002 | ignition_fault | catalyst_failure | Catalyst_Failure | expected_drift |
| MIX-003 | sensor_fault | sensor_fault | Vacuum_Leak_Intake | threshold_tweak |
| MIX-004 | mechanical_fault | fuel_delivery | Fuel_Delivery_Low | expected_drift |
| MIX-005 | sensor_fault | lean_condition | Fuel_Delivery_Low | threshold_tweak |
| MIX-006 | exhaust_fault | lean_condition | Lean_Condition | expected_drift |
| MIX-007 | catalyst_fault | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| MIX-008 | sensor_fault | rich_mixture | High_Fuel_Pressure | threshold_tweak |
| MIX-009 | ignition_fault | late_ignition_timing | Vacuum_Leak_Intake | threshold_tweak |

## Classification Definitions

- **schema_gap**: V1 fault ID missing from V2 `faults.yaml`.
- **threshold_tweak**: Same fault family, different specific diagnosis.
- **expected_drift**: V2 intentionally differs due to architectural changes.
- **blocker**: V2 result is clearly wrong (systematic failure).

## Blocker Details

### CSV-095
- **Expected:** exhaust_leak
- **V1:** exhaust_leak (confidence=0.1026)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.5807646808071, 'raw_score': 0.5807646808071, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### REAL-004
- **Expected:** lean_condition
- **V1:** stuck_egr_open (confidence=0.2273)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.4, 'raw_score': 0.40064750000000005, 'evidence_layers_used': ['L1'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### MECH-002
- **Expected:** mechanical_wear
- **V1:** head_gasket (confidence=0.0916)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.37675393625000003, 'raw_score': 0.37675393625000003, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### PDF-4G-03
- **Expected:** rich_mixture
- **V1:** rich_mixture (confidence=0.1206)
- **V2:** {'fault_id': 'Leaking_Injector', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.4, 'raw_score': 0.43231, 'evidence_layers_used': ['L1'], 'tier_delta': 0.38981000000000005, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### YAML-CSV95
- **Expected:** exhaust_leak
- **V1:** exhaust_leak (confidence=0.1204)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.4, 'raw_score': 0.416011525, 'evidence_layers_used': ['L1'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### CSV-113
- **Expected:** lean_condition
- **V1:** stuck_egr_open (confidence=0.2614)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.48725393625, 'raw_score': 0.48725393625, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### CSV-114
- **Expected:** lean_condition
- **V1:** stuck_egr_open (confidence=0.2614)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.48725393625, 'raw_score': 0.48725393625, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### EGR-001
- **Expected:** egr_fault
- **V1:** stuck_egr_open (confidence=0.1224)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.47366294229875, 'raw_score': 0.47366294229875, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### EGR-004
- **Expected:** egr_fault
- **V1:** stuck_egr_open (confidence=0.1224)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.47366294229875, 'raw_score': 0.47366294229875, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### EGR-007
- **Expected:** egr_fault
- **V1:** stuck_egr_open (confidence=0.1224)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.47366294229875, 'raw_score': 0.47366294229875, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### EGR-011
- **Expected:** egr_fault
- **V1:** stuck_egr_open (confidence=0.1224)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.47366294229875, 'raw_score': 0.47366294229875, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}

### EGR-017
- **Expected:** egr_fault
- **V1:** stuck_egr_open (confidence=0.1224)
- **V2:** {'fault_id': 'Fuel_Delivery_Low', 'symptom_chain': [], 'root_cause': None, 'confidence': 0.47366294229875, 'raw_score': 0.47366294229875, 'evidence_layers_used': ['L1', 'L3'], 'tier_delta': 0.0, 'discriminator_satisfied': False, 'promoted_from_parent': True}
