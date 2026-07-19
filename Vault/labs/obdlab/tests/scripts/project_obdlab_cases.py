"""T-TST-6: Project obdlab_cases.csv from the reconciled master CSV.

Reads the reconciled master (post T-MASTER-RECON), filters OBD-decidable rows,
maps column names per the MASTER_RECON_REPORT inventory, derives DNA-relative
columns, and writes the per-lab fixture.
"""

from __future__ import annotations

import csv
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
MASTER = REPO_ROOT / "TestSuite" / "cases_petrol_master_v6.csv"
OUT = Path(__file__).resolve().parent.parent / "fixtures" / "obdlab_cases.csv"

# Column-name mapping per MASTER_RECON_REPORT.md §"Master → OBD input-column inventory"
COLUMN_MAP = {
    "rpm": "engine_rpm",
    "ect": "coolant_temp_c",
    "maf": "mass_airflow_gps",
    "map": "manifold_vacuum_kpa",
    "stft_b1": "shrtft1",
    "ltft_b1": "longft1",
    "stft_b2": "shrtft2",
    "ltft_b2": "longft2",
}

# Expected-output columns — all characterization (master has no OBD ground truth)
EXPECTED_COLS = [
    "expected_obd_lambda",
    "expected_ve_pct",
    "expected_ve_validity",
    "expected_trim_analytics_gate",
    "expected_maf_status",
    "expected_map_status",
    "expected_o2_failure_mode",
]

# Input columns to carry through from master (beyond the mapped ones)
PASSTHROUGH_COLS = [
    "case_id",
    "fuel_status",
    "obd_lambda",
    "o2_upstream_classification",
    "o2_downstream_voltage",
]

# Output column order
OUTPUT_COLS = (
    ["case_id"]
    + list(COLUMN_MAP.values())
    + ["calculated_engine_load_pct", "number_of_banks", "has_maf", "has_map"]
    + PASSTHROUGH_COLS[1:]  # case_id already included
    + EXPECTED_COLS
    + ["gt_source"]
)


def derive_number_of_banks(bank_config: str) -> str:
    """Derive number_of_banks from bank_config field."""
    cfg = bank_config.strip().lower()
    if cfg == "dual":
        return "2"
    return "1"


def derive_has_maf(maf_val: str) -> str:
    """Derive has_maf from MAF column presence."""
    return str(maf_val.strip() != "").lower()


def derive_has_map(map_val: str) -> str:
    """Derive has_map from MAP column presence."""
    return str(map_val.strip() != "").lower()


def build_gt_source() -> str:
    """Build the gt_source field for a row whose expected outputs are all characterization."""
    parts = ["gt_method=characterization"]
    for col in EXPECTED_COLS:
        parts.append(f"{col}:characterization")
    return "; ".join(parts)


def main() -> None:
    if not MASTER.exists():
        raise FileNotFoundError(f"Master CSV not found: {MASTER}")

    rows_out: list[dict[str, str]] = []

    with open(MASTER, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lab_decidability = row.get("lab_decidability", "")
            if "OBD" not in lab_decidability:
                continue

            out: dict[str, str] = {}

            # case_id
            out["case_id"] = row.get("case_id", "")

            # Map input columns
            for master_col, out_col in COLUMN_MAP.items():
                out[out_col] = row.get(master_col, "")

            # Derived columns
            bank_config = row.get("bank_config", "single")
            out["number_of_banks"] = derive_number_of_banks(bank_config)
            out["has_maf"] = derive_has_maf(row.get("maf", ""))
            out["has_map"] = derive_has_map(row.get("map", ""))

            # calculated_engine_load_pct — absent from master, default empty
            out["calculated_engine_load_pct"] = ""

            # Passthrough columns
            for col in PASSTHROUGH_COLS[1:]:  # skip case_id
                out[col] = row.get(col, "")

            # Expected output columns — all characterization
            for col in EXPECTED_COLS:
                out[col] = ""

            # gt_source
            out["gt_source"] = build_gt_source()

            rows_out.append(out)

    with open(OUT, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLS)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"Wrote {len(rows_out)} OBD-decidable rows to {OUT}")


if __name__ == "__main__":
    main()
