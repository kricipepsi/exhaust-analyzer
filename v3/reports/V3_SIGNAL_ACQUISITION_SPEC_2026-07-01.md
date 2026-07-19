# V3_SIGNAL_ACQUISITION_SPEC_2026-07-01

**Task:** `T-V3-P4-1`  **Mode:** DISCLOSE only  **Writes engine code:** no

This is the owner data-acquisition contract for Phase 4. It names the corpus columns, producer state, consumer rule, cases unlocked, and abstain fallback for each signal pack. It does not add corpus columns, synthesize values, modify rules, or change the yardstick.

## Tier 1 — headline acquisition matrix

| Cluster | Measurement | Feasibility | New corpus column(s) | Producer state | Consumer rule | Residual cases mapped | Running cumulative |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C2 | Mode $06 catalyst monitor + fuel trims; optional pre/post-cat or upstream/downstream O2/5-gas conversion check | Tier (a) OBD Mode $01/$06 first; Tier (b) existing 5-gas used as dual-point/dual-probe corroboration | mode06_catalyst_margin_pct, catalyst_index_ratio, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct | OBDLab CatalystMonitorState plus GASLab CatalystConversionState | labs/comlab/registry/rules/rich_mixture.json RM-001/RM-003/RM-004 and catalyst_failure.json CF-001/CF-002/CF-006/CF-007 | 22 | 22 |
| C9 | OBD health-confirmation bundle: readiness complete, no stored/pending/permanent DTCs, Mode $06 margins, trim stability, two-point gas stability | Tier (a) OBD Mode $01/$03/$07/$06 plus Mode $0A/Service $09 when supported; Tier (b) two-point 5-gas corroboration | readiness_supported_complete_bool, stored_dtc_count, pending_dtc_count, permanent_dtc_count, mode06_min_margin_pct, warmup_cycles_since_clear, miles_since_clear, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, gas_delta_hc_ppm, gas_delta_co_pct, gas_delta_co2_pct, gas_delta_o2_pct | OBDLab NoFaultEvidenceState | labs/comlab/registry/rules/no_fault.json NF-001/NF-002 | 11 | 33 |
| C5 | STFT/LTFT across idle, 2500 rpm, and load/WOT; calculated load/MAF and fuel pressure under load | Tier (a) OBD live PIDs where supported; Tier (c) fuel-pressure gauge/transducer where rail pressure PID absent | stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct, calc_load_wot_pct, maf_gps_idle, maf_gps_2500, fuel_rail_pressure_load_kpa, wideband_lambda_wot | OBDLab LeanRootCauseState | labs/comlab/registry/rules/lean_condition.json LC-001/LC-002/LC-003 plus exhaust_leak.json EL-001 when C4 consumes the shared trim columns | 10 | 43 |
| C8 | Cranking evidence bundle: RPM, relative compression, cranking vacuum, fuel pressure, injector pulse, spark, immobilizer/security status | Tier (a) OBD RPM/DTC/freeze-frame where supported; Tier (c) vacuum gauge, fuel-pressure gauge, spark tester, noid light/scope, current clamp | crank_rpm, cranking_vacuum_inhg, koeo_fuel_pressure_kpa, cranking_fuel_pressure_kpa, injector_pulse_ms, spark_present_bool, immobilizer_active_bool, relative_compression_min_pct | OBDLab NonStarterCrankState | labs/comlab/registry/rules/non_starter.json NS-001/NS-002/NS-003/NS-004 | 6 | 49 |
| C1 | Mode $06 per-cylinder misfire/freeze-frame + cooling headspace HC/block test + compression/leak-down or relative compression + two-point HC/O2 behavior | Tier (a) OBD Mode $06/freeze-frame; Tier (b) existing 5-gas for coolant headspace/two-point tailpipe; Tier (c) compression/leak-down/current clamp | mode06_misfire_counts_json, misfire_cold_start_seconds, cooling_headspace_hc_ppm, relative_compression_min_pct, leakdown_pct, two_point_hc_delta_ppm, tailpipe_o2_2500_pct | OBDLab MisfireLocalizerState plus GASLab MechanicalWearEvidenceState | labs/comlab/registry/rules/mechanical_wear.json MW-001/MW-002/MW-003/MW-007/MW-008/MW-009 and misfire.json MF-001/MF-005 | 5 | 54 |
| C3 | KOEO MAP-vs-BARO plausibility, module supply/ground voltage under load, gas-vs-OBD lambda divergence, bidirectional response | Tier (a) OBD live data for MAP/BARO/trims/voltage; Tier (b) 5-gas for physical lambda; Tier (c) DMM/breakout/bidirectional scan tool | koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta, bidirectional_fuel_response_ok_bool | OBDLab ControlPlausibilityState | labs/comlab/registry/rules/ecu_fault.json EF-001/EF-002/EF-003 and sensor_fault.json SF-001/SF-002 when dispersion presents as sensor bias | 21 | 75 |
| C6 | Mode $06 O2-sensor dynamics with rich↔lean response fallback; MAF actual-vs-calculated airflow plausibility | Tier (a) OBD Mode $06/live PIDs when decisive; Tier (c) scope for millisecond response or missing scan-tool dynamics | mode06_o2_response_margin_pct, o2_rich_to_lean_ms, o2_lean_to_rich_ms, maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, calc_airflow_gps_2500 | OBDLab SensorDynamicsState | labs/comlab/registry/rules/sensor_fault.json SF-005/SF-008/SF-001/SF-002 and no_fault.json NF-001/NF-002 for healthy-vs-under-detected split | 14 | 89 |
| C7 | VVT command-vs-actual angle, cam-to-crank correlation, VE/MAF-at-RPM signature | Tier (a) OBD live data/DTC/freeze-frame when supported; Tier (c) scope/OEM tool for cam correlation if generic PIDs unavailable | vvt_command_deg, vvt_actual_deg, vvt_tracking_error_deg, cam_crank_correlation_deg, ve_idle_pct, ve_2500_load_pct, maf_gps_2500_load | OBDLab CamVvtEvidenceState plus GASLab CamTimingState | labs/comlab/registry/rules/cam_timing.json CT-001/CT-002/CT-004/CT-005/CT-007/CT-008 | 3 | 92 |

**C4 note:** C4 is not a new-column ask; its residuals consume the shared C5 trim/load columns and C6 O2/MAF dynamics columns. C4 residual cases mapped in Tier 3: **11**.

**Reconciliation:** residual rows mapped = 103 = PRODUCER_GAP·SIGNAL_REQUIRED 23 + DATA_GAP·ACQUISITION_GAP 19 + OUTRANKED·HARD 49 + TUNABLE_HELD 12. No engine/scorer/oracle/CSV/registry/lab file is modified; cases without supplied signal stay abstained.

## Tier 2 — per-cluster contracts

### C2 — rich mixture vs catalyst failure

1. **Discriminating measurement:** Mode $06 catalyst monitor + fuel trims; optional pre/post-cat or upstream/downstream O2/5-gas conversion check
2. **Corpus column contract:** `mode06_catalyst_margin_pct, catalyst_index_ratio, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct`. Units: %, ratio, %, %, %, %, ppm, %. Allowed range/enum: margin >= 10% pass-band; index_ratio <= 0.20 pass / high ratio fail; total trim near 0 for catalyst, <= -10% for true rich; nullable if tool unsupported. Acquisition maneuver: Warm closed-loop; hold 2500±100 rpm for 120 s; collect idle trims; read Mode $06 catalyst monitor; if available compare pre/post catalyst gas or upstream/downstream O2 during lean/rich perturbation.
3. **Producer state:** OBDLab CatalystMonitorState plus GASLab CatalystConversionState. Bound/threshold: Rich producer emits TRUE_RICH when negative trims are sustained; catalyst producer emits LOW_OSC_OR_HIGH_INDEX when Mode $06 margin/index fails without rich trims.
4. **Consumer rule:** labs/comlab/registry/rules/rich_mixture.json RM-001/RM-003/RM-004 and catalyst_failure.json CF-001/CF-002/CF-006/CF-007. Separates: rich_mixture from catalyst_failure, and C2 catalyst-vs-lean/rich runner-ups.
5. **Cases unlocked:** 22 mapped residual rows (OUTRANKED_HARD=11, PRODUCER_GAP_SIGNAL_REQUIRED=11): CASE-015, CSV-100, CSV-121, CSV-122, EXP-N017, EXT-232, EXT-233, PDF-HI-006, case_004, era1_017, era2_015, CASE-023, CASE-029, CASE-040, EXT-217, PDF-HI-001, RULE-CO-1, YAML-PDF_HI_001, case_002, case_015, case_017, era2_019.
6. **Abstain fallback:** If Mode $06 catalyst data and fuel trims are absent, leave the case abstained; a single downstream tailpipe snapshot is not a discriminator.
**Research source:** `cluster2.md §Evaluation/Protocol/Quantitative Signatures`.

### C9 — confirm no fault reliably

1. **Discriminating measurement:** OBD health-confirmation bundle: readiness complete, no stored/pending/permanent DTCs, Mode $06 margins, trim stability, two-point gas stability
2. **Corpus column contract:** `readiness_supported_complete_bool, stored_dtc_count, pending_dtc_count, permanent_dtc_count, mode06_min_margin_pct, warmup_cycles_since_clear, miles_since_clear, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, gas_delta_hc_ppm, gas_delta_co_pct, gas_delta_co2_pct, gas_delta_o2_pct`. Units: bool, count, count, count, %, cycles, miles, %, %, %, %, ppm, %, %, %. Allowed range/enum: all readiness complete; DTC counts 0; Mode $06 margin >= 10%; warmups>=15 and miles>=200 when available; trims near zero; gas stable. Acquisition maneuver: Warm closed-loop; read OBD status before any clear; capture stable idle and 2500 rpm no-load trim/gas windows.
3. **Producer state:** OBDLab NoFaultEvidenceState. Bound/threshold: Emit HEALTH_CONFIRMED only when OBD bundle is complete and non-marginal; otherwise emit HEALTH_UNPROVEN_ABSTAIN.
4. **Consumer rule:** labs/comlab/registry/rules/no_fault.json NF-001/NF-002. Separates: no_fault from catalyst-masked, sensor-under-detected, ECU/control, and intermittent pending faults.
5. **Cases unlocked:** 11 mapped residual rows (DATA_GAP_ACQUISITION_GAP=10, TUNABLE_HELD=1): CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014, era2_016.
6. **Abstain fallback:** If any OBD health evidence is unsupported, incomplete, marginal, contradictory, or freshly reset, leave the case abstained.
**Research source:** `cluster9.1.md §Bottom Line/Decision Rule and cluster9.2.md §Recommended decision rule`.

### C5 — lean-condition root cause

1. **Discriminating measurement:** STFT/LTFT across idle, 2500 rpm, and load/WOT; calculated load/MAF and fuel pressure under load
2. **Corpus column contract:** `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct, calc_load_wot_pct, maf_gps_idle, maf_gps_2500, fuel_rail_pressure_load_kpa, wideband_lambda_wot`. Units: %, %, %, %, %, %, %, g/s, g/s, kPa, lambda. Allowed range/enum: vacuum leak: trim positive at idle then recovers at 2500; fuel delivery: lean worsens under load with pressure drop >35 kPa; MAF under-read: peak load <80% with positive trims. Acquisition maneuver: Warm closed-loop; 60 s idle; 30 s 2500±100 rpm no-load; safe WOT/load sweep where available; sample >=10 Hz.
3. **Producer state:** OBDLab LeanRootCauseState. Bound/threshold: Emit VACUUM_LEAK_TRIM_PATTERN, FUEL_DELIVERY_SHORTFALL, or MAF_UNDERREAD based on multi-point trim/load/pressure signature.
4. **Consumer rule:** labs/comlab/registry/rules/lean_condition.json LC-001/LC-002/LC-003 plus exhaust_leak.json EL-001 when C4 consumes the shared trim columns. Separates: lean_condition sub-causes and shared C4 exhaust-leak/true-lean collisions.
5. **Cases unlocked:** 10 mapped residual rows (DATA_GAP_ACQUISITION_GAP=5, OUTRANKED_HARD=4, TUNABLE_HELD=1): EXP-N011, EXP-N022, EXP-N029, case_003, case_016, CSV-113, CSV-114, REAL-004, era1_001, era3_015.
6. **Abstain fallback:** If only one warm-idle trim/gas point is available, leave the case abstained.
**Research source:** `cluster5.md §Multi-Point Diagnostic Acquisition Protocol/Signal Evaluation`.

### C8 — non-starter root cause

1. **Discriminating measurement:** Cranking evidence bundle: RPM, relative compression, cranking vacuum, fuel pressure, injector pulse, spark, immobilizer/security status
2. **Corpus column contract:** `crank_rpm, cranking_vacuum_inhg, koeo_fuel_pressure_kpa, cranking_fuel_pressure_kpa, injector_pulse_ms, spark_present_bool, immobilizer_active_bool, relative_compression_min_pct`. Units: rpm, inHg, kPa, kPa, ms, bool, bool, %. Allowed range/enum: rpm=0 -> CKP path; vacuum <3 inHg or relative compression <85% -> compression; low pressure -> fuel; pulse 0 -> ECU/immobilizer; no spark -> ignition. Acquisition maneuver: No-start crank test; 10-15 s maximum crank with 2 min cooldown; collect OBD while cranking plus shop measurements.
3. **Producer state:** OBDLab NonStarterCrankState. Bound/threshold: Emit the no-start substate indicated by the first positive cranking discriminator.
4. **Consumer rule:** labs/comlab/registry/rules/non_starter.json NS-001/NS-002/NS-003/NS-004. Separates: non_starter root causes from invalid ambient-air exhaust samples and misfire-like no-starts.
5. **Cases unlocked:** 6 mapped residual rows (DATA_GAP_ACQUISITION_GAP=1, OUTRANKED_HARD=1, PRODUCER_GAP_SIGNAL_REQUIRED=4): REAL-002, case_006, REAL-001, REAL-003, case_007, case_040.
6. **Abstain fallback:** If cranking data are absent, keep no-start rows abstained; warm-idle gas cannot exist for these cases.
**Research source:** `cluster8.md §Diagnostic Acquisition Protocol/Signature Table`.

### C1 — mechanical wear vs misfire vs coolant intrusion

1. **Discriminating measurement:** Mode $06 per-cylinder misfire/freeze-frame + cooling headspace HC/block test + compression/leak-down or relative compression + two-point HC/O2 behavior
2. **Corpus column contract:** `mode06_misfire_counts_json, misfire_cold_start_seconds, cooling_headspace_hc_ppm, relative_compression_min_pct, leakdown_pct, two_point_hc_delta_ppm, tailpipe_o2_2500_pct`. Units: json, s, ppm, %, %, ppm, %. Allowed range/enum: coolant breach: headspace HC >50 ppm; mechanical loss: compression <90 psi or relative <85%; ignition misfire: elevated O2 around 5% with normal compression; valve-seal plume uses sustained two-point HC, not snap folklore. Acquisition maneuver: Cold-start OBD misfire capture; warm coolant headspace sniff; cranking compression/leak-down; idle then 2500 rpm 5-gas hold.
3. **Producer state:** OBDLab MisfireLocalizerState plus GASLab MechanicalWearEvidenceState. Bound/threshold: Emit COOLANT_INTRUSION, COMPRESSION_LOSS, OIL_BURNING_PATTERN, or IGNITION_MISFIRE_CORROBORATED from the combined evidence.
4. **Consumer rule:** labs/comlab/registry/rules/mechanical_wear.json MW-001/MW-002/MW-003/MW-007/MW-008/MW-009 and misfire.json MF-001/MF-005. Separates: mechanical_wear from ignition/misfire and coolant-intrusion lookalikes.
5. **Cases unlocked:** 5 mapped residual rows (OUTRANKED_HARD=2, PRODUCER_GAP_SIGNAL_REQUIRED=3): PDF-4G-04, case_044, CSV-117, EXP-N030, MECH-001.
6. **Abstain fallback:** If OBD misfire/cooling/compression evidence is not supplied, keep the case abstained rather than using HC alone.
**Research source:** `cluster1.md §Comparative Framework/Critical Signal Evaluation`.

### C3 — ECU/control-system fault

1. **Discriminating measurement:** KOEO MAP-vs-BARO plausibility, module supply/ground voltage under load, gas-vs-OBD lambda divergence, bidirectional response
2. **Corpus column contract:** `koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta, bidirectional_fuel_response_ok_bool`. Units: kPa, V, V, lambda, lambda, bool. Allowed range/enum: MAP-BARO delta >=5 kPa, ground drop >0.20 V, ground joint >0.10 V, lambda divergence >=0.05, trims railed ±25%, active response absent/reversed. Acquisition maneuver: KOEO pressure/voltage gate; high electrical load ground test; warm closed-loop 5-gas+OBD capture; optional +25%/-12.5% fuel command response.
3. **Producer state:** OBDLab ControlPlausibilityState. Bound/threshold: Emit CONTROL_REFERENCE_FAULT when electrical/reference or gas-vs-OBD divergence gates pass.
4. **Consumer rule:** labs/comlab/registry/rules/ecu_fault.json EF-001/EF-002/EF-003 and sensor_fault.json SF-001/SF-002 when dispersion presents as sensor bias. Separates: ecu_fault/control dispersion from true lean/rich/sensor/catalyst chemistry.
5. **Cases unlocked:** 21 mapped residual rows (OUTRANKED_HARD=18, PRODUCER_GAP_SIGNAL_REQUIRED=3): CSV-041, CSV-045, CSV-123, CSV-124, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-TC47, case_001, case_013, CSV-125, CSV-126, YAML-RULE_NOx_1.
6. **Abstain fallback:** If no KOEO plausibility or voltage/divergence data are supplied, keep control-dispersion cases abstained.
**Research source:** `cluster3.md §Acquisition Protocols/Quantitative Diagnostic Signature Mapping`.

### C6 — sensor fault under-detection

1. **Discriminating measurement:** Mode $06 O2-sensor dynamics with rich↔lean response fallback; MAF actual-vs-calculated airflow plausibility
2. **Corpus column contract:** `mode06_o2_response_margin_pct, o2_rich_to_lean_ms, o2_lean_to_rich_ms, maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, calc_airflow_gps_2500`. Units: %, ms, ms, %, %, g/s, g/s, g/s, g/s. Allowed range/enum: use vehicle Mode $06 limits; O2 slower than OEM limit is fault; MAF sustained >10-15% low vs modeled airflow at both points is provisional fault. Acquisition maneuver: Warm closed-loop; read Mode $06; if absent/equivocal, hold ~2500 rpm then decel fuel cut and controlled return; capture MAF/MAP/IAT/BARO/RPM at idle and 2500.
3. **Producer state:** OBDLab SensorDynamicsState. Bound/threshold: Emit O2_LAZY_OR_BIASED, MAF_UNDERREAD, or SENSOR_HEALTH_UNPROVEN_ABSTAIN.
4. **Consumer rule:** labs/comlab/registry/rules/sensor_fault.json SF-005/SF-008/SF-001/SF-002 and no_fault.json NF-001/NF-002 for healthy-vs-under-detected split. Separates: sensor_fault from no_fault, misfire, lean, and catalyst lookalikes.
5. **Cases unlocked:** 14 mapped residual rows (DATA_GAP_ACQUISITION_GAP=3, OUTRANKED_HARD=6, TUNABLE_HELD=5): CASE-045, CASE-048, YAML-TC46, CASE-014, EXT-229, EXT-230, YAML-CSV25, case_046, era1_006, CSV-025, EXP-N020, PDF-4G-05, TC-046, era2_012.
6. **Abstain fallback:** If only static O2/MAF values are supplied, keep the case abstained.
**Research source:** `cluster6.md §Question One/Three/Four Answers`.

### C7 — cam timing / VVT fault

1. **Discriminating measurement:** VVT command-vs-actual angle, cam-to-crank correlation, VE/MAF-at-RPM signature
2. **Corpus column contract:** `vvt_command_deg, vvt_actual_deg, vvt_tracking_error_deg, cam_crank_correlation_deg, ve_idle_pct, ve_2500_load_pct, maf_gps_2500_load`. Units: deg, deg, deg, deg, %, %, g/s. Allowed range/enum: tracking error beyond OEM tolerance; cam-crank correlation fault/P0016-class; depressed VE/MAF at 2500 load compared with expected displacement/RPM model. Acquisition maneuver: Warm engine; baseline idle; WOT or loaded sweep; 2500±50 rpm at 50-70% calculated load for 30 s; sample >=10 Hz.
3. **Producer state:** OBDLab CamVvtEvidenceState plus GASLab CamTimingState. Bound/threshold: Emit VVT_TRACKING_FAULT, STATIC_CAM_CORRELATION_FAULT, or VE_DEPRESSED_CAM_TIMING_PATTERN.
4. **Consumer rule:** labs/comlab/registry/rules/cam_timing.json CT-001/CT-002/CT-004/CT-005/CT-007/CT-008. Separates: cam_timing/VVT from misfire, sensor, and chemically non-normal exhaust.
5. **Cases unlocked:** 3 mapped residual rows (PRODUCER_GAP_SIGNAL_REQUIRED=2, TUNABLE_HELD=1): EXP-N023, era1_011, era2_011.
6. **Abstain fallback:** If cam/VVT or VE evidence is unavailable, keep cam-timing residuals abstained.
**Research source:** `cluster7.md §Evaluation/Acquisition Protocol`.

### C4 — shared residual note (not a separate new-column ask)

C4 is not a new-column ask; its residuals consume the shared C5 trim/load columns and C6 O2/MAF dynamics columns.

C4 cases: CSV-129, CSV-130, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95, CASE-020, CASE-022, EXT-211, EXT-212.
Producer/consumer path: C5 `LeanRootCauseState` for true-lean vs load/trim behavior plus C6 `SensorDynamicsState` for biased/lazy O2 behavior; consumers are `EL-001/EL-003`, `LC-001/LC-002`, and `SF-001/SF-002/SF-008` in the existing registry rule families.
Abstain fallback: absent shared trim/load/O2 dynamics, these stay abstained; no independent C4 corpus column is requested here.

## Tier 3 — JSON per-case unlock table

Machine-readable table: `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json`.

## Honest gaps and abstain policy

No residual row is left unmapped. All mapped rows remain `abstain-if-absent` until the owner supplies the named real measurement; no synthetic value may be filled.
