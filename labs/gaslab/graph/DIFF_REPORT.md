# 4DLab v2 — GASLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 1312 | 1345 | +33 |
| **Edges (Links)** | 1611 | 1774 | +163 |
| **Communities** | 121 | 136 | +15 |

## Structural Relocation Verification

Below are examples of source file path transformations verified in the AST:

| Symbol / File | v1 Source Path | v2 Source Path |
| :--- | :--- | :--- |
| `4.1 Discretiser thresholds` | `docs/wiki/GAS_VOCABULARY.md` | `wiki/GAS_VOCABULARY.md` |

> [!NOTE]
> The paths have been updated to reflect the new flat layout: `4DLabV2/labs/<lab>/...`

## Added Nodes

Total added nodes: 816

- `fixtures_test_synthetic_grid_probes_rationale_64` (Type: `rationale`, Label: `Every hard-to-reach signature appears at least once via edge probes.      Runs ``)
- `gaslab_contracts_rationale_106` (Type: `rationale`, Label: `Directional pattern language for rule bodies.  Source: ``GAS_VOCABULARY §8``.`)
- `gaslab_contracts_rationale_117` (Type: `rationale`, Label: `Inferred catalyst health.  Internal-only in v1.  Source: ``GAS_VOCABULARY §9``.`)
- `gaslab_contracts_rationale_132` (Type: `rationale`, Label: `Five raw analyser inputs.  All fields required — no 4-gas fallback.      Source:`)
- `gaslab_contracts_rationale_144` (Type: `rationale`, Label: `Reject readings outside analyser measurement envelope.          Source: ``GAS_VO`)
- `gaslab_contracts_rationale_166` (Type: `rationale`, Label: `Output fragment GASLab hands to COMLab.  Source: ``GAS_VOCABULARY §12.1``.`)
- `gaslab_contracts_rationale_76` (Type: `rationale`, Label: `Discretised lambda regions.  Source: ``GAS_VOCABULARY §4``.`)
- `gaslab_contracts_rationale_88` (Type: `rationale`, Label: `Triangle-gate verdict.  Source: ``GAS_VOCABULARY §5``.`)
- `gaslab_contracts_rationale_97` (Type: `rationale`, Label: `RPM-bucket label consumed by GASLab.  Source: ``GAS_VOCABULARY §7``.`)
- `gaslab_process_rationale_37` (Type: `rationale`, Label: `Run the 5-gas diagnostic pipeline.  Source: ``GAS_WIKI §2.1``.`)
- `gaslab_ranking_rationale_212` (Type: `rationale`, Label: `Return all surviving GASLab candidates ordered by raw evidence score.      Sourc`)
- `gaslab_ranking_rationale_253` (Type: `rationale`, Label: `Return up to three canonical families with GASLab confidence scores.      Source`)
- `gaslab_readme_labs_gaslab_gaslab_v2_stage_1` (Type: `document`, Label: `labs/gaslab — GASLab v2 (Stage 1)`)
- `gaslab_resolution_euro_thresholds` (Type: `code`, Label: `_euro_thresholds()`)
- `gaslab_resolution_eurothresholds` (Type: `code`, Label: `EuroThresholds`)
- ... and 801 more.
## Removed Nodes

Total removed nodes: 783

- `docs_coolantleaksig_1_obdlab_signature_thermal_shock_volumetric_shift` (Type: `document`, Label: `1. OBDLab Signature: Thermal Shock & Volumetric Shift`)
- `docs_coolantleaksig_1_the_chemical_signature_logic` (Type: `document`, Label: `1. The Chemical Signature Logic`)
- `docs_coolantleaksig_1_update_your_rule_evaluator_to_check_for_the_coolant_intrusion_profiledef_evaluate_priority_rules_enhanced_reading_gasreading_block_test_str_optional_str` (Type: `document`, Label: `1. Update your rule evaluator to check for the coolant intrusion profiledef evaluate_priority_rules_enhanced(reading: GasReading, block_test: str) -> Optional[str]:`)
- `docs_coolantleaksig_2_dtclab_signature_rationality_failures_freeze_frame_triggers` (Type: `document`, Label: `2. DTCLab Signature: Rationality Failures & Freeze Frame Triggers`)
- `docs_coolantleaksig_2_inside_your_test_gaslab_suite_case_runner_update_the_fault_assertion_block_if_case_expected_fault_or_case_test_id_startswith_test_13_or_case_test_id_startswith_test_14` (Type: `document`, Label: `2. Inside your test_gaslab_suite(case) runner, update the fault assertion block:if case['expected_fault'] or case['test_id'].startswith("TEST_13") or case['test_id'].startswith("TEST_14"):`)
- `docs_coolantleaksig_2_new_csv_test_profile_additions_gas_test_suite_csv` (Type: `document`, Label: `2. New CSV Test Profile Additions (gas_test_suite.csv)`)
- `docs_coolantleaksig_3_how_comlab_the_orchestrator_uses_these_signatures` (Type: `document`, Label: `3. How COMLab (The Orchestrator) Uses These Signatures`)
- `docs_coolantleaksig_3_updating_the_python_code_logic_test_gaslab_py` (Type: `document`, Label: `3. Updating the Python Code Logic (test_gaslab.py)`)
- `docs_coolantleaksig_add_inside_your_existing_classify_ve_validity_function_in_test_obdlab_pyif_ve_pct_110_0_and_total_fuel_trim_25_0_and_coolant_temp_c_100_0` (Type: `document`, Label: `Add inside your existing classify_ve_validity function in test_obdlab.pyif ve_pct > 110.0 and total_fuel_trim > 25.0 and coolant_temp_c > 100.0:`)
- `docs_coolantleaksig_add_into_evaluate_freeze_frame_flags_processing_logicdef_evaluate_coolant_dtc_context_dtc_code_str_status_fuelsystemstatus_str` (Type: `document`, Label: `Add into evaluate_freeze_frame_flags processing logicdef evaluate_coolant_dtc_context(dtc_code: str, status: FuelSystemStatus) -> str:`)
- `docs_coolantleaksig_data_row_additions_dtc_test_suite_csv` (Type: `document`, Label: `Data Row Additions (dtc_test_suite.csv)`)
- `docs_coolantleaksig_data_row_additions_obd_test_suite_csv` (Type: `document`, Label: `Data Row Additions (obd_test_suite.csv)`)
- `docs_coolantleaksig_md` (Type: `document`, Label: `CoolantLeakSig.md`)
- `docs_coolantleaksig_python_implementation_test_dtclab_py` (Type: `document`, Label: `Python Implementation (test_dtclab.py)`)
- `docs_coolantleaksig_python_implementation_test_obdlab_py` (Type: `document`, Label: `Python Implementation (test_obdlab.py)`)
- ... and 768 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
