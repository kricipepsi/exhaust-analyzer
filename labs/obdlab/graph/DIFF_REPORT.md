# 4DLab v2 — OBDLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 1974 | 1245 | -729 |
| **Edges (Links)** | 2346 | 1664 | -682 |
| **Communities** | 236 | 103 | -133 |

## Structural Relocation Verification

Below are examples of source file path transformations verified in the AST:

| Symbol / File | v1 Source Path | v2 Source Path |
| :--- | :--- | :--- |
| `_healthy_pids()` | `code/tests/unit/test_analytics_preconditions.py` | `tests/unit/test_analytics_preconditions.py` |
| `test_gate4_fail_shrtft1_below_min()` | `code/tests/unit/test_semantic_consistency_checker.py` | `tests/unit/test_semantic_consistency_checker.py` |
| `translator()` | `code/tests/unit/test_sensor_signal_translator.py` | `tests/unit/test_sensor_signal_translator.py` |
| `TrimAnalyticsGate` | `code/obdlab/schemas/vocabulary.py` | `obdlab/schemas/vocabulary.py` |
| `ResolvedHorizon` | `code/obdlab/schemas/dna_view.py` | `obdlab/schemas/dna_view.py` |

> [!NOTE]
> The paths have been updated to reflect the new flat layout: `4DLabV2/labs/<lab>/...`

## Added Nodes

Total added nodes: 392

- `core_o2_normalizer_rationale_138` (Type: `rationale`, Label: `Direct wideband pass-through per §11.2.          Reads pid_wideband_equivalenc`)
- `core_o2_normalizer_rationale_173` (Type: `rationale`, Label: `3-zone voltage → lambda mapping for WB sensor in NB simulation mode §11.3.`)
- `core_o2_normalizer_rationale_95` (Type: `rationale`, Label: `3-zone narrowband voltage → lambda mapping per §11.1.          Reads pid_oxyge`)
- `obdlab_config_physical_sensor_bounds_json` (Type: `code`, Label: `physical_sensor_bounds.json`)
- `obdlab_core_analytics_preconditions_py` (Type: `code`, Label: `analytics_preconditions.py`)
- `obdlab_core_exceptions_py` (Type: `code`, Label: `exceptions.py`)
- `obdlab_core_init_py` (Type: `code`, Label: `__init__.py`)
- `obdlab_core_o2_normalizer_py` (Type: `code`, Label: `o2_normalizer.py`)
- `obdlab_core_pid_ingestion_validator_py` (Type: `code`, Label: `pid_ingestion_validator.py`)
- `obdlab_core_semantic_consistency_checker_py` (Type: `code`, Label: `semantic_consistency_checker.py`)
- `obdlab_core_sensor_signal_translator_py` (Type: `code`, Label: `sensor_signal_translator.py`)
- `obdlab_core_state_bucketing_py` (Type: `code`, Label: `state_bucketing.py`)
- `obdlab_core_trim_vector_aggregator_py` (Type: `code`, Label: `trim_vector_aggregator.py`)
- `obdlab_core_ve_engine_py` (Type: `code`, Label: `ve_engine.py`)
- `obdlab_family_map_py` (Type: `code`, Label: `family_map.py`)
- ... and 377 more.
## Removed Nodes

Total removed nodes: 1121

- `answ2_md` (Type: `document`, Label: `answ2.md`)
- `bp_obdlab_1_functional_architecture_core_mandate` (Type: `document`, Label: `1. Functional Architecture & Core Mandate`)
- `bp_obdlab_1_the_3_way_polymorphic_math_routing_matrix` (Type: `document`, Label: `1. The 3-Way Polymorphic Math Routing Matrix`)
- `bp_obdlab_1_the_architectural_crisis_narrowband_vs_wideband` (Type: `document`, Label: `1. The Architectural Crisis: Narrowband vs. Wideband`)
- `bp_obdlab_1_the_core_volumetric_efficiency_equation` (Type: `document`, Label: `1. The Core Volumetric Efficiency Equation`)
- `bp_obdlab_1_the_obd_lab_architectural_component_tree` (Type: `document`, Label: `1. The OBD Lab Architectural Component Tree`)
- `bp_obdlab_2_complete_sequence_timeline_within_the_obd_lab_module` (Type: `document`, Label: `2. Complete Sequence Timeline within the OBD Lab Module`)
- `bp_obdlab_2_guarding_against_traversal_crashes` (Type: `document`, Label: `2. Guarding Against Traversal Crashes`)
- `bp_obdlab_2_high_density_node_inventory_the_8_pid_minimalist_schema` (Type: `document`, Label: `2. High-Density Node Inventory (The 8-PID Minimalist Schema)`)
- `bp_obdlab_2_the_solution_the_2_way_sensor_normalization_layer` (Type: `document`, Label: `2. The Solution: The 2-Way Sensor Normalization Layer`)
- `bp_obdlab_2_ve_validation_internal_logic_gates` (Type: `document`, Label: `2. VE Validation & Internal Logic Gates`)
- `bp_obdlab_3_data_preparation_blueprint_for_your_developer` (Type: `document`, Label: `3. Data Preparation Blueprint for Your Developer`)
- `bp_obdlab_3_edge_interactions_internal_conditional_logic` (Type: `document`, Label: `3. Edge Interactions & Internal Conditional Logic`)
- `bp_obdlab_3_how_to_present_this_adaptive_strategy_to_your_coder` (Type: `document`, Label: `3. How to Present This Adaptive Strategy to Your Coder`)
- `bp_obdlab_3_how_to_present_this_structure_to_your_coder` (Type: `document`, Label: `3. How to Present This Structure to Your Coder`)
- ... and 1106 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
