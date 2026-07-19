# SHIP_COMMIT — T-SHIP-5 (owner-delegated commit ritual)
**Date:** 2026-07-07 · **Runner:** Cowork architect (owner delegation 2026-07-07)
**Branch:** `task/t-com-vault` (pre-existing — no branch operations performed; **merge to the
mainline is an owner call**, not delegated).

## Commits (grouped, explicit paths; NO `git add -A` used)
```
9e73110 chore(root): stale-doc deletions, launcher scripts, local-state gitignore (T-SHIP-5 G8)
2eeb67b chore(apps+v3+skills): ship pack, v3 residue, wired reports, skills sync (T-SHIP-5 G7)
ce11bda docs(vault): mirror task annotations (Q-GRAPH-LANES ruling) (T-SHIP-5 G5)
99b6c34 docs(planning+graph): audits, graph rollout, ship audit home (T-SHIP-5 G4)
d67b4d4 chore(labs): post-C9B code/test/ledger sync + VIN brand-spelling repair (T-SHIP-5 G3)
fc18aa7 docs(comlab): Vocabulary + adr relocation, §17 34-value doc-sync (T-SHIP-5 G2)
2b89662 chore(docs): root doc restructure + stale doc sweep (T-SHIP-5 G1)
d2b7350 T-V3-P4-C9B: C9 signal commit and V3_YARDSTICK_2026-07-06-C9B mint
```
| Group | Content |
|---|---|
| G1 `2b89662` | root docs (CLAUDE/README/START_HERE/DECISIONS/AGENTS/4DLab_CLAUDE), .agent/, .gitignore |
| G2 `fc18aa7` | labs/comlab/docs Vocabulary+adr relocation incl. §17 34-value sync |
| G3 `d67b4d4` | labs/** code/test/ledger sync + VIN brand repair (incl. lab graph artifacts) |
| G4 `99b6c34` | planning/ (ship audit, VIN audit, graph rollout), docs/, root graph manifests |
| G5 `ce11bda` | Vault/ mirror annotations (Q-GRAPH-LANES ruling; annotations only) |
| G7 `2eeb67b` | apps/ (ship pack, wired reports), v3/ residue, _skills/, harness/, scripts/ |
| G8 `9e73110` | root stale-doc deletions (previously archived), run-*.sh launchers, local-state gitignore |
| G9 | this report + final ledger flip (closing commit) |

## Gates
- **Secrets gate:** ran on every staged diff (`api_key/secret/token/password/BEGIN RSA|OPENSSH/sk-…`).
  Hits were all prose or env-var *names* in agent instructions ("No secrets in files",
  "do NOT set GEMINI_API_KEY") — zero secret values. CLEAN.
- **Junk gate:** zero `__pycache__/.pytest_cache/egg-info` paths were tracked-dirty.
- **Ignore gate (new .gitignore lines, each cited):** `vpic/` (81 MB local source DB,
  host-restorable) · `.vinlab_empty_dbs/` · `node_modules/` (298 MB) · `.obsidian/` ·
  `.omp/` (agent runtime) · `CLAUDE.local.md` (local-only by convention) · `scratch/` ·
  `re` (stray PostScript file). **Owner review:** if any of these should be repo content,
  say so — nothing was deleted, only left untracked.
- **G6 (.firecrawl/):** already gitignored — nothing to commit (research caches stay local).

## Verify
`git status --porcelain` → empty before G9. No branch/stash/amend/push performed.
