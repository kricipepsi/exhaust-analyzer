#!/usr/bin/env python3
"""graph_health.py — cheap, read-only consistency check for 4DLabV2 graphify graphs.

Opens each graph.json and reports four things WITHOUT re-running graphify
(no tokens, no extraction, seconds):

  nodes / links      size of the graph
  dangling           links whose source or target is not a real node  -> HARD fail (corrupt)
  isolated           nodes with no links                              -> SOFT signal
  built (commit/date) staleness signal

Usage:
  python3 scripts/graph_health.py                 # scan all canonical graphs
  python3 scripts/graph_health.py labs/gaslab     # scan one lab / subtree
  python3 scripts/graph_health.py path/to/graph.json   # check one file

Exit code is non-zero if any graph has dangling edges (corruption).

This is the CHECK, not the BUILD. It never modifies anything and never
regenerates a graph. See GRAPH_MANIFEST.md for how to read the output.
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time

# Probe/test/scratch trees are not canonical graphs — skip them by default.
SKIP = ("skilltest", "/scratch/", "gfx_probe", "_skills/")


def find_graphs(arg: str | None) -> list[str]:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 4DLabV2/
    if arg:
        target = arg if os.path.isabs(arg) else os.path.join(root, arg)
        if target.endswith(".json") and os.path.isfile(target):
            return [target]
        pattern = os.path.join(target, "**", "graph.json")
    else:
        pattern = os.path.join(root, "**", "graph.json")
    return sorted(p for p in glob.glob(pattern, recursive=True)
                  if not any(s in p for s in SKIP))


def check(path: str) -> tuple[int, int, int, int, str, str]:
    d = json.load(open(path))
    nodes, links = d.get("nodes", []), d.get("links", [])
    ids = {n.get("id") for n in nodes}
    dangling = sum(1 for l in links
                   if l.get("source") not in ids or l.get("target") not in ids)
    deg: dict = {}
    for l in links:
        deg[l.get("source")] = deg.get(l.get("source"), 0) + 1
        deg[l.get("target")] = deg.get(l.get("target"), 0) + 1
    isolated = sum(1 for n in nodes if deg.get(n.get("id"), 0) == 0)
    commit = (d.get("built_at_commit") or "")[:8]
    built = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))
    return len(nodes), len(links), dangling, isolated, commit, built


def main() -> int:
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    graphs = find_graphs(arg)
    if not graphs:
        print("no graph.json found for:", arg or "(all)")
        return 0
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    print(f"{'graph':46} {'nodes':>6} {'links':>6} {'dangl':>5} {'isol':>5} {'commit':>9}  built")
    print("-" * 100)
    corrupt = 0
    for p in graphs:
        try:
            n, e, dang, iso, commit, built = check(p)
        except Exception as ex:  # noqa: BLE001 - report and continue
            print(f"{p.replace(root, ''):46}  PARSE ERROR: {ex}")
            corrupt += 1
            continue
        if dang:
            corrupt += 1
        flag = "  <-- DANGLING" if dang else ""
        print(f"{p.replace(root, ''):46} {n:6} {e:6} {dang:5} {iso:5} {commit:>9}  {built}{flag}")
    if corrupt:
        print(f"\n{corrupt} graph(s) with dangling edges / parse errors — investigate.")
        return 1
    print("\nAll graphs structurally sound (0 dangling edges).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
