"""D3 check (4): instructions that point coders at absolute machine paths.

Usage (from repo root):  python audit/scratch/D3/machine_paths.py
Scans the D3 target docs plus the files they make coders load first (nested CLAUDE.md, per-coder
.agent/coders/*/AGENTS.md, .agent/rules/*.md, run-*.sh launchers) and every tracked symlink.
For each absolute path it reports whether it exists on this fresh clone's host and whether the
repo-relative remainder (after /agent_workspace/) resolves, i.e. whether a relative path would have worked.
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT, target_docs  # noqa: E402

ABS = re.compile(r"(/agent_workspace[^\s`'\")|,;]*|/home/m[^\s`'\")|,;]*|~/[^\s`'\")|,;]*|"
                 r"[A-Z]:\\[^\s`'\")|,;]*|/mnt/[^\s`'\")|,;]*)")


def extra_files() -> list[str]:
    pats = ["**/CLAUDE.md", ".agent/coders/*/AGENTS.md", ".agent/rules/*.md", "run-*.sh"]
    out = []
    for p in pats:
        for f in glob.glob(os.path.join(ROOT, p), recursive=True):
            rel = os.path.relpath(f, ROOT)
            if rel.startswith(("Vault/", "ARCHIVE/", "audit/", "node_modules/")) or "/node_modules/" in rel:
                continue
            out.append(rel)
    return sorted(set(out))


def main() -> int:
    files = list(dict.fromkeys(target_docs() + extra_files()))
    hits = []
    for f in files:
        for n, line in enumerate(open(os.path.join(ROOT, f), encoding="utf-8", errors="replace"), 1):
            for m in ABS.findall(line):
                p = m.rstrip(".:")
                exists = os.path.exists(os.path.expanduser(p)) if not re.match(r"^[A-Z]:\\", p) else False
                inner = re.sub(r"^/agent_workspace/?", "", p) if p.startswith("/agent_workspace") else None
                rel_ok = inner is not None and inner != "" and os.path.exists(os.path.join(ROOT, inner))
                hits.append((f, n, p, exists, rel_ok))
    by_file = defaultdict(list)
    for h in hits:
        by_file[h[0]].append(h)
    prefix = Counter(re.match(r"(/agent_workspace|/home/m|~|[A-Z]:\\|/mnt)", h[2]).group(1) for h in hits)
    print(f"files scanned: {len(files)}  absolute-path occurrences: {len(hits)}  in {len(by_file)} files")
    print("by prefix:", dict(prefix))
    print("exist on this host:", sum(h[3] for h in hits), " | /agent_workspace/<x> where repo-relative <x> resolves:",
          sum(h[4] for h in hits))
    print("\n## per file (count; first 3 distinct)")
    for f, hs in sorted(by_file.items(), key=lambda kv: -len(kv[1])):
        distinct = list(dict.fromkeys(h[2] for h in hs))[:3]
        print(f"{len(hs):3d}  {f}  e.g. " + ", ".join(f"{h}" for h in distinct))
    print("\n## command lines (cd/source/python/uv) using an absolute path")
    for f in files:
        for n, line in enumerate(open(os.path.join(ROOT, f), encoding="utf-8", errors="replace"), 1):
            if ABS.search(line) and re.search(r"\b(cd|source|uv|python3?(\.14)?|pip|pytest)\b", line):
                print(f"{f}:{n}: {line.strip()[:150]}")
    print("\n## tracked symlinks")
    ls = subprocess.run(["git", "ls-files", "-s"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    for row in ls.splitlines():
        if row.startswith("120000"):
            path = row.split("\t", 1)[1]
            tgt = os.readlink(os.path.join(ROOT, path))
            ok = os.path.exists(os.path.join(ROOT, path))
            print(f"{path} -> {tgt}  resolves={ok}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
