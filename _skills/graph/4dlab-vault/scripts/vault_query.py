#!/usr/bin/env python3
"""vault_query.py - query the 4DLab Obsidian vault as a database from the sandbox.

Why this exists (see reference/obsidian-cli-optional.md): the native `obsidian`
CLI is an IPC remote control for the Windows desktop app and is unreachable from
the agent's Linux sandbox. This script treats the mounted vault folder as raw
data instead - no app, no IPC, no Catalyst licence. It reads BOTH the YAML
frontmatter (the `.base` view contract) and the inline `**Status:**` markdown
the task ledger uses, and it parses Python files via the AST (Abstract Syntax
Tree - Python's own structural view of source) rather than text-matching.

Commands (all accept --vault PATH, default = cwd; --json for machine output):

  consumers [--missing]   mirror consumers.base: framed notes + named consumers
  drift                   mirror drift-guards.base: implements vs guarding tests
  modules                 mirror modules.base: framed notes grouped by lab
  tasks [STATUS]          task ledger rows (frontmatter first, inline fallback)
  next                    first pending task whose blocked_by are all done
  backlinks TARGET        notes that link to / mention TARGET
  code LAB [SYMBOL]       AST map of classes/functions/imports in labs/LAB/code
  docs LAB QUERY          content search inside labs/LAB/docs
  wiki LAB QUERY          content search inside labs/LAB/wiki
  grep LAB QUERY          combined search over wiki, docs, and code
  health                  one-shot health report (PASS/WARN/FAIL, exit code)

Examples:
  python3 vault_query.py --vault Vault next
  python3 vault_query.py --vault Vault consumers --missing
  python3 vault_query.py --vault Vault code gaslab ChemicalSignature
"""
from __future__ import annotations
import argparse
import ast
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None


# ---------- low-level note loading ----------
def iter_md(root):
    for d, _, files in os.walk(root):
        if os.sep + "." in d:
            continue
        for fn in files:
            if fn.endswith(".md"):
                yield os.path.join(d, fn)


def parse_note(path):
    """Return (frontmatter: dict, body: str). Tolerates CRLF and BOM."""
    with open(path, encoding="utf-8-sig") as f:
        text = f.read()
    fm, body = {}, text
    stripped = text.lstrip()
    if stripped.startswith("---"):
        parts = stripped.split("---", 2)
        if len(parts) == 3:
            if yaml is not None:
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                except Exception:
                    fm = {}
            body = parts[2]
    return (fm if isinstance(fm, dict) else {}), body


def load(vault):
    notes = []
    for p in iter_md(vault):
        fm, body = parse_note(p)
        notes.append((os.path.relpath(p, vault).replace(os.sep, "/"), fm, body))
    return notes


def as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# ---------- task ledger (frontmatter first, inline markdown fallback) ----------
TASK_ID_RE = re.compile(r"T-[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+")


def task_row(path, fm, body):
    """Normalise one task note to {id,status,pack,blocked_by[],consumers[]}."""
    tid = fm.get("task_id")
    if not tid:
        m = re.match(r"#\s*(T-[A-Z0-9-]+)", body.lstrip())
        tid = m.group(1) if m else os.path.basename(path).split("_")[0]
    status = fm.get("status")
    if not status:
        m = re.search(r"\*\*Status:\*\*\s*`?([\w-]+)", body)
        status = m.group(1).lower() if m else "?"
    status = str(status).lower()
    blocked = as_list(fm.get("blocked_by"))
    if not blocked and "blocked_by" not in fm:
        m = re.search(r"\*\*Blocked by:\*\*\s*(.+)", body)
        if m:
            blocked = TASK_ID_RE.findall(m.group(1))
    pack = fm.get("pack")
    if not pack:
        m = re.search(r"\*\*Pack:\*\*\s*([^\n.*]+)", body)
        pack = m.group(1).strip() if m else "?"
    return {
        "id": tid,
        "status": status,
        "pack": str(pack).strip(),
        "blocked_by": blocked,
        "consumers": as_list(fm.get("consumers")),
        "path": path,
    }


def task_rows(notes):
    rows = []
    for path, fm, body in notes:
        if "/tasks/" not in "/" + path or "/progress_notes/" in path:
            continue
        if not os.path.basename(path).startswith("T-"):
            continue
        rows.append(task_row(path, fm, body))
    return rows


def is_done(status):
    return status in ("done", "void")


# ---------- AST code query (closes the frontmatter gap on code) ----------
def analyze_py(path):
    try:
        tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    except Exception as e:
        return {"classes": [], "functions": [], "imports": [], "error": str(e)}
    out = {"classes": [], "functions": [], "imports": []}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            out["classes"].append(node.name)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out["functions"].append(node.name)
        elif isinstance(node, ast.Import):
            out["imports"] += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            out["imports"].append(node.module or "")
    return out


# ---------- commands ----------
def cmd_consumers(notes, args):
    rows = []
    for path, fm, _ in notes:
        if "node_type" in fm and fm.get("node_type") != "task":
            cons = as_list(fm.get("consumers"))
            if args.missing and cons:
                continue
            rows.append({"path": path, "module": fm.get("module", "-"),
                         "node_type": fm.get("node_type", "-"),
                         "signal_noise": "MISSING" if not cons else "ok(%d)" % len(cons),
                         "consumers": cons})
    return rows


def cmd_drift(notes, _args):
    rows = []
    for path, fm, _ in notes:
        if fm.get("node_type") == "task":   # tasks have their own view (tasks.base)
            continue
        impl = as_list(fm.get("implements"))
        if impl:
            g = as_list(fm.get("drift_guards"))
            rows.append({"path": path, "module": fm.get("module", "-"),
                         "implements": len(impl), "guards": "NONE" if not g else len(g)})
    return rows


def cmd_modules(notes, _args):
    by = {}
    for path, fm, _ in notes:
        if path.startswith("labs") and "module" in fm and fm.get("node_type") != "task":
            by.setdefault(fm.get("lab", "?"), []).append(
                {"path": path, "module": fm.get("module"),
                 "subsystem": fm.get("subsystem", "-"), "node_type": fm.get("node_type", "-")})
    return by


def cmd_tasks(notes, args):
    rows = task_rows(notes)
    if args.status:
        rows = [r for r in rows if r["status"].startswith(args.status.lower())]
    return sorted(rows, key=lambda r: (r["status"], r["id"]))


def cmd_next(notes, _args):
    rows = task_rows(notes)
    done = {r["id"] for r in rows if is_done(r["status"])}
    unblocked = [r for r in rows if r["status"] == "pending"
                 and all(b in done for b in r["blocked_by"])]
    return sorted(unblocked, key=lambda r: r["id"])


def cmd_backlinks(notes, args):
    t = args.target
    base = os.path.basename(t).replace(".md", "")
    return [path for path, _, body in notes
            if t in body or ("[[" + base) in body or base in body]


def cmd_code(notes, args):
    vault = args.vault
    code_dir = os.path.join(vault, "labs", args.lab, "code")
    if not os.path.isdir(code_dir):
        return {"error": "no code dir for lab '%s' (%s)" % (args.lab, code_dir)}
    out = []
    for root, _, files in os.walk(code_dir):
        for fn in files:
            if fn.endswith(".py"):
                p = os.path.join(root, fn)
                a = analyze_py(p)
                if args.symbol and args.symbol not in a.get("classes", []) + a.get("functions", []):
                    continue
                rec = {"file": os.path.relpath(p, vault).replace(os.sep, "/")}
                rec.update(a)
                out.append(rec)
    return out


def cmd_docs(notes, args):
    q = args.query.lower()
    pre = "labs/%s/docs" % args.lab
    return [path for path, _, body in notes if path.startswith(pre) and q in body.lower()]


def cmd_wiki(notes, args):
    q = args.query.lower()
    pre = "labs/%s/wiki" % args.lab
    return [path for path, _, body in notes if path.startswith(pre) and q in body.lower()]


def cmd_grep(notes, args):
    vault = args.vault
    lab = args.lab
    q = args.query.lower()
    search_dirs = [
        ("wiki", ".md"),
        ("docs", ".md"),
        ("code", ".py"),
    ]
    out = []
    for sub, ext in search_dirs:
        dir_path = os.path.join(vault, "labs", lab, sub)
        if not os.path.isdir(dir_path):
            continue
        for root, _, files in os.walk(dir_path):
            for fn in files:
                if fn.endswith(ext):
                    p = os.path.join(root, fn)
                    rel_p = os.path.relpath(p, vault).replace(os.sep, "/")
                    try:
                        with open(p, encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, 1):
                                if q in line.lower():
                                    out.append({
                                        "path": rel_p,
                                        "line": idx,
                                        "text": line.rstrip("\r\n")
                                    })
                    except Exception:
                        pass
    return out


def cmd_health(notes, args):
    """One-shot vault health report. Returns exit code 0 (clean) / 1 (failures)."""
    fails, warns, ok = [], [], []

    # 1. signal/noise: framed LAB notes must name a consumer
    framed = [(p, fm) for p, fm, _ in notes
              if fm.get("node_type") and fm.get("node_type") != "task"]
    miss = [p for p, fm in framed if not as_list(fm.get("consumers"))]
    (ok if not miss else fails).append(
        "signal/noise: %d/%d framed notes name a consumer%s"
        % (len(framed) - len(miss), len(framed), "" if not miss else " -- MISSING: " + ", ".join(miss)))

    # 2. coverage: implements without a guarding test (tasks excluded)
    none = [p for p, fm, _ in notes
            if fm.get("node_type") != "task" and as_list(fm.get("implements"))
            and not as_list(fm.get("drift_guards"))]
    (ok if not none else warns).append(
        "coverage: %d note(s) implement code with no drift_guard%s"
        % (len(none), "" if not none else " -- " + ", ".join(none)))

    # 3. task ledger integrity
    rows = task_rows(notes)
    ids = {r["id"] for r in rows}
    by_status = {}
    for r in rows:
        by_status[r["status"]] = by_status.get(r["status"], 0) + 1
    ok.append("ledger: %d tasks (%s)"
              % (len(rows), ", ".join("%s=%d" % (s, n) for s, n in sorted(by_status.items()))))

    t_miss = [r["id"] for r in rows if not r["consumers"]]
    (ok if not t_miss else fails).append(
        "task consumers: %d/%d non-empty%s"
        % (len(rows) - len(t_miss), len(rows), "" if not t_miss else " -- MISSING: " + ", ".join(t_miss)))

    # 4. anti-orphan: blocked_by should reference a task id IN THIS ledger.
    # Refs outside it are cross-pack (e.g. T-SEM-*) and unverifiable here -> WARN,
    # not FAIL. `next` treats an external blocker as unresolved (conservative).
    external = sorted({b for r in rows for b in r["blocked_by"] if b not in ids})
    if not external:
        ok.append("blocked_by refs: all resolve in-ledger")
    else:
        warns.append("blocked_by refs: %d cross-ledger ref(s) -- verify in source pack: %s"
                     % (len(external), ", ".join(external)))

    # 5. dependency cycle detection (a task transitively blocking itself)
    dep = {r["id"]: [b for b in r["blocked_by"] if b in ids] for r in rows}
    cyc = []
    def walk(n, seen):
        for d in dep.get(n, []):
            if d in seen:
                cyc.append(" -> ".join(seen + [d]))
                return
            walk(d, seen + [d])
    for n in dep:
        walk(n, [n])
    (ok if not cyc else fails).append(
        "dependency cycles: %s" % ("none" if not cyc else "FOUND -> " + "; ".join(sorted(set(cyc)))))

    # 6. .base views present in the live vault
    bdir = os.path.join(args.vault, "_bases")
    want = ["consumers.base", "drift-guards.base", "modules.base", "tasks.base"]
    missing_bases = [b for b in want if not os.path.isfile(os.path.join(bdir, b))]
    (ok if not missing_bases else fails).append(
        ".base views: %d/%d present%s"
        % (len(want) - len(missing_bases), len(want), "" if not missing_bases else " -- MISSING: " + ", ".join(missing_bases)))

    # 7. ready-to-run preview (mirrors `next`)
    ready = [r["id"] for r in cmd_next(notes, args)]
    ok.append("next unblocked: %d -- %s" % (len(ready), ", ".join(ready) if ready else "(none)"))

    if args.json:
        print(json.dumps({"fails": fails, "warns": warns, "ok": ok,
                          "verdict": "FAIL" if fails else ("WARN" if warns else "PASS")}, indent=2))
    else:
        verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
        print("=== 4DLab vault health: %s ===" % verdict)
        for line in fails:
            print("  [FAIL] " + line)
        for line in warns:
            print("  [WARN] " + line)
        for line in ok:
            print("  [OK]   " + line)
    return 1 if fails else 0


# ---------- output ----------
def emit(obj, as_json):
    if as_json:
        print(json.dumps(obj, indent=2))
        return
    if isinstance(obj, dict) and "error" in obj:
        print("ERROR:", obj["error"])
        return
    if isinstance(obj, dict):  # modules grouping
        for lab, items in sorted(obj.items()):
            print("== %s (%d) ==" % (lab, len(items)))
            for it in items:
                print("   %-22s %-10s %s" % (it.get("module", "-"), it.get("node_type", "-"), it["path"]))
        return
    for r in obj:
        if isinstance(r, str):
            print(r)
        elif "signal_noise" in r:
            print("%-9s %-20s %s" % (r["signal_noise"], str(r["module"]), r["path"]))
        elif "guards" in r:
            print("guards=%-5s impl=%-3d %s" % (str(r["guards"]), r["implements"], r["path"]))
        elif "status" in r:
            blk = ",".join(r["blocked_by"]) or "-"
            print("%-9s %-22s blocked_by=%-34s %s" % (r["status"], r["id"], blk, r["path"]))
        elif "classes" in r:
            print("%s\n   classes:   %s\n   functions: %s" % (
                r["file"], ", ".join(r["classes"]) or "-", ", ".join(r["functions"]) or "-"))
        elif isinstance(r, dict) and "line" in r and "path" in r and "text" in r:
            print("%s:%d:%s" % (r["path"], r["line"], r["text"]))
        else:
            print(r)


def main(argv=None):
    p = argparse.ArgumentParser(description="Query the 4DLab Obsidian vault.")
    p.add_argument("--vault", default=".")
    p.add_argument("--json", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("consumers")
    sp.add_argument("--missing", action="store_true")
    sub.add_parser("drift")
    sub.add_parser("modules")
    sub.add_parser("next")
    sp = sub.add_parser("tasks")
    sp.add_argument("status", nargs="?")
    sp = sub.add_parser("backlinks")
    sp.add_argument("target")
    sp = sub.add_parser("code")
    sp.add_argument("lab")
    sp.add_argument("symbol", nargs="?")
    sp = sub.add_parser("docs")
    sp.add_argument("lab")
    sp.add_argument("query")
    sp = sub.add_parser("wiki")
    sp.add_argument("lab")
    sp.add_argument("query")
    sp = sub.add_parser("grep")
    sp.add_argument("lab")
    sp.add_argument("query")
    sub.add_parser("health")
    args = p.parse_args(argv)
    if yaml is None:
        sys.stderr.write("warning: pyyaml not available; frontmatter ignored, inline fallback only\n")
    notes = load(args.vault)
    if args.cmd == "health":
        sys.exit(cmd_health(notes, args))
    table = {"consumers": cmd_consumers, "drift": cmd_drift, "modules": cmd_modules,
             "tasks": cmd_tasks, "next": cmd_next, "backlinks": cmd_backlinks,
             "code": cmd_code, "docs": cmd_docs, "wiki": cmd_wiki, "grep": cmd_grep}
    emit(table[args.cmd](notes, args), args.json)


if __name__ == "__main__":
    main()
