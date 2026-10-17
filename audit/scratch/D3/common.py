"""Shared helpers for the D3 governance-doc audit. Read-only: never writes outside audit/scratch/D3/."""
from __future__ import annotations

import glob
import os
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

ROOT_DOCS = [
    "CLAUDE.md", "AGENTS.md", "4DLab_CLAUDE.md", "START_HERE.md", "ROADMAP.md",
    "DECISIONS.md", "README.md", "GRAPH_MANIFEST.md",
]


def lab_ledgers() -> list[str]:
    return sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "labs/*/tasks/PROGRESS.md")))


def app_ledgers() -> list[str]:
    out = []
    for dp, dn, fn in os.walk(os.path.join(ROOT, "apps")):
        dn[:] = [d for d in dn if d not in ("node_modules", "__pycache__", ".git")]
        for f in fn:
            if "PROGRESS" in f and f.endswith(".md"):
                out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)


def start_heres() -> list[str]:
    out = []
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        dn[:] = [d for d in dn if d not in ("node_modules", "__pycache__", ".git", "ARCHIVE")
                 and not (rel == "." and d == "audit")]
        for f in fn:
            if f.endswith("_START_HERE.md"):
                out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)


def target_docs() -> list[str]:
    return ROOT_DOCS + lab_ledgers() + app_ledgers() + start_heres()


def tracked_files() -> set[str]:
    r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True)
    return set(r.stdout.splitlines())


def is_ignored(path: str) -> bool:
    """True when .gitignore would keep `path` out of a clone (read-only check-ignore)."""
    r = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT, stderr=subprocess.DEVNULL)
    return r.returncode == 0
