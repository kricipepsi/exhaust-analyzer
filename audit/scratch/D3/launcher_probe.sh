#!/usr/bin/env bash
# D3 probe: what a coder launcher (run-codex.sh) does on a fresh clone, WITHOUT running omp.
# It replays run-codex.sh with `exec omp` replaced by a stub that prints what omp would receive,
# and skips line 2 (wire_skills.sh writes .agent/skills/). Read-only: writes nothing.
# Usage (from repo root): bash audit/scratch/D3/launcher_probe.sh
set -u
src=run-codex.sh
body=$(sed -e '2d' -e 's/^exec omp /omp_stub /' "$src")
omp_stub() {
  local cwd="" prompt_len=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --cwd) cwd="$2"; shift 2 ;;
      --append-system-prompt) prompt_len=${#2}; shift 2 ;;
      *) shift ;;
    esac
  done
  echo "omp would get: --cwd=$cwd (exists: $([ -d "$cwd" ] && echo yes || echo no))"
  echo "identity prompt length: $prompt_len chars (codex AGENTS.md in this clone: $(wc -c < .agent/coders/codex/AGENTS.md) chars)"
  echo "FIRECRAWL_API_KEY set: ${FIRECRAWL_API_KEY:+yes}${FIRECRAWL_API_KEY:-no}" | sed 's/yes.*/yes/'
  echo "VIRTUAL_ENV: ${VIRTUAL_ENV:-<unset>}"
}
export -f omp_stub
bash -c "$(declare -f omp_stub); $body" 2>&1
echo "launcher exit: $?"
echo "API.md tracked in git: $(git ls-files --error-unmatch _skills/firecrawl-web-scraping-search/API.md >/dev/null 2>&1 && echo yes || echo no)"
