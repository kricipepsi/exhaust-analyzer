# 4DLab v2 — VINLAB Graph Diff Report

**Date:** 2026-06-06 · **Scope:** Structural change verification

## Overview Metrics

| Metric | v1 Baseline | v2 Current | Difference |
| :--- | :--- | :--- | :--- |
| **Nodes** | 2093 | 1364 | -729 |
| **Edges (Links)** | 2386 | 1723 | -663 |
| **Communities** | 155 | 92 | -63 |

## Structural Relocation Verification

No path changes detected for common nodes. (The nodes might not specify a `source_file` or they might be completely identical.)

## Added Nodes

Total added nodes: 1

- `vinlab_readme_labs_vinlab_vinlab_v2` (Type: `document`, Label: `labs/vinlab — VINLab v2`)
## Removed Nodes

Total removed nodes: 730

- `claude_code_prompt_md` (Type: `document`, Label: `CLAUDE_CODE_PROMPT.md`)
- `progress_md` (Type: `document`, Label: `PROGRESS.md`)
- `progress_notes_t_csv_4_codeblock_1` (Type: `document`, Label: `code:block1 (Syntax:         PASS)`)
- `progress_notes_t_csv_4_inline_code_review` (Type: `document`, Label: `INLINE CODE REVIEW`)
- `progress_notes_t_csv_4_md` (Type: `document`, Label: `T-CSV-4.md`)
- `progress_notes_t_csv_4_python_immediate_checklist_10_items` (Type: `document`, Label: `Python Immediate Checklist (10 items)`)
- `progress_notes_t_csv_4_sanitization_note` (Type: `document`, Label: `Sanitization note`)
- `progress_notes_t_csv_4_t_csv_4_progress_notes` (Type: `document`, Label: `T-CSV-4 — Progress Notes`)
- `progress_notes_t_csv_4_unplanned_follow_ups` (Type: `document`, Label: `Unplanned follow-ups`)
- `progress_notes_t_csv_4_verification_gate_t_csv_4` (Type: `document`, Label: `VERIFICATION GATE — T-CSV-4`)
- `progress_notes_t_fx_10_codeblock_1` (Type: `document`, Label: `code:block1 (VERIFICATION GATE — T-FX-10)`)
- `progress_notes_t_fx_10_inline_code_review` (Type: `document`, Label: `Inline CODE REVIEW`)
- `progress_notes_t_fx_10_md` (Type: `document`, Label: `T-FX-10.md`)
- `progress_notes_t_fx_10_python_immediate_checklist` (Type: `document`, Label: `Python Immediate Checklist`)
- `progress_notes_t_fx_10_t_fx_10_session_notes` (Type: `document`, Label: `T-FX-10 — Session Notes`)
- ... and 715 more.

## Summary Verdict

⚠️ **WARNING**: The node count difference is significant. This could be due to split sub-packages (e.g. DNA split into 3 labs) or substantial cleanup of simple variants.
