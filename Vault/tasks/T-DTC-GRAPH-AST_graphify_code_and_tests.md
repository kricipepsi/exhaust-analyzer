---
node_type: task
task_id: T-DTC-GRAPH-AST
status: pending
pack: VAULT
lab: dtclab
mode: graph-tooling
blocked_by:
- T-DTC-CODEPREP
- T-DTC-TESTPREP
consumers:
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
implements:
- graph/v2_code/graph.json
tags:
- task
- vault
- dtclab
---

# T-DTC-GRAPH-AST — Graphify DTCLab code + tests (Pass 1 AST) → `graph/v2_code/`, `graph/v2_tests/`

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** GRAPH-TOOLING (sanctioned graphify run — see §0)
**Origin:** pipeline guide §5 (ingestion, code + test corpora) · **Blocked by:** T-DTC-CODEPREP, T-DTC-TESTPREP
**Consumer (signal/noise):** **Adds no schema field.** Builds the two AST graphs the vault build reads to
derive `module` / `implements` / `drift_guards` frontmatter (`modules.base`, `drift-guards.base`). The
graphs *are* the consumer surface; no new fields ship here.

### §0 — This is a SANCTIONED graphify run (read carefully) ###

The DTCLab repo holds frozen canonical graphs at `graph/v2_current/` and `graph/v1_baseline/`. Pack rule
(START_HERE §0) forbids graphify as a side-effect of normal tasks and forbids re-extracting those frozen
graphs. **This task is the explicit, owner-instructed exception** named by the pipeline: it builds the
**new** tier graphs and **does not touch** `graph/v2_current/` or `graph/v1_baseline/`. Guards (guide §5):

- **Never `graphify .` from a repo root.** Scope each run to the specific dir:
  `labs/dtclab/dtclab/` then `labs/dtclab/tests/`. (The 81.9k-node incident is why.)
- **Build only the two new tier dirs**; the canonical `v2_current` / `v1_baseline` graphs are byte-unchanged.
- **Relocate, then confirm no root `graphify-out/` survives.**

### Runs (Pass 1 AST — offline, free, no key) ###

| Corpus | Scope dir | Dest | Directed |
|---|---|---|---|
| code | `labs/dtclab/dtclab/` | `labs/dtclab/graph/v2_code/` | usually undirected |
| tests | `labs/dtclab/tests/` | `labs/dtclab/graph/v2_tests/` | usually undirected |

Flow per corpus (via `4dlab-graphify-run`): `resolve → run → relocate → verify`.

### "Skip graph testing" applies here ###

- Build the two AST graphs and run the **Part-A health-check only** (single-graph, no LLM, no tokens,
  no re-extraction). The **Pass-3 LLM cross-check** (`eval-*-graph` two-graph mode) is **not run** —
  owner skipped graph testing for this pack.
- The prose graphs (`v2_wiki`, `v2_docs`) are **waived** (`T-DTC-GRAPH-LLM` is not authored).

### Success criteria ###

1. `graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` and `graph/v2_tests/{…}` exist; node/edge
   counts > 0.
2. **No collateral:** `graph/v2_current/`, `graph/v1_baseline/`, and other `graph/*` dirs byte-unchanged
   (`git status --porcelain` + mtime); no root `graphify-out/` survives.
3. **Health-check passes (Part-A only):**
   ```bash
   python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dtclab/graph/v2_code/graph.json
   ```
   Expect verdict GOOD; **0 dangling**, **0 isolated** for code; a higher INFERRED share is a normal AST
   baseline, not a fault. Run the same health-check shape on `v2_tests`.
4. Spot-check key symbols appear as nodes: `DataFusionSanitizer`, `RoutingTagMapper`, `DTCRoutingTag`,
   `rank_candidates`, `classify_top3`, `ROUTING_TAG_TO_FAMILY`, `evaluate_coolant_dtc_context`; and that
   `tests/` produced `VERIFIES`-style edges to them.
5. A missing edge is a **prep gap routed back to T-DTC-CODEPREP/TESTPREP** — never hand-patched into
   `graph.json`.

### Out of scope ###

- The Pass-3 LLM cross-check (`eval-*-graph` two-graph mode) — **owner skipped graph testing**; do not run it.
- Wiki/docs prose graphs (**waived**) · re-extracting `v2_current`/`v1_baseline` (forbidden).

### Files to touch ###

- `labs/dtclab/graph/v2_code/…`, `labs/dtclab/graph/v2_tests/…` (new).

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/dtclab/graph/v2_code labs/dtclab/graph/v2_tests
test -d labs/dtclab/graphify-out && echo "FAIL stray graphify-out" || echo "OK relocated"
git status --porcelain labs/dtclab/graph/v2_current labs/dtclab/graph/v1_baseline | grep . \
  && echo "FAIL canonical graph touched" || echo "OK canonical untouched"
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/dtclab/graph/v2_code/graph.json
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-GRAPH-AST.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (two graphs built, health GOOD, 0 dangling/isolated, canonical untouched, no stray
graphify-out) + `CODE REVIEW` (node/edge counts, key symbols present). Ledger row → `done` only when clean.
