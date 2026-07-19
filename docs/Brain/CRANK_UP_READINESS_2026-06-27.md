# Crank-up readiness — 4DLabV2 Linux migration (2026-06-27, session 2)

Verification of the full migration against the two reference docs' acceptance lists
(`LINUX_MINT_MIGRATION_PROPOSAL.md` Part 4 + `HANDOFF_2026-06-26_linux_migration.md` §10),
plus this session's git migration, Windows-residue purge, and Python-setup check.

**Bottom line:** the environment is ready to crank up GASLab (Stage 1). Everything verifiable
by the architect is green. The only open items need **you**: the two coder `/login`s and the
first migration commit.

## Definition-of-Done — verified

| # | Item (from §10 / Part 4) | Status | Evidence |
|---|---|---|---|
| 1 | `/agent_workspace` = 4DLabV2; parent infra recipe obtained | ✅ | adapted in-mount as `4DLab_CLAUDE.md` |
| 2 | rebuild/skip dirs gone; graphs intact; parent `graphify-out/` not rebuilt | ✅ | no Windows venvs/caches; per-lab graphs present |
| 3 | `AGENTS.md` capitalised; no stale `agents.md` refs | ✅ | 1 hit = intentional doc-text in `CLAUDE.md:28` |
| 4 | shared venv built; inner loop green | ✅ | `.venv-wired` on host py3.14.6; gaslab ruff clean · pyright 0 · 208 passed |
| 5 | graphs queryable without rebuild | ✅ | `graph_health.py` → all labs structurally sound, 0 dangling |
| 6 | launchers wire per-coder profile + `mnemopi` | ✅ (cfg) | `run-codex.sh`/`run-agy.sh` +x, syntax-ok, export `VIRTUAL_ENV`; profiles set `modelRoles` + `mnemopi` |
| 7 | each coder `agent.db` resolves a model | ⏳ YOU | needs `/login` per profile |
| 8 | coder self-reports role/boundaries (Codex ≠ Agy) | ⏳ YOU | needs `/login`; identities + lane-guard already in place |
| 9 | `.env` ignored; no secrets committed | ✅ | `.env`/`**/.env` added to `.gitignore`; secret scan clean |
| 10 | 204 pre-migration changes accounted for | ✅ | committed by owner as `c5034a3` WIP checkpoint |
| 11 | case-sensitivity (rename + `core.ignorecase false`) | ✅ | `AGENTS.md` rename; `git config core.ignorecase=false` |
| 12 | line endings LF; no CRLF | ✅ | `ls-files --eol` = `i/lf w/lf`; no CRLF blobs |
| 13 | parent-`4DLab` decision made; off-mount refs marked | ✅ | D1 child-only; bootstrap table marks `[off-mount]` rows |

## Done this session (beyond the original DoD)

- **Git migrated + set up.** `.git` placed from the Desktop backup; branch `master` @ `c5034a3`;
  `core.ignorecase=false`; `.gitignore`/`.gitattributes` restored (lean copy had dropped them) + `.env` added.
  Stat-cache/mode phantom (627 false "modified") cleared. **Working tree = the migration delta
  (16 edits + `agents.md→AGENTS.md` rename + ~90 new files), uncommitted — yours to commit by explicit path.**
- **Windows residue purged (recommended scope).** Fixed active canon/config: `vinlab/settings.json`
  (dead PowerShell statusline), `DELTA_PICKUP_START_HERE.md` + `SEMANTIC_START_HERE.md` (venv/git → Linux),
  `REGISTRY_START_HERE.md` (stale banner). Left frozen graphs + historical records untouched.
  Remaining code/doc items tracked in `WINDOWS_RESIDUE_FOLLOWUPS.md`.
- **Python setup verified vs `pythonagents.md`.** Method matches (uv + 3.14 + venv + editable + venv-python,
  never bare). Standardised on **one name `.venv-wired`**: fixed the `~/.bashrc` auto-activation hook
  (was pointing at non-existent `.venv`) → `cd /agent_workspace` now yields Python 3.14.6; added the
  venv rule to `.agent/coders/{codex,agy}/AGENTS.md`; adapted `pythonagents.md` to the real env.
- **omp skill discovery wired (was a hard blocker).** A coder hit `Unknown skill … Available: none` —
  omp only scans conventional dirs, but the 56 repo skills live in `_skills/`/`_<lab>_skills/`.
  Added `scripts/wire_skills.sh` (symlinks every skill into `.agent/skills/<name>` by its frontmatter
  name; idempotent), git-ignored `.agent/skills/`, and made `run-codex.sh`/`run-agy.sh` rebuild it on
  launch. **Verified headless:** `omp -p "Read skill://comlab-python"` → resolves. The COMLab trio and
  all COM_VAULT-referenced skills (`4dlab-vault`, `eval-code-graph`, prep skills, registry trio, …) resolve.

## Remaining — all need YOU

1. **`/login` each coder** (one-time): `omp --profile codex` → ChatGPT/Codex Pro; `omp --profile agy` →
   Google/Gemini Pro. Then the coder self-report (DoD #7/#8) can be confirmed. I can't authenticate for you.
2. **Commit the migration delta** — by explicit path, per the git ritual (I did not commit).
3. **`WINDOWS_RESIDUE_FOLLOWUPS.md`** — coder fixes for `vinlab/tools/*.py` hardcoded paths (needs the
   Linux data location), the registry bootstrap rewrite (when brought on-mount), and `.ps1` → `.sh`.
4. **Optional hygiene:** the lean copy landed the tree mode **777** (world-writable). Functional, and
   `core.fileMode=false` keeps it out of commits, but consider `find /agent_workspace -type f -not -path '*/.git/*' -exec chmod 644 {} +` then restore `+x` on `*.sh`.
5. **deepseek + claude coders:** deferred per your call — add later via the `run-<name>.sh` + `.agent/coders/<name>/` pattern (shared venv already exists).

## To crank up
Boot order unchanged: `START_HERE.md` → `ROADMAP.md` → GASLab first
(`labs/gaslab/tasks/GASLAB_TASKS_START_HERE.md`). Assign one task per coder via `.agent/assignments.md`.
