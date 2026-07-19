# PASS-3 cross-check — document graph (checker, not adder)

**Task:** T-VAULT-DOCGRAPH-2 · **Lane:** graph-tooling · **Run date:** 2026-06-10
**Verdict:** **0 real GAPs.** All 6 candidate edges already exist in the baseline under a proper signal
relation, same chunk anchor — the LLM merely restated them in generic vocabulary. Nothing is routed to
`4dlab-doc-prep`; nothing is written into the canonical graph.

- Baseline (deterministic, DOCGRAPH-1): `graph/v2_docs/graph.json` — 480 nodes, **1045 edges**, 100% EXTRACTED
- LLM Pass-3 (deepseek-v4-pro, default mode): `graph/v2_docs_llm/graph.json` — 111 nodes, **84 edges**
- Exact run command (default mode, **NO `--deep`**):
  `graphify.exe extract graph\v2_docs\ingest_ready --backend deepseek --out .` with `GRAPHIFY_DEEPSEEK_MODEL=deepseek-v4-pro`
- Cost: 44,720 in / 62,621 out tokens, **est. $0.0238**, 22 min wall.
- Consumer anchor for a real GAP: **COMLab analytics / fault-atlas routing**

---

## ⚠️ Methodology note — read before the counts (why CONFIRMED = 0 is NOT a defect)

The objective differ (`eval_doc_graph.py`) matches edges on the exact tuple `(source_id, target_id, relation)`.
That match is **near-vacuous on this run** because the two graphs were built by different extractors that do
not share a namespace:

| | Baseline (deterministic prep) | LLM Pass-3 (graphify default) |
|---|---|---|
| **Relation vocabulary** | `CONSUMES, GATED_BY, ROUTES_TO, VERIFIES, ENUMERATES, DERIVED_FROM, MIRRORS_CONTRACT_IN, SUPERSEDES, OWNED_BY, MENTIONS, DESCRIBES` | `references(53), calls(14), implements(9), conceptually_related_to(7), semantically_similar_to(1)` |
| **Relation-name overlap with baseline** | — | **0** (none) |
| **Node-id overlap** | 480 ids | only **24 of 111** ids also in baseline |
| **Edges using a baseline SIGNAL relation** | 1045 | **0** |

Because the LLM never emits an edge in the baseline's controlled diagnostic vocabulary, **no LLM edge can
tuple-match a baseline edge** → `CONFIRMED = 0` and `BASELINE_ONLY = 1045` are *artifacts of vocabulary
divergence*, not evidence the baseline is incomplete. The meaningful check is therefore done **by hand
below**: for each LLM "signal-ish" edge, does the baseline already carry the same relationship (same source
chunk + line) under a controlled relation? The answer for all 6 is **yes**.

This is exactly the noise Step 5 anticipates: an LLM reading prose produces generic adjacency
(`references`/`implements` ≈ `MENTIONS`), and the gate's job is to confirm none of it is a missed
*diagnostic* edge with a consumer.

### Coverage cap (no silent truncation)

The LLM graph references **57 of the 68** ingest_ready chunks; **38 baseline chunks have no edge in the LLM
graph** — they were either skipped on invalid/truncated JSON (deepseek-v4-pro hit the 16k output cap on the
single 68-file mega-chunk and graphify split it 34/34; some halves still failed to parse) or yielded no
edges. Skipped families include most of `ADR_*`, `BDD_Feature_*`, `DLD_*`, and `PRD_Section_*`. **This makes
the LLM run a sparse, conservative probe — it can surface a missed edge but cannot prove completeness by
absence.** Completeness evidence for the baseline comes from DOCGRAPH-1's deterministic 100%-EXTRACTED build,
not from this run.

---

## Classification of every LLM edge (84 total)

| Class | Count | Meaning / action |
|---|---|---|
| CONFIRMED | 0 | tuple-present in baseline — vacuous here (disjoint vocab, see note) |
| CANDIDATE_GAP (known signal rel) | 0 | none — the LLM emitted no edge in the baseline signal vocabulary |
| CANDIDATE_GAP_unknown_rel | 6 | generic-vocab edges (`references`/`implements`) flagged for inspection — **all 6 demoted to NOISE below** |
| NOISE_inferred | 3 | confidence != EXTRACTED — rejected |
| NOISE_new_node | 75 | an endpoint is an LLM-invented node absent from baseline — rejected |
| NOISE_generic_rel | 0 | (LLM's generic relations aren't in the doc differ's MENTIONS/DESCRIBES set, so they fell to unknown_rel instead) |
| BASELINE_ONLY | 1045 | in baseline, LLM did not find — informational (vocab artifact, see note) |

**Result: 0 real GAPs · 84 NOISE (78 by the differ + 6 demoted by agent judgment below) · 0 promotions.**

LLM-graph confidence split: **EXTRACTED 81 / INFERRED 3 / AMBIGUOUS 0.** A nonzero INFERRED share is expected
and is precisely what the gate discards — reported, not acted on.

---

## Candidate-GAP adjudication (the 6 `unknown_rel` rows) — all demote to NOISE

Each LLM candidate is a generic-vocabulary echo of a relationship the **baseline already carries under a
signal relation, anchored to the same chunk line**. Per the Step-5 gate and the anti-orphan rule, an edge
already present in the baseline is **CONFIRMED-equivalent, not a GAP** — there is nothing to route to
`4dlab-doc-prep`.

| LLM candidate (src → tgt, rel, anchor) | Already in baseline? | Baseline edge (signal rel, same anchor) | Disposition |
|---|---|---|---|
| `comlab_fault_atlas_router → obdlivepayload` · references · HLD/1_Responsibility.md | **Yes** | `COMLab fault_atlas_router → OBDLivePayload` **CONSUMES** @L25 | **NOISE** (already covered) |
| `comlab_t_comv2_ecu_fuse_1 → lambda_perception_delta` · references · LLD/13_…Guard.md | **Yes** | `COMLab T-COMV2-ECU-FUSE-1 → lambda_perception_delta` **CONSUMES** @L23 | **NOISE** (already covered) |
| `freeze_frame_pids → comlab` · references · LLD/14_…Forwarding_Contract.md | **Yes** | `COMLab → freeze_frame_pids` **CONSUMES** @L12 | **NOISE** (already covered) |
| `maf_linearity_helpers → comlab_t_comv2_maf_lin_1` · references · LLD/11_MAF_Linearity.md | **Yes** | `COMLab T-COMV2-MAF-LIN-1 → w_theo / sensor_error_delta` **CONSUMES** @L26 | **NOISE** (already covered) |
| `obdlivepayload → comlab` · implements · HLD/7_COMLab_Integration_Points.md | **Yes** | `OBDLivePayload → COMLab frozen contract surface` **MIRRORS_CONTRACT_IN** @L48 | **NOISE** (already covered) |
| `anti_orphan_s4 → obdlivepayload` · references · HLD/9_Known_Gaps_…md | **Yes (as documented gap)** | `Anti-orphan (S4) → forward-registered fields without live COMLab reader` **DESCRIBES** @L16 | **NOISE** (prose adjacency; the chunk explicitly documents these as *forward-registered without a live reader* — i.e. deliberately not a live consumer, so even as a relation it is anti-orphan-excluded) |

**No proposals recorded** in `comlab/config/proposals/`: none of the 6 names a *new* diagnostic relationship
with a nameable live consumer that the baseline lacks — each is a vocabulary restatement of an existing
baseline edge, so there is nothing to propose. The last row (`anti_orphan_s4`) is the textbook anti-orphan
case: the source chunk itself flags those fields as having **no live COMLab reader**, so promoting the edge
would manufacture an orphan — correctly dropped.

---

## Health delta (baseline → LLM)

| metric | baseline | LLM Pass-3 |
|---|---|---|
| nodes | 480 | 111 |
| links | 1045 | 84 |
| density | 0.0045 | 0.0069 |
| dangling | 0 | 0 |
| isolated | 0 | 11 |
| confidence split | EXTRACTED 1045 | EXTRACTED 81 / INFERRED 3 |
| chunks covered | 68 / 68 | 57 / 68 |

> A high INFERRED/sparse share in the LLM graph is expected and is exactly what the gate filters out —
> reported, not acted on. The 11 isolated LLM nodes are scratch-graph artifacts and do not affect the canonical graph.

---

## Bottom line

Pass 3 surfaced **zero EXTRACTED signal edges, between two existing nodes, with a named consumer, that the
deterministic pass missed.** Every candidate was an existing baseline relationship re-expressed in generic
graph vocabulary. The deterministic docs graph stands unmodified; the auditable-by-construction position
(no LLM-inferred edge has entered any 4DLab graph) is preserved. The LLM graph remains a scratch comparison
artefact in `graph/v2_docs_llm/`.
