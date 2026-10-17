"""SlopCodeBench-style erosion census for 4DLab (read-only).

erosion   = share of complexity mass CC*sqrt(SLOC) held by functions with CC > 10
            (SlopCodeBench, arXiv 2603.24755, eq. 2-4).
clone     = share of lines inside duplicated 4-statement windows (normalised AST dump).
Reduced variant: no ast-grep rule set, so values compare only within this tool.

Usage: python audit/tools/erosion.py [--json out.json] PATH [PATH ...]
Needs: radon (pip install radon). Excludes tests/, research/, graph/, .venv*, __pycache__.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

from radon.complexity import cc_visit
from radon.raw import analyze

SKIP = ("tests", "test", "research", "graph", "__pycache__", "graphify-out")


def py_files(root: Path):
    for p in sorted(root.rglob("*.py")):
        parts = set(p.parts)
        if parts & set(SKIP) or any(x.startswith(".venv") for x in p.parts) or p.name.startswith("test_"):
            continue
        yield p


def windows(tree: ast.AST, size: int = 4):
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list) or len(body) < size:
            continue
        for i in range(len(body) - size + 1):
            stmts = body[i:i + size]
            key = hashlib.sha1("".join(ast.dump(s, annotate_fields=False) for s in stmts).encode()).hexdigest()
            lines = set()
            for s in stmts:
                lines.update(range(s.lineno, (s.end_lineno or s.lineno) + 1))
            yield key, lines


def census(root: Path) -> dict:
    mass_all = mass_hot = 0.0
    loc = 0
    funcs = []
    seen = defaultdict(list)
    for f in py_files(root):
        src = f.read_text(encoding="utf-8", errors="replace")
        try:
            tree = ast.parse(src)
            blocks = cc_visit(src)
        except SyntaxError:
            continue
        loc += analyze(src).sloc
        for b in blocks:
            if not hasattr(b, "endline"):
                continue
            sloc = max(1, b.endline - b.lineno + 1)
            m = b.complexity * math.sqrt(sloc)
            mass_all += m
            if b.complexity > 10:
                mass_hot += m
            funcs.append((b.complexity, sloc, f"{f.relative_to(root)}:{b.lineno} {b.name}"))
        for key, lines in windows(tree):
            seen[key].append((f, lines))
    clone_lines = set()
    for occ in seen.values():
        if len(occ) > 1:
            for f, lines in occ:
                clone_lines.update((str(f), ln) for ln in lines)
    funcs.sort(reverse=True)
    return {
        "path": str(root), "sloc": loc, "functions": len(funcs),
        "cc_gt_10": sum(1 for c, _, _ in funcs if c > 10),
        "erosion": round(mass_hot / mass_all, 3) if mass_all else None,
        "clone_share": round(len(clone_lines) / loc, 3) if loc else None,
        "worst": [{"cc": c, "sloc": s, "where": w} for c, s, w in funcs[:8]],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json")
    a = ap.parse_args()
    rows = [census(Path(p)) for p in a.paths]
    for r in rows:
        print(f"{r['path']:<28} sloc={r['sloc']:>6} funcs={r['functions']:>5} cc>10={r['cc_gt_10']:>4} "
              f"erosion={r['erosion']} clone={r['clone_share']}")
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
