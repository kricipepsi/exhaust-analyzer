# T-SYMGRAPH-LLM — Build the Pass-3 LLM tiers `v2_wiki/` + `v2_docs/` (KG-LANE)

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE / KG-lane (token cost)
**Blocked by:** T-SYMGRAPH-WIKIPREP, T-SYMGRAPH-DOCPREP

> **THIS IS A KG-LANE TASK** — the second sanctioned exception to the standing graph-rebuild
> guard ([GRAPH GATE] in START_HERE), alongside T-SYMGRAPH-4. graphify runs **only** here,
> **only** on the two scopes below, and **never** on a repo root, `graphify-out/`,
> `v2_current/`, or `v1_baseline/`. These are **new** tiers (`v2_wiki`/`v2_docs` do not exist
> for symptomlab) — this is a first build, not a re-extraction of a canonical graph.
>
> **Cost note:** Pass 3 is an **LLM** pass — it costs tokens + needs the backend. Unlike the
> free Pass-1 AST run (T-SYMGRAPH-4), confirm the owner expects the spend before running.

### Goal ###

Build SymptomLab's two **Pass-3 (LLM, semantic)** graph tiers with `4dlab-graphify-run`
(`resolve → run → relocate → verify`), `--directed`, one per corpus, each relocated into its
destination dir and health-checked. Proof of done: `labs/symptomlab/graph/v2_wiki/graph.json`
and `labs/symptomlab/graph/v2_docs/graph.json` exist, nodes/edges > 0, **0 dangling**,
**EXTRACTED dominant**, health verdict **GOOD**, no collateral change to any other `graph/*`
dir.

### Success criteria ###

- `labs/symptomlab/graph/v2_wiki/graph.json` built from `labs/symptomlab/wiki/` (Pass 3,
  `--directed`); health verdict **GOOD** (dangling=0, nodes/edges>0, EXTRACTED dominant).
  *Isolated nodes are expected for wiki* (fault/enum stubs awaiting relations) — not a defect.
- `labs/symptomlab/graph/v2_docs/graph.json` built from
  `labs/symptomlab/graph/v2_docs/ingest_ready/` (Pass 3, `--directed`); health verdict
  **GOOD** (dangling=0, **isolated=0** — docs should be fully wired, like code).
- Both dirs also contain the relocated `GRAPH_REPORT.md` + `graph.html`; no root
  `graphify-out/` survives.
- `git status --porcelain labs/symptomlab/graph` shows **only** the two new tier dirs changed —
  `v2_code/`, `v2_tests/`, `v2_current/`, `v1_baseline/`, `DIFF_REPORT.md` byte-unchanged.

### Context ###

This fills the **wiki + docs** half of SymptomLab's graph (T-SYMGRAPH-4 built the code+tests
half). Both corpora are `.md` prose → Pass 3 (LLM semantic read), `--directed`, unlike the
offline AST Pass 1. The prep tasks (WIKIPREP, DOCPREP) already made relations explicit, so the
extractor should produce EXTRACTED-dominant graphs. A missing edge is a **prep gap routed back
to WIKIPREP/DOCPREP**, never patched into `graph.json` by hand.

**Load skills:** `_skills\graph\4dlab-graphify-run\SKILL.md` — read end-to-end first. Use the
**wiki branch** for the wiki run and the **docs branch** for the docs run. ⚠ The pipeline guide
(§5) flags that the docs branch was being added under `T-VAULT-DOCGRAPH-1` — **confirm the docs
branch (dest `graph/v2_docs/`, verify focus = architectural-predicate proof-set) is present in
the installed skill before running the docs corpus.** If it is absent, STOP and surface it
(critical ambiguity (a): named skill operation missing).

Eval scripts for the health-check: `_skills/graph/eval/eval-wiki-graph/` and
`_skills/graph/eval/eval-doc-graph/`.

### Consumer (signal/noise) ###

**Adds no schema field.** The two graphs are consumed by the SymptomLab vault build
(`T-SYMGRAPH-VAULT`): `4dlab-vault` → `scripts/build_lab_vault.py` reads
`graph/v2_wiki/graph.json` + `graph/v2_docs/graph.json` to inject `module`/`implements`/
`consumers`/`drift_guards` frontmatter on the copied wiki + docs notes, and the three `.base`
views read them as the design→code→test spine. Real and existing once the vault task runs; the
tiers are its prerequisite.

### Deliverables ###

1. `labs/symptomlab/graph/v2_wiki/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) — CREATE.
2. `labs/symptomlab/graph/v2_docs/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) — CREATE.
3. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-LLM.md` (CREATE) — `## Plan` +
   both health verdicts + the EXTRACTED-vs-INFERRED split + `git status --porcelain` collateral
   proof + the no-root-`graphify-out` check.

### Files to touch ###

- `labs/symptomlab/graph/v2_wiki/` (CREATE — graphify output, relocated)
- `labs/symptomlab/graph/v2_docs/` (CREATE — graphify output, relocated; sits beside the
  `ingest_ready/` tree DOCPREP made)
- progress note (CREATE)

### Out of scope ###

The Pass-3 cross-check (Part B — re-extracts a canonical graph into a scratch dir, owner-gated;
tasks `T-VAULT-WIKIGRAPH-1`/`-DOCGRAPH-2` elsewhere). The vault build (T-SYMGRAPH-VAULT). No
prose/prep edits — a missing edge is routed back to the prep task, never patched into
`graph.json`. **HARD GUARDS — never skip:**

- **Never `graphify .` from a repo root** — scope each run to the exact corpus
  (`labs/symptomlab/wiki/`, then `labs/symptomlab/graph/v2_docs/ingest_ready/`). The
  81.9k-node incident rule.
- **Never touch `graphify-out/`** (FROZEN root graph), `v2_current/`, `v1_baseline/`,
  `v2_code/`, `v2_tests/`.
- **Relocate, then confirm no root `graphify-out/` survives.**
- **No collateral** — every other `graph/*` dir byte-unchanged.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# (build via 4dlab-graphify-run, --directed, scoped — see its SKILL.md for the exact CLI)
#   run 1 scope: labs/symptomlab/wiki                          -> relocate to graph/v2_wiki/
#   run 2 scope: labs/symptomlab/graph/v2_docs/ingest_ready    -> relocate to graph/v2_docs/

# Health-check each new tier (Part-A: reads graph.json only, no extra LLM, no tokens)
python _skills/graph/eval/eval-wiki-graph/scripts/eval_wiki_graph.py labs/symptomlab/graph/v2_wiki/graph.json
python _skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py  labs/symptomlab/graph/v2_docs/graph.json

# Collateral proof — only the two new tiers may show as changed
git status --porcelain labs/symptomlab/graph

# Confirm no stray root output survived
test ! -e graphify-out/graph.json && echo "OK: no root graphify-out" || echo "FAIL: relocate incomplete"
```

Both health verdicts must read **GOOD** (wiki: dangling=0, EXTRACTED dominant, isolated
expected; docs: dangling=0, isolated=0, EXTRACTED dominant). Paste both verdicts + the
collateral proof into the progress note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-LLM`: Status=done, Files=2 tiers,
Verification="v2_wiki + v2_docs built, both GOOD, EXTRACTED-dominant, 0 collateral".
