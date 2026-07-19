# T-SYMGRAPH-4 — Build the Pass-1 AST tiers `v2_code/` + `v2_tests/` (KG-LANE)

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE
**Blocked by:** T-SYMGRAPH-2 (code-prep), T-SYMGRAPH-3 (test-prep)

> **THIS IS THE ONE KG-LANE TASK IN THE PACK.** It is the sole sanctioned exception to the
> standing graph-rebuild guard ([GRAPH GATE] in START_HERE). graphify runs **only** here,
> **only** on the two scopes below, and **never** on a repo root, `graphify-out/`,
> `v2_current/`, or `v1_baseline/`. Re-read the guards before running anything.

### Goal ###

Build SymptomLab's two missing **Pass-1 (AST, offline, free)** graph tiers with
`4dlab-graphify-run` (`resolve → run → relocate → verify`), one per corpus, each relocated
into its own destination dir, then health-checked. Proof of done: `labs/symptomlab/graph/v2_code/graph.json`
and `labs/symptomlab/graph/v2_tests/graph.json` exist, each with nodes/edges > 0, **0
dangling**, **0 isolated**, health verdict **GOOD**, and no collateral change to any other
`graph/*` dir.

### Success criteria ###

- `labs/symptomlab/graph/v2_code/graph.json` built from `labs/symptomlab/symptomlab/`
  (Pass 1 AST); health-check verdict **GOOD** (dangling=0, isolated=0, nodes/edges>0).
- `labs/symptomlab/graph/v2_tests/graph.json` built from `labs/symptomlab/tests/`
  (Pass 1 AST); health-check verdict **GOOD** (same thresholds).
- Both dirs also contain the relocated `GRAPH_REPORT.md` + `graph.html`; no root
  `graphify-out/` survives the run.
- `git status --porcelain labs/symptomlab/graph` shows **only** the two new tier dirs
  changed — `v2_current/`, `v1_baseline/`, `DIFF_REPORT.md` byte-unchanged.

### Context ###

SymptomLab has no build tiers today — only `v2_current/` (the stale 06-06 query index, 101
nodes — a symbol→file/line lookup, not a ship tier) and `v1_baseline/`. `GRAPH_MANIFEST.md`
§4 lists symptomlab as a must-be-graphed gap. This task fills the **code + tests** half;
wiki/docs (Pass 3 LLM) is owner-SKIPPED and PARKED. Pass 1 is tree-sitter — it just reads
code structure statically, so it is free and needs no API key. The prep tasks
(T-SYMGRAPH-2/3) already made the package and tests AST-legible, so the extractor should
produce 0 isolated nodes.

**Load skills:** `_skills\graph\4dlab-graphify-run\SKILL.md` — read end-to-end first; it
defines `resolve → run → relocate → verify` and routes by file type to Pass 1 for `.py`.
Use the **code branch** for both runs (both corpora are `.py`).

### Consumer (signal/noise) ###

- **Consumer:** the future SymptomLab vault build (`T-SYMGRAPH-VAULT`, parked) reads these
  two tiers to derive frontmatter; until then they are the canonical code/test index for the
  lab (queried in place of the stale `v2_current` for code symbols).
- **Code path:** `4dlab-vault` → `scripts/build_lab_vault.py` reads `graph/v2_code/graph.json`
  + `graph/v2_tests/graph.json` to inject the `module`/`implements`/`drift_guards`
  frontmatter on the copied notes. Real and existing once the vault task runs; the tiers are
  a prerequisite, not a speculative artefact.

### Deliverables ###

1. `labs/symptomlab/graph/v2_code/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) — CREATE.
2. `labs/symptomlab/graph/v2_tests/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) — CREATE.
3. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-4.md` — `## Plan` + both
   health-check verdicts + the `git status --porcelain` collateral proof + key-symbol
   spot-check.

### Files to touch ###

- `labs/symptomlab/graph/v2_code/` (CREATE — graphify output, relocated)
- `labs/symptomlab/graph/v2_tests/` (CREATE — graphify output, relocated)
- progress note (CREATE)

### Out of scope ###

Wiki and docs graphs (Pass 3 LLM) — PARKED, do not build. The Pass-3 cross-check (gated,
re-extracts a canonical graph — owner-only). The vault build. **HARD GUARDS — never skip:**

- **Never `graphify .` from a repo root** — scope each run to the exact corpus dir
  (`labs/symptomlab/symptomlab/`, then `labs/symptomlab/tests/`). This is the rule the
  81.9k-node incident exists to enforce.
- **Never touch `graphify-out/`** (FROZEN ~43k-node root graph), `v2_current/`, or
  `v1_baseline/`.
- **Relocate, then confirm no root `graphify-out/` survives** — move `graph.json` +
  `GRAPH_REPORT.md` + `graph.html` into each destination dir.
- **No collateral** — every other `graph/*` dir byte-unchanged.
- A missing edge is a **prep gap routed back to T-SYMGRAPH-2/3**, never patched into
  `graph.json` by hand.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# (build via 4dlab-graphify-run code branch, scoped — see its SKILL.md for the exact CLI)
#   run 1 scope: labs/symptomlab/symptomlab   -> relocate to labs/symptomlab/graph/v2_code/
#   run 2 scope: labs/symptomlab/tests        -> relocate to labs/symptomlab/graph/v2_tests/

# Health-check each new tier (Part-A: reads graph.json only, no LLM, no tokens)
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/symptomlab/graph/v2_code/graph.json
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/symptomlab/graph/v2_tests/graph.json

# Collateral proof — only the two new tiers may show as changed
git status --porcelain labs/symptomlab/graph

# Confirm no stray root output survived
test ! -e graphify-out/graph.json && echo "OK: no root graphify-out" || echo "FAIL: relocate incomplete"
```

Both health verdicts must read **GOOD** (dangling=0, isolated=0). Spot-check that key
symbols resolve to correct file/line in `v2_code` (e.g. `grep` the validator's `validate`
entry point and the `allowed_combinations` catalog node). Paste both verdicts + the
collateral proof into the progress note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-4`: Status=done, Files changed=2 tiers, Verification="v2_code + v2_tests built, both GOOD, 0 collateral".
