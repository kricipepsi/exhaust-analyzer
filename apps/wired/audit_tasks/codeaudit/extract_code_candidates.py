"""T-AUD-22: list the numeric literals of one lab group's production code and data files (Cowork tool).

python -I extract_code_candidates.py --group gaslab|comlab|rest
Writes candidates_<group>.csv beside this file: one row per source line that holds a numeric literal.
- .py files: literals found by ast (int/float constants). A line whose literals are all trivial (-1, 0, 1, 2), a
  subscript index, a range() argument or round()'s digits gets auto=NON_DOMAIN.
- data files (.json, .yaml, .csv the code loads): one row per digit-bearing line; a line whose digits sit only in
  ids, dates, versions or section references gets auto=NON_DOMAIN.
Tests, task packs, graph caches, docs and wikis are not production code and are not listed.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
GROUPS = {
    "gaslab": {"py": ["labs/gaslab/gaslab"], "data": []},  # the ontology is T-GASA-16's (wikiaudit register)
    "comlab": {"py": ["labs/comlab/comlab", "labs/comlab/registry"],
               "data": ["labs/comlab/comlab/config", "labs/comlab/registry/rules"]},
    "rest": {"py": ["labs/obdlab/obdlab", "labs/dtclab/dtclab", "labs/dnalab", "labs/symptomlab", "apps/wired/v7",
                    "apps/wired/wired", "apps/ui"],
             "data": ["labs/dtclab/dtclab/config", "labs/obdlab/obdlab", "labs/symptomlab"]},
}
SKIP_PARTS = {"tests", "test", "audit_tasks", "tasks", "scratch", "graph", "docs", "wiki", "__pycache__", "research",
              "fl_tasks", "reports"}
TRIVIAL = {-1, 0, 1, 2}
DATA_NON_DOMAIN = re.compile("|".join([
    r"\b(?:F|T|R)-[A-Z0-9]+(?:-[A-Za-z0-9]+)*", r"\bADR-\d+\b", r"\b20\d\d-\d\d-\d\d(?:T[\d:.]+Z?)?\b",
    r"\bv\d+(?:\.\d+)*\b", r"§\s*\d+(?:\.\d+)*", r"\b[A-Z]{2,}[-_]\d+[A-Z]?\b", r"\b[PBCU][0-9A-F]{4}\b",
    r"\"version\"\s*:\s*\"?[\d.]+\"?", r"^\s*#.*$",
]))


def skip(rel: Path) -> bool:
    return any(p in SKIP_PARTS or p.endswith(".egg-info") for p in rel.parts[:-1]) or rel.name.startswith("test_") \
        or rel.name == "conftest.py"


def py_rows(path: Path) -> list[tuple[int, bool]]:
    """(line, all_trivial) for every line holding a numeric literal."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    exempt: set[int] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Subscript):
            for c in ast.walk(n.slice):
                exempt.add(id(c))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("range", "round"):
            args = n.args if n.func.id == "range" else n.args[1:]
            for a in args:
                exempt.add(id(a))
    lines: dict[int, bool] = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and type(n.value) in (int, float):
            trivial = (type(n.value) is int and n.value in TRIVIAL) or id(n) in exempt
            lines[n.lineno] = lines.get(n.lineno, True) and trivial
    return sorted(lines.items())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", choices=sorted(GROUPS), required=True)
    g = GROUPS[ap.parse_args().group]
    rows: list[dict[str, object]] = []

    def add(rel: str, n: int, text: str, auto: bool) -> None:
        rows.append({"cand_id": f"K{len(rows) + 1:04d}", "file": rel, "line": n,
                     "sha": hashlib.sha1(text.encode("utf-8")).hexdigest()[:10],
                     "auto": "NON_DOMAIN" if auto else "", "text": text.strip()})

    for root in g["py"]:
        for p in sorted((REPO / root).rglob("*.py")):
            rel = p.relative_to(REPO)
            if skip(rel):
                continue
            src = p.read_text(encoding="utf-8").splitlines()
            for n, trivial in py_rows(p):
                add(rel.as_posix(), n, src[n - 1], trivial)
    for root in g["data"]:
        for p in sorted((REPO / root).rglob("*")):
            rel = p.relative_to(REPO)
            if p.suffix not in (".json", ".yaml", ".yml", ".csv") or skip(rel):
                continue
            for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if re.search(r"\d", line):
                    add(rel.as_posix(), n, line, not re.search(r"\d", DATA_NON_DOMAIN.sub(" ", line)))
    out = HERE / f"candidates_{ap.parse_args().group}.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["cand_id", "file", "line", "sha", "auto", "text"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    auto = sum(1 for r in rows if r["auto"])
    files = len({r["file"] for r in rows})
    print(f"files {files} candidates {len(rows)} auto_non_domain {auto} to_classify {len(rows) - auto}")


if __name__ == "__main__":
    main()
