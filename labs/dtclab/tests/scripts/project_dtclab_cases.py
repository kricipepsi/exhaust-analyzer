"""T-TST-7: Project dtclab_cases.csv from the reconciled master CSV.

Reads the reconciled master (post T-MASTER-RECON), filters DTC-decidable rows,
and writes the DTCLab fixture using only columns present in the master. This is a
pure projection: DTC cells are carried as raw strings and no DTCLab runtime code
or DTC regex is invoked.
"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from pathlib import Path

FOUR_DLAB_ROOT = Path(__file__).resolve().parents[5]
MASTER = FOUR_DLAB_ROOT / "TestSuite" / "cases_petrol_master_v6.csv"
OUT = Path(__file__).resolve().parent.parent / "fixtures" / "dtclab_cases.csv"

EXPECTED_ROW_COUNT = 194

INPUT_COLS = [
    "dtcs",
    "ff_dtcs",
    "ff_ect",
    "ff_rpm",
    "ff_load",
    "ff_map",
    "ff_stft_b1",
    "ff_ltft_b1",
    "fuel_status",
]

EXPECTED_COLS = [
    "expected_routing_tags",
    "expected_historical_context",
    "expected_freeze_frame_status",
]

OUTPUT_COLS = ["case_id", *INPUT_COLS, *EXPECTED_COLS, "gt_source"]
REQUIRED_MASTER_COLS = {"case_id", "lab_decidability", *INPUT_COLS}


def parse_dtc_cell(value: str) -> list[str]:
    """Split a master DTC cell into tokens without validating DTC syntax."""
    return [token.strip() for token in value.split(",") if token.strip()]


def build_gt_source() -> str:
    """Build the gt_source field for characterization-only expected outputs."""
    parts = ["gt_method=characterization"]
    parts.extend(f"{col}:characterization" for col in EXPECTED_COLS)
    return "; ".join(parts)


def require_master_columns(fieldnames: Sequence[str] | None) -> None:
    """Raise if the reconciled master does not expose required projection columns."""
    if fieldnames is None:
        raise ValueError(f"Master CSV has no header: {MASTER}")

    missing = sorted(REQUIRED_MASTER_COLS.difference(fieldnames))
    if missing:
        missing_cols = ", ".join(missing)
        raise ValueError(f"Master CSV missing required DTCLab columns: {missing_cols}")


def project_row(row: dict[str, str]) -> dict[str, str]:
    """Project one DTC-decidable master row into the DTCLab fixture schema."""
    projected = {"case_id": row.get("case_id", "")}
    for col in INPUT_COLS:
        projected[col] = row.get(col, "")

    for col in EXPECTED_COLS:
        projected[col] = ""

    projected["gt_source"] = build_gt_source()
    return projected


def project_rows(master_path: Path) -> list[dict[str, str]]:
    """Read and project all DTC-decidable rows from the master CSV."""
    if not master_path.exists():
        raise FileNotFoundError(f"Master CSV not found: {master_path}")

    rows_out: list[dict[str, str]] = []

    with master_path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        require_master_columns(reader.fieldnames)

        for row in reader:
            if "DTC" not in row.get("lab_decidability", ""):
                continue
            rows_out.append(project_row(row))

    if len(rows_out) != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_ROW_COUNT} DTC-decidable rows, found {len(rows_out)}"
        )

    return rows_out


def write_rows(rows: list[dict[str, str]], out_path: Path) -> None:
    """Write projected rows to the DTCLab fixture CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_COLS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    """Generate the DTCLab projected fixture from the reconciled master."""
    rows = project_rows(MASTER)
    write_rows(rows, OUT)

    non_empty_dtcs = sum(bool(parse_dtc_cell(row["dtcs"])) for row in rows)
    non_empty_ff_dtcs = sum(bool(parse_dtc_cell(row["ff_dtcs"])) for row in rows)
    print(
        f"Wrote {len(rows)} DTC-decidable rows to {OUT} "
        f"({non_empty_dtcs} with dtcs, {non_empty_ff_dtcs} with ff_dtcs)"
    )


if __name__ == "__main__":
    main()
