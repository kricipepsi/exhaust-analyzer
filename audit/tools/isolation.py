"""Lab-isolation scan (AGENTS.md rule 5): cross-lab Python imports under labs/ (read-only).

Sanctioned exception: dnalab -> vinlab + symptomlab (labs/dnalab/docs/ADR_DNALab.md ADR-0002).
Usage: python audit/tools/isolation.py   (run from the repo root)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

LABS = {"comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab"}
FOREIGN = LABS | {"wired", "fl_tasks", "v7"}
SANCTIONED = {("dnalab", "vinlab"), ("dnalab", "symptomlab")}


def main() -> int:
    bad = 0
    for lab in sorted(LABS):
        for p in sorted(Path("labs", lab).rglob("*.py")):
            if {"research", "graph"} & set(p.parts) or any(x.startswith(".venv") for x in p.parts):
                continue
            try:
                tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
            except SyntaxError:
                continue
            for n in ast.walk(tree):
                if isinstance(n, ast.Import):
                    mods = [a.name for a in n.names]
                elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                    mods = [n.module]
                else:
                    continue
                for m in mods:
                    top = m.split(".")[0]
                    if top in FOREIGN and top != lab and (lab, top) not in SANCTIONED:
                        bad += 1
                        print(f"{p}:{n.lineno}\t{lab} -> {m}")
    print(f"violations: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
