"""P1 static sweep instrument: six analysers over the production scope -> audit/scratch/P1/sweep.json.

Usage (repo root, .venv-audit active, pyright on PATH from `npm i -g pyright`):
    python audit/scratch/P1/sweep.py [out.json]
Deterministic: no timestamps or durations; records sorted by id. Labels come from adjudication.json.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CTRL = HERE / "controls"

# Production scope (P1 prompt). Tier "offline" = labs/vinlab/tools (lower priority).
SCOPE_DIRS = [
    "labs/comlab/comlab", "labs/comlab/registry", "labs/dnalab/dnalab", "labs/dtclab/dtclab",
    "labs/gaslab/gaslab", "labs/obdlab/obdlab", "labs/symptomlab/symptomlab", "labs/vinlab/vinlab",
    "labs/vinlab/tools", "apps/ui", "apps/wired",
]
SCOPE_FILES = ["app.py"]
SKIP_PARTS = {"tests", "_jaeger", "harness", "__pycache__"}
VERDICT_CODE = ("labs/comlab/", "labs/gaslab/", "apps/ui/ui_payload.py", "apps/wired/wired/composition.py")

# deptry roots: (cwd, sources, known-first-party, extra args). Manifest = cwd's pyproject unless overridden.
DEPTRY_RUNS = [
    ("labs/comlab", ["comlab"], "comlab", ["--pep621-dev-dependency-groups", "dev"]),
    ("labs/comlab", ["registry"], "registry,comlab", ["--pep621-dev-dependency-groups", "dev"]),
    ("labs/dnalab", ["dnalab"], "dnalab", []),
    ("labs/dtclab", ["dtclab"], "dtclab", ["--pep621-dev-dependency-groups", "dev"]),
    ("labs/gaslab", ["gaslab"], "gaslab", ["--pep621-dev-dependency-groups", "dev"]),
    ("labs/obdlab", ["obdlab"], "obdlab", ["--pep621-dev-dependency-groups", "dev"]),
    ("labs/symptomlab", ["symptomlab"], "symptomlab", []),
    ("labs/vinlab", ["vinlab"], "vinlab", []),
    ("labs/vinlab", ["tools"], "vinlab,tools", ["--config", "no-such.toml", "--requirements-files", "requirements.txt"]),
    ("apps/wired", ["wired"], "wired", []),
    ("apps/wired", ["v7", "fl_tasks", "trace"], "wired,v7,fl_tasks,trace", []),
    (".", ["apps/ui"], "ui_payload,app", ["--requirements-files", "requirements.txt"]),
]
LABS = ["comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab"]
IL_ROOTS = LABS + ["registry", "wired"]
IL_OWNER = {"registry": "comlab"}
SANCTIONED = {("dnalab", "vinlab"), ("dnalab", "symptomlab")}  # labs/dnalab/docs/ADR_DNALab.md ADR-0002
PKG_DIR = {lab: f"labs/{lab}/{lab}" for lab in LABS} | {"registry": "labs/comlab/registry",
                                                       "wired": "apps/wired/wired"}


def sh(cmd: list[str], cwd: Path = ROOT, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)


def scope_files() -> list[str]:
    out = []
    for d in SCOPE_DIRS:
        for p in (ROOT / d).rglob("*.py"):
            rel = p.relative_to(ROOT)
            if not SKIP_PARTS & set(rel.parts):
                out.append(rel.as_posix())
    return sorted(out + SCOPE_FILES)


_SYM_CACHE: dict[str, list[tuple[int, int, str]]] = {}


def enclosing(path: str, line: int | None) -> tuple[str, str]:
    """(enclosing qualified symbol, stripped source line) for a repo-relative path."""
    p = ROOT / path
    if line is None or not p.is_file() or p.suffix != ".py":
        return "", ""
    src = p.read_text(encoding="utf-8", errors="replace")
    if path not in _SYM_CACHE:
        spans: list[tuple[int, int, str]] = []

        def walk(node: ast.AST, prefix: str) -> None:
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    q = f"{prefix}.{ch.name}" if prefix else ch.name
                    spans.append((ch.lineno, ch.end_lineno or ch.lineno, q))
                    walk(ch, q)
                else:
                    walk(ch, prefix)
        try:
            walk(ast.parse(src), "")
        except SyntaxError:
            pass
        _SYM_CACHE[path] = spans
    sym = ""
    for a, b, q in _SYM_CACHE[path]:
        if a <= line <= b and len(q) >= len(sym):
            sym = q
    lines = src.splitlines()
    text = lines[line - 1].strip() if 0 < line <= len(lines) else ""
    return sym or "<module>", text


def fp(msg: str) -> str:
    norm = re.sub(r"\d+", "#", msg.strip())
    return hashlib.sha1(norm.encode()).hexdigest()[:12]


def rec(tool: str, rule: str, path: str, line: int | None, msg: str, **extra) -> dict:
    sym, text = enclosing(path, line)
    if not text and line is None:
        text = extra.get("module", "")
    return {"tool": tool, "rule": rule, "path": path, "symbol": sym, "text": text, "line": line,
            "message": msg.strip().splitlines()[0][:300], "message_fp": fp(msg), **extra}


def rel(p: str) -> str:
    q = Path(p)
    q = q if q.is_absolute() else (ROOT / q)
    return q.resolve().relative_to(ROOT).as_posix()


# ---------------------------------------------------------------- analysers
def run_pyright(files: list[str]) -> tuple[list[dict], dict]:
    r = sh(["pyright", "-p", str(HERE / "pyrightconfig.json"), "--outputjson", *files])
    d = json.loads(r.stdout)
    recs = [rec("pyright", x.get("rule", ""), rel(x["file"]), x["range"]["start"]["line"] + 1,
                x["message"], severity=x["severity"]) for x in d["generalDiagnostics"]]
    analysed = d["summary"]["filesAnalyzed"]
    unresolved = sorted({x["path"] for x in recs if x["rule"] == "reportMissingImports"})
    st = {"status": "RAN" if analysed == len(files) else "INCOMPLETE", "files_in": len(files),
          "files_analysed": analysed, "mode": "basic",
          "overrides": {"reportPossiblyUnboundVariable": "warning (basic sets it off in pyright 1.1.414)"},
          "files_with_unresolved_imports": unresolved,
          "blind_spot": "basic mode; unresolved imports and unannotated parameters type as Unknown, "
                        "so attribute/optional errors through them are not reported"}
    return recs, st


def run_bandit(files: list[str]) -> tuple[list[dict], dict]:
    r = sh(["bandit", "-ll", "-f", "json", "-q", *files])
    d = json.loads(r.stdout)
    recs = [rec("bandit", x["test_id"], rel(x["filename"]), x["line_number"], x["issue_text"],
                severity=x["issue_severity"], confidence=x["issue_confidence"]) for x in d["results"]]
    st = {"status": "RAN" if not d["errors"] else "INCOMPLETE", "files_in": len(files),
          "errors": sorted(e["filename"] for e in d["errors"]), "threshold": "-ll (severity >= MEDIUM)",
          "loc": d["metrics"]["_totals"]["loc"]}
    return recs, st


VULTURE_RE = re.compile(r"^(.*?):(\d+): (.*) \((\d+)% confidence(?:, \d+ lines?)?\)$")


def run_vulture(files: list[str]) -> tuple[list[dict], dict]:
    r = sh(["vulture", "--min-confidence", "60", *files])
    recs, unparsed = [], []
    for ln in r.stdout.splitlines():
        m = VULTURE_RE.match(ln)
        if not m:
            unparsed.append(ln)
            continue
        kind = re.sub(r" '.*'", "", m.group(3))
        recs.append(rec("vulture", kind, rel(m.group(1)), int(m.group(2)), m.group(3),
                        confidence=int(m.group(4))))
    st = {"status": "RAN" if not unparsed and r.returncode in (0, 3) else "INCOMPLETE",
          "files_in": len(files), "unparsed": unparsed, "min_confidence": 60,
          "blind_spot": "whole-scope run: a name used only from tests, other labs or dynamic access counts as used/unused by text"}
    return recs, st


def run_deptry() -> tuple[list[dict], dict]:
    recs, runs = [], []
    with tempfile.TemporaryDirectory() as td:
        for i, (cwd, srcs, kfp, extra) in enumerate(DEPTRY_RUNS):
            out = Path(td) / f"d{i}.json"
            r = sh(["deptry", *srcs, "--known-first-party", kfp, "--extend-exclude", ".*/tests/.*",
                    "--json-output", str(out), *extra], cwd=ROOT / cwd)
            ok = out.exists()
            runs.append({"cwd": cwd, "sources": srcs, "status": "RAN" if ok else "ABSENT",
                         "exit": r.returncode, "issues": len(json.loads(out.read_text())) if ok else None})
            if not ok:
                continue
            for x in json.loads(out.read_text()):
                loc = x["location"]
                path = rel(str(ROOT / cwd / loc["file"]))
                recs.append(rec("deptry", x["error"]["code"], path, loc["line"], x["error"]["message"],
                                module=x["module"], manifest_root=cwd))
    st = {"status": "RAN" if all(r["status"] == "RAN" for r in runs) else "INCOMPLETE", "runs": runs,
          "not_run": ["app.py (root Render shim: stdlib-only, no own manifest)"],
          "blind_spot": "a declared distribution that is not installed cannot be mapped to its import name "
                        "(mysql-connector-python -> mysql shows as DEP001+DEP002)"}
    return recs, st


def il_config(path: Path) -> None:
    out = ["[importlinter]", "root_packages =", *[f"    {r}" for r in IL_ROOTS],
           "include_external_packages = False", ""]
    for src in LABS + ["registry"]:
        me = IL_OWNER.get(src, src)
        forb = [r for r in IL_ROOTS if IL_OWNER.get(r, r) != me and (me, r) not in SANCTIONED]
        out += [f"[importlinter:contract:iso-{src}]", f"name = iso-{src}", "type = forbidden",
                "source_modules =", f"    {src}", "forbidden_modules =", *[f"    {f}" for f in forb], ""]
    out += ["[importlinter:contract:emitters-not-comlab]", "name = emitters-not-comlab", "type = forbidden",
            "source_modules =", "    obdlab", "    dtclab", "    gaslab",
            "forbidden_modules =", "    comlab", "    registry", ""]
    path.write_text("\n".join(out))


def lint_imports(cfg: Path, pypath: str) -> dict[str, str]:
    env = dict(os.environ, PYTHONPATH=pypath)
    r = sh(["lint-imports", "--config", str(cfg), "--no-cache"], env=env)
    res = {}
    for m in re.finditer(r"^(iso-\w+|emitters-not-comlab) (KEPT|BROKEN)$", r.stdout, re.M):
        res[m.group(1)] = m.group(2)
    return res


def run_import_linter() -> tuple[list[dict], dict]:
    cfg = HERE / "importlinter.ini"
    il_config(cfg)
    real = lint_imports(cfg, str(ROOT / "labs/comlab"))
    # Proofs on a private copy: plant one violation per contract, plus one sanctioned import (must stay KEPT).
    plants = {f"iso-{s}": (s, next(r for r in IL_ROOTS if IL_OWNER.get(r, r) != IL_OWNER.get(s, s)
                                    and (s, r) not in SANCTIONED)) for s in LABS + ["registry"]}
    plants["emitters-not-comlab"] = ("gaslab", "comlab")
    proofs = {}
    with tempfile.TemporaryDirectory() as td:
        tdp = Path(td)
        for name, d in PKG_DIR.items():
            shutil.copytree(ROOT / d, tdp / name, ignore=shutil.ignore_patterns("__pycache__"))
        base = lint_imports(cfg, td)
        proofs["clean_copy"] = {"expect": "all KEPT", "got": base,
                                "pass": len(base) == 9 and set(base.values()) == {"KEPT"}}
        for contract, (src, tgt) in sorted(plants.items()) + [("sanctioned", ("dnalab", "vinlab"))]:
            init = tdp / src / "__init__.py"
            orig = init.read_text()
            init.write_text(orig + f"\nimport {tgt}  # P1 planted\n")
            got = lint_imports(cfg, td)
            init.write_text(orig)
            if contract == "sanctioned":
                ok = set(got.values()) == {"KEPT"}
                proofs[contract] = {"planted": f"{src} -> {tgt}", "expect": "all KEPT", "pass": ok}
            else:
                broken = sorted(k for k, v in got.items() if v == "BROKEN")
                proofs[contract] = {"planted": f"{src} -> {tgt}", "broken": broken, "pass": contract in broken}
    recs = [rec("import-linter", c, "audit/scratch/P1/importlinter.ini", None, f"{c} BROKEN")
            for c, v in sorted(real.items()) if v == "BROKEN"]
    st = {"status": "RAN" if len(real) == 9 else "INCOMPLETE", "contracts": real, "proofs": proofs,
          "blind_spot": "apps/ui is not a package (app.py, ui_payload.py) so it is outside the import graph; "
                        "tests/ outside packages are outside the graph; importlib/string imports invisible"}
    return recs, st


def run_semgrep(files: list[str]) -> tuple[list[dict], dict]:
    r = sh(["semgrep", "--config", str(HERE / "semgrep_rules.yml"), "--metrics=off",
            "--disable-version-check", "--json", *files])
    d = json.loads(r.stdout)
    recs = [rec("semgrep", x["check_id"].split(".")[-1], rel(x["path"]), x["start"]["line"],
                x["extra"]["message"]) for x in d["results"]]
    errs = sorted({rel(e["path"]) for e in d["errors"] if e.get("path")})
    scanned = len(d.get("paths", {}).get("scanned", files))
    st = {"status": "INCOMPLETE", "files_in": len(files), "files_scanned": scanned,
          "files_with_parse_errors": errs,
          "absent": "p/python registry pack: semgrep.dev refused by the session egress proxy (connect_rejected)",
          "ran": "6 local rules in semgrep_rules.yml"}
    return recs, st


# ---------------------------------------------------------------- reconciliation and controls
def own_isolation_scan(files: list[str]) -> list[str]:
    """Cross-lab/app imports in production files (AST, absolute imports), same rule as the contracts."""
    owner_of = {}
    for name, d in PKG_DIR.items():
        if name != "wired":  # apps may import labs
            owner_of[d] = IL_OWNER.get(name, name)
    hits = []
    foreign = set(IL_ROOTS) | {"ui_payload", "v7", "fl_tasks"}
    for f in files:
        me = next((o for d, o in owner_of.items() if f.startswith(d + "/")), None)
        if me is None:
            continue
        for n in ast.walk(ast.parse((ROOT / f).read_text(encoding="utf-8"))):
            mods = [a.name for a in n.names] if isinstance(n, ast.Import) else (
                [n.module] if isinstance(n, ast.ImportFrom) and n.module and n.level == 0 else [])
            for m in mods:
                top = m.split(".")[0]
                if top in foreign and IL_OWNER.get(top, top) != me and (me, top) not in SANCTIONED:
                    hits.append(f"{f}:{n.lineno} {me} -> {m}")
    return sorted(hits)


def isolation_reconcile(files: list[str], il_real: dict) -> dict:
    r = sh([sys.executable, "audit/tools/isolation.py"])
    iso = [ln for ln in r.stdout.splitlines() if not ln.startswith("violations")]
    prod = set(files)
    iso_prod = [ln for ln in iso if ln.split(":")[0] in prod]
    own = own_isolation_scan(files)
    broken = sorted(k for k, v in il_real.items() if v == "BROKEN")
    return {"isolation_py_total": len(iso), "isolation_py_in_production_scope": iso_prod,
            "isolation_py_outside_scope": iso, "own_ast_scan_production": own, "import_linter_broken": broken,
            "agree": (not iso_prod) == (not own) == (not broken)}


def controls() -> dict:
    out = {}
    pos, cln = CTRL / "positive", CTRL / "clean"
    pr = json.loads(sh(["pyright", "-p", str(HERE / "pyrightconfig.json"), "--outputjson",
                        str(pos / "pos_pyright.py"), str(cln / "clean_pyright.py")]).stdout)
    rules = lambda f: sorted(x.get("rule", "") for x in pr["generalDiagnostics"] if x["file"].endswith(f))  # noqa: E731
    out["pyright"] = {"positive": rules("pos_pyright.py"), "clean": rules("clean_pyright.py")}
    out["pyright"]["pass"] = {"reportOptionalMemberAccess", "reportPossiblyUnboundVariable",
                              "reportAttributeAccessIssue"} <= set(out["pyright"]["positive"]) and not out["pyright"]["clean"]
    b = lambda f: sorted(x["test_id"] for x in json.loads(sh(["bandit", "-ll", "-f", "json", "-q", str(f)]).stdout)["results"])  # noqa: E731
    out["bandit"] = {"positive": b(pos / "pos_bandit.py"), "clean": b(cln / "clean_bandit.py")}
    out["bandit"]["pass"] = {"B602", "B506"} <= set(out["bandit"]["positive"]) and not out["bandit"]["clean"]
    v = lambda f: sorted(VULTURE_RE.match(ln).group(3) for ln in sh(["vulture", "--min-confidence", "60", str(f)]).stdout.splitlines())  # noqa: E731
    out["vulture"] = {"positive": v(pos / "pos_vulture.py"), "clean": v(cln / "clean_vulture.py")}
    out["vulture"]["pass"] = len(out["vulture"]["positive"]) >= 2 and not out["vulture"]["clean"]
    dres = {}
    for tag, d, k in (("positive", CTRL / "deptry_pos", "pkgpos"), ("clean", CTRL / "deptry_clean", "pkgclean")):
        with tempfile.TemporaryDirectory() as td:
            o = Path(td) / "o.json"
            sh(["deptry", k, "--known-first-party", k, "--json-output", str(o)], cwd=d)
            dres[tag] = sorted(f'{x["error"]["code"]}:{x["module"]}' for x in json.loads(o.read_text()))
    out["deptry"] = dres | {"pass": {"DEP001:no_such_dist_xyz", "DEP003:yaml"} <= set(dres["positive"]) and not dres["clean"]}
    sg = json.loads(sh(["semgrep", "--config", str(HERE / "semgrep_rules.yml"), "--metrics=off",
                        "--disable-version-check", "--json", str(pos / "pos_semgrep.py"),
                        str(cln / "clean_semgrep.py")]).stdout)["results"]
    out["semgrep"] = {"positive": sorted(x["check_id"].split(".")[-1] for x in sg if x["path"].endswith("pos_semgrep.py")),
                      "clean": sorted(x["check_id"].split(".")[-1] for x in sg if x["path"].endswith("clean_semgrep.py"))}
    out["semgrep"]["pass"] = len(set(out["semgrep"]["positive"])) == 6 and not out["semgrep"]["clean"]
    return out


# ---------------------------------------------------------------- adjudication
def adjudicate(recs: list[dict]) -> None:
    rules = json.loads((HERE / "adjudication.json").read_text())
    for r in recs:
        r["class"] = "UNADJUDICATED"
        for a in rules:
            m = a["match"]
            if all(re.search(v, str(r.get(k, ""))) for k, v in m.items()):
                r["class"] = a["class"]
                r["reason"] = a["reason"]
                for k in ("dup_of", "finding", "probe"):
                    if k in a:
                        r[k] = a[k]
                break


def main() -> None:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sweep.json"
    files = scope_files()
    status, recs = {}, []
    for name, fn in (("pyright", lambda: run_pyright(files)), ("bandit", lambda: run_bandit(files)),
                     ("vulture", lambda: run_vulture(files)), ("deptry", run_deptry),
                     ("import-linter", run_import_linter), ("semgrep", lambda: run_semgrep(files))):
        try:
            rr, st = fn()
        except (OSError, json.JSONDecodeError, KeyError) as exc:
            rr, st = [], {"status": "ABSENT", "error": f"{type(exc).__name__}: {exc}"}
        recs += rr
        status[name] = st
    seen: dict[str, int] = {}
    for r in sorted(recs, key=lambda r: (r["tool"], r["rule"], r["path"], r["symbol"], r["text"], r["line"] or 0)):
        key = "|".join((r["tool"], r["rule"], r["path"], r["symbol"], r["text"]))
        n = seen[key] = seen.get(key, 0) + 1
        r["id"] = hashlib.sha1(f"{key}|{n}".encode()).hexdigest()[:16]
        r["verdict_code"] = r["path"].startswith(VERDICT_CODE)
        r["tier"] = "offline" if r["path"].startswith("labs/vinlab/tools/") else "production"
    adjudicate(recs)
    recs.sort(key=lambda r: r["id"])
    totals: dict[str, dict[str, int]] = {}
    for r in recs:
        totals.setdefault(r["tool"], {}).setdefault(r["class"], 0)
        totals[r["tool"]][r["class"]] += 1
    doc = {"scope": {"dirs": SCOPE_DIRS, "files": SCOPE_FILES, "n_files": len(files),
                     "excluded": ["*/tests/*", "apps/wired/_jaeger", "apps/wired/harness",
                                  "apps/vault (0 .py files, no README)"]},
           "analysers": status,
           "isolation_reconcile": isolation_reconcile(files, status["import-linter"].get("contracts", {})),
           "controls": controls(), "totals": totals, "n_records": len(recs), "records": recs}
    out_path.write_text(json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    print(json.dumps({"n_records": len(recs), "totals": totals,
                      "status": {k: v["status"] for k, v in status.items()}}, indent=1))


if __name__ == "__main__":
    main()
