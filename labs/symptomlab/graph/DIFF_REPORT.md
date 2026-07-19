# 4DLab v2 — SYMPTOMLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 250 | 101 | -149 |
| **Edges (Links)** | 311 | 180 | -131 |
| **Communities** | 26 | 11 | -15 |

## Structural Relocation Verification

No path changes detected for common nodes. (The nodes might not specify a `source_file` or they might be completely identical.)

## Added Nodes

Total added nodes: 1

- `symptomlab_readme_labs_symptomlab_symptomlab_v2` (Type: `document`, Label: `labs/symptomlab — SymptomLab v2`)
## Removed Nodes

Total removed nodes: 150

- `claude_code_prompt_md` (Type: `document`, Label: `CLAUDE_CODE_PROMPT.md`)
- `progress_md` (Type: `document`, Label: `PROGRESS.md`)
- `progress_notes_t_sl_1_md` (Type: `document`, Label: `T-SL-1.md`)
- `progress_notes_t_sl_1_pythonskill_checklist` (Type: `document`, Label: `Pythonskill checklist`)
- `progress_notes_t_sl_1_summary` (Type: `document`, Label: `Summary`)
- `progress_notes_t_sl_1_t_sl_1_decision_table_yaml` (Type: `document`, Label: `T-SL-1 — Decision Table YAML`)
- `progress_notes_t_sl_1_verification` (Type: `document`, Label: `Verification`)
- `progress_notes_t_sl_2_md` (Type: `document`, Label: `T-SL-2.md`)
- `progress_notes_t_sl_2_pythonskill_checklist` (Type: `document`, Label: `Pythonskill checklist`)
- `progress_notes_t_sl_2_summary` (Type: `document`, Label: `Summary`)
- `progress_notes_t_sl_2_t_sl_2_module_scaffold` (Type: `document`, Label: `T-SL-2 — Module Scaffold`)
- `progress_notes_t_sl_2_verification` (Type: `document`, Label: `Verification`)
- `progress_notes_t_sl_3_md` (Type: `document`, Label: `T-SL-3.md`)
- `progress_notes_t_sl_3_pythonskill_checklist` (Type: `document`, Label: `Pythonskill checklist`)
- `progress_notes_t_sl_3_summary` (Type: `document`, Label: `Summary`)
- ... and 135 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
