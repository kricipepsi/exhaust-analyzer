---
node_type: task
task_id: T-VAULT-CODEGRAPH-1
status: pending
pack: VAULT
lab: obdlab
mode: graph-tooling lane
blocked_by:
- T-VAULT-DOCGRAPH-2
consumers:
- Obsidian graph navigation
- drift-guards.base — coverage view
- design→code→test spine (.base views)
implements:
- labs/obdlab/graph/v2_code/GRAPH_HEALTH.md
- labs/obdlab/graph/v2_code/PASS3_CROSSCHECK.md
tags:
- task
- vault
- obdlab
---

# T-VAULT-CODEGRAPH-1 — cross-check of the deterministic (AST) code graph (checker, not adder)

**Status:** `pending` · **Pack:** VAULT · **Mode:** GRAPH-TOOLING lane (graphify run — no lab inner-loop/gate)
**Origin:** Owner request 2026-06-10 — extend the DOCGRAPH-2 checker to the **code** tier (`graph/v2_code/`).
**Blocked by:**
1. **T-VAULT-DOCGRAPH-2** — run the docs cross-check first; only pursue the code tier if it shows Pass 3 earns its keep.
2. **Explicit owner instruction to re-extract `v2_code`** (canonical graph; CLAUDE.md HARD RULE) — Part B only.

> **Read this before scoping the code tier — the instrument is different here.** The code graph's baseline is built by
> **Pass 1 (AST — a static read of the source, no LLM)**, so its structural edges (`calls/contains/inherits/method/
> uses/references`) are **ground truth**. Two consequences: (a) an LLM re-reading code mostly manufactures INFERRED
> noise — the v2_code baseline is *already ~50% INFERRED* — and (b) graphify's Pass 3 is designed for **prose**, so an
> LLM pass over `.py` may be unsupported or meaningless. Therefore the code "check" is split into a cheap, always-valid
> part and a gated, low-value part.

### Part A — health-check (DEFAULT; runnable now, no extraction, no tokens, no owner gate) ###

This is the part that actually "confirms the code graph is in good condition":

```bash
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py \
  labs/obdlab/graph/v2_code/graph.json \
  --out labs/obdlab/graph/v2_code/GRAPH_HEALTH.md
```

Expect **Condition: GOOD** (0 dangling, 0 isolated — every symbol node wired). Report the confidence split (the high
INFERRED share is a property of the baseline, not a defect). **Part A alone satisfies the owner's "check the code
graph" request** and needs no re-extraction or owner waiver.

### Part B — LLM Pass-3 cross-check (OPTIONAL, GATED, expected near-pure-noise) ###

Only if the owner explicitly wants it **and** docs Pass 3 proved valuable. **Precondition to resolve first:** confirm
`4dlab-graphify-run` / graphify actually supports an LLM pass over a `.py` package. If it does not, **stop** — Part B
is not runnable and the code check ends at Part A (optionally plus a deterministic AST-reproducibility diff: re-run
Pass 1 into a scratch dir and confirm it reproduces the baseline edge-for-edge — that, not an LLM pass, is the right
"is the graph stable?" check for AST code; spec it as a follow-up if wanted).

If supported: run the LLM pass over the code package with `--backend deepseek` **default mode** → relocate to
`graph/v2_code_llm/` → classify:

```bash
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py \
  labs/obdlab/graph/v2_code/graph.json \
  labs/obdlab/graph/v2_code_llm/graph.json \
  --out labs/obdlab/graph/v2_code/PASS3_CROSSCHECK.md
```

Treat every `CANDIDATE_GAP` as a **candidate AST blind spot**: open the source and confirm it is a relation the static
parse genuinely cannot see (dynamic dispatch, `getattr`/reflection, runtime-registered call). If the AST *should* have
caught it, the LLM edge is NOISE. A genuine blind spot is fixed in the **extractor / AST config**, never patched into
`graph.json`. Consumer anchor: **graph navigation / drift-guards / the design→code→test spine** (NOT COMLab analytics —
code edges are structural).

### Success criteria ###

- **Part A:** `graph/v2_code/GRAPH_HEALTH.md` exists with a GOOD/CHECK verdict and the confidence split; canonical
  graph byte-unchanged (read-only).
- **Part B (if run):** separate-dir guard (`graph/v2_code_llm/`; canonical byte-unchanged; no root `graphify-out/`);
  default mode recorded; `PASS3_CROSSCHECK.md` classifies every edge; every surviving GAP is a confirmed AST blind spot
  with a named consumer (else NOISE); zero edges written into the canonical graph; no collateral on sibling graphs.

### Deliverables ###

1. `labs/obdlab/graph/v2_code/GRAPH_HEALTH.md` — the Part-A condition report (the default deliverable).
2. *(Part B only)* `labs/obdlab/graph/v2_code_llm/` + `labs/obdlab/graph/v2_code/PASS3_CROSSCHECK.md`.

### Files to touch ###

- `labs/obdlab/graph/v2_code/GRAPH_HEALTH.md` (new — Part A)
- *(Part B)* `labs/obdlab/graph/v2_code_llm/` + `labs/obdlab/graph/v2_code/PASS3_CROSSCHECK.md`
- `Vault/tasks/progress_notes/T-VAULT-CODEGRAPH-1.md` (gate + review blocks)

### Out of scope ###

- Writing any edge into `graph/v2_code/graph.json` — a genuine AST gap is fixed in the extractor/AST config.
- `--deep` mode. Re-running `v2_wiki/v2_docs/v2_tests` extraction.
- Implementing an extractor fix for a confirmed blind spot — record it; speccing/implementing is a separate task.

### Verification (graph-tooling lane) ###

Part A: confirm the health report renders a verdict and the canonical graph is byte-unchanged. Part B: use the
protocol's checks in `_skills/graph/eval/PASS3_EVAL_PROTOCOL.md` §"Success criteria" with `<tier>=v2_code`.
Anti-orphan note: a code GAP is only "real" if it is both a true AST blind spot AND read in a live code path.

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-CODEGRAPH-1.md` opens with the confirmed `## Plan`. The run session fills
`VERIFICATION GATE` (Part A verdict + confidence split; if Part B run, the separate-dir guard + CONFIRMED/GAP/NOISE
counts) and `CODE REVIEW` (each candidate AST blind spot validated against source; zero edges entered the canonical
graph). The row flips to `done` only when both blocks are clean and the canonical graph is byte-unchanged.
