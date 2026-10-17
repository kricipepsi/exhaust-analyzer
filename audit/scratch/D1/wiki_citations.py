#!/usr/bin/env python3
"""D1 probe: resolve every `# wiki: §` citation and check its literal values.

Run from the repo root:
    python audit/scratch/D1/wiki_citations.py

Writes (all under audit/scratch/D1/out/):
    citations.tsv          one row per bare `# wiki: §` citation (the D1 population)
    citations_named.tsv    one row per `# wiki: <File>.md §` citation (extension, not in the 316)
    uncited_literals.tsv   threshold-shaped numeric literals in labs/*/<pkg>/ with no citation
    summary.json           totals

Citation grammar (worked out from the 316 lines, see report):
    "# wiki:" SP CITE { SP "/" SP CITE } [ SP NOTE ]
    CITE  := "§" SECNUM [ SP WORD ]          e.g. §6.4, §6.4 UNKNOWN, §4, §4.1
    NOTE  := ("—" | "-") free text           (free text may itself carry "§x" or "File.md §x")
    A bare "§" names no file. The governing document is the first one, walking out from the line,
    that is named in a docstring (innermost class/def -> module -> package __init__ chain) AND has
    the section; failing that, the citing lab's own labs/<lab>/wiki/*.md.
Section = a markdown heading whose first token is SECNUM ("## 6.", "### 6.4 ", "## 12.1 ..."), the
text runs to the next heading of the same or higher level (sub-sections included).
"""
from __future__ import annotations

import ast
import io
import json
import re
import subprocess
import sys
import tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "out"
EXCLUDE_DIRS = ("/Vault/", "/graph/", "/research/", "/_archive/", "/audit/", "/archive/", "/v2/", "/v6/")

NUM_RE = re.compile(r"(?<![\w.$])(\d+(?:\.\d+)?)(?![\w])")
HEAD_RE = re.compile(r"^(#{1,6})\s+(?:§\s*)?(\d+(?:\.\d+)*)\.?(?=\s|$)")
MD_NAME_RE = re.compile(r"([\w./-]+\.md)\b")
SEC_RE = re.compile(r"§\s*(\d+(?:\.\d+)*)")


# ---------------------------------------------------------------- markdown index
_md_cache: dict[Path, dict[str, str]] = {}


def sections(md: Path) -> dict[str, str]:
    if md in _md_cache:
        return _md_cache[md]
    lines = md.read_text(encoding="utf-8", errors="replace").splitlines()
    heads = []  # (idx, level, num)
    in_fence = False
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if ln.startswith("#"):
            m = HEAD_RE.match(ln)
            lvl = len(ln) - len(ln.lstrip("#"))
            heads.append((i, lvl, m.group(2) if m else None))
    out: dict[str, str] = {}
    for k, (i, lvl, num) in enumerate(heads):
        if num is None or num in out:
            continue
        end = len(lines)
        for j, l2, _ in heads[k + 1:]:
            if l2 <= lvl:
                end = j
                break
        out[num] = "\n".join(lines[i:end])
    _md_cache[md] = out
    return out


def all_md() -> list[Path]:
    res = []
    for p in (ROOT / "labs").rglob("*.md"):
        s = "/" + str(p.relative_to(ROOT)) + "/"
        if any(x in s for x in EXCLUDE_DIRS):
            continue
        res.append(p)
    return res


ALL_MD = all_md()


def find_doc(name: str, lab: str) -> tuple[Path | None, str]:
    """Resolve a doc name from a docstring/citation. Returns (path, how)."""
    base = Path(name).name
    cands = [p for p in ALL_MD if p.name == base]
    if not cands:
        return None, "missing"
    def rank(p: Path) -> tuple[int, int]:
        rel = str(p.relative_to(ROOT))
        exact = 0 if rel.endswith(name) else 1
        if rel.startswith(f"labs/{lab}/"):
            loc = 0
        elif rel.startswith("labs/comlab/docs/Vocabulary/"):
            loc = 1
        else:
            loc = 2
        return (loc, exact)
    cands.sort(key=rank)
    p = cands[0]
    how = "exact" if str(p.relative_to(ROOT)).endswith(name) else "basename"
    return p, how


def lab_wikis(lab: str) -> list[Path]:
    return sorted((ROOT / "labs" / lab / "wiki").glob("*.md"))


# ---------------------------------------------------------------- python helpers
def docstring_chain(py: Path, line: int) -> list[tuple[str, str]]:
    """[(level, docstring)] innermost first, then module, then package __init__ files."""
    tree = ast.parse(py.read_text(encoding="utf-8"))
    chain: list[tuple[str, str]] = []
    nodes = []
    for n in ast.walk(tree):
        if isinstance(n, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.lineno <= line <= (n.end_lineno or n.lineno):
                nodes.append(n)
    nodes.sort(key=lambda n: n.lineno, reverse=True)
    for n in nodes:
        d = ast.get_docstring(n)
        if d:
            chain.append((f"{type(n).__name__}:{n.name}", d))
    d = ast.get_docstring(tree)
    if d:
        chain.append(("module", d))
    # package __init__ chain up to the lab dir
    d_ = py.parent
    while (d_ / "__init__.py").exists():
        ip = d_ / "__init__.py"
        if ip != py:
            dd = ast.get_docstring(ast.parse(ip.read_text(encoding="utf-8")))
            if dd:
                chain.append((f"pkg:{ip.relative_to(ROOT)}", dd))
        d_ = d_.parent
    return chain


def literals_by_line(py: Path) -> dict[int, dict[str, list]]:
    src = py.read_text(encoding="utf-8")
    toks = list(tokenize.generate_tokens(io.StringIO(src).readline))
    out: dict[int, dict[str, list]] = {}
    # docstring token positions to skip
    tree = ast.parse(src)
    doc_lines = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
                doc_lines.update(range(n.body[0].lineno, (n.body[0].end_lineno or n.body[0].lineno) + 1))
    prev = None
    for t in toks:
        ln = t.start[0]
        if t.type == tokenize.NUMBER:
            neg = prev is not None and prev.type == tokenize.OP and prev.string == "-" and prev.start[0] == ln
            out.setdefault(ln, {"num": [], "str": []})["num"].append(("-" if neg else "") + t.string)
        elif t.type == tokenize.STRING and ln not in doc_lines:
            try:
                v = ast.literal_eval(t.string)
            except Exception:
                v = None
            if isinstance(v, str) and 2 <= len(v) <= 40 and " " not in v:
                out.setdefault(ln, {"num": [], "str": []})["str"].append(v)
        if t.type not in (tokenize.NL, tokenize.NEWLINE, tokenize.COMMENT, tokenize.INDENT, tokenize.DEDENT):
            prev = t
    return out


def to_float(s: str) -> float | None:
    try:
        return float(s.replace("_", ""))
    except ValueError:
        try:
            return float(int(s.replace("_", ""), 0))
        except ValueError:
            return None


def text_numbers(text: str) -> set[float]:
    t = text.replace("−", "-").replace("–", " ").replace("—", " ")
    return {float(m) for m in NUM_RE.findall(t)}


def num_present(v: float, nums: set[float]) -> str | None:
    a = abs(v)
    for n in nums:
        if abs(n - a) <= 1e-9 * max(1.0, a):
            return "exact"
    for n in nums:  # percent <-> fraction
        if a and (abs(n - a * 100) <= 1e-9 * max(1.0, a * 100) or abs(n * 100 - a) <= 1e-9 * max(1.0, a)):
            return "scaled"
    return None


# ---------------------------------------------------------------- citation parse
def parse_citation(comment: str) -> tuple[list[str], str]:
    body = comment.split("wiki:", 1)[1].strip()
    m = re.split(r"\s[—–]\s|\s-\s|\s—|—\s", body, maxsplit=1)
    head = m[0]
    note = m[1] if len(m) > 1 else ""
    secs = SEC_RE.findall(head)
    return secs, note


def resolve(lab: str, py: Path, line: int, secs: list[str], explicit: str | None = None):
    """Return dict with class, governing doc(s), resolution level, section text."""
    levels: list[tuple[str, list[Path], list[str]]] = []  # (level, docs, missing names)
    if explicit:
        p, how = find_doc(explicit, lab)
        levels.append((f"explicit({how})", [p] if p else [], [] if p else [explicit]))
    else:
        for lvl, d in docstring_chain(py, line):
            names = list(dict.fromkeys(MD_NAME_RE.findall(d)))
            if not names:
                continue
            docs, missing = [], []
            for nm in names:
                p, how = find_doc(nm, lab)
                if p and p not in docs:
                    docs.append(p)
                elif not p:
                    missing.append(nm)
            levels.append((lvl, docs, missing))
        levels.append(("lab-wiki", lab_wikis(lab), []))
    per_sec = {}
    any_doc = any(docs for _, docs, _ in levels)
    for s in secs:
        hit = None
        for lvl, docs, _ in levels:
            found = [d for d in docs if s in sections(d)]
            own = [d for d in found if str(d.relative_to(ROOT)).startswith(f"labs/{lab}/wiki/")]
            if len(found) > 1 and len(own) == 1:
                found = own  # a "wiki:" citation prefers the lab's own wiki/ when a docstring names both
            if found:
                hit = (lvl, found)
                break
        per_sec[s] = hit
    missing_names = sorted({m for _, _, ms in levels for m in ms})
    if not any_doc:
        cls = "UNRESOLVED_FILE"
    elif any(v is None for v in per_sec.values()):
        cls = "UNRESOLVED_SECTION"
    elif any(len(v[1]) > 1 for v in per_sec.values()):
        cls = "AMBIGUOUS"
    else:
        cls = "RESOLVED"
    text = ""
    gov = []
    for s, v in per_sec.items():
        if v:
            for d in v[1]:
                text += "\n" + sections(d)[s]
                gov.append(f"{d.relative_to(ROOT)}§{s}@{v[0]}")
    # shadow: the same section number also exists in the lab's own wiki/ in a different file
    shadow = []
    for s, v in per_sec.items():
        for w in lab_wikis(lab):
            if s in sections(w) and (not v or w not in v[1]):
                shadow.append(f"{w.relative_to(ROOT)}§{s}")
    return cls, gov, text, missing_names, shadow


def target_line(lines: list[str], i: int) -> int:
    """1-based line whose literals the citation on line i (1-based) governs."""
    def is_code(k: int) -> bool:  # k is 1-based
        if k < 1 or k > len(lines):
            return False
        s = lines[k - 1].strip()
        return bool(s) and not s.startswith("#")
    code = lines[i - 1].split("#", 1)[0]
    if code.strip():
        return i
    # comment-only citation: "comment above" if the very next line is code,
    # else "comment below" (payload.py / freeze_frame.py field style) if the previous line is code.
    if is_code(i + 1):
        return i + 1
    if is_code(i - 1):
        return i - 1
    j = i
    while j < len(lines):
        nxt = lines[j].strip()
        j += 1
        if nxt and not nxt.startswith("#"):
            return j
    return i


def run_population(pattern: str, explicit_mode: bool):
    cmd = ["grep", "-rn", pattern, "--include=*.py", "labs", "apps"]
    raw = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True).stdout.splitlines()
    rows = []
    lit_cache: dict[Path, dict] = {}
    for r in raw:
        path, ln, rest = r.split(":", 2)
        py = ROOT / path
        ln = int(ln)
        lab = path.split("/")[1] if path.startswith("labs/") else "apps"
        is_test = "/tests/" in path or Path(path).name.startswith("test_") or Path(path).name == "conftest.py"
        lines = py.read_text(encoding="utf-8").splitlines()
        full = lines[ln - 1]
        if "#" not in full or "wiki:" not in full.split("#", 1)[1] and "wiki:" not in full:
            continue
        comment = full[full.index("# wiki:"):] if "# wiki:" in full else full[full.index("wiki:"):]
        explicit = None
        if explicit_mode:
            m = re.match(r"#?\s*wiki:\s*([\w./-]+\.md)\s*§", comment.lstrip("# ").join(["", ""]) or comment)
            m = re.search(r"wiki:\s*([\w./-]+\.md)\s*§", comment)
            if not m:
                continue
            explicit = m.group(1)
            secs = SEC_RE.findall(comment.split("—")[0])
            note = comment.split("—", 1)[1] if "—" in comment else ""
        else:
            secs, note = parse_citation(comment)
        tl = target_line(lines, ln)
        if py not in lit_cache:
            lit_cache[py] = literals_by_line(py)
        lits = lit_cache[py].get(tl, {"num": [], "str": []})
        cls, gov, text, missing, shadow = resolve(lab, py, ln, secs, explicit)
        nums = text_numbers(text)
        num_res, str_res, note_res = [], [], []
        for n in lits["num"]:
            f = to_float(n)
            if f is None:
                continue
            num_res.append((n, num_present(f, nums) if text else None))
        for s in lits["str"]:
            ok = s in text or s.lower() in text.lower()
            str_res.append((s, ok))
        note_clean = re.sub(r"[\w./-]*\.md\s*§\s*[\d.]+|§\s*[\d.]+(?:/[\d.]+)*|\bDESIGN\b", " ", note)
        for n in NUM_RE.findall(note_clean.replace("−", "-")):
            note_res.append((n, num_present(float(n), nums) if text else None))
        # table-row check: if the governing section has a markdown table row naming the field on the
        # target line, the literal must appear in THAT row (catches 140 matching another row's 140).
        row_note = ""
        mname = re.match(r"\s*(\w+)\s*[:=]", lines[tl - 1])
        if mname and text:
            fname = mname.group(1)
            rows_ = [r for r in text.splitlines() if r.lstrip().startswith("|") and re.search(rf"(?<![\w]){re.escape(fname)}(?![\w])", r)]
            if rows_:
                rnums = text_numbers("\n".join(rows_))
                bad = [n for n, _ in num_res if to_float(n) is not None and num_present(to_float(n), rnums) is None]
                if bad:
                    row_note = f"ROW_MISMATCH:{fname}:{','.join(bad)}"
                    num_res = [(n, (r if n not in bad else None)) for n, r in num_res]
        if cls in ("RESOLVED", "AMBIGUOUS"):
            if num_res:
                vcls = "MATCH" if all(r for _, r in num_res) else "VALUE_ABSENT"
            elif str_res:
                vcls = "MATCH" if all(r for _, r in str_res) else "VALUE_ABSENT"
            else:
                vcls = "NO_LITERAL"
            full_cls = f"{cls}+{vcls}"
        else:
            full_cls = cls
        if explicit_mode:
            # Extension population: anchors are mixed (§2a, §CONCEPT_X, §RULE_Y), so only the FILE is
            # checked here; values are not. A missing file is also searched repo-wide (incl. archives).
            if cls == "UNRESOLVED_FILE":
                hits = [str(p.relative_to(ROOT)) for p in ROOT.rglob(Path(explicit).name) if ".git/" not in str(p)]
                full_cls = "UNRESOLVED_FILE" + (f"(only at {hits[0]})" if hits else "")
            else:
                full_cls = "FILE_OK"
        rows.append({
            "file": path, "line": ln, "target_line": tl, "lab": lab, "test": is_test,
            "secs": ",".join(secs), "class": full_cls,
            "nums": ";".join(f"{n}={r or 'ABSENT'}" for n, r in num_res),
            "strs": ";".join(f"{s}={'ok' if r else 'ABSENT'}" for s, r in str_res),
            "note_nums": ";".join(f"{n}={r or 'ABSENT'}" for n, r in note_res),
            "governing": " | ".join(gov), "missing_docs": ",".join(missing),
            "wiki_shadow": " | ".join(shadow), "explicit": explicit or "", "row_check": row_note,
            "src": full.strip()[:220],
        })
    return rows, raw


# ---------------------------------------------------------------- uncited literals
TRIVIAL = {0.0, 1.0, -1.0}
CMP_KW = {"ge", "le", "gt", "lt", "min_length", "max_length", "default"}


def uncited_literals():
    pkgs = []
    for lab in sorted((ROOT / "labs").iterdir()):
        p = lab / lab.name
        if (p / "__init__.py").exists():
            pkgs.append(p)
    rows = []
    for pkg in pkgs:
        for py in sorted(pkg.rglob("*.py")):
            rel = str(py.relative_to(ROOT))
            if "/tests/" in rel or py.name.startswith("test_"):
                continue
            src = py.read_text(encoding="utf-8")
            lines = src.splitlines()
            tree = ast.parse(src)
            parent: dict[int, ast.AST] = {}
            for n in ast.walk(tree):
                for c in ast.iter_child_nodes(n):
                    parent[id(c)] = n

            def cited(ln: int) -> bool:
                if "wiki" in lines[ln - 1].lower() or "§" in lines[ln - 1].split("#", 1)[-1]:
                    return True
                j = ln - 2
                while j >= 0 and lines[j].strip().startswith("#"):
                    if "wiki" in lines[j].lower():
                        return True
                    j -= 1
                # "comment below" convention (fault_atlas_router.py constants, payload.py fields)
                if ln < len(lines) and lines[ln].strip().startswith("#") and "wiki" in lines[ln].lower():
                    return True
                return False

            for n in ast.walk(tree):
                if not (isinstance(n, ast.Constant) and type(n.value) in (int, float)):
                    continue
                node, val = n, float(n.value)
                par = parent.get(id(n))
                if isinstance(par, ast.UnaryOp) and isinstance(par.op, ast.USub):
                    node, val = par, -val
                    par = parent.get(id(par))
                if val in TRIVIAL:
                    continue
                kind = None
                if isinstance(par, ast.Compare):
                    ops = par.ops
                    sides = [par.left, *par.comparators]
                    if any(isinstance(x, ast.Call) and isinstance(x.func, ast.Name) and x.func.id == "len" for x in sides):
                        continue  # structural count (len(vin) != 17), not a threshold
                    if type(n.value) is int and all(isinstance(o, (ast.Eq, ast.NotEq, ast.In, ast.NotIn)) for o in ops):
                        continue  # categorical integer equality (banks == 2, cyl == 6), not a threshold
                    kind = "compare"
                elif isinstance(par, ast.keyword) and par.arg in CMP_KW:
                    kind = f"kw:{par.arg}"
                elif isinstance(par, (ast.Assign, ast.AnnAssign)):
                    tgts = par.targets if isinstance(par, ast.Assign) else [par.target]
                    names = [t.id for t in tgts if isinstance(t, ast.Name)]
                    if names and all(re.fullmatch(r"_?[A-Z][A-Z0-9_]*", x) for x in names):
                        kind = "const"
                elif isinstance(par, ast.Call) and isinstance(par.func, ast.Name) and par.func.id in ("min", "max"):
                    kind = "clamp"
                elif isinstance(par, (ast.Tuple, ast.List, ast.Set)) and isinstance(parent.get(id(par)), ast.Compare):
                    continue  # membership in a literal set (cyl in (3, 4, 6, 8)) is categorical
                elif isinstance(par, ast.Dict) and node in par.values:
                    kind = "table-value"
                if kind is None:
                    continue  # arithmetic factor, index, slice, call arg, ...
                strict = cited(node.lineno)
                # statement-level: a citation anywhere on the enclosing statement (for if/while: its
                # condition) or in the comment block right above it covers every literal in it.
                stmt = node
                while stmt is not None and not isinstance(stmt, ast.stmt):
                    stmt = parent.get(id(stmt))
                lenient = strict
                if stmt is not None and not strict:
                    span_node = stmt.test if isinstance(stmt, (ast.If, ast.While)) else stmt
                    lo, hi = span_node.lineno, (span_node.end_lineno or span_node.lineno)
                    if isinstance(stmt, (ast.If, ast.While)):
                        lo = stmt.lineno
                    lenient = any("wiki" in lines[k - 1].lower() for k in range(lo, hi + 1)) or cited(lo)
                if lenient:
                    continue
                rows.append({"file": rel, "line": node.lineno, "value": val, "kind": kind,
                             "src": lines[node.lineno - 1].strip()[:200]})
    return rows


def main() -> int:
    OUT.mkdir(exist_ok=True)
    rows, raw = run_population("# wiki: §", explicit_mode=False)
    named, _ = run_population(r"wiki: [A-Za-z0-9_./-]*\.md §", explicit_mode=True)
    unc = uncited_literals()
    cols = list(rows[0].keys())
    for name, data in (("citations.tsv", rows), ("citations_named.tsv", named)):
        with open(OUT / name, "w", encoding="utf-8") as fh:
            fh.write("\t".join(cols) + "\n")
            for r in data:
                fh.write("\t".join(str(r[c]).replace("\t", " ") for c in cols) + "\n")
    with open(OUT / "uncited_literals.tsv", "w", encoding="utf-8") as fh:
        fh.write("file\tline\tvalue\tkind\tsrc\n")
        for r in unc:
            fh.write(f"{r['file']}\t{r['line']}\t{r['value']}\t{r['kind']}\t{r['src']}\n")

    def tally(rs):
        t: dict[str, int] = {}
        for r in rs:
            t[r["class"]] = t.get(r["class"], 0) + 1
        return dict(sorted(t.items()))
    summary = {
        "grep_lines": len(raw),
        "population": len(rows),
        "all": tally(rows),
        "production": tally([r for r in rows if not r["test"]]),
        "tests": tally([r for r in rows if r["test"]]),
        "note_value_absent": sum("ABSENT" in r["note_nums"] for r in rows),
        "string_absent_rows": sum("ABSENT" in r["strs"] for r in rows),
        "wiki_shadow_rows": sum(bool(r["wiki_shadow"]) for r in rows),
        "named_population": len(named),
        "named": tally(named),
        "uncited": len(unc),
        "uncited_by_kind": {k: sum(r["kind"] == k for r in unc) for k in sorted({r["kind"] for r in unc})},
        "uncited_by_pkg": {k: sum(r["file"].startswith(k) for r in unc) for k in sorted({"/".join(r["file"].split("/")[:3]) for r in unc})},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
