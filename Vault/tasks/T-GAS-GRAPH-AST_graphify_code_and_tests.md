---
node_type: task
task_id: T-GAS-GRAPH-AST
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling
blocked_by:
- T-GAS-CODEPREP
- T-GAS-TESTPREP
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
- gaslab
---

# T-GAS-GRAPH-AST — Graphify GASLab code + tests (Pass 1 AST) → `graph/v2_code/`, `graph/v2_tests/`

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING (sanctioned graphify run — see §0)
**Origin:** pipeline guide §5 (ingestion, code + test corpora) · **Blocked by:** T-GAS-CODEPREP, T-GAS-TESTPREP
**Consumer (signal/noise):** **Adds no schema field.** Builds the two AST graphs that the vault build
reads to derive `module` / `implements` / `drift_guards` frontmatter (`modules.base`,
`drift-guards.base`, plan §4). The graphs *are* the consumer surface; no new fields ship here.

### §0 — This is a SANCTIONED graphify run (read carefully) ###

GASLab START_HERE §0 forbids graphify as a side-effect of normal tasks and forbids re-extracting the
frozen `graph/v2_current/`. **This task is the explicit, owner-instructed exception** named by the
pipeline: it builds the **new** four-tier graphs and **does not touch** `graph/v2_current/` or
`graph/v1_baseline/`. Guards (guide §5):

- **Never `graphify .` from a repo root.** Scope each run to the specific dir:
  `labs/gaslab/gaslab/` then `labs/gaslab/tests/`. (The 81.9k-node incident is why.)
- **Build only the two new tier dirs**; the canonical `v2_current` graph is byte-unchanged.
- **Relocate, then confirm no root `graphify-out/` survives.**

### Runs (Pass 1 AST — offline, free, no key) ###

| Corpus | Scope dir | Dest | Directed |
|---|---|---|---|
| code | `labs/gaslab/gaslab/` | `labs/gaslab/graph/v2_code/` | usually undirected |
| tests | `labs/gaslab/tests/` | `labs/gaslab/graph/v2_tests/` | usually undirected |

Flow per corpus (via `4dlab-graphify-run`): `resolve → run → relocate → verify`.

### Success criteria ###

1. `graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}` and `graph/v2_tests/{…}` exist; node/edge
   counts > 0.
2. **No collateral:** `graph/v2_current/`, `graph/v1_baseline/`, and the other `graph/*` dirs are
   byte-unchanged (`git status --porcelain` + mtime); no root `graphify-out/` survives.
3. **Health-check passes (Part-A only — the graph-review cross-check is SKIPPED this pack):**
   ```bash
   python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/gaslab/graph/v2_code/graph.json
   ```
   Expect verdict GOOD; **0 dangling**, **0 isolated** for code; a higher INFERRED share is a normal
   AST baseline, not a fault. Run the same health-check shape on `v2_tests`.
4. Spot-check key symbols appear as nodes: `ChemicalSignature`, `CAM_TIMING_*`, `GasLabDnaView`,
   `rule_engine`, `resolution`, and that `tests/` produced `VERIFIES`-style edges to them.
5. A missing edge is a **prep gap routed back to T-GAS-CODEPREP/TESTPREP** — never hand-patched into
   `graph.json`.

### Out of scope ###

- The Pass-3 LLM cross-check (`eval-*-graph` two-graph mode) — **owner deferred graph review** for
  this pack; do not run it.
- Wiki/docs graphs (→ T-GAS-GRAPH-LLM).
- Re-extracting `v2_current` (forbidden).

### Files to touch ###

- `labs/gaslab/graph/v2_code/…`, `labs/gaslab/graph/v2_tests/…` (new).

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/gaslab/graph/v2_code labs/gaslab/graph/v2_tests
test -d labs/gaslab/graphify-out && echo "FAIL stray graphify-out" || echo "OK relocated"
git status --porcelain labs/gaslab/graph/v2_current labs/gaslab/graph/v1_baseline | grep . \
  && echo "FAIL canonical graph touched" || echo "OK canonical untouched"
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/gaslab/graph/v2_code/graph.json
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-GRAPH-AST.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (two graphs built, health GOOD, 0 dangling/isolated, canonical untouched, no stray
graphify-out) + `CODE REVIEW` (node/edge counts, key symbols present). Ledger row → `done` only when clean.
