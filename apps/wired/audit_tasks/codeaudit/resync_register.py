"""T-AUD-22-RESYNC: re-key a line-keyed register after the audited files changed (Cowork tool).

python -I resync_register.py --register gaslab-code|wiki --base <git rev> [--apply]
The register's candidates were keyed (line + sha of the line text) to the files as they were at --base. For each
candidate whose line no longer matches, the old file (git show <base>:<file>) is diffed against the working file:
- an unchanged line that moved gets its new line number (candidates and claims rows);
- a replaced line (paired in order inside a replaced block) gets its new line number, sha and text, and is listed as CHANGED: its claims keep their
  old value until a person re-classifies them (the claims checker then flags any value no longer in the line);
- a deleted line is listed as GONE and left as it is.
Without --apply nothing is written. Prints one line per CHANGED/GONE candidate and a summary line.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REGISTERS = {
    "gaslab-code": (REPO, HERE / "candidates_gaslab.csv", HERE / "claims_gaslab.csv"),
    "wiki": (REPO / "labs" / "gaslab", REPO / "labs/gaslab/audit_tasks/wikiaudit/candidates.csv",
             REPO / "labs/gaslab/audit_tasks/wikiaudit/claims.csv"),
}


def sha(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:10]


def line_map(old: list[str], new: list[str]) -> dict[int, tuple[str, int]]:
    """1-based old line -> (kind, new line): kind 'same' or 'changed'; deleted lines are absent."""
    out: dict[int, tuple[str, int]] = {}
    sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                out[i1 + k + 1] = ("same", j1 + k + 1)
        elif tag == "replace":  # paired in order; extra old lines are deleted, extra new lines are new
            for k in range(min(i2 - i1, j2 - j1)):
                out[i1 + k + 1] = ("changed", j1 + k + 1)
    return out


def read_csv(p: Path) -> tuple[list[str], list[dict[str, str]]]:
    with p.open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        return list(rd.fieldnames or []), list(rd)


def write_csv(p: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", choices=sorted(REGISTERS), required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    root, cand_p, claim_p = REGISTERS[a.register]
    cfields, cands = read_csv(cand_p)
    kfields, claims = read_csv(claim_p)
    rel_root = root.relative_to(REPO).as_posix()
    new_lines: dict[str, list[str]] = {}
    maps: dict[str, dict[int, tuple[str, int]]] = {}
    moved = changed = gone = 0
    remap: dict[str, int] = {}
    for c in cands:
        f = c["file"]
        if f not in new_lines:
            new_lines[f] = (root / f).read_text(encoding="utf-8").splitlines()
        cur = new_lines[f]
        n = int(c["line"])
        if n <= len(cur) and sha(cur[n - 1]) == c["sha"]:
            continue
        if f not in maps:
            gpath = f if rel_root == "." else f"{rel_root}/{f}"
            old = subprocess.run(["git", "-C", str(REPO), "show", f"{a.base}:{gpath}"], capture_output=True,
                                 text=True, encoding="utf-8", check=True).stdout.splitlines()
            maps[f] = line_map(old, cur)
        hit = maps[f].get(n)
        if hit is None:
            gone += 1
            print(f"GONE {c['cand_id']} {f}:{n}")
            continue
        kind, m = hit
        if kind == "same" and sha(cur[m - 1]) == c["sha"]:
            moved += 1
        else:
            changed += 1
            print(f"CHANGED {c['cand_id']} {f}:{n}->{m} {cur[m - 1].strip()[:100]}")
            c["sha"], c["text"] = sha(cur[m - 1]), cur[m - 1].strip()
        c["line"] = str(m)
        remap[c["cand_id"]] = m
    for k in claims:
        if k["cand_id"] in remap:
            k["line"] = str(remap[k["cand_id"]])
    print(f"RESYNC {a.register} base={a.base} moved {moved} changed {changed} gone {gone}"
          f" claims re-keyed {sum(1 for k in claims if k['cand_id'] in remap)}" + ("" if a.apply else " (dry run)"))
    if a.apply:
        write_csv(cand_p, cfields, cands)
        write_csv(claim_p, kfields, claims)
    return 0


if __name__ == "__main__":
    sys.exit(main())
