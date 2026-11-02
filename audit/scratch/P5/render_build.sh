#!/usr/bin/env bash
# P5: rebuild the Render service exactly as render.yaml states it, in a fresh venv holding nothing else.
#   PYTHON_VERSION 3.14.3 · buildCommand `pip install -r requirements.txt` · tree = `git archive origin/main`
# usage (repo root): bash audit/scratch/P5/render_build.sh <outdir>
set -euo pipefail
OUT=${1:?outdir}
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.14.3 >/dev/null
PY=$(uv python find 3.14.3)
rm -rf "$OUT" && mkdir -p "$OUT"
git archive origin/main | tar -x -C "$OUT"
cd "$OUT"
"$PY" -m venv .venv                       # Render: fresh virtualenv per build
.venv/bin/python -m pip install -r requirements.txt   # buildCommand, unmodified
.venv/bin/python -m pip freeze --all
