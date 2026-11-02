"""List SURVIVED / KILLED-WRONG-REASON / TIMEOUT mutants from a matrix JSON, grouped by target and line.

Usage: python audit/scratch/P4/survivors.py audit/scratch/P4/matrix.json [target]
"""

from __future__ import annotations

import json
import sys

m = json.load(open(sys.argv[1]))
only = sys.argv[2] if len(sys.argv) > 2 else None
for tid, t in sorted(m["targets"].items()):
    if only and tid != only:
        continue
    print(f"== {tid} {t['counts']} by_op={t['by_op']}")
    for r in t["mutants"]:
        if r["outcome"] != "KILLED":
            extra = f" crash={r['crash_tests'][:2]}" if r["outcome"] == "KILLED-WRONG-REASON" else ""
            print(f"  {r['id']:32s} L{r['line']:<5d} {r['op']:5s} {r['outcome']:20s} "
                  f"{r['original'][:60]!r} -> {r['replacement'][:60]!r}{extra}")
