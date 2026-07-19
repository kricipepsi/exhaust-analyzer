# T-KG-OBD-1 — Graphify ingest of the enhanced OBDLab wiki → brand-new KG

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Lane:** dedicated **KG-lane** task — the *only* OBDLab task permitted to run graphify
(`OBDLAB_TASKS_START_HERE.md` §0: "A build runs only inside a dedicated `T-PREP-*`/`T-KG-*`
task whose own Deliverables name `graph.json`"). This task's deliverable **is** `graph.json`.
**Blocked by:** — (the wiki enhancement pass is **done** — see
`research/CHUNK_ENHANCEMENT_PREP_REPORT.md`).
**Consumer (signal/noise):** the produced `graph.json` is a **KG artefact, not a schema field**,
so the field-level signal/noise rule does not bite. Its named consumer is the **architect's
KG-query / fault-atlas-design workflow** (the same role the existing `graph/v2_current/graph.json`
plays for `/graphify query` and the wired graph-map `T-W-5`). The owner may later **promote** this
wiki KG to canonical; until then it is a parallel reference graph.

> **Task shape — read first.** This is a **mechanical KG build**, not a code change. No `gaslab/`
> or `obdlab/` Python is touched; no schema field is added. The architect has already applied the
> three IngestGraph.md enhancements to all 63 chunks (prep report above). The coder's job is to run
> the **graphify skill pipeline** on the enhanced wiki and land a **brand-new** `graph.json` in a
> **new** location, leaving the old graph intact.

## Why this exists

The enhanced wiki (`research/chunks/`, 63 `.md`) now states its diagnostic relations **explicitly**
as `**SUBJECT** PREDICATE **OBJECT**` lines and carries a per-chunk `## Core Entities` roster with
byte-identical entity labels (per `IngestGraph.md`’s three recommendations). Graphify pass-3 tags an
edge **EXTRACTED** (confidence 1.0) only when the relation is stated directly in text; the prior
graph (built before the enhancements) carries those links as weaker **INFERRED** edges or misses
them. Re-ingesting the enhanced corpus produces a KG whose diagnostic edges (e.g. `P0131 →
STUCK_LEAN`, `VACUUM_LEAK → DELTA_TRIM`) are now first-class EXTRACTED edges.

## Scope decision (owner-ratified 2026-06-08)

- **Brand-new build from the chunked wiki only.** INPUT = `research/chunks/` (the 63 enhanced
  `.md`). **Not** the whole `labs/obdlab` lab.
- **Do NOT overwrite `graph/v2_current/`.** That 1245-node / 1664-link graph (commit `f754422`) was
  built from the **whole lab** (code AST + docs) and is the **old** graph — it stays on disk,
  untouched, as the prior artefact.
- **Output to a NEW location:** `graph/v2_wiki/` (recommended name — **coder/owner may rename**;
  this is the one open naming detail). Holds `graph.json`, `GRAPH_REPORT.md`, `graph.html`.

## Procedure (the standard graphify pipeline)

Run the installed **graphify skill** (`/graphify`, `graphifyy 0.8.35` in `.venv-wired`). Steps per
the skill's `skill.md` (detect → extract AST+semantic → build/cluster → label → outputs → manifest).

**Canonical invocation** (from the lab root, pointed at the wiki, directed):

```
cd <repo>/labs/obdlab
/graphify research/chunks --directed
```

- `--directed` is **recommended**: the enhancement’s explicit relations are directional
  (`INDICATES`, `PRODUCES`, `CONSUMED_BY`, `SETS`, `SUPPRESSES` …); a directed graph preserves
  `source → target`. The existing lab graphs are undirected, so the **owner may drop `--directed`**
  for convention parity — record which was used in the progress note.
- Semantic extraction has **no `GEMINI_API_KEY`** set in this lab, so the skill dispatches
  **`general-purpose` subagents** (the host session is the LLM). 63 docs / ~320 KB → ~3 chunks of
  20–25 files. Use `subagent_type="general-purpose"` (NOT `Explore` — it cannot write chunk files).
- After the pipeline writes `./graphify-out/`, **relocate** it to the new lab graph dir:
  ```bash
  mkdir -p graph/v2_wiki
  mv graphify-out/graph.json graph/v2_wiki/graph.json
  mv graphify-out/GRAPH_REPORT.md graph/v2_wiki/GRAPH_REPORT.md
  mv graphify-out/graph.html graph/v2_wiki/graph.html
  # carry the interpreter/label sidecars the same way the existing v2_current/ dir holds them
  ```

## Hard guards (the recurring failure mode — do NOT repeat it)

- **NEVER run `graphify update .` from the repo root.** A prior session did this and regenerated the
  ~81.9k-node root `graphify-out/` — a rule violation, excluded from commits (PROGRESS.md "Unplanned
  follow-ups / incidents"). This task is scoped to `research/chunks` and outputs to `graph/v2_wiki/`
  **only**.
- **Do NOT touch `graph/v1_baseline/` or `graph/v2_current/`.** No overwrite, no clObber. They are
  excluded inputs (`.graphifyignore` already excludes `graph/v1_baseline/`); leave `v2_current/` as
  the old artefact.
- **Brand-new build — do not reuse the old whole-lab semantic cache.** Ensure no stale
  `graphify-out/` from the prior whole-lab run bleeds in (start clean; the wiki cache lives under the
  new output dir).
- No root-level `graphify-out/` may survive the task; if the pipeline created one, its contents are
  relocated to `graph/v2_wiki/` and the empty root dir removed.

## Success criteria

- `graph/v2_wiki/graph.json` exists, **non-empty** (`nodes > 0`, `edges > 0`); graphify's "Graph is
  empty" error did **not** fire.
- `graph/v2_wiki/GRAPH_REPORT.md` generated with community labels (Step 5) — God Nodes / Surprising
  Connections / Suggested Questions sections present.
- **EXTRACTED-edge spot-check (the point of the enhancement):** at least these authored relations
  appear as edges in `graph.json` (grep the node/edge labels):
  - `P0131` → `STUCK_LEAN`  (o2-logic/07)
  - `VACUUM_LEAK` → `DELTA_TRIM`  (delta-relations/01–02)
  - `TOTAL_TRIM` ↔ `STFT` / `LTFT`  (fuel-trim/01)
  - `control_module_voltage_v` → COMLab electrical pre-check  (ecu-diagnosis/09)
- **No collateral:** `graph/v2_current/` and `graph/v1_baseline/` unchanged (mtime + `git status`);
  no surviving root-level `graphify-out/`.

## Deliverables

1. `graph/v2_wiki/graph.json` — the brand-new wiki KG (GraphRAG-ready).
2. `graph/v2_wiki/GRAPH_REPORT.md` — audit report with labelled communities.
3. `graph/v2_wiki/graph.html` — interactive view.
4. `tasks/progress_notes/T-KG-OBD-1.md` — `## Plan` → `VERIFICATION GATE` → `CODE REVIEW`,
   recording node/edge counts, the EXTRACTED-edge spot-check results, whether `--directed` was used,
   and confirmation that `v2_current/`/`v1_baseline/` were untouched.

## Files to touch

- `graph/v2_wiki/` (new dir — outputs only)
- `tasks/progress_notes/T-KG-OBD-1.md` (new)
- `tasks/PROGRESS.md` (flip this row to `done`)

## Out of scope

No edits to the chunks (the enhancement pass is complete and verified — prep report). No whole-lab
rebuild. No promotion of `v2_wiki` to canonical (separate owner call). No reconciliation of the
logged band/doc follow-ups (O2-FU-2/3, etc.) — they are research-doc items, not KG-build steps. Do
**not** wire any live consumer to `v2_wiki/graph.json` in this task.

## Verification

```bash
cd <repo>/labs/obdlab
# 1. brand-new graph exists and is non-empty
python3 -c "import json; d=json.load(open('graph/v2_wiki/graph.json')); \
  assert len(d['nodes'])>0 and len(d.get('links',d.get('edges',[])))>0, 'empty graph'; \
  print('nodes',len(d['nodes']),'links',len(d.get('links',d.get('edges',[]))))"
# 2. EXTRACTED-edge spot-check — authored relations surfaced as edges
python3 - <<'PY'
import json
d=json.load(open('graph/v2_wiki/graph.json'))
labels={ (n.get('label') or n.get('id') or '').upper() for n in d['nodes'] }
for a,b in [('P0131','STUCK_LEAN'),('VACUUM_LEAK','DELTA_TRIM'),('TOTAL_TRIM','STFT')]:
    print(a, a in labels, '|', b, b in labels)
PY
# 3. old graphs untouched, no stray root graphify-out
git status --porcelain graph/v2_current graph/v1_baseline | grep . && echo "FAIL: old graphs changed" || echo "OK old graphs untouched"
test -d ../../graphify-out && echo "FAIL: root graphify-out exists" || echo "OK no root graphify-out"
```

All steps pass; brand-new wiki KG in `graph/v2_wiki/`, old graphs untouched, no root-level build.

## Progress hook

`tasks/progress_notes/T-KG-OBD-1.md` opens with the confirmed `## Plan` (input = `research/chunks`,
output = `graph/v2_wiki`, `--directed` y/n), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md
row → `done` with node/edge counts and "brand-new wiki KG built from 63 enhanced chunks; EXTRACTED
spot-check green; v2_current/v1_baseline untouched."
