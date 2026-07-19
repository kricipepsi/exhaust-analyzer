# T-GR-6 — Docs tier: dnalab (v2_docs)
**Task:** build offline docs tier `labs/dnalab/graph/v2_docs/` (gap G2, offline structure, free/no key).
**Lane:** ARCHITECT (Q-GRAPH-LANES). **Date:** 2026-07-06 · **Executor:** Architect (Cowork) ·
graphify 0.9.7 (T-GR-2) · host: Linux headless
## What was done
1. **Prep check (read-only):** `ingest_ready/` populated — 51 prepared chunks (ADR/BDD/DLD/HLD/LLD/PRD)
   with explicit `## Graph relations` blocks (doc-prep note T-DNAV-DOCPREP). Confirmed done; not raw prose.
2. **Build (offline, no key):** scoped copy to `/tmp/dnalab_docs`; `env -u *_API_KEY graphify update`.
   Relocated graph.json + GRAPH_REPORT.md + graph.html to `labs/dnalab/graph/v2_docs/`.
3. **Cleanup:** no root `graphify-out/` (built under /tmp, outside repo).
## Health / verify
- 215 nodes · 164 edges · 51 communities
- **0 dangling · 0 isolated · 100% EXTRACTED · INFERRED = 0**
- Spot-checks (`graphify explain … --graph labs/dnalab/graph/v2_docs/graph.json` -> file+line, correct):
  - `adr_dnalab_adr_0001_..._decision` -> ADR_DNALab/ADR-0001_DNALab_composes_it_does_not_decode.md L13
  - `dld_dnalab_4_assemblypy_buildvehicledna` -> DLD_DNALab/4_assemblypy_buildvehicledna.md L1
  - `bdd_dnalab_feature_json_roundtrip` -> BDD_DNALab/Feature_JSON_roundtrip.md L1
- Collateral: only the 3 files under `dnalab/graph/v2_docs/` touched (mtime 14:20); other lab graphs unchanged; no root `graphify-out/`.
## Note — predicate layer deferred (by design)
All 164 edges are `contains`; architectural predicates (SUPERSEDES/CONSUMES/VERIFIES/MIRRORS_CONTRACT_IN)
require the `graphify extract` LLM pass — out of scope for this pack. Offline 100%-EXTRACTED docs tier is
the sanctioned deliverable (registry precedent = GOOD). Matches siblings T-GR-3/4/5.
## VERIFICATION GATE — T-GR-6
1. Prep : PASS (51 prepared chunks; relation blocks present)
2. Build : PASS (offline `graphify update`, no key; relocated; no root graphify-out)
3. Health : PASS (0 dangling, 0 isolated, 100% EXTRACTED, 0 INFERRED)
4. Spotcheck: PASS (3/3 resolve to correct file+line)
5. Isolation: PASS (only dnalab/v2_docs touched; pre-existing repo dirt unrelated)
Result: CLEAN
## CODE REVIEW — T-GR-6
Scope: PASS (this note + ledger row + GRAPH_AUDIT row + 3 graph files; no lab source, no Vault).
Composition: PASS (offline `update` only, scoped to /tmp; no existing tier rebuilt; no `graphify-out/` survives; `extract`/LLM not invoked).
Result: CLEAN
