"""P3 reachability instrument: classify every passing test and census production-function reach.

Inputs  (from run_suites.sh): <outdir>/.coverage.<suite> (per-test contexts, branch data) and
        <outdir>/nodeids_<suite>.json (node ID -> outcome, recorded by p3_nodeids.py in the same run).
Output: deterministic JSON (sorted keys, no timestamps) -- audit/scratch/P3/reachability.json.

Usage: python audit/scratch/P3/reachability.py <outdir> <out.json> [--spec controls]

Test classes (mechanism = per-test coverage context  x  intraprocedural AST taint pass):
  behaviour   own-package production lines executed in the test's run/setup context AND >=1 assertion
              whose asserted value data-flows from a production call (function/method or constructor).
  interface   >=1 assertion on a production-derived value, but every such value sits under a shape
              wrapper (isinstance/type/hasattr/len/keys/is None/"k" in x/schema attrs).
  placeholder no own-package production line executed (and no shape check on a production symbol), or
              every assertion is on a double (Mock/.assert_called*), a production constant or a local value.
  UNDECIDED   own lines executed but no assertion found statically (smoke test, or assertion in an
              unresolved helper), or the test function was not found in the AST (generated test).
"""
from __future__ import annotations

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

import coverage
from radon.complexity import cc_visit

ROOT = Path(__file__).resolve().parents[3]

# ---------------------------------------------------------------- populations
SUITES = {  # suite key -> (suite dir, own production paths)
    "comlab": ("labs/comlab", ["labs/comlab/comlab", "labs/comlab/registry"]),
    "dnalab": ("labs/dnalab", ["labs/dnalab/dnalab"]),
    "dtclab": ("labs/dtclab", ["labs/dtclab/dtclab"]),
    "gaslab": ("labs/gaslab", ["labs/gaslab/gaslab"]),
    "obdlab": ("labs/obdlab", ["labs/obdlab/obdlab"]),
    "symptomlab": ("labs/symptomlab", ["labs/symptomlab/symptomlab"]),
    "vinlab": ("labs/vinlab", ["labs/vinlab/vinlab"]),
    "wired": ("apps/wired", ["apps/wired/wired"]),
    "ui": ("apps/ui", ["apps/ui/app.py", "apps/ui/ui_payload.py"]),
    # orphan suite: labs/comlab/registry/tests (outside labs/comlab testpaths; run from labs/comlab)
    "registry": ("labs/comlab", ["labs/comlab/registry"]),
}
# production import roots: dotted top-level name -> directory (or file) whose modules it names
PROD_ROOTS = {
    "comlab": "labs/comlab/comlab", "registry": "labs/comlab/registry", "dnalab": "labs/dnalab/dnalab",
    "dtclab": "labs/dtclab/dtclab", "gaslab": "labs/gaslab/gaslab", "obdlab": "labs/obdlab/obdlab",
    "symptomlab": "labs/symptomlab/symptomlab", "vinlab": "labs/vinlab/vinlab", "wired": "apps/wired/wired",
    "ui_payload": "apps/ui/ui_payload.py", "app": "apps/ui/app.py",
}
OFFLINE = ("labs/comlab/registry/tools/",)  # offline builders inside a production package (lower priority)
EXCLUDE_PARTS = ("/tests/", "/__pycache__/")

NAMED = [  # (rel file, qualname) the prompt requires in the census
    ("labs/comlab/comlab/core/fault_atlas_router.py", "execute_triage_loop"),
    ("labs/comlab/comlab/core/fault_atlas_router.py", "route"),
    ("labs/comlab/registry/integration_shim.py", "_score_rule"),
    ("labs/gaslab/gaslab/resolution.py", "apply_differentiators"),
    ("labs/gaslab/gaslab/rule_engine.py", "_definitive_match"),
    ("apps/ui/ui_payload.py", "build_diagnose_payload"),
    ("apps/wired/wired/composition.py", "_run_obdlab"),
]
# verdict-producing population for the branch census: modules that emit a diagnosis, state or verdict
VERDICT_MODULES = [
    "labs/comlab/comlab/core/fault_atlas_router.py", "labs/comlab/registry/integration_shim.py",
    "labs/comlab/comlab/core/lab_pipeline_aggregator.py", "labs/gaslab/gaslab/rule_engine.py",
    "labs/gaslab/gaslab/resolution.py", "labs/dtclab/dtclab/ranking.py", "apps/wired/wired/composition.py",
]

SHAPE_FUNCS = {"isinstance", "issubclass", "type", "hasattr", "callable", "len", "dir", "vars", "signature",
               "get_type_hints", "fields", "import_module", "find_spec", "is_dataclass", "iscoroutinefunction",
               "isclass", "isfunction"}
SHAPE_ATTRS = {"keys", "__name__", "__class__", "__module__", "__dict__", "model_fields", "__fields__",
               "__annotations__", "model_json_schema", "schema", "__members__", "__qualname__", "_fields",
               "__dataclass_fields__", "__signature__"}
DOUBLE_CTORS = {"Mock", "MagicMock", "AsyncMock", "NonCallableMock", "create_autospec", "PropertyMock",
                "SimpleNamespace"}
UNITTEST_SHAPE = {"assertIsInstance", "assertNotIsInstance", "assertIsNone", "assertIsNotNone"}


def rel(p: str | Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def prod_files(spec_roots: dict[str, str]) -> list[str]:
    out = []
    for r in sorted(set(spec_roots.values())):
        p = ROOT / r
        cands = [p] if p.suffix == ".py" else sorted(p.rglob("*.py"))
        for f in cands:
            s = "/" + rel(f)
            if any(x in s for x in EXCLUDE_PARTS) or Path(s).name.startswith("test_"):
                continue
            out.append(rel(f))
    return sorted(set(out))


# ---------------------------------------------------------------- production symbol index
class ProdIndex:
    """dotted module -> {name: 'class'|'enum'|'func'|'other'}; resolves an import to a symbol kind."""

    def __init__(self, roots: dict[str, str]):
        self.roots = roots
        self.mods: dict[str, dict[str, str]] = {}
        for top, r in roots.items():
            p = ROOT / r
            files = [p] if p.suffix == ".py" else sorted(p.rglob("*.py"))
            for f in files:
                if "/tests/" in "/" + rel(f):
                    continue
                if p.suffix == ".py":
                    dotted = top
                else:
                    parts = list(f.relative_to(p).with_suffix("").parts)
                    if parts[-1] == "__init__":
                        parts = parts[:-1]
                    dotted = ".".join([top, *parts])
                self.mods[dotted] = self._symbols(f)

    @staticmethod
    def _symbols(f: Path) -> dict[str, str]:
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            return {}
        syms: dict[str, str] = {}
        for n in tree.body:
            if isinstance(n, ast.ClassDef):
                bases = {ast.unparse(b).split(".")[-1] for b in n.bases}
                syms[n.name] = "enum" if bases & {"Enum", "StrEnum", "IntEnum", "str, Enum"} or any(
                    "Enum" in b for b in bases) else "class"
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                syms[n.name] = "func"
            elif isinstance(n, (ast.Assign, ast.AnnAssign)):
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                    for nm in ast.walk(t):
                        if isinstance(nm, ast.Name):
                            syms[nm.id] = "other"
        return syms

    def is_prod_module(self, dotted: str) -> bool:
        return dotted.split(".")[0] in self.roots

    def kind(self, dotted: str, name: str) -> str:
        if f"{dotted}.{name}" in self.mods:
            return "module"
        return self.mods.get(dotted, {}).get(name, "func")  # unknown re-export: treat as callable


# ---------------------------------------------------------------- taint pass
CALL, CTOR, REF, DOUBLE, MODULE = "CALL", "CTOR", "REF", "DOUBLE", "MODULE"


class Scope:
    """Per-module analysis context: production imports, local helpers/fixtures, resolvable test helpers."""

    def __init__(self, path: Path, idx: ProdIndex, search_roots: list[Path], depth: int = 0,
                 cache: dict | None = None):
        self.path, self.idx, self.search_roots, self.depth = path, idx, search_roots, depth
        self.cache = cache if cache is not None else {}
        self.tree = ast.parse(path.read_text(encoding="utf-8"))
        self.prod: dict[str, str] = {}      # local name -> kind (func/class/enum/other/module)
        self.ext_helpers: dict[str, tuple[Scope, ast.AST]] = {}  # name -> (scope, def) from test helper modules
        self.unresolved: set[str] = set()   # names imported from non-production, non-resolvable modules
        self.funcs: dict[str, ast.AST] = {}
        self.fixtures: dict[str, ast.AST] = {}
        self.classes: dict[str, ast.ClassDef] = {}
        self._imports()
        for n in self.tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                (self.fixtures if is_fixture(n) else self.funcs)[fixture_name(n) if is_fixture(n) else n.name] = n
            elif isinstance(n, ast.ClassDef):
                self.classes[n.name] = n
        self.summ: dict[str, dict] = {}
        self.mod_env: dict[str, set] = {}
        self.mod_env = self._module_env()

    def _resolve_file(self, dotted: str, level: int) -> Path | None:
        parts = dotted.split(".") if dotted else []
        bases = [self.path.parent] if level else self.search_roots
        if level:
            b = self.path.parent
            for _ in range(level - 1):
                b = b.parent
            bases = [b]
        for b in bases:
            for c in (b.joinpath(*parts).with_suffix(".py"), b.joinpath(*parts, "__init__.py")):
                if parts and c.is_file():
                    return c
        return None

    def sub(self, f: Path) -> Scope | None:
        if self.depth >= 3:
            return None
        key = str(f)
        if key not in self.cache:
            self.cache[key] = None
            try:
                self.cache[key] = Scope(f, self.idx, self.search_roots, self.depth + 1, self.cache)
            except (SyntaxError, UnicodeDecodeError):
                pass
        return self.cache[key]

    def _imports(self):
        for n in ast.walk(self.tree):
            if isinstance(n, ast.Import):
                for a in n.names:
                    if self.idx.is_prod_module(a.name):
                        self.prod[(a.asname or a.name).split(".")[0]] = "module"
            elif isinstance(n, ast.ImportFrom):
                mod = n.module or ""
                if n.level == 0 and self.idx.is_prod_module(mod):
                    for a in n.names:
                        self.prod[a.asname or a.name] = self.idx.kind(mod, a.name)
                    continue
                f = self._resolve_file(mod, n.level)
                if f is not None and f.resolve() != self.path.resolve():
                    s = self.sub(f)
                    for a in n.names:
                        nm = a.asname or a.name
                        if s is None:
                            self.unresolved.add(nm)
                        elif a.name in s.funcs:
                            self.ext_helpers[nm] = (s, s.funcs[a.name])
                        elif a.name in s.fixtures:
                            self.fixtures.setdefault(nm, s.fixtures[a.name])
                        elif a.name in s.prod:
                            self.prod[nm] = s.prod[a.name]
                        elif a.name in s.mod_env and s.mod_env[a.name]:
                            self.prod.setdefault(nm, "derived:" + ",".join(sorted(s.mod_env[a.name])))
                        else:
                            sub_f = s._resolve_file(a.name, 1) if f.name == "__init__.py" else None
                            if sub_f is None:
                                self.unresolved.add(nm)
                elif f is None and mod.split(".")[0] in ("tests", "fixtures", "conftest", "helpers"):
                    for a in n.names:
                        self.unresolved.add(a.asname or a.name)

    def _module_env(self) -> dict[str, set]:
        env: dict[str, set] = {}
        body = [n for n in self.tree.body if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                                                ast.ClassDef))]
        for _ in range(2):
            for st in body:
                Flow(self, env, None).stmt(st)
        return env

    # helper summary: does the return value carry production taint (unconditional or via params),
    # and which params does it assert on.
    def summary(self, fn: ast.AST) -> dict:
        key = id(fn)
        if key in self.summ:
            return self.summ[key]
        self.summ[key] = {"ret": set(), "ret_params": False, "asserts": [], "param_asserts": set()}
        params = [a.arg for a in fn.args.args + fn.args.kwonlyargs]
        env = {k: set(v) for k, v in self.mod_env.items()}
        fl = Flow(self, env, None)
        fl.run(fn.body)
        ret = set()
        nested = {n.name: n for n in fn.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for n in ast.walk(fn):
            if isinstance(n, (ast.Return, ast.Yield, ast.YieldFrom)) and n.value is not None:
                ret |= fl.taint(n.value)
                if isinstance(n.value, ast.Name) and n.value.id in nested:  # factory: returns a builder
                    ret |= self.summary(nested[n.value.id])["ret"]
        # param-dependence: mark params with a sentinel kind
        env2 = {k: set(v) for k, v in self.mod_env.items()}
        for p in params:
            env2[p] = {"PARAM"}
        fl2 = Flow(self, env2, None)
        fl2.run(fn.body)
        ret_params = any("PARAM" in fl2.taint(n.value) for n in ast.walk(fn)
                         if isinstance(n, (ast.Return, ast.Yield)) and n.value is not None)
        param_asserts = {a["kind"] for a in fl2.asserts if a.get("param")}
        self.summ[key] = {"ret": ret - {"PARAM"}, "ret_params": ret_params, "asserts": fl.asserts,
                          "param_asserts": param_asserts}
        return self.summ[key]


def is_fixture(fn) -> bool:
    return any("fixture" in ast.unparse(d) for d in fn.decorator_list)


def fixture_name(fn) -> str:
    for d in fn.decorator_list:
        if isinstance(d, ast.Call):
            for k in d.keywords:
                if k.arg == "name" and isinstance(k.value, ast.Constant):
                    return k.value.value
    return fn.name


def root_name(e: ast.AST) -> str | None:
    while isinstance(e, (ast.Attribute, ast.Subscript, ast.Call)):
        e = e.value if not isinstance(e, ast.Call) else e.func
    return e.id if isinstance(e, ast.Name) else None


class Flow:
    """Flow-insensitive taint over one function body (two passes to a fixpoint for loops)."""

    def __init__(self, scope: Scope, env: dict[str, set], cls: ast.ClassDef | None):
        self.s, self.env, self.cls = scope, env, cls
        self.asserts: list[dict] = []
        self.unresolved_calls: set[str] = set()
        self.collect = False
        self.ctx: list[set] = []  # taint of enclosing if/while tests and try bodies (control dependence)

    def ctx_t(self) -> set:
        out = set()
        for c in self.ctx:
            out |= c
        return out & {CALL, CTOR}

    # ---- expression taint
    def taint(self, e: ast.AST | None, value_only: bool = False) -> set:
        if e is None:
            return set()
        if isinstance(e, ast.Name):
            if e.id in self.env:
                return set(self.env[e.id])
            k = self.s.prod.get(e.id)
            if k is None:
                return set()
            if k.startswith("derived:"):
                return set(k[8:].split(","))
            return {MODULE} if k == "module" else {REF}
        if isinstance(e, ast.Attribute):
            if value_only and e.attr in SHAPE_ATTRS:
                return set()
            if isinstance(e.value, ast.Name) and e.value.id == "self" and self.cls is not None:
                return set(self.env.get("self." + e.attr, set()))
            t = self.taint(e.value, value_only)
            return {REF} if t == {MODULE} else t
        if isinstance(e, ast.Call):
            return self.call_taint(e, value_only)
        if isinstance(e, ast.Compare) and value_only:
            ops = e.ops
            if all(isinstance(o, (ast.Is, ast.IsNot)) for o in ops) and all(
                    isinstance(c, ast.Constant) and c.value is None for c in e.comparators):
                return set()
            if len(ops) == 1 and isinstance(ops[0], (ast.In, ast.NotIn)) and isinstance(e.left, ast.Constant):
                return set()
        if isinstance(e, ast.Lambda):
            return set()
        out = set()
        for c in ast.iter_child_nodes(e):
            if isinstance(c, ast.expr_context):
                continue
            out |= self.taint(c, value_only)
        return out

    def call_taint(self, e: ast.Call, value_only: bool) -> set:
        f = e.func
        fname = f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else "")
        args = list(e.args) + [k.value for k in e.keywords]
        if value_only and fname in SHAPE_FUNCS:
            return set()
        if value_only and isinstance(f, ast.Attribute) and f.attr in SHAPE_ATTRS:
            return set()
        if fname in DOUBLE_CTORS or fname in ("patch", "object") and root_name(f) in ("mock", "patch", "mocker"):
            return {DOUBLE}
        if isinstance(f, ast.Name):
            k = self.s.prod.get(f.id)
            if k is not None and f.id not in self.env:
                if k.startswith("derived:"):
                    return {CALL}
                return {CTOR} if k in ("class", "enum") else {CALL}
            if f.id in self.s.funcs or f.id in self.s.ext_helpers:
                sc, fn = (self.s, self.s.funcs[f.id]) if f.id in self.s.funcs else self.s.ext_helpers[f.id]
                sm = sc.summary(fn)
                t = set(sm["ret"])
                at = set()
                for a in args:
                    at |= self.taint(a)
                if sm["ret_params"]:
                    t |= at
                return t
            if f.id in self.s.unresolved:
                self.unresolved_calls.add(f.id)
            if f.id in self.env and self.env[f.id] & {CALL, CTOR}:
                return {CALL}
        ft = self.taint(f.value) if isinstance(f, ast.Attribute) else set()
        if isinstance(f, ast.Attribute):
            if isinstance(f.value, ast.Name) and f.value.id in self.s.prod and f.value.id not in self.env:
                k = self.s.prod[f.value.id]
                if k == "module":
                    sub = self.s.idx.mods.get(f.value.id, {})
                    return {CTOR} if sub.get(f.attr) in ("class", "enum") else {CALL}
                return {CALL}  # Class.method(...) / Enum(...) helpers
            if MODULE in ft:
                return {CALL}
            if ft & {CALL, CTOR, REF}:
                return {CALL} | (ft & {DOUBLE})
            if DOUBLE in ft:
                return {DOUBLE}
        out = set(ft)
        for a in args:
            out |= self.taint(a, value_only)
        return out

    # ---- statements
    def bind(self, target: ast.AST, t: set):
        t = set(t) | self.ctx_t()
        for n in ast.walk(target):
            if isinstance(n, ast.Name):
                self.env.setdefault(n.id, set()).update(t)
            elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "self":
                self.env.setdefault("self." + n.attr, set()).update(t)
        if isinstance(target, ast.Subscript):
            r = root_name(target)
            if r:
                self.env.setdefault(r, set()).update(t)

    def record(self, kind: str, node: ast.AST, t_all: set, t_val: set):
        if not self.collect:
            return
        c = self.ctx_t()
        cls = classify_assert(t_all | c, t_val | c)
        self.asserts.append({"line": node.lineno, "kind": kind, "class": cls,
                             "param": "PARAM" in t_all})

    def stmt(self, st: ast.stmt):
        if isinstance(st, ast.Assign):
            t = self.taint(st.value)
            for tg in st.targets:
                self.bind(tg, t)
        elif isinstance(st, (ast.AnnAssign, ast.AugAssign)) and st.value is not None:
            self.bind(st.target, self.taint(st.value))
        elif isinstance(st, (ast.For, ast.AsyncFor)):
            self.bind(st.target, self.taint(st.iter))
        elif isinstance(st, (ast.With, ast.AsyncWith)):
            raises = None
            for it in st.items:
                ce = it.context_expr
                if isinstance(ce, ast.Call) and getattr(ce.func, "attr", getattr(ce.func, "id", "")) in (
                        "raises", "assertRaises", "assertRaisesRegex", "warns"):
                    raises = ce
                if it.optional_vars is not None:
                    self.bind(it.optional_vars, self.taint(ce))
            if raises is not None:
                body_t = set()
                for b in st.body:  # any production-derived value used in the block (calls, mutations)
                    for n in ast.walk(b):
                        if isinstance(n, ast.Call):
                            body_t |= self.call_taint(n, False)
                        elif isinstance(n, (ast.Name, ast.Attribute)):
                            body_t |= self.taint(n) & {CALL, CTOR}
                self.record("raises", st, body_t, body_t)
        elif isinstance(st, ast.Assert):
            self.record("assert", st, self.taint(st.test), self.taint(st.test, True))
        elif isinstance(st, ast.Expr) and isinstance(st.value, ast.Call):
            self.expr_call(st.value)
        for n in ast.walk(st):
            if isinstance(n, ast.NamedExpr):
                self.bind(n.target, self.taint(n.value))
        cond = set()
        if isinstance(st, (ast.If, ast.While)):
            cond = self.taint(st.test)
        elif isinstance(st, ast.Try):  # a handler runs because the try body raised
            for b in st.body:
                for n in ast.walk(b):
                    if isinstance(n, ast.Call):
                        cond |= self.call_taint(n, False)
        for fld in ("body", "orelse", "finalbody", "handlers"):
            push = fld in ("body", "orelse") and isinstance(st, (ast.If, ast.While)) or fld == "handlers"
            if push:
                self.ctx.append(cond)
            for b in getattr(st, fld, []) or []:
                if isinstance(b, ast.ExceptHandler):
                    for bb in b.body:
                        self.stmt(bb)
                elif isinstance(b, ast.stmt) and not isinstance(b, (ast.FunctionDef, ast.AsyncFunctionDef,
                                                                     ast.ClassDef)):
                    self.stmt(b)
            if push:
                self.ctx.pop()
        if isinstance(st, ast.Match):
            for c in st.cases:
                for b in c.body:
                    self.stmt(b)

    def expr_call(self, c: ast.Call):
        f = c.func
        name = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
        args = list(c.args) + [k.value for k in c.keywords]
        if isinstance(f, ast.Attribute) and name in ("append", "extend", "update", "add", "insert",
                                                     "setdefault", "appendleft"):
            r = root_name(f.value)
            if r:
                t = set()
                for a in args:
                    t |= self.taint(a)
                self.env.setdefault(r, set()).update(t)
                return
        if name.startswith("assert_") and isinstance(f, ast.Attribute) and (
                name.startswith(("assert_called", "assert_not_called", "assert_any_call", "assert_has_calls",
                                 "assert_awaited"))):
            self.record("mock_assert", c, {DOUBLE}, {DOUBLE})
            return
        if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "self" and \
                name.startswith("assert"):
            ta, tv = set(), set()
            for i, a in enumerate(args):
                ta |= self.taint(a)
                if name in UNITTEST_SHAPE or (name in ("assertIn", "assertNotIn") and i == 0 and
                                              isinstance(a, ast.Constant)):
                    continue
                tv |= self.taint(a, True)
            if name in ("assertIn", "assertNotIn") and args and isinstance(args[0], ast.Constant):
                tv = set()
            self.record("unittest", c, ta, tv)
            return
        if name == "raises" and args:  # pytest.raises(E, fn, *args)
            t = set()
            for a in args[1:]:
                t |= self.taint(a)
            t2 = self.taint(ast.Call(func=args[1], args=[], keywords=[])) if len(args) > 1 else set()
            self.record("raises", c, t | t2, t | t2)
            return
        if isinstance(f, ast.Name) and (f.id in self.s.funcs or f.id in self.s.ext_helpers):
            sc, fn = (self.s, self.s.funcs[f.id]) if f.id in self.s.funcs else self.s.ext_helpers[f.id]
            sm = sc.summary(fn)
            at = set()
            for a in args:
                at |= self.taint(a)
            for a in sm["asserts"]:
                if not a.get("param") and a["class"] != "NONE":
                    self.asserts.append({**a, "kind": "helper:" + f.id, "line": c.lineno})
            if sm["param_asserts"] and at:
                for k in sm["param_asserts"]:
                    cls = classify_assert(at, at if k in ("VALUE", "VALUE_CTOR") else set())
                    self.asserts.append({"line": c.lineno, "kind": "helper:" + f.id, "class": cls,
                                         "param": False})
            return
        if name.startswith("assert") and isinstance(f, (ast.Name, ast.Attribute)):
            ta = set()
            for a in args:
                ta |= self.taint(a)
            tv = set()
            for a in args:
                tv |= self.taint(a, True)
            if isinstance(f, ast.Name) and f.id in self.s.unresolved:
                self.unresolved_calls.add(f.id)
            self.record("assert_fn", c, ta, tv)
            return
        if isinstance(f, ast.Name) and f.id in self.s.unresolved:
            self.unresolved_calls.add(f.id)

    def run(self, body: list[ast.stmt]):
        for p in range(2):
            self.collect = p == 1
            if self.collect:
                self.asserts = []
            for st in body:
                self.stmt(st)


def classify_assert(t_all: set, t_val: set) -> str:
    if CALL in t_val:
        return "VALUE"
    if CTOR in t_val:
        return "VALUE_CTOR"
    if t_all & {CALL, CTOR, REF, MODULE}:
        return "SHAPE" if not (t_val & {REF}) else "CONST"
    if DOUBLE in t_all:
        return "DOUBLE"
    return "NONE"


# ---------------------------------------------------------------- per-test analysis
def find_test(scope: Scope, parts: list[str]):
    name = parts[-1].split("[")[0]
    cls = None
    body = scope.tree.body
    for p in parts[:-1]:
        nxt = [n for n in body if isinstance(n, ast.ClassDef) and n.name == p]
        if not nxt:
            return None, None
        cls = nxt[0]
        body = cls.body
    fns = [n for n in body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name]
    if not fns and cls is not None:  # inherited test method
        for b in cls.bases:
            bn = ast.unparse(b)
            if bn in scope.classes:
                fns = [n for n in scope.classes[bn].body if isinstance(n, (ast.FunctionDef,
                                                                           ast.AsyncFunctionDef))
                       and n.name == name]
    return (fns[-1] if fns else None), cls


def conftest_fixtures(test_file: Path, suite_dir: Path, idx, roots, cache) -> dict[str, tuple]:
    out: dict[str, tuple] = {}
    d = test_file.parent
    chain = []
    while True:
        chain.append(d)
        if d == suite_dir or d == d.parent:
            break
        d = d.parent
    for d in reversed(chain):
        c = d / "conftest.py"
        if c.is_file():
            key = str(c)
            if key not in cache:
                cache[key] = Scope(c, idx, roots, 0, cache)
            sc = cache[key]
            for k, fn in sc.fixtures.items():
                out[k] = (sc, fn)
    return out


def analyse_test(nodeid: str, suite_dir: Path, idx: ProdIndex, cache: dict) -> dict:
    fpart, *parts = nodeid.split("::")
    f = (suite_dir / fpart).resolve()
    roots = [suite_dir, suite_dir.parent, f.parent]
    key = str(f)
    if key not in cache:
        cache[key] = Scope(f, idx, roots, 0, cache)
    sc = cache[key]
    fn, cls = find_test(sc, parts)
    if fn is None:
        return {"found": False}
    fixtures = conftest_fixtures(f, suite_dir, idx, roots, cache)
    for k, v in sc.fixtures.items():
        fixtures[k] = (sc, v)
    env = {k: set(v) for k, v in sc.mod_env.items()}
    # fixtures requested by parameter (also via usefixtures/autouse -- not traced: blind spot)
    def fixture_taint(name, seen):
        if name not in fixtures or name in seen:
            return set()
        fsc, ffn = fixtures[name]
        sm = fsc.summary(ffn)
        t = set(sm["ret"])
        if sm["ret_params"]:
            for a in ffn.args.args:
                t |= fixture_taint(a.arg, seen | {name})
        return t
    for a in fn.args.args + fn.args.kwonlyargs:
        if a.arg in ("self", "cls"):
            continue
        env[a.arg] = fixture_taint(a.arg, set())
    if cls is not None:  # setUp / setup_method / class fixtures assigning self.<attr>
        for m in cls.body:
            if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)) and (
                    m.name in ("setUp", "setup_method", "setup_class", "setUpClass") or is_fixture(m)):
                fl0 = Flow(sc, env, cls)
                fl0.run(m.body)
    fl = Flow(sc, env, cls)
    fl.run(fn.body)
    return {"found": True, "asserts": fl.asserts, "unresolved_calls": sorted(fl.unresolved_calls),
            "line": fn.lineno, "file": rel(f)}


def classify(info: dict, own_lines: int, other_lines: int) -> tuple[str, str]:
    if not info.get("found"):
        return "UNDECIDED", "test function not found in AST (generated or dynamic)"
    classes = [a["class"] for a in info["asserts"]]
    has = set(classes)
    if own_lines == 0:
        if has & {"SHAPE"} and not has & {"VALUE", "VALUE_CTOR"}:
            return "interface", "shape-only assertion on a production symbol; no own line executed"
        if has & {"VALUE", "VALUE_CTOR"}:
            return "UNDECIDED", ("executed value assertion on a production call that ran no own Python line "
                                 "(declarative pydantic/enum/dataclass code: invisible to line coverage)")
        why = "no own-package production line executed"
        if other_lines:
            why += f" (executes {other_lines} lines of other packages)"
        return "placeholder", why
    if "VALUE" in has:
        return "behaviour", "assertion data-flows from a production call"
    if "VALUE_CTOR" in has:
        return "behaviour", "assertion data-flows from a production constructor only (ctor_only)"
    if "SHAPE" in has:
        return "interface", "only shape/type/presence assertions on production values"
    if has & {"CONST", "DOUBLE", "NONE"}:
        return "placeholder", "assertions only on " + "/".join(sorted(has & {"CONST", "DOUBLE", "NONE"})).lower()
    if info.get("not_executed"):
        return "placeholder", "no assertion executed (all assertion lines skipped at run time)"
    if info["unresolved_calls"]:
        return "UNDECIDED", "no assertion found; calls unresolved helper(s) " + ",".join(info["unresolved_calls"])
    return "UNDECIDED", "no assertion found statically (smoke test: passes if nothing raises)"


# ---------------------------------------------------------------- function census
def functions_of(path: Path) -> list[dict]:
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    cc = {}
    for b in cc_visit(src):
        cc[(b.name, b.lineno)] = b.complexity
        for m in getattr(b, "methods", []) or []:
            cc[(m.name, m.lineno)] = m.complexity
        for c in getattr(b, "closures", []) or []:
            cc[(c.name, c.lineno)] = c.complexity
    out = []

    def visit(node, prefix):
        for n in ast.iter_child_nodes(node):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                q = prefix + n.name
                first = n.body[0]
                if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
                        and len(n.body) > 1:
                    first = n.body[1]
                out.append({"qualname": q, "line": n.lineno, "end": n.end_lineno, "body_start": first.lineno,
                            "cc": cc.get((n.name, n.lineno)), "nested": [(c.lineno, c.end_lineno) for c in
                                                                          ast.walk(n) if c is not n and
                                                                          isinstance(c, (ast.FunctionDef,
                                                                                         ast.AsyncFunctionDef,
                                                                                         ast.Lambda))]})
                visit(n, q + ".")
            elif isinstance(n, ast.ClassDef):
                visit(n, prefix + n.name + ".")
    visit(tree, "")
    return out


def is_named(f: str, q: str) -> bool:  # a NAMED entry matches a function or a method of that name
    return any(f == a and (q == b or q.endswith("." + b)) for a, b in NAMED)


def main(outdir: str, out_json: str, spec: str = "repo"):
    global SUITES, PROD_ROOTS, NAMED, VERDICT_MODULES
    if spec == "controls":
        from controls import spec as cspec  # noqa: E402  (planted-control spec)
        SUITES, PROD_ROOTS, NAMED, VERDICT_MODULES = cspec.SUITES, cspec.PROD_ROOTS, cspec.NAMED, cspec.VERDICT
    od = Path(outdir)
    idx = ProdIndex(PROD_ROOTS)
    pfiles = prod_files(PROD_ROOTS)
    owner = set(pfiles)

    def owns(s: str, f: str) -> bool:
        return any(f == o or f.startswith(o + "/") for o in SUITES[s][1])
    # per-test lines from contexts + union data
    union = coverage.CoverageData(no_disk=True)
    line_ctx: dict[str, dict[int, set]] = defaultdict(lambda: defaultdict(set))
    results, suite_status = {}, {}
    test_exec: dict[tuple, set] = defaultdict(set)  # (test key, test file) -> executed test-file lines
    for s, (sdir, _) in SUITES.items():
        df, nf = od / f".coverage.{s}", od / f"nodeids_{s}.json"
        if not df.exists() or not nf.exists():
            suite_status[s] = "ABSENT"
            continue
        suite_status[s] = "RAN"
        results[s] = json.loads(nf.read_text())["results"]
        d = coverage.CoverageData(basename=str(df))
        d.read()
        union.update(d)
        for mf in d.measured_files():
            r = rel(mf)
            if r not in owner:
                if "/tests/" in "/" + r or Path(r).name.startswith(("test_", "conftest")):
                    for ln, ctxs in d.contexts_by_lineno(mf).items():
                        for c in ctxs:
                            nid, _, phase = c.rpartition("|")
                            if c and phase == "run":
                                test_exec[(f"{s}::{nid}", r)].add(ln)
                continue
            for ln, ctxs in d.contexts_by_lineno(mf).items():
                for c in ctxs:
                    if not c:
                        line_ctx[r][ln].add("<import>")
                        continue
                    nid, _, phase = c.rpartition("|")
                    if phase in ("run", "setup", "teardown"):
                        line_ctx[r][ln].add(f"{s}::{nid}")
    tests_lines: dict[str, set] = defaultdict(set)
    for f, lm in line_ctx.items():
        for ln, ts in lm.items():
            for t in ts:
                if t != "<import>":
                    tests_lines[t].add((f, ln))
    # classify
    cache: dict = {}
    tests = {}
    for s in sorted(results):
        sdir = ROOT / SUITES[s][0]
        for nid, outc in sorted(results[s].items()):
            if outc != "passed":
                continue
            key = f"{s}::{nid}"
            try:
                info = analyse_test(nid, sdir, idx, cache)
            except (SyntaxError, OSError, RecursionError) as ex:
                info = {"found": False, "error": type(ex).__name__}
            if info.get("found"):  # keep only assertions whose line executed in this test's run phase
                ran = test_exec.get((key, info["file"]), set())
                info["not_executed"] = [a for a in info["asserts"] if a["line"] not in ran]
                info["asserts"] = [a for a in info["asserts"] if a["line"] in ran]
            own = sum(1 for f, _ in tests_lines[key] if owns(s, f))
            other = len(tests_lines[key]) - own
            cls, why = classify(info, own, other)
            ac = defaultdict(int)
            for a in info.get("asserts", []):
                ac[a["class"]] += 1
            tests[key] = {"suite": s, "class": cls, "reason": why, "own_lines": own, "other_lines": other,
                          "assert_classes": dict(sorted(ac.items())),
                          "unresolved_calls": info.get("unresolved_calls", []),
                          "asserts_not_executed": len(info.get("not_executed", []))}
    # function census (union coverage)
    cov = coverage.Coverage(data_file=None, branch=True)
    cov._data = union  # noqa: SLF001 -- analyse the in-memory union
    cov._inited = True
    funcs = {}
    branches = {}
    for f in pfiles:
        p = ROOT / f
        try:
            an = cov._analyze(str(p))  # noqa: SLF001
            stmts, executed = set(an.statements), set(an.executed)
            missing_arcs = an.missing_branch_arcs()
        except Exception as ex:  # noqa: BLE001 -- unparsable by coverage
            funcs[f] = {"error": type(ex).__name__}
            continue
        for fn in functions_of(p):
            nested = fn["nested"]
            body = {ln for ln in stmts if fn["body_start"] <= ln <= fn["end"] and
                    not any(a < ln <= b for a, b in nested)}
            hit = body & executed
            ctx = set()
            for ln in hit:
                ctx |= line_ctx.get(f, {}).get(ln, set())
            reached_by_test = sorted(c for c in ctx if c != "<import>")
            q = f"{f}::{fn['qualname']}"
            funcs[q] = {"file": f, "qualname": fn["qualname"], "line": fn["line"], "cc": fn["cc"],
                        "stmts": len(body), "hit": len(hit), "reached": bool(reached_by_test),
                        "import_only": bool(hit) and not reached_by_test,
                        "n_tests": len(reached_by_test), "suites": sorted({c.split("::")[0]
                                                                            for c in reached_by_test}),
                        "offline": f.startswith(OFFLINE)}
            if f in VERDICT_MODULES or is_named(f, fn["qualname"]):
                mb = []
                for src_ln, dests in sorted(missing_arcs.items()):
                    if fn["body_start"] <= src_ln <= fn["end"] and not any(a < src_ln <= b for a, b in nested):
                        for d in sorted(dests):
                            mb.append([src_ln, d])
                tot = sum(1 for (a, b) in an.arc_possibilities if fn["body_start"] <= a <= fn["end"]
                          and a in an._branch_lines() and not any(x < a <= y for x, y in nested))  # noqa: SLF001
                branches[q] = {"missing_branch_arcs": mb, "branch_arcs_total": tot}
    data = {"suite_status": suite_status, "tests": tests, "functions": funcs, "verdict_branches": branches,
            "named": sorted(k for k, v in funcs.items() if "qualname" in v and is_named(v["file"], v["qualname"]))}
    Path(out_json).write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "repo")
