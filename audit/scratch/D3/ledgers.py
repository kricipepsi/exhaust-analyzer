"""D3 check (2): ledger rows.

Usage (from repo root):  python audit/scratch/D3/ledgers.py
Writes audit/scratch/D3/out/ledger_rows.tsv and prints:
  A. pending rows whose spec file is missing, or whose named blockers are not `done`
  B. the first `pending` row per ledger (AGENTS.md rule 3: "the next runnable task") and its verdict
  C. done rows whose spec, progress note, gate blocks, or other named files are missing
  D. task IDs that appear in more than one row (same or different ledger) with different status
  E. status cells that are not one of the canonical words (rule 3 forbids `pending (...)` variants)

Primary ledgers = labs/*/tasks/PROGRESS.md + apps/**/*PROGRESS*.md (the D3 scope). All other
*PROGRESS*.md files in the tree (planning/, harness/, v3/, registry) are parsed as SECONDARY so that
cross-ledger blockers and duplicate IDs can be looked up; their own rows are not judged.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT, app_ledgers, is_ignored, lab_ledgers, start_heres  # noqa: E402

CANON = ("done", "pending", "deferred", "blocked", "void")
ID_RE = re.compile(r"\b((?:T|CHI|EVAL|AUD|FX|FU|RM|DEP|PCT)-[A-Za-z0-9](?:[A-Za-z0-9.·\-]*[A-Za-z0-9])?)")
RANGE_RE = re.compile(r"\b((?:T|CHI)-[A-Za-z0-9\-]*?-?)(\d+)\.\.(\d+)\b")

INDEX: dict[str, list[str]] = defaultdict(list)


def build_index() -> None:
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "__pycache__", "Vault", "ARCHIVE")]
        for f in fn:
            INDEX[f].append(os.path.relpath(os.path.join(dp, f), ROOT))


def secondary_ledgers(primary: set[str]) -> list[str]:
    out = []
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "Vault", "ARCHIVE", "_skills", "progress_notes")
                 and not (rel == "." and d == "audit")]
        for f in fn:
            p = os.path.relpath(os.path.join(dp, f), ROOT)
            if "PROGRESS" in f and f.endswith(".md") and p not in primary:
                out.append(p)
    return sorted(out)


def cells(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|"):
        return []
    # split on | not inside backticks
    parts, cur, tick = [], "", False
    for ch in line[1:]:
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    return parts


def norm_id(c: str) -> str | None:
    m = ID_RE.search(c.replace("*", "").replace("`", ""))
    if not m:
        m2 = re.match(r"^\s*\**`?([A-Z][A-Za-z0-9]*-[A-Za-z0-9.·\-]+)", c)
        return m2.group(1) if m2 else None
    return m.group(1).rstrip(".")


def norm_status(c: str) -> tuple[str, str]:
    raw = c.replace("*", "").replace("`", "").strip()
    low = raw.lower()
    for w in CANON + ("in-progress", "in progress", "superseded", "open", "partial", "ready", "todo", "active"):
        if low.startswith(w):
            return w, raw
    m = re.search(r"\b(done|pending|deferred|blocked|void)\b", low)
    return (m.group(1) if m else "?"), raw


def expand_ids(text: str) -> list[str]:
    ids = []
    text = re.sub(r"\b([A-Z]+-)(\d+),(\d+)\b", r"\1\2 \1\3", text)  # PCT-2,4 -> PCT-2 PCT-4
    for m in RANGE_RE.finditer(text):
        pre, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        ids += [f"{pre}{i}" for i in range(a, b + 1)]
    text = RANGE_RE.sub(" ", text)
    ids += [m.rstrip(".") for m in ID_RE.findall(text.replace("*", "").replace("`", ""))]
    return list(dict.fromkeys(ids))


def parse(ledger: str) -> list[dict]:
    rows = []
    lines = open(os.path.join(ROOT, ledger), encoding="utf-8").read().splitlines()
    i = 0
    while i < len(lines) - 1:
        hdr = cells(lines[i])
        if hdr and re.match(r"^\|\s*:?-{3,}", lines[i + 1].strip()):
            names = [h.replace("*", "").strip().lower() for h in hdr]
            col = lambda pat: next((k for k, n in enumerate(names) if re.search(pat, n)), None)  # noqa: E731
            c_id, c_st = col(r"^(id|task id|item|task)$"), col(r"^(status|state)")
            c_task, c_blk = col(r"task file|^spec|^file"), col(r"blocked|^depends")
            j = i + 2
            while j < len(lines) and (lines[j].strip().startswith("|") or (
                    not lines[j].strip() and j + 1 < len(lines) and lines[j + 1].strip().startswith("|")
                    and not re.match(r"^\|\s*:?-{3,}", lines[j + 2].strip() if j + 2 < len(lines) else ""))):
                if not lines[j].strip():  # blank line inside a table (v3 ledger style)
                    j += 1
                    continue
                cs = cells(lines[j])
                if c_id is not None and c_st is not None and len(cs) > max(c_id, c_st):
                    rid = norm_id(cs[c_id])
                    st, raw = norm_status(cs[c_st])
                    if rid:
                        rows.append(dict(ledger=ledger, line=j + 1, id=rid, status=st, raw=raw,
                                         task=cs[c_task] if c_task is not None and c_task < len(cs) else "",
                                         blocked=cs[c_blk] if c_blk is not None and c_blk < len(cs) else "",
                                         text=lines[j]))
                j += 1
            i = j
        else:
            i += 1
    return rows


def resolve_spec(row: dict) -> tuple[str, str]:
    """-> (state, where). state: OK | ELSEWHERE | MISSING | NONE."""
    ldir = os.path.dirname(row["ledger"])
    cell = row["task"]
    toks = re.findall(r"`([^`]+\.md)`", cell) or re.findall(r"([\w./\-·]+\.md)", cell)
    bases = [ldir, os.path.dirname(ldir), os.path.dirname(os.path.dirname(ldir)), ""]
    if toks:
        t = toks[0].strip()
        for b in bases:
            if os.path.exists(os.path.join(ROOT, b, t)):
                return "OK", os.path.normpath(os.path.join(b, t))
        hits = INDEX.get(os.path.basename(t), [])
        near = [h for h in hits if h.startswith(ldir + "/")]
        if near:
            return "OK-SUBDIR", near[0]
        return ("ELSEWHERE", "; ".join(hits[:2])) if hits else ("MISSING", t)
    # no file named in the row: look for <ID>_*.md or <ID>.md under the ledger's dir
    rid = row["id"]
    for dp, dn, fn in os.walk(os.path.join(ROOT, ldir)):
        dn[:] = [d for d in dn if d != "progress_notes"]
        for f in fn:
            if f == f"{rid}.md" or f.startswith(f"{rid}_"):
                return "OK", os.path.relpath(os.path.join(dp, f), ROOT)
    return "NONE", ""


def progress_note(row: dict) -> tuple[str, str]:
    ldir = os.path.dirname(row["ledger"])
    rid = row["id"]
    for dp, dn, fn in os.walk(os.path.join(ROOT, ldir)):
        if os.path.basename(dp) != "progress_notes":
            continue
        for f in fn:
            if f == f"{rid}.md" or f.startswith(f"{rid}_") or f.startswith(f"{rid}."):
                p = os.path.join(dp, f)
                body = open(p, encoding="utf-8", errors="replace").read()
                up = body.upper()
                gates = ("VERIFICATION GATE" in up, "CODE REVIEW" in up)
                return ("OK" if all(gates) else f"NO-GATES(v={gates[0]},r={gates[1]})"), os.path.relpath(p, ROOT)
    return "MISSING", ""


def missing_named_files(row: dict) -> list[str]:
    out = []
    ldir = os.path.dirname(row["ledger"])
    for span in re.findall(r"`([^`]+)`", row["text"]):
        t = span.strip().split()[0] if span.strip() else ""
        t = re.sub(r"[:#].*$", "", t).rstrip("/")
        if not t or not re.search(r"\.(md|py|yaml|yml|json|csv|sh|html)$", t) or any(c in t for c in "*<>{}$"):
            continue
        if any(os.path.exists(os.path.join(ROOT, b, t)) for b in (ldir, os.path.dirname(ldir), "")):
            continue
        if is_ignored(os.path.normpath(t)):
            continue
        if INDEX.get(os.path.basename(t)) and "/" not in t:
            continue  # bare name that exists somewhere: shorthand, not a missing deliverable
        out.append(t)
    return out


def main() -> int:
    build_index()
    primary = lab_ledgers() + app_ledgers()
    secondary = secondary_ledgers(set(primary)) + start_heres()  # START_HERE files that embed a pack ledger
    rows = []
    for led in primary:
        rows += [dict(r, scope="primary") for r in parse(led)]
    for led in secondary:
        rows += [dict(r, scope="secondary") for r in parse(led)]
    status_of: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        status_of[r["id"]].append(r)

    out_dir = os.path.join(os.path.dirname(__file__), "out")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ledger_rows.tsv"), "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["scope", "ledger", "line", "id", "status", "raw_status", "task", "blocked"])
        for r in rows:
            w.writerow([r["scope"], r["ledger"], r["line"], r["id"], r["status"], r["raw"][:80], r["task"][:80], r["blocked"][:80]])

    print(f"primary ledgers: {len(primary)}  secondary: {len(secondary)}  rows: "
          f"{sum(r['scope'] == 'primary' for r in rows)} primary / {sum(r['scope'] == 'secondary' for r in rows)} secondary")
    by_status = defaultdict(int)
    for r in rows:
        if r["scope"] == "primary":
            by_status[r["status"]] += 1
    print("primary status counts:", dict(by_status))

    def blocker_report(r: dict) -> list[str]:
        bad = []
        for b in expand_ids(r["blocked"]):
            if b == r["id"]:
                continue
            hits = status_of.get(b)
            if not hits:
                bad.append(f"{b}=NOT-IN-ANY-LEDGER")
            elif not all(h["status"] in ("done", "void") for h in hits):
                bad.append(f"{b}=" + "/".join(sorted({h['status'] for h in hits})))
        return bad

    print("\n## A. pending rows (primary): spec + blockers")
    for r in rows:
        if r["scope"] != "primary" or r["status"] != "pending":
            continue
        spec, where = resolve_spec(r)
        bad = blocker_report(r)
        flag = "OK" if spec in ("OK", "OK-SUBDIR") and not bad else "FAIL"
        print(f"{flag}\t{r['ledger']}:{r['line']}\t{r['id']}\tspec={spec}:{where}\tblockers_not_done={bad or '-'}")

    print("\n## A2. pending rows in SECONDARY ledgers whose named blockers are not done (rule 3: pending = runnable now)")
    for r in rows:
        if r["scope"] == "secondary" and r["status"] == "pending":
            bad = blocker_report(r)
            if bad:
                print(f"{r['ledger']}:{r['line']}\t{r['id']}\tblockers_not_done={bad}")

    print("\n## B. first `pending` row per ledger (rule 3: next runnable task); secondary ledgers marked [S]")
    for led in primary + secondary:
        firsts = [r for r in rows if r["ledger"] == led and r["status"] == "pending"]
        if not firsts:
            print(f"{'[S] ' if led in secondary else ''}{led}\t(no pending row)")
            continue
        r = firsts[0]
        spec, where = resolve_spec(r)
        print(f"{'[S] ' if led in secondary else ''}{led}:{r['line']}\t{r['id']}\tspec={spec}:{where}\tblockers_not_done={blocker_report(r) or '-'}\traw='{r['raw'][:60]}'")

    print("\n## C. done rows (primary): spec / progress note / gates / named files")
    for r in rows:
        if r["scope"] != "primary" or r["status"] != "done":
            continue
        spec, where = resolve_spec(r)
        note, npath = progress_note(r)
        miss = missing_named_files(r)
        problems = []
        if spec in ("MISSING", "ELSEWHERE"):
            problems.append(f"spec={spec}:{where}")
        if note != "OK":
            problems.append(f"note={note}:{npath}")
        if miss:
            problems.append(f"named-missing={miss}")
        if problems:
            print(f"{r['ledger']}:{r['line']}\t{r['id']}\t" + "  ".join(problems))

    print("\n## D. IDs in more than one row with different status (any scope)")
    for rid, hs in sorted(status_of.items()):
        if len(hs) > 1 and len({h["status"] for h in hs}) > 1 and any(h["scope"] == "primary" for h in hs):
            print(f"{rid}\t" + " | ".join(f"{h['ledger']}:{h['line']}={h['status']}('{h['raw'][:30]}')" for h in hs))
    print("\n## D2. IDs in more than one primary row with the same status (duplicates)")
    for rid, hs in sorted(status_of.items()):
        ps = [h for h in hs if h["scope"] == "primary"]
        if len(ps) > 1 and len({h["status"] for h in hs}) == 1:
            print(f"{rid}\t" + " | ".join(f"{h['ledger']}:{h['line']}" for h in ps))

    print("\n## F. task spec files (T-*.md under a tasks dir) whose ID is in no ledger row (any scope)")
    known = set(status_of)
    for dp, dn, fn in os.walk(ROOT):
        rel = os.path.relpath(dp, ROOT)
        dn[:] = [d for d in dn if d not in (".git", "node_modules", "Vault", "ARCHIVE", "progress_notes", "reports", "audit")]
        if not re.search(r"(^|/)(tasks|[a-z_]+_tasks)(/|$)", rel):
            continue
        for f in sorted(fn):
            m = re.match(r"^((?:T|CHI|FL|REG)-[A-Za-z0-9.\-]+?)(?:_|\.md$)", f)
            if m and m.group(1) not in known and not any(k.startswith(m.group(1) + "·") for k in known):
                mentioned = any(m.group(1) in open(os.path.join(ROOT, l), encoding="utf-8").read()
                                for l in set(r["ledger"] for r in rows))
                print(f"{rel}/{f}\tid={m.group(1)}\tmentioned-in-ledger-prose={mentioned}")

    print("\n## G. live (uncommented) assignments in .agent/assignments.md and their ledger status")
    txt = open(os.path.join(ROOT, ".agent/assignments.md"), encoding="utf-8").read()
    live = re.sub(r"<!--.*?-->", "", txt, flags=re.S)
    sec = live.split("## Active", 1)[1].split("## History", 1)[0] if "## Active" in live else ""
    for n, line in enumerate(sec.splitlines()):
        m = re.match(r"^\s*([\w +]+?)\s*→\s*(\S+)", line)
        if m:
            tid = m.group(2)
            hits = status_of.get(tid, [])
            st = ", ".join(f"{h['ledger']}:{h['line']}={h['status']}" for h in hits) or "family id / not a single ledger row"
            print(f".agent/assignments.md\t{m.group(1).strip()} → {tid}\t{st}")

    print("\n## H. status claims made in governance docs vs the ledgers")
    claims = [
        ("CLAUDE.md", r"`T-WIRE-1` blocked until gaslab `T-GV2-2` is `done`", ["T-WIRE-1", "T-GV2-2"], "blocked/not done"),
        ("CLAUDE.md", r"pilot `T-VLIVE-1` runnable now", ["T-VLIVE-1"], "runnable (pending)"),
        ("CLAUDE.md", r"only `T-V7-1` \(library research\) is `pending`", ["T-V7-1"], "pending"),
        ("CLAUDE.md", r"T-SHIP-1/3/4/UI-1 `pending`", ["T-SHIP-1", "T-SHIP-3", "T-SHIP-4", "T-SHIP-UI-1"], "pending"),
        ("ROADMAP.md", r"T-GV2-2 deferred to Stage 4", ["T-GV2-2"], "deferred"),
        ("labs/comlab/tasks/PROGRESS.md", r"the task is a pure path re-point and stays `pending`/runnable", ["T-COMV2-LAMBDAPROJ-1"], "pending"),
        ("labs/comlab/tasks/PROGRESS.md", r"`REG-V2-CHEMSIG-34` `pending` \(registry ledger\)", [], "pending"),
        ("labs/comlab/registry/docs/REGISTRY_PROGRESS.md", r"Needs to be bumped to 73\. \| pending \|", [], "pending (guard still 68)"),
    ]
    for path, rx, ids, claimed in claims:
        txt = open(os.path.join(ROOT, path), encoding="utf-8").read()
        m = re.search(rx, txt)
        where = f"{path}:{txt.count(chr(10), 0, m.start()) + 1}" if m else f"{path}:NOT-FOUND"
        actual = "; ".join(f"{i}=" + ",".join(f"{h['status']}@{h['ledger']}:{h['line']}" for h in status_of.get(i, [])
                                              if not h['raw'].startswith('specs authored')) for i in ids)
        print(f"{where}\tclaims {claimed}\tledger says: {actual or 'see note'}")
    reg = open(os.path.join(ROOT, "labs/comlab/registry/docs/REGISTRY_PROGRESS.md"), encoding="utf-8").read()
    m = re.search(r"^\| REG-V2-CHEMSIG-34 \|[^\n]*\| (\w+) \|", reg, flags=re.M)
    print(f"  REG-V2-CHEMSIG-34 in registry ledger: {m.group(1) if m else '?'}")
    guard = open(os.path.join(ROOT, "apps/wired/wired/registry_guard.py"), encoding="utf-8").read()
    g = re.search(r"_EXPECTED_RULE_COUNT = (\d+)", guard)
    print(f"  apps/wired/wired/registry_guard.py _EXPECTED_RULE_COUNT = {g.group(1) if g else '?'}")

    print("\n## E. non-canonical status cells (primary)")
    for r in rows:
        if r["scope"] == "primary" and (r["status"] not in CANON or re.match(r"pending\s*\(", r["raw"].lower())):
            print(f"{r['ledger']}:{r['line']}\t{r['id']}\t'{r['raw'][:70]}'")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
