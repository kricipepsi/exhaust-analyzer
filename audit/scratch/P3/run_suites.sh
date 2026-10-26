#!/usr/bin/env bash
# P3 reachability: run every package suite under coverage.py with per-test contexts.
# Usage (repo root, .venv-audit active): bash audit/scratch/P3/run_suites.sh <outdir>
# Every run measures ALL production dirs (so cross-package reach is visible); classification
# later restricts "own package" lines. labs/comlab is on PYTHONPATH (F-C1-5 workaround).
# COVERAGE_CORE=ctrace: the 3.14 default (sysmon) disables a line after its first hit, so per-test contexts would be lost.
set -uo pipefail
ROOT=$(git rev-parse --show-toplevel)
OUT=${1:?outdir}
mkdir -p "$OUT"
P3="$ROOT/audit/scratch/P3"
SRC="$ROOT/labs/comlab/comlab,$ROOT/labs/comlab/registry,$ROOT/labs/dnalab/dnalab,$ROOT/labs/dtclab/dtclab,$ROOT/labs/gaslab/gaslab,$ROOT/labs/obdlab/obdlab,$ROOT/labs/symptomlab/symptomlab,$ROOT/labs/vinlab/vinlab,$ROOT/apps/wired/wired,$ROOT/apps/ui"
# test dirs are measured too, so the classifier counts only assertions that actually executed
TST="$ROOT/labs/comlab/tests,$ROOT/labs/comlab/registry/tests,$ROOT/labs/dnalab/tests,$ROOT/labs/dtclab/tests,$ROOT/labs/gaslab/tests,$ROOT/labs/obdlab/tests,$ROOT/labs/symptomlab/tests,$ROOT/labs/vinlab/tests,$ROOT/apps/wired/tests,$ROOT/apps/ui/tests"
# key|suite dir|pytest args. "registry" is labs/comlab/registry/tests: excluded by labs/comlab testpaths=["tests"],
# so no baseline run collects it; it is measured here as a separate (orphan) suite.
for spec in comlab\|labs/comlab\| dnalab\|labs/dnalab\| dtclab\|labs/dtclab\| gaslab\|labs/gaslab\| obdlab\|labs/obdlab\| \
            symptomlab\|labs/symptomlab\| vinlab\|labs/vinlab\| wired\|apps/wired\| ui\|apps/ui\| registry\|labs/comlab\|registry/tests; do
  IFS='|' read -r key d targs <<<"$spec"
  rm -f "$OUT/.coverage.$key"
  ( cd "$ROOT/$d" && COVERAGE_CORE=ctrace COVERAGE_FILE="$OUT/.coverage.$key" P3_NODEIDS_OUT="$OUT/nodeids_$key.json" \
    PYTHONPATH="$ROOT/labs/comlab:$P3${PYTHONPATH:+:$PYTHONPATH}" \
    timeout 1200 python -m pytest -q --no-header -p no:cacheprovider -p p3_nodeids \
      --continue-on-collection-errors --cov-config="$P3/coveragerc" \
      --cov-branch --cov-context=test --cov-report= $targs \
      $(for s in ${SRC//,/ } ${TST//,/ }; do printf -- '--cov=%s ' "$s"; done) 2>&1 | tail -1 ) | sed "s|^|$key: |"
done
