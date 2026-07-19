---
name: eval-wiki-graph
description: >
  Evaluate a Pass-3 (LLM) WIKI graph against the deterministic baseline as a
  checker, not an adder. Use this whenever you need to judge whether graphify's
  Pass 3 over a wiki tier (the curated diagnostic-knowledge graph: fault/enum/flag
  nodes and diagnostic relations — e.g. obdlab graph/v2_wiki) ADDED genuine
  missing edges or just NOISE. Trigger on "evaluate pass 3 on the wiki graph",
  "wiki pass-3 cross-check", "does the third pass help the wiki graph",
  "classify the LLM wiki edges", "v2_wiki_llm diff", or any request to decide if
  an LLM wiki-graph pass is beneficial vs noisy. Promotes nothing; produces a
  CONFIRMED/GAP/NOISE report.
allowed-tools: Read, Grep, Glob, Bash
---

# eval-wiki-graph — Pass-3 cross-check for the wiki graph

## What this is for

The wiki graph is the **curated diagnostic-knowledge graph** — fault, enum and
flag nodes wired by diagnostic relations (`indicates`, `consumed_by`, `maps_to`,
`routes_to`, `produces`, `raises`, …). It carries the real signal/noise backbone,
so its baseline is built deterministically from the chunks' explicit relation
blocks. Pass 3 lets an LLM re-read the wiki prose and propose edges; that can add
plausible-but-unsourced links. This skill grades Pass 3 **as a checker, not an
adder** and writes nothing into any graph.

(Owner gloss: a "consumer" is the later code that actually reads an edge. An edge
no code reads is noise, however plausible it looks.)

## Inputs

- **baseline** — canonical deterministic graph, e.g. `labs/obdlab/graph/v2_wiki/graph.json`.
- **llm** — Pass-3 scratch graph, e.g. `labs/obdlab/graph/v2_wiki_llm/graph.json`,
  from `4dlab-graphify-run --backend deepseek` in **default mode** (never `--deep`).

**Precondition — read before running.** Unlike the docs tier, the wiki tier has no
`ingest_ready/` staging dir today, and CLAUDE.md forbids re-running `v2_wiki`
extraction unless explicitly instructed. So the **llm** graph does not exist yet
and cannot be produced without an owner-instructed graphify run on the wiki
sources. This skill grades that graph once it exists; it does not create it. See
`PASS3_EVAL_PROTOCOL.md` for the precondition gate.

## How to run it

```bash
python scripts/eval_wiki_graph.py \
  <baseline>/graph.json <llm>/graph.json \
  --out <baseline_dir>/PASS3_CROSSCHECK.md
```

Objective half done by the script:

- set-math (CONFIRMED already in baseline; BASELINE_ONLY = LLM missed it),
- confidence gating (not `EXTRACTED`, i.e. INFERRED **or** AMBIGUOUS → `NOISE_inferred`),
- node gating (invents a node → `NOISE_new_node`),
- relation gating (organizational `documents`/`member_of`/`has_value` → `NOISE_generic_rel`;
  diagnostic relations → `CANDIDATE_GAP`),
- health delta, with `isolated`-node tracking (the wiki baseline carries fault/enum
  stubs that are not yet wired).

## Your job after the script (the judgment half)

For each `CANDIDATE_GAP`, name the **existing** consumer in **COMLab analytics /
fault-atlas routing** and the code path that reads it. Scrutinise first any
candidate that wires a previously **isolated** fault/enum node with an EXTRACTED
diagnostic edge — that is where a real missing relation is most likely.

- Consumer nameable and live → real **GAP** → route through `4dlab-doc-prep`
  (make the relation explicit in the wiki chunk, re-run the deterministic pass).
- Consumer would be new → record as a **proposal** in `comlab/config/proposals/`.
- No consumer → **demote to NOISE.** "Future use" is not a consumer.

Promote nothing into the baseline graph.

## What "beneficial vs noise" means here (the verdict)

- **Beneficial** if ≥1 real GAP (EXTRACTED diagnostic edge, both nodes exist,
  named consumer) the deterministic pass missed.
- **Pure noise** if every new edge is NOISE and every diagnostic edge was already
  CONFIRMED — the expected, healthy result for a mature wiki; report it as
  confirmation of completeness.

## Hard guardrails

- Read-only on every canonical graph; only output is the report (+ any hand-added
  `proposals/` entry).
- Never `--deep`. Never re-run `v2_wiki/v2_code/v2_tests` extraction without
  explicit owner instruction (CLAUDE.md HARD RULE).
- A GAP is real only if its consumer is read in a **live** code path.
