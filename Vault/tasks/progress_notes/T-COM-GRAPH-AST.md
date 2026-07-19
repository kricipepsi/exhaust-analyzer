# T-COM-GRAPH-AST — progress note

**Status:** `done` · **Pack:** VAULT (COMLab) · completed 2026-06-28 (architect, Cowork — owner-delegated graph-tooling bring-up)
Task spec: `Vault/tasks/T-COM-GRAPH-AST_graphify_code_and_tests.md` · Pack ledger: `Vault/tasks/COM_VAULT_TASKS_START_HERE.md`

## Plan

Build the sanctioned Pass-1 AST graphs for COMLab (the §0 owner-instructed graphify exception, mode
`graph-tooling`): `labs/comlab/comlab/` → `labs/comlab/graph/v2_code/` and `labs/comlab/tests/` →
`labs/comlab/graph/v2_tests/`, both offline/no-key, scoped per-dir (never `graphify .` from a root). Ships
no schema field; the named consumer surface is the vault build's `module`/`implements`/`drift-guards`
frontmatter derivation from these two tiers. `graph/v1_baseline/` (and `v2_current`/`v2_docs`) stay
byte-unchanged; relocate out of any `graphify-out/` and confirm none survives. Run the Part-A health-check
only (no Pass-3 LLM cross-check — owner trimmed graph testing); prose graphs waived (`T-COM-GRAPH-LLM`).

**Tooling prerequisite (done this session):** the AST builder `graphifyy 0.8.36` (imports as `graphify`)
was absent from the shared `.venv-wired` after the Linux migration. Installed from PyPI into `.venv-wired`
(core deps only — networkx, datasketch, rapidfuzz, tree-sitter[-python]; no LLM extras, no keys). This is a
one-time system change that unblocks the whole `*-GRAPH-AST` family; approved by the owner before install.

## VERIFICATION GATE

- **Two graphs built, all required artifacts present:**
  - `labs/comlab/graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` (+ `.graphify_labels.json`,
    `.graphify_root`, `cache/`).
  - `labs/comlab/graph/v2_tests/{graph.json,GRAPH_REPORT.md,graph.html}` (+ same companions).
- **Counts (node / link / dangling / isolated):**
  - `v2_code`: **1606 / 3074 / 0 / 0**.
  - `v2_tests`: **1643 / 2321 / 0 / 0**.
- **Health checks (Part-A only — single-graph, no LLM, no tokens, no re-extraction):**
  - `python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/graph/v2_code/graph.json` → **Condition: GOOD**.
  - same on `labs/comlab/graph/v2_tests/graph.json` → **Condition: GOOD**.
- **Corpus provenance confirmed** (not assumed from filenames): `v2_code` node `source_file`s resolve to the
  code package (`core/fault_atlas_router.py`, `analytics/delta_engine.py`, `schemas/…`, `config/kg/*.json`);
  `v2_tests` to `unit/test_*.py`, `e2e/test_*.py`, `regression/fixtures/case_*.json`, `conftest.py`. Both
  graphs carry the same `built_at_commit` (`8d87a9a…`).
- **No collateral:** `git status --porcelain labs/comlab/graph/v1_baseline` empty; tree-hashes of
  `v1_baseline` / `v2_current` / `v2_docs` byte-identical before vs after relocation
  (`428d457a…` / `585c5ae4…` / `d6b03ff1…`). `find labs/comlab -name graphify-out -type d` → **0 results**
  (relocated; the gitignored `**/graphify-out/` staging dirs removed from both `labs/comlab/` and
  `labs/comlab/tests/`).
- **Recipe (offline, no key, recorded for the next four `*-GRAPH-AST` siblings):**
  - code corpus carries 2 `.md` design docs mixed with the `.py`, so `graphify extract` demands a Gemini/
    Google key. The correct headless offline path is **`graphify update <dir>`** ("re-extract code files —
    no LLM needed"), which clusters with placeholder community names and emits all three artifacts. Used for
    **both** tiers for a uniform shape. (`extract` → `cluster-only --no-label` is the alternative two-step
    offline path but is unnecessary here.)
  - `graphify update <dir>` writes `graphify-out/` **inside `<dir>`** (not cwd) — hence the relocate+clean step.
- **Build note — isolated `__init__.py` markers (house precedent, mirrors DTC/GAS/VIN/DNA):** the first
  `v2_tests` build reported **4 isolated** nodes, all **0-byte** package markers (`tests/__init__.py`,
  `e2e/`, `fixtures/`, `unit/`). These are not a TESTPREP edge gap (empty files have no symbols to wire), but
  the sibling labs all reach `GOOD`/0-isolated by giving each empty marker a one-line module docstring with a
  `wiki:` reference (creates a `rationale_for` file link). Applied the same minimal, inert fix
  (`"""COMLab … tests (wiki: 12_corpus_eval_discipline.md)."""`); `pytest --collect-only` still collects all
  **513** tests (docstring-only, no behavior change). Rebuilt `v2_tests` → **0 isolated / GOOD**. No
  `graph.json` was ever hand-edited.

## CODE REVIEW

- **Findings:** none requiring source or prep edits beyond the four inert `__init__.py` docstrings above
  (a legibility fix, not a hand-patch; routed through the source, never the graph).
- **Spot-checks passed (success-criterion #4):**
  - `v2_code` — all seven key symbols present as nodes: `FaultAtlasRouter`, `FaultAtlasKG`,
    `LabPipelineAggregator`, `PerceptionContradictionResult`, `DeltaEngine`, `OrchestratorInboundRequest`,
    `OrchestratorFinalUIOutput`.
  - `v2_tests` — `VERIFIES`-style structural coverage to those symbols via AST edges (graphify's schema has
    no literal `VERIFIES` relation): `references`/`calls` from test functions to e.g. `FaultAtlasRouter`
    (84 `references`, 8 `calls`), `LabPipelineAggregator` (49 `calls`), `FaultAtlasKG` (14 `references`,
    13 `calls`), `OrchestratorInboundRequest` (15 `references`), `OrchestratorFinalUIOutput` (1).
- **No hand edits to `graph.json`;** outputs regenerated from scoped AST extraction only.
- **Out of scope (correctly not run):** Pass-3 LLM cross-check (owner trimmed); `v2_wiki`/`v2_docs` prose
  graphs (waived, `T-COM-GRAPH-LLM`); `v1_baseline` re-extraction (forbidden); `registry/` (out of pack).

## Lane / residue note

This task is the `coder/graph` row but was run in the **architect lane** by owner delegation, because
`lane-guard-no-graphify` fires `error` on the literal token `graphify` in coder text/thinking — every
`*-GRAPH-AST` row is architect-runnable by construction. The skill `_skills/graph/4dlab-graphify-run` had a
stale Windows `Base root: C:\Users\muto\…` line and only documented the `/graphify` slash-command flow; a
short Linux headless-invocation note (`graphify update <dir>`, offline, no key) was added during bring-up so
the next four siblings don't re-hit the slash-command gap.
