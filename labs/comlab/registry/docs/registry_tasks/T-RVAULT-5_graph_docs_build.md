### Goal ###

Build the registry's **docs (Pass-3, LLM, `--directed`)** graph via
`4dlab-graphify-run` from the ingest-ready corpus produced in T-RVAULT-3 →
`labs/comlab/registry/graph/v2_docs/graph.json`, then run the Part-A health-check eval.
Done when the graph exists with nodes/edges > 0, **EXTRACTED dominates**, 0 dangling,
0 isolated, and an `eval-doc-graph` **GOOD** verdict.

### Success criteria ###

- `labs/comlab/registry/graph/v2_docs/{graph.json,GRAPH_REPORT.md,graph.html}` exist.
- `eval-doc-graph` health-check prints **GOOD**: EXTRACTED is the dominant confidence
  class (Pass-3 expectation), 0 dangling, 0 isolated (docs tier must be fully wired).
- No repo-root `graphify-out/` survives; `v2_code`/`v2_tests` and all other lab graphs
  are byte-unchanged.

### Context ###

Phase 3 ingestion (LLM half) from `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §5`. Pass-3
is an LLM semantic pass: **it costs tokens + needs the backend**, so it is held in a
separate task from the free AST batch (T-RVAULT-4) and is **GATED** — confirm owner
approval before running (the run consumes API budget). Input is the EXTRACTED-annotated
`ingest_ready/` corpus from T-RVAULT-3; quality depends on those explicit relation
lines, not on re-reading the raw docs.

**Confirm the docs branch exists in the skill first.** Per `§5` note,
`4dlab-graphify-run` originally documented only code+wiki branches; the docs branch
(dest `graph/v2_docs/`, prep skill `4dlab-doc-prep`, verify focus = architectural
predicate proof-set) was added under `T-VAULT-DOCGRAPH-1`. Verify that branch is
present in the skill before running; if absent, STOP and surface it.

**Hard guards (`§5`):** scope to the `ingest_ready/` dir; relocate outputs; confirm no
root `graphify-out/`; no collateral. A missing edge is a **prep gap routed back to
T-RVAULT-3**, never patched into `graph.json`.

Load skills: `_skills/graph/4dlab-graphify-run`; eval at
`_skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py`; protocol
`_skills/graph/eval/PASS3_EVAL_PROTOCOL.md`.

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. Consumer is the vault build's frontmatter derivation
(T-RVAULT-6).

### Deliverables ###

1. `labs/comlab/registry/graph/v2_docs/{graph.json,GRAPH_REPORT.md,graph.html}`
2. `labs/comlab/registry/graph/DOCS_GRAPH_EVAL.md` — the health-check verdict.

### Files to touch ###

- `labs/comlab/registry/graph/v2_docs/**` (CREATE — graph.json + report + html)
- `labs/comlab/registry/graph/DOCS_GRAPH_EVAL.md` (CREATE)

### Out of scope ###

Do NOT run the optional Part-B LLM cross-check (separate gated task). Do NOT re-run the
AST graphs. Do NOT edit `ingest_ready/` to chase an edge — route gaps back to
T-RVAULT-3. Do NOT proceed if owner approval for the token-costing run is not given.

GRAPH GUARDRAIL (task-scoped exception): this KG-lane task names `graph.json` in its
Deliverables and MAY run graphify, scoped to `ingest_ready/` only, gated on owner
approval, never against an existing canonical graph.

### Verification ###

```bash
cd /agent_workspace
test -f labs/comlab/registry/graph/v2_docs/graph.json && echo "v2_docs graph present"
python3 _skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py labs/comlab/registry/graph/v2_docs/graph.json
test ! -d graphify-out && echo "no root graphify-out"
git -C /agent_workspace status --porcelain | grep 'graph/' | grep -v 'labs/comlab/registry/graph/v2_docs\|labs/comlab/registry/graph/DOCS_GRAPH_EVAL.md' && echo "COLLATERAL!" || echo "no collateral"
```

All steps must pass (eval verdict GOOD, EXTRACTED-dominant).

### Progress hook ###

PROGRESS.md `T-RVAULT-5`: Status=done, Files changed={COUNT}, Verification="v2_docs built; eval GOOD; EXTRACTED-dominant; no collateral"
