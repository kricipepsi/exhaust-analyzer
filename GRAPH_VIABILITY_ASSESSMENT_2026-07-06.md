# GRAPH VIABILITY ASSESSMENT — 2026-07-06
**Question (owner):** should the labs be graphified so agents can fetch wiki/docs/code from the
Vault easily? Companion to `GRAPH_MANIFEST.md` (06-12, stale) and `GRAPH_AUDIT_2026-06-28.md` (live
canon). Authored by the architect; all numbers verified on disk today.

## 1. Verdict
**Viable — and mostly already done.** The tool is healthy, the offline tiers exist for every lab,
and the graphs are structurally sound. What actually blocks "agents easily fetch wiki/docs/code"
is NOT missing graphs — it is (a) the sanctioned query tool cannot see wiki content at all, and
(b) coders skip the lookup step (the 2026-07-06 Q-C5-EGR incident: the answer sat in
`dtclab/wiki/03_fuel_trim_grammar.md` while a coder re-researched it from memory). Close those two
gaps first; they are free. LLM wiki graphs stay waived.

## 2. Tool health (checked today)
- **Upstream (github.com/Graphify-Labs/graphify):** actively maintained — last commit 2026-07-05
  (hours before this scan), v8 branch, ~2,900-test suite, published benchmarks (LOCOMO recall@10
  0.497), multi-language AST. Notably now ships an **MCP server mode**
  (`python -m graphify.serve graph.json`, stdio or HTTP) — graph queries as first-class agent
  tools instead of hand-rolled JSON reads. Evidence: `.firecrawl/github-graphify-labs.md`.
- **Local:** `graphifyy 0.8.36` in `.venv-wired`, works. PyPI latest is **0.9.7**
  (`.firecrawl/pypi-graphifyy.md`) — behind but not blocking. Any upgrade must be its own pinned
  task and must NOT trigger rebuilds of existing graphs (GRAPH GUARDRAIL: frozen graphs are
  query-only; a version bump is not a rebuild licence).

## 3. What already exists (live, per GRAPH_AUDIT + today's mtimes)
- Every lab: `v2_code` + `v2_tests` (offline, free) — rebuilt 06-26/06-28, 0 dangling edges.
- Docs tiers: obdlab, symptomlab, comlab/registry (all EXTRACTED-only, GOOD).
- Wiki LLM tiers: obdlab, symptomlab only; the rest **waived by owner** (T-COM-GRAPH-LLM ruling:
  feasible but low value — best case was only ~17% INFERRED edges).
- Vault: built with provenance, references graphs by path (never copies them);
  `vault_query.py` runs (health: 1 FAIL — 2 task notes missing consumers; 9 cross-ledger WARNs).

## 4. The real gaps (ranked by value per unit cost)
| # | Gap | Cost | Why it matters |
|---|---|---|---|
| G1 | **`vault_query.py` cannot search wiki.** `docs`/`code` subcommands filter `labs/<lab>/docs\|code` paths only — `labs/<lab>/wiki/**` is invisible to the sanctioned query path. | ~an hour, free | This is the exact C5-EGR failure surface. "Wiki-first" canon currently bottoms out in raw grep, which coders skip. |
| G2 | **Missing offline docs tiers:** gaslab, dtclab, vinlab, dnalab, comlab-main. | free (`graphify update` after doc-prep), 1 lab/session | Completes the free tier matrix; docs = ADR/HLD/LLD/PRD where design intent lives. |
| G3 | **No agent-native query interface.** Agents hand-read `graph.json` / call vault_query via bash. | pilot: hours | Upstream `graphify.serve` exposes the graph as MCP tools — usable by Cowork AND omp coders. Pilot on one lab before committing. |
| G4 | Vault health FAIL (2 consumers) + 9 cross-ledger refs. | minutes | Bookkeeping; keeps `health` green so it stays trusted. |
| G5 | graphifyy 0.8.36 → 0.9.7. | small, risky-if-careless | Optional. Own task; verify new output format against ONE new build first; frozen graphs untouched. |
| — | LLM wiki tiers for remaining labs | tokens + backend | **Keep waived.** G1 gives wiki search for free; revisit only if query utility proves insufficient. |

## 5. Recommended sequence (each = one task spec, owner activates)
1. **T-VQ-WIKI** — add a `wiki` subcommand (and `grep`-style body search across wiki+docs+code) to
   `_skills/graph/4dlab-vault/scripts/vault_query.py`; wire it into the AGENTS.md wiki-first rule so
   "in doubt → query" is one command. Includes G4 cleanup.
2. **T-GRAPH-DOCS-{GAS,DTC,VIN,DNA,COM}** — offline docs tiers via prep→`4dlab-graphify-run`,
   one lab per session, EXTRACTED-dominance verified, PROVENANCE updated.
3. **T-GRAPH-MCP-1** — pilot `graphify.serve` (stdio) on `obdlab/graph/v2_current` for one coder
   session + Cowork; measure whether lookups actually replace grep. Decide roll-out after.
4. **T-GRAPHIFY-UPGRADE (optional)** — 0.9.7 in `.venv-wired`, smoke-build a scratch corpus,
   diff output schema, then unlock G2 builds on the new version. Never rebuild existing graphs.

## 6. Guardrails restated (unchanged by this assessment)
Frozen/existing graphs are query-only — no rebuild without an explicit task line. Never run
graphify from repo root (81.9k-node incident). Vault holds no `graph.json` (references by path).
Wiki tier is the only token-spending tier and stays waived. One graph task per session.
