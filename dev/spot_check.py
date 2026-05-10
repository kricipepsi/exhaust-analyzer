"""Spot-check: run a few corpus cases through the pipeline."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dev.run_corpus import csv_to_input
from engine.v2.pipeline import diagnose


def main() -> None:
    corpus = Path(__file__).resolve().parent.parent / "cases" / "csv" / "cases_petrol_master_v6.csv"
    with corpus.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    for row in rows[:8]:
        expected_state = row.get("expected_state", "").strip()
        expected_fault = row.get("expected_top_fault", "").strip()
        try:
            di = csv_to_input(row)
        except Exception:
            continue
        result = diagnose(di)
        case_id = row.get("case_id", "")
        fault = result["primary"]["fault_id"] if result["primary"] else "None"
        raw = round(result["primary"]["raw_score"], 3) if result["primary"] else 0
        print(
            f"{case_id}: state={result['state']} (exp={expected_state}) "
            f"fault={fault} (exp={expected_fault}) raw={raw}"
        )


if __name__ == "__main__":
    main()
