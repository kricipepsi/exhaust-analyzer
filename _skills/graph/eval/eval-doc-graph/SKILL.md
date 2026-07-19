---
name: eval-doc-graph
description: >
  Evaluate a Pass-3 (LLM) DOCUMENT graph against the deterministic baseline as a
  checker, not an adder. Use this whenever you need to judge whether graphify's
  Pass 3 over a docs tier (ADRs, HLD/DLD, BDD, task specs — e.g. obdlab
  graph/v2_docs) ADDED genuine missing edges or just NOISE. Trigger on
  "evaluate pass 3", "pass-3 cross-check", "does the third pass help the docs
  graph", "classify the LLM doc edges", "v2_docs_llm diff", or any request to
  decide if an LLM document-graph pass is beneficial vs noisy. Promotes nothing;
  produces a CONFIRMED/GAP/NOISE report.
allowed-tools: Read, Grep, Glob, Bash
---

# eval-doc-graph — Pass-3 cross-check for the document graph

## What this is for

graphify builds every 4DLab graph from **deterministic** sources (the chunks'
explicit relation blocks). Pass 3 lets an LLM re-read the same prose and propose
edges. That can *break* the auditable-by-construction position by adding
plausible-but-unsourced edges. So Pass 3 is run **as a checker, not an adder**:
it answers one question — *reading the same prose, does the model find an
EXTRACTED edge, between two existing nodes, with a named consumer, that the
hand-authored relation blocks missed?* — and everything else is noise.

This skill grades that question for a **document** graph. It never writes an edge
into any graph. (Schema/consumer rule, glossed for the owner: a "consumer" is the
later code that actually reads an edge; an edge with no reader is noise.)

## Inputs

Two graphify node-link files (`graph.json`):

- **baseline** — the canonical deterministic graph, e.g.
  `labs/obdlab/graph/v2_docs/graph.json` (byte-unchanged; this skill only reads it).
- **llm** — the Pass-3 scratch graph, e.g. `labs/obdlab/graph/v2_docs_llm/graph.json`,
  produced by `4dlab-graphify-run` with `--backend deepseek` in **default mode**
  (never `--deep` — deep mode manufactures the INFERRED edges we are trying to filter).

If the `llm` graph does not exist yet, this skill cannot run — producing it is the
`4dlab-graphify-run` step (task `T-VAULT-DOCGRAPH-2`), not this skill.

## How to run it

```bash
python scripts/eval_doc_graph.py \
  <baseline>/graph.json <llm>/graph.json \
  --out <baseline_dir>/PASS3_CROSSCHECK.md
```

The script does the **objective** half and writes the report skeleton:

- edge set-math (CONFIRMED = already in baseline; BASELINE_ONLY = LLM missed it),
- confidence gating (anything not `EXTRACTED` → `NOISE_inferred`),
- node gating (invents a node → `NOISE_new_node`),
- relation gating (`MENTIONS`/`DESCRIBES` → `NOISE_generic_rel`; signal relations
  `CONSUMES/GATED_BY/ROUTES_TO/VERIFIES/ENUMERATES/DERIVED_FROM/...` → `CANDIDATE_GAP`),
- a health delta (nodes, edges, density, dangling, isolated, confidence split).

## Your job after the script (the judgment half)

The script **cannot** decide whether a `CANDIDATE_GAP` has a real consumer — that
is the signal/noise call only you can make. For each `CANDIDATE_GAP` row:

1. Name the **existing** consumer in **COMLab analytics / fault-atlas routing**
   and the code path that would read this edge. If you can name one, it is a real
   **GAP** → route it through `4dlab-doc-prep` (make the relation explicit in the
   owning chunk, then re-run the deterministic pass). If you can name a consumer
   that does not exist yet, record it as a **proposal** in
   `comlab/config/proposals/` — never silently in the live graph.
2. If you cannot name any consumer, **demote the row to NOISE.** "Future use" is
   not a consumer.

Promote nothing into the baseline `graph.json`. The whole point is that no
LLM-inferred edge ever enters a canonical graph.

## What "beneficial vs noise" means here (the verdict)

State the verdict plainly using the counts:

- **Beneficial** if there is ≥1 real GAP (EXTRACTED, both nodes exist, named
  consumer) the deterministic pass missed — Pass 3 earned its keep on this run.
- **Pure noise** if every new edge is NOISE and every signal edge was already
  CONFIRMED — Pass 3 only re-derived what the deterministic pass already had.
  That is the *expected, healthy* result for a mature graph; report it as
  confirmation of completeness, not as a failure.

A high INFERRED share in the LLM graph is normal and is precisely what the gate
removes. Report it; do not act on it.

## Hard guardrails

- Read-only on every canonical graph; the only file you create is the report
  (and any `proposals/` entry the agent adds by hand).
- Never run `--deep`. Never re-run extraction on `v2_wiki/v2_code/v2_tests`
  (CLAUDE.md HARD RULE — those are canonical).
- A GAP is only real if its consumer is read in a **live** code path. An edge
  defined but read nowhere is an orphan and a signal/noise breach.
