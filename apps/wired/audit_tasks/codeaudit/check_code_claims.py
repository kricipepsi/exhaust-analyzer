"""T-AUD-22: check claims_<group>.csv against candidates_<group>.csv and the source files (Cowork tool).

python -I check_code_claims.py --group gaslab|comlab|rest [--files GLOB ...]
--files limits the coverage check to candidates whose file matches a glob (one inventory slice); every claim row is
still checked. With no --files the whole group must be covered.
Exit 0 and a last line "CLAIMS OK ..." when every check passes; exit 1 and one "ERROR" line per defect otherwise.
The format is README.md beside this file. same_as may name a wiki claim (W id, wikiaudit/claims.csv) or an earlier
claim of the same group.
"""
from __future__ import annotations

import argparse
import csv
import fnmatch
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
# Files whose candidates need no claim row, with the reason (Cowork ruling, T-AUD-22h). A claim row on one is an error.
OUT_OF_SCOPE = {
    "apps/ui/_sample_app_reference.py": "not production: imported by nothing, imports the absent `engine` package",
}


def norm(n: str) -> str:
    try:
        return repr(float(n))
    except ValueError:
        return n


def nums(s: str) -> set[str]:
    return {norm(n) for n in NUM_RE.findall(s)}


ESCAPE_RE = re.compile(r"\\u([0-9a-fA-F]{4})")


def unescape(s: str) -> str:
    """Decode JSON \\uXXXX escapes in a candidate line, so the hex digits of `\\u00b110` do not join the number 10
    (T-AUD-22e hand-back: 44 KG claims read `\\u00b1`, `\\u2013`, `\\u2212` or `\\u2192` right before a digit)."""
    return ESCAPE_RE.sub(lambda m: chr(int(m.group(1), 16)), s)


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
    ap.add_argument("--group", choices=sorted(PREFIX), required=True)
    ap.add_argument("--files", nargs="+", default=None, metavar="GLOB")
    args = ap.parse_args()
    group = args.group
    globs = args.files

    def in_scope(f: str) -> bool:
        return f not in OUT_OF_SCOPE and (globs is None or any(fnmatch.fnmatchcase(f, g) for g in globs))
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
        for f in FIELDS:
            if mojibake(r[f]):
                errors.append(f"ERROR {cid}: {f} is double-encoded (UTF-8 read as cp1252): {r[f][:40]!r}")
        if not re.fullmatch(rf"{pre}\d{{4}}", cid):
            errors.append(f"ERROR {cid}: claim_id must be {pre} + 4 digits")
        c = cands.get(r["cand_id"])
        if c is None:
            errors.append(f"ERROR {cid}: unknown cand_id {r['cand_id']}")
            continue
        covered.add(c["cand_id"])
        if c["file"] in OUT_OF_SCOPE:
            errors.append(f"ERROR {cid}: {c['file']} is out of scope ({OUT_OF_SCOPE[c['file']]})")
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
        missing = nums(r["value"]) - nums(unescape(c["text"]))
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
        if not c["auto"] and in_scope(c["file"]) and c["cand_id"] not in covered:
            errors.append(f"ERROR uncovered {c['cand_id']} {c['file']}:{c['line']}")
    for e in errors:
        print(e)
    if errors:
        print(f"CLAIMS FAIL {len(errors)} error(s)")
        return 1
    cls = Counter(r["class"] for r in claims)
    todo = sum(1 for c in cands.values() if not c["auto"] and in_scope(c["file"]))
    print("classes " + " ".join(f"{k}={cls[k]}" for k in sorted(cls)))
    print(f"suspect {sum(1 for r in claims if r['suspect'].strip())} "
          f"same_as_wiki {sum(1 for r in claims if r['same_as'].startswith('W'))}")
    scope = "" if globs is None else " scope=" + ",".join(globs)
    out = sum(1 for c in cands.values() if not c["auto"] and c["file"] in OUT_OF_SCOPE)
    if out:
        print(f"out_of_scope {out} candidate(s) in {len(OUT_OF_SCOPE)} file(s)")
    print(f"CLAIMS OK group={group}{scope} candidates {todo} covered claims {len(claims)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
