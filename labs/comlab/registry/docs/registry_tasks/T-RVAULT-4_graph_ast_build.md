### Goal ###

Build the registry's two **AST (Pass-1, offline, free)** graphs via
`4dlab-graphify-run`: the package → `labs/comlab/registry/graph/v2_code/graph.json`
and the test suite → `labs/comlab/registry/graph/v2_tests/graph.json`, then run the
Part-A health-check eval on each. Done when both graphs exist with nodes/edges > 0, 0
dangling edges, 0 isolated nodes, and a **GOOD** verdict from the eval scripts.

### OFFLINE — NO API KEY (read first) ###
This is a **Pass-1 AST** build: it runs **100% offline**. You need **no API key and no LLM**.
Do NOT set, search for, or wait on `GEMINI_API_KEY` / `GOOGLE_API_KEY` / `DEEPSEEK_API_KEY` /
`ANTHROPIC_API_KEY` / `OPENAI_API_KEY`, do NOT start Ollama, and do NOT use any tool-bridge.
If a command asks you for a backend or a key, **you ran the wrong subcommand** — switch to
`graphify update` (see below).

Use **`graphify update <scoped-path>`** — it re-extracts code via tree-sitter with **no LLM**, and
writes `graph.json` + `GRAPH_REPORT.md` + `graph.html` in one pass. Do NOT use `graphify extract`:
that one is "AST **+ semantic LLM**" (its backend = whichever API key is set), and that semantic
step is the only reason a key is ever requested. Build on a `/tmp` copy of the scoped corpus, then
relocate the three files into the destination dir (keeps any stray `graphify-out/` out of the repo):

```bash
GBIN=/agent_workspace/.venv-wired/bin/graphify
# --- v2_code: the registry PACKAGE (exclude tests/docs/graph) ---
rm -rf /tmp/rvault4_code && mkdir -p /tmp/rvault4_code/pkg
rsync -a --exclude tests --exclude docs --exclude graph --exclude graphify-out --exclude __pycache__ \
  /agent_workspace/labs/comlab/registry/ /tmp/rvault4_code/pkg/
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u DEEPSEEK_API_KEY -u ANTHROPIC_API_KEY -u OPENAI_API_KEY \
  "$GBIN" update /tmp/rvault4_code/pkg                       # offline AST, no key
mkdir -p labs/comlab/registry/graph/v2_code
cp /tmp/rvault4_code/pkg/graphify-out/{graph.json,GRAPH_REPORT.md,graph.html} \
   labs/comlab/registry/graph/v2_code/
# --- v2_tests: the registry TEST SUITE ---
rm -rf /tmp/rvault4_tests && mkdir -p /tmp/rvault4_tests/pkg
rsync -a --exclude __pycache__ /agent_workspace/labs/comlab/registry/tests/ /tmp/rvault4_tests/pkg/
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u DEEPSEEK_API_KEY -u ANTHROPIC_API_KEY -u OPENAI_API_KEY \
  "$GBIN" update /tmp/rvault4_tests/pkg                      # offline AST, no key
mkdir -p labs/comlab/registry/graph/v2_tests
cp /tmp/rvault4_tests/pkg/graphify-out/{graph.json,GRAPH_REPORT.md,graph.html} \
   labs/comlab/registry/graph/v2_tests/
```
(If the eval reports an isolated `__init__` node, fix it by adding an inert module docstring with a
`wiki:` reference in the prep task — never hand-patch `graph.json`.)

### Success criteria ###

- `labs/comlab/registry/graph/v2_code/graph.json` and `…/v2_tests/graph.json` exist
  (+ their `GRAPH_REPORT.md`, `graph.html`), each with node count > 0.
- `eval-code-graph` health-check on each prints **GOOD**: 0 dangling, 0 isolated
  (code/test tiers must be fully wired), confidence split reported.
- No repo-root `graphify-out/` survives; the other `graph/*` dirs are byte-unchanged
  (`git status --porcelain` clean outside the two new dirs).

### Context ###

Phase 3 ingestion from `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §5`. Confirmed gap
(architect probe 2026-06-28): the registry package has **0 nodes** in every existing
comlab graph (`v2_code`/`v2_tests`/`v2_current` were scoped to `comlab/` + `tests/`,
never `registry/`). So these two graphs must be built fresh; they are not a re-extract
of a canonical graph (the never-re-extract rule does not apply — nothing exists yet).

Pass-1 is tree-sitter AST: free, no API key, no LLM — run it with `graphify update` (NOT `graphify extract`, which is the backend-coupled semantic path; see the OFFLINE section above). Inputs are the AST-legible package and
tests from T-RVAULT-2. The `rules/*.json` data files enter via the package run as data
nodes (that is why T-RVAULT-2 left them untouched).

**Hard guards (never skip — `§5`):** scope graphify to the **specific package /
tests directory**, NEVER `graphify .` from a repo root (the 81.9k-node incident rule).
Relocate `graph.json` + `GRAPH_REPORT.md` + `graph.html` into the destination dir,
then confirm no root `graphify-out/` survives. A missing edge is a **prep gap routed
back to T-RVAULT-2**, never patched into `graph.json`.

Load skills: `_skills/graph/4dlab-graphify-run` (resolve → run → relocate → verify) — but for this CODE corpus use its `graphify update` path, not `extract`;
eval at `_skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py`.

### Consumer (signal/noise) ###

N/A — no new field/enum/fault. The graphs' consumer is the vault build's frontmatter
derivation + the design→code→test spine in the `.base` views — both named/real once
the vault is wired in T-RVAULT-6.

### Deliverables ###

1. `labs/comlab/registry/graph/v2_code/{graph.json,GRAPH_REPORT.md,graph.html}`
2. `labs/comlab/registry/graph/v2_tests/{graph.json,GRAPH_REPORT.md,graph.html}`
3. `labs/comlab/registry/graph/AST_GRAPH_EVAL.md` — the two health-check verdicts.

### Files to touch ###

- `labs/comlab/registry/graph/v2_code/**` (CREATE)
- `labs/comlab/registry/graph/v2_tests/**` (CREATE)
- `labs/comlab/registry/graph/AST_GRAPH_EVAL.md` (CREATE)

### Out of scope ###

Do NOT build the docs graph (Pass-3, token cost) — that is T-RVAULT-5. Do NOT run the
optional Part-B LLM cross-check (gated; AST is ground truth here). Do NOT modify code,
tests, or `rules/*.json` — if the graph reveals a legibility miss, route it back to
T-RVAULT-2 as a follow-up, do not edit `graph.json`. Do NOT touch any other lab's
graph dirs.

GRAPH GUARDRAIL (task-scoped exception): this task is a KG-lane task whose Deliverables
explicitly name `graph.json` — it MAY run graphify, but ONLY scoped to the registry
package and `tests/`, never repo-root, and never against an existing canonical graph.

### Verification ###

```bash
cd /agent_workspace
for t in v2_code v2_tests; do
  test -f labs/comlab/registry/graph/$t/graph.json && echo "$t graph present"
done
python3 _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/registry/graph/v2_code/graph.json
python3 _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/comlab/registry/graph/v2_tests/graph.json
# no stray root graphify-out, no collateral on sibling graphs
test ! -d graphify-out && echo "no root graphify-out"
git -C /agent_workspace status --porcelain | grep -v 'labs/comlab/registry/graph/v2_code\|labs/comlab/registry/graph/v2_tests\|labs/comlab/registry/graph/AST_GRAPH_EVAL.md' | grep 'graph/' && echo "COLLATERAL!" || echo "no collateral"
```

All steps must pass (eval verdict GOOD on both).

### Progress hook ###

PROGRESS.md `T-RVAULT-4`: Status=done, Files changed={COUNT}, Verification="v2_code+v2_tests built; eval GOOD; 0 dangling/isolated; no collateral"
