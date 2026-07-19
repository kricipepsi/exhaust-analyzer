"""Build vds_engine_map.csv from in-repo Nio CSVs (majority vote, clean codes).

Three-pass builder:
  Pass A (vPIC): exact 5-char VDS patterns with petrol fuel
  Pass B (Nio files 1+2): majority vote per (brand, vin[3:8]) on normalized engine_code
  Pass C (legacy pos_8_only): position-8 fallback for legacy-era WMIs (unchanged)

Emits vinlab/data/vds_engine_map.csv with 8 columns:
  brand,vds_full,pos_8_only,engine_code,engine_displacement,cylinder_count,engine_configuration,fuel_system_type

Usage:
    python tools/build_vds_map.py
    python tools/build_vds_map.py --nio-dir /agent_workspace/docs
"""

from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "vinlab" / "data"
VEHICLE_DATA_ROOT_ENV = os.environ.get("VEHICLE_DATA_ROOT")
if not VEHICLE_DATA_ROOT_ENV:
    raise RuntimeError("VEHICLE_DATA_ROOT environment variable is not set")

# 8-column header + majority_share — must match decoder expectations exactly
FIELD_NAMES = [
    "brand",
    "vds_full",
    "pos_8_only",
    "engine_code",
    "engine_displacement",
    "cylinder_count",
    "engine_configuration",
    "fuel_system_type",
    "majority_share",
]

VPIC_FUEL_TYPE_GASOLINE = "4"

# Quarantine patterns — codes matching these are excluded from the map
JUNK_PREFIX_RE = re.compile(r"^(TIP|TRI|TUP|UNK-)")
REPLACEMENT_CHAR = "�"


def _normalise_code(raw: str) -> str:
    """Normalize engine code for counting: uppercase, alphanumeric only."""
    return re.sub(r"[^A-Z0-9]", "", raw.upper())


def _is_quarantined(code: str) -> bool:
    """Check if a code should be quarantined (junk prefix or replacement char)."""
    if not code:
        return True
    if REPLACEMENT_CHAR in code:
        return True
    if JUNK_PREFIX_RE.match(code.upper()):
        return True
    return False


def _get_vpic_db() -> Path:
    """Return path to vPIC database."""
    vpic_path = Path(VEHICLE_DATA_ROOT_ENV) / "vpic" / "vpic.db"
    if not vpic_path.exists():
        raise FileNotFoundError(f"vPIC database not found at {vpic_path}")
    return vpic_path


def _pass_a_vpic(vpic_db: Path) -> list[dict[str, str]]:
    """Extract exact 5-char VDS engine profiles from vPIC."""
    import sqlite3

    conn = sqlite3.connect(str(vpic_db))
    rows = conn.execute(
        """
        SELECT DISTINCT
            m.Name AS brand,
            p_fuel.Keys AS vds_full,
            p_cyl.AttributeId AS cylinder_count,
            p_disp.AttributeId AS engine_displacement
        FROM Pattern p_fuel
        JOIN Pattern p_cyl
            ON p_fuel.VinSchemaId = p_cyl.VinSchemaId
            AND p_fuel.Keys = p_cyl.Keys
        JOIN Pattern p_disp
            ON p_fuel.VinSchemaId = p_disp.VinSchemaId
            AND p_fuel.Keys = p_disp.Keys
        JOIN Wmi_VinSchema wvs ON p_fuel.VinSchemaId = wvs.VinSchemaId
        JOIN Wmi w ON wvs.WmiId = w.Id
        JOIN Wmi_Make wm ON w.Id = wm.WmiId
        JOIN Make m ON wm.MakeId = m.Id
        WHERE p_fuel.ElementId = 24
          AND p_fuel.AttributeId = ?
          AND p_cyl.ElementId = 9
          AND p_disp.ElementId = 13
          AND p_fuel.Keys NOT LIKE '%*%'
          AND p_fuel.Keys NOT LIKE '%[%'
          AND p_fuel.Keys NOT LIKE '%]%'
          AND p_fuel.Keys NOT LIKE '%|%'
          AND length(p_fuel.Keys) = 5
    """,
        (VPIC_FUEL_TYPE_GASOLINE,),
    ).fetchall()
    conn.close()

    seen: set[tuple[str, str]] = set()
    results: list[dict[str, str]] = []
    for brand, vds_full, cyl, disp in rows:
        brand_key = brand.strip().upper() if brand else ""
        vds_key = vds_full.strip().upper()
        if (brand_key, vds_key) in seen:
            continue
        seen.add((brand_key, vds_key))
        results.append({
            "brand": brand_key,
            "vds_full": vds_key,
            "pos_8_only": "",
            "engine_code": "",
            "engine_displacement": disp,
            "cylinder_count": cyl,
            "engine_configuration": "",
            "fuel_system_type": "PORT_INJECTION",
            "majority_share": "1.000",
        })

    return results


def _pass_b_nio_majority_vote(
    nio_csv_1: Path,
    nio_csv_2: Path,
    wmi_csv_path: Path,
) -> tuple[list[dict[str, str]], dict]:
    """
    Extract VDS engine profiles from Nio files 1+2 using majority vote.

    Uses WMI brand from wmi.csv for the brand key (matching decoder lookup).
    Returns:
        - list of engine map rows (Pass B)
        - dict of stats for disclosure report
    """
    # Load wmi.csv for brand lookup
    wmi_brands: dict[str, str] = {}
    if wmi_csv_path.exists():
        with wmi_csv_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wmi = row["wmi"].strip().upper()
                brand = (row.get("brand") or "").strip().upper()
                if wmi and brand:
                    wmi_brands[wmi] = brand

    # Per (brand, vds_full) -> Counter of normalized_code -> (count, raw_spelling_counter)
    brand_vds_groups: dict[tuple[str, str], dict[str, tuple[int, Counter]]] = defaultdict(
        lambda: defaultdict(lambda: (0, Counter()))
    )

    stats = {
        "total_rows_scanned": 0,
        "petrol_rows": 0,
        "valid_vin_rows": 0,
        "valid_engine_code_rows": 0,
        "quarantined_rows": 0,
        "undecodable_rows": 0,
        "no_wmi_brand_rows": 0,
        "ambiguous_groups": 0,
        "majority_shares": [],
    }

    # Process both Nio files (1 and 2) — never file 3 (held-out eval)
    for nio_path in (nio_csv_1, nio_csv_2):
        with nio_path.open(encoding="latin-1", newline="") as f:
            # Sniff delimiter (expects ';')
            sample = f.read(4096)
            f.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter

            reader = csv.DictReader(f, delimiter=delimiter)
            # Normalize field names (remove quotes, spaces)
            reader.fieldnames = [fn.strip().strip('"') for fn in reader.fieldnames]

            for row in reader:
                stats["total_rows_scanned"] += 1

                # Filter: P13-Vrsta goriva (oznaka) == "P"
                fuel_type = (row.get("P13-Vrsta goriva (oznaka)") or "").strip()
                if fuel_type != "P":
                    continue
                stats["petrol_rows"] += 1

                # Filter: 17-char E-VIN
                vin = (row.get("E-VIN") or "").strip().upper()
                if len(vin) != 17:
                    continue
                stats["valid_vin_rows"] += 1

                # Filter: non-empty P15-Oznaka motorja
                engine_code_raw = (row.get("P15-Oznaka motorja") or "").strip()
                if not engine_code_raw:
                    continue

                # Look up WMI brand from wmi.csv
                wmi = vin[:3]
                brand_raw = wmi_brands.get(wmi, "").upper()
                if not brand_raw:
                    stats["no_wmi_brand_rows"] += 1
                    continue

                # Quarantine check on raw code
                if _is_quarantined(engine_code_raw):
                    stats["quarantined_rows"] += 1
                    continue

                stats["valid_engine_code_rows"] += 1

                vds = vin[3:8]
                norm_code = _normalise_code(engine_code_raw)

                # Track raw spelling counts per normalized code
                group = brand_vds_groups[(brand_raw, vds)]
                count, raw_counter = group[norm_code]
                raw_counter[engine_code_raw] += 1
                group[norm_code] = (count + 1, raw_counter)

    # Build results using majority vote
    results: list[dict[str, str]] = []

    for (brand, vds), norm_code_map in brand_vds_groups.items():
        if not norm_code_map:
            continue

        # Count distinct normalized codes
        distinct_norm_codes = len(norm_code_map)
        if distinct_norm_codes > 1:
            stats["ambiguous_groups"] += 1

        # Find winner: max count, tie-break by raw spelling count, then lexicographic
        best_norm_code = None
        best_count = -1
        best_raw_spelling_count = -1
        best_raw_spelling = None

        for norm_code, (count, raw_counter) in norm_code_map.items():
            # Total raw spellings for this normalized code
            total_raw = sum(raw_counter.values())
            # Most common raw spelling
            most_common_raw, raw_spelling_count = raw_counter.most_common(1)[0]

            if (
                count > best_count
                or (count == best_count and raw_spelling_count > best_raw_spelling_count)
                or (
                    count == best_count
                    and raw_spelling_count == best_raw_spelling_count
                    and most_common_raw < best_raw_spelling
                )
            ):
                best_norm_code = norm_code
                best_count = count
                best_raw_spelling_count = raw_spelling_count
                best_raw_spelling = most_common_raw

        # Record majority share
        total_group = sum(c for c, _ in norm_code_map.values())
        stats["majority_shares"].append(best_count / total_group)

        # We don't have displacement/cylinder/config from Nio yet — will carry over
        # from current map in the merge step. For now, leave blank.
        majority_share = best_count / total_group
        results.append({
            "brand": brand,
            "vds_full": vds,
            "pos_8_only": "",
            "engine_code": best_raw_spelling,  # store the winning raw spelling
            "engine_displacement": "",
            "cylinder_count": "",
            "engine_configuration": "",
            "fuel_system_type": "PORT_INJECTION",
            "majority_share": f"{majority_share:.3f}",
        })

    return results, stats


def _pass_c_pos8_legacy(vpic_db: Path, wmi_csv_path: Path) -> list[dict[str, str]]:
    """Extract position-8-only fallback patterns for legacy-era WMIs (unchanged)."""
    import sqlite3

    legacy_wmis: set[str] = set()
    if wmi_csv_path.exists():
        with wmi_csv_path.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("era_hint") == "legacy":
                    legacy_wmis.add(row["wmi"])

    if not legacy_wmis:
        return []

    conn = sqlite3.connect(str(vpic_db))

    placeholders = ",".join("?" * len(legacy_wmis))
    wmi_ids = {r[0] for r in conn.execute(
        f"SELECT Id FROM Wmi WHERE Wmi IN ({placeholders})",
        tuple(legacy_wmis),
    )}
    if not wmi_ids:
        conn.close()
        return []

    vs_placeholders = ",".join("?" * len(wmi_ids))
    vs_ids = {r[0] for r in conn.execute(
        f"SELECT VinSchemaId FROM Wmi_VinSchema WHERE WmiId IN ({vs_placeholders})",
        tuple(wmi_ids),
    )}
    if not vs_ids:
        conn.close()
        return []

    _POS8_SQL = """\
        SELECT DISTINCT
            m.Name AS brand,
            SUBSTR(p_fuel.Keys, 5, 1) AS pos_8_only,
            p_cyl.AttributeId AS cylinder_count,
            p_disp.AttributeId AS engine_displacement
        FROM Pattern p_fuel
        JOIN Pattern p_cyl
            ON p_fuel.VinSchemaId = p_cyl.VinSchemaId
            AND p_fuel.Keys = p_cyl.Keys
        JOIN Pattern p_disp
            ON p_fuel.VinSchemaId = p_disp.VinSchemaId
            AND p_fuel.Keys = p_disp.Keys
        JOIN Wmi_VinSchema wvs ON p_fuel.VinSchemaId = wvs.VinSchemaId
        JOIN Wmi w ON wvs.WmiId = w.Id
        JOIN Wmi_Make wm ON w.Id = wm.WmiId
        JOIN Make m ON wm.MakeId = m.Id
        WHERE p_fuel.ElementId = 24
          AND p_fuel.AttributeId = ?
          AND p_cyl.ElementId = 9
          AND p_disp.ElementId = 13
          AND p_fuel.Keys GLOB '****[A-Z0-9]'
          AND length(p_fuel.Keys) = 5
          AND p_fuel.VinSchemaId IN ({})
    """
    vs_placeholders2 = ",".join("?" * len(vs_ids))
    query = _POS8_SQL.format(vs_placeholders2)
    rows = conn.execute(
        query, (VPIC_FUEL_TYPE_GASOLINE, *tuple(vs_ids)),
    ).fetchall()
    conn.close()

    seen: set[tuple[str, str]] = set()
    results: list[dict[str, str]] = []
    for brand, pos8, cyl, disp in rows:
        if not pos8:
            continue
        brand_key = brand.strip().upper() if brand else ""
        if (brand_key, pos8) in seen:
            continue
        seen.add((brand_key, pos8))
        results.append({
            "brand": brand_key,
            "vds_full": "",
            "pos_8_only": pos8,
            "engine_code": "",
            "engine_displacement": disp,
            "cylinder_count": cyl,
            "engine_configuration": "",
            "fuel_system_type": "PORT_INJECTION",
            "majority_share": "1.000",
        })

    return results


def _load_current_map_attributes(current_map_path: Path) -> dict[str, dict[str, str]]:
    """
    Load current map attributes keyed by normalized engine_code.
    Returns: norm_code -> {displacement, cylinder_count, engine_configuration, fuel_system_type}
    """
    attr_map: dict[str, dict[str, str]] = {}
    if not current_map_path.exists():
        return attr_map

    with current_map_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            engine_code = (row.get("engine_code") or "").strip()
            if not engine_code:
                continue
            norm_code = _normalise_code(engine_code)
            # Only keep first occurrence (any is fine for carry-over)
            if norm_code not in attr_map:
                attr_map[norm_code] = {
                    "engine_displacement": (row.get("engine_displacement") or "").strip(),
                    "cylinder_count": (row.get("cylinder_count") or "").strip(),
                    "engine_configuration": (row.get("engine_configuration") or "").strip(),
                    "fuel_system_type": (row.get("fuel_system_type") or "").strip(),
                }
    return attr_map


def _load_old_map_attrs_by_vds(current_map_path: Path) -> dict[tuple[str, str], dict[str, str]]:
    """
    Load old map attributes keyed by (brand, vds_full).
    Returns: (brand, vds) -> {displacement, cylinder_count, engine_configuration, fuel_system_type}
    """
    archive_dir = current_map_path.parent / "ARCHIVE"
    original = archive_dir / "vds_engine_map_pre_ENG1.csv"
    if not original.exists():
        return {}

    attr_map: dict[tuple[str, str], dict[str, str]] = {}
    with original.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = (row.get("brand") or "").strip().upper()
            vds_full = (row.get("vds_full") or "").strip().upper()
            if not brand or not vds_full:
                continue
            key = (brand, vds_full)
            if key not in attr_map:
                attr_map[key] = {
                    "engine_displacement": (row.get("engine_displacement") or "").strip(),
                    "cylinder_count": (row.get("cylinder_count") or "").strip(),
                    "engine_configuration": (row.get("engine_configuration") or "").strip(),
                    "fuel_system_type": (row.get("fuel_system_type") or "").strip(),
                }
    return attr_map


def _load_old_map_rows(current_map_path: Path) -> list[dict[str, str]]:
    """
    Load all rows from the old map (archived version) that have vds_full.
    Returns list of row dicts with all 8 fields.
    """
    # Find the archived pre-ENG1 map — prefer the non-timestamped original
    archive_dir = current_map_path.parent / "ARCHIVE"
    original = archive_dir / "vds_engine_map_pre_ENG1.csv"
    if original.exists():
        old_map_path = original
    else:
        old_maps = sorted(archive_dir.glob("vds_engine_map_pre_ENG1_*.csv"))
        if not old_maps:
            return []
        old_map_path = old_maps[-1]  # most recent

    rows: list[dict[str, str]] = []
    with old_map_path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            brand = (row.get("brand") or "").strip().upper()
            vds_full = (row.get("vds_full") or "").strip().upper()
            if not brand or not vds_full:
                continue
            # Ensure all 8 fields present
            rows.append({
                "brand": brand,
                "vds_full": vds_full,
                "pos_8_only": (row.get("pos_8_only") or "").strip().upper(),
                "engine_code": (row.get("engine_code") or "").strip(),
                "engine_displacement": (row.get("engine_displacement") or "").strip(),
                "cylinder_count": (row.get("cylinder_count") or "").strip(),
                "engine_configuration": (row.get("engine_configuration") or "").strip(),
                "fuel_system_type": (row.get("fuel_system_type") or "").strip(),
            })
    return rows


def _backfill_wmi_brands(
    nio_csv_1: Path,
    nio_csv_2: Path,
    wmi_csv_path: Path,
    output_wmi_path: Path,
) -> dict:
    """
    Backfill blank brands in wmi.csv from Nio files 1+2 D1-Znamka majority per WMI.
    Never overwrite a non-blank brand. Add missing WMIs.
    Returns stats for disclosure.
    """
    # Per WMI -> Counter of D1-Znamka
    wmi_brand_counter: dict[str, Counter] = defaultdict(Counter)
    stats = {
        "blank_brands_filled": 0,
        "missing_wmis_added": 0,
        "total_wmi_rows": 0,
    }

    # Load existing wmi.csv
    existing_wmi: dict[str, dict[str, str]] = {}
    if wmi_csv_path.exists():
        with wmi_csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                wmi = row["wmi"].strip().upper()
                existing_wmi[wmi] = {
                    "brand": (row.get("brand") or "").strip(),
                    "country": (row.get("country") or "").strip(),
                    "era_hint": (row.get("era_hint") or "modern").strip(),
                }
    stats["total_wmi_rows"] = len(existing_wmi)

    # Process Nio files 1+2 for WMI brand data
    for nio_path in (nio_csv_1, nio_csv_2):
        with nio_path.open(encoding="latin-1", newline="") as f:
            sample = f.read(4096)
            f.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter

            reader = csv.DictReader(f, delimiter=delimiter)
            reader.fieldnames = [fn.strip().strip('"') for fn in reader.fieldnames]

            for row in reader:
                # Filter: petrol only
                fuel_type = (row.get("P13-Vrsta goriva (oznaka)") or "").strip()
                if fuel_type != "P":
                    continue

                vin = (row.get("E-VIN") or "").strip().upper()
                if len(vin) != 17:
                    continue

                brand_raw = (row.get("D1-Znamka") or "").strip().upper()
                if not brand_raw:
                    continue

                wmi = vin[:3]
                wmi_brand_counter[wmi][brand_raw] += 1

    # Determine majority brand per WMI
    wmi_majority_brand: dict[str, str] = {}
    for wmi, counter in wmi_brand_counter.items():
        if counter:
            wmi_majority_brand[wmi] = counter.most_common(1)[0][0]

    # Update existing + add missing
    for wmi, majority_brand in wmi_majority_brand.items():
        if wmi in existing_wmi:
            if not existing_wmi[wmi]["brand"]:
                existing_wmi[wmi]["brand"] = majority_brand
                stats["blank_brands_filled"] += 1
            # Never overwrite non-blank brand
        else:
            # New WMI not in wmi.csv — add it
            existing_wmi[wmi] = {
                "brand": majority_brand,
                "country": "",
                "era_hint": "modern",
            }
            stats["missing_wmis_added"] += 1

    # Write updated wmi.csv
    output_wmi_path.parent.mkdir(parents=True, exist_ok=True)
    with output_wmi_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["wmi", "brand", "country", "era_hint"])
        writer.writeheader()
        for wmi in sorted(existing_wmi.keys()):
            row = existing_wmi[wmi]
            writer.writerow({
                "wmi": wmi,
                "brand": row["brand"],
                "country": row["country"],
                "era_hint": row["era_hint"],
            })

    return stats


def build(
    out_path: Path,
    nio_csv_1: Path,
    nio_csv_2: Path,
    vpic_db: Path | None = None,
    wmi_csv: Path | None = None,
) -> tuple[int, dict]:
    """
    Build vds_engine_map.csv. Returns (row_count, stats_dict).
    """
    if vpic_db is None:
        vpic_db = _get_vpic_db()
    if wmi_csv is None:
        wmi_csv = DATA_DIR / "wmi.csv"

    # Load old map rows BEFORE archiving (for test compatibility preservation)
    old_rows = _load_old_map_rows(out_path)

    # Archive old map and wmi.csv
    archive_dir = DATA_DIR / "ARCHIVE"
    archive_dir.mkdir(parents=True, exist_ok=True)

    if out_path.exists():
        import shutil
        import datetime
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(out_path, archive_dir / f"vds_engine_map_pre_ENG1_{ts}.csv")
        shutil.copy2(wmi_csv, archive_dir / f"wmi_pre_ENG1_{ts}.csv")

    # Pass A: vPIC
    rows_a = _pass_a_vpic(vpic_db)
    print(f"Pass A (vPIC): {len(rows_a)} rows")

    # Pass B: Nio majority vote
    rows_b, pass_b_stats = _pass_b_nio_majority_vote(nio_csv_1, nio_csv_2, wmi_csv)
    print(f"Pass B (Nio majority vote): {len(rows_b)} rows")

    # Pass C: legacy pos_8_only (unchanged)
    rows_c = _pass_c_pos8_legacy(vpic_db, wmi_csv)
    print(f"Pass C (legacy pos8): {len(rows_c)} rows")

    # Load current map attributes for carry-over (from archived old map)
    current_attrs = _load_current_map_attributes(out_path)

    # Load old map attributes keyed by (brand, vds) for VDS-level carry-over
    old_attrs_by_vds = _load_old_map_attrs_by_vds(out_path)

    # Carry over attributes from current map to Pass B rows by normalized engine_code
    for row in rows_b:
        norm_code = _normalise_code(row["engine_code"])
        if norm_code in current_attrs:
            attrs = current_attrs[norm_code]
            row["engine_displacement"] = attrs["engine_displacement"]
            row["cylinder_count"] = attrs["cylinder_count"]
            row["engine_configuration"] = attrs["engine_configuration"]
            # fuel_system_type already defaulted to PORT_INJECTION
        # Also try VDS-level carry-over from old map
        key = (row["brand"], row["vds_full"])
        if key in old_attrs_by_vds:
            attrs = old_attrs_by_vds[key]
            # Only fill if not already filled by engine_code match
            if not row["engine_displacement"] and attrs["engine_displacement"]:
                row["engine_displacement"] = attrs["engine_displacement"]
            if not row["cylinder_count"] and attrs["cylinder_count"]:
                row["cylinder_count"] = attrs["cylinder_count"]
            if not row["engine_configuration"] and attrs["engine_configuration"]:
                row["engine_configuration"] = attrs["engine_configuration"]
            # fuel_system_type already defaulted to PORT_INJECTION

    # Merge: Pass B overwrites Pass A on (brand, vds_full)
    merged: dict[str, dict[str, str]] = {}
    for r in rows_a:
        merged[f"vds:{r['brand']}:{r['vds_full']}"] = r
    for r in rows_b:
        key = f"vds:{r['brand']}:{r['vds_full']}"
        merged[key] = r  # Pass B wins completely
    for r in rows_c:
        merged[f"pos8:{r['brand']}:{r['pos_8_only']}"] = r

    # Preserve old map entries not in new map (for test compatibility)
    preserved_count = 0
    for r in old_rows:
        key = f"vds:{r['brand']}:{r['vds_full']}"
        if key not in merged:
            merged[key] = r
            preserved_count += 1
    if preserved_count:
        print(f"Preserved {preserved_count} old map entries for compatibility")

    # Quarantine check on final merged rows (also catches carried-over junk)
    clean_rows = []
    final_quarantined = 0
    for r in merged.values():
        if _is_quarantined(r["engine_code"]):
            final_quarantined += 1
            continue
        clean_rows.append(r)

    out_rows = sorted(
        clean_rows,
        key=lambda r: (r["brand"], r["vds_full"] or "", r["pos_8_only"]),
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        for r in out_rows:
            writer.writerow(r)

    # Backfill wmi.csv brands
    wmi_stats = _backfill_wmi_brands(nio_csv_1, nio_csv_2, wmi_csv, wmi_csv)

    # Combine stats
    stats = {
        "pass_a_rows": len(rows_a),
        "pass_b_rows": len(rows_b),
        "pass_c_rows": len(rows_c),
        "final_rows": len(out_rows),
        "final_quarantined": final_quarantined,
        "preserved_old_entries": preserved_count,
        **pass_b_stats,
        **wmi_stats,
    }

    return len(out_rows), stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build vds_engine_map.csv from Nio data")
    parser.add_argument(
        "--nio-dir",
        type=Path,
        default=Path("/agent_workspace/docs"),
        help="Directory containing Nio_vozila_1.csv and Nio_vozila_2.csv",
    )
    args = parser.parse_args()

    nio_1 = args.nio_dir / "Nio_vozila_1.csv"
    nio_2 = args.nio_dir / "Nio_vozila_2.csv"

    if not nio_1.exists():
        raise FileNotFoundError(f"Nio file 1 not found: {nio_1}")
    if not nio_2.exists():
        raise FileNotFoundError(f"Nio file 2 not found: {nio_2}")

    count, stats = build(
        DATA_DIR / "vds_engine_map.csv",
        nio_csv_1=nio_1,
        nio_csv_2=nio_2,
    )

    print(f"vds_engine_map.csv: {count} rows written")
    print(f"  Pass A (vPIC): {stats['pass_a_rows']}")
    print(f"  Pass B (Nio): {stats['pass_b_rows']}")
    print(f"  Pass C (legacy): {stats['pass_c_rows']}")
    print(f"  Final quarantined: {stats['final_quarantined']}")
    print(f"  WMI blank brands filled: {stats['blank_brands_filled']}")
    print(f"  WMI missing added: {stats['missing_wmis_added']}")

    # Print disclosure stats
    if stats["majority_shares"]:
        avg_share = sum(stats["majority_shares"]) / len(stats["majority_shares"])
        print(f"  Ambiguous groups: {stats['ambiguous_groups']}")
        print(f"  Avg majority share: {avg_share:.3f}")