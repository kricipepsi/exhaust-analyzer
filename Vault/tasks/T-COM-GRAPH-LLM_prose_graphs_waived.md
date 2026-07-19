---
node_type: task
task_id: T-COM-GRAPH-LLM
status: waived
pack: VAULT
lab: comlab
mode: graph-tooling
blocked_by:
- T-COM-WIKIPREP
- T-COM-DOCPREP
consumers:
- graph/v2_wiki — wiki prose graph (NOT built this pack)
- graph/v2_docs — docs prose graph (NOT built this pack)
tags:
- task
- vault
- comlab
- waived
---

# T-COM-GRAPH-LLM — Prose Pass-3 graphs (wiki + docs) — WAIVED (liftable)

**Status:** `waived` (owner direction 2026-06-26) · **Pack:** VAULT (COMLab) · **Mode:** GRAPH-TOOLING
**Origin:** pipeline guide §5 (wiki/docs Pass-3) · **Blocked by:** T-COM-WIKIPREP, T-COM-DOCPREP
**Load skills:** n/a while waived. **If lifted:** `4dlab-graphify-run`, `eval-wiki-graph`, `eval-doc-graph`.

> This row exists so the chain is explicit and the waiver + its lift condition are recorded. **No work runs
> here unless the owner lifts the waiver.** Do not build these graphs as a side-effect of any other task.

## Why waived (the "skip graph testing" trim — mirror DTC/VIN/DNA)

The LLM Pass-3 prose graphs (`v2_wiki`, `v2_docs`) cost tokens and **require an LLM backend** on the coder
host (graphify auto-selects `gemini → kimi → claude → openai → deepseek …` from whichever API key is set, or
an authenticated `claude-cli`). That backend is an **unverified external dependency** for this pack, and the
last four labs (GAS/DTC/VIN/DNA) all waived prose graphs because:

- The Phase-2 prep already makes relations **explicit** (`T-COM-WIKIPREP`, `T-COM-DOCPREP` append the
  `CONSUMES`/`VERIFIES` lines), and
- The vault copies wiki/docs as raw `.md` + **injected frontmatter** regardless of whether a prose graph
  exists — `consumers` are architect-named, not derived from the prose graph.

So the prose graph adds marginal value here for real token + backend cost. `build_lab_vault.py`'s `comlab`
entry therefore requires only `("v2_code", "v2_tests")` (set by `T-COM-PATHS-1`).

## Viability note (the assessment behind the waiver)

The Pass-3 pipeline is **technically proven** — OBDLab built `v2_wiki` + `v2_docs` (+ a `v2_docs_llm`
cross-check) and symptomlab built `v2_wiki` + `v2_docs`. So it is *feasible*, not *blocked*. The trim is a
cost/dependency decision, not an infeasibility. Hence: liftable.

## Lift condition (how to enable, if the owner says yes)

1. Confirm a Pass-3 backend on the coder host (`--backend deepseek` with `DEEPSEEK_API_KEY`, or
   `--backend claude-cli` with `loggedIn: true`). Get the owner's explicit "graphify comlab wiki + docs" + a
   token-cost ack on the record.
2. Run `4dlab-graphify-run` on `labs/comlab/wiki/` → `graph/v2_wiki/` `--directed`, and on
   `labs/comlab/graph/v2_docs/ingest_ready/` → `graph/v2_docs/` `--directed`.
3. Health-check each with `eval-wiki-graph` / `eval-doc-graph` (Part-A): EXTRACTED dominates; dangling = 0;
   isolated may be > 0 for wiki (expected). Optionally run the Part-B cross-check (re-extracts a canonical
   graph → gated, owner instruction only).
4. Edit the `comlab` entry in `LAB_SRC_PATHS` to `required_graph_tiers: ("v2_code","v2_tests","v2_wiki","v2_docs")`
   and remove `comlab` from the "waived by owner direction" provenance branch (the symptomlab precedent).
5. Re-run `T-COM-VAULT` (idempotent) so the wiki/docs frontmatter can reference the prose graph.

## Out of scope while waived

Everything — this row builds nothing. Re-extracting `v1_baseline` is forbidden. `registry/` is out of pack.

## Progress hook

No progress note while `waived`. If lifted, create `Vault/tasks/progress_notes/T-COM-GRAPH-LLM.md` with the
confirmed `## Plan` (backend named + owner ack) and the usual `VERIFICATION GATE` + `CODE REVIEW` blocks.
