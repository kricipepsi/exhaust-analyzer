"""T-AUD-22: check claims_<group>.csv against candidates_<group>.csv and the source files (Cowork tool).

python -I check_code_claims.py --group gaslab|comlab|rest
Exit 0 and a last line "CLAIMS OK ..." when every check passes; exit 1 and one "ERROR" line per defect otherwise.
The format is README.md beside this file. same_as may name a wiki claim (W id, wikiaudit/claims.csv) or an earlier
claim of the same group.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
WIKI_CLAIMS = REPO / "labs" / "gaslab" / "audit_tasks" / "wikiaudit" / "claims.csv"
CLASSES = {"LEGAL_LIMIT", "PHYSICAL_CONSTANT", "ANALYSER_SPEC", "TYPICAL_RANGE", "DIAGNOSTIC_THRESHOLD",
           "RULE_OF_THUMB", "INTERNAL_PARAMETER", "NON_DOMAIN"}
FIELDS = ["claim_id", "cand_id", "file", "line", "quantity", "value", "unit", "condition", "class", "citation",
          "same_as", "suspect"]
PREFIX = {"gaslab": "GK", "comlab": "CK", "rest": "RK"}
NUM_RE = re.compile(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")


def norm(n: str) -> str:
    try:
        return repr(float(n))
    except ValueError:
        return n


def nums(s: str) -> set[str]:
    return {norm(n) for n in NUM_RE.findall(s)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", choices=sorted(PREFIX), required=True)
    group = ap.parse_args().group
    pre = PREFIX[group]
    errors: list[str] = []
    cands = {r["cand_id"]: r for r in csv.DictReader((HERE / f"candidates_{group}.csv").open(encoding="utf-8"))}
    cache: dict[str, list[str]] = {}
    for c in cands.values():
        lines = cache.setdefault(c["file"], (REPO / c["file"]).read_text(encoding="utf-8").splitlines())
        n = int(c["line"])
        sha = hashlib.sha1(lines[n - 1].encode("utf-8")).hexdigest()[:10] if n <= len(lines) else ""
        if sha != c["sha"]:
            errors.append(f"ERROR drift {c['cand_id']} {c['file']}:{n} no longer matches the candidates file")
    wiki_ids: set[str] = set()
    if WIKI_CLAIMS.is_file():
        wiki_ids = {r["claim_id"] for r in csv.DictReader(WIKI_CLAIMS.open(encoding="utf-8"))}
    with (HERE / f"claims_{group}.csv").open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != FIELDS:
            print(f"ERROR header {rd.fieldnames} != {FIELDS}")
            return 1
        claims = list(rd)
    for cid, k in Counter(r["claim_id"] for r in claims).items():
        if k > 1:
            errors.append(f"ERROR duplicate claim_id {cid}")
    by_id = {r["claim_id"]: r for r in claims}
    covered: set[str] = set()
    for r in claims:
        cid = r["claim_id"]
        if not re.fullmatch(rf"{pre}\d{{4}}", cid):
            errors.append(f"ERROR {cid}: claim_id must be {pre} + 4 digits")
        c = cands.get(r["cand_id"])
        if c is None:
            errors.append(f"ERROR {cid}: unknown cand_id {r['cand_id']}")
            continue
        covered.add(c["cand_id"])
        if r["file"] != c["file"] or r["line"] != c["line"]:
            errors.append(f"ERROR {cid}: file/line {r['file']}:{r['line']} != candidate {c['file']}:{c['line']}")
        if r["class"] not in CLASSES:
            errors.append(f"ERROR {cid}: class {r['class']!r} not in {sorted(CLASSES)}")
            continue
        if r["class"] == "NON_DOMAIN":
            continue
        for f in ("quantity", "value", "unit", "condition"):
            if not r[f].strip():
                errors.append(f"ERROR {cid}: {f} empty for class {r['class']}")
        missing = nums(r["value"]) - nums(c["text"])
        if missing:
            errors.append(f"ERROR {cid}: value number(s) {sorted(missing)} not in the line text")
        s = r["same_as"].strip()
        if s:
            if s.startswith("W"):
                if s not in wiki_ids:
                    errors.append(f"ERROR {cid}: same_as {s} is not a wiki claim_id")
            elif s not in by_id:
                errors.append(f"ERROR {cid}: same_as {s} is not a claim_id")
            elif by_id[s]["cand_id"] == r["cand_id"]:
                errors.append(f"ERROR {cid}: same_as points into its own line")
    for c in cands.values():
        if not c["auto"] and c["cand_id"] not in covered:
            errors.append(f"ERROR uncovered {c['cand_id']} {c['file']}:{c['line']}")
    for e in errors:
        print(e)
    if errors:
        print(f"CLAIMS FAIL {len(errors)} error(s)")
        return 1
    cls = Counter(r["class"] for r in claims)
    todo = sum(1 for c in cands.values() if not c["auto"])
    print("classes " + " ".join(f"{k}={cls[k]}" for k in sorted(cls)))
    print(f"suspect {sum(1 for r in claims if r['suspect'].strip())} "
          f"same_as_wiki {sum(1 for r in claims if r['same_as'].startswith('W'))}")
    print(f"CLAIMS OK group={group} candidates {todo} covered claims {len(claims)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
