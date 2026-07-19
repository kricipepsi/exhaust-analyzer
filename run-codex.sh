#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # wire omp skill:// discovery (show summary + any SKIP/DUPE warnings)
# run-codex.sh — launch the Codex coder (GPT-5.5 / openai-codex) in its isolated omp profile.
# Auth (one-time): `omp --profile codex` then `/login` to ChatGPT/Codex Pro. No API key.
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-codex] note: $VENV not built yet — running without a project venv"; fi
# Firecrawl auth — key lives in _skills/firecrawl-web-scraping-search/API.md (owner-managed, value never copied into scripts)
FC_KEY_FILE="$WS/_skills/firecrawl-web-scraping-search/API.md"
[ -f "$FC_KEY_FILE" ] && export FIRECRAWL_API_KEY="$(tr -d '[:space:]' < "$FC_KEY_FILE")"
exec omp --profile codex --cwd "$WS" \
  --append-system-prompt "$(cat "$WS/.agent/coders/codex/AGENTS.md")" \
  "$@"
