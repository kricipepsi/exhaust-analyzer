"""T-GASA-WIKIAUDIT: list every digit-bearing line of the audited GASLab documents as a candidate (Cowork tool).

Writes candidates.csv beside this file: one row per line that holds a digit. A line whose digits all sit in
non-domain tokens (section numbers, file prefixes, dates, versions, finding / task / ADR ids, anchors, list markers)
gets auto=NON_DOMAIN and needs no claims.csv row. Every other candidate needs at least one claims.csv row.
Run from anywhere: python -I extract_candidates.py
"""
from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parents[1]  # repo/labs/gaslab
FILES = sorted(p.relative_to(LAB).as_posix() for p in (LAB / "wiki").glob("*.md")) + [
    "docs/GAS_VOCABULARY.md",
    "gaslab/data/gas_lab_ontology.yaml",
]

# Tokens that carry digits but no domain value. Stripped before the "any digit left?" test.
NON_DOMAIN = [
    r"\{#[^}]*\}",                                  # markdown anchors {#GAS_HC}
    r"\b(?:F|T|R|M|L|H)-[A-Z0-9]+(?:-[A-Za-z0-9]+)*",  # finding / task ids F-C2-14, T-GASA-7
    r"\bADR-\d+\b",
    r"\b20\d\d-\d\d-\d\d\b",                        # ISO dates
    r"\bv\d+(?:\.\d+)*\b",                          # versions v2.1
    r"\b\d\d[ab]?_[a-z_]+(?:\.md)?\b",              # wiki file names 03_five_gases_reference
    r"§\s*\d+(?:\.\d+)*",                           # section refs
    r"\bGASWIKI-\d+[A-Z]?\b",
    r"^\s*#+\s*\d+(?:\.\d+)*[a-z]?\b",              # heading numbers "## 3.1"
    r"^\s*\d+\.\s",                                 # ordered-list markers "1. "
    r"\bchunk\s+\d+\b",
]
NON_DOMAIN_RE = re.compile("|".join(NON_DOMAIN))


def main() -> None:
    rows = []
    for rel in FILES:
        text = (LAB / rel).read_text(encoding="utf-8").splitlines()
        for n, line in enumerate(text, 1):
            if not re.search(r"\d", line):
                continue
            stripped = NON_DOMAIN_RE.sub(" ", line)
            auto = "" if re.search(r"\d", stripped) else "NON_DOMAIN"
            sha = hashlib.sha1(line.encode("utf-8")).hexdigest()[:10]
            rows.append({"cand_id": f"C{len(rows) + 1:04d}", "file": rel, "line": n, "sha": sha, "auto": auto,
                         "text": line.strip()})
    out = HERE / "candidates.csv"
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["cand_id", "file", "line", "sha", "auto", "text"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    auto = sum(1 for r in rows if r["auto"])
    print(f"candidates {len(rows)} auto_non_domain {auto} to_classify {len(rows) - auto}")


if __name__ == "__main__":
    main()
