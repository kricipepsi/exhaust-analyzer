#!/usr/bin/env bash
# Run the planted controls through the same coverage + classifier path and check every expectation.
# Usage (repo root, venv active): bash audit/scratch/P3/controls/run_controls.sh <outdir>
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel); OUT=${1:?outdir}; P3="$ROOT/audit/scratch/P3"; C="$P3/controls/suite"
mkdir -p "$OUT"; rm -f "$OUT/.coverage.ctl"
( cd "$C" && COVERAGE_CORE=ctrace COVERAGE_FILE="$OUT/.coverage.ctl" P3_NODEIDS_OUT="$OUT/nodeids_ctl.json" \
  PYTHONPATH="$C:$P3" python -m pytest -q --no-header -p no:cacheprovider -p p3_nodeids \
  --cov-config="$P3/coveragerc" --cov-branch --cov-context=test --cov-report= \
  --cov="$C/p3ctl" --cov="$C/tests" | tail -1 )
python "$P3/reachability.py" "$OUT" "$OUT/controls.json" controls
python - "$OUT/controls.json" <<'PY'
import json, sys
sys.path.insert(0, "audit/scratch/P3")
from controls.spec import EXPECT_CLASS
d = json.load(open(sys.argv[1]))
ok = True
for k, t in sorted(d["tests"].items()):
    name = k.rsplit("::", 1)[1]
    exp = EXPECT_CLASS[name]
    good = t["class"] == exp
    ok &= good
    print(f"{'PASS' if good else 'FAIL'} {name}: got {t['class']} expected {exp} ({t['reason']})")
f = d["functions"]
nc = [v for k, v in f.items() if k.endswith("::never_called")][0]
vd = [v for k, v in f.items() if k.endswith("::verdict")][0]
br = [v for k, v in d["verdict_branches"].items() if k.endswith("::verdict")][0]
checks = [("never_called unreached (positive)", not nc["reached"]), ("verdict reached (clean)", vd["reached"]),
          ("x<0 branch listed untaken (positive)", any(a[0] == 8 for a in br["missing_branch_arcs"])),
          ("x>10 branch not listed (clean)", not any(a[0] == 6 for a in br["missing_branch_arcs"]))]
for n, g in checks:
    ok &= g
    print(f"{'PASS' if g else 'FAIL'} {n}")
print("CONTROLS", "ALL PASS" if ok else "FAILED")
PY
