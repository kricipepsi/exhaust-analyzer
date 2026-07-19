# T-VAULT-WIKIGRAPH-1 — progress note

## Plan

Pre-step (now, no tokens): run `eval-wiki-graph --health-only` on `graph/v2_wiki/graph.json`; expect Condition GOOD
(0 dangling; ~22 isolated fault/enum stubs expected). Record the line here. Then — only after T-VAULT-DOCGRAPH-2 lands
and the owner authorises re-extracting the canonical `v2_wiki` — run `4dlab-graphify-run` Pass 3 over
`labs/obdlab/research/chunks/` with `--backend deepseek` in **default mode** (NO `--deep`), scoped to that dir only
(never repo root). Relocate to the **scratch** `graph/v2_wiki_llm/` — never over canonical. Classify with
`eval-wiki-graph/scripts/eval_wiki_graph.py baseline llm --out graph/v2_wiki/PASS3_CROSSCHECK.md`: every LLM edge →
CONFIRMED / CANDIDATE_GAP (EXTRACTED diagnostic edge, both nodes exist, missing, **named** COMLab/fault-atlas consumer
+ chunk anchor → route to `4dlab-wiki-prep`) / NOISE (INFERRED/AMBIGUOUS, new-node, or organizational
documents/member_of/has_value). Scrutinise candidates that wire a previously isolated node first. Promote nothing.
Verify no collateral on sibling graphs or `research/chunks/`. Graph-tooling lane — no lab inner-loop/gate.

Preflight: `DEEPSEEK_API_KEY` set, no stale `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` shadowing it; name `--backend
deepseek` explicitly. Reconcile the runner's `graphifyy` version with `.venv-wired` before spending tokens.


## VERIFICATION GATE

_(runner fills: pre-step health line · separate-dir guard · default-mode command recorded · LLM-graph confidence
split · CONFIRMED/GAP/NOISE counts · no collateral · canonical v2_wiki byte-unchanged)_


## CODE REVIEW

_(runner fills: PASS3_CROSSCHECK.md diff walk · every GAP names a live consumer + chunk anchor or is demoted to NOISE ·
zero edges entered the canonical graph)_
