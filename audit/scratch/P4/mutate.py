"""Step 2: AST mutant census over the executed lines of each target function.

Operators (one condition / one site per mutant):
  CMP   comparison flip (one op of a chained compare): < >=, <= >, > <=, >= <, == !=, in / not in, is / is not
  NUM   numeric boundary: int +1 / -1, float +1 ulp / -1 ulp (math.nextafter)
  BOOL  and/or swap at one junction of a BoolOp
  RET   constant return: `return <expr>` -> `return None` (bool constant -> its negation)
  GUARD delete a single-condition exit guard (`if <c>:` ending in return/raise/continue/break, no else)
  ENUM  swap an Enum member attribute for the next member of the same Enum
A site is eligible only if its enclosing statement's first line is in coverage_lines.json "executed".
Blind spots: string-literal enum values (bare "LEAN" strings) are not mutated; a short-circuited
operand on an executed line counts as executed.

Usage: python audit/scratch/P4/mutate.py   -> audit/scratch/P4/mutants.json (deterministic)
"""

from __future__ import annotations

import ast
import enum
import importlib
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_config import LAB_PATHS, REPO, SAMPLE_CAP, SCRATCH, SEED, TARGETS  # noqa: E402

for p in [*LAB_PATHS, "apps/ui"]:
    sys.path.insert(0, str(REPO / p))

CMP_FLIP = {ast.Lt: ast.GtE, ast.LtE: ast.Gt, ast.Gt: ast.LtE, ast.GtE: ast.Lt, ast.Eq: ast.NotEq,
            ast.NotEq: ast.Eq, ast.In: ast.NotIn, ast.NotIn: ast.In, ast.Is: ast.IsNot, ast.IsNot: ast.Is}
EXITS = (ast.Return, ast.Raise, ast.Continue, ast.Break)


def find_func(tree: ast.Module, qualname: str) -> ast.FunctionDef:
    body, node = tree.body, None
    for part in qualname.split("."):
        node = next(n for n in body if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == part)
        body = node.body
    assert isinstance(node, ast.FunctionDef)
    return node


def parent_map(root: ast.AST) -> dict[ast.AST, ast.AST]:
    return {c: p for p in ast.walk(root) for c in ast.iter_child_nodes(p)}


def enclosing_stmt(node: ast.AST, parents: dict) -> ast.stmt:
    while not isinstance(node, ast.stmt):
        node = parents[node]
    return node


def in_fstring(node: ast.AST, parents: dict) -> bool:
    while node in parents:
        node = parents[node]
        if isinstance(node, ast.JoinedStr):
            return True
    return False


def dotted(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f"{base}.{node.attr}" if base else None
    return None


def resolve_enum(expr: str, mod) -> enum.Enum | None:
    obj = mod.__dict__
    parts = expr.split(".")
    try:
        cur = obj[parts[0]]
        for p in parts[1:]:
            cur = getattr(cur, p)
    except (KeyError, AttributeError):
        return None
    return cur if isinstance(cur, enum.Enum) else None


def seg(src_lines: list[bytes], n: ast.AST) -> str:
    """Exact source text of node n (utf-8 byte columns)."""
    if n.lineno == n.end_lineno:
        return src_lines[n.lineno - 1][n.col_offset:n.end_col_offset].decode()
    parts = [src_lines[n.lineno - 1][n.col_offset:]]
    parts += src_lines[n.lineno:n.end_lineno - 1]
    parts.append(src_lines[n.end_lineno - 1][:n.end_col_offset])
    return b"".join(parts).decode()


def census(tid: str) -> tuple[list[dict], dict]:
    f, qn, suite, modname = TARGETS[tid]
    cov = json.loads((SCRATCH / "coverage_lines.json").read_text())[tid]
    executed = set(cov["executed"])
    src = (REPO / f).read_bytes()
    src_lines = src.splitlines(keepends=True)
    tree = ast.parse(src)
    fn = find_func(tree, qn)
    parents = parent_map(tree)
    mod = importlib.import_module(modname)
    muts: list[dict] = []
    skipped_unexecuted = 0

    def add(node: ast.AST, op: str, repl: str, note: str = "") -> None:
        nonlocal skipped_unexecuted
        st = enclosing_stmt(node, parents) if not isinstance(node, ast.stmt) else node
        if st.lineno not in executed:
            skipped_unexecuted += 1
            return
        muts.append({"target": tid, "file": f, "suite": suite, "op": op, "line": node.lineno,
                     "col": node.col_offset, "start": [node.lineno, node.col_offset],
                     "end": [node.end_lineno, node.end_col_offset], "original": seg(src_lines, node),
                     "replacement": repl, "note": note})

    for node in ast.walk(fn):
        if node is fn or in_fstring(node, parents):
            continue
        if isinstance(node, ast.Compare):
            for i, op in enumerate(node.ops):
                new = ast.Compare(left=node.left, ops=list(node.ops), comparators=node.comparators)
                new.ops[i] = CMP_FLIP[type(op)]()
                add(node, "CMP", "(" + ast.unparse(new) + ")", f"op{i}")
        elif isinstance(node, ast.Constant) and type(node.value) in (int, float):
            v = node.value
            if isinstance(v, int):
                vs = [v + 1, v - 1]
            else:
                vs = [math.nextafter(v, math.inf), math.nextafter(v, -math.inf)]
            for nv in vs:
                add(node, "NUM", "(" + repr(nv) + ")", f"{v!r}->{nv!r}")
        elif isinstance(node, ast.BoolOp):
            other = ast.Or if isinstance(node.op, ast.And) else ast.And
            for k in range(1, len(node.values)):
                grouped = ast.BoolOp(op=other(), values=[node.values[k - 1], node.values[k]])
                vals = node.values[:k - 1] + [grouped] + node.values[k + 1:]
                new = grouped if len(vals) == 1 else ast.BoolOp(op=type(node.op)(), values=vals)
                add(node, "BOOL", "(" + ast.unparse(new) + ")", f"junction{k}")
        elif isinstance(node, ast.Return) and node.value is not None:
            v = node.value
            if isinstance(v, ast.Constant) and isinstance(v.value, bool):
                add(v, "RET", repr(not v.value), "bool-negate")
            elif not (isinstance(v, ast.Constant) and v.value is None):
                add(v, "RET", "None", "const-None")
        elif (isinstance(node, ast.If) and not node.orelse and isinstance(node.body[-1], EXITS)
              and not isinstance(node.test, ast.BoolOp) and seg(src_lines, node).startswith("if")):
            # compound guards are covered per condition by CMP/BOOL, never deleted whole
            add(node, "GUARD", "pass", "delete-guard")
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Load):
            d = dotted(node)
            m = resolve_enum(d, mod) if d else None
            if m is not None:
                members = list(type(m))
                if len(members) > 1:
                    nxt = members[(members.index(m) + 1) % len(members)]
                    base = d.rsplit(".", 1)[0]
                    add(node, "ENUM", f"{base}.{nxt.name}", f"{m.name}->{nxt.name}")

    muts.sort(key=lambda m: (m["line"], m["col"], m["op"], m["note"]))
    seen, uniq = set(), []
    for m in muts:  # a node can be visited once only, but guard against identical text mutants
        key = (tuple(m["start"]), tuple(m["end"]), m["replacement"])
        if key not in seen:
            seen.add(key)
            uniq.append(m)
    for i, m in enumerate(uniq):
        m["id"] = f"{tid}#{i:04d}"
    pop = len(uniq)
    by_op: dict[str, int] = {}
    for m in uniq:
        by_op[m["op"]] = by_op.get(m["op"], 0) + 1
    sampled = uniq
    if pop > SAMPLE_CAP:
        sampled = sorted(random.Random(f"{SEED}:{tid}").sample(uniq, SAMPLE_CAP), key=lambda m: m["id"])
    meta = {"population": pop, "population_by_op": dict(sorted(by_op.items())),
            "sampled": len(sampled), "sample_seed": f"{SEED}:{tid}" if pop > SAMPLE_CAP else None,
            "sites_skipped_unexecuted": skipped_unexecuted}
    return sampled, meta


def main() -> None:
    allm, meta = [], {}
    for tid in sorted(TARGETS):
        ms, md = census(tid)
        allm += ms
        meta[tid] = md
        print(f"{tid:28s} population={md['population']:4d} sampled={md['sampled']:4d} "
              f"skipped_unexecuted={md['sites_skipped_unexecuted']:4d} {md['population_by_op']}")
    (SCRATCH / "mutants.json").write_text(
        json.dumps({"meta": meta, "mutants": allm}, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
