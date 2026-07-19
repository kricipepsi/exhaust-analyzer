---
node_type: task
task_id: T-GAS-GRAPH-LLM
status: void
pack: VAULT
lab: gaslab
mode: graph-tooling
blocked_by:
- T-GAS-WIKIPREP
- T-GAS-DOCPREP
consumers:
- consumers.base — signal/noise audit view
- graph/v2_docs — docs graph
- graph/v2_wiki — wiki graph
implements:
- graph/v2_docs/graph.json
- graph/v2_wiki/graph.json
tags:
- task
- vault
- gaslab
---

# T-GAS-GRAPH-LLM — Graphify GASLab wiki + docs (Pass 3 LLM) → `graph/v2_wiki/`, `graph/v2_docs/`

**Status:** `void — owner waived Pass-3` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING (sanctioned graphify run — see §0)
**Origin:** pipeline guide §5 (ingestion, wiki + docs corpora) · **Blocked by:** T-GAS-WIKIPREP, T-GAS-DOCPREP
**Consumer (signal/noise):** **Adds no schema field.** Builds the two Pass-3 graphs the vault build
reads to derive `consumers` / `implements` / `source` frontmatter (`consumers.base` signal/noise audit
view, plan §4). The graphs are the consumer surface; no new fields ship here.

### §0 — Sanctioned graphify run (same exception as T-GAS-GRAPH-AST) ###

**Owner direction 2026-06-11:** do not run this Pass-3 LLM step for GASLab. The Phase-2 wiki/doc prep
outputs are sufficient for this vault pack, and avoiding the token-spending third pass is intentional.
Leave `graph/v2_wiki/` and `graph/v2_docs/graph.json` absent unless the owner explicitly reopens this
task later.

Explicit, owner-instructed; builds **new** tier dirs; **does not** touch `graph/v2_current/` or
`graph/v1_baseline/`. Guards: never `graphify .` from a repo root — scope to the wiki dir then the
prepped docs dir; relocate and confirm no root `graphify-out/` survives; other `graph/*` dirs
byte-unchanged.

### Runs (Pass 3 LLM — costs tokens + backend; `--directed`) ###

| Corpus | Scope dir | Dest | Notes |
|---|---|---|---|
| wiki | **`labs/gaslab/wiki/`** (NOT `research/chunks/`) | `labs/gaslab/graph/v2_wiki/` | prepped trailers from T-GAS-WIKIPREP |
| docs | `labs/gaslab/graph/v2_docs/ingest_ready/` | `labs/gaslab/graph/v2_docs/` | prepped chunks from T-GAS-DOCPREP |

> **Docs branch check:** `4dlab-graphify-run` originally documented only code+wiki branches; the docs
> branch (dest `graph/v2_docs/`, verify focus = architectural-predicate proof-set) was added under
> OBDLab `T-VAULT-DOCGRAPH-1`. **Confirm that branch is present in the skill before running the docs
> corpus.** If absent, stop and surface it (do not improvise a docs run).

Flow per corpus: `resolve → run → relocate → verify`.

### Success criteria ###

1. `graph/v2_wiki/{graph.json,GRAPH_REPORT.md,graph.html}` and `graph/v2_docs/{…}` exist; counts > 0.
2. **EXTRACTED dominates** on both (Pass-3 quality signal — the WIKIPREP/DOCPREP explicit relations are
   why); `INFERRED`/`AMBIGUOUS` is the minority.
3. **Health-check passes (Part-A only — cross-check SKIPPED this pack):**
   ```bash
   python _skills/graph/eval/eval-wiki-graph/scripts/eval_wiki_graph.py labs/gaslab/graph/v2_wiki/graph.json
   python _skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py  labs/gaslab/graph/v2_docs/graph.json
   ```
   Expect GOOD. **0 dangling** on both. **isolated > 0 is a defect for docs** (wire every node) but
   **expected for wiki** (fault/enum stubs await relations) — the wiki skill does not flag it.
4. **No collateral:** `v2_current` / `v1_baseline` byte-unchanged; no stray root `graphify-out/`.
5. A missing/weak edge is a **prep gap routed back to T-GAS-WIKIPREP/DOCPREP** — never patched into
   `graph.json`.

### Out of scope ###

- The gated Pass-3 LLM **cross-check** (`eval-*-graph` two-graph mode, scratch `*_llm/` dirs) — that is
  the "graph review" the owner **deferred** for this pack. Do not run it; do not author it.
- Code/test graphs (→ T-GAS-GRAPH-AST). Re-extracting `v2_current` (forbidden).

### Files to touch ###

- `labs/gaslab/graph/v2_wiki/…`, `labs/gaslab/graph/v2_docs/…` (new).

### Verification ###

```bash
cd <repo>/4DLabV2
ls labs/gaslab/graph/v2_wiki labs/gaslab/graph/v2_docs
test -d labs/gaslab/graphify-out && echo "FAIL stray graphify-out" || echo "OK relocated"
git status --porcelain labs/gaslab/graph/v2_current labs/gaslab/graph/v1_baseline | grep . \
  && echo "FAIL canonical touched" || echo "OK"
python _skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py labs/gaslab/graph/v2_docs/graph.json
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-GRAPH-LLM.md` opens with the confirmed `## Plan` (incl. docs-branch
presence confirmation); the run session fills `VERIFICATION GATE` (two graphs, EXTRACTED-dominant,
health GOOD, 0 dangling, docs 0 isolated, canonical untouched) + `CODE REVIEW` (counts, confidence
split). Ledger row → `done` only when clean.

For the waived path, record the owner direction in the progress note and leave the ledger row `void`
instead of `done`.
