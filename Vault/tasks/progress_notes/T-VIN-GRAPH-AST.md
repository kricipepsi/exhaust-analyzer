# T-VIN-GRAPH-AST — progress note

**Status:** `done` · **Pack:** VAULT (VINLab) · completed 2026-06-13 (coder)
Task spec: `Vault/tasks/T-VIN-GRAPH-AST_graphify_code_and_tests.md` · Pack ledger: `Vault/tasks/VIN_VAULT_TASKS_START_HERE.md`

## Plan

Build the two sanctioned Pass-1 AST graphs for VINLab — `labs/vinlab/vinlab/` → `labs/vinlab/graph/v2_code/`
and `labs/vinlab/tests/` → `labs/vinlab/graph/v2_tests/` — both undirected (code-map default), offline
(tree-sitter AST only, no LLM, no token cost), scoped away from repo/lab root. This ships **no schema
field**; the named signal/noise consumer is the **vault build's frontmatter derivation**
(`implements`/`module`/`source`) + the design→code→test spine in the three `.base` views, both wired by
`T-VIN-VAULT`. Files touched: the two new graph tier dirs + this note + the ledger row. The frozen
`graph/v2_current/`, `graph/v1_baseline/`, `DIFF_REPORT.md` are never re-extracted.

**Build method.** graphify is a Windows CLI (`pipx graphifyy`, Py 3.14); the bash sandbox is Linux and
cannot run it, so the offline AST pipeline (`detect → extract(parallel=False) → build_from_json →
cluster → analyze → report/to_json/to_html`) was driven via PowerShell, writing **directly** into each
tier dir (no root `graphify-out/` ever produced for the graph outputs). `parallel=False` + an
`if __name__=="__main__"` guard avoided the Windows spawn re-import pitfall.

## VERIFICATION GATE

- **Both graphs built + written directly to tier dirs** (no relocation step needed):
  - `labs/vinlab/graph/v2_code/{graph.json, GRAPH_REPORT.md, graph.html}`
  - `labs/vinlab/graph/v2_tests/{graph.json, GRAPH_REPORT.md, graph.html}`
- **Counts (eval Part-A, single-graph condition check, no LLM, no re-extraction):**
  - `v2_code`: **150 nodes, 255 links**, dangling **0**, isolated **1**, confidence `{EXTRACTED: 215, INFERRED: 40}`.
  - `v2_tests`: **542 nodes, 567 links**, dangling **0**, isolated **4**, confidence `{EXTRACTED: 550, INFERRED: 17}`.
- **Health verdict:** both tools printed **CHECK**, triggered **solely** by `isolated > 0`; **dangling = 0**
  on both (the always-a-defect metric is clean). Per success criterion #2, isolated nodes are admissible
  when **each is explained** — done below. None is a missing structural edge, so **no prep route-back** is
  warranted and (per this spec, unlike the DTC sibling) **no source edit** was made.
  - **Isolated nodes are all AST-extractor artifacts, not orphaned code symbols:**
    - `v2_code` `vinlab_models_rationale_257` — the **docstring** of `VinDNA.from_json()`. The method node
      `vinlab_models_from_json` **is present and wired (deg 13)**; tree-sitter does not link a classmethod
      docstring to its `def` (the same limitation the DTC `T-DTC-GRAPH-AST` note recorded).
    - `v2_tests` `init_py` — the **empty** `tests/__init__.py` (0 bytes → file node with no symbols to wire).
    - `v2_tests` 3 rationale nodes (`unit_test_decoder_rationale_184/213/293`) — **docstrings** of
      `test_european_vin_bypasses_checksum`, `test_passthrough_year_vins_decode`,
      `test_io_vin_not_blocked_by_invalid_chars`; all three test functions are present and wired.
- **Frozen graphs byte-unchanged:** md5 of all 239 files under `graph/v1_baseline/`, `graph/v2_current/`,
  `graph/DIFF_REPORT.md` **identical** before and after the run (and again after cache cleanup).
- **No surviving `graphify-out/`:** the AST extractor created empty `graphify-out/cache/` dirs under
  `tests/` and `vinlab/` (cache only — no graph outputs landed there); both removed; `find` confirms none
  survive under `labs/vinlab/`. Frozen md5 re-confirmed identical post-cleanup.
- **No collateral:** `git status --porcelain` under `labs/vinlab/` shows only the two new tier dirs
  (`?? graph/v2_code/`, `?? graph/v2_tests/`) as this task's additions. Pre-existing uncommitted `docs/`
  relocations were left untouched per the git rule.
- No prose Pass-3 run (`v2_wiki`/`v2_docs` waived); no schema field added; no source file edited.

## CODE REVIEW

- **Findings:** none requiring source or prep edits. Every isolated node resolves to a tree-sitter
  docstring/empty-file artifact whose real owner symbol is present and wired — not a prep gap.
- **Key symbols spot-checked present (criterion #2):**
  - `v2_code`: `RobustVINDecoder` (deg 23), `VinDNA` (deg 8), `infer_cylinder` (deg 3),
    `euro_to_horizon` (deg 4), plus `from_json()` (deg 13), `decode_vin_payload` (top hub).
  - `v2_tests`: `test_decoder.py` (deg 17), `TestValidDecodes`, `decoder()` conftest fixture, and the
    per-test functions behind the orphan docstrings — verification-style coverage via AST edges
    (`calls`, `contains`, `references`, `rationale_for`), not a literal `VERIFIES` relation.
- **Top hubs** are the expected god nodes: `RobustVINDecoder`, `overlay_cylinder_heuristic`,
  `decode_vin_payload`, the displacement/cylinder fallbacks (code); the cylinder-heuristic test module and
  the pre-refactor VinDNA fixtures (tests).
- No hand edits to `graph.json`; outputs regenerated wholesale from scoped, deterministic AST extraction.
