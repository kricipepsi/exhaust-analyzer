# OBDLab PID Log Set — Signal Map

This table maps each test case to the **single** channel it is designed to move, or, for rejection cases, the expected exception type.

| Case ID | Target Channel / Expected Rejection | Expected Value / Type | Notes / Description |
|:---|:---|:---|:---|
| `pid_case_01_na_dual_nb_stoich_healthy` | *Baseline Stoich / Healthy* | `ve_validity`: `VALID`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `-6.0` | 2.0L I4 NA, DUAL_MAF_MAP, NARROWBAND, warm idle baseline |
| `pid_case_02_na_map_wb_stoich_healthy` | *Baseline Stoich / Healthy* | `ve_validity`: `UNKNOWN`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `3.0` | 1.8L I4 NA, MAP_ONLY, WIDEBAND_LINEAR, warm idle baseline |
| `pid_case_03_turbo_maf_wbsim_stoich_healthy` | *Baseline Stoich / Healthy* | `ve_validity`: `UNKNOWN`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `0.0` | 2.5L I5 Turbo, MAF_ONLY, WIDEBAND_NB_SIM, warm idle baseline |
| `pid_case_04_narrowband_lean` | `normalized_obd_lambda` | `1.05` | Narrowband voltage (0.2V) mapped to lean lambda |
| `pid_case_05_narrowband_rich` | `normalized_obd_lambda` | `0.95` | Narrowband voltage (0.75V) mapped to rich lambda |
| `pid_case_06_wideband_lean` | `normalized_obd_lambda` | `1.15` | Wideband equivalence ratio pass-through (1.15) |
| `pid_case_07_wideband_rich` | `normalized_obd_lambda` | `0.85` | Wideband equivalence ratio pass-through (0.85) |
| `pid_case_08_narrowband_clamp_lean` | `o2_failure_mode` / `normalized_obd_lambda` | `STUCK_LEAN` / `1.05` (clamped) | O2 voltage < 0.1V clamps to lean / sets STUCK_LEAN failure mode |
| `pid_case_09_narrowband_clamp_rich` | `o2_failure_mode` / `normalized_obd_lambda` | `STUCK_RICH` / `0.95` (clamped) | O2 voltage > 0.9V clamps to rich / sets STUCK_RICH failure mode |
| `pid_case_10_wideband_clamp_lean` | `normalized_obd_lambda` | `0.70` (clamped) | Wideband ratio < 0.7 clamps to min limit |
| `pid_case_11_wideband_clamp_rich` | `normalized_obd_lambda` | `1.30` (clamped) | Wideband ratio > 1.3 clamps to max limit |
| `pid_case_12_wbsim_clamp_lean` | `o2_failure_mode` / `normalized_obd_lambda` | `STUCK_LEAN` / `1.05` (clamped) | NB-sim O2 voltage < 0.1V clamps to lean / sets STUCK_LEAN |
| `pid_case_13_wbsim_clamp_rich` | `o2_failure_mode` / `normalized_obd_lambda` | `STUCK_RICH` / `0.95` (clamped) | NB-sim O2 voltage > 0.9V clamps to rich / sets STUCK_RICH |
| `pid_case_14_large_positive_trim` | `total_trim_correction_delta` | `25.0` | Large positive trim delta (> 15%) from vacuum leak |
| `pid_case_15_large_negative_trim` | `total_trim_correction_delta` | `-25.0` | Large negative trim delta (< -15%) from leaking injector |
| `pid_case_16_bank2_healthy` | `total_trim_correction_delta_b2` | `3.0` | V6 engine carrying bank 2 trims (shrtft2 + longft2) |
| `pid_case_17_ve_idle_collapse` | `ve_validity` | `FAULT_VE_IDLE_COLLAPSE` | VE collapse: VE < 50% at warm stabilized idle, MAP > 45 kPa |
| `pid_case_18_maf_contamination` | `ve_validity` | `FAULT_MAF_CONTAMINATION` | MAF contamination: VE < 65% at high idle with TFT > 15% |
| `pid_case_19_ve_sensor_skew` | `ve_validity` | `FAULT_VE_SENSOR_SKEW` | VE sensor skew: VE > 90% at idle on a naturally aspirated engine |
| `pid_case_20_stabilized_warm_idle` | `rpm_state_bucket` | `STABILIZED_IDLE` | Normal warm idle RPM and load bucket |
| `pid_case_21_regulatory_high_idle` | `rpm_state_bucket` | `REGULATORY_HIGH_IDLE` | High idle emission test RPM and load bucket |
| `pid_case_22_stress_idle` | `rpm_state_bucket` | `STRESS_IDLE` | Clinical high RPM / stress idle target bucket |
| `pid_case_23_cold_open_loop_invalid` | `rpm_state_bucket` / `trim_analytics_gate` | `COLD_OPEN_LOOP_INVALID` / `ENGINE_COLD` | Engine below 75°C triggers thermal gate, freezes analytics |
| `pid_case_24_gate_engine_cold` | `trim_analytics_gate` | `ENGINE_COLD` | Engine coolant < 70°C, blocking trim analytics |
| `pid_case_25_gate_open_loop` | `trim_analytics_gate` | `OPEN_LOOP` | Fuel status is Open_Loop_Fault, blocking trim analytics |
| `pid_case_26_gate_o2_fault_active` | `trim_analytics_gate` | `O2_FAULT_ACTIVE` | Active O2 sensor DTC (P0130), blocking trim analytics |
| `pid_case_27_gate_ckp_cmp_fault_active` | `trim_analytics_gate` | `CKP_CMP_FAULT_ACTIVE` | Active crankshaft position sensor DTC (P0335), blocking trim |
| `pid_case_28_gate_codes_recently_cleared` | `trim_analytics_gate` | `CODES_RECENTLY_CLEARED` | Less than 1 drive cycle since code clear, blocking trim |
| `pid_case_29_gate_wot_active` | `trim_analytics_gate` | `WOT_ACTIVE` | Wide open throttle (throttle_pos >= 90%), blocking trim |
| `pid_case_30_gate_dfco_active` | `trim_analytics_gate` | `DFCO_ACTIVE` | Decel fuel cut-off active, blocking trim |
| `pid_case_31_rej_maf_out_of_bounds` | `PIDValidationError` | Bounds violation | `mass_airflow_gps` = 700.0 exceeds 655.35 g/s limit |
| `pid_case_32_rej_temp_out_of_bounds` | `PIDValidationError` | Bounds violation | `coolant_temp_c` = 999.0 exceeds 140.0°C limit |
| `pid_case_33_rej_vacuum_out_of_bounds` | `PIDValidationError` | Bounds violation | `manifold_vacuum_kpa` = 999.0 exceeds 255.0 kPa limit |
| `pid_case_34_rej_bank2_null_contract_violation` | `PIDValidationError` | Bank-2 contract breach | Bank-2 trims present on a 1-bank (4-cylinder) engine |
| `pid_case_35_rej_dna_rpm_limit_breach` | `PIDValidationError` | Rated RPM exceedance | Engine RPM (6500) exceeds high-confidence rated RPM (6000 * 1.05) |
| `pid_case_36_rej_physics_gate_1_violation` | `SemanticConsistencyError` | Moving while stalled | VSS = 25 km/h while engine RPM = 200 (stalled) |
| `pid_case_37_rej_physics_gate_2_violation` | `SemanticConsistencyError` | Open Loop cold when hot | Fuel system status is Open_Loop_Cold while ECT = 85.0°C (hot) |
| `pid_case_38_rej_physics_gate_3_violation` | `SemanticConsistencyError` | High VE ceiling at idle | VE = 95.0% on a naturally aspirated engine at STABILIZED_IDLE |
| `pid_case_39_misfire_active` | `trim_analytics_gate` | `VALID` | Active P0300 misfire DTC is warm-idle non-blocking |
| `pid_case_40_catalyst_efficiency_low` | `trim_analytics_gate` | `VALID` | Active P0420 catalyst efficiency DTC is warm-idle non-blocking |
| `pid_case_41_evap_leak` | `trim_analytics_gate` | `VALID` | Active P0442 EVAP leak DTC is warm-idle non-blocking |
| `pid_case_42_egr_flow_low` | `trim_analytics_gate` | `VALID` | Active P0401 EGR flow DTC is warm-idle non-blocking |
| `pid_case_43_maf_circuit_fault` | `trim_analytics_gate` | `VALID` | Active P0103 MAF circuit DTC is warm-idle non-blocking |
| `pid_case_44_map_circuit_fault` | `trim_analytics_gate` | `VALID` | Active P0107 MAP circuit DTC is warm-idle non-blocking |
| `pid_case_45_ambient_temp_sensor_fault` | `trim_analytics_gate` | `VALID` | Active P0070 ambient temp sensor DTC is warm-idle non-blocking |
| `pid_case_46_throttle_pedal_sensor_fault` | `trim_analytics_gate` | `VALID` | Active P0220 throttle sensor DTC is warm-idle non-blocking |
| `pid_case_47_transmission_fault` | `trim_analytics_gate` | `VALID` | Active P0700 transmission DTC is warm-idle non-blocking |
| `pid_case_48_warm_idle_stoich_volvo_s60` | *Baseline Stoich / Healthy* | `ve_validity`: `VALID`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `0.0` | 2.5L I5 Turbo, DUAL_MAF_MAP, WIDEBAND_NB_SIM, warm idle baseline |
| `pid_case_49_warm_idle_stoich_mazda_3` | *Baseline Stoich / Healthy* | `ve_validity`: `VALID`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `0.0` | 1.8L I4 NA, DUAL_MAF_MAP, WIDEBAND_LINEAR, warm idle baseline |
| `pid_case_50_warm_idle_stoich_ford_escort` | *Baseline Stoich / Healthy* | `ve_validity`: `VALID`<br>`normalized_obd_lambda`: `1.00`<br>`total_trim_correction_delta`: `0.0` | 2.0L I4 NA, DUAL_MAF_MAP, NARROWBAND, warm idle baseline |
