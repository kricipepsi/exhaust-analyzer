---
name: eval-code-graph
description: >
  Evaluate a Pass-3 (LLM) CODE graph against the deterministic AST baseline as a
  checker, not an adder. Use this whenever you need to judge whether graphify's
  Pass 3 over a code tier (AST-derived symbol graph: classes, methods, calls,
  imports — e.g. obdlab graph/v2_code) ADDED genuine missing edges or just NOISE.
  Trigger on "evaluate pass 3 on the code graph", "code pass-3 cross-check",
  "does the third pass help the code graph", "classify the LLM code edges",
  "v2_code_llm diff", or any request to decide if an LLM code-graph pass is
  beneficial vs noisy. Promotes nothing; produces a CONFIRMED/GAP/NOISE report.
allowed-tools: Read, Grep, Glob, Bash
---

# eval-code-graph — Pass-3 cross-check for the code graph

## What this is for, and why the bar is highest here

The code graph is built from the **AST** — `calls`, `contains`, `inherits`,
`method`, `uses`, `references` are ground truth read straight off the parse tree,
not interpreted from prose. Two consequences make Pass 3 risky on code:

1. **The AST is already authoritative**, so an LLM "finding" a structural edge the
   AST missed is usually a hallucination, not a discovery.
2. **The baseline is already ~50% INFERRED**, so a Pass-3 graph mostly inflates that
   share — exactly the noise the gate rejects.

So expect Pass 3 on the code graph to be **almost entirely NOISE**, and treat any
EXTRACTED-but-new structural edge as a *candidate AST blind spot* to validate
against the source, not an automatic gap. This skill grades that and writes
nothing into any graph. (Owner gloss: AST = the structure a parser reads directly
from the code; a "consumer" is the later code that actually reads a graph edge.)

## Inputs

- **baseline** — canonical AST graph, e.g. `labs/obdlab/graph/v2_code/graph.json`.
- **llm** — Pass-3 scratch graph, e.g. `labs/obdlab/graph/v2_code_llm/graph.json`,
  from `4dlab-graphify-run --backend deepseek` in **default mode** (never `--deep`).

**Precondition — read before running.** The code tier has no `ingest_ready/`
staging dir today, and CLAUDE.md forbids re-running `v2_code` extraction unless
explicitly instructed. The **llm** graph therefore does not exist yet and cannot
be produced without an owner-instructed graphify run on the code sources. This
skill grades that graph once it exists; it does not create it. See
`PASS3_EVAL_PROTOCOL.md` for the precondition gate.

## How to run it

```bash
python scripts/eval_code_graph.py \
  <baseline>/graph.json <llm>/graph.json \
  --out <baseline_dir>/PASS3_CROSSCHECK.md
```

Objective half done by the script: set-math (CONFIRMED / BASELINE_ONLY),
confidence gating (not `EXTRACTED` → `NOISE_inferred`, the dominant class here),
node gating (`NOISE_new_node`), structural-relation gating (new EXTRACTED
structural edge → `CANDIDATE_GAP` = candidate AST blind spot), and a health delta.

## Your job after the script (the judgment half)

For each `CANDIDATE_GAP`:

1. **Open the source and confirm it is a real AST blind spot** — a relation the
   static parse genuinely cannot see (dynamic dispatch, `getattr`/reflection,
   a runtime-registered call/plugin). If the AST simply *should* have caught it,
   the LLM edge is suspect → **NOISE**.
2. **Name the consumer** that reads it — graph navigation, a drift-guard, or the
   design→code→test spine (**not** COMLab analytics; code edges are structural).
   No consumer ⇒ NOISE.

A genuine AST blind spot is fixed in the **extractor / AST config**, never patched
into `graph.json`. Promote nothing.

## What "beneficial vs noise" means here (the verdict)

- **Beneficial** only if ≥1 CANDIDATE_GAP is confirmed as a true AST blind spot
  with a named consumer — rare, and worth a fix to the extractor rather than the graph.
- **Pure noise** (the expected result) if every new edge is NOISE and every
  structural edge was already CONFIRMED — Pass 3 re-derived the AST and added
  inference. Report it as confirmation the AST graph is complete.

## Hard guardrails

- Read-only on every canonical graph; only output is the report.
- Never `--deep`. Never re-run `v2_code/v2_wiki/v2_tests` extraction without
  explicit owner instruction (CLAUDE.md HARD RULE).
- A GAP is real only if it is both a true AST blind spot AND read in a live code path.
