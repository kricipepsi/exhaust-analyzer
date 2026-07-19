#!/usr/bin/env bash
bash "$(dirname "$0")/scripts/wire_skills.sh" || true  # parity with run-claude.sh (harmless if unused)
# run-deepseek.sh — launch DeepSeek (deepseek-v4-pro) as a coder/auditor on the Claude Code harness,
# routed to DeepSeek's Anthropic-compatible API. Peer of run-claude.sh / run-codex.sh / run-agy.sh.
# Owner uses it primarily for NON-CODING work (audits, doc-conformance).
#
# SECRET — read from the environment, NEVER stored in-repo (project rule: no secrets in files):
#   export DEEPSEEK_API_KEY=...        # in your shell / secret manager, before running this
# Optional overrides (defaults below) — CONFIRM the base URL against your DeepSeek account:
#   export DEEPSEEK_BASE_URL=https://api.deepseek.com/anthropic
#   export DEEPSEEK_MODEL=deepseek-v4-pro
set -euo pipefail
WS=/agent_workspace
VENV="$WS/.venv-wired"   # shared host venv (built on host python3.14 via uv)
if [ -d "$VENV" ]; then export VIRTUAL_ENV="$VENV"; export PATH="$VENV/bin:$PATH"
else echo "[run-deepseek] note: $VENV not built yet — running without a project venv"; fi

: "${DEEPSEEK_API_KEY:?set DEEPSEEK_API_KEY in your environment (never commit it)}"
# Route the Claude Code CLI at DeepSeek's Anthropic-compatible endpoint.
export ANTHROPIC_BASE_URL="${DEEPSEEK_BASE_URL:-https://api.deepseek.com/anthropic}"
export ANTHROPIC_AUTH_TOKEN="$DEEPSEEK_API_KEY"
export ANTHROPIC_MODEL="${DEEPSEEK_MODEL:-deepseek-v4-pro}"

cd "$WS"
exec claude --append-system-prompt "$(cat "$WS/.agent/coders/deepseek/AGENTS.md")" "$@"
