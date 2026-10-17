#!/usr/bin/env bash
# Round-0 baseline (read-only): per-package pytest last line, erosion census, isolation scan.
# Usage (repo root, venv active): bash audit/tools/baseline.sh > audit/reports/baseline_$(date +%Y%m%d).txt
set -uo pipefail
PKGS="labs/comlab labs/dnalab labs/dtclab labs/gaslab labs/obdlab labs/symptomlab labs/vinlab apps/wired"
echo "## git"; git log -1 --format='%h %ad %s' --date=iso
echo "## pytest (per package, collection errors continue)"
for d in $PKGS; do
  r=$(cd "$d" && timeout 600 python -m pytest -q --no-header -p no:cacheprovider --continue-on-collection-errors 2>&1 | tail -1)
  printf '%-16s %s\n' "$d" "$r"
done
echo "## erosion"
python audit/tools/erosion.py $PKGS apps/ui
echo "## isolation"
python audit/tools/isolation.py
