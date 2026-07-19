# DeepSeek — manual notes (human-readable; git-tracked)
Repeated gotchas and patterns worth re-reading. One fact per line. **Do not store secrets.**

## Environment — Linux host (recorded 2026-06-29)
- HARNESS: Claude Code CLI routed to DeepSeek (`deepseek-v4-pro`), launched via `run-deepseek.sh`.
  Root `CLAUDE.md` is the architect profile; your identity (`.agent/coders/deepseek/AGENTS.md`)
  overrides it to a coder/auditor role.
- API KEY: read from `$DEEPSEEK_API_KEY` in the environment by `run-deepseek.sh`. NEVER written to any
  file (project rule: no secrets in files). Endpoint/model are env-overridable
  (`DEEPSEEK_BASE_URL`, `DEEPSEEK_MODEL`) — confirm the base URL matches your DeepSeek account's
  Anthropic-compatible endpoint.
- PRIMARY LANE: read-only audits — `T-DCA-*` (doc-conformance, `planning/doc_conformance/`) and
  `T-GTA-*` (graph-trust, `apps/vault/audit/`). Discover, don't fix; one report file per task.
- SKILLS: read real skills directly under `_skills/` and per-lab `_<lab>_skills/` (no omp `skill://`).
- PYTHON (only if a task needs it): shared venv `/agent_workspace/.venv-wired` (3.14). Never bare python.
- GIT: commits are owner-only, by explicit path. You never commit/branch/stash.
