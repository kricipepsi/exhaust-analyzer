# T-KG-OBD-1 — Graphify ingest of the enhanced OBDLab wiki → brand-new KG

**Date:** 2026-06-09 · **Mode:** STRICT · **Lane:** KG (the one permitted graphify exception,
`OBDLAB_TASKS_START_HERE.md` §0; Deliverables name `graph.json`).

## Plan

- **Input:** `research/chunks/` — 63 enhanced `.md` (7 topic dirs), 32,889 words, 0 code files.
  Enhancement pass pre-verified in `research/CHUNK_ENHANCEMENT_PREP_REPORT.md` (314 explicit
  relations + per-chunk Core Entities, byte-identical labels).
- **Output:** `graph/v2_wiki/` (spec-recommended name, owner-confirmed this session).
- **`--directed`: YES** (owner-confirmed) — `build_from_json(extraction, directed=True)`;
  `graph.json` has `"directed": true`. The existing lab graphs stay undirected; this one preserves
  the authored `source → target` arrows.
- **Pipeline:** graphify skill (graphifyy in `.venv-wired`, Python 3.14.5), run from the **lab
  root** on Windows PowerShell — never from the repo root. Doc-only corpus → AST step is an empty
  fast-path; semantic extraction via 3 parallel `general-purpose` subagents (~21 files each).
- **Consumer (signal/noise):** KG artefact, not a schema field — named consumer is the architect's
  KG-query / fault-atlas-design workflow (same role `graph/v2_current/graph.json` plays).
- Inner loop (ruff/pyright/pytest) N/A — zero Python source files changed.

## VERIFICATION GATE

**1. Brand-new graph exists, non-empty — PASS**

```
nodes 451  links 494  hyperedges 9  directed: true  communities 62
```

`GRAPH_REPORT.md` generated with labelled communities; **God Nodes / Surprising Connections /
Suggested Questions** sections all present. `graph.html` written (451 nodes < 5,000 viz cap).

**2. EXTRACTED-edge spot-check (the point of the enhancement) — PASS 5/5**

| Authored relation | Found in graph.json | Tag |
|---|---|---|
| `P0131` → `STUCK_LEAN` | `P0131 --indicates--> STUCK_LEAN` | EXTRACTED 1.0 |
| `VACUUM_LEAK` → `DELTA_TRIM` | `VACUUM_LEAK --produces_negative--> DELTA_TRIM` | EXTRACTED 1.0 |
| `TOTAL_TRIM` ↔ `STFT` | `TOTAL_TRIM --equals--> STFT` | EXTRACTED 1.0 |
| `TOTAL_TRIM` ↔ `LTFT` | `TOTAL_TRIM --equals--> LTFT` | EXTRACTED 1.0 |
| `control_module_voltage_v` → COMLab electrical pre-check | `control_module_voltage_v --consumed_by--> COMLab electrical-health pre-check` | EXTRACTED 1.0 |

**3. Graph health (4dlab-graph `health` semantics, run on `graph/v2_wiki/graph.json`)**

- Confidence distribution: **408 EXTRACTED / 84 INFERRED / 2 AMBIGUOUS** — the enhancement did its
  job (82.6 % of edges are first-class EXTRACTED; the prior whole-lab graph carried these links as
  INFERRED or missed them).
- Relation types are domain-specific: `indicates` 54, `consumed_by` 47, `raises` 21, `maps_to` 17,
  `produces` 15, `emits` 13, `routes_to` 8, `suppresses` 8 … Generic fallback relations between
  domain nodes: **1** (`COMLab delta engine --semantically_similar_to--> COMLab delta-calculation
  script` — a borderline alias pair, logged, not a failure threshold breach).
- God nodes (top): `LTFT` 26, `TOTAL_TRIM` 17, `lambda_chem` 16, `ECU_HARDWARE_CHECKER` 16,
  `fuel_trim_invalid` 11 — all expected domain hubs, no pathological hub.
- Isolated nodes (excl. hyperedge members): **15** — 11 per-file document stub nodes (chunk-2
  subagent created doc nodes per file; entities link to each other rather than to the doc node),
  3 open-loop `FuelSystemStatus.*` enum values, and `P0442`. All are leaf/documentary, none is a
  lost domain relation; acceptable for a wiki KG (4dlab-graph flags >10 *non-leaf* isolates —
  these are leaves/doc stubs).

**4. No collateral — PASS**

- `git status --porcelain graph/v2_current graph/v1_baseline` → empty (untouched).
- mtime/file-count snapshot before vs after: `graph/v2_current` 64 files, `graph/v1_baseline`
  140 files — counts and newest LastWriteTime **identical**.
- No lab-root `graphify-out/` survives (relocated to `graph/v2_wiki/`, dir removed); no
  `research/chunks/graphify-out/` created.
- ⚠ **Pre-existing** root `graphify-out/` dirs at `4DLab/` (5,998 files) and `4DLabV2/`
  (2,119 files) — the logged PURGE-1/2 incident artefacts — were already on disk **before** this
  task (baseline snapshot 2026-06-08) and are byte-count/mtime **unchanged** after it. Left
  untouched per the workspace git rule (never touch pre-existing uncommitted changes); they remain
  excluded from commits.
- Fresh build: lab `graphify-out/` did not exist at session start → no stale whole-lab semantic
  cache could bleed in; the new cache lives under `graph/v2_wiki/cache/`.

**Gate verdict: PASS** — brand-new directed wiki KG in `graph/v2_wiki/`, old graphs untouched.

## CODE REVIEW

- **No source code changed.** Deliverables are KG artefacts + this note + the ledger row. Scope
  honored: no chunk edits, no whole-lab rebuild, no consumer wiring, no promotion to canonical.
- **Pipeline fidelity:** graphify skill steps 1–9 followed (detect → cache check → 3 parallel
  subagent extraction → merge/dedup → directed build → cluster → 62 labelled communities → HTML →
  benchmark → manifest/cost). Token benchmark: ~666 tokens avg query vs ~43.9k naive corpus read
  (65.8× reduction). Recorded cost: 2,163,281 subagent tokens (combined in+out, logged as output
  in `cost.json`).
- **Subagent incident (recovered):** first dispatch — chunks 2 and 3 exhausted context before
  writing their JSON (chunk 1 landed). Re-dispatched both with incremental-write instructions;
  both landed valid JSON (188 n / 176 e and 186 n / 200 e). No partial/corrupt data merged —
  merge step asserts non-empty valid JSON per chunk.
- **Known minor blemishes (logged, not blockers):** 1 `semantically_similar_to` edge between two
  COMLab-alias nodes; 11 isolated per-file doc-stub nodes from chunk 2's id scheme; 3 isolated
  open-loop enum leaves + `P0442`. None affects the EXTRACTED diagnostic spine. A future
  KG-lane pass may dedupe doc stubs; out of scope here.
- **Honesty rules held:** the O2-FU-2 non-edge (`SUPPRESS_POST_CAT_TRIM` IS_NOT a
  `TrimAnalyticsGate` value) was **not** asserted as an edge (subagents instructed; chunk-3 agent
  confirmed skip).
