---
node_type: task
task_id: T-VAULT-DOCGRAPH-1
status: done
pack: VAULT · **Mode:** GRAPH-TOOLING lane
lab: obdlab
mode: graph-tooling lane
blocked_by:
- T-VAULT-DOCPREP-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_docs — docs graph
- /check-impact command
- /graph-find command
- design→code→test spine (.base views)
implements:
- graph/v2_docs/graph.json
tags:
- task
- vault
- obdlab
---

# T-VAULT-DOCGRAPH-1 — Graphify the prepared docs tier → `graph/v2_docs/` (TODO-4, part 2)

**Status:** `done` · **Pack:** VAULT · **Mode:** GRAPH-TOOLING lane (graphify run — no lab inner-loop/gate)
**Origin:** HANDOFF TODO-4 + plan §2 "docs tier pending TODO-4" + owner request 2026-06-10 · **Blocked by:** T-VAULT-DOCPREP-1
**Consumer (signal/noise):** **Adds no schema field.** Produces `graph/v2_docs/graph.json` — the docs-tier piece the
4-tier vault model (plan §2, wired by T-VAULT-PATHS-1 `done`) already routes on. Consumers: the **vault build**
(`build_lab_vault.py` reads the graph to inform design-doc frontmatter) and the **design→code→test spine** in the
three `.base` views (`modules.base` / `consumers.base` / `drift-guards.base`) + `/check-impact` / `/graph-find`
(plan §4). Edge-level signal/noise was enforced upstream in T-VAULT-DOCPREP-1; this task does **not** invent or
patch edges — a missing edge is a prep gap routed back to `4dlab-doc-prep`, never stamped into `graph.json`.

### Role note (graph-tooling lane) ###

Running `4dlab-graphify-run` is graph tooling, not lab diagnostic code — no `obdlab/` inner-loop / 6-phase gate.
The skill is authored; this task **runs** it (resolve → run → relocate → verify) on the **prepared** docs chunks
and confirms graph health. It **never** edits source/docs and **never** post-patches `graph.json`.

### Goal ###

Ingest the prepared `graph/v2_docs/ingest_ready/` chunk tree (Pass-3 LLM, prose) into the canonical docs-tier graph
`graph/v2_docs/`, and **fix the one skill gap the owner flagged**: `4dlab-graphify-run` currently documents only
**code** and **wiki** corpora — it has no **docs** branch, even though the doc-prep skill emits a third corpus into
`graph/v2_docs/`. Without the branch, a run session has no documented destination/verify-focus for design docs and
would mis-route them to the wiki path.

### Skill gap (the owner's "check if skill needs separate mention of docs") — CONFIRMED, fix is a deliverable ###

`_skills/graph/4dlab-graphify-run/SKILL.md` mentions only two corpora. The docs corpus is **prose like wiki** (Pass-3
LLM, `--directed`) but its **destination is `graph/v2_docs/`**, its **prep skill is `4dlab-doc-prep`** (not
`4dlab-wiki-prep`), and its **verify focus is the architectural-predicate proof-set** (`consumes` /
`mirrors_contract_in` / `supersedes` / `verifies`), not the generic wiki proof-set. The fix adds the docs branch
everywhere the wiki branch appears:

```text
ASCII — where the docs branch slots in (mirrors wiki, new destination):

  resolve ─┬─ .py            → code branch  → graph/v2_code/   (Pass 1, offline)
           ├─ .md (research) → wiki branch  → graph/v2_wiki/   (Pass 3, LLM)
           └─ .md (ingest_ready/ from doc-prep) → DOCS branch → graph/v2_docs/  (Pass 3, LLM, --directed)  ← ADD
                                                  verify: EXTRACTED ratio + architectural-predicate proof-set
                                                  miss → route back to 4dlab-doc-prep (NOT wiki-prep)
```

### Success criteria ###

1. `graph/v2_docs/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) exist, relocated out of any root `graphify-out/`;
   `test -d graphify-out` is false (no surviving root artefact).
2. Health check: `nodes > 0`, `links > 0`; relation-type distribution reported; isolated-node count reported and
   explained; **EXTRACTED dominates** INFERRED/AMBIGUOUS (the prep aimed for that).
3. Architectural-predicate spot-check: the key edges the prep made explicit are present — at minimum the
   `SUPERSEDES`, `MIRRORS_CONTRACT_IN`, `CONSUMES`, `VERIFIES` lines from the prepped chunks resolve to graph edges;
   report found/missing with the chunk anchor. **Any miss is routed back to `4dlab-doc-prep` to make the relation
   explicit and re-run — never patched into `graph.json`.**
4. **No collateral:** `graph/v1_baseline/`, `graph/v2_code/`, `graph/v2_tests/`, `graph/v2_wiki/` byte-unchanged
   (`git status --porcelain` + mtime). `research/chunks/` not moved; `graphify-out/manifest.json` untouched.
5. **Never run from repo root** (the 81.9k-node guard) — scoped to `graph/v2_docs/ingest_ready/` only.
6. `4dlab-graphify-run/SKILL.md` carries a complete **docs branch** (Deliverable 1 below).

### Deliverables ###

1. `_skills/graph/4dlab-graphify-run/SKILL.md` — **add the docs branch** (graph-tooling lane edit):
   - **Corpus table** (§ "Purpose"): add a **docs** row — input prepped `.md` design-doc chunks; pass *Pass 3 — LLM*;
     cost *tokens + backend*; verify focus *EXTRACTED ratio + architectural-predicate proof-set*.
   - **`description` frontmatter:** add docs/design-doc corpus to the corpus list and to the "prep comes first"
     sentence (`4dlab-doc-prep` for design docs).
   - **Step 1 `resolve`:** detect the docs corpus (path under `graph/v2_docs/ingest_ready/`) → destination
     `graph/v2_docs/`, `--directed` (directed predicates, like the OBDLab wiki).
   - **Step 2 `run`:** docs take the Pass-3 path, scoped to the `ingest_ready/` dir (never `.`).
   - **Step 3 `relocate`:** `graph/v2_docs/` destination.
   - **Step 4 `verify`:** docs branch references the architectural-predicate proof-set and routes misses back to
     **`4dlab-doc-prep`** (not wiki-prep); collateral check lists `v2_wiki` + `v2_code` + `v2_tests`.
   - **Reference / prep-skills list:** add `4dlab-doc-prep` (design docs).
2. `graph/v2_docs/graph.json` + `GRAPH_REPORT.md` + `graph.html` — the built, relocated docs-tier graph.

### Files to touch ###

- `_skills/graph/4dlab-graphify-run/SKILL.md` (add docs branch)
- `labs/obdlab/graph/v2_docs/graph.json` (+ `GRAPH_REPORT.md`, `graph.html`) — new

### Out of scope ###

- Editing source/docs or the prepped chunks — that is `4dlab-doc-prep` / T-VAULT-DOCPREP-1.
- Patching missing edges into `graph.json` — forbidden; route back to prep.
- Re-running `graph/v2_wiki|v2_code|v2_tests` extraction — canonical, do not rebuild (CLAUDE.md HARD RULE).
- The vault populate build (`build_lab_vault.py --lab obdlab`) — separate step (plan §8) the docs tier now unblocks.

### Verification (graph-tooling lane) ###

```bash
cd <repo>/labs/obdlab
# 1) built + relocated, no root artefact survives
test -f graph/v2_docs/graph.json && echo "OK graph present" || echo "FAIL no graph"
test -d graphify-out && echo "FAIL root graphify-out remains" || echo "OK relocated"
# 2) health: nodes/links/relation split, EXTRACTED dominates
python3.14 - <<'PY'
import json,collections
g=json.load(open('graph/v2_docs/graph.json'))
n,l=g.get('nodes',[]),g.get('links',[])
conf=collections.Counter((e.get('confidence_tag') or e.get('tag') or '?') for e in l)
print('nodes',len(n),'links',len(l)); 
for k,c in conf.most_common(): print(f'  {c:4d} {k}')
PY
# 3) no collateral on the other three graph pieces
git status --porcelain graph/v1_baseline graph/v2_code graph/v2_tests graph/v2_wiki | grep . \
  && echo "FAIL other graphs changed" || echo "OK no collateral"
# 4) corpus + manifest untouched
git status --porcelain research/chunks graphify-out/manifest.json | grep . \
  && echo "FAIL corpus/manifest changed" || echo "OK corpus/manifest intact"
# 5) skill now has a docs branch
grep -qiE 'v2_docs' ../../_skills/graph/4dlab-graphify-run/SKILL.md \
  && echo "OK skill docs branch present" || echo "FAIL skill still code+wiki only"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-DOCGRAPH-1.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (the five checks + node/edge counts + EXTRACTED split + proof-set found/missing) + `CODE REVIEW`
(skill docs-branch diff; graph counts). The plan §8 row flips to `done` only when both blocks are clean, the docs
graph is built+relocated, the proof-set passes (or misses are routed back to prep), and no collateral changed.
Verification = "graph/v2_docs/ built from ingest_ready/ (Pass-3, directed), EXTRACTED dominant, architectural
proof-set resolves, root graphify-out gone, no collateral on v2_code/v2_tests/v2_wiki, manifest untouched;
graphify-run SKILL.md gains a docs branch (dest graph/v2_docs/, prep=4dlab-doc-prep)".
