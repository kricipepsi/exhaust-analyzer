"""P2 suspect-site census (kinds a-f; kind g is joined in from suites.json written by suites.py).

Usage (repo root, venv active):
    python audit/scratch/P2/census.py [--suites audit/scratch/P2/suites.json] > audit/scratch/P2/census.json
    python audit/scratch/P2/census.py --controls          # planted positive / clean controls only

Every kind in the output declares mechanism, unit, population and blind_spot. Output is sorted and has
no timestamps or absolute paths, so two runs on the same tree are byte-identical.
"""
from __future__ import annotations

import ast
import importlib.machinery
import importlib.metadata as md
import importlib.util
import inspect
import io
import json
import re
import sys
import tokenize
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
LABS = ["comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab"]


# ----------------------------------------------------------------------------------------- populations
def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def pyfiles(d: Path) -> list[Path]:
    return sorted(p for p in d.rglob("*.py") if "__pycache__" not in p.parts)


def prod_population() -> dict[str, str]:
    """path -> module name for production code (plus 'offline' tooling, tagged separately)."""
    out: dict[str, str] = {}
    for lab in LABS:
        pkg = ROOT / "labs" / lab / lab
        for p in pyfiles(pkg):
            if "tests" in p.relative_to(pkg).parts:
                continue
            out[rel(p)] = modname(p, pkg.parent)
    reg = ROOT / "labs/comlab/registry"
    for p in pyfiles(reg):
        r = p.relative_to(reg).parts
        if r[0] in ("tests", "tools"):
            continue
        out[rel(p)] = modname(p, reg.parent)
    for p in pyfiles(ROOT / "apps/wired/wired"):
        out[rel(p)] = modname(p, ROOT / "apps/wired")
    out["apps/ui/ui_payload.py"] = "ui_payload"
    out["apps/ui/app.py"] = "ui_app"
    out["app.py"] = "app_shim"
    return out


def offline_population() -> dict[str, str]:
    out = {}
    for p in pyfiles(ROOT / "labs/vinlab/tools"):
        out[rel(p)] = "vinlab_tools." + p.stem
    for p in pyfiles(ROOT / "labs/comlab/registry/tools"):
        out[rel(p)] = "registry.tools." + p.stem
    for sub in ("v7", "fl_tasks", "trace"):
        for p in pyfiles(ROOT / "apps/wired" / sub):
            if "tests" in p.parts:
                continue
            out[rel(p)] = modname(p, ROOT / "apps/wired")
    return out


TEST_DIRS = [*(f"labs/{lab}/tests" for lab in LABS), "labs/comlab/registry/tests",
             "apps/wired/tests", "apps/wired/v7/tests", "apps/ui/tests"]


def test_population() -> dict[str, str]:
    out = {}
    for d in TEST_DIRS:
        for p in pyfiles(ROOT / d):
            out[rel(p)] = rel(p)[:-3].replace("/", ".")
    return out


def modname(p: Path, base: Path) -> str:
    parts = list(p.relative_to(base).with_suffix("").parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def parse(path: str) -> ast.Module:
    return ast.parse((ROOT / path).read_text(encoding="utf-8"), filename=path)


def comments(path: str) -> list[tuple[int, str]]:
    src = (ROOT / path).read_text(encoding="utf-8")
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT:
            out.append((tok.start[0], tok.string))
    return out


def dotted(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f"{base}.{node.attr}" if base else ""
    if isinstance(node, ast.Call):
        return dotted(node.func)
    return ""


def src(node: ast.AST) -> str:
    return ast.unparse(node)[:160]


# ------------------------------------------------------------------------- (a) never-pass / never-run
def is_test_fn(name: str) -> bool:
    return name.startswith("test")


def iter_tests(tree: ast.Module):
    """Yield (class_or_None, funcdef) for every function pytest would collect by name."""
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_test_fn(node.name):
            yield None, node
        elif isinstance(node, ast.ClassDef) and node.name.startswith("Test"):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)) and is_test_fn(sub.name):
                    yield node, sub


def mark_kind(dec: ast.AST) -> tuple[str, ast.Call | None]:
    d = dotted(dec)
    for k in ("skipif", "skip", "xfail"):
        if d.endswith(f"mark.{k}"):
            return k, dec if isinstance(dec, ast.Call) else None
    return "", None


def kw(call: ast.Call | None, name: str):
    if call is None:
        return None
    for k in call.keywords:
        if k.arg == name:
            return k.value
    return None


def reason_of(call: ast.Call | None) -> str:
    if call is None:
        return ""
    r = kw(call, "reason")
    if r is None and call.args and isinstance(call.args[-1], ast.Constant) and isinstance(call.args[-1].value, str):
        r = call.args[-1]
    return r.value if isinstance(r, ast.Constant) else (src(r) if r is not None else "")


def kind_a(tests: dict[str, str]) -> list[dict]:
    sites = []
    for path in sorted(tests):
        tree = parse(path)
        base = Path(path).name
        collectable = base.startswith("test_")
        # module-level marks and calls
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in node.targets):
                for m in ast.walk(node.value):
                    k, call = mark_kind(m)
                    if k and (isinstance(m, ast.Call) or not any(m is a.func for a in ast.walk(node.value) if isinstance(a, ast.Call))):
                        sites.append(dict(path=path, line=node.lineno, scope="module", test="*", kind=f"mark.{k}",
                                          condition=src(call.args[0]) if call is not None and k != "skip" and call.args else "",
                                          reason=reason_of(call)))
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                d = dotted(node.value.func)
                if d in ("pytest.skip", "pytest.fail", "pytest.xfail", "pytest.importorskip"):
                    sites.append(dict(path=path, line=node.lineno, scope="module", test="*", kind=d,
                                      condition=src(node.value.args[0]) if node.value.args else "", reason=""))
        names_seen: dict[tuple[str, str], int] = {}
        for cls, fn in iter_tests(tree):
            tid = f"{cls.name}::{fn.name}" if cls else fn.name
            key = (cls.name if cls else "", fn.name)
            if key in names_seen:
                sites.append(dict(path=path, line=names_seen[key], scope="function", test=tid, kind="shadowed-by-redefinition",
                                  condition=f"redefined at line {fn.lineno}", reason=""))
            names_seen[key] = fn.lineno
            decs = list(fn.decorator_list) + (list(cls.decorator_list) if cls else [])
            for dec in decs:
                k, call = mark_kind(dec)
                if not k:
                    continue
                cond = ""
                if call is not None and call.args and not (isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str)):
                    cond = src(call.args[0])
                sites.append(dict(path=path, line=dec.lineno, scope="class" if cls and dec in cls.decorator_list else "function",
                                  test=tid, kind=f"mark.{k}", condition=cond, reason=reason_of(call),
                                  strict=src(kw(call, "strict")) if kw(call, "strict") is not None else ""))
            for stmt in fn.body:  # unconditional calls at function top level only
                if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
                    d = dotted(stmt.value.func)
                    if d in ("pytest.skip", "pytest.fail", "pytest.xfail", "pytest.importorskip"):
                        a0 = stmt.value.args[0] if stmt.value.args else None
                        sites.append(dict(path=path, line=stmt.lineno, scope="function-body", test=tid, kind=d,
                                          condition=src(a0) if d == "pytest.importorskip" and a0 is not None else "",
                                          reason=a0.value if isinstance(a0, ast.Constant) and d != "pytest.importorskip" else ""))
            if any(isinstance(n, (ast.Yield, ast.YieldFrom)) for n in ast.walk(fn)) and not any(
                    dotted(d).endswith("fixture") for d in fn.decorator_list):
                sites.append(dict(path=path, line=fn.lineno, scope="function", test=tid, kind="yield-test", condition="", reason=""))
        if cls_with_init := [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name.startswith("Test")
                             and any(isinstance(s, ast.FunctionDef) and s.name == "__init__" for s in n.body)]:
            for c in cls_with_init:
                sites.append(dict(path=path, line=c.lineno, scope="class", test=c.name, kind="class-has-__init__ (not collected)",
                                  condition="", reason=""))
        if not collectable and base != "conftest.py":
            for cls, fn in iter_tests(tree):
                sites.append(dict(path=path, line=fn.lineno, scope="file", test=fn.name, kind="file-name-not-collected",
                                  condition="python_files=test_*.py", reason=""))
        for node in tree.body:  # test-named functions in non-Test classes
            if isinstance(node, ast.ClassDef) and not node.name.startswith("Test"):
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef) and is_test_fn(sub.name):
                        sites.append(dict(path=path, line=sub.lineno, scope="class", test=f"{node.name}::{sub.name}",
                                          kind="class-name-not-collected", condition="", reason=""))
    return sites


# ----------------------------------------------------------------------------- (b) import guards
def requirements_closure() -> set[str]:
    """Distribution names installed by `pip install -r requirements.txt` (the Render build)."""
    roots = []
    for line in (ROOT / "requirements.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-e "):
            roots.append(Path(line[3:]).name)
        else:
            roots.append(re.split(r"[=<>!~\[ ;]", line)[0])
    seen: set[str] = set()
    q = deque(roots)
    while q:
        name = q.popleft().lower().replace("_", "-")
        if name in seen:
            continue
        seen.add(name)
        try:
            reqs = md.requires(name) or []
        except md.PackageNotFoundError:
            continue
        for r in reqs:
            if "extra ==" in r:
                continue
            q.append(re.split(r"[=<>!~\[ ;(]", r)[0])
    return seen


STDLIB = set(sys.stdlib_module_names)


def module_present(mod: str, ctx: str, closure: set[str], pkg_dists: dict[str, list[str]]) -> bool:
    top = mod.split(".")[0]
    if top in STDLIB:
        return importlib.util.find_spec(mod) is not None
    if ctx == "deploy":
        dists = {d.lower().replace("_", "-") for d in pkg_dists.get(top, [])}
        repo_tops = {"comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab", "wired"}
        if top not in repo_tops and not (dists & closure):
            return False
        if top == "registry":  # not installed by requirements.txt; on sys.path only via labs/comlab
            return False
    try:
        return importlib.util.find_spec(mod) is not None
    except (ModuleNotFoundError, ValueError):
        return False


def abs_module(node: ast.ImportFrom, modname_: str, is_pkg: bool) -> str:
    if node.level == 0:
        return node.module or ""
    parts = modname_.split(".")
    base = parts if is_pkg else parts[:-1]
    base = base[: len(base) - (node.level - 1)]
    return ".".join(base + ([node.module] if node.module else []))


def guard_mods(body: list[ast.stmt], modname_: str, is_pkg: bool) -> list[str]:
    mods = []
    for n in body:
        for m in ast.walk(n):
            if isinstance(m, ast.Import):
                mods += [a.name for a in m.names]
            elif isinstance(m, ast.ImportFrom):
                mods.append(abs_module(m, modname_, is_pkg))
    return mods


def kind_b(files: dict[str, str], group: str, closure, pkg_dists) -> list[dict]:
    sites = []
    for path, mod in sorted(files.items()):
        tree = parse(path)
        is_pkg = path.endswith("__init__.py")
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                for h in node.handlers:
                    names = [dotted(e) for e in (h.type.elts if isinstance(h.type, ast.Tuple) else [h.type])] if h.type else []
                    if not any(n in ("ImportError", "ModuleNotFoundError") for n in names):
                        continue
                    mods = guard_mods(node.body, mod, is_pkg)
                    if not mods:
                        sites.append(dict(group=group, path=path, line=h.lineno, kind="try-import", modules=[],
                                          status="UNADJUDICATED", note="ImportError guard with no import in try body"))
                        continue
                    pres = {ctx: all(module_present(m, ctx, closure, pkg_dists) for m in mods) for ctx in ("audit-venv", "deploy")}
                    sites.append(dict(group=group, path=path, line=h.lineno, kind="try-import", modules=sorted(set(mods)),
                                      present=pres, status=classify(pres)))
            if isinstance(node, ast.Call) and dotted(node.func) in ("importlib.util.find_spec", "find_spec", "pytest.importorskip") \
                    and node.args and isinstance(node.args[0], ast.Constant):
                m = node.args[0].value
                pres = {ctx: module_present(m, ctx, closure, pkg_dists) for ctx in ("audit-venv", "deploy")}
                sites.append(dict(group=group, path=path, line=node.lineno, kind=dotted(node.func), modules=[m],
                                  present=pres, status=classify(pres)))
    return sites


def classify(pres: dict[str, bool]) -> str:
    v = set(pres.values())
    if v == {True}:
        return "UNREACHABLE-FALLBACK"
    if v == {False}:
        return "UNREACHABLE-PRIMARY"
    return "LIVE"


# ----------------------------------------------------------------------------- (c) assertion-free
class Helpers:
    """Resolve a call in a test module to a function body by AST; decide if it asserts."""

    def __init__(self, tests: dict[str, str]):
        self.trees = {p: parse(p) for p in tests}
        self.cache: dict[tuple, bool | None] = {}

    def defs(self, path: str) -> dict[str, ast.AST]:
        out = {}
        for n in self.trees[path].body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                out[n.name] = n
        return out

    def imports(self, path: str) -> dict[str, str]:
        out = {}
        for n in ast.walk(self.trees[path]):
            if isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                for a in n.names:
                    out[a.asname or a.name] = f"{n.module}.{a.name}"
            elif isinstance(n, ast.ImportFrom) and n.level > 0:
                for a in n.names:
                    out[a.asname or a.name] = f"{'.' * n.level}{n.module or ''}.{a.name}"
            elif isinstance(n, ast.Import):
                for a in n.names:
                    out[a.asname or a.name.split(".")[0]] = a.asname and a.name or a.name.split(".")[0]
        return out

    def test_module_path(self, path: str, target: str) -> str | None:
        """Find a test-population file that defines dotted target's module (relative or sibling import)."""
        modpart = target.rsplit(".", 1)[0]
        d = (ROOT / path).parent
        if modpart.startswith("."):
            lvl = len(modpart) - len(modpart.lstrip("."))
            for _ in range(lvl - 1):
                d = d.parent
            cand = d / (modpart.lstrip(".").replace(".", "/") + ".py")
        else:
            cand = None
            for base in [d, *d.parents]:
                c = base / (modpart.replace(".", "/") + ".py")
                if c.exists():
                    cand = c
                    break
                if base == ROOT:
                    break
        if cand is not None and cand.exists():
            r = rel(cand)
            return r if r in self.trees else None
        return None

    def body_asserts(self, path: str, fn: ast.AST, depth: int, cls: ast.ClassDef | None = None) -> bool | None:
        """True if fn asserts (directly or via a resolved helper); None if an unresolved candidate exists."""
        unresolved = False
        nodes = [m for st in fn.body for m in ast.walk(st)] if hasattr(fn, "body") else list(ast.walk(fn))
        for n in nodes:  # decorators (parametrize, skip marks) are not part of the test body
            if isinstance(n, ast.Assert):
                return True
            if isinstance(n, ast.Raise):
                return True
            if isinstance(n, ast.Call):
                d = dotted(n.func)
                if d.split(".")[-1] in ("raises", "warns", "fail", "deprecated_call") and d.startswith("pytest"):
                    return True
                if d.startswith("self.") and cls is not None:
                    meth = d.split(".", 1)[1]
                    target = next((s for s in cls.body if isinstance(s, ast.FunctionDef) and s.name == meth), None)
                    if target is not None and depth < 6:
                        r = self.body_asserts(path, target, depth + 1, cls)
                        if r:
                            return True
                    elif target is None and any(dotted(b).endswith("TestCase") for b in cls.bases) and meth.startswith(("assert", "fail")):
                        return lib_asserts("unittest.TestCase." + meth) or None
                    continue
                r = self.resolve_call(path, d, depth)
                if r is True:
                    return True
                if r is None:
                    unresolved = True
        return None if unresolved else False

    def resolve_call(self, path: str, d: str, depth: int) -> bool | None:
        """True/False if the call resolves to a test helper or library function; 'skip' (False) for production."""
        if not d or depth > 6:
            return False
        key = (path, d)
        if key in self.cache:
            return self.cache[key]
        self.cache[key] = False  # cycle guard
        head = d.split(".")[0]
        result: bool | None = False
        defs = self.defs(path)
        imps = self.imports(path)
        if head in defs and "." not in d and not isinstance(defs[head], ast.ClassDef):
            result = bool(self.body_asserts(path, defs[head], depth + 1))
        elif head in imps:
            target = imps[head] + d[len(head):]
            tpath = self.test_module_path(path, imps[head])
            if tpath is not None:
                name = imps[head].rsplit(".", 1)[1]
                fn = self.defs(tpath).get(name)
                result = bool(self.body_asserts(tpath, fn, depth + 1)) if fn is not None and not isinstance(fn, ast.ClassDef) else False
            elif target.split(".")[0] in REPO_TOPS:
                result = False  # production code: a call is not an assertion
            else:
                result = lib_asserts(target)
        self.cache[key] = result
        return result


REPO_TOPS = {"comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab", "wired", "registry", "ui_payload",
             "app", "v7", "fl_tasks", "harness", "tests"}
_LIB_CACHE: dict[str, bool] = {}


def lib_asserts(target: str) -> bool:
    """Resolve a library callable and inspect its source AST for assert / raise AssertionError / fail()."""
    if target in _LIB_CACHE:
        return _LIB_CACHE[target]
    res = False
    parts = target.split(".")
    obj = None
    for i in range(len(parts), 0, -1):
        try:
            obj = importlib.import_module(".".join(parts[:i]))
        except Exception:  # noqa: BLE001 — probing arbitrary dotted names
            continue
        try:
            for p in parts[i:]:
                obj = getattr(obj, p)
        except AttributeError:
            obj = None
        break
    if obj is not None and callable(obj) and not inspect.ismodule(obj) and not inspect.isclass(obj):
        try:
            tree = ast.parse(inspect.getsource(inspect.unwrap(obj)).lstrip() if True else "")
        except (OSError, TypeError, SyntaxError, IndentationError):
            tree = None
        if tree is not None:
            for n in ast.walk(tree):
                if isinstance(n, ast.Assert):
                    res = True
                elif isinstance(n, ast.Raise) and n.exc is not None and re.search(r"AssertionError|failureException", src(n.exc)):
                    res = True
                elif isinstance(n, ast.Call) and dotted(n.func).split(".")[-1] in ("fail", "_raise_assertion", "fail_test"):
                    res = True
    _LIB_CACHE[target] = res
    return res


def kind_c(tests: dict[str, str]) -> tuple[list[dict], int]:
    H = Helpers(tests)
    sites, total = [], 0
    for path in sorted(tests):
        if not Path(path).name.startswith("test_"):
            continue
        for cls, fn in iter_tests(H.trees[path]):
            total += 1
            r = H.body_asserts(path, fn, 0, cls)
            if r is True:
                continue
            calls = sorted({dotted(n.func) for st in fn.body for n in ast.walk(st) if isinstance(n, ast.Call) and dotted(n.func)})
            stmts = [s for s in fn.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
            sites.append(dict(path=path, line=fn.lineno, test=f"{cls.name}::{fn.name}" if cls else fn.name,
                              status="UNADJUDICATED" if r is None else ("EMPTY" if not calls else "NO-ASSERTION"),
                              body_statements=len(stmts), calls=calls[:12]))
    return sites, total


# ---------------------------------------------------------------------------- (d) swallowed errors
BROAD = {"Exception", "BaseException"}


def handler_shape(h: ast.ExceptHandler) -> tuple[str, str]:
    body = [s for s in h.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    if any(isinstance(n, ast.Raise) for s in body for n in ast.walk(s)):
        return "RERAISE", ""
    if not body or all(isinstance(s, ast.Pass) for s in body):
        return "PASS", ""
    kinds = []
    ret = ""
    for s in body:
        if isinstance(s, ast.Continue):
            kinds.append("CONTINUE")
        elif isinstance(s, ast.Break):
            kinds.append("BREAK")
        elif isinstance(s, ast.Return):
            kinds.append("RETURN")
            ret = src(s.value) if s.value is not None else "None"
        elif isinstance(s, ast.Expr) and isinstance(s.value, ast.Call) and re.search(
                r"(^|\.)(log|logger|logging|warn|warning|warnings|error|exception|debug|info|print|st)\b", dotted(s.value.func)):
            kinds.append("LOG")
        elif isinstance(s, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            kinds.append("ASSIGN")
        else:
            kinds.append("OTHER")
    for k in ("RETURN", "CONTINUE", "BREAK"):
        if k in kinds:
            return f"{k}{'+LOG' if 'LOG' in kinds else ''}", ret
    if set(kinds) == {"LOG"}:
        return "LOG-ONLY", ""
    if "ASSIGN" in kinds and "OTHER" not in kinds:
        return "ASSIGN-DEFAULT", src(body[[i for i, k in enumerate(kinds) if k == "ASSIGN"][0]])
    return "OTHER", src(body[0])


def enclosing_functions(tree: ast.Module) -> list[tuple[int, int, str]]:
    spans = []

    def visit(node, prefix):
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                q = f"{prefix}.{ch.name}" if prefix else ch.name
                if not isinstance(ch, ast.ClassDef):
                    spans.append((ch.lineno, ch.end_lineno, q))
                visit(ch, q)
            else:
                visit(ch, prefix)
    visit(tree, "")
    return spans


def innermost(spans, line: int) -> str:
    best = None
    for a, b, q in spans:
        if a <= line <= b and (best is None or a >= best[0]):
            best = (a, b, q)
    return best[2] if best else "<module>"


def kind_d(files: dict[str, str], group: str) -> tuple[list[dict], dict]:
    sites, denom = [], {"handlers_total": 0, "broad": 0, "narrow": 0}
    for path in sorted(files):
        tree = parse(path)
        spans = enclosing_functions(tree)
        for h in [n for n in ast.walk(tree) if isinstance(n, ast.ExceptHandler)]:
            denom["handlers_total"] += 1
            types = [dotted(e) for e in (h.type.elts if isinstance(h.type, ast.Tuple) else [h.type])] if h.type else []
            broad = h.type is None or any(t.split(".")[-1] in BROAD for t in types)
            denom["broad" if broad else "narrow"] += 1
            shape, detail = handler_shape(h)
            sites.append(dict(group=group, path=path, line=h.lineno, function=f"{files[path]}.{innermost(spans, h.lineno)}",
                              caught="bare" if h.type is None else ",".join(types), shape=shape, detail=detail,
                              broad=broad, swallowed=broad and shape != "RERAISE"))
    return sites, denom


# --------------------------------------------------------------------------------- (e) loose types
def kind_e(files: dict[str, str], group: str) -> list[dict]:
    rows = []
    for path in sorted(files):
        tree = parse(path)
        any_names = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module in ("typing", "typing_extensions")
                     for a in n.names if a.name == "Any"}
        typing_mods = {a.asname or a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names if a.name in ("typing", "typing_extensions")}
        ann_any = other_any = 0
        ann_nodes = set()
        for n in ast.walk(tree):
            anns = []
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                anns = [a.annotation for a in [*n.args.args, *n.args.kwonlyargs, *n.args.posonlyargs, n.args.vararg, n.args.kwarg] if a and a.annotation]
                if n.returns:
                    anns.append(n.returns)
            elif isinstance(n, ast.AnnAssign):
                anns = [n.annotation]
            for a in anns:
                for m in ast.walk(a):
                    ann_nodes.add(id(m))
                    if isinstance(m, ast.Constant) and isinstance(m.value, str):
                        ann_any += len(re.findall(r"\bAny\b", m.value))
        for n in ast.walk(tree):
            hit = (isinstance(n, ast.Name) and n.id in any_names) or (
                isinstance(n, ast.Attribute) and n.attr == "Any" and isinstance(n.value, ast.Name) and n.value.id in typing_mods)
            if hit:
                if id(n) in ann_nodes:
                    ann_any += 1
                elif not isinstance(getattr(n, "ctx", None), ast.Store):
                    other_any += 1
        cm = comments(path)
        tig = sum(1 for _, c in cm if re.search(r"type:\s*ignore", c))
        pig = sum(1 for _, c in cm if re.search(r"pyright:\s*ignore", c))
        nq = sum(1 for _, c in cm if re.search(r"\bnoqa\b", c, re.I))
        if ann_any or other_any or tig or pig or nq:
            rows.append(dict(group=group, path=path, any_annotation=ann_any, any_other=other_any,
                             type_ignore=tig, pyright_ignore=pig, noqa=nq))
    return rows


# ------------------------------------------------------------------------- (f) call graph + reachability
class Graph:
    def __init__(self, files: dict[str, str]):
        self.files = files
        self.mod2path = {m: p for p, m in files.items()}
        self.trees = {p: parse(p) for p in files}
        self.funcs: dict[str, tuple[str, ast.AST, str | None]] = {}  # qual -> (path, node, class qual)
        self.classes: dict[str, tuple[str, ast.ClassDef]] = {}
        self.aliases: dict[str, dict[str, str]] = {}
        self.edges: dict[str, set[str]] = defaultdict(set)
        self.unresolved_calls = 0
        self.resolved_calls = 0
        for p, m in files.items():
            self._index(p, m)
        for p, m in files.items():
            self._edges(p, m)

    def _index(self, path, mod):
        tree = self.trees[path]
        self.funcs[f"{mod}.<module>"] = (path, tree, None)
        al = {}
        is_pkg = path.endswith("__init__.py")
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    al[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
            elif isinstance(n, ast.ImportFrom):
                base = abs_module(n, mod, is_pkg)
                for a in n.names:
                    al[a.asname or a.name] = f"{base}.{a.name}"
        self.aliases[mod] = al

        def visit(node, prefix, cls):
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, ast.ClassDef):
                    q = f"{prefix}.{ch.name}"
                    self.classes[q] = (path, ch)
                    visit(ch, q, q)
                elif isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    q = f"{prefix}.{ch.name}"
                    self.funcs[q] = (path, ch, cls)
                    visit(ch, q, None)
                else:
                    visit(ch, prefix, cls)
        visit(tree, mod, None)

    def resolve(self, q: str, depth: int = 0) -> str | None:
        """Follow module aliases (package re-exports) to a function/class/module qualname."""
        if depth > 8:
            return None
        if q in self.funcs or q in self.classes:
            return q
        parts = q.split(".")
        for i in range(len(parts) - 1, 0, -1):
            mod = ".".join(parts[:i])
            if mod in self.aliases:
                rest = parts[i:]
                if rest[0] in self.aliases[mod]:
                    return self.resolve(".".join([self.aliases[mod][rest[0]], *rest[1:]]), depth + 1)
                return None
        if q in self.aliases:
            return f"{q}.<module>"
        return None

    def method(self, cls_q: str, name: str, depth=0) -> str | None:
        if f"{cls_q}.{name}" in self.funcs:
            return f"{cls_q}.{name}"
        if cls_q not in self.classes or depth > 6:
            return None
        path, cnode = self.classes[cls_q]
        mod = self.files[path]
        for b in cnode.bases:
            bq = self.resolve(self._qualify(mod, dotted(b)) or "")
            if bq and bq in self.classes:
                r = self.method(bq, name, depth + 1)
                if r:
                    return r
        return None

    def _qualify(self, mod, d):
        if not d:
            return None
        head = d.split(".")[0]
        al = self.aliases.get(mod, {})
        if head in al:
            return al[head] + d[len(head):]
        cand = f"{mod}.{d}"
        return cand

    def _edges(self, path, mod):
        for q, (p, node, cls) in list(self.funcs.items()):
            if p != path:
                continue
            local_types: dict[str, str] = {}
            body_nodes = []
            stack = list(ast.iter_child_nodes(node)) if not isinstance(node, ast.Module) else list(node.body)
            while stack:  # do not descend into nested defs (they are their own nodes)
                n = stack.pop()
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)) and n is not node:
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.edges[q].add(f"{q}.{n.name}" if f"{q}.{n.name}" in self.funcs else q)
                    if isinstance(n, ast.Lambda):
                        stack.extend(ast.iter_child_nodes(n))
                    continue
                body_nodes.append(n)
                stack.extend(ast.iter_child_nodes(n))
            for n in body_nodes:  # simple local type inference: x = Cls(...)
                if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call):
                    t = self.resolve(self._qualify(mod, dotted(n.value.func)) or "")
                    if t in self.classes:
                        for tg in n.targets:
                            if isinstance(tg, ast.Name):
                                local_types[tg.id] = t
                            elif isinstance(tg, ast.Attribute) and isinstance(tg.value, ast.Name) and tg.value.id == "self":
                                local_types[f"self.{tg.attr}"] = t
            if cls:
                for n2 in ast.walk(self.classes[cls][1]):
                    if isinstance(n2, ast.Assign) and isinstance(n2.value, ast.Call):
                        t = self.resolve(self._qualify(mod, dotted(n2.value.func)) or "")
                        for tg in n2.targets:
                            if t in self.classes and isinstance(tg, ast.Attribute) and dotted(tg.value) == "self":
                                local_types.setdefault(f"self.{tg.attr}", t)
            for n in body_nodes:
                if isinstance(n, ast.Call):
                    tgt = self._call_target(mod, cls, dotted(n.func), local_types)
                    if tgt:
                        self.resolved_calls += 1
                        self.edges[q].add(tgt)
                        if tgt in self.classes:
                            for m in ("__init__", "__post_init__", "__call__"):
                                mq = self.method(tgt, m)
                                if mq:
                                    self.edges[q].add(mq)
                        if tgt.endswith(".<module>") is False and tgt in self.funcs:
                            pass
                    else:
                        self.unresolved_calls += 1
                elif isinstance(n, (ast.Name, ast.Attribute)) and isinstance(getattr(n, "ctx", None), ast.Load):
                    # function passed by reference (dispatch tables, callbacks)
                    tgt = self._call_target(mod, cls, dotted(n), local_types)
                    if tgt and tgt in self.funcs and not tgt.endswith("<module>"):
                        self.edges[q].add(tgt)
                elif isinstance(n, (ast.Import, ast.ImportFrom)):
                    base = abs_module(n, mod, path.endswith("__init__.py")) if isinstance(n, ast.ImportFrom) else None
                    names = [a.name for a in n.names] if isinstance(n, ast.Import) else [base] + [f"{base}.{a.name}" for a in n.names]
                    for nm in names:
                        for cand in (nm, nm.rsplit(".", 1)[0]):
                            if cand in self.mod2path:
                                self.edges[q].add(f"{cand}.<module>")

    def _call_target(self, mod, cls, d, local_types) -> str | None:
        if not d:
            return None
        head, _, rest = d.partition(".")
        if d.startswith("self.") and cls:
            parts = d.split(".")
            if len(parts) == 2:
                return self.method(cls, parts[1])
            key = f"self.{parts[1]}"
            if key in local_types and len(parts) == 3:
                return self.method(local_types[key], parts[2])
            return None
        if d.startswith("super().") and cls:
            path, cnode = self.classes[cls]
            for b in cnode.bases:
                bq = self.resolve(self._qualify(mod, dotted(b)) or "")
                if bq:
                    r = self.method(bq, d.split(".")[-1])
                    if r:
                        return r
            return None
        if head in local_types and rest and "." not in rest:
            return self.method(local_types[head], rest)
        r = self.resolve(self._qualify(mod, d) or "")
        if r:
            return r
        if "." in d:  # Class.method on a resolved class
            base, meth = d.rsplit(".", 1)
            b = self.resolve(self._qualify(mod, base) or "")
            if b in self.classes:
                return self.method(b, meth)
        return None

    def reach(self, entries: list[str]) -> dict[str, str | None]:
        parent: dict[str, str | None] = {}
        q = deque()
        for e in entries:
            if e in self.funcs:
                parent[e] = None
                q.append(e)
        while q:
            cur = q.popleft()
            nxt = set(self.edges.get(cur, ()))
            if cur in self.classes:
                pass
            for n in sorted(nxt):
                if n in self.classes:
                    for m in ("__init__", "__post_init__"):
                        mq = self.method(n, m)
                        if mq and mq not in parent:
                            parent[mq] = cur
                            q.append(mq)
                    continue
                if n not in parent and n in self.funcs:
                    parent[n] = cur
                    q.append(n)
            # a method's class body (validators, defaults) runs when its module loads
        return parent

    def chain(self, parent, node) -> list[str]:
        out = []
        while node is not None:
            out.append(node)
            node = parent[node]
        return out[::-1]


ENTRIES = ["wired.composition.diagnose", "ui_payload.build_diagnose_payload", "ui_app.<module>", "app_shim.<module>"]


def owner_of(G: Graph, path: str, line: int) -> str:
    best, span = f"{G.files[path]}.<module>", None
    for q, (p, node, _) in G.funcs.items():
        if p == path and not isinstance(node, ast.Module) and node.lineno <= line <= node.end_lineno:
            if span is None or node.lineno >= span:
                best, span = q, node.lineno
    return best


def kind_f(G: Graph, parent) -> list[dict]:
    sites = []
    for path in sorted(G.files):
        tree = G.trees[path]
        for n in ast.walk(tree):
            if isinstance(n, ast.Raise) and n.exc is not None and "NotImplementedError" in dotted(n.exc):
                sites.append((path, n.lineno, "raise NotImplementedError", src(n)))
        for line, c in comments(path):
            if re.search(r"\b(TODO|FIXME|XXX|HACK)\b", c):
                sites.append((path, line, "comment", c.strip()[:160]))
    out = []
    for path, line, kind, text in sites:
        o = owner_of(G, path, line)
        reach = o in parent
        out.append(dict(path=path, line=line, kind=kind, text=text, owner=o,
                        reachable=reach, chain=G.chain(parent, o) if reach else []))
    return out


# --------------------------------------------------------------------------------------- (g) join
def runtime_outcome(site: dict, g: dict) -> list[str]:
    """Outcomes recorded in suites.json for the nodes of this site's test (module sites: any node of the file)."""
    if "skipped_or_xfailed" not in g:
        return ["ABSENT"]
    tname = site["test"].split("::")[-1]
    out = set()
    for row in g["skipped_or_xfailed"] + g["failing"]:
        if not site["path"].startswith(row["cwd"] + "/"):
            continue
        dotted_rel = site["path"][len(row["cwd"]) + 1:-3].replace("/", ".")
        cls, _, name = row["node"].partition("::")
        if not (cls == dotted_rel or cls.startswith(dotted_rel + ".")):
            continue
        if site["test"] == "*" or name.split("[")[0] == tname:
            out.add(f'{row["suite"]}:{row["outcome"]}')
    return sorted(out) or ["not-skipped-or-failed (passed, deselected or not collected)"]


def kind_g(suites_path: Path) -> dict:
    if not suites_path.exists():
        return {"status": "ABSENT", "note": f"{suites_path.name} not found; run suites.py first"}
    data = json.loads(suites_path.read_text())
    rows = []
    for s in data:
        for c in s["non_passing"]:
            if c["outcome"] in ("failure", "error"):
                rows.append(dict(suite=s["suite"], cwd=s["cwd"], collected_by_baseline=s["collected_by_baseline"], **c))
    return {"suites": [{k: s[k] for k in ("suite", "cwd", "args", "summary", "collected_by_baseline")} for s in data],
            "failing": rows,
            "skipped_or_xfailed": [dict(suite=s["suite"], cwd=s["cwd"], **c) for s in data for c in s["non_passing"]
                                   if c["outcome"] in ("skipped", "xfailed")]}


# --------------------------------------------------------------------------------------- driver
def census(prod, offline, tests, suites_path, entries=ENTRIES) -> dict:
    closure = requirements_closure()
    pkg_dists = md.packages_distributions()
    G = Graph(prod)
    parent = G.reach(entries)
    a = kind_a(tests)
    g = kind_g(suites_path)
    for site in a:
        site["runtime"] = runtime_outcome(site, g)
    b = kind_b(prod, "prod", closure, pkg_dists) + kind_b(offline, "offline", closure, pkg_dists) + kind_b(tests, "tests", closure, pkg_dists)
    c, ctotal = kind_c(tests)
    dprod, dden = kind_d(prod, "prod")
    doff, doffden = kind_d(offline, "offline")
    for s in dprod:
        s["reachable"] = s["function"] in parent or owner_of(G, s["path"], s["line"]) in parent
        s["owner"] = owner_of(G, s["path"], s["line"])
        s["chain"] = G.chain(parent, s["owner"]) if s["owner"] in parent else []
    e = kind_e(prod, "prod") + kind_e(offline, "offline")
    f = kind_f(G, parent)
    return {
        "populations": {"prod_files": len(prod), "offline_files": len(offline), "test_files": len(tests),
                        "prod_functions_indexed": sum(1 for q in G.funcs if not q.endswith("<module>")),
                        "callgraph_resolved_calls": G.resolved_calls, "callgraph_unresolved_calls": G.unresolved_calls,
                        "reachable_functions": len(parent), "entries": entries,
                        "requirements_closure": sorted(closure)},
        "a_never_pass_or_run": {
            "mechanism": "AST over test files: pytestmark/decorator marks skip|skipif|xfail, unconditional top-level "
                         "pytest.skip|fail|xfail|importorskip calls, duplicate test names, yield tests, non-collectable "
                         "classes/files; joined with runtime outcomes from suites.json",
            "unit": "one site (mark, call, or shadowing) on one test or module",
            "population": f"{len(tests)} .py files under {TEST_DIRS}",
            "blind_spot": "conditional skips inside if/try bodies; skips raised by fixtures/conftest hooks; marks added "
                          "via pytest_collection_modifyitems; -m deselection outside pyproject addopts",
            "sites": a},
        "b_dead_guard": {
            "mechanism": "AST: try/except ImportError|ModuleNotFoundError bodies and find_spec/importorskip literal "
                         "args; each module resolved with importlib.util.find_spec in the audit venv, and for the "
                         "deploy context additionally required to belong to the requirements.txt dependency closure",
            "unit": "one guard site",
            "population": "prod + offline + test files",
            "blind_spot": "guards on non-literal module names; `if FLAG:` uses of a guard's flag are not separately "
                          "counted (the guard is); deploy context assumes Render's sys.path = repo root + apps/ui + "
                          "editable installs (no labs/comlab, so `registry` is absent)",
            "sites": b},
        "c_assertion_free": {
            "mechanism": "AST per collected-by-name test function: assert stmt, raise, pytest.raises|warns|fail, "
                         "self.assert* on unittest.TestCase, or a call resolved by AST to a test-population helper or "
                         "library function whose body asserts / raises AssertionError (transitive, depth 6)",
            "unit": "one test function (parametrised variants count once)",
            "population": f"{ctotal} test functions in test_*.py files of the test population",
            "blind_spot": "assertions inside fixtures; snapshot/approval comparisons done by plugins; production "
                          "calls are deliberately not counted as assertions (an exception would fail the test)",
            "total_tests": ctotal, "sites": c},
        "d_swallowed": {
            "mechanism": "AST ExceptHandler whose type is bare, Exception or BaseException (or a tuple holding "
                         "one); body shape classified; reachability from the call graph of kind f",
            "unit": "one broad except handler",
            "population": "prod and offline files (separately)",
            "blind_spot": "narrow handlers (ValueError, KeyError...) are listed with broad=false and their shape but are "
                          "not counted as swallowed; contextlib.suppress and errors swallowed by callers' "
                          "frameworks (pydantic, streamlit) are not counted",
            "denominator_prod": dden, "denominator_offline": doffden, "sites": dprod + doff},
        "e_loose_types": {
            "mechanism": "AST: Name/Attribute nodes bound to typing.Any (annotation vs other positions, plus string "
                         "annotations); tokenize COMMENT tokens matching type: ignore / pyright: ignore / noqa",
            "unit": "occurrence, per file",
            "population": "prod and offline files",
            "blind_spot": "missing annotations (implicit Any), object, cast(), dict without params are not counted",
            "rows": e},
        "f_unfinished_reachable": {
            "mechanism": "AST raise NotImplementedError + TODO/FIXME/XXX/HACK comments; owner = innermost enclosing "
                         "function; reachability by BFS over a static call graph (imports, aliases, package "
                         "re-exports, self/super methods, local x = Cls() inference, function references)",
            "unit": "one site",
            "population": "prod files",
            "blind_spot": "dynamic dispatch (getattr, string registries, duck-typed attribute calls on untyped "
                          "objects); unresolved calls are counted in populations.callgraph_unresolved_calls",
            "sites": f},
        "g_failing": {
            "mechanism": "pytest --junitxml per suite (suites.py), failures + errors listed",
            "unit": "one pytest node id or collection-error module",
            "population": "suites in suites.json",
            "blind_spot": "test dirs outside suites.py SUITES",
            **g},
    }


def controls(suites_path: Path = HERE / "suites.json") -> dict:
    """Run the same kinds on planted controls; report flag/no-flag for each."""
    cdir = HERE / "controls"
    prod = {rel(cdir / "prod_pos.py"): "ctl_pos", rel(cdir / "prod_clean.py"): "ctl_clean"}
    tests = {rel(cdir / "test_pos.py"): "ctl.test_pos", rel(cdir / "test_clean.py"): "ctl.test_clean"}
    closure = requirements_closure()
    pkg_dists = md.packages_distributions()
    G = Graph(prod)
    parent = G.reach(["ctl_pos.entry", "ctl_clean.entry"])
    a = kind_a(tests)
    b = kind_b(prod, "ctl", closure, pkg_dists)
    c, _ = kind_c(tests)
    d, _ = kind_d(prod, "ctl")
    e = kind_e(prod, "ctl")
    f = kind_f(G, parent)
    res = {}

    def chk(name, cond):
        res[name] = "PASS" if cond else "FAIL"
    pos_t, cln_t = rel(cdir / "test_pos.py"), rel(cdir / "test_clean.py")
    pos_p, cln_p = rel(cdir / "prod_pos.py"), rel(cdir / "prod_clean.py")
    akinds = {(s["path"], s["test"], s["kind"]) for s in a}
    chk("a+ unconditional skip flagged", (pos_t, "test_skipped", "mark.skip") in akinds)
    chk("a+ body pytest.fail flagged", (pos_t, "test_always_fails", "pytest.fail") in akinds)
    chk("a+ shadowed test flagged", any(s["path"] == pos_t and s["kind"] == "shadowed-by-redefinition" for s in a))
    chk("a- clean file has no site", not any(s["path"] == cln_t for s in a))
    st = {(s["path"], tuple(s["modules"])): s["status"] for s in b}
    chk("b+ stdlib guard UNREACHABLE-FALLBACK", st.get((pos_p, ("json",))) == "UNREACHABLE-FALLBACK")
    chk("b+ missing module UNREACHABLE-PRIMARY", st.get((pos_p, ("p2_no_such_module_xyz",))) == "UNREACHABLE-PRIMARY")
    chk("b- optional dev-only module LIVE", st.get((cln_p, ("hypothesis",))) == "LIVE")
    cflag = {(s["path"], s["test"]) for s in c}
    chk("c+ assertion-free test flagged", (pos_t, "test_no_assert") in cflag)
    chk("c- helper-asserting test not flagged", (cln_t, "test_via_helper") not in cflag)
    chk("c- pytest.raises test not flagged", (cln_t, "test_raises") not in cflag)
    dsw = {(s["path"], s["shape"]) for s in d if s["swallowed"]}
    chk("d+ except Exception: return default flagged", (pos_p, "RETURN") in dsw)
    chk("d+ bare except pass flagged", (pos_p, "PASS") in dsw)
    chk("d- re-raising handler not swallowed", not any(s["path"] == cln_p and s["swallowed"] for s in d))
    erow = {r["path"]: r for r in e}
    chk("e+ Any/type-ignore/noqa counted", erow.get(pos_p, {}).get("any_annotation") == 2 and erow[pos_p]["type_ignore"] == 1 and erow[pos_p]["noqa"] == 1)
    chk("e- clean file has no row", cln_p not in erow)
    fr = {(s["path"], s["kind"], s["reachable"]) for s in f}
    chk("f+ reachable NotImplementedError flagged", (pos_p, "raise NotImplementedError", True) in fr)
    chk("f+ reachable TODO flagged", (pos_p, "comment", True) in fr)
    chk("f- unreachable NotImplementedError not reachable", (cln_p, "raise NotImplementedError", False) in fr
        and (cln_p, "raise NotImplementedError", True) not in fr)
    g = kind_g(suites_path)
    if "failing" in g:
        fails = {r["node"] for r in g["failing"] if r["suite"] == "controls"}
        chk("g+ planted failing test listed", "test_pos::test_always_fails" in fails)
        chk("g- clean test file not listed", not any(n.startswith("test_clean") for n in fails))
    else:
        res["g controls"] = "ABSENT (no suites.json)"
    return res


def main() -> None:
    if "--controls" in sys.argv:
        json.dump(controls(), sys.stdout, indent=1, sort_keys=True)
        sys.stdout.write("\n")
        return
    sp = HERE / "suites.json"
    if "--suites" in sys.argv:
        sp = Path(sys.argv[sys.argv.index("--suites") + 1])
    out = census(prod_population(), offline_population(), test_population(), sp)
    out["controls"] = controls(sp)
    json.dump(out, sys.stdout, indent=1, sort_keys=True, default=str)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
