#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # parity with run-codex/agy (harmless if unused)
# run-claude.sh — launch Claude Code (Opus 4.8) as a third coder, parallel to run-codex.sh / run-agy.sh.
# Harness: Anthropic Claude Code CLI. NOT omp.
#
# Claude Code auto-loads the repo CLAUDE.md (the ARCHITECT profile). The appended
# identity below overrides that to a coder role, the same way run-codex.sh appends
# the codex identity. If you instead launch interactively via `bonsai start` and it
# does NOT forward --append-system-prompt, paste the contents of
# .agent/coders/claude/AGENTS.md as message 1 of the session to get the same framing.
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-claude] note: $VENV not built yet — running without a project venv"; fi
cd "$WS"
# Firecrawl auth — key lives in _skills/firecrawl-web-scraping-search/API.md (owner-managed, value never copied into scripts)
FC_KEY_FILE="$WS/_skills/firecrawl-web-scraping-search/API.md"
[ -f "$FC_KEY_FILE" ] && export FIRECRAWL_API_KEY="$(tr -d '[:space:]' < "$FC_KEY_FILE")"
exec claude --append-system-prompt "$(cat "$WS/.agent/coders/claude/AGENTS.md")" "$@"
