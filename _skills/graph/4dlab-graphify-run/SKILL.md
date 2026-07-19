---
name: 4dlab-graphify-run
description: >
  Run graphify safely on a PREPARED 4DLab corpus and verify the result — for both code packages and
  wiki/prose, and docs/design-doc corpora. Encodes the scoped run, the never-run-from-root guardrail (the 81.9k-node incident),
  output relocation to a named graph dir, and a verification pass (node/edge health + corpus-specific
  spot-check).
  Use this skill whenever the user wants to build/run/refresh a graphify knowledge graph, run
  /graphify on a directory, ingest a package, wiki, or docs corpus into a graph, relocate graphify-out, or verify a
  freshly built graph.json (counts, key symbols, EXTRACTED/INFERRED ratio, isolated nodes). Use it
  for GASLab, OBDLab, DTCLab, COMLab, DNALab.
  Prep comes FIRST in a separate session: 4dlab-code-prep for .py source, 4dlab-wiki-prep for .md
  prose, and 4dlab-doc-prep for prepared docs/design-doc chunks. THIS skill is the build/verify step
  that runs after prep. It auto-handles the difference between a code corpus (Pass 1, AST, offline,
  free), a docs corpus (offline structure extraction — free, no key; after doc-prep edges come back EXTRACTED), and a wiki corpus (Pass 3, LLM — the ONLY tier that costs tokens + needs a backend).
  Supersedes the build/proof/criteria half of the retired 4dlab-graph skill.
allowed-tools: Read, Grep, Glob, Bash
metadata:
  version: "0.1"
  verified-graphifyy: "0.9.7 (2026-07-06, T-GR-2; note: 0.9.x output drops built_at_commit — stale-check via mtime/GRAPH_REPORT). CAVEAT (T-GR-9, 2026-07-06): 0.9.7 extracts ZERO nodes from JSON files (upstream #1666) — for any JSON-bearing corpus (kg configs, registry rules, fixtures) BUILD with the 0.8.36 rollback pin in a throwaway venv; 0.9.7 stays the query CLI"
  argument-hint: "[corpus-path] [--directed] — auto-detects code vs wiki"
  model: sonnet
  context: fork
---

## Purpose

The ingestion *step* is one command — `/graphify <path>` — but it has one recurring catastrophic
failure (running it from the repo root produced an 81.9k-node graph and overwrote work) and a couple
of must-not-skip safety and verification steps. This skill encodes the safe procedure once so every
build session inherits it, for **code, wiki, and docs** corpus types. graphify auto-routes by file
extension and the scoped input path:

| Corpus | graphify pass | Cost | Verify focus |
|---|---|---|---|
| **code** (`.py` package) | Pass 1 — tree-sitter AST, offline | free, no API key | key-symbol presence, `imports`/`calls` edges |
| **wiki** (`.md` prose) | Pass 3 — LLM subagents | tokens + a backend | EXTRACTED/INFERRED ratio, proof-set |
| **docs/design-docs** (prepared `.md` chunks in `graph/v2_docs/ingest_ready/`) | offline structure extraction (`graphify update`); LLM Pass-3 optional | **free, no key** (LLM optional, marginal) | EXTRACTED dominance, architectural predicates (`SUPERSEDES`, `MIRRORS_CONTRACT_IN`, `CONSUMES`, `VERIFIES`) |

This skill **runs graphify and reads the result**; it does **not** edit source or wiki (that is the
prep skills) and does **not** post-patch `graph.json`.

**Flow:** `resolve` → `run` → `relocate` → `verify`. Run it end-to-end unless the user asks for one
stage.

---

> **graphify ≠ LLM (canon):** code/tests/docs tiers build **offline & free** via `graphify update` (no key, no backend); only the **wiki** tier runs an LLM Pass-3. If an AST/docs build asks for a key, you used `extract` instead of `update`. Full canon: `GRAPH_AUDIT_2026-06-28.md`.

## Hard guards (read first — these are the failure modes)

- **NEVER `graphify update .` or `/graphify .` from a repo root.** Always scope to the specific
  package or chunks subdirectory. This is the rule the 81.9k-node incident exists to enforce.
- **Never re-run extraction on a canonical graph.** `graphify-out/graph.json` artefacts that are
  already verified are canonical — do not rebuild them unless explicitly instructed.
- **No collateral.** Other `graph/*` dirs (`v1_baseline/`, `v2_current/`, the *other* corpus's graph)
  must be byte-unchanged. Verify with `git status --porcelain` and mtime.
- **No surviving root-level `graphify-out/`** after the task — relocate, then confirm it's gone.
- **Confirm prep + any code-freeze gate are done** before running (a code map built on in-flux source
  is stale).

---

## Step 1 — `resolve` (target + corpus type)

Take the corpus path (e.g. `obdlab/obdlab`, `obdlab/research/chunks`, or
`obdlab/graph/v2_docs/ingest_ready`). **Base root:** `/agent_workspace`. Detect corpus type by contents:

- mostly `.py` → **code branch** (offline; no API key required).
- mostly `.md` → **wiki branch** (LLM; needs a backend — `claude-cli` uses the Claude subscription,
  no key; otherwise an API key per graphify's backend list).

Pick the destination dir (`graph/v2_code/` for code, `graph/v2_wiki/` for wiki) and decide
`--directed` (the OBDLab wiki used directed; the code map defaults undirected unless a true
call-direction graph is wanted). For the docs branch, use `graph/v2_docs/` as the destination and
run with `--directed`. Record the choices.

---

## Step 2 — `run` (scoped, never from root)

**Linux headless (this host): the CODE branch has no `/graphify` slash command wired — use the CLI.**
graphify is installed in `.venv-wired`; the deterministic offline AST build uses **`graphify update`**
(NOT `graphify extract`):
```bash
cd /agent_workspace/labs/<lab>
# copy the scoped corpus to /tmp first so no graphify-out/ lands in the repo, then:
env -u GEMINI_API_KEY -u GOOGLE_API_KEY -u DEEPSEEK_API_KEY -u ANTHROPIC_API_KEY -u OPENAI_API_KEY \
  graphify update /tmp/<lab>_<corpus>
# update writes graph.json + GRAPH_REPORT.md + graph.html in one offline pass — no LLM, no key.
# relocate /tmp/<lab>_<corpus>/graphify-out/{graph.json,GRAPH_REPORT.md,graph.html} → graph/<dest>/
```
**`graphify update` = "re-extract code files, no LLM needed"** — the correct key-free path for a code
corpus. **Do NOT use `graphify extract` here:** that subcommand is "AST **+ semantic LLM**" and its
backend defaults to whichever API key is set, so it (or a stale key) is what makes a run demand a
backend/Ollama/bridge. If you only need GRAPH_REPORT.md/graph.html regenerated on an existing graph,
`graphify cluster-only <path> --no-label` does that offline too. Building under `/tmp` (not the repo)
guarantees no stray `graphify-out/` survives in the tree.

_Original slash-command flow (only when the graphify skill is installed into the agent platform):_
```bash
cd <repo>/labs/<lab>   # repo root = /agent_workspace
# CODE branch — offline AST, no key:
/graphify <scoped-package>            # e.g. obdlab/obdlab   [add --directed for call direction]
# WIKI branch — LLM Pass 3, costs tokens:
/graphify <scoped-chunks-dir> --directed   # e.g. research/chunks
# DOCS branch - LLM Pass 3, prepared design chunks, costs tokens:
/graphify graph/v2_docs/ingest_ready --directed
```

Never substitute `.` (root) for the scoped path. For wiki/docs, confirm a backend is available
before spending tokens.

**Backend selection (Pass 3 only) — name it explicitly.** graphify auto-detects the backend from
whichever API key is set, in the fixed order `gemini → kimi → claude → openai → deepseek → …`. A stale
`ANTHROPIC_API_KEY`/`OPENAI_API_KEY` in the environment therefore *shadows* DeepSeek silently. Always
pass the backend by name so the run is deterministic:

```bash
/graphify <scoped-dir> --directed --backend deepseek    # DEEPSEEK_API_KEY set; default model deepseek-v4-flash
```

`--backend claude-cli` is only viable when the local `claude` CLI is authenticated (`loggedIn: true`);
an unauthenticated CLI fails the whole pass (the 2026-06-10 DOCGRAPH-1 incident). DeepSeek is the
default Pass-3 backend for this workspace.

---

## Step 3 — `relocate`

```bash
mkdir -p graph/<dest>          # v2_code, v2_wiki, or v2_docs
mv graphify-out/graph.json       graph/<dest>/graph.json
mv graphify-out/GRAPH_REPORT.md  graph/<dest>/GRAPH_REPORT.md
mv graphify-out/graph.html       graph/<dest>/graph.html
test -d graphify-out && echo "FAIL: root graphify-out remains" || echo "OK: relocated"
```

---

## Step 4 — `verify`

Shared health check (harvested from the proven `4dlab-graph health` op) — parse `graph.json` and
report node/edge counts, relation-type distribution, isolated-node count, and top god nodes:

```python
import json, collections
g = json.load(open(GRAPH_JSON))
nodes, links = g.get('nodes', []), g.get('links', [])
rels = collections.Counter(e.get('relation','?') for e in links)
deg = collections.Counter()
for e in links: deg[e['source']] += 1; deg[e['target']] += 1
he = set(m for h in g.get('hyperedges', []) for m in h.get('members', []))
isolated = [n['id'] for n in nodes if deg[n['id']] == 0 and n['id'] not in he]
print("nodes", len(nodes), "links", len(links), "isolated", len(isolated))
for r, c in rels.most_common(): print(f"  {c:4d}  {r}")
```

Then the corpus-specific spot-check:

**Code branch.** Assert `nodes > 0` and `links > 0` (not the empty-graph error), then grep the node
labels for the key symbols the task names (e.g. `o2_normalizer`, `translate`, `OBDLivePayload`,
`O2FailureMode`, `TrimAnalyticsGate`). Expect structural relations (`calls`, `imports`, `implements`);
do **not** expect domain edges or `rationale` nodes unless the corpus has rich docstrings/comments.

**Wiki branch.** Report the `EXTRACTED` / `INFERRED` / `AMBIGUOUS` split and confirm EXTRACTED
dominates (the prep aimed for that). If a proof-set exists, check each expected edge against the
graph (harvested `4dlab-graph proof` logic) and report found/missing with the wiki anchor — never
patch a missing edge into `graph.json`; route it back to `4dlab-wiki-prep` to make the relation
explicit and re-run.

**Docs branch.** Report the `EXTRACTED` / `INFERRED` / `AMBIGUOUS` split and confirm EXTRACTED
dominates. Check the docs-prep architectural predicates in extracted graph edges:
`SUPERSEDES`, `MIRRORS_CONTRACT_IN`, `CONSUMES`, `VERIFIES` (also accept lowercase equivalents).
Report found/missing with the source chunk anchor when available. Never patch a missing edge into
`graph.json`; route missing proof edges back to `4dlab-doc-prep` to make the relationship explicit
and re-run.

**Collateral check (both):**

```bash
git status --porcelain graph/v1_baseline graph/v2_current <other-corpus-graph> | grep . \
  && echo "FAIL: other graphs changed" || echo "OK: no collateral"
```

---

## Step 5 — Pass 3 noise control (checker, not adder)

Pass 3 is an LLM reading prose, so left unconstrained it *adds* plausible-but-unsourced edges — the
exact noise the signal/noise rule forbids. Run it as a **checker against the deterministic graph**, not
as a writer into it. The discipline:

- **Default mode, never `--deep`.** Deep mode is explicitly designed to emit *more* `INFERRED` edges
  (broad conceptual/architectural guesses). Plain extraction stays close to what the text states.
- **Build into a SEPARATE dir** (`graph/v2_docs_llm/`), never over the canonical `graph/v2_docs/`. The
  LLM graph is a scratch comparison artefact, not a deliverable graph.
- **graphify already tags every Pass-3 edge** `confidence: EXTRACTED | INFERRED | AMBIGUOUS`
  (`EXTRACTED` = explicit in source; `INFERRED` = model guess; `AMBIGUOUS` = flagged). And
  `semantic_cleanup` already drops edges that reference a non-existent node. Lean on both.

**Promotion gate — an edge from the LLM graph may influence the canonical graph only if it passes ALL:**

```text
LLM edge (src → tgt, relation, confidence)
   │
   ├─ confidence == EXTRACTED ?                         no ─► DROP (INFERRED/AMBIGUOUS never auto-promote)
   ├─ both src and tgt already exist in v2_docs ?       no ─► DROP (no new nodes from a checker run)
   ├─ already present in deterministic v2_docs ?        yes ─► CONFIRMED — no action (this is the win:
   │                                                            it proves the deterministic pass is complete)
   └─ MISSING from v2_docs AND edge-type has a NAMED
      COMLab/fault-atlas consumer ?
            yes ─► real gap → route to 4dlab-doc-prep: make the relation EXPLICIT in the chunk,
                   then re-run the DETERMINISTIC docs pass. NEVER patch graph.json.
            no  ─► consumer-less → proposals registry (comlab/config/proposals/) or DROP. Not the graph.
```

The output of a checker run is a **diff report**, not an edited graph: `CONFIRMED` (LLM agrees with
deterministic), `GAP` (EXTRACTED edge with a consumer the deterministic pass missed → prep fix), and
`NOISE` (INFERRED/AMBIGUOUS/consumer-less → rejected). A clean run is mostly CONFIRMED with zero GAPs —
that is positive evidence the hand-authored relation blocks are complete, which is the whole point of
running Pass 3 here.

## Output conventions

- Section header: `--=={ 4dlab-graphify-run: CORPUS / STAGE }==--`
- Always report the four results: counts, spot-check, relocation confirmed, no-collateral confirmed.
- Never edit source/wiki and never write to `graph.json`. A missing edge is a prep gap, not a patch.

## Reference

- graphify pipeline, passes, confidence tags, graph format —
  `https://github.com/safishamsi/graphify/blob/v8/docs/how-it-works.md`.
- Prep skills: `4dlab-code-prep` (source), `4dlab-wiki-prep` (prose),
  `4dlab-doc-prep` (docs/design-doc chunks).
