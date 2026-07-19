# GRAPH ROLLOUT — pack bootstrap (paste as msg 1 of each coder session)
**Mission:** make lab knowledge (wiki, docs, code) queryable by agents — per
`GRAPH_VIABILITY_ASSESSMENT_2026-07-06.md`. Query paths: `vault_query.py` (Vault) and the
`graphify` CLI (`query|path|explain|affected --graph labs/<lab>/graph/<tier>/graph.json`).
MCP serve is a pilot, not a dependency — **CLI is the sanctioned baseline access path.**
## Rules (non-negotiable)
- One task per session, in ledger order (`GRAPH_ROLLOUT_PROGRESS.md`). STRICT dual-gate
  (VERIFICATION GATE + CODE REVIEW blocks in the progress note).
- **Never rebuild an existing graph** unless the task file names the exact tier dir. Never touch
  `graphify-out/`. Never run graphify from repo root (81.9k-node incident). Never `Vault/` writes.
- Offline only for T-GR-1..9: `graphify update` (free, no key). **Canon amended (owner, 2026-07-06):**
  `extract` (LLM) is now in-pack as **T-GR-10/11 only** (Nemo lane, DeepSeek backend, builds into
  separate `v2_docs_llm/` dirs, disclosure-gated promotion). Still never over a canonical graph.
- Wiki-first for domain facts; firecrawl for genuine web needs (auth auto-exported by run-*.sh).
- Skills: `4dlab-graphify-run` (build+verify), `4dlab-doc-prep` (only if a prep gap surfaces).
## Lanes (owner ruling 2026-07-06, DECISIONS.md Q-GRAPH-LANES)
**T-GR-2..9 are ARCHITECT-lane** (graph builds/venv/serve). Coders take only tasks the ledger
assigns them (T-GR-1: done/Nemo). Coders may run read-only `graphify query|explain|path|affected`;
never build subcommands; never edit `.omp/rules/**`.
## Ledger order
T-GR-1 (query ergonomics) → T-GR-2 (tool upgrade) → T-GR-3…7 (docs tiers, one lab each,
any order after GR-2) → T-GR-8 (MCP pilot, owner-gated) → T-GR-9 (staleness refresh, owner-gated,
AFTER T-V3-P4-C5B lands — landed 2026-07-06) → T-GR-10 (LLM extract pilot, Nemo, owner-gated) →
T-GR-11 (LLM extract rollout, gated on the T-GR-10 promotion decision). T-GR-9 and T-GR-10/11 are
independent (code tiers vs docs predicate layer) — either may run first.
