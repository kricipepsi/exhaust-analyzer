#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # wire omp skill:// discovery (show summary + any SKIP/DUPE warnings)
# run-agy.sh — launch the Agy coder (Gemini 3.5 Flash / google-antigravity) in its isolated omp profile.
# Auth (one-time): `omp --profile agy` then `/login` to Google/Gemini Pro. No API key.
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-agy] note: $VENV not built yet — running without a project venv"; fi
# Firecrawl auth — key lives in _skills/firecrawl-web-scraping-search/API.md (owner-managed, value never copied into scripts)
FC_KEY_FILE="$WS/_skills/firecrawl-web-scraping-search/API.md"
[ -f "$FC_KEY_FILE" ] && export FIRECRAWL_API_KEY="$(tr -d '[:space:]' < "$FC_KEY_FILE")"
exec omp --profile agy --cwd "$WS" \
  --append-system-prompt "$(cat "$WS/.agent/coders/agy/AGENTS.md")" \
  "$@"
