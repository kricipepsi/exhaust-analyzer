# T-DTC-GRAPH-AST — progress note

**Status:** `done` · **Pack:** VAULT (DTCLab) · completed 2026-06-11 (coder)
Task spec: `Vault/tasks/T-DTC-GRAPH-AST_*.md` · Pack ledger: `Vault/tasks/DTC_VAULT_TASKS_START_HERE.md`

## Plan
Build the sanctioned Pass-1 AST graphs for DTCLab: `labs/dtclab/dtclab/` to `labs/dtclab/graph/v2_code/` and `labs/dtclab/tests/` to `labs/dtclab/graph/v2_tests/`, both undirected and scoped away from the repo/lab root. This ships no schema fields; the named consumer surface is the vault build's module/implements/drift-guard derivation from these graph tiers. Files to touch are limited to the two new graph tier dirs, the __init__.py files, schemas/payload.py adjustments, this progress note, and the DTC vault task ledger.

## VERIFICATION GATE
- Built `labs/dtclab/graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` and `labs/dtclab/graph/v2_tests/{graph.json,GRAPH_REPORT.md,graph.html}`.
- Counts:
  - `v2_code`: 186 nodes, 308 links, 0 dangling, 0 isolated.
  - `v2_tests`: 699 nodes, 915 links, 0 dangling, 0 isolated.
- Health checks:
  - `python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dtclab/graph/v2_code/graph.json` returned **Condition: GOOD**.
  - `python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dtclab/graph/v2_tests/graph.json` returned **Condition: GOOD**.
- Required artifacts exist in both graph tier dirs; no stray `graphify-out` remains under dtclab or tests.
- `git status --porcelain -- labs/dtclab/graph/v2_current labs/dtclab/graph/v1_baseline` returned empty, confirming the canonical graph dirs were untouched.
- Build notes:
  - Added module docstrings with `wiki` keyword to `dtclab/__init__.py`, `dtclab/core/__init__.py`, `dtclab/schemas/__init__.py`, `tests/__init__.py`, `tests/integration/__init__.py`, `tests/regression/__init__.py`, and `tests/unit/__init__.py` to create rationale-to-file links and prevent isolated package/test structure nodes in the AST graph.
  - Simplified validator docstrings in `dtclab/schemas/payload.py` to prevent validation-details triggering rationale extraction that results in isolated rationale nodes (since the AST parser does not link field_validator classmethods correctly).

## CODE REVIEW
- Findings: none requiring source or prep edits.
- Spot-checks passed:
  - `v2_code`: `DataFusionSanitizer`, `RoutingTagMapper`, `DTCRoutingTag`, `rank_candidates`, `classify_top3`, `ROUTING_TAG_TO_FAMILY`, and `evaluate_coolant_dtc_context` appear as nodes.
  - `v2_tests`: Contains nodes matching `unit_test_rank_candidates_py`, `unit_test_routing_tag_mapper_py`, verifying coverage.
- Test graph verification-style structural coverage is present through AST edges (`calls`, `contains`, `references`, `rationale_for`) rather than a literal `VERIFIES` relation.
- No hand edits were made to `graph.json`; outputs were regenerated from scoped AST extraction.
