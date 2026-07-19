#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # wire omp skill:// discovery (parity with run-codex.sh / run-glm.sh)
# run-nemo.sh — launch the Nemo coder (nvidia/nemotron-3-ultra-550b-a55b:free) in its isolated
# omp profile, routed through OpenRouter. Peer of run-codex.sh / run-agy.sh / run-glm.sh.
#
# Auth: OpenRouter API key, read from the environment — NEVER stored in-repo (project rule: no secrets in files):
#   export OPENROUTER_API_KEY=...     # in your shell / secret manager (already in ~/.bashrc)
# Optional override (default below):
#   export NEMO_MODEL=openrouter/nvidia/nemotron-3-ultra-550b-a55b:free
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-nemo] note: $VENV not built yet — running without a project venv"; fi
: "${OPENROUTER_API_KEY:?set OPENROUTER_API_KEY in your environment (never commit it)}"
# OpenRouter: use the /chat/completions wire format, not the OpenAI Responses API.
# Verified 2026-06-30: Nemotron-3-ultra over OpenRouter's /responses endpoint errors
# (upstream Nvidia ResourceExhausted / stream not terminated); /chat/completions returns clean.
export PI_OPENROUTER_RESPONSES=0
# Skip the first-run setup wizard. A fresh profile otherwise shows an onboarding panel
# (login-based providers only) and ignores --model; OpenRouter auth comes from the env
# key above, so go straight to the Nemo session.
export OMP_SKIP_SETUP=1
# Reasoning effort: medium = viable default for real implementation. Override per launch:
#   NEMO_THINKING=low  ./run-nemo.sh   (trivial/fast tasks)
#   NEMO_THINKING=high ./run-nemo.sh   (gnarly debugging / planning)
# Firecrawl auth — key lives in _skills/firecrawl-web-scraping-search/API.md (owner-managed, value never copied into scripts)
FC_KEY_FILE="$WS/_skills/firecrawl-web-scraping-search/API.md"
[ -f "$FC_KEY_FILE" ] && export FIRECRAWL_API_KEY="$(tr -d '[:space:]' < "$FC_KEY_FILE")"
exec omp --profile nemo --model "${NEMO_MODEL:-openrouter/nvidia/nemotron-3-ultra-550b-a55b:free}" --cwd "$WS" \
  --thinking="${NEMO_THINKING:-medium}" --hide-thinking \
  --append-system-prompt "$(cat "$WS/.agent/coders/nemo/AGENTS.md")" \
  "$@"
