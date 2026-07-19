# 4DLab v2 — DTCLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 2042 | 1072 | -970 |
| **Edges (Links)** | 2539 | 1540 | -999 |
| **Communities** | 217 | 91 | -126 |

## Structural Relocation Verification

Below are examples of source file path transformations verified in the AST:

| Symbol / File | v1 Source Path | v2 Source Path |
| :--- | :--- | :--- |
| `name` | `code/dtclab/config/mode_06_hex_dictionary.json` | `dtclab/config/mode_06_hex_dictionary.json` |
| `ECT < 60 must return COLD_START_TRANSIT_FAULT even when RPM/load match idle.` | `code/tests/unit/test_historical_context_classifier.py` | `tests/unit/test_historical_context_classifier.py` |
| `_make_dict()` | `code/tests/unit/test_mode06_evaluator.py` | `tests/unit/test_mode06_evaluator.py` |
| `ff_ect_warmup` | `code/tests/regression/fixtures/case_03_catalyst_ect_gate.json` | `tests/regression/fixtures/case_03_catalyst_ect_gate.json` |
| `3D` | `code/dtclab/config/mode_06_hex_dictionary.json` | `dtclab/config/mode_06_hex_dictionary.json` |

> [!NOTE]
> The paths have been updated to reflect the new flat layout: `4DLabV2/labs/<lab>/...`

## Added Nodes

Total added nodes: 111

- `dtclab_config_mode_06_hex_dictionary_json` (Type: `code`, Label: `mode_06_hex_dictionary.json`)
- `dtclab_core_data_fusion_sanitizer_py` (Type: `code`, Label: `data_fusion_sanitizer.py`)
- `dtclab_core_dtc_ingestion_gate_py` (Type: `code`, Label: `dtc_ingestion_gate.py`)
- `dtclab_core_freeze_frame_extractor_py` (Type: `code`, Label: `freeze_frame_extractor.py`)
- `dtclab_core_historical_context_classifier_py` (Type: `code`, Label: `historical_context_classifier.py`)
- `dtclab_core_init_py` (Type: `code`, Label: `__init__.py`)
- `dtclab_core_mode06_evaluator_py` (Type: `code`, Label: `mode06_evaluator.py`)
- `dtclab_core_routing_tag_mapper_py` (Type: `code`, Label: `routing_tag_mapper.py`)
- `dtclab_family_map_py` (Type: `code`, Label: `family_map.py`)
- `dtclab_init_py` (Type: `code`, Label: `__init__.py`)
- `dtclab_ranking_py` (Type: `code`, Label: `ranking.py`)
- `dtclab_readme_labs_dtclab_dtclab_v2_stage_3` (Type: `document`, Label: `labs/dtclab — DTCLab v2 (Stage 3)`)
- `dtclab_schemas_dna_view_py` (Type: `code`, Label: `dna_view.py`)
- `dtclab_schemas_freeze_frame_py` (Type: `code`, Label: `freeze_frame.py`)
- `dtclab_schemas_init_py` (Type: `code`, Label: `__init__.py`)
- ... and 96 more.
## Removed Nodes

Total removed nodes: 1081

- `archive_graph_patch_prompt_3_after_patching_verification_checklist` (Type: `document`, Label: `§3 — After patching: verification checklist`)
- `archive_graph_patch_prompt_4_step1_verification_log_md_template` (Type: `document`, Label: `§4 — STEP1_VERIFICATION_LOG.md template`)
- `archive_graph_patch_prompt_codeblock_1` (Type: `document`, Label: `code:python (import json, copy)`)
- `archive_graph_patch_prompt_codeblock_2` (Type: `document`, Label: `code:python (for e in g["links"]:)`)
- `archive_graph_patch_prompt_codeblock_3` (Type: `document`, Label: `code:python (import json)`)
- `archive_graph_patch_prompt_codeblock_4` (Type: `document`, Label: `code:python (import json, collections)`)
- `archive_graph_patch_prompt_codeblock_5` (Type: `document`, Label: `code:block5 (# DTCLab Bootstrap Step 1 — Verification Log (Run 3))`)
- `archive_graph_patch_prompt_constraints` (Type: `document`, Label: `Constraints`)
- `archive_graph_patch_prompt_dtclab_graph_json_option_3_deterministic_patch` (Type: `document`, Label: `DTCLab graph.json — Option 3 deterministic patch`)
- `archive_graph_patch_prompt_issue_1_18_routes_to_edges_have_source_and_target_swapped` (Type: `document`, Label: `Issue 1 — 18 `routes_to` edges have source and target swapped`)
- `archive_graph_patch_prompt_issue_2_18_conceptually_related_to_edges_need_domain_specific_relabelling` (Type: `document`, Label: `Issue 2 — 18 `conceptually_related_to` edges need domain-specific relabelling`)
- `archive_master_wiki_v1_pre_split_10_1_mandatory_pids_sae_j1979_mode_02` (Type: `document`, Label: `10.1 Mandatory PIDs (SAE J1979 Mode $02)`)
- `archive_master_wiki_v1_pre_split_10_2_fuel_system_status_enum` (Type: `document`, Label: `10.2 Fuel system status enum`)
- `archive_master_wiki_v1_pre_split_10_3_calculated_load_value_clv_threshold_table` (Type: `document`, Label: `10.3 Calculated Load Value (CLV) threshold table`)
- `archive_master_wiki_v1_pre_split_10_4_ect_gate_for_freeze_frame_validity` (Type: `document`, Label: `10.4 ECT gate for freeze frame validity`)
- ... and 1066 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
