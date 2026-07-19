# Claude — manual notes (human-readable; git-tracked)
Repeated build/test gotchas, local quirks, and patterns worth re-reading. One fact per line.
Do not store secrets. This harness has no omp durable memory; this file is the durable store.
## Environment — Linux host (recorded 2026-06-29)
- HARNESS: Claude Code (Opus 4.8), launched via `run-claude.sh` (or `bonsai start`). NOT omp.
  Root `CLAUDE.md` is the architect profile — your identity (`.agent/coders/claude/AGENTS.md`)
  overrides it to a coder role.
- SKILLS: `skill://<name>` shorthand is an omp feature (wired by `scripts/wire_skills.sh` for
  run-codex/agy). On Claude Code, read the real skills directly under `_skills/` and per-lab
  `_<lab>_skills/`.
- PYTHON: ONE shared venv `/agent_workspace/.venv-wired` (Python 3.14, uv-built). Use
  `source /agent_workspace/.venv-wired/bin/activate`, or call `/agent_workspace/.venv-wired/bin/python`
  and `.../bin/pip` directly. NEVER bare `python`/`python3`/system pip — system default is 3.12.
- INNER LOOP: run PER-LAB — `cd labs/<lab>` then `ruff check .` → `pyright <pkg>` → `pytest -x -q`.
  Collecting `labs` + `apps` together throws spurious duplicate-test-basename errors — always per-lab.
- GIT: branch `master`, `core.ignorecase=false`. Commits are owner-only, by explicit path.
  Never stage `.venv-wired/`, `graphify-out/`, `**/mysql_data/`, or `.agent/skills/`.
- CANON: infra + rules in `/agent_workspace/4DLab_CLAUDE.md`; shared coder rules
  `/agent_workspace/AGENTS.md`; your identity `.agent/coders/claude/AGENTS.md`.
