---
node_type: task
task_id: T-VAULT-WIKIGRAPH-1
status: pending
pack: VAULT · **Mode:** GRAPH-TOOLING lane
lab: obdlab
mode: graph-tooling lane
blocked_by:
- T-VAULT-DOCGRAPH-2
consumers:
- graph/v2_wiki — wiki graph
- COMLab analytics / fault-atlas routing
- design→code→test spine (.base views)
implements:
- graph/v2_wiki/graph.json
- graph/v2_wiki_llm/graph.json
- graph/v2_wiki/PASS3_CROSSCHECK.md
tags:
- task
- vault
- obdlab
---

# T-VAULT-WIKIGRAPH-1 — Pass-3 LLM **cross-check** of the deterministic wiki graph (checker, not adder)

**Status:** `pending` · **Pack:** VAULT · **Mode:** GRAPH-TOOLING lane (graphify run — no lab inner-loop/gate)
**Origin:** Owner request 2026-06-10 — extend the DOCGRAPH-2 Pass-3 checker to the **wiki** tier (`graph/v2_wiki/`).
**Blocked by:**
1. **T-VAULT-DOCGRAPH-2** — run the docs cross-check first. It is the cheapest, cleanest test (100% EXTRACTED
   baseline) and proves out the runner. Only pursue the wiki tier if the docs run shows Pass 3 can find a real GAP.
2. **Explicit owner instruction to re-extract `v2_wiki`.** `graph/v2_wiki/graph.json` is a **canonical** graph;
   CLAUDE.md forbids re-running its extraction without an explicit instruction. Producing the LLM graph below **is**
   a re-extraction of the wiki source, so this task does not start until the owner says go.

**Consumer (signal/noise):** Adds no schema field and writes no edge into the canonical graph. Deliverable is a
**diff report** (`graph/v2_wiki/PASS3_CROSSCHECK.md`). A confirmed gap feeds the existing consumers — **COMLab
analytics / fault-atlas routing** via the vault-build frontmatter + the design→code→test `.base` views — **only
after** it is made explicit in the wiki chunk and the deterministic pass re-run (via `4dlab-wiki-prep`); it is never
patched into `graph.json` from the LLM graph.

### Pre-step (runnable now, no extraction, no tokens) ###

Confirm the wiki baseline is in good condition before spending anything:

```bash
python _skills/graph/eval/eval-wiki-graph/scripts/eval_wiki_graph.py \
  labs/obdlab/graph/v2_wiki/graph.json
```

Expect **Condition: GOOD** (0 dangling; the ~22 isolated fault/enum stubs are expected for the wiki tier). If it
reports dangling edges, stop and surface that — the baseline itself needs attention before any Pass-3 work.

### Goal (gated half) ###

Run graphify Pass 3 over the wiki source `labs/obdlab/research/chunks/` with `--backend deepseek` in **default mode**
(NOT `--deep`), relocate the result to a **separate scratch dir** `graph/v2_wiki_llm/`, then classify with the skill:

```bash
python _skills/graph/eval/eval-wiki-graph/scripts/eval_wiki_graph.py \
  labs/obdlab/graph/v2_wiki/graph.json \
  labs/obdlab/graph/v2_wiki_llm/graph.json \
  --out labs/obdlab/graph/v2_wiki/PASS3_CROSSCHECK.md
```

For each `CANDIDATE_GAP`, name the existing COMLab/fault-atlas consumer + the wiki-chunk anchor, or demote to NOISE.
Scrutinise first any candidate that wires a previously **isolated** fault/enum node. Promote nothing into the
canonical graph; route a real GAP to `4dlab-wiki-prep`.

> **Note on the wiki source.** Unlike the docs tier, the wiki tier is pre-chunked — Pass 3 runs directly on
> `research/chunks/` (no `ingest_ready/` step). `research/chunks/` is graph-canonical at its source; do not move or
> rename it. Running Pass 3 reads it but must not edit it.

### Success criteria ###

1. **Separate-dir guard.** Pass-3 output lands in `graph/v2_wiki_llm/`; canonical `graph/v2_wiki/graph.json` is
   byte-unchanged (`git status --porcelain` + mtime); no surviving root `graphify-out/`.
2. **Default mode confirmed.** Run used `--backend deepseek` and **no** `--deep` (record the exact command).
3. **Report exists** — `graph/v2_wiki/PASS3_CROSSCHECK.md` — classifying every LLM edge as exactly one of
   CONFIRMED / CANDIDATE_GAP / NOISE, with counts (signal set: `consumed_by/indicates/maps_to/routes_to/produces/
   produces_negative/raises/emits/requires/suppresses/refines/triggers`; generic→NOISE: `documents/member_of/has_value`).
4. **Every surviving GAP names a live consumer + chunk anchor** (else demoted to NOISE, or recorded as a proposal in
   `comlab/config/proposals/`). Zero edges written into the canonical graph.
5. **Health sanity** on the LLM graph reported (confidence split; a high INFERRED share is expected and filtered out).
6. **No collateral:** `graph/v1_baseline/`, `graph/v2_code/`, `graph/v2_tests/`, `graph/v2_docs/`, canonical
   `graph/v2_wiki/graph.json`, and `research/chunks/` all byte-unchanged.

### Deliverables ###

1. `labs/obdlab/graph/v2_wiki_llm/` — the Pass-3 LLM scratch graph.
2. `labs/obdlab/graph/v2_wiki/PASS3_CROSSCHECK.md` — the CONFIRMED/GAP/NOISE report (the real deliverable).
3. The pre-step health line recorded in the progress note (baseline condition before the run).

### Files to touch ###

- `labs/obdlab/graph/v2_wiki_llm/` (new scratch graph)
- `labs/obdlab/graph/v2_wiki/PASS3_CROSSCHECK.md` (new report)
- `Vault/tasks/progress_notes/T-VAULT-WIKIGRAPH-1.md` (gate + review blocks)

### Out of scope ###

- Writing any edge into `graph/v2_wiki/graph.json` — route GAPs to `4dlab-wiki-prep`.
- Editing `research/chunks/` — that is `4dlab-wiki-prep`.
- `--deep` mode — excluded (it manufactures the noise this task suppresses).
- Acting on a proposal candidate — recording it is in scope; speccing/implementing it is a separate task.

### Verification (graph-tooling lane) ###

Use the protocol's checks in `_skills/graph/eval/PASS3_EVAL_PROTOCOL.md` §"Success criteria" with `<tier>=v2_wiki`.
Anti-orphan note: a GAP is only "real" if its consumer is read in a **live** code path — otherwise it is NOISE,
regardless of being EXTRACTED.

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-WIKIGRAPH-1.md` opens with the confirmed `## Plan` + the pre-step health line; the
run session fills `VERIFICATION GATE` (the checks + LLM-graph confidence split + CONFIRMED/GAP/NOISE counts) and
`CODE REVIEW` (the report diff; confirmation zero edges entered the canonical graph). The row flips to `done` only when
both blocks are clean and the canonical `graph/v2_wiki/graph.json` plus all sibling graphs are byte-unchanged.
