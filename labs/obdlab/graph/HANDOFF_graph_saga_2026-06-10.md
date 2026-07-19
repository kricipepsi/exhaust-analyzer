# Handoff — graph / Pass-3 saga (2026-06-10)

## Where we landed

The OBDLab docs-tier graph is **healthy; Pass 3 is not the blocker.** The real gap is that the graph's
edges are built but **nothing reads them yet**. Next move = wire a consumer, *then* let Pass 3 verify.

## What was decided / delivered this session

1. **Pass-3 auth root cause confirmed.** graphify's Pass 3 spawns an LLM via `claude-cli`; the Claude
   Pro OAuth session blocks it. Fix: graphify ships a **native DeepSeek backend** — no Codex, no
   claude-cli needed. Run `graphify extract <dir> --backend deepseek` (DeepSeek key is set).
   `--backend deepseek` must be **named explicitly** or a stale `ANTHROPIC_API_KEY` shadows it.
   Setup notes: `4DLab/graphify_deepseek_setup.md`.
2. **Skill updated** — `4DLabV2/_skills/graph/4dlab-graphify-run/SKILL.md` gained the DeepSeek backend
   guidance + new **Step 5 "Pass 3 noise control"** (checker-not-adder gate).
3. **Task specced (not run)** — `Vault/tasks/T-VAULT-DOCGRAPH-2_pass3_llm_crosscheck.md` (+ progress
   note): run Pass 3 into a scratch `v2_docs_llm/`, diff vs deterministic `v2_docs/`, classify edges
   CONFIRMED / GAP / NOISE, promote nothing. **Recommend HOLDING this until consumer wiring exists.**
4. **Graph audit done** — `graph/GRAPH_AUDIT_2026-06-10.md`. Findings below.

## Audit findings (the state of the graph)

- `v2_docs`: 480 nodes / 1045 edges, **100% EXTRACTED**, 0 dangling / 0 isolated / 0 duplicate. Clean.
- Consumer edges real & well-formed: `CONSUMES` (76, COMLab/VEEngine/etc → fields), `GATED_BY` (24),
  `ROUTES_TO` (10), `VERIFIES` (93). The signal/noise backbone is already encoded.
- **The gap:** `build_lab_vault.py` only checks the graph *exists*, doesn't traverse edges; signal/noise
  is enforced on note frontmatter, not graph edges. `/check-impact` + `/graph-find` are **planned, not
  built**. Only `CONSUMES` has any reader; `GATED_BY` / `ROUTES_TO` / `VERIFIES` have none.

## Open flags (carry forward — not fixed)

1. **Path mismatch:** `build_lab_vault.py` reads `labs/obdlab/graphify-out/graph.json` (a stale
   2026-06-09 artefact) — canonical docs graph is at `graph/v2_docs/graph.json` (2026-06-10).
2. **Stale ledger:** `T-VAULT-DOCGRAPH-1` header says `pending`; its progress note shows gates done.
3. **Version drift:** DOCGRAPH-1 note = `graphifyy 0.8.36`; `.venv-wired` = `0.8.35`. Pin the env.

## Recommended next session (one task)

**Author + run a consumer-wiring task** before DOCGRAPH-2:
- fix the `graphify-out → graph/v2_docs` path so the consumer reads the *current* graph, and
- make one consumer actually traverse the edges (e.g. `CONSUMES` in `build_lab_vault.py`, or stub
  `/check-impact` / `/graph-find`).

Then run `T-VAULT-DOCGRAPH-2` as a checker. Start next session via the relevant `*_START_HERE.md`;
one task per session.

## Files touched this session

- `4DLab/graphify_deepseek_setup.md` (new)
- `4DLabV2/_skills/graph/4dlab-graphify-run/SKILL.md` (edited: backend + Step 5)
- `4DLabV2/Vault/tasks/T-VAULT-DOCGRAPH-2_pass3_llm_crosscheck.md` (new)
- `4DLabV2/Vault/tasks/progress_notes/T-VAULT-DOCGRAPH-2.md` (new)
- `4DLabV2/labs/obdlab/graph/GRAPH_AUDIT_2026-06-10.md` (new)
- `4DLabV2/labs/obdlab/graph/HANDOFF_graph_saga_2026-06-10.md` (this file)
