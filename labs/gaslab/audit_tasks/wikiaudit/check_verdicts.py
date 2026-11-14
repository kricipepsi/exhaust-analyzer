"""T-GASA-WIKIAUDIT / T-AUD-22: check sources.csv and verdicts.csv for one verification row (Cowork tool).

python -I check_verdicts.py --scope scope/<ROW>.txt
The scope file lists root claim ids (one per line, wiki register W… or code register GK/CK/RK…). Every listed claim
needs a verdict. A quote must appear in its source's fetched file (whitespace-normalised, case-sensitive).
Exit 0 and a last line "VERDICTS OK ..." when every check passes; exit 1 and one "ERROR" line per defect otherwise.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
REGISTERS = [HERE / "claims.csv"] + sorted((REPO / "apps" / "wired" / "audit_tasks" / "codeaudit").glob("claims_*.csv"))
SRC_FIELDS = ["source_id", "url", "title", "publisher", "kind", "fetched_file", "fetched_date"]
VER_FIELDS = ["claim_id", "verdict", "source_id", "quote", "source_value", "note"]
KINDS = {"PRIMARY_LAW", "PRIMARY_REGULATOR", "PRIMARY_STANDARD", "OEM", "TRADE", "ACADEMIC", "SECONDARY"}
PRIMARY = {"PRIMARY_LAW", "PRIMARY_REGULATOR", "PRIMARY_STANDARD"}
VERDICTS = {"CONFIRMED", "CONTRADICTED", "PARTLY", "CITATION_WRONG", "UNSOURCED"}
NEEDS_SOURCE = VERDICTS - {"UNSOURCED"}


def mojibake(s: str) -> bool:
    if s.isascii():
        return False
    try:
        return s.encode("cp1252").decode("utf-8") != s
    except (UnicodeEncodeError, UnicodeDecodeError):
        return False


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def read(path: Path, fields: list[str], errors: list[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        rd = csv.DictReader(fh)
        if rd.fieldnames != fields:
            errors.append(f"ERROR {path.name} header {rd.fieldnames} != {fields}")
            return []
        rows = list(rd)
    for i, r in enumerate(rows, 2):
        for f in fields:
            if mojibake(r[f] or ""):
                errors.append(f"ERROR {path.name}:{i} {f} is double-encoded (UTF-8 read as cp1252)")
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", required=True)
    scope_path = HERE / ap.parse_args().scope
    errors: list[str] = []
    claims: dict[str, dict[str, str]] = {}
    for reg in REGISTERS:
        for r in csv.DictReader(reg.open(encoding="utf-8")):
            claims[r["claim_id"]] = r
    scope = [s.strip() for s in scope_path.read_text(encoding="utf-8").splitlines() if s.strip()]
    sources = {r["source_id"]: r for r in read(HERE / "sources.csv", SRC_FIELDS, errors)}
    texts: dict[str, str] = {}
    for sid, s in sources.items():
        if not re.fullmatch(r"S\d{3}", sid):
            errors.append(f"ERROR source {sid}: id must be S + 3 digits")
        if s["kind"] not in KINDS:
            errors.append(f"ERROR source {sid}: kind {s['kind']!r} not in {sorted(KINDS)}")
        if not s["url"].startswith(("https://", "http://")):
            errors.append(f"ERROR source {sid}: url {s['url']!r}")
        f = HERE / s["fetched_file"]
        if not s["fetched_file"].startswith("sources/") or not f.is_file():
            errors.append(f"ERROR source {sid}: fetched_file {s['fetched_file']!r} is not a file under sources/")
        else:
            texts[sid] = squash(f.read_text(encoding="utf-8", errors="replace"))
    verdicts = read(HERE / "verdicts.csv", VER_FIELDS, errors)
    seen = Counter(v["claim_id"] for v in verdicts)
    for cid, k in seen.items():
        if k > 1:
            errors.append(f"ERROR duplicate verdict for {cid}")
    for v in verdicts:
        cid = v["claim_id"]
        c = claims.get(cid)
        if c is None:
            errors.append(f"ERROR verdict {cid}: not a claim in any register")
            continue
        if c["same_as"].strip():
            errors.append(f"ERROR verdict {cid}: has same_as {c['same_as']}; give the verdict to the root claim")
        if v["verdict"] not in VERDICTS:
            errors.append(f"ERROR verdict {cid}: {v['verdict']!r} not in {sorted(VERDICTS)}")
            continue
        if v["verdict"] == "UNSOURCED":
            if not v["note"].strip():
                errors.append(f"ERROR verdict {cid}: UNSOURCED needs a note naming what was searched")
            continue
        s = sources.get(v["source_id"])
        if s is None:
            errors.append(f"ERROR verdict {cid}: unknown source_id {v['source_id']!r}")
            continue
        q = squash(v["quote"])
        if len(q) < 12:
            errors.append(f"ERROR verdict {cid}: quote shorter than 12 characters")
        elif v["source_id"] in texts and q not in texts[v["source_id"]]:
            errors.append(f"ERROR verdict {cid}: quote not found in {s['fetched_file']}: {q[:60]!r}")
        if c["class"] == "LEGAL_LIMIT" and v["verdict"] in {"CONFIRMED", "CONTRADICTED"} and s["kind"] not in PRIMARY:
            errors.append(f"ERROR verdict {cid}: a LEGAL_LIMIT {v['verdict']} needs a PRIMARY_* source, got {s['kind']}")
        if v["verdict"] in {"CONTRADICTED", "PARTLY", "CITATION_WRONG"} and not v["source_value"].strip():
            errors.append(f"ERROR verdict {cid}: {v['verdict']} needs source_value (what the source says)")
    have = set(seen)
    for cid in scope:
        if cid not in claims:
            errors.append(f"ERROR scope {cid}: not a claim")
        elif cid not in have:
            errors.append(f"ERROR scope {cid}: no verdict")
    for e in errors:
        print(e)
    if errors:
        print(f"VERDICTS FAIL {len(errors)} error(s)")
        return 1
    in_scope = [v for v in verdicts if v["claim_id"] in set(scope)]
    cnt = Counter(v["verdict"] for v in in_scope)
    print("verdicts " + " ".join(f"{k}={cnt[k]}" for k in sorted(cnt)))
    print(f"sources {len(sources)} primary {sum(1 for s in sources.values() if s['kind'] in PRIMARY)}")
    print(f"VERDICTS OK scope={scope_path.name} claims {len(scope)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
