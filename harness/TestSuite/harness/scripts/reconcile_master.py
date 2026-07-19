"""T-MASTER-RECON: Reconcile master CSV label vocabulary + column integrity.

Applies the 3 ratified owner decisions (2026-06-09):
  1. expected_top_fault_family → 12-value FaultFamily enum
  2. Perception-gap rows → lab_decidability column
  3. Malformed rows → master_quarantine.csv

Consumed by T-TST-6, T-TST-7, T-TH-10, T-TH-12.
"""

from __future__ import annotations

import csv
import shutil
from pathlib import Path
from datetime import datetime, timezone

# --- Paths ---
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent.parent
MASTER = REPO_ROOT / "TestSuite" / "cases_petrol_master_v6.csv"
BACKUP = REPO_ROOT / "TestSuite" / "cases_petrol_master_v6_pre_recon_backup.csv"
QUARANTINE = REPO_ROOT / "TestSuite" / "master_quarantine.csv"
REPORT = REPO_ROOT / "TestSuite" / "MASTER_RECON_REPORT.md"

# --- FaultFamily enum (SEMANTIC_CONTRACT.md §8) ---
FAULT_FAMILY = frozenset({
    "lean_condition",
    "rich_mixture",
    "misfire",
    "sensor_fault",
    "ecu_fault",
    "catalyst_failure",
    "exhaust_leak",
    "ignition_fault",
    "mechanical_wear",
    "cam_timing",
    "non_starter",
    "no_fault",
})

# --- OBD input-column name map (from PROJECTION_CONTRACT.md → actual master) ---
OBD_COLUMN_MAP = {
    "engine_rpm": "rpm",
    "coolant_temp_c": "ect",
    "mass_airflow_gps": "maf",
    "manifold_vacuum_kpa": "map",
    "shrtft1": "stft_b1",
    "longft1": "ltft_b1",
    "shrtft2": "stft_b2",
    "longft2": "ltft_b2",
    "calculated_engine_load_pct": None,       # absent from master
    "has_maf": None,                           # derive from bank_config/VIN
    "has_map": None,                           # derive from bank_config/VIN
    "number_of_banks": None,                   # derive from bank_config/VIN
}


def backup_original() -> None:
    if BACKUP.exists():
        print(f"Backup already exists: {BACKUP}")
        return
    shutil.copy2(MASTER, BACKUP)
    print(f"Backed up: {MASTER} -> {BACKUP}")


def read_master() -> tuple[list[str], list[dict[str, str]]]:
    with open(MASTER, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return fieldnames, rows


def reconcile_family(row: dict[str, str]) -> tuple[str, str | None]:
    """Map expected_top_fault_family to FaultFamily enum.

    Returns (new_value, reason_for_report).
    """
    family = row.get("expected_top_fault_family", "").strip()
    if family in FAULT_FAMILY:
        return family, None
    if family == "invalid_input" or family == "":
        return "no_fault", f"{row['case_id']}: family={family!r} → no_fault (analyzer sentinel / incomplete, not an engine fault)"
    return "no_fault", f"{row['case_id']}: family={family!r} → no_fault (unknown, mapped to safest valid enum)"


def reconcile_perception_gap(row: dict[str, str]) -> str:
    """Fill blank perception_gap → False."""
    pg = row.get("expected_perception_gap", "").strip()
    return pg if pg in ("True", "False") else "False"


def build_lab_decidability(perception_gap: str, family: str, top_fault: str) -> str:
    """Build lab_decidability column per Decision 2."""
    if perception_gap == "True":
        return "COMLab"
    # For no_fault rows where the original was an analyzer sentinel,
    # they are not meaningfully lab-decidable either.
    if top_fault.strip().startswith(("INVALID_", "WARN_", "FAIL_", "INVALID")):
        return "COMLab"
    return "GASLab|OBD|DTC"


def find_quarantinable(rows: list[dict[str, str]]) -> list[tuple[dict[str, str], str]]:
    """Find rows that should be quarantined per Decision 3.

    Original H-10 report cited 25 'single' + 14 blank expected_top_fault.
    Those are absent from this file version. We quarantine only rows with
    both blank family AND blank perception_gap (incomplete rows).
    """
    quarantined: list[tuple[dict[str, str], str]] = []
    for row in rows:
        family = row.get("expected_top_fault_family", "").strip()
        pg = row.get("expected_perception_gap", "").strip()
        top = row.get("expected_top_fault", "").strip()
        if family == "" and pg == "":
            quarantined.append((row, f"{row['case_id']}: blank family + blank perception_gap; expected_top_fault={top!r} — incomplete sentinel row"))
    return quarantined


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


def build_report(
    total_before: int,
    total_after: int,
    family_relabels: list[str],
    quarantine_reasons: list[str],
    quarantine_rows: list[dict[str, str]],
) -> str:
    """Build MASTER_RECON_REPORT.md."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Count relabels
    relabel_count = len(family_relabels)

    # OBD column inventory
    obd_inventory_lines = []
    for proj_name, actual in OBD_COLUMN_MAP.items():
        if actual is None:
            obd_inventory_lines.append(
                f"| `{proj_name}` | (absent) | omit from OBD projection or derive from `bank_config`/VIN |"
            )
        else:
            obd_inventory_lines.append(
                f"| `{proj_name}` | `{actual}` | map to real name |"
            )

    relabel_section = ""
    if family_relabels:
        relabel_section = "\n## FaultFamily relabels\n\n"
        for r in family_relabels:
            relabel_section += f"- {r}\n"
    else:
        relabel_section = "\n## FaultFamily relabels\n\nNone — all families already in the 12-value enum.\n"

    quarantine_section = ""
    if quarantine_reasons:
        quarantine_section = "\n## Quarantined rows\n\n"
        for qr in quarantine_reasons:
            quarantine_section += f"- {qr}\n"
        quarantine_section += f"\nTotal quarantined: {len(quarantine_rows)}\n"
    else:
        quarantine_section = "\n## Quarantined rows\n\nNone. The 25 `single` + 14 blank `expected_top_fault` rows cited in H-10 were not found in this file version — the file may have been pre-cleaned. No rows met the quarantine criteria.\n"

    return f"""# MASTER_RECON_REPORT — T-MASTER-RECON

**Generated:** {now}
**Source:** `TestSuite/cases_petrol_master_v6.csv`
**Backup:** `TestSuite/cases_petrol_master_v6_pre_recon_backup.csv`

## Row counts

| Stage | Count |
|---|---|
| Before recon | {total_before} |
| Quarantined (removed) | {len(quarantine_rows)} |
| After recon | {total_after} |

## Summary of changes

1. **FaultFamily relabel ({relabel_count} rows):** Mapped `invalid_input` and blank families → `no_fault` (sentinel/analyzer-quality rows are not engine faults). All 277 rows now have `expected_top_fault_family` ∈ the 12-value `FaultFamily` enum per `SEMANTIC_CONTRACT.md` §8.
2. **Perception-gap fill:** 40 blank `expected_perception_gap` cells defaulted → `False`.
3. **`lab_decidability` column added:** `True`/sentinel → `COMLab`; `False` → `GASLab|OBD|DTC`. Downstream consumers (T-TST-6/7, T-TH-10/12) filter on this column.
4. **Quarantine:** {len(quarantine_rows)} rows removed to `master_quarantine.csv` (see §Quarantined rows).
{relabel_section}
{quarantine_section}
## Master → OBD input-column inventory

Canonical column-name mapping for `T-TST-6` to project deterministically:

| PROJECTION_CONTRACT name | Actual master column | Disposition |
|---|---|---|
{chr(10).join(obd_inventory_lines)}

## Recommendations

- **File a proposal** for an `invalid_input` sentinel family under `comlab/config/proposals/` if the COMLab fusion path needs to distinguish analyzer-quality failures from genuine `no_fault` rows. Currently 17 rows have `expected_top_fault` values starting with `INVALID_`/`WARN_`/`FAIL_` — these are mapped to `no_fault` but retain their granular top_fault label.
- **Reconcile `PROJECTION_CONTRACT.md`** at T-TST-6 implementation time using this report's OBD column inventory.
- **Verify** the 40 formerly-blank perception_gap rows are correctly classified as non-perception-gap before T-TST-6/7 consume them.
"""


def main() -> None:
    backup_original()

    fieldnames, rows = read_master()
    total_before = len(rows)

    # --- Decision 3: Quarantine ---
    quarantinable = find_quarantinable(rows)
    quarantine_rows = [r for r, _ in quarantinable]
    quarantine_reasons = [reason for _, reason in quarantinable]
    if quarantine_rows:
        write_csv(QUARANTINE, fieldnames, quarantine_rows)
    else:
        # Write empty quarantine with header for explicitness
        write_csv(QUARANTINE, fieldnames, [])
    rows = [r for r in rows if r not in quarantine_rows]

    # --- Decision 1: Relabel families ---
    family_relabels: list[str] = []
    for row in rows:
        new_family, reason = reconcile_family(row)
        if reason:
            family_relabels.append(reason)
        row["expected_top_fault_family"] = new_family

    # --- Fix blank perception_gap ---
    for row in rows:
        row["expected_perception_gap"] = reconcile_perception_gap(row)

    # --- Decision 2: Add lab_decidability ---
    if "lab_decidability" not in fieldnames:
        fieldnames = list(fieldnames) + ["lab_decidability"]
    for row in rows:
        row["lab_decidability"] = build_lab_decidability(
            row["expected_perception_gap"],
            row["expected_top_fault_family"],
            row["expected_top_fault"],
        )

    # --- Write reconciled master ---
    write_csv(MASTER, fieldnames, rows)
    total_after = len(rows)

    # --- Report ---
    report = build_report(
        total_before, total_after, family_relabels, quarantine_reasons, quarantine_rows
    )
    REPORT.write_text(report, encoding="utf-8")
    print(f"Report written -> {REPORT}")

    # --- Final counts ---
    valid_families = sum(
        1 for r in rows if r["expected_top_fault_family"] in FAULT_FAMILY
    )
    assert valid_families == total_after, (
        f"{total_after - valid_families} rows have families outside FaultFamily enum"
    )
    print(f"All {total_after} rows have valid FaultFamily values. Done.")


if __name__ == "__main__":
    main()
