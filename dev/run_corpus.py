"""Corpus replay script for Layer-2 accuracy benchmark.

Reads cases_petrol_master_v6.csv and (once the engine exists) runs each case
through the diagnostic pipeline. For now, returns empty results since the
engine modules are not yet built.

source: V2_START_HERE.md L13 (corpus in CI from day one)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "cases" / "csv" / "cases_petrol_master_v6.csv"
OUTPUT_PATH = ROOT / "results" / "L2_latest.json"


def main() -> None:
    if not CORPUS_PATH.exists():
        print(f"Corpus not found at {CORPUS_PATH}")
        raise SystemExit(1)

    with open(CORPUS_PATH, encoding="utf-8") as f:
        header = f.readline()
    cols = header.strip().split(",")
    print(f"Corpus found: {CORPUS_PATH}")
    print(f"Columns: {len(cols)}")

    with open(CORPUS_PATH, encoding="utf-8") as f:
        case_count = sum(1 for _ in f) - 1
    print(f"Cases in corpus: {case_count}")

    results: dict[str, float] = {}
    print("Engine modules not yet built — returning empty results.")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Results written to {OUTPUT_PATH}")
    print("0 cases processed (engine not yet built).")


if __name__ == "__main__":
    main()
