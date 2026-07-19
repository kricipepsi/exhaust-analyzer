# Master-to-Per-Lab CSV Projection Contract

This contract defines how local test fixtures (`fixtures/<lab>_cases.csv`) are derived from the canonical master corpus (`cases_petrol_master_v6.csv`).

## 1. Column and Row Selection Rules per Lab

### GASLab
- **Consumed Columns (Inputs):**
  - `co`, `co2`, `hc`, `o2`, `nox` (raw gas concentration values)
  - `has_catalyst` (DNA field)
  - `egr_valve_type` (DNA field)
  - `cylinder_count` (DNA field)
- **Consumed Columns (Expected Outputs):**
  - `expected_chemical_state` (chemical state fault or nominal verdict)
  - `expected_sample_validity` (valid/invalid sample status)
- **Row Selection Predicate (Decidable Rows):**
  - Expected fault must be purely chemical (e.g., `RICH_MIXTURE`, `LEAN_MISFIRE`, `EXHAUST_AIR_LEAK`, `NORMAL_OPERATION`, etc.).
  - No perception gap must exist: `expected_perception_gap` must be `False` (meaning the physical chemistry directly matches the ECU/final state).

### OBDLab
- **Consumed Columns (Inputs):**
  - `engine_rpm`, `coolant_temp_c`, `calculated_engine_load_pct`, `mass_airflow_gps`, `manifold_vacuum_kpa`
  - `shrtft1`, `longft1`, `shrtft2`, `longft2`
  - `number_of_banks` (DNA field)
  - `has_maf`, `has_map` (DNA fields)
- **Consumed Columns (Expected Outputs):**
  - `expected_obd_lambda`
  - `expected_ve_pct`
  - `expected_ve_validity`
  - `expected_trim_analytics_gate`
  - `expected_maf_status`
  - `expected_map_status`
  - `expected_o2_failure_mode`
- **Row Selection Predicate (Decidable Rows):**
  - Rows with valid telemetry where OBD diagnostics can run (warmed engine, valid telemetry inputs).
  - Rows where the obd-specific anomalies (e.g. MAF drift, O2 sensor failure, trim deviation) are set, or normal operation when telemetry is present.

### DTCLab
- **Consumed Columns (Inputs):**
  - `dtcs_mode_03`, `dtcs_mode_07`, `dtcs_mode_0a` (lists of DTC codes)
  - `freeze_frame_coolant_temp_c`, `freeze_frame_rpm`, `freeze_frame_load_pct` (freeze frame context PIDs)
  - `mode_06_monitor_results` (Mode $06 margins)
  - `codes_cleared`, `active_mil`, `mil_flashing`
- **Consumed Columns (Expected Outputs):**
  - `expected_routing_tags`
  - `expected_historical_context`
  - `expected_freeze_frame_status`
- **Row Selection Predicate (Decidable Rows):**
  - Any row with active DTCs, freeze frame records, or Mode $06 monitor failures.

### COMLab
- **Consumed Columns:**
  - COMLab is the final decision spine and fusion gate. It consumes the **full** master corpus.
- **Row Selection Predicate:**
  - COMLab's projection is the **identity** function: it consumes 100% of the master rows (the full integration gate).

## 2. Shared-Engine Import Contract

Each lab's test suite MUST import the shared generative engine. Under no circumstances should the engine modules (`ModuleDescriptor`, `runner`, `generators/*`) be copied into individual labs.

- **Import path:** `harness.harness` (from `harness/harness`)
- **Example Import:**
  ```python
  from harness.descriptor import ModuleDescriptor
  from harness.runner import run_generative_suite
  ```
