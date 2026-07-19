#!/usr/bin/env python3
"""T-SHIP-3 — repair corrupted brand spellings in the VIN data CSVs.

Two corruption classes broke the brand -> engine-map join (fold-keys cannot
recover a *dropped* letter):
  1. Diacritic-stripped: ``ŠKODA`` written as ``KODA`` (wmi.csv rows TMB/TNB and
     445 legacy vds_engine_map.csv rows).
  2. Mojibake: ``�KODA`` (30 rows) / ``CITRO�N`` (1 row) in vds_engine_map.csv —
     decypher-era ``errors="replace"`` artifacts (audit 2026-07-06 §2.3).

Repairs are an explicit spelling table (no guessing). On duplicate
brand+vds_full keys after renaming, the row with a populated ``majority_share``
(the T-VIN-ENG-1 rebuild provenance column) wins; ties keep the first row.
Deterministic and idempotent.
"""
from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "vinlab" / "data"
# Keys are matched AFTER stripping control chars (C0/C1) and U+FFFD from the raw
# cell — covers both the \x8a-prefixed latin-1 misdecode ("\x8aKODA") and the
# UTF-8 replacement-char mojibake ("\ufffdKODA", "CITRO\ufffdN").
REPAIRS = {"KODA": "SKODA", "CITRON": "CITROEN"}


def _clean(brand: str) -> str:
    return "".join(c for c in brand if ord(c) >= 32 and not (127 <= ord(c) < 160) and c != "\ufffd")


def _repaired(brand: str) -> str | None:
    cleaned = _clean(brand.strip())
    if cleaned != brand.strip() or cleaned in REPAIRS:
        return REPAIRS.get(cleaned, cleaned)
    return None


def repair_wmi(path: Path) -> int:
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    fixed = 0
    for row in rows:
        new = _repaired(row.get("brand") or "")
        if new is not None:
            row["brand"] = new
            fixed += 1
    if fixed:
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
    return fixed


def repair_map(path: Path) -> tuple[int, int]:
    rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
    fieldnames = list(rows[0].keys())
    fixed = 0
    for row in rows:
        new = _repaired(row.get("brand") or "")
        if new is not None:
            row["brand"] = new
            fixed += 1
    # Dedupe on brand+vds_full: prefer rows with populated majority_share (ENG-1 provenance).
    kept: dict[tuple[str, str], dict[str, str]] = {}
    dropped = 0
    for row in rows:
        key = (row.get("brand", ""), row.get("vds_full", ""))
        current = kept.get(key)
        if current is None:
            kept[key] = row
        elif not (current.get("majority_share") or "").strip() and (row.get("majority_share") or "").strip():
            kept[key] = row
            dropped += 1
        else:
            dropped += 1
    if fixed or dropped:
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(kept.values())
    return fixed, dropped


def main() -> None:
    wmi_fixed = repair_wmi(DATA_DIR / "wmi.csv")
    map_fixed, map_dropped = repair_map(DATA_DIR / "vds_engine_map.csv")
    print(f"wmi.csv brands repaired: {wmi_fixed}")
    print(f"vds_engine_map.csv brands repaired: {map_fixed}, duplicate keys dropped: {map_dropped}")


if __name__ == "__main__":
    main()
