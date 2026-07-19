# V3_MIN_SIGNAL_SET_2026-07-01

**Task:** `T-V3-P4-2`  **Mode:** DISCLOSE only  **Writes engine code:** no

## Headline

The cheapest first move is **A1_TRIMS — enable live fuel trims at idle and 2500 rpm**. It reaches 50 residual cases across C2/C4/C5/C9 for one Tier-a OBD action, but it is a shared start, not a standalone unlock. The first full signal pack should still be **T-V3-P4-C2**: C2 has 22 canonical cases, uses that same trim action plus Mode $06 catalyst data, and is cheaper than the C3 control-plausibility bundle. `CASE-039` is folded into C3 as a +1 overlay, so the operating set reconciles to 104 cases.

## Corrected cluster yield order

This supersedes `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md`'s stale `ordered_clusters` for owner sequencing.

| Rank | Cluster | Spec count | Effective count with CASE-039 | Note |
| ---: | --- | ---: | ---: | --- |
| 1 | C2 | 22 | 22 |  |
| 2 | C3 | 21 | 22 | includes CASE-039 overlay |
| 3 | C6 | 14 | 14 |  |
| 4 | C9 | 11 | 11 |  |
| 5 | C4 | 11 | 11 |  |
| 6 | C5 | 10 | 10 |  |
| 7 | C8 | 6 | 6 |  |
| 8 | C1 | 5 | 5 |  |
| 9 | C7 | 3 | 3 |  |

## Minimum added-signal set — greedy shop-action order

Cost scale: Tier-a = 1, Tier-b = 2, Tier-c = 3, Tier-d = 5. `Marginal cases` counts cases newly reached by at least one column from the action. `Full unlock cases` counts cases whose complete current column contract is contained inside that one action. Shared columns lower acquisition cost; they do **not** independently unlock a case until the cluster's decisive producer signal is present.

| Rank | Action | Tier | Cost | Marginal cases | Marginal / cost | Cumulative cases | Clusters reached | Full unlock cases |
| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| 1 | A2_MODE06_EMISSIONS: Read Mode $06 catalyst, O2, no-fault, and misfire monitors | a | 1 | 63 | 63.0 | 63 | C1, C2, C4, C6, C9 | 0 |
| 2 | A6_TWO_POINT_5GAS: Use existing 5-gas analyzer differently: two-point/delta/pre-post catalyst/headspace | b | 2 | 22 | 11.0 | 85 | C1, C2, C3, C9 | 0 |
| 3 | A4_MAF_LOAD: Log MAF/load/airflow plausibility at idle, 2500 rpm, and load | a | 1 | 10 | 10.0 | 95 | C4, C5, C6 | 0 |
| 4 | A8_COMPRESSION_LEAKDOWN: Compression/leak-down or relative-compression mechanical check | c | 3 | 6 | 2.0 | 101 | C1, C8 | 0 |
| 5 | A10_VVT_CAM: VVT command/actual, cam correlation, and loaded VE capture | a/c | 3 | 3 | 1.0 | 104 | C7 | 3 |

## Shop-action details

### A1_TRIMS — Enable live fuel trims at idle and 2500 rpm

- **Tier/cost:** a / 1
- **Columns:** `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct`
- **Clusters reached:** C2, C4, C5, C9
- **Cases reached:** 54 (CASE-015, CASE-020, CASE-022, CASE-023, CASE-029, CASE-040, CSV-100, CSV-113, CSV-114, CSV-121, CSV-122, CSV-127, CSV-128, CSV-129, CSV-130, EXP-N011, EXP-N017, EXP-N022, EXP-N029, EXT-211, EXT-212, EXT-216, EXT-217, EXT-232, EXT-233, EXT-238, EXT-239, PDF-HI-001, PDF-HI-005, PDF-HI-006, PDF-HI-007, PDF-HI-010, REAL-004, RULE-CO-1, TC-048, YAML-CSV95, YAML-PDF_HI_001, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_002, case_003, case_004, case_014, case_015, case_016, case_017, era1_001, era1_017, era2_015, era2_016, era2_019, era3_014, era3_015)
- **Full unlock cases:** 0 (none)
- **Research basis:** RESEARCH_PROMPT output item 3; cluster4.md §1.7; cluster5.md §Multi-Point Diagnostic Acquisition Protocol
- **Caveat:** Shared OBD Mode $01 start point; reaches C2/C4/C5/C9 but is not alone decisive for any cluster.

### A2_MODE06_EMISSIONS — Read Mode $06 catalyst, O2, no-fault, and misfire monitors

- **Tier/cost:** a / 1
- **Columns:** `mode06_catalyst_margin_pct, catalyst_index_ratio, mode06_min_margin_pct, mode06_o2_response_margin_pct, mode06_misfire_counts_json, misfire_cold_start_seconds`
- **Clusters reached:** C1, C2, C4, C6, C9
- **Cases reached:** 63 (CASE-014, CASE-015, CASE-020, CASE-022, CASE-023, CASE-029, CASE-040, CASE-045, CASE-048, CSV-025, CSV-100, CSV-117, CSV-121, CSV-122, CSV-127, CSV-128, CSV-129, CSV-130, EXP-N017, EXP-N020, EXP-N030, EXT-211, EXT-212, EXT-216, EXT-217, EXT-229, EXT-230, EXT-232, EXT-233, EXT-238, EXT-239, MECH-001, PDF-4G-04, PDF-4G-05, PDF-HI-001, PDF-HI-005, PDF-HI-006, PDF-HI-007, PDF-HI-010, RULE-CO-1, TC-046, TC-048, YAML-CSV25, YAML-CSV95, YAML-PDF_HI_001, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, YAML-TC46, case_002, case_004, case_014, case_015, case_017, case_044, case_046, era1_006, era1_017, era2_012, era2_015, era2_016, era2_019, era3_014)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster2.md §Instrumentation Feasibility Tiers; cluster6.md §Question One Answer; cluster1.md §On-Board Diagnostics Mode 06
- **Caveat:** Cheap scan-tool read before any code clear; decisive only when paired with each cluster's corroborating columns.

### A3_OBD_HEALTH — Capture OBD health/readiness and reset-age counters

- **Tier/cost:** a / 1
- **Columns:** `readiness_supported_complete_bool, stored_dtc_count, pending_dtc_count, permanent_dtc_count, warmup_cycles_since_clear, miles_since_clear`
- **Clusters reached:** C9
- **Cases reached:** 11 (CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era2_016, era3_014)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster9.1.md §Bottom Line/Decision Rule and cluster9.2.md §Recommended decision rule
- **Caveat:** No-fault gate; supports C9 only, and unsupported/freshly reset vehicles remain abstained.

### A4_MAF_LOAD — Log MAF/load/airflow plausibility at idle, 2500 rpm, and load

- **Tier/cost:** a / 1
- **Columns:** `maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, calc_airflow_gps_2500, maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, calc_load_wot_pct, stft_load_pct, ltft_load_pct, wideband_lambda_wot`
- **Clusters reached:** C4, C5, C6
- **Cases reached:** 35 (CASE-014, CASE-020, CASE-022, CASE-045, CASE-048, CSV-025, CSV-113, CSV-114, CSV-129, CSV-130, EXP-N011, EXP-N020, EXP-N022, EXP-N029, EXT-211, EXT-212, EXT-229, EXT-230, EXT-238, EXT-239, PDF-4G-05, PDF-HI-007, REAL-004, TC-046, TC-048, YAML-CSV25, YAML-CSV95, YAML-TC46, case_003, case_016, case_046, era1_001, era1_006, era2_012, era3_015)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster5.md §Bottom Line Diagnostic Recommendation; cluster6.md §Question Three/Four Answers
- **Caveat:** Shared OBD live-PID action for lean/sensor/exhaust-leak splits; WOT/load parts are safety- and vehicle-dependent.

### A5_CONTROL_PLAUSIBILITY — Run KOEO MAP/BARO plus control-module voltage/lambda plausibility

- **Tier/cost:** a/b/c / 3
- **Columns:** `koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta, bidirectional_fuel_response_ok_bool`
- **Clusters reached:** C3
- **Cases reached:** 22 (CASE-039, CSV-041, CSV-045, CSV-123, CSV-124, CSV-125, CSV-126, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-RULE_NOx_1, YAML-TC47, case_001, case_013)
- **Full unlock cases:** 22 (CASE-039, CSV-041, CSV-045, CSV-123, CSV-124, CSV-125, CSV-126, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-RULE_NOx_1, YAML-TC47, case_001, case_013)
- **Research basis:** cluster3.md §Acquisition Protocols/Quantitative Diagnostic Signature Mapping; V3_P4_CLASSIFIER_FIXABLE_RECHECK CASE-039 reroute
- **Caveat:** C3 decisive bundle; includes Tier-a/b observations but true confirmation may need DMM/breakout or bidirectional response.

### A6_TWO_POINT_5GAS — Use existing 5-gas analyzer differently: two-point/delta/pre-post catalyst/headspace

- **Tier/cost:** b / 2
- **Columns:** `pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct, gas_delta_hc_ppm, gas_delta_co_pct, gas_delta_co2_pct, gas_delta_o2_pct, gas_obd_lambda_delta, lambda_perception_delta, cooling_headspace_hc_ppm, two_point_hc_delta_ppm, tailpipe_o2_2500_pct`
- **Clusters reached:** C1, C2, C3, C9
- **Cases reached:** 60 (CASE-015, CASE-023, CASE-029, CASE-039, CASE-040, CSV-041, CSV-045, CSV-100, CSV-117, CSV-121, CSV-122, CSV-123, CSV-124, CSV-125, CSV-126, CSV-127, CSV-128, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N017, EXP-N018, EXP-N019, EXP-N030, EXT-216, EXT-217, EXT-221, EXT-232, EXT-233, MECH-001, PDF-4G-04, PDF-HI-001, PDF-HI-005, PDF-HI-006, PDF-HI-010, RULE-CO-1, TC-021, YAML-CSV41, YAML-CSV45, YAML-PDF_HI_001, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-RULE_NOx_1, YAML-TC1, YAML-TC47, case_001, case_002, case_004, case_013, case_014, case_015, case_017, case_044, era1_017, era2_015, era2_016, era2_019, era3_014)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster1.md §Comparative Framework; cluster2.md §Protocol; cluster3.md §Quantitative Diagnostic Signature Mapping
- **Caveat:** Reuses the gas bench; completes parts of C1/C2/C3/C9 that static idle gas cannot decide.

### A7_CRANKING_BUNDLE — Collect cranking no-start evidence bundle

- **Tier/cost:** a/c / 3
- **Columns:** `crank_rpm, cranking_vacuum_inhg, koeo_fuel_pressure_kpa, cranking_fuel_pressure_kpa, injector_pulse_ms, spark_present_bool, immobilizer_active_bool, relative_compression_min_pct`
- **Clusters reached:** C1, C8
- **Cases reached:** 11 (CSV-117, EXP-N030, MECH-001, PDF-4G-04, REAL-001, REAL-002, REAL-003, case_006, case_007, case_040, case_044)
- **Full unlock cases:** 6 (REAL-001, REAL-002, REAL-003, case_006, case_007, case_040)
- **Research basis:** cluster8.md §Diagnostic Acquisition Protocol/Signature Table
- **Caveat:** Special-case no-start workflow; warm-idle gas cannot exist for these rows.

### A8_COMPRESSION_LEAKDOWN — Compression/leak-down or relative-compression mechanical check

- **Tier/cost:** c / 3
- **Columns:** `relative_compression_min_pct, leakdown_pct`
- **Clusters reached:** C1, C8
- **Cases reached:** 11 (CSV-117, EXP-N030, MECH-001, PDF-4G-04, REAL-001, REAL-002, REAL-003, case_006, case_007, case_040, case_044)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster1.md §Comparative Framework/Critical Signal Evaluation
- **Caveat:** Expensive but needed for mechanical-loss separation when Mode $06/headspace/two-point gas is insufficient.

### A9_O2_SCOPE_FALLBACK — Scope or active rich↔lean O2 response fallback

- **Tier/cost:** c / 3
- **Columns:** `o2_rich_to_lean_ms, o2_lean_to_rich_ms`
- **Clusters reached:** C4, C6
- **Cases reached:** 25 (CASE-014, CASE-020, CASE-022, CASE-045, CASE-048, CSV-025, CSV-129, CSV-130, EXP-N020, EXT-211, EXT-212, EXT-229, EXT-230, EXT-238, EXT-239, PDF-4G-05, PDF-HI-007, TC-046, TC-048, YAML-CSV25, YAML-CSV95, YAML-TC46, case_046, era1_006, era2_012)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster6.md §Question One/Three/Four Answers
- **Caveat:** Escalation when Mode $06 O2 dynamics are absent/equivocal or scan-tool timing is too coarse.

### A10_VVT_CAM — VVT command/actual, cam correlation, and loaded VE capture

- **Tier/cost:** a/c / 3
- **Columns:** `vvt_command_deg, vvt_actual_deg, vvt_tracking_error_deg, cam_crank_correlation_deg, ve_idle_pct, ve_2500_load_pct, maf_gps_2500_load`
- **Clusters reached:** C7
- **Cases reached:** 3 (EXP-N023, era1_011, era2_011)
- **Full unlock cases:** 3 (EXP-N023, era1_011, era2_011)
- **Research basis:** cluster7.md §Evaluation/Acquisition Protocol
- **Caveat:** Low-yield but decisive for the cam/VVT residuals; may require OEM tool or scope on generic-PID-poor vehicles.

### A11_FUEL_PRESSURE_LOAD — Fuel-pressure-under-load confirmation where rail PID is absent

- **Tier/cost:** c / 3
- **Columns:** `fuel_rail_pressure_load_kpa`
- **Clusters reached:** C4, C5
- **Cases reached:** 21 (CASE-020, CASE-022, CSV-113, CSV-114, CSV-129, CSV-130, EXP-N011, EXP-N022, EXP-N029, EXT-211, EXT-212, EXT-238, EXT-239, PDF-HI-007, REAL-004, TC-048, YAML-CSV95, case_003, case_016, era1_001, era3_015)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster5.md §Multi-Point Diagnostic Acquisition Protocol/Signal Evaluation
- **Caveat:** Escalates C5/C4 lean-source cases when live PIDs cannot prove fuel delivery shortfall.

### A12_BIDIRECTIONAL_RESPONSE — Bidirectional fuel-response check if passive C3 evidence is contradictory

- **Tier/cost:** c / 3
- **Columns:** `bidirectional_fuel_response_ok_bool`
- **Clusters reached:** C3
- **Cases reached:** 22 (CASE-039, CSV-041, CSV-045, CSV-123, CSV-124, CSV-125, CSV-126, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-RULE_NOx_1, YAML-TC47, case_001, case_013)
- **Full unlock cases:** 0 (none)
- **Research basis:** cluster3.md §Evaluation and Ranking of Diagnostic Candidates
- **Caveat:** Already included in C3 full bundle; listed separately so costly escalation is visible.

## Column → served index

| Column | Clusters | Case count | Shop actions |
| --- | --- | ---: | --- |
| `bidirectional_fuel_response_ok_bool` | C3 | 22 | A12_BIDIRECTIONAL_RESPONSE, A5_CONTROL_PLAUSIBILITY |
| `calc_airflow_gps_2500` | C4, C6 | 25 | A4_MAF_LOAD |
| `calc_airflow_gps_idle` | C4, C6 | 25 | A4_MAF_LOAD |
| `calc_load_wot_pct` | C4, C5 | 21 | A4_MAF_LOAD |
| `cam_crank_correlation_deg` | C7 | 3 | A10_VVT_CAM |
| `catalyst_index_ratio` | C2 | 22 | A2_MODE06_EMISSIONS |
| `cooling_headspace_hc_ppm` | C1 | 5 | A6_TWO_POINT_5GAS |
| `crank_rpm` | C8 | 6 | A7_CRANKING_BUNDLE |
| `cranking_fuel_pressure_kpa` | C8 | 6 | A7_CRANKING_BUNDLE |
| `cranking_vacuum_inhg` | C8 | 6 | A7_CRANKING_BUNDLE |
| `dlc_signal_ground_drop_v` | C3 | 22 | A5_CONTROL_PLAUSIBILITY |
| `fuel_rail_pressure_load_kpa` | C4, C5 | 21 | A11_FUEL_PRESSURE_LOAD |
| `gas_delta_co2_pct` | C9 | 11 | A6_TWO_POINT_5GAS |
| `gas_delta_co_pct` | C9 | 11 | A6_TWO_POINT_5GAS |
| `gas_delta_hc_ppm` | C9 | 11 | A6_TWO_POINT_5GAS |
| `gas_delta_o2_pct` | C9 | 11 | A6_TWO_POINT_5GAS |
| `gas_obd_lambda_delta` | C3 | 22 | A5_CONTROL_PLAUSIBILITY, A6_TWO_POINT_5GAS |
| `immobilizer_active_bool` | C8 | 6 | A7_CRANKING_BUNDLE |
| `injector_pulse_ms` | C8 | 6 | A7_CRANKING_BUNDLE |
| `koeo_fuel_pressure_kpa` | C8 | 6 | A7_CRANKING_BUNDLE |
| `koeo_map_baro_delta_kpa` | C3 | 22 | A5_CONTROL_PLAUSIBILITY |
| `lambda_perception_delta` | C3 | 22 | A5_CONTROL_PLAUSIBILITY, A6_TWO_POINT_5GAS |
| `leakdown_pct` | C1 | 5 | A8_COMPRESSION_LEAKDOWN |
| `ltft_2500_pct` | C2, C4, C5, C9 | 54 | A1_TRIMS |
| `ltft_idle_pct` | C2, C4, C5, C9 | 54 | A1_TRIMS |
| `ltft_load_pct` | C4, C5 | 21 | A4_MAF_LOAD |
| `maf_actual_calc_delta_pct_2500` | C4, C6 | 25 | A4_MAF_LOAD |
| `maf_actual_calc_delta_pct_idle` | C4, C6 | 25 | A4_MAF_LOAD |
| `maf_gps_2500` | C4, C5, C6 | 35 | A4_MAF_LOAD |
| `maf_gps_2500_load` | C7 | 3 | A10_VVT_CAM |
| `maf_gps_idle` | C4, C5, C6 | 35 | A4_MAF_LOAD |
| `miles_since_clear` | C9 | 11 | A3_OBD_HEALTH |
| `misfire_cold_start_seconds` | C1 | 5 | A2_MODE06_EMISSIONS |
| `mode06_catalyst_margin_pct` | C2 | 22 | A2_MODE06_EMISSIONS |
| `mode06_min_margin_pct` | C9 | 11 | A2_MODE06_EMISSIONS |
| `mode06_misfire_counts_json` | C1 | 5 | A2_MODE06_EMISSIONS |
| `mode06_o2_response_margin_pct` | C4, C6 | 25 | A2_MODE06_EMISSIONS |
| `module_voltage_loaded_v` | C3 | 22 | A5_CONTROL_PLAUSIBILITY |
| `o2_lean_to_rich_ms` | C4, C6 | 25 | A9_O2_SCOPE_FALLBACK |
| `o2_rich_to_lean_ms` | C4, C6 | 25 | A9_O2_SCOPE_FALLBACK |
| `pending_dtc_count` | C9 | 11 | A3_OBD_HEALTH |
| `permanent_dtc_count` | C9 | 11 | A3_OBD_HEALTH |
| `pre_post_cat_co_delta_pct` | C2 | 22 | A6_TWO_POINT_5GAS |
| `pre_post_cat_hc_delta_ppm` | C2 | 22 | A6_TWO_POINT_5GAS |
| `readiness_supported_complete_bool` | C9 | 11 | A3_OBD_HEALTH |
| `relative_compression_min_pct` | C1, C8 | 11 | A7_CRANKING_BUNDLE, A8_COMPRESSION_LEAKDOWN |
| `spark_present_bool` | C8 | 6 | A7_CRANKING_BUNDLE |
| `stft_2500_pct` | C2, C4, C5, C9 | 54 | A1_TRIMS |
| `stft_idle_pct` | C2, C4, C5, C9 | 54 | A1_TRIMS |
| `stft_load_pct` | C4, C5 | 21 | A4_MAF_LOAD |
| `stored_dtc_count` | C9 | 11 | A3_OBD_HEALTH |
| `tailpipe_o2_2500_pct` | C1 | 5 | A6_TWO_POINT_5GAS |
| `two_point_hc_delta_ppm` | C1 | 5 | A6_TWO_POINT_5GAS |
| `ve_2500_load_pct` | C7 | 3 | A10_VVT_CAM |
| `ve_idle_pct` | C7 | 3 | A10_VVT_CAM |
| `vvt_actual_deg` | C7 | 3 | A10_VVT_CAM |
| `vvt_command_deg` | C7 | 3 | A10_VVT_CAM |
| `vvt_tracking_error_deg` | C7 | 3 | A10_VVT_CAM |
| `warmup_cycles_since_clear` | C9 | 11 | A3_OBD_HEALTH |
| `wideband_lambda_wot` | C4, C5 | 21 | A4_MAF_LOAD |

## Recommended first pack

**Author `T-V3-P4-C2` first after owner data lands.** C2 remains the best first commit because its 22-case canonical yield is tied for the largest cluster, it consumes the cheapest shared start (`A1_TRIMS`) plus Tier-a Mode $06 catalyst evidence (`A2_MODE06_EMISSIONS`), and the same acquisition also starts C4/C5/C9. C3 becomes 22 effective cases after `CASE-039`, but its decisive bundle (`A5_CONTROL_PLAUSIBILITY`) may escalate to DMM/breakout or bidirectional tooling, so it is second for acquisition cost even though it is near-tied by yield.

## Reconciliation and honest gaps

- P4-1 residual rows: 103.
- `CASE-039` overlay: +1 C3 ECU/control signal row from `V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md`.
- Operating rows attributed to at least one shop action: 104 / 104.
- Unattributed cases: (none).
- Expensive-to-unlock cases are any row whose first decisive evidence needs Tier-c action (`A5_CONTROL_PLAUSIBILITY`, `A7_CRANKING_BUNDLE`, `A8_COMPRESSION_LEAKDOWN`, `A9_O2_SCOPE_FALLBACK`, `A10_VVT_CAM`, `A11_FUEL_PRESSURE_LOAD`, or `A12_BIDIRECTIONAL_RESPONSE`). They stay abstained until the owner supplies real measurements.
- Shared-column caveat: fuel trims, MAF, Mode $06, and two-point gas lower acquisition cost across clusters, but a case is not unlocked unless its named producer can emit the cluster's decisive state; partial columns are only a cost-efficient start.
- No engine, scorer, oracle, CSV, registry, lab, graph, or `Vault/` file was modified.
