# OBDLab graph — pre-Pass-3 state audit (2026-06-10)

**Scope:** read-only audit of `labs/obdlab/graph/*` to determine the graph's state before deciding
whether to run Pass 3 (the LLM semantic pass). No files were modified.

## Verdict (read this first)

**The graph is healthy. Pass 3 is not needed to fix it, and running it now would only risk adding
noise to a currently-pristine artefact.** The deterministic docs-tier graph is 100% `EXTRACTED`
(every edge traces to explicit text), structurally clean, and its consumer-bearing edges are
well-formed and meaningful. The real open work is *downstream of the graph* — the edges are built but
not yet read by a live code path (the "consumer" in the signal/noise rule). That wiring, not edge
enrichment, is what should come next.

```text
   GRAPH CONTENT          ✅ sound — no defect Pass 3 would repair
   EDGE → CONSUMER WIRING ⚠️ partial — most relation types have no live reader yet
   => fix the wiring, not the graph. Pass 3 stays a CHECKER (DOCGRAPH-2), not a fix.
```

## 1. Tier inventory

OBDLab carries six graph tiers (a "tier" here is one built graph for one corpus slice):

| Tier | nodes | links | what it is |
|---|---:|---:|---|
| `v1_baseline` | 1974 | 2346 | legacy baseline (frozen) |
| `v2_code` | 188 | 492 | code structure (AST pass, offline) |
| `v2_current` | 1245 | 1664 | current code graph |
| `v2_tests` | 878 | 1196 | test map |
| `v2_wiki` | 451 | 494 | prose/wiki tier (9 hyperedges) |
| **`v2_docs`** | **480** | **1045** | **design-docs tier — the one under review** |

## 2. `v2_docs` deep audit (the docs tier built by DOCGRAPH-1)

Built from 68 prepared chunks (~15,673 words), directed, into 19 communities.

**Provenance — fully deterministic:**

```
1045 / 1045 edges = EXTRACTED   (0 INFERRED · 0 AMBIGUOUS · 0 token cost)
```

Every edge is explicit-in-text. This is the auditable-by-construction position: nothing was guessed.

**Integrity — pristine:**

| Check | Result |
|---|---|
| Dangling edges (endpoint not a node) | **0** |
| Isolated nodes (degree 0) | **0** |
| Duplicate `(src, rel, tgt)` edges | **0** |
| Node types | 412 `concept` + 68 `document` (one per chunk) |

**Relation mix (11 types, all meaningful):**

```
 696 MENTIONS   (document → concept — the chunk-to-concept index/backbone)
  93 VERIFIES        ┐
  76 CONSUMES        │
  52 ENUMERATES      │  concept → concept domain edges —
  51 DESCRIBES       │  the architectural/diagnostic signal
  24 GATED_BY        │
  16 SUPERSEDES      │
  15 DERIVED_FROM    │
  10 ROUTES_TO       │
   9 MIRRORS_CONTRACT_IN
   3 OWNED_BY        ┘
```

`MENTIONS` (67% of edges) is the `document → concept` provenance layer — not noise, but also not the
diagnostic signal. The **349 concept→concept edges** are the substance, and they are genuinely good.

## 3. Consumer-bearing edges — are they real?

Yes. Sampled and confirmed well-formed:

- **`CONSUMES` (76)** — names which analytics consumer reads which field. Top sources:
  `COMLab` (8) plus specific COMLab tasks (`T-COMV2-MAF-LIN-1`, `T-COMV2-VE-GATE-1`, …),
  `VEEngine.compute_ve` (6), `O2Normalizer.normalize` (5), `AnalyticsPreconditions.evaluate` (5),
  `PIDIngestionValidator` (5), `fault_atlas_router` (1). Targets are real fields:
  `normalized_obd_lambda`, `OBDLivePayload`, `total_trim_correction_delta`, `freeze_frame_pids`.
  This *is* the signal/noise backbone, already encoded.
- **`GATED_BY` (24)** — real bounds/gates: `shrtft1 GATED_BY [-127,127]`, `thermal freeze GATED_BY
  ECT < 75`, `PIDValidationError GATED_BY engine_rpm > rated_rpm × 1.05`.
- **`ROUTES_TO` (10)** — pipeline-step routing: `compute_bucket → step[2]`, `VEEngine.compute_ve →
  step[4]`, `O2Normalizer.normalize → step[5]`.

There is no structural reason to run Pass 3 over this content. An LLM re-reading the same prose would,
at best, reproduce these `EXTRACTED` edges (CONFIRMED) and, at worst, add `INFERRED` edges that this
clean 0%-inferred graph currently doesn't carry.

## 4. The real gap — edges are built but not yet *consumed*

Under the signal/noise rule, an edge earns its place only if a **named consumer reads it in a live
code path**. Here the graph's *content* satisfies the first half (named consumers are encoded as edge
sources) but the *wiring* — code that actually traverses these edges — is mostly not in place yet:

- **`build_lab_vault.py`** (a "consumer" named in DOCGRAPH-1) requires `graph.json` to **exist** as an
  eligibility gate, but **does not traverse its edges**. Its signal/noise enforcement runs on note
  **frontmatter** (the YAML `consumers:` field at the top of each note), not on graph `CONSUMES` edges.
- **`consumers.base`** (the audit view) likewise audits the note `consumers:` property, not graph edges.
- **`/check-impact` and `/graph-find`** — the commands that *would* read graph relations — appear only
  in `VAULT_IMPLEMENTATION_PLAN.md` and the frontmatter-schema reference as **planned**, not as
  implemented command code. No command files exist for them yet.
- Per-relation reader check: only `CONSUMES` is referenced by a consumer file at all; `GATED_BY`,
  `ROUTES_TO`, `VERIFIES`, `SUPERSEDES`, `MIRRORS_CONTRACT_IN` have **zero** live readers today.

So the docs graph is currently a **navigation + build-eligibility artefact**, not yet an edge-level
input to analytics. That is fine as a stage — but it means enriching it further (Pass 3) is premature:
you'd be improving recall on edges nothing reads yet.

## 5. Wiring flags (for follow-up, not fixed here)

1. **Path mismatch.** `build_lab_vault.py` reads `labs/obdlab/graphify-out/graph.json`, but the
   canonical docs graph was relocated to `labs/obdlab/graph/v2_docs/graph.json`. An older
   `graphify-out/graph.json` (mtime **2026-06-09**, i.e. *before* the 2026-06-10 docs build) is present
   at the path the consumer points at — and read inconsistently in this audit (one check found it, a
   second failed to open it). The vault build may be gated on a **stale graph at the wrong path**.
2. **Stale ledger (carried from DOCGRAPH-1).** That task's header still says `Status: pending` while
   its progress note shows the verification gate completed. Reconcile before building on top of it.
3. **Version drift.** DOCGRAPH-1's note records the runner on `graphifyy 0.8.36`; `.venv-wired` shows
   `0.8.35`. Pin which environment actually runs before spending tokens.

## 6. Recommended order of operations

1. **Hold Pass 3 (DOCGRAPH-2).** The cross-check spec is authored and correct, but it is most valuable
   *after* a consumer reads the edges — otherwise CONFIRMED/GAP/NOISE has no downstream meaning.
2. **Close the consumer wiring first** — implement (or stub) the edge-reading path
   (`/check-impact` / `/graph-find`, or have `build_lab_vault.py` actually traverse `CONSUMES`), and fix
   the `graphify-out` → `graph/v2_docs` path mismatch so the consumer reads the current graph.
3. **Then run DOCGRAPH-2 as a checker** to prove the deterministic edges are complete for the now-live
   consumer — exactly the noise-controlled flow already specced.

**Bottom line:** the graph is in good shape. The blocker to "moving on" is not graph quality and not
Pass 3 — it is that nothing reads the edges yet. Wire the consumer, then let Pass 3 verify, not enrich.
