#!/usr/bin/env bash
# D3 probe: dry-run the editable-install half of the 4DLab_CLAUDE.md "Build recipe" (lines 202-206)
# on this clone. --dry-run --offline --no-deps: installs nothing, needs no network.
# Usage (from repo root): bash audit/scratch/D3/recipe_probe.sh [python]
PY=${1:-/home/claude/venv4d/bin/python}
echo "== recipe as documented (4DLab_CLAUDE.md:204-205)"
uv pip install --dry-run --offline --no-deps --python "$PY" \
  -e apps/wiredV2 -e labs/comlab -e labs/dnalab -e labs/dtclab \
  -e labs/gaslab -e labs/obdlab -e labs/symptomlab -e labs/vinlab 2>&1 | grep -v UV_NATIVE_TLS
echo "exit=${PIPESTATUS[0]}"
echo "== same recipe with apps/wired"
uv pip install --dry-run --offline --no-deps --python "$PY" \
  -e apps/wired -e labs/comlab -e labs/dnalab -e labs/dtclab \
  -e labs/gaslab -e labs/obdlab -e labs/symptomlab -e labs/vinlab 2>&1 | grep -v UV_NATIVE_TLS | tail -2
echo "exit=${PIPESTATUS[0]}"
