"""P5 instrument — dependency and deploy surface. Writes audit/scratch/P5/surface.json.

usage (repo root):  python audit/scratch/P5/surface.py
env:
  P5_RENDER     a Render-simulated tree + venv built by render_build.sh (required for sections 1, 3)
  P5_PIPAUDIT   path of a pip-audit executable (section 3; absent -> ABSENT, never 0)
  P5_PY310, P5_PY311  interpreters for the requires-python probe (section 2b; absent -> ABSENT)

Sections (each carries its own controls block):
  1 render_cases   AppTest drive of root app.py inside the Render venv (cases.py, one process each)
  2 inventory      AST import census per production package vs declared dependencies
  3 pip_audit      known-vulnerability query for the deployed third-party closure
  4 capabilities   static AST sink census of the first-party closure (+ dynamic events from 1)
  5 secrets        regex census of tracked files (path + kind only, never the value)
Deterministic: no timestamps, sorted keys and lists, temp/absolute paths normalised.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CTRL = HERE / "controls"
RENDER = Path(os.environ["P5_RENDER"]).resolve() if os.environ.get("P5_RENDER") else None
RPY = RENDER / ".venv/bin/python" if RENDER else None
STD = set(sys.stdlib_module_names) | {"__future__"}

# production packages (prompt scope): top-level import name -> source dir, manifest
PKGS = {
    "comlab": ("labs/comlab/comlab", "labs/comlab"),
    "registry": ("labs/comlab/registry", None),  # imported by comlab, shipped by no manifest
    "dnalab": ("labs/dnalab/dnalab", "labs/dnalab"),
    "dtclab": ("labs/dtclab/dtclab", "labs/dtclab"),
    "gaslab": ("labs/gaslab/gaslab", "labs/gaslab"),
    "obdlab": ("labs/obdlab/obdlab", "labs/obdlab"),
    "symptomlab": ("labs/symptomlab/symptomlab", "labs/symptomlab"),
    "vinlab": ("labs/vinlab/vinlab", "labs/vinlab"),
    "wired": ("apps/wired/wired", "apps/wired"),
    "ui": ("apps/ui", "."),  # app.py + ui_payload.py only (what the root shim reaches); manifest = root
}
UI_FILES = ["app.py", "ui_payload.py"]
OFFLINE = {"vinlab_tools": "labs/vinlab/tools"}  # lower priority population, reported apart
FIRST_PARTY = {"comlab", "registry", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab",
               "wired", "ui_payload"}
DIST_OF_FIRST = {k: k for k in FIRST_PARTY} | {"ui_payload": None, "registry": None}


def env_clean() -> dict:
    return {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/root"),
            "PYTHONDONTWRITEBYTECODE": "1", "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE", ""),
            "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE", ""),
            "PIP_CERT": os.environ.get("PIP_CERT", "")}


def rel(p) -> str:
    s = str(p)
    for base, tag in ((str(RENDER) if RENDER else None, "<render>"), (str(ROOT), "<repo>")):
        if base:
            s = s.replace(base + "/", "").replace(base, tag)
    return s


# ---------------------------------------------------------------- 1 render cases
CASES = [("blank", "faithful"), ("unticked", "faithful"), ("minimal", "faithful"),
         ("minimal_vin", "faithful"), ("taint", "faithful"),
         ("blank", "comlab"), ("unticked", "comlab"), ("minimal", "comlab"),
         ("minimal_vin", "comlab"), ("taint", "comlab"),
         ("control_pos", "faithful"), ("control_clean", "faithful")]


def run_case(case: str, mode: str) -> dict:
    p = subprocess.run([str(RPY), str(HERE / "cases.py"), str(RENDER), case, mode],
                       capture_output=True, text=True, env=env_clean(), cwd=str(RENDER), timeout=600)
    line = [x for x in p.stdout.splitlines() if x.startswith("P5JSON ")]
    if not line:
        return {"case": case, "mode": mode, "status": "ABSENT", "stderr_tail": p.stderr[-400:]}
    d = json.loads(line[0][7:])
    d["first_party_events"] = sorted(e for e in d.pop("capability_events")
                                     if not e[1].startswith("third-party"))
    d.pop("loaded_top_modules", None)
    return d


def section_cases() -> dict:
    if not RPY or not RPY.exists():
        return {"status": "ABSENT", "why": "P5_RENDER not set or venv missing"}
    out = [run_case(c, m) for c, m in CASES]
    pos = next(o for o in out if o["case"] == "control_pos")
    clean = next(o for o in out if o["case"] == "control_clean")
    ev = lambda o, k: any(e[0] == k for e in o.get("first_party_events", []))  # noqa: E731
    controls = {
        "positive": {"must_flag": "subprocess + file write + user text in unsafe HTML",
                     "flagged": ev(pos, "subprocess.Popen") and ev(pos, "open")
                     and pos.get("taint_in_unsafe_html", 0) > 0},
        "clean": {"must_not_flag": "escaped user text, no subprocess/write",
                  "flagged": bool(clean.get("first_party_events")) or clean.get("taint_in_unsafe_html", 0) > 0},
    }
    return {"status": "RAN", "mechanism": "streamlit.testing AppTest on root app.py + sys.addaudithook",
            "cases": [o for o in out if not o["case"].startswith("control")], "controls": controls}


def render_meta() -> dict:
    if not RPY or not RPY.exists():
        return {"status": "ABSENT"}
    code = ("import json,sys,importlib.metadata as m;"
            "d={x.metadata['Name'].lower().replace('_','-'):x.version for x in m.distributions()};"
            "t={k:sorted({v.lower().replace('_','-') for v in vs}) for k,vs in m.packages_distributions().items()};"
            "print(json.dumps({'python':sys.version.split()[0],'dists':d,'top':t},sort_keys=True))")
    p = subprocess.run([str(RPY), "-I", "-c", code], capture_output=True, text=True, env=env_clean())
    meta = json.loads(p.stdout)
    pipv = subprocess.run([str(RPY), "-m", "pip", "--version"], capture_output=True, text=True).stdout.split()[1]
    meta["pip"] = pipv
    return meta


# ---------------------------------------------------------------- 2 inventory
def py_files(pkg: str, d: str) -> list[Path]:
    base = ROOT / d
    if pkg == "ui":
        return [base / f for f in UI_FILES]
    return sorted(f for f in base.rglob("*.py") if "tests" not in f.relative_to(base).parts
                  and "__pycache__" not in f.parts)


def guarded(node, parents) -> bool:
    for p in parents:
        if isinstance(p, ast.Try) and any(
            isinstance(h.type, ast.Name) and h.type.id in ("ImportError", "ModuleNotFoundError", "Exception")
            or isinstance(h.type, ast.Tuple) for h in p.handlers if h.type is not None
        ):
            return True
    return False


def imports_of(files: list[Path]) -> tuple[list[dict], int]:
    """Every import statement: (top name, file:line, guarded, lazy). Returns (rows, dynamic_unresolved)."""
    rows, dyn = [], 0
    for f in files:
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        stack: list = []

        def visit(n, parents):
            nonlocal dyn
            names = []
            if isinstance(n, ast.Import):
                names = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.level == 0 and n.module:
                names = [n.module]
            elif isinstance(n, ast.Call):
                fn = n.func
                fname = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
                if fname in ("import_module", "__import__", "find_spec"):
                    if n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                        names = [n.args[0].value]
                    else:
                        dyn += 1
            for nm in names:
                rows.append({"top": nm.split(".")[0], "at": f"{rel(f)}:{n.lineno}",
                             "guarded": guarded(n, parents),
                             "lazy": any(isinstance(p, (ast.FunctionDef, ast.AsyncFunctionDef)) for p in parents)})
            for c in ast.iter_child_nodes(n):
                visit(c, parents + [n])

        visit(tree, stack)
    return rows, dyn


REQ_RE = re.compile(r"^\s*([A-Za-z0-9_.\-]+)\s*(\[[^\]]*\])?\s*([<>=!~][^#;]*)?")


def norm(n: str) -> str:
    return re.sub(r"[-_.]+", "-", n).lower()


def parse_reqfile(p: Path) -> list[dict]:
    out, section = [], "runtime"
    if not p.exists():
        return out
    for line in p.read_text().splitlines():
        s = line.strip()
        if s.startswith("#"):
            # a section header is a comment that STARTS with the section word ("# Runtime", "# Dev / test",
            # "# Build-time"); prose comments ("# Render build manifest ...") do not switch sections
            m = re.match(r"#\s*(runtime|dev|test|build)", s, re.I)
            if m:
                w = m.group(1).lower()
                section = "dev" if w in ("dev", "test") else w
            continue
        if not s or s.startswith("-e"):
            if s.startswith("-e"):
                out.append({"name": norm(Path(s[2:].strip()).name), "spec": "editable", "section": "runtime"})
            continue
        m = REQ_RE.match(s)
        if m:
            out.append({"name": norm(m.group(1)), "spec": (m.group(3) or "").strip(), "section": section})
    return out


def manifest(mdir: str | None) -> dict:
    if mdir is None:
        return {"pyproject": None, "requirements": None, "requires_python": None, "extras": []}
    d = ROOT / mdir
    pp = d / "pyproject.toml"
    proj = tomllib.loads(pp.read_text())["project"] if pp.exists() else None
    deps = []
    if proj:
        for r in proj.get("dependencies", []):
            m = REQ_RE.match(r)
            deps.append({"name": norm(m.group(1)), "spec": (m.group(3) or "").strip()})
    return {"pyproject": deps if proj else None,
            "requirements": parse_reqfile(d / "requirements.txt") if (d / "requirements.txt").exists() else None,
            "requires_python": proj.get("requires-python") if proj else None,
            "extras": sorted((proj or {}).get("optional-dependencies", {}))}


def classify(top: str, own: str, topmap: dict) -> tuple[str, str | None]:
    if top in STD:
        return "stdlib", None
    if top == own or (own == "ui" and top == "ui_payload"):
        return "self", None
    if top in FIRST_PARTY:
        return "first_party", DIST_OF_FIRST.get(top)
    if top in topmap:
        return "third_party", topmap[top][0]
    return "UNADJUDICATED", None


def inventory_one(pkg: str, files: list[Path], declared: set[str], topmap: dict) -> dict:
    rows, dyn = imports_of(files)
    by_dist: dict = defaultdict(lambda: {"sites": 0, "hard": 0})
    unadj = Counter()
    for r in rows:
        kind, dist = classify(r["top"], pkg, topmap)
        r["kind"] = kind
        if kind == "UNADJUDICATED":
            unadj[r["top"]] += 1
            continue
        if kind in ("first_party", "third_party"):
            key = dist or f"<no-dist:{r['top']}>"
            by_dist[key]["sites"] += 1
            by_dist[key]["hard"] += 0 if r["guarded"] else 1
    used = {k for k in by_dist}
    undeclared = sorted(k for k in used if k not in declared)
    unused = sorted(d for d in declared if d not in used)
    unadj_sites = [r["at"] + " " + r["top"] for r in rows if r["kind"] == "UNADJUDICATED"]
    return {"files": len(files), "import_sites": len(rows), "dynamic_unresolved": dyn,
            "by_kind": dict(sorted(Counter(r["kind"] for r in rows).items())),
            "used_dists": {k: dict(v) for k, v in sorted(by_dist.items())},
            "declared": sorted(declared), "undeclared_imports": undeclared,
            "declared_unused": unused,
            "UNADJUDICATED": {"names": dict(sorted(unadj.items())), "sites": sorted(unadj_sites)}}


def section_inventory(meta: dict) -> dict:
    topmap = meta.get("top", {}) if meta.get("status") != "ABSENT" else {}
    root_req = parse_reqfile(ROOT / "requirements.txt")
    out: dict = {"status": "RAN" if topmap else "INCOMPLETE",
                 "mechanism": "ast walk of every .py (tests excluded): Import, ImportFrom(level 0), "
                              "import_module/__import__/find_spec with a literal; top name -> dist via "
                              "the Render venv's importlib.metadata.packages_distributions()",
                 "unit": "import site (statement) and distribution",
                 "blind_spot": "non-literal dynamic imports (counted in dynamic_unresolved); "
                               "imports executed only via exec/runpy strings; vendored code",
                 "root_requirements": root_req, "packages": {}}
    for pkg, (d, mdir) in PKGS.items():
        man = manifest(mdir) if pkg != "ui" else {"pyproject": None, "requirements": root_req,
                                                   "requires_python": None, "extras": []}
        declared = set()
        for src in (man["pyproject"] or []), (man["requirements"] or []):
            declared |= {x["name"] for x in src if x.get("section", "runtime") == "runtime"}
        inv = inventory_one(pkg, py_files(pkg, d), declared, topmap)
        inv["manifest"] = man
        if man["pyproject"] is not None and man["requirements"] is not None:
            a = {x["name"]: x["spec"] for x in man["pyproject"]}
            b = {x["name"]: x["spec"] for x in man["requirements"] if x["section"] == "runtime"}
            inv["pyproject_vs_requirements"] = {
                "only_pyproject": sorted(set(a) - set(b)), "only_requirements": sorted(set(b) - set(a)),
                "spec_differs": sorted(f"{k}: pyproject '{a[k]}' vs requirements '{b[k]}'"
                                       for k in set(a) & set(b) if a[k] != b[k]),
                "requirements_non_runtime": sorted(f"{x['name']} ({x['section']})" for x in man["requirements"]
                                                   if x["section"] != "runtime")}
        out["packages"][pkg] = inv
    for name, d in OFFLINE.items():
        out["offline_" + name] = inventory_one(name, sorted((ROOT / d).rglob("*.py")), set(), topmap)
    # specs across all manifests + resolved version check
    specs: dict = defaultdict(dict)
    for x in root_req:
        specs[x["name"]]["requirements.txt"] = x["spec"]
    for pkg, (d, mdir) in PKGS.items():
        if mdir and mdir != ".":
            man = manifest(mdir)
            for x in man["pyproject"] or []:
                specs[x["name"]][f"{mdir}/pyproject.toml"] = x["spec"]
            for x in man["requirements"] or []:
                specs[x["name"]][f"{mdir}/requirements.txt ({x['section']})"] = x["spec"]
    dists = meta.get("dists", {})
    from packaging.specifiers import SpecifierSet  # audit venv has packaging (pip dep)
    rows = {}
    for n, by in sorted(specs.items()):
        if n in FIRST_PARTY:
            continue
        v = dists.get(n)
        bad = [f"{k} '{s}'" for k, s in by.items() if s and s != "editable" and v and v not in SpecifierSet(s)]
        rows[n] = {"specs": dict(sorted(by.items())), "resolved_in_render": v,
                   "pinned_anywhere": any(s.startswith("==") for s in by.values()),
                   "distinct_specs": len(set(by.values())), "resolved_violates": bad}
    out["spec_matrix"] = rows
    third = {k: v for k, v in dists.items() if k not in FIRST_PARTY and k not in ("pip",)}
    out["deployed_closure"] = {"third_party_dists": len(third),
                               "pinned_by_a_manifest": sorted(n for n, r in rows.items() if r["pinned_anywhere"]),
                               "unpinned_transitive": len([n for n in third if n not in rows or not rows[n]["pinned_anywhere"]]),
                               "lockfile": sorted(p.name for p in ROOT.glob("*.lock")) + sorted(
                                   p.name for p in ROOT.glob("constraints*.txt"))}
    # planted controls
    cpos = inventory_one("inv_pos", sorted((CTRL / "inv_pos").rglob("*.py")), {"requests"}, topmap)
    cclean = inventory_one("inv_clean", sorted((CTRL / "inv_clean").rglob("*.py")), {"pyyaml"}, topmap)
    out["controls"] = {
        "positive": {"must_flag": "imports yaml undeclared; declares requests unused",
                     "flagged": cpos["undeclared_imports"] == ["pyyaml"] and cpos["declared_unused"] == ["requests"]},
        "clean": {"must_not_flag": "declares pyyaml, imports yaml",
                  "flagged": bool(cclean["undeclared_imports"] or cclean["declared_unused"])}}
    out["requires_python_probe"] = requires_python_probe()
    return out


def requires_python_probe() -> dict:
    """Install a package on the oldest interpreter its requires-python admits, then import it."""
    res = {}
    for pkg, var in (("comlab", "P5_PY310"), ("dtclab", "P5_PY311"), ("gaslab", "P5_PY311"),
                     ("obdlab", "P5_PY311"), ("symptomlab", "P5_PY311"), ("vinlab", "P5_PY311")):
        py = os.environ.get(var)
        claim = manifest(PKGS[pkg][1])["requires_python"]
        if not py:
            res[pkg] = {"claim": claim, "status": "ABSENT"}
            continue
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(["uv", "venv", "-q", "-p", py, td + "/v"], capture_output=True)
            import shutil  # install from a copy so the build backend leaves no build/ in the repo
            src = shutil.copytree(ROOT / PKGS[pkg][1], td + "/src", ignore=shutil.ignore_patterns(
                "build", "*.egg-info", "__pycache__", "graph", "research", "wiki", "docs", "tests"))
            inst = subprocess.run(["uv", "pip", "install", "-q", "-p", td + "/v/bin/python", src],
                                  capture_output=True, text=True)
            imp = subprocess.run([td + "/v/bin/python", "-I", "-c",
                                  f"import importlib,pkgutil,{pkg};"
                                  f"[importlib.import_module(m.name) for m in pkgutil.walk_packages({pkg}.__path__,'{pkg}.')]"],
                                 capture_output=True, text=True, cwd=td)
            ver = subprocess.run([td + "/v/bin/python", "-c", "import sys;print(sys.version.split()[0])"],
                                 capture_output=True, text=True).stdout.strip()
        err = (imp.stderr.strip().splitlines() or [""])[-1]
        res[pkg] = {"claim": claim, "interpreter": ".".join(ver.split(".")[:2]),
                    "install_ok": inst.returncode == 0, "import_all_ok": imp.returncode == 0,
                    "error": rel(err)[:200]}
    return res


# ---------------------------------------------------------------- 3 pip-audit
def run_pip_audit(reqs: list[str]) -> dict:
    exe = os.environ.get("P5_PIPAUDIT")
    if not exe or not Path(exe).exists():
        return {"status": "ABSENT", "why": "pip-audit not installed (P5_PIPAUDIT)"}
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        fh.write("\n".join(reqs) + "\n")
        path = fh.name
    p = subprocess.run([exe, "-r", path, "--no-deps", "--disable-pip", "-f", "json",
                        "--progress-spinner", "off", "-s", "pypi"], capture_output=True, text=True, timeout=900)
    os.unlink(path)
    try:
        data = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"status": "ABSENT", "why": "pip-audit output unparseable: " + p.stderr[-300:]}
    deps = data.get("dependencies", [])
    vulns = sorted({(d["name"], d["version"], v["id"], ",".join(sorted(v.get("aliases", []))),
                    ",".join(sorted(v.get("fix_versions", [])))) for d in deps for v in d.get("vulns", [])})
    skipped = sorted(d["name"] for d in deps if d.get("skip_reason"))
    return {"status": "RAN" if not skipped else "INCOMPLETE", "audited": len(deps) - len(skipped),
            "skipped": skipped, "vulns": [list(v) for v in vulns]}


def section_pip_audit(meta: dict) -> dict:
    if meta.get("status") == "ABSENT":
        return {"status": "ABSENT", "why": "no Render venv"}
    reqs = sorted(f"{n}=={v}" for n, v in meta["dists"].items() if n not in FIRST_PARTY and n != "pip")
    main = run_pip_audit(reqs)
    pipself = run_pip_audit([f"pip=={meta['pip']}"])  # build-time tool, reported apart
    pos = run_pip_audit(["requests==2.19.0"])
    clean = run_pip_audit(["six==1.17.0"])
    main.update({"mechanism": "pip-audit -r <frozen third-party closure> --no-deps -s pypi (PyPI JSON advisories)",
                 "unit": "distribution==version", "population": "every non-editable dist in the Render venv",
                 "blind_spot": "first-party editable labs (not on PyPI); advisories absent from PyPI/OSV; "
                               "reachability is not decided by the tool",
                 "build_tool_pip": pipself,
                 "controls": {"positive": {"must_flag": "requests==2.19.0 (CVE-2018-18074)",
                                           "flagged": bool(pos.get("vulns")), "status": pos.get("status")},
                              "clean": {"must_not_flag": "six==1.17.0",
                                        "flagged": bool(clean.get("vulns")), "status": clean.get("status")}}})
    return main


# ---------------------------------------------------------------- 4 capabilities (static)
SINKS = {
    "subprocess": re.compile(r"^(subprocess\.\w+|os\.(system|popen|exec\w*|spawn\w*|posix_spawn\w*))$"),
    "socket": re.compile(r"^(socket\.\w+|urllib\.request\.\w+|requests\.\w+|http\.client\.\w+|httpx\.\w+|"
                         r"smtplib\.\w+|ftplib\.\w+|webbrowser\.open\w*)$"),
    "file_write": re.compile(r"^(.*\.(write_text|write_bytes|mkdir|unlink|touch|rmdir)|"
                             r"os\.(remove|unlink|rename|replace|mkdir|makedirs|rmdir)|"
                             r"shutil\.\w+|tempfile\.\w+|sqlite3\.connect)$"),
}


def dotted(fn) -> str:
    parts = []
    while isinstance(fn, ast.Attribute):
        parts.append(fn.attr)
        fn = fn.value
    if isinstance(fn, ast.Name):
        parts.append(fn.id)
    elif isinstance(fn, ast.Call):
        parts.append("()")
    return ".".join(reversed(parts))


def cap_scan(files: list[Path]) -> list[list[str]]:
    hits = []
    for f in files:
        tree = ast.parse(f.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            name = dotted(n.func)
            last2 = ".".join(name.split(".")[-2:]) if "." in name else name
            for kind, rx in SINKS.items():
                if rx.match(name) or rx.match(last2):
                    if kind == "file_write" and last2 in ("tempfile.gettempdir",):
                        continue
                    hits.append([kind, f"{rel(f)}:{n.lineno}", name])
            if name in ("open", "io.open", "codecs.open") or name.endswith(".open"):
                mode = None
                if len(n.args) > 1 and isinstance(n.args[1], ast.Constant):
                    mode = n.args[1].value
                for k in n.keywords:
                    if k.arg == "mode" and isinstance(k.value, ast.Constant):
                        mode = k.value.value
                if isinstance(mode, str) and any(c in mode for c in "wax+"):
                    hits.append(["file_write", f"{rel(f)}:{n.lineno}", f"{name}(mode={mode})"])
            if any(k.arg == "unsafe_allow_html" and isinstance(k.value, ast.Constant) and k.value.value is True
                   for k in n.keywords) or name.endswith(("components.html", "components.v1.html", "st.html",
                                                          "components.iframe")):
                hits.append(["unescaped_html", f"{rel(f)}:{n.lineno}", name])
            if name in ("eval", "exec", "pickle.loads", "pickle.load", "yaml.load", "yaml.unsafe_load",
                        "marshal.loads"):
                hits.append(["code_exec_or_unsafe_load", f"{rel(f)}:{n.lineno}", name])
    return sorted(hits)


def static_closure() -> list[Path]:
    """First-party files reachable from root app.py by static imports (all import sites, incl. lazy)."""
    roots = {k: ROOT / v[0] for k, v in PKGS.items() if k != "ui"}
    seen: set[Path] = set()
    todo = [ROOT / "app.py", ROOT / "apps/ui/app.py"]

    def resolve(mod: str) -> list[Path]:
        parts = mod.split(".")
        if parts[0] == "ui_payload":
            return [ROOT / "apps/ui/ui_payload.py"]
        if parts[0] not in roots:
            return []
        base = roots[parts[0]]
        out = [base / "__init__.py"]
        cur = base
        for p in parts[1:]:
            cur = cur / p
            if (cur / "__init__.py").exists():
                out.append(cur / "__init__.py")
            elif cur.with_suffix(".py").exists():
                out.append(cur.with_suffix(".py"))
                break
        return [p for p in out if p.exists()]

    while todo:
        f = todo.pop()
        if f in seen or not f.exists():
            continue
        seen.add(f)
        tree = ast.parse(f.read_text(encoding="utf-8"))
        pkgdir = f.parent
        for n in ast.walk(tree):
            mods = []
            if isinstance(n, ast.Import):
                mods = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                if n.level:
                    b = pkgdir
                    for _ in range(n.level - 1):
                        b = b.parent
                    tgt = b / (n.module or "").replace(".", "/") if n.module else b
                    cands = [tgt.with_suffix(".py"), tgt / "__init__.py"] + [
                        (tgt / a.name).with_suffix(".py") for a in n.names] + [tgt / a.name / "__init__.py" for a in n.names]
                    todo += [c for c in cands if c.exists()]
                    continue
                mods = [n.module] + [f"{n.module}.{a.name}" for a in n.names]
            for m in mods:
                todo += resolve(m)
    return sorted(seen)


def section_capabilities(cases: dict) -> dict:
    files = static_closure()
    hits = cap_scan(files)
    pos = cap_scan([CTRL / "cap_pos.py"])
    clean = cap_scan([CTRL / "cap_clean.py"])
    dyn = sorted({tuple(e) for c in cases.get("cases", []) for e in c.get("first_party_events", [])})
    third = {}
    if RENDER:
        sp = next((RENDER / ".venv/lib").glob("python3.*/site-packages"))
        for pat_name, pat in (("subprocess", r"^\s*(import subprocess|from subprocess import)"),
                              ("socket", r"^\s*(import socket|from socket import|import ssl)")):
            p = subprocess.run(["grep", "-rlE", pat, str(sp), "--include=*.py"], capture_output=True, text=True)
            c = Counter(Path(x).relative_to(sp).parts[0] for x in p.stdout.split())
            third[pat_name] = dict(sorted(c.items()))
    return {"status": "RAN", "mechanism": "ast call-site census of the static first-party closure of root app.py; "
                                          "dynamic: audit-hook events from section 1",
            "unit": "call site", "population_files": len(files),
            "population": sorted(rel(f) for f in files),
            "blind_spot": "aliased callables (x = subprocess.run; x()), sinks reached through third-party code, "
                          "f-strings passed to st.markdown without unsafe_allow_html are escaped by Streamlit and not counted",
            "static_hits": hits, "static_by_kind": dict(sorted(Counter(h[0] for h in hits).items())),
            "dynamic_first_party_events": [list(e) for e in dyn],
            "third_party_files_importing": third,
            "controls": {"positive": {"must_flag": "subprocess, socket, file write, unsafe html, components.html",
                                      "flagged": {k for k, *_ in pos} >= {"subprocess", "socket", "file_write", "unescaped_html"}},
                         "clean": {"must_not_flag": "read-only open, escaped markdown", "flagged": bool(clean)}}}


# ---------------------------------------------------------------- 5 secrets
SECRET_RX = {
    "firecrawl_key": r"\bfc-[A-Za-z0-9]{20,}",
    "google_api_key": r"\bAIza[0-9A-Za-z_\-]{35}",
    "openai_or_anthropic_key": r"\bsk-(ant-)?[A-Za-z0-9_\-]{20,}",
    "github_token": r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{40,}",
    "aws_access_key": r"\b(AKIA|ASIA)[0-9A-Z]{16}\b",
    "slack_token": r"\bxox[abprs]-[A-Za-z0-9-]{10,}",
    "private_key_block": r"-----BEGIN (RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY",
    "jwt": r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
    "huggingface_token": r"\bhf_[A-Za-z0-9]{30,}",
    "assigned_secret": r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|auth[_-]?token|password|passwd)\b"
                       r"\s*[:=]\s*['\"][A-Za-z0-9_\-/+=.]{12,}['\"]",
    "url_credentials": r"[a-z][a-z0-9+.-]*://[^/\s:@'\"]{2,}:[^/\s:@'\"]{6,}@[A-Za-z0-9.-]+",
}
SECRET_FILE_RX = re.compile(r"(^|/)(\.env(\..+)?|id_rsa|id_ed25519|.*\.pem|.*\.p12|.*\.pfx|.*\.key|credentials\.json|"
                            r"service[-_]account.*\.json|\.netrc|\.pypirc|secrets?\.(ya?ml|json|toml))$", re.I)
PLACEHOLDER = re.compile(r"(?i)(x{6,}|your[_-]?|example|placeholder|dummy|changeme|<[^>]+>|\*{4,}|\.\.\.)")


def scan_tree(repo: Path, ref: str | None = None, content_root: Path | None = None) -> dict:
    """ref None: `git ls-files` of the work tree. ref given: `git ls-tree -r ref`, contents read from
    content_root (a `git archive ref` extraction, e.g. the Render tree)."""
    cmd = ["git", "-C", str(repo), "ls-files", "-z"] if ref is None else \
        ["git", "-C", str(repo), "ls-tree", "-r", "-z", "--name-only", ref]
    files = subprocess.run(cmd, capture_output=True).stdout.split(b"\0")
    files = [f.decode() for f in files if f]
    repo = content_root or repo
    hits: dict = defaultdict(set)
    named = []
    unread = 0
    for f in files:
        if SECRET_FILE_RX.search(f):
            named.append(f)
        p = repo / f
        try:
            if p.is_symlink() or not p.is_file():
                continue
            b = p.read_bytes()
        except OSError:
            unread += 1
            continue
        if b"\0" in b[:4096]:
            continue
        t = b.decode("utf-8", "replace")
        for kind, rx in SECRET_RX.items():
            for m in re.finditer(rx, t):
                if kind in ("assigned_secret", "url_credentials") and PLACEHOLDER.search(m.group(0)):
                    continue
                hits[(f, kind)].add(m.group(0))
    rows = sorted([f, k, len(v)] for (f, k), v in hits.items())
    return {"files_scanned": len(files), "unreadable": unread, "credential_named_files": sorted(named),
            "hits": rows}


def section_secrets() -> dict:
    tree = scan_tree(ROOT)
    main = scan_tree(ROOT, "origin/main", RENDER) if RENDER else {"status": "ABSENT"}
    for t in (tree, main):
        for r in t.get("hits", []):
            r.append("known noise R0-6 (Google web-client key / apiKey in saved Gemini page)"
                     if r[1] in ("google_api_key", "assigned_secret") and "/research/" in r[0] else "")
    # planted controls in a throwaway repo; the fake values are assembled here, never stored in the repo
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        subprocess.run(["git", "init", "-q", td], check=True)
        (d / "pos.py").write_text('FIRECRAWL = "' + "fc-" + "a1b2c3d4" * 4 + '"\napi_key = "' + "Zq9" * 6 + '"\n')
        (d / ".env").write_text("X=1\n")
        (d / "clean.py").write_text('css = "fc-color"\napi_key = os.environ["API_KEY"]\npassword = "<your-password>"\n')
        subprocess.run(["git", "-C", td, "add", "-A"], check=True)
        ctl = scan_tree(d)
    kinds_pos = {(f, k) for f, k, _ in ctl["hits"] if f == "pos.py"}
    hist = {"status": "ABSENT"}
    try:
        p = subprocess.run(["git", "-C", str(ROOT), "log", "--all", "--format=%h", "-G", SECRET_RX["firecrawl_key"]],
                           capture_output=True, text=True, timeout=300)
        hist = {"status": "RAN", "firecrawl_key_commits_touching": len(p.stdout.split()),
                "mechanism": "git log --all -G <firecrawl regex> (pickaxe on diffs)"}
    except subprocess.TimeoutExpired:
        hist = {"status": "INCOMPLETE", "why": "timeout 300 s"}
    return {"status": "RAN", "mechanism": "regex census over `git ls-files` text blobs + credential-file names",
            "unit": "(file, kind) pair; count = distinct matched strings", "population": "tracked files at HEAD",
            "blind_spot": "binary blobs (skipped), secrets split across lines or encoded, kinds without a regex, "
                          "history except the firecrawl pickaxe",
            **tree, "origin_main_tree": main, "history": hist,
            "controls": {"positive": {"must_flag": "firecrawl-shaped key, assigned api_key, .env file",
                                      "flagged": {("pos.py", "firecrawl_key"), ("pos.py", "assigned_secret")} <= kinds_pos
                                      and ".env" in ctl["credential_named_files"]},
                         "clean": {"must_not_flag": "fc-color, env lookup, placeholder password",
                                   "flagged": any(f == "clean.py" for f, *_ in ctl["hits"])}}}


def section_start() -> dict:
    """render.yaml startCommand, verbatim, with PORT set; poll /_stcore/health and GET / for 90 s."""
    if not RPY or not RPY.exists():
        return {"status": "ABSENT"}
    import time
    import urllib.request
    port = "8599"
    env = env_clean() | {"PORT": port, "STREAMLIT_SERVER_HEADLESS": "true",
                         "PATH": f"{RENDER}/.venv/bin:/usr/bin:/bin", "NO_PROXY": "*", "no_proxy": "*"}
    cmd = f"streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
    proc = subprocess.Popen(["bash", "-c", cmd], cwd=str(RENDER), env=env,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    res = {"status": "RAN", "command": cmd, "health": None, "root_http": None}
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        for _ in range(90):
            time.sleep(1)
            try:
                r = opener.open(f"http://127.0.0.1:{port}/_stcore/health", timeout=2)
                res["health"] = f"{r.status} {r.read().decode()[:20]}"
                res["root_http"] = opener.open(f"http://127.0.0.1:{port}/", timeout=5).status
                break
            except OSError:
                if proc.poll() is not None:
                    break
    finally:
        proc.terminate()
        try:
            out = proc.communicate(timeout=10)[0]
        except subprocess.TimeoutExpired:
            proc.kill()
            out = proc.communicate()[0]
    res["server_log_errors"] = sorted({ln.strip()[:160] for ln in out.splitlines()
                                       if "Error" in ln or "Traceback" in ln})
    return res


def pypi_exists(name: str) -> dict:
    import urllib.error
    import urllib.request
    try:
        d = json.load(urllib.request.urlopen(f"https://pypi.org/pypi/{name}/json", timeout=20))
    except urllib.error.HTTPError as e:
        return {"exists": False, "http": e.code}
    except OSError as e:
        return {"exists": None, "why": type(e).__name__}
    i = d["info"]
    return {"exists": True, "version": i["version"], "files": sorted(u["packagetype"] for u in d["urls"])}


def section_names() -> dict:
    """First-party distribution names vs PyPI; dry-run what pip picks when one -e line is missing."""
    names = sorted(FIRST_PARTY - {"registry", "ui_payload"})
    res = {"status": "RAN", "mechanism": "PyPI JSON API per first-party dist name; pip --dry-run --report",
           "pypi": {n: pypi_exists(n) for n in names}}
    if any(v["exists"] is None for v in res["pypi"].values()):
        res["status"] = "INCOMPLETE"
    res["declared_bare_by"] = sorted(f"apps/wired/pyproject.toml -> {x['name']} '{x['spec']}'"
                                     for x in manifest("apps/wired")["pyproject"] or [] if x["name"] in names)
    if RENDER:
        py = next((RENDER / ".venv/bin").glob("python3.14"))
        with tempfile.TemporaryDirectory() as td:
            req = Path(td) / "req.txt"
            lines = [ln.replace("-e ", f"-e {RENDER}/") for ln in (RENDER / "requirements.txt").read_text().splitlines()
                     if ln.strip() and not ln.startswith("#") and "labs/dnalab" not in ln]
            req.write_text("\n".join(lines) + "\n")
            subprocess.run([str(py), "-m", "venv", "--without-pip", td + "/v"], check=True)
            rep = Path(td) / "r.json"
            subprocess.run([str(py), "-m", "pip", "--python", td + "/v/bin/python", "install", "-q", "--dry-run",
                            "--ignore-installed", "--report", str(rep), "-r", str(req)], capture_output=True)
            if rep.exists():
                inst = json.loads(rep.read_text())["install"]
                pick = {i["metadata"]["name"].lower(): ("local-editable" if i["download_info"]["url"].startswith("file:")
                                                       else "pypi " + i["metadata"]["version"]) for i in inst
                        if i["metadata"]["name"].lower() in names}
                res["dry_run_without_dnalab_line"] = dict(sorted(pick.items()))
            else:
                res["dry_run_without_dnalab_line"] = "ABSENT"
    res["controls"] = {"positive": {"must_flag": "requests exists on PyPI", "flagged": bool(pypi_exists("requests")["exists"])},
                       "clean": {"must_not_flag": "p5-no-such-dist-zq9x", "flagged": bool(pypi_exists("p5-no-such-dist-zq9x")["exists"])}}
    return res


def main() -> None:
    meta = render_meta()
    cases = section_cases()
    out = {
        "git_sha": subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%h"], capture_output=True,
                                  text=True).stdout.strip(),
        "render_yaml": {"python": "3.14.3", "build": "pip install -r requirements.txt",
                        "start": "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"},
        "render_env": {k: v for k, v in meta.items() if k in ("python", "pip", "status")},
        "render_dists": meta.get("dists"),
        "0_start_command": section_start(),
        "1_render_cases": cases,
        "2_inventory": section_inventory(meta),
        "2c_dist_names": section_names(),
        "3_pip_audit": section_pip_audit(meta),
        "4_capabilities": section_capabilities(cases),
        "5_secrets": section_secrets(),
    }
    (HERE / "surface.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=list) + "\n")
    print("wrote", rel(HERE / "surface.json"))


if __name__ == "__main__":
    main()
