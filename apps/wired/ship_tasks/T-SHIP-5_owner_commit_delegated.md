# T-SHIP-5 — commit all remaining paths (owner-delegated git ritual)
**Pack:** ship · **Blocked by:** T-SHIP-1 (tree proven green before it is frozen; owner may waive)
**Lane:** coder · **Write scope:** git index/history + one report + progress note. **Zero file edits**
except an optional `.gitignore` addition (step 3).

## Authority (read first)
Canon (`4DLab_CLAUDE.md`) reserves commits for the owner. **The owner explicitly delegated
this commit to a coder on 2026-07-07 (ship pack, Cowork architect session).** That delegation
covers exactly this task: staging and committing the current working tree by explicit path.
It does NOT extend to: branching, stashing, amending, rebasing, force operations, tag
creation, or pushing to any remote. Those remain owner-only. One-shot — future commits
revert to the owner ritual unless re-delegated.

## Why
~900 dirty paths (audit R-1): root doc deletions/moves, `labs/comlab/docs/Vocabulary/` +
`adr/` relocation, ledger and progress-note edits, graph caches, Vault mirror annotations,
`.firecrawl/` research caches, and this ship pack. A published app must build from a
committed tree, and the registry ledger already flags the mixed tree as a
"commit-scope hazard for `git add -A`" — which is exactly why this task forbids `git add -A`.

## Steps
1. **Inventory.** `git status --porcelain` → save the full list into the report. Group every
   path into the commit groups below; any path that fits no group goes to a FINDINGS list
   and is left uncommitted (surface, don't guess).
2. **Junk gate.** Identify tracked-dirty or untracked paths that are build junk
   (`__pycache__/`, `.pytest_cache/`, `*.egg-info/`, `.venv*`): these are NOT committed.
3. **Ignore gate.** If junk from step 2 is untracked-and-recurring, add the minimal
   `.gitignore` lines (the file is already dirty with edits — fold in, cite each line in the
   report). Do not gitignore graph caches or `.firecrawl/` — they are cited artifacts.
4. **Secrets gate (hard).** Before EACH commit: `git diff --cached | grep -inE
   "(api[_-]?key|secret|token|password|BEGIN (RSA|OPENSSH))"` — any hit aborts the whole
   task and is reported. No-secrets is canon; this gate is non-negotiable.
5. **Commit by explicit path, one group per commit**, suggested order + messages:
   | # | Group | Paths (explicit, from step-1 inventory) | Message stem |
   |---|---|---|---|
   | 1 | Root doc restructure | root-level `M`/`D` `.md` files (START_HERE, README, DECISIONS, deleted stale audits/handoffs/props), `.gitignore`, `.agent/` | `chore(docs): root doc restructure + stale doc sweep` |
   | 2 | Vocabulary/ADR relocation | `labs/comlab/docs/Vocabulary/`, `labs/comlab/docs/adr/`, related deletions of old wiki paths | `docs(comlab): relocate vocabulary + adr to docs/` |
   | 3 | Lab code + ledgers | remaining `labs/**` source/test/ledger/progress-note edits | `chore(labs): post-C9B ledger + residue sync` |
   | 4 | Graph artifacts | `labs/**/graph/**`, `GRAPH_MANIFEST.md`, `GRAPH_AUDIT_*.md`, `planning/graph_rollout/` | `chore(graph): cache + manifest sync` |
   | 5 | Vault mirror annotations | `Vault/**` (annotation edits only — verify no content deletions) | `docs(vault): task annotations (Q-GRAPH-LANES ruling)` |
   | 6 | Research caches | `.firecrawl/**` | `docs(research): firecrawl citation caches` |
   | 7 | Ship pack | `planning/SHIP_AUDIT_2026-07-07.md`, `apps/wired/ship_tasks/**`, `CLAUDE.md` bootstrap row | `chore(ship): pre-publish audit + ship pack` |
   | 8 | Apps/ECO/harness residue | remaining `apps/**`, `ECO/**`, `harness/**` edits | `chore(apps): residue sync` |
6. **Verify.** `git status --short` → empty (or FINDINGS-listed paths only). `git log
   --oneline -10` recorded in the report. Working tree byte-identical (no file edits —
   `git stash list` empty, nothing touched).
7. Report `apps/wired/ship_tasks/reports/SHIP_COMMIT_2026-07-07.md`: inventory, group→commit
   map (hash per group), junk/ignore/secrets gate results, FINDINGS. Fill both gate blocks;
   flip the ledger row.

## Success criteria
- `git status --short` empty apart from explicitly FINDINGS-listed paths (each with a reason).
- Every commit lists its paths explicitly in the report; **no `git add -A` / `git add .` anywhere**.
- Secrets gate ran before every commit, all clean; no branch/stash/amend/push occurred.
