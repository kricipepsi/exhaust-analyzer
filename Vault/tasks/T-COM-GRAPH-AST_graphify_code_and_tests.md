---
node_type: task
task_id: T-COM-GRAPH-AST
status: done
pack: VAULT
lab: comlab
mode: graph-tooling
blocked_by:
- T-COM-CODEPREP
- T-COM-TESTPREP
consumers:
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
implements:
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
tags:
- task
- vault
- comlab
---

# T-COM-GRAPH-AST — Graphify COMLab code + tests (Pass 1 AST) → `graph/v2_code/`, `graph/v2_tests/`

**Status:** `done` (2026-06-28, architect, owner-delegated — gate in `progress_notes/T-COM-GRAPH-AST.md`) · **Pack:** VAULT (COMLab) · **Mode:** GRAPH-TOOLING (sanctioned graphify run — see §0)
**Origin:** pipeline guide §5 (ingestion, code + test corpora) · **Blocked by:** T-COM-CODEPREP, T-COM-TESTPREP
**Load skills:** **`4dlab-graphify-run`**, **`eval-code-graph`** (`_skills/graph/eval/`), `comlab-verification-loop`
(the frozen-graph guard). **Do NOT** load `comlab-vault-prep` (prep is done) or `4dlab-vault` (that is VAULT).
**Consumer (signal/noise):** **Adds no schema field.** Builds the two AST graphs the vault build reads to
derive `module`/`implements`/`drift_guards` frontmatter (`modules.base`, `drift-guards.base`). The graphs
*are* the consumer surface.

### §0 — This is a SANCTIONED graphify run (read carefully) ###

COMLab holds a frozen canonical graph at `graph/v1_baseline/`. The pack rule (START_HERE §0) forbids
graphify as a side-effect of normal tasks and forbids re-extracting the frozen graph. **This task is the
explicit, owner-instructed exception** named by the pipeline: it builds the **new** tier graphs and **does
not touch** `graph/v1_baseline/`. Guards (guide §5):

- **Never `graphify .` from a repo root.** Scope each run: `labs/comlab/comlab/` then `labs/comlab/tests/`
  (the 81.9k-node incident is why). **Do not scope to `registry/`** — it is out of pack.
- **Build only the two new tier dirs**; `graph/v1_baseline/` stays byte-unchanged.
- **Relocate, then confirm no root `graphify-out/` survives.**

### Runs (Pass 1 AST — offline, free, no key) ###

| Corpus | Scope dir | Dest | Directed |
|---|---|---|---|
| code | `labs/comlab/comlab/` | `labs/comlab/graph/v2_code/` | usually undirected |
| tests | `labs/comlab/tests/` | `labs/comlab/graph/v2_tests/` | usually undirected |

Flow per corpus (via `4dlab-graphify-run`): `resolve → run → relocate → verify`.

### "Skip graph testing" applies here ###

- Build the two AST graphs; run the **Part-A health-check only** (single-graph, no LLM, no tokens, no
  re-extraction). The **Pass-3 LLM cross-check** (`eval-*-graph` two-graph mode) is **not run** — owner
  trimmed graph testing for this pack.
- The prose graphs (`v2_wiki`, `v2_docs`) are **waived** (`T-COM-GRAPH-LLM` is a waived row, not built).

### Success criteria ###

1. `graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` and `graph/v2_tests/{…}` exist; node/edge
   counts > 0.
2. **No collateral:** `graph/v1_baseline/` and any other `graph/*` dir byte-unchanged
   (`git status --porcelain` + mtime); no root `graphify-out/` survives.
3. **Health-check passes (Part-A only):**
   ```bash
   python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/graph/v2_code/graph.json
   ```
   Expect verdict GOOD; **0 dangling**, **0 isolated** for code; higher INFERRED share is a normal AST
   baseline. Run the same shape on `v2_tests`.
4. Spot-check key symbols are nodes: `FaultAtlasRouter`, `FaultAtlasKG`, `LabPipelineAggregator`,
   `PerceptionContradictionResult`, `DeltaEngine`, `OrchestratorInboundRequest`, `OrchestratorFinalUIOutput`;
   and that `tests/` produced `VERIFIES`-style edges to them.
5. A missing edge is a **prep gap routed back to T-COM-CODEPREP/TESTPREP** — never hand-patched into `graph.json`.

### Out of scope ###

- The Pass-3 LLM cross-check (**owner trimmed graph testing** — do not run it) · wiki/docs prose graphs
  (**waived**) · re-extracting `v1_baseline` (forbidden) · `registry/` (out of pack).

### Files to touch ###

- `labs/comlab/graph/v2_code/…`, `labs/comlab/graph/v2_tests/…` (new).

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/comlab/graph/v2_code labs/comlab/graph/v2_tests
test -d labs/comlab/graphify-out && echo "FAIL stray graphify-out" || echo "OK relocated"
git status --porcelain labs/comlab/graph/v1_baseline | grep . && echo "FAIL canonical touched" || echo "OK canonical untouched"
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/graph/v2_code/graph.json
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-GRAPH-AST.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (two graphs built, health GOOD, 0 dangling/isolated, canonical untouched, no stray
graphify-out) + `CODE REVIEW` (node/edge counts, key symbols present). Ledger row → `done` only when clean.
