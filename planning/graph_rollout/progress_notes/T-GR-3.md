# T-GR-3 — Docs tier: gaslab (v2_docs)

**Task:** build offline docs tier `labs/gaslab/graph/v2_docs/` (assessment gap G2, offline structure
extraction, free/no key). **Lane:** ARCHITECT (Q-GRAPH-LANES). **Date:** 2026-07-06 ·
**Executor:** Architect (Cowork) · graphify 0.9.7 (T-GR-2) · host: Linux headless

## What was done
1. **Prep check (read-only):** `labs/gaslab/graph/v2_docs/ingest_ready/` populated — 71 prepared chunks
   (ADR/BDD/DLD/HLD/LLD/PRD) carrying explicit `## Graph relations` blocks. Prep confirmed done; not raw prose.
2. **Build (offline, no key):** scoped corpus copied to `/tmp/gaslab_v2docs`; ran
   `env -u {GEMINI,GOOGLE,DEEPSEEK,ANTHROPIC,OPENAI}_API_KEY graphify update /tmp/gaslab_v2docs`.
   Output relocated to `labs/gaslab/graph/v2_docs/` (graph.json + GRAPH_REPORT.md + graph.html).
3. **Cleanup:** stray root `graphify-out/` (manifest.json only, this run) removed; `/tmp` scratch cleared.

## Health / verify
- 344 nodes · 273 edges · 71 communities
- **0 dangling · 0 isolated · 100% EXTRACTED · INFERRED = 0**
- Spot-checks (`graphify explain … --graph labs/gaslab/graph/v2_docs/graph.json` → file+line, all correct):
  - `ADR-0007`            -> ADR_GASLab/00_Preamble.md L43
  - `CAM_TIMING_ADVANCED` -> LLD_GASLab/6._RPM-Differential_Family_Separation_(resolution.apply_differentiators).md L23
  - `Physical Constants`  -> DLD_GASLab/2._contracts.py.md L5
- Collateral: only the 3 files under `gaslab/graph/v2_docs/` touched (mtime-confirmed 13:43);
  all other lab graphs byte-unchanged. `graphify-out/` gone.

## Note — predicate layer deferred (by design)
All 273 edges are `contains` (doc→heading structure); the architectural predicates
(SUPERSEDES/CONSUMES/VERIFIES/MIRRORS_CONTRACT_IN) declared in the chunks require the `graphify extract`
LLM pass (`llm.py`), which is **out of scope for this pack** (START_HERE: "extract (LLM) is out of scope").
Per GRAPH_AUDIT canon the offline 100%-EXTRACTED docs tier is the sanctioned deliverable — registry's
offline-only docs graph is the GOOD precedent. Predicate layer to be added later via a separate LLM
`extract` task (owner: "finish all tasks then we move to llm extract").

## VERIFICATION GATE — T-GR-3
1. Prep     : PASS (71 prepared chunks; explicit relation blocks present)
2. Build    : PASS (offline `graphify update`, no key; relocated; no root graphify-out)
3. Health   : PASS (0 dangling, 0 isolated, 100% EXTRACTED, 0 INFERRED)
4. Spotcheck: PASS (3/3 doc symbols resolve to correct file+line)
5. Isolation: PASS (only gaslab/v2_docs touched; other graphs hash/mtime unchanged; /tmp cleared)
Result: CLEAN

## CODE REVIEW — T-GR-3
Scope: PASS (this note + ledger row + GRAPH_AUDIT inventory row + the 3 graph files; no lab source, no Vault).
Composition: PASS (offline `update` only, scoped to /tmp — never repo root; no existing tier rebuilt;
  no `graphify-out/` survives; `extract`/LLM not invoked).
Result: CLEAN
