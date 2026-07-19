> **Context:** OBDLab BDD v2.0 (2026-06-10) · Module: OBDLab · Feature: Optional ferried channels + isolation/CI guards · Parent document: BDD_OBDLab.md

## Feature: Optional ferried channels validate strictly

```gherkin
Feature: Optional dict channels are validated or passed through as null

  Scenario: Per-cylinder misfire counts must be 1-indexed, non-negative
    Given per_cylinder_misfire_counts with a cylinder index of 0
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: LTFT cell vector values must lie within ±127
    Given ltft_cell_vector with a cell value of 200
    When the translator runs
    Then a PIDValidationError is raised

  Scenario: Absent optional channels are emitted as null
    Given neither per_cylinder_misfire_counts nor ltft_cell_vector is supplied
    When the translator runs
    Then both fields are null in the payload
```

### Entity: Optional channels test mapping

- **Tests:** `test_pid_ingestion_validator`

## Feature: Isolation and vocabulary guards (CI-level behaviour)

```gherkin
Feature: OBDLab stays an isolated, drift-free codebase

  Scenario: No cross-lab Python imports exist
    Given the obdlab package
    When the import-isolation audit runs
    Then there are zero imports from gaslab, dtclab, comlab, dnalab, or vinlab

  Scenario: The forbidden HIGH_IDLE_LOAD token is absent
    Given the obdlab codebase
    When the vocabulary scan runs
    Then HIGH_IDLE_LOAD appears nowhere (superseded by REGULATORY_HIGH_IDLE / STRESS_IDLE)
```

### Entity: CI guards test mapping

- **Tests:** `test_dna_view` (import isolation), `test_vocabulary` (token scan)

### Entity: Traceability summary

- **End-to-end pipeline** → `integration/test_pipeline_smoke`, `test_sensor_signal_translator`
- **PID validation / bounds / units** → `test_pid_ingestion_validator`, `test_sensor_bounds`
- **Bucketing** → `test_state*`, smoke
- **Semantic gates / thermal freeze** → `test_semantic_consistency_checker`
- **VE routing + validity** → `test_ve_engine`
- **O2 normalisation** → `test_o2_normalizer`
- **Trim aggregation / bank asymmetry** → `test_trim_vector_aggregator`, `test_bank_asym`
- **Analytics gate** → `test_analytics_preconditions`
- **Perception delta / MAF linearity** → `test_ecu_perception_delta`, `test_maf_linearity`
- **Schema contracts** → `test_payload`, `test_dna_view`, `test_vocabulary`
- **Regression + generative** → `test_obdlab_regression`, generative suite

## Graph relations (explicit)

**test_pid_ingestion_validator.py** VERIFIES **per_cylinder_misfire_counts** (cyl ≥ 1, count ≥ 0)
**test_pid_ingestion_validator.py** VERIFIES **ltft_cell_vector** (cell ≥ 0, value ∈ [−127, 127])
**test_pid_ingestion_validator.py** VERIFIES **absent optional channels → null** (non-blocking)
**test_dna_view.py** VERIFIES **import isolation** (0 cross-lab imports)
**test_vocabulary.py** VERIFIES **HIGH_IDLE_LOAD absent** (token scan)
**BDD_OBDLab v2.0** VERIFIES **optional channel validation + CI guards**
