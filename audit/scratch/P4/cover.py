"""Step 1: line coverage of each target function under its owning suite, measured inside a clean copy.

Usage (repo root, venv active): python audit/scratch/P4/cover.py <workdir>
Writes audit/scratch/P4/coverage_lines.json (deterministic: sorted keys and lines, no timings).
"""

from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_config import SCRATCH, SUITES, TARGETS  # noqa: E402
from p4_lib import make_copy, run_suite  # noqa: E402


def func_range(path: Path, qualname: str) -> tuple[int, int]:
    tree = ast.parse(path.read_text())
    parts = qualname.split(".")
    body = tree.body
    node = None
    for p in parts:
        node = next(n for n in body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == p)
        body = node.body
    assert node is not None
    return node.lineno, node.end_lineno or node.lineno


def main() -> None:
    work = Path(sys.argv[1])
    root = make_copy(work / "cov")
    out: dict = {}
    for suite in SUITES:
        files = sorted({t[0] for t in TARGETS.values() if t[2] == suite})
        data = work / f"cov_{suite}.data"
        data.unlink(missing_ok=True)
        res = run_suite(root, suite, 1200, cov_include=[str(root / f) for f in files], cov_data=data)
        jpath = work / f"cov_{suite}.json"
        subprocess.run([sys.executable, "-m", "coverage", "json", f"--data-file={data}", "-o", str(jpath),
                        "-q"], check=True)
        cj = json.loads(jpath.read_text())["files"]
        for tid, (f, qn, s, _m) in sorted(TARGETS.items()):
            if s != suite:
                continue
            a, b = func_range(root / f, qn)
            rec = next(v for k, v in cj.items() if k.endswith(f))
            ex = sorted(x for x in rec["executed_lines"] if a <= x <= b)
            miss = sorted(x for x in rec["missing_lines"] if a <= x <= b)
            out[tid] = {"file": f, "qualname": qn, "suite": suite, "def_lines": [a, b],
                        "executed": ex, "missing": miss,
                        "stmt_coverage": round(len(ex) / max(1, len(ex) + len(miss)), 4),
                        "suite_summary": res["summary"].split(" in ")[0],
                        "guard_ok": res["state"].get("guard_ok")}
    (SCRATCH / "coverage_lines.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for k, v in sorted(out.items()):
        print(f"{k:28s} stmts={len(v['executed'])+len(v['missing']):4d} exec={len(v['executed']):4d} "
              f"cov={v['stmt_coverage']:.2f} suite='{v['suite_summary']}' guard={v['guard_ok']}")


if __name__ == "__main__":
    main()
