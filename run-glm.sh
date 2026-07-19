#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # wire omp skill:// discovery (parity with run-codex.sh / run-agy.sh)
# run-glm.sh — launch the GLM coder (z-ai/glm-5.2) in its isolated omp profile,
# routed through OpenRouter. Peer of run-codex.sh / run-agy.sh on the omp harness.
#
# Auth: OpenRouter API key, read from the environment — NEVER stored in-repo (project rule: no secrets in files):
#   export OPENROUTER_API_KEY=...     # in your shell / secret manager (already in ~/.bashrc)
# Optional override (default below):
#   export GLM_MODEL=openrouter/z-ai/glm-5.2
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-glm] note: $VENV not built yet — running without a project venv"; fi
: "${OPENROUTER_API_KEY:?set OPENROUTER_API_KEY in your environment (never commit it)}"
# OpenRouter: use the /chat/completions wire format, not the OpenAI Responses API.
# GLM-5.2 over OpenRouter's /responses endpoint closes the stream before a terminal
# event ("stream closed before a terminal response event"); chat-completions is stable.
export PI_OPENROUTER_RESPONSES=0
# Skip the first-run setup wizard. A fresh profile otherwise shows an onboarding panel
# (login-based providers only) and ignores --model; OpenRouter auth comes from the env
# key above, so go straight to the GLM session.
export OMP_SKIP_SETUP=1
# Firecrawl auth — key lives in _skills/firecrawl-web-scraping-search/API.md (owner-managed, value never copied into scripts)
FC_KEY_FILE="$WS/_skills/firecrawl-web-scraping-search/API.md"
[ -f "$FC_KEY_FILE" ] && export FIRECRAWL_API_KEY="$(tr -d '[:space:]' < "$FC_KEY_FILE")"
exec omp --profile glm --model "${GLM_MODEL:-openrouter/z-ai/glm-5.2}" --cwd "$WS" \
  --append-system-prompt "$(cat "$WS/.agent/coders/glm/AGENTS.md")" \
  "$@"
