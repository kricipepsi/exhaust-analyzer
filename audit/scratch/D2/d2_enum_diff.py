"""D2 probe — mechanical diff of enum / Literal value sets: design docs vs code.

Run from the repo root:
    python audit/scratch/D2/d2_enum_diff.py [comlab|gaslab]

Doc side: every ``class <Name>(StrEnum):`` block inside a fenced code block of the
lab's design / vocabulary docs, member lines ``NAME = "VALUE"``; plus every
``<Name>Lit = Literal[...]`` alias in the docs.
Code side: the same class name / alias name parsed by AST from the lab package
(and, for classes the lab does not define, from the owning sibling lab).
Output: one line per (doc anchor, class) with values only-in-doc / only-in-code.
Read-only; prints to stdout.
"""
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

DOCS = {
    "comlab": [
        "labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md",
        "labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md",
        "labs/comlab/docs/Vocabulary/DTC_VOCABULARY.md",
        "labs/comlab/docs/COMLab_LLD.md",
        "labs/comlab/docs/COMLab_HLD.md",
    ],
    "gaslab": [],  # filled in main() from labs/gaslab/docs + GAS_VOCABULARY
}
CODE_PKGS = {
    "comlab": ["labs/comlab/comlab"],
    "gaslab": ["labs/gaslab/gaslab"],
}
SIBLING_PKGS = ["labs/dtclab/dtclab", "labs/obdlab/obdlab", "labs/gaslab/gaslab",
                "labs/comlab/comlab", "labs/comlab/registry"]

CLASS_RE = re.compile(r"^\s*class\s+(\w+)\((?:str,\s*)?(?:StrEnum|Enum|str)\)\s*:")
MEMBER_RE = re.compile(r"^\s+([A-Z][A-Z0-9_]*)\s*=\s*\"([^\"]*)\"")
LIT_RE = re.compile(r"^\s*(\w+Lit)\s*=\s*Literal\[")


def doc_enums(path: Path):
    """Yield (name, lineno, values) for enum classes and Literal aliases in fenced code."""
    lines = path.read_text(encoding="utf-8").splitlines()
    in_code = False
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            m = CLASS_RE.match(ln)
            if m:
                name, start, vals = m.group(1), i + 1, []
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith("```"):
                    if CLASS_RE.match(lines[j]) or re.match(r"^\S", lines[j]):
                        break
                    mm = MEMBER_RE.match(lines[j])
                    if mm:
                        vals.append(mm.group(2))
                    j += 1
                if vals:
                    yield name, start, vals
                i = j
                continue
            m = LIT_RE.match(ln)
            if m:
                name, start = m.group(1), i + 1
                buf = ln
                j = i
                while buf.count("[") > buf.count("]") and j + 1 < len(lines):
                    j += 1
                    buf += lines[j]
                yield name, start, re.findall(r"\"([^\"]*)\"", buf.split("Literal", 1)[1])
                i = j + 1
                continue
        i += 1


def code_enums(pkg_dirs):
    """Return {name: [(path:line, values)]} for StrEnum classes + *Lit Literal aliases."""
    out: dict[str, list] = {}
    for d in pkg_dirs:
        for py in sorted((ROOT / d).rglob("*.py")):
            if "/tests/" in str(py) or "__pycache__" in str(py):
                continue
            try:
                tree = ast.parse(py.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            rel = py.relative_to(ROOT)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and any(
                    getattr(b, "id", getattr(b, "attr", "")) in ("StrEnum", "Enum", "str")
                    for b in node.bases
                ):
                    vals = [
                        st.value.value
                        for st in node.body
                        if isinstance(st, ast.Assign)
                        and isinstance(st.value, ast.Constant)
                        and isinstance(st.value.value, str)
                    ]
                    if vals:
                        out.setdefault(node.name, []).append((f"{rel}:{node.lineno}", vals))
                if isinstance(node, ast.Assign) and len(node.targets) == 1:
                    t = node.targets[0]
                    if isinstance(t, ast.Name) and t.id.endswith("Lit"):
                        src = ast.get_source_segment(py.read_text(encoding="utf-8"), node.value) or ""
                        if src.startswith("Literal"):
                            out.setdefault(t.id, []).append(
                                (f"{rel}:{node.lineno}", re.findall(r"\"([^\"]*)\"", src))
                            )
    return out


def main() -> None:
    lab = sys.argv[1] if len(sys.argv) > 1 else "comlab"
    docs = DOCS[lab]
    if lab == "gaslab":
        docs = [str(p.relative_to(ROOT)) for p in sorted((ROOT / "labs/gaslab/docs").rglob("*.md"))]
    own = code_enums(CODE_PKGS[lab])
    sib = code_enums(SIBLING_PKGS)
    ndiff = 0
    for d in docs:
        for name, line, vals in doc_enums(ROOT / d):
            cands = own.get(name) or sib.get(name)
            if not cands:
                print(f"NO-CODE  {d}:{line} {name} ({len(vals)} values) — no class/alias of that name in code")
                ndiff += 1
                continue
            for cpath, cvals in cands:
                only_doc = [v for v in vals if v not in cvals]
                only_code = [v for v in cvals if v not in vals]
                tag = "OK     " if not (only_doc or only_code) else "DIFF   "
                if only_doc or only_code:
                    ndiff += 1
                print(f"{tag} {d}:{line} {name} doc={len(vals)} code={len(cvals)} @ {cpath}"
                      + (f" only_doc={only_doc}" if only_doc else "")
                      + (f" only_code={only_code}" if only_code else ""))
    print(f"\nTOTAL DIFF/NO-CODE lines: {ndiff}")


if __name__ == "__main__":
    main()
