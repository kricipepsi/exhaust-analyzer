# T-GAS-GRAPH-AST — progress note

**Status:** `done` · **Pack:** VAULT (GASLab) · authored 2026-06-10 (architect)
Task spec: `Vault/tasks/T-GAS-GRAPH-AST_*.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan
Build the sanctioned Pass-1 AST graphs for GASLab only: `labs/gaslab/gaslab/` to
`labs/gaslab/graph/v2_code/` and `labs/gaslab/tests/` to `labs/gaslab/graph/v2_tests/`, both
undirected and scoped away from the repo/lab root. This ships no schema fields; the named consumer
surface is the vault build's module/implements/drift-guard derivation from these graph tiers. Files
to touch are limited to the two new graph tier dirs, this progress note, and the GAS vault task
ledger after verification.

## VERIFICATION GATE
- Built `labs/gaslab/graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` and
  `labs/gaslab/graph/v2_tests/{graph.json,GRAPH_REPORT.md,graph.html}`.
- Counts:
  - `v2_code`: 237 nodes, 407 links, 0 dangling, 0 isolated.
  - `v2_tests`: 494 nodes, 723 links, 0 dangling, 0 isolated.
- Health checks:
  - `python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/gaslab/graph/v2_code/graph.json`
    returned **Condition: GOOD**.
  - `python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/gaslab/graph/v2_tests/graph.json`
    returned **Condition: GOOD**.
- Required artifacts exist in both graph tier dirs; no `labs/gaslab/graphify-out` survives.
- `git status --porcelain -- labs/gaslab/graph/v2_current labs/gaslab/graph/v1_baseline` returned
  empty, confirming the canonical graph dirs were untouched.
- Build notes:
  - `v2_code` uses a deterministic AST supplement for Python `Enum`/`StrEnum` class members, so
    `ChemicalSignature.CAM_TIMING_*` values are represented as extracted enum-member nodes.
  - `v2_tests` excludes 3 zero-byte package marker files (`__init__.py`) that otherwise produced
    isolated no-signal nodes.

## CODE REVIEW
- Findings: none requiring source or prep edits.
- Spot-checks passed:
  - `v2_code`: `ChemicalSignature` 36 hits, `CAM_TIMING_` 3, `GasLabDnaView` 5, `rule_engine` 33,
    `resolution` 33.
  - `v2_tests`: `ChemicalSignature` 7 hits, `CAM_TIMING_` 16, `GasLabDnaView` 17, `rule_engine`
    164, `resolution` 59.
- Test graph verification-style structural coverage is present through AST edges
  (`calls`, `contains`, `references`, `rationale_for`) rather than a literal `VERIFIES` relation in
  this Pass-1 graph.
- No hand edits were made to `graph.json`; outputs were regenerated from scoped AST extraction.

> Flip the ledger row to `done` only when BOTH blocks above are clean (and any contracted consumer is
> grep-confirmed read in a live path).
