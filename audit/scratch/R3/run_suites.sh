#!/usr/bin/env bash
# Run every package suite in tree $1 (default: repo root), write per-test outcomes to $2 (TSV: pkg nodeid outcome).
# Lab sources of tree $1 are put first on PYTHONPATH so a worktree does not import the editable (tip) installs.
set -uo pipefail
ROOT=$(cd "${1:-.}" && pwd); OUT=$2
PKGS="labs/comlab labs/dnalab labs/dtclab labs/gaslab labs/obdlab labs/symptomlab labs/vinlab apps/wired apps/ui"
PP=""; for d in $PKGS; do PP="$PP:$ROOT/$d"; done
: > "$OUT"
for d in $PKGS; do
  (cd "$ROOT/$d" && PYTHONPATH="${PP#:}" timeout 900 python -m pytest -q -rA --no-header -p no:cacheprovider \
     --continue-on-collection-errors 2>&1) > "$OUT.$(basename $d).log"
  grep -E '^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS) ' "$OUT.$(basename $d).log" \
    | sed -E 's/^(\w+) ([^ ]+).*/\1\t\2/' | awk -v p="$d" -F'\t' '{print p"\t"$2"\t"$1}' >> "$OUT"
  echo "$d: $(tail -1 "$OUT.$(basename $d).log")"
done
