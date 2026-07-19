# Nemo — msg 1: T-GR-10 (LLM extract pilot, gaslab) — paste this as your first message

You are running ONE task: `planning/graph_rollout/tasks/T-GR-10_llm_extract_pilot_gaslab.md`.
Read, in order, before doing anything:
1. `planning/graph_rollout/GRAPH_ROLLOUT_START_HERE.md` (pack rules — non-negotiable)
2. the task file above (goal, success criteria, verification block)
3. `_skills/graph/4dlab-graphify-run/SKILL.md` — especially §"Pass 3 noise control" and the
   metadata CAVEAT (T-GR-9): the tool has known sharp edges.

## What this task is
Build the LLM Pass-3 docs graph for gaslab into `labs/gaslab/graph/v2_docs_llm/` and write a diff
report vs the canonical offline `labs/gaslab/graph/v2_docs/`. **Disclosure only** — you produce a
report and a scratch-tier graph; the owner decides promotion afterward. You do NOT touch the
canonical graph, any ledger "deferred" wording, or any other lab.

## Backend — resolve FIRST, before spending anything
- If `DEEPSEEK_API_KEY` is set in your environment → `--backend deepseek`.
- Else → check `claude` CLI auth (`loggedIn: true` required). If authenticated →
  `--backend claude-cli` (concurrency is forced to 1; it will be slow — that's fine for one lab).
- If NEITHER works: **STOP and report back.** Do not hunt for keys, do not try other backends,
  do not hand-author edges (writing edges into graph.json yourself is forbidden, always).
- Always pass the backend by NAME. Never let graphify auto-detect. Record which backend ran.

## The run (exact shape)
```bash
cp -r /agent_workspace/labs/gaslab/graph/v2_docs/ingest_ready /tmp/gaslab_docs_llm
cd /agent_workspace/labs/gaslab
graphify extract /tmp/gaslab_docs_llm --directed --backend <resolved>   # default mode. NEVER --deep
# relocate graphify-out/{graph.json,GRAPH_REPORT.md,graph.html} -> labs/gaslab/graph/v2_docs_llm/
```
Use `/agent_workspace/.venv-wired/bin/graphify`. Never run from repo root (81.9k-node incident).
No root `graphify-out/` may survive.

## Hard guards (violating any one = stop and report)
- NEVER write over `labs/gaslab/graph/v2_docs/` (canonical). Output dir is `v2_docs_llm/` only.
- NEVER rebuild any other graph; never touch `Vault/`; never edit `.omp/rules/**`.
- No key material in any file, note, or report — env only.
- Read-only everywhere except: `labs/gaslab/graph/v2_docs_llm/`, your report, your progress note.

## Deliverables (success criteria 1–5 in the task file are the contract)
1. `labs/gaslab/graph/v2_docs_llm/{graph.json,GRAPH_REPORT.md,graph.html}` — 0 dangling,
   confidence split reported, EXTRACTED dominant.
2. Predicate counts: SUPERSEDES / CONSUMES / VERIFIES / MIRRORS_CONTRACT_IN (lowercase accepted).
   Zeros stated honestly. 3 predicate spot-checks resolving to chunk file+line via `explain`.
3. `planning/graph_rollout/REPORT_T-GR-10_llm_extract_pilot.md` — diff vs canonical v2_docs
   classified CONFIRMED / GAP / NOISE (skill §5 promotion gate), token/cost figure, backend used,
   and a promotion recommendation (A adopt-as-tier / B supplementary / C drop) with reasoning.
4. Dual-gate progress note `planning/graph_rollout/progress_notes/T-GR-10.md`
   (VERIFICATION GATE + CODE REVIEW blocks, house style — see T-GR-9.md for the shape).
5. Run the task file's verification block verbatim; paste output in the note.
Ledger flip T-GR-10 → done only when all gates are CLEAN. The promotion decision itself stays OPEN
for the owner — do not make it.

## If anything goes sideways
Backend refuses, extraction hangs, counts look absurd, or a guard is at risk → stop, write down
exactly what you saw, report back. A clean STOP is a valid outcome; a quiet workaround is not.
Final git commit is the owner's, by explicit path — never commit, branch, or stash.
