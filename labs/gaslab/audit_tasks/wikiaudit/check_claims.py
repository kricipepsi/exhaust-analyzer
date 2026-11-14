"""T-GASA-WIKIAUDIT: check claims.csv against candidates.csv and the documents (Cowork tool).

python -I check_claims.py --scope wiki|vocab_ontology|all
Exit 0 and a last line "CLAIMS OK ..." when every check passes; exit 1 and one "ERROR" line per defect otherwise.
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
LAB = HERE.parents[1]
CLASSES = {"LEGAL_LIMIT", "PHYSICAL_CONSTANT", "ANALYSER_SPEC", "TYPICAL_RANGE", "DIAGNOSTIC_THRESHOLD",
           "RULE_OF_THUMB", "INTERNAL_PARAMETER", "NON_DOMAIN"}
FIELDS = ["claim_id", "cand_id", "file", "line", "quantity", "value", "unit", "condition", "class", "same_as",
          "suspect"]
NUM_RE = re.compile(r"\d+(?:[.,]\d+)?")


def in_scope(rel: str, scope: str) -> bool:
    is_wiki = rel.startswith("wiki/")
    return scope == "all" or (scope == "wiki") == is_wiki


def nums(s: str) -> set[str]:
    return {n.replace(",", ".").lstrip("0") or "0" for n in NUM_RE.findall(s)}


def mojibake(s: str) -> bool:
    """True when s is UTF-8 text that was decoded as cp1252 and re-encoded (e.g. 'Â°' for '°', 'â€“' for '–')."""
    if s.isascii():
        return False
    try:
        return s.encode("cp1252").decode("utf-8") != s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["wiki", "vocab_ontology", "all"], required=True)
    scope = ap.parse_args().scope
    errors: list[str] = []
    cands = {r["cand_id"]: r for r in csv.DictReader((HERE / "candidates.csv").open(encoding="utf-8"))}
    cache: dict[str, list[str]] = {}
    for c in cands.values():
        lines = cache.setdefault(c["file"], (LAB / c["file"]).read_text(encoding="utf-8").splitlines())
        n = int(c["line"])
        sha = hashlib.sha1(lines[n - 1].encode("utf-8")).hexdigest()[:10] if n <= len(lines) else ""
        if sha != c["sha"]:
            errors.append(f"ERROR drift {c['cand_id']} {c['file']}:{n} no longer matches candidates.csv")
    with (HERE / "claims.csv").open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != FIELDS:
            print(f"ERROR header {rd.fieldnames} != {FIELDS}")
            return 1
        claims = list(rd)
    ids = Counter(r["claim_id"] for r in claims)
    for cid, k in ids.items():
        if k > 1:
            errors.append(f"ERROR duplicate claim_id {cid}")
    by_id = {r["claim_id"]: r for r in claims}
    covered: set[str] = set()
    for r in claims:
        cid = r["claim_id"]
        for f in FIELDS:
            if mojibake(r[f]):
                errors.append(f"ERROR {cid}: {f} is double-encoded (UTF-8 read as cp1252): {r[f][:40]!r}")
        if not re.fullmatch(r"W\d{4}", cid):
            errors.append(f"ERROR {cid}: claim_id must be W + 4 digits")
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
        if r["same_as"]:
            t = by_id.get(r["same_as"])
            if t is None:
                errors.append(f"ERROR {cid}: same_as {r['same_as']} is not a claim_id")
            elif t["cand_id"] == r["cand_id"]:
                errors.append(f"ERROR {cid}: same_as points into its own line")
    todo = [c for c in cands.values() if not c["auto"] and in_scope(c["file"], scope)]
    for c in todo:
        if c["cand_id"] not in covered:
            errors.append(f"ERROR uncovered {c['cand_id']} {c['file']}:{c['line']}")
    for e in errors:
        print(e)
    if errors:
        print(f"CLAIMS FAIL {len(errors)} error(s)")
        return 1
    scoped = [r for r in claims if in_scope(r["file"], scope)]
    cls = Counter(r["class"] for r in scoped)
    print("classes " + " ".join(f"{k}={cls[k]}" for k in sorted(cls)))
    print(f"suspect {sum(1 for r in scoped if r['suspect'].strip())}")
    print(f"CLAIMS OK scope={scope} candidates {len(todo)} covered claims {len(scoped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
