# T-DNAV-GRAPH-AST — progress note

**Status:** `done` · **Pack:** VAULT (DNALab) · completed 2026-06-13 (coder)
Task spec: `Vault/tasks/T-DNAV-GRAPH-AST_graphify_code_and_tests.md` · Pack ledger: `Vault/tasks/DNA_VAULT_TASKS_START_HERE.md`

## Plan

Build the two sanctioned Pass-1 AST graphs for DNALab — `labs/dnalab/dnalab/` → `labs/dnalab/graph/v2_code/` and `labs/dnalab/tests/` → `labs/dnalab/graph/v2_tests/` — both undirected (code-map default), offline (tree-sitter AST only, no LLM, no token cost), scoped away from repo/lab root. This ships **no schema field**; the named signal/noise consumer is the **vault build's frontmatter derivation** (`implements`/`module`/`source`) + the design→code→test spine in the three `.base` views, both wired by `T-DNAV-VAULT`. Files touched: the two new graph tier dirs + this note + the ledger row. The frozen `graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` are never re-extracted.

**Build method.** Driven via a dedicated python script `scratch/build_ast_graph.py` running the offline AST pipeline (`detect → extract(parallel=False) → build_from_json → cluster → analyze → report/to_json/to_html`), writing **directly** into each tier dir. `parallel=False` avoided any Windows spawn re-import issues.

## VERIFICATION GATE

- **Both graphs built + written directly to tier dirs**:
  - [v2_code/graph.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/graph/v2_code/graph.json)
  - [v2_tests/graph.json](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/graph/v2_tests/graph.json)
- **Counts (eval Part-A, single-graph health check, no LLM, no re-extraction):**
  - `v2_code`: **26 nodes, 38 links**, dangling **0**, isolated **0**, confidence `{EXTRACTED: 27, INFERRED: 11}`.
  - `v2_tests`: **58 nodes, 95 links**, dangling **0**, isolated **2**, confidence `{EXTRACTED: 55, INFERRED: 40}`.
- **Health verdict:**
  - `v2_code`: **GOOD** (0 dangling, 0 isolated).
  - `v2_tests`: **CHECK** (0 dangling, 2 isolated). Isolated nodes are explained below. Dangling = 0 on both.
  - **Isolated nodes in `v2_tests` are AST-extractor artifacts (empty files), not orphaned code symbols:**
    - `init` — corresponds to empty `tests/__init__.py`.
    - `unit_init` — corresponds to empty `tests/unit/__init__.py`.
    Both have 0 bytes of content, so they contain no symbols and have no edges. This is expected and explained.
- **Frozen graphs byte-unchanged:** verified no modifications inside `labs/dnalab/graph/v1_baseline/`, `labs/dnalab/graph/v2_current/`, or `labs/dnalab/graph/DIFF_REPORT.md` (`git diff` clean).
- **No surviving `graphify-out/`:** removed the temporary `graphify-out/` folders created under the package/test source directories (`labs/dnalab/dnalab/graphify-out/` and `labs/dnalab/tests/graphify-out/`).
- **No collateral:** `git status --porcelain` shows only the two new tier dirs and this note as additions.
- No prose Pass-3 run (`v2_wiki`/`v2_docs` waived); no schema field added; no source file edited.

## CODE REVIEW

- **Findings:** none requiring source or prep edits. Every isolated node resolves to a tree-sitter empty-file artifact — not a prep gap.
- **Key symbols spot-checked present (criterion #2):**
  - `v2_code`: `build_vehicle_dna` (`assembly_build_vehicle_dna`, deg 4), `VehicleDNA` (`models_vehicledna`, deg 10), `from_json_payload` (`models_vehicledna_from_json_payload`, deg 3).
  - `v2_tests`: `test_assembly` (deg 3), conftest `make_vin_dna` (deg 22), conftest `make_symptom_dna` (deg 21), `test_real_pipeline_smoke` (deg 1).
- **Top hubs** are the expected god nodes / orchestrators:
  - `v2_code`: `VehicleDNA` (`models_vehicledna`), `SymptomDNA` (`symptomdna`), `VinDNA` (`vindna`).
  - `v2_tests`: conftest fixture generators `make_vin_dna` and `make_symptom_dna`.
- No hand edits to `graph.json`; outputs regenerated wholesale from scoped, deterministic AST extraction.
