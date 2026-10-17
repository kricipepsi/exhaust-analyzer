#!/usr/bin/env bash
# Audit environment for a cloud or local Linux session: Python 3.14 venv with the labs installed editable.
# Usage (repo root): bash audit/tools/setup.sh   then   source .venv-audit/bin/activate
set -euo pipefail
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv python install 3.14
uv venv -p 3.14 .venv-audit
# shellcheck disable=SC1091
source .venv-audit/bin/activate
uv pip install -r requirements.txt pytest hypothesis radon opentelemetry-api opentelemetry-sdk
python --version
