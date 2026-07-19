# Codex — manual notes (human-readable; NOT omp durable memory)

Repeated build/test gotchas, local quirks, and patterns worth re-reading. One fact per line.
Do not store secrets. Native durable memory is omp **mnemopi** (`retain`/`recall`); this file is the
part a human wants to skim and version in git.

## Environment — Linux host (recorded 2026-06-27)

- SKILLS: `skill://<name>` resolves from `.agent/skills/` (git-ignored), wired by
  `scripts/wire_skills.sh` (run automatically by run-codex.sh / run-agy.sh on launch),
  keyed by each skill's frontmatter `name`. The real skills live in `_skills/` and per-lab
  `_<lab>_skills/`. If a `skill://X` ever errors `Unknown skill … Available: none`, run
  `bash scripts/wire_skills.sh` from `/agent_workspace`, then retry.
- PYTHON: ONE shared venv `/agent_workspace/.venv-wired` (Python 3.14.6, uv-built). Use
  `source /agent_workspace/.venv-wired/bin/activate`, or call `/agent_workspace/.venv-wired/bin/python`
  and `.../bin/pip` directly. NEVER bare `python`/`python3`/system pip — system default is 3.12.
  There is no `.sandbox-py` and no per-session Python download ritual (obsolete Windows-era).
- INNER LOOP: run PER-LAB — `cd labs/<lab>` then `ruff check .` → `pyright <pkg>` → `pytest -x -q`.
  pyright needs the venv active (or pass `--pythonpath /agent_workspace/.venv-wired/bin/python`).
  Collecting `labs` + `apps` together throws spurious duplicate-test-basename errors — always per-lab.
- GIT: branch `master`, `core.ignorecase=false`. Commits are owner-only, by explicit path.
  Never stage `.venv-wired/`, `graphify-out/`, `**/mysql_data/`, or `.agent/skills/`.
- CANON: infra + rules in `/agent_workspace/4DLab_CLAUDE.md` (Python environment, Git); shared
  coder rules `/agent_workspace/AGENTS.md`; your identity `.agent/coders/<you>/AGENTS.md`.
