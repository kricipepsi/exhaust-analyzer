"""D3 check (1): does every repo-relative or backticked path in the governance docs resolve?

Usage (from repo root):  python audit/scratch/D3/paths.py [--all]
Writes audit/scratch/D3/out/paths.tsv and prints dangling references grouped by class.

Resolution: a token resolves if it exists relative to the repo root, the doc's own directory, or any
ancestor of the doc's directory (lenient on purpose; the base is recorded). Skipped: URLs, globs,
placeholders (<lab>, <id>, X, ...), command flags. Dangling classes:
  DECLARED   the doc itself (same line, or CLAUDE.md:50 / 4DLab_CLAUDE.md [off-mount]) says it dangles
  IGNORED    .gitignore keeps it out of every clone (git check-ignore --no-index)
  ABSOLUTE   machine path (/home/m, /agent_workspace, ~/...) -> see machine_paths.py
  LEGACY     starts with 4DLabV2/ or 4DLab/ ; `fix=` says whether stripping the prefix resolves
  MOVED      not at the stated place, but a file with the same basename exists elsewhere
  MISSING    no file of that name anywhere in the tree
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT, is_ignored, target_docs  # noqa: E402

EXT = (".md", ".py", ".yaml", ".yml", ".json", ".sh", ".html", ".csv", ".toml", ".txt", ".jsonl", ".skill", ".base")
DECLARE_KW = re.compile(r"dangle|off-mount|git-ignored|gitignored|not present|NOT present|obsolete|out-of-band", re.I)
NON_REF_KW = re.compile(r"never stage|never commit|Never stage|Never commit|never `git init`", re.I)
GLOBAL_DECLARED = ("../v2-restructure/", "4DLab/graphify-out/", "CLAUDE.local.md")
SKIP_CHARS = set("*?{}[]<>|$=\"'")
PLACEHOLDER = re.compile(r"(^|[/_-])(X|N|NN|ID|id|lab|LAB|you|pkg)($|[/_.-])|\.\.\.|…|\.\.\d")
BARE_PATH = re.compile(r"(?<![\w./\-`])((?:\.\.?/|/|~/)?[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+/?)")
BARE_FILE = re.compile(r"(?<![\w./\-`])([A-Za-z0-9_.\-]+\.(?:md|py|yaml|yml|json|sh|html|toml))(?![\w])")

EXAMPLE = re.compile(r"^:|^s/|foo\.py|path/to/|^/graph|^/labs|^/graphify|update/extract")
FILE_INDEX: dict[str, list[str]] = defaultdict(list)
ALL_PATHS: list[str] = []


def build_index() -> None:
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__", ".hypothesis")]
        for f in fn + dn:
            FILE_INDEX[f].append(os.path.relpath(os.path.join(dp, f), ROOT))
            ALL_PATHS.append(os.path.relpath(os.path.join(dp, f), ROOT))


def clean(tok: str) -> str:
    tok = tok.strip().strip("()[]\"'*,;")
    tok = tok.lstrip("@")
    tok = re.sub(r"[.,;:)\]]+$", "", tok)
    tok = re.sub(r"#.*$", "", tok)
    tok = re.sub(r":\d+(-\d+)?$", "", tok)
    tok = re.sub(r"§.*$", "", tok)
    return tok


def path_like(tok: str, docdir: str) -> bool:
    if EXAMPLE.search(tok):
        return False
    if not tok or "://" in tok or tok.startswith(("www.", "-", "github.com", "claude.ai")):
        return False
    if any(c in SKIP_CHARS for c in tok) or PLACEHOLDER.search(tok):
        return False
    if re.search(r"\.(com|org|net|io)(/|$)", tok):
        return False
    if "/" not in tok:
        return tok.endswith(EXT) and not tok.startswith(".")  # bare file names
    if tok.endswith(EXT) or tok.endswith("/"):
        return True
    first = tok.split("/")[0]
    roots = set(os.listdir(ROOT)) | set(os.listdir(os.path.join(ROOT, docdir) or ROOT))
    return first in roots or first in ("", ".", "..", "~", "4DLab", "4DLabV2")


def candidates(line: str) -> list[str]:
    toks: list[str] = []
    for span in re.findall(r"`([^`]+)`", line):
        toks += re.split(r"[\s,→]+", span)
    toks += re.findall(r"\]\(([^)\s]+)\)", line)
    stripped = re.sub(r"`[^`]*`", " ", line)
    stripped = re.sub(r"\]\([^)]*\)", " ", stripped)
    stripped = re.sub(r"https?://\S+", " ", stripped)
    toks += BARE_PATH.findall(stripped) + BARE_FILE.findall(stripped)
    return toks


def resolve(tok: str, docdir: str) -> str | None:
    t = tok.rstrip("/")
    if t.startswith(("/", "~")):
        return None
    d = docdir
    bases = [""]
    while True:
        bases.append(d)
        if not d:
            break
        d = os.path.dirname(d)
    for b in dict.fromkeys(bases):
        p = os.path.normpath(os.path.join(ROOT, b, t))
        if not p.startswith(ROOT):
            continue
        if os.path.exists(p):
            return b or "."
    return None


def classify(tok: str, doc: str, line: str) -> tuple[str, str]:
    t = tok.rstrip("/")
    if os.path.islink(os.path.join(ROOT, t)):
        return "BROKEN-SYMLINK", "-> " + os.readlink(os.path.join(ROOT, t))
    if tok.startswith(GLOBAL_DECLARED) or (doc == "4DLab_CLAUDE.md" and "[off-mount]" in line):
        return "DECLARED", "global/off-mount"
    if DECLARE_KW.search(line):
        return "DECLARED", "same-line keyword"
    if NON_REF_KW.search(line):
        return "NONREF", "mentioned only as never-stage/never-commit"
    if tok.startswith(("/home/", "/agent_workspace", "~/", "/mnt/")):
        inner = re.sub(r"^/agent_workspace/?", "", tok)
        fix = "resolves-under-repo" if tok.startswith("/agent_workspace") and resolve(inner, "") else ""
        return "ABSOLUTE", fix
    if "\\" in tok or re.match(r"^[A-Za-z]:", tok):
        return "ABSOLUTE", "windows"
    rel = os.path.normpath(t) + ("/" if tok.endswith("/") else "")
    if not rel.startswith(("..", "/")) and (is_ignored(rel) or is_ignored(rel.rstrip("/") + "/")):
        return "IGNORED", ""
    for pre in ("4DLabV2/", "4DLab/"):
        if tok.startswith(pre):
            inner = tok[len(pre):]
            return "LEGACY", "strip-prefix-resolves" if resolve(inner, "") else "strip-prefix-still-missing"
    base = os.path.basename(t)
    hits = FILE_INDEX.get(base, [])
    if hits and "/" not in t:
        return "BARE-ELSEWHERE", "; ".join(hits[:3]) + (f" (+{len(hits) - 3})" if len(hits) > 3 else "")
    if any(p == t or p.endswith("/" + t) for p in ALL_PATHS):
        return "SUFFIX", "shorthand: an existing path ends with it"
    if hits:
        return "MOVED", "; ".join(hits[:3]) + (f" (+{len(hits) - 3})" if len(hits) > 3 else "")
    return "MISSING", ""


def main() -> int:
    build_index()
    rows = []
    for doc in target_docs():
        docdir = os.path.dirname(doc)
        with open(os.path.join(ROOT, doc), encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                seen = set()
                for raw in candidates(line):
                    tok = clean(raw)
                    if tok in seen or not path_like(tok, docdir):
                        continue
                    seen.add(tok)
                    base = resolve(tok, docdir)
                    if base is not None:
                        rows.append((doc, n, tok, "OK", base))
                        continue
                    cls, info = classify(tok, doc, line)
                    rows.append((doc, n, tok, cls, info))
    out = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "paths.tsv"), "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["doc", "line", "path", "class", "info"])
        w.writerows(rows)
    counts: dict[str, int] = defaultdict(int)
    for r in rows:
        counts[r[3]] += 1
    print(f"docs scanned: {len(target_docs())}  references: {len(rows)}  " +
          "  ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    show_all = "--all" in sys.argv
    for cls in ("BROKEN-SYMLINK", "MISSING", "MOVED", "SUFFIX", "BARE-ELSEWHERE", "LEGACY", "IGNORED", "ABSOLUTE", "DECLARED", "NONREF"):
        sel = [r for r in rows if r[3] == cls]
        if not sel:
            continue
        print(f"\n## {cls} ({len(sel)})")
        for r in sel if (show_all or cls not in ("DECLARED", "NONREF", "BARE-ELSEWHERE", "SUFFIX")) else sel[:0]:
            print(f"{r[0]}:{r[1]}\t{r[2]}\t{r[4]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
