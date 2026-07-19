# 4DLab v2 — COMLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 1139 | 3090 | +1951 |
| **Edges (Links)** | 7495 | 4139 | -3356 |
| **Communities** | 35 | 326 | +291 |

## Structural Relocation Verification

Below are examples of source file path transformations verified in the AST:

| Symbol / File | v1 Source Path | v2 Source Path |
| :--- | :--- | :--- |
| `End-to-end diagnostic engine tests — one fixture per routable registry family.` | `tests\e2e\test_diagnostic_engine.py` | `tests/e2e/test_diagnostic_engine.py` |
| `TrimAnalyticsGate` | `comlab\schemas\vocabulary.py` | `comlab/schemas/vocabulary.py` |
| `test_v2_route_emits_prune_span_with_rule_pruned_events()` | `tests\test_router_spans.py` | `tests/test_router_spans.py` |
| `De-cat + NONE role → no incoherence (secondary loop not present).` | `tests\unit\test_perception_contradiction.py` | `tests/unit/test_perception_contradiction.py` |
| `Role of the downstream O2 sensor in the ECU's closed-loop strategy.      COMLab` | `comlab\schemas\vocabulary.py` | `comlab/schemas/vocabulary.py` |

> [!NOTE]
> The paths have been updated to reflect the new flat layout: `4DLabV2/labs/<lab>/...`

## Added Nodes

Total added nodes: 2236

- `comlab_config_global_fault_registry_json` (Type: `code`, Label: `global_fault_registry.json`)
- `comlab_config_kg_cam_timing_json` (Type: `code`, Label: `cam_timing.json`)
- `comlab_config_kg_catalyst_failure_json` (Type: `code`, Label: `catalyst_failure.json`)
- `comlab_config_kg_ecu_fault_json` (Type: `code`, Label: `ecu_fault.json`)
- `comlab_config_kg_exhaust_leak_json` (Type: `code`, Label: `exhaust_leak.json`)
- `comlab_config_kg_ignition_fault_json` (Type: `code`, Label: `ignition_fault.json`)
- `comlab_config_kg_invalid_input_json` (Type: `code`, Label: `invalid_input.json`)
- `comlab_config_kg_kg_schema_json` (Type: `code`, Label: `_kg_schema.json`)
- `comlab_config_kg_lean_condition_json` (Type: `code`, Label: `lean_condition.json`)
- `comlab_config_kg_mechanical_wear_json` (Type: `code`, Label: `mechanical_wear.json`)
- `comlab_config_kg_misfire_json` (Type: `code`, Label: `misfire.json`)
- `comlab_config_kg_no_fault_json` (Type: `code`, Label: `no_fault.json`)
- `comlab_config_kg_non_starter_json` (Type: `code`, Label: `non_starter.json`)
- `comlab_config_kg_rich_mixture_json` (Type: `code`, Label: `rich_mixture.json`)
- `comlab_config_kg_sensor_fault_json` (Type: `code`, Label: `sensor_fault.json`)
- ... and 2221 more.
## Removed Nodes

Total removed nodes: 285

- `comlab_diagnostic_logic` (Type: `document`, Label: `COMLab Diagnostic Logic`)
- `comlab_dna_architecture` (Type: `document`, Label: `COMLab DNA Architecture`)
- `comlab_fault_taxonomy` (Type: `document`, Label: `COMLab Fault Taxonomy`)
- `comlab_horizon_eras` (Type: `document`, Label: `COMLab Horizon Eras`)
- `comlab_lab_input_reference` (Type: `document`, Label: `COMLab Lab Input Reference`)
- `comlab_projection_rationale_115` (Type: `rationale`, Label: `Project once into all three views.  # lld: §5.2      Returned tuple-shaped model`)
- `core_fault_atlas_router_rationale_101` (Type: `rationale`, Label: `Top-level shape of global_fault_registry.json.`)
- `core_fault_atlas_router_rationale_1055` (Type: `rationale`, Label: `Return a minimal sentinel UserInputEchoAudit when none provided.`)
- `core_fault_atlas_router_rationale_106` (Type: `rationale`, Label: `Internal result from execute_triage_loop → route().`)
- `core_fault_atlas_router_rationale_121` (Type: `rationale`, Label: `One rule in the global fault registry. Validated at boot.`)
- `core_fault_atlas_router_rationale_135` (Type: `rationale`, Label: `Top-level shape of global_fault_registry.json.`)
- `core_fault_atlas_router_rationale_137` (Type: `rationale`, Label: `Resolve a registry PID name to a runtime float value.      Returns None when the`)
- `core_fault_atlas_router_rationale_140` (Type: `rationale`, Label: `Internal result from execute_triage_loop → route().`)
- `core_fault_atlas_router_rationale_168` (Type: `rationale`, Label: `Stage B decision core. 5-phase triage walk per LLD §6.4.      Constructor accept`)
- `core_fault_atlas_router_rationale_196` (Type: `rationale`, Label: `Load + validate ``global_fault_registry.json`` at boot.          Raises ValueErr`)
- ... and 270 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
