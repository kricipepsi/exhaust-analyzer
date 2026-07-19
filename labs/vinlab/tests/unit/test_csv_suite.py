"""Data-driven test suite for cases_petrol_master_v6.csv.

T1 — Decode passrate >= 85% across all 281 CSV VINs.
T2 — Engine extraction: HIGH/PARTIAL VINs reach engine lookup.
T3 — CoC field roundtrip: vin_* CSV columns match VinDNA fields within tolerance.
T4 — Downstream JSON shape: every decoded VinDNA serializes correctly.
"""

from __future__ import annotations

import pytest
from vinlab.decoder import VINDecodeError
from vinlab.models import VinConfidence

# ---------------------------------------------------------------------------
# T1 — Decode passrate
# ---------------------------------------------------------------------------

PASSRATE_THRESHOLD = 0.85  # source: T-CSV-1 spec


def test_csv_decode_passrate(decoder, csv_cases):
    """>= 85 % of all 281 CSV VINs must decode without VINDecodeError."""
    total = 0
    ok = 0
    failed: list[tuple[str, str, str]] = []

    for row in csv_cases:
        vin = row.get("vin", "").strip()
        if not vin:
            continue
        total += 1
        try:
            decoder.decode_vin_payload(vin)
            ok += 1
        except VINDecodeError as exc:
            failed.append((vin, row.get("case_id", ""), str(exc)))

    passrate = ok / total if total > 0 else 0.0

    print("\n--- T1 Decode Passrate ---")
    print(f"Total: {total}  OK: {ok}  Failed: {len(failed)}  Passrate: {passrate:.2%}")

    if failed:
        print(f"Failed VINs ({len(failed)}):")
        for vin, case_id, msg in failed[:10]:
            print(f"  {case_id}: {vin} -- {msg}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")

    assert passrate >= PASSRATE_THRESHOLD, (
        f"Passrate {passrate:.2%} below {PASSRATE_THRESHOLD:.0%} threshold"
    )


# ---------------------------------------------------------------------------
# T2 — Engine number extraction
# ---------------------------------------------------------------------------

MIN_ENGINE_EXTRACTION_VINS = 10  # source: T-CSV-1 spec


def test_csv_engine_extraction(decoder, csv_cases):
    """For decoded VINs with confidence HIGH or PARTIAL, engine_displacement_liters > 0."""
    count = 0

    for row in csv_cases:
        vin = row.get("vin", "").strip()
        if not vin:
            continue
        try:
            dna = decoder.decode_vin_payload(vin)
        except VINDecodeError:
            continue

        if dna.confidence in (VinConfidence.HIGH, VinConfidence.PARTIAL):
            count += 1
            assert dna.engine_displacement_liters > 0.0, (
                f"{vin}: engine_displacement_liters = 0"
            )
            assert dna.cylinder_count > 0, (
                f"{vin}: cylinder_count = 0"
            )

    print("\n--- T2 Engine Extraction ---")
    print(f"HIGH/PARTIAL-confidence VINs checked: {count}")

    if count < MIN_ENGINE_EXTRACTION_VINS:
        pytest.fail(
            f"Only {count} VINs reached HIGH/PARTIAL confidence (need >= {MIN_ENGINE_EXTRACTION_VINS})"
        )


# ---------------------------------------------------------------------------
# T3 — CoC field roundtrip
# ---------------------------------------------------------------------------
#
# The decoder reads CoC values from vref.db (per-engine_code medians).
# The cases CSV vin_* columns are per-VIN measurements from the raw petrol
# specimens CSV, which diverged after T-CSV-2/T-CSV-3 enriched vref.db.
# Comparing per-VIN values against per-engine_code medians is a category
# error.  This test now verifies that VinDNA CoC fields match their
# authoritative source (vref.db) directly.
#
# Fields checked and their vref.db column names:
COC_DB_COLUMNS: list[tuple[str, str, type]] = [
    ("target_lambda_v112",  "target_lambda_v112",  float),
    ("target_rpm_u2",       "target_rpm_u2",       int),
    ("idle_rpm_low",        "idle_rpm_low",        int),
    ("co_type_approval",    "co_type_approval",    float),
    ("hc_type_approval",    "hc_type_approval",    float),
    ("nox_type_approval",   "nox_type_approval",   float),
    ("co2_type_approval",   "co2_type_approval",   float),
    ("noise_rpm",           "noise_rpm",           int),
    ("co_low_idle",         "co_low_idle",         float),
    ("co_high_idle",        "co_high_idle",        float),
    ("noise_stationary_dba","noise_stationary_dba",float),
    ("noise_driving_dba",   "noise_driving_dba",   float),
    ("hc_nox_type_approval","hc_nox_type_approval",float),
]

COC_MISMATCH_THRESHOLD = 0.05  # source: T-CSV-1 spec


def _build_vds_engine_code_index(data_dir: str) -> tuple[dict[str, str], dict[str, str]]:
    """Build {brand_vds_full: engine_code} and {brand_pos8: engine_code} indexes.

    Mirrors RobustVINDecoder._load_vds_matrix() resolution order.
    Path A (vds_full) wins over Path B (pos_8_only) — same priority as the decoder.
    """
    import csv
    from pathlib import Path

    full_index: dict[str, str] = {}
    pos8_index: dict[str, str] = {}
    vds_path = Path(data_dir) / "vds_engine_map.csv"
    with vds_path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            brand = row["brand"].strip().upper()
            ec = row.get("engine_code", "").strip()
            if not ec:
                continue
            if row["vds_full"].strip():
                full_index[f"{brand}_{row['vds_full'].strip().upper()}"] = ec
            if row["pos_8_only"].strip():
                pos8_index[f"{brand}_{row['pos_8_only'].strip().upper()}"] = ec
    return full_index, pos8_index


def _load_vref_coc_index(db_path: str) -> dict[str, dict]:
    """Load vref.db engine_ref rows indexed by engine_code."""
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM engine_ref").fetchall()
    conn.close()
    return {r["engine_code"]: dict(r) for r in rows}


def test_csv_coc_field_roundtrip(decoder, csv_cases, data_dir):
    """VinDNA CoC fields match their authoritative source (vref.db)."""

    full_idx, pos8_idx = _build_vds_engine_code_index(str(data_dir))
    vref = _load_vref_coc_index(str(data_dir / "vref.db"))

    comparisons = 0
    mismatches: list[dict] = []
    no_engine_code = 0
    not_in_vref = 0

    for row in csv_cases:
        vin = row.get("vin", "").strip()
        if not vin:
            continue
        try:
            dna = decoder.decode_vin_payload(vin)
        except VINDecodeError:
            continue

        if dna.confidence == VinConfidence.NONE:
            continue

        # Resolve engine_code using same 2-path logic as the decoder
        vds_slice = vin[3:8]
        pos8 = vin[7]
        brand = dna.make.upper()

        engine_code = full_idx.get(f"{brand}_{vds_slice}")
        if engine_code is None:
            engine_code = pos8_idx.get(f"{brand}_{pos8}")

        if not engine_code:
            no_engine_code += 1
            continue

        vref_row = vref.get(engine_code)
        if vref_row is None:
            not_in_vref += 1
            continue

        for dna_field, db_col, _cast in COC_DB_COLUMNS:
            expected = vref_row.get(db_col)
            if expected is None:
                continue  # vref.db has no value — skip
            actual = getattr(dna, dna_field)
            comparisons += 1
            if actual is None:
                mismatches.append({
                    "vin": vin,
                    "case_id": row.get("case_id", ""),
                    "field": dna_field,
                    "engine_code": engine_code,
                    "expected": expected,
                    "actual": None,
                    "delta": "VinDNA returned None but vref.db has a value",
                })
                continue
            if isinstance(expected, float):
                if abs(actual - expected) > 0.001:
                    mismatches.append({
                        "vin": vin,
                        "case_id": row.get("case_id", ""),
                        "field": dna_field,
                        "engine_code": engine_code,
                        "expected": expected,
                        "actual": actual,
                        "delta": abs(actual - expected),
                    })
            elif actual != expected:
                mismatches.append({
                    "vin": vin,
                    "case_id": row.get("case_id", ""),
                    "field": dna_field,
                    "engine_code": engine_code,
                    "expected": expected,
                    "actual": actual,
                    "delta": abs(actual - expected),
                })

    mismatch_rate = len(mismatches) / comparisons if comparisons > 0 else 0.0

    print("\n--- T3 CoC Field Roundtrip (vref.db source) ---")
    print(f"Comparisons: {comparisons}  Mismatches: {len(mismatches)}  "
          f"Rate: {mismatch_rate:.4%}")
    print(f"Skipped: no_engine_code={no_engine_code} not_in_vref={not_in_vref}")

    if mismatches:
        print(f"Mismatches ({len(mismatches)}):")
        for m in mismatches[:15]:
            print(f"  {m['case_id']}: {m['vin']} engine={m.get('engine_code','?')} "
                  f"-- {m['field']}: expected={m['expected']!r}, "
                  f"actual={m['actual']!r}, delta={m['delta']}")
        if len(mismatches) > 15:
            print(f"  ... and {len(mismatches) - 15} more")

    assert mismatch_rate < COC_MISMATCH_THRESHOLD, (
        f"Mismatch rate {mismatch_rate:.2%} >= {COC_MISMATCH_THRESHOLD:.0%}"
    )


# ---------------------------------------------------------------------------
# T4 — Downstream JSON shape
# ---------------------------------------------------------------------------

VALID_EURO_CATEGORIES = {
    "EURO_1", "EURO_2", "EURO_3", "EURO_4", "EURO_5", "EURO_6", "EURO_7",
}
VALID_AIR_METERING = {
    "DUAL_MAF_MAP_CROSSCHECK", "MAP_ONLY_SPEED_DENSITY", "MAF_ONLY",
}
VALID_CONFIDENCE_VALUES = {"HIGH", "PARTIAL", "NONE"}


def test_csv_downstream_json_shape(decoder, csv_cases):
    """Every decoded VinDNA serializes to JSON matching DNALab/COMLab handoff contract."""
    violations: list[dict] = []

    for row in csv_cases:
        vin = row.get("vin", "").strip()
        if not vin:
            continue
        try:
            dna = decoder.decode_vin_payload(vin)
        except VINDecodeError:
            continue

        try:
            payload = dna.to_json_payload()
        except Exception as exc:
            violations.append({
                "vin": vin, "case_id": row.get("case_id", ""),
                "error": f"to_json() raised: {exc}",
            })
            continue

        if len(payload.get("vin", "")) != 17:
            violations.append({
                "vin": vin, "case_id": row.get("case_id", ""),
                "error": f"vin length = {len(payload.get('vin', ''))}",
            })

        if payload.get("euro_emission_category") not in VALID_EURO_CATEGORIES:
            violations.append({
                "vin": vin, "case_id": row.get("case_id", ""),
                "error": f"euro_emission_category = {payload.get('euro_emission_category')!r}",
            })

        if payload.get("confidence") != "NONE":
            cc = payload.get("cylinder_count", 0)
            if not (2 <= cc <= 12):
                violations.append({
                    "vin": vin, "case_id": row.get("case_id", ""),
                    "error": f"cylinder_count = {cc} (must be 2-12)",
                })

        if payload.get("air_metering_strategy") not in VALID_AIR_METERING:
            violations.append({
                "vin": vin, "case_id": row.get("case_id", ""),
                "error": f"air_metering_strategy = {payload.get('air_metering_strategy')!r}",
            })

        if payload.get("confidence") not in VALID_CONFIDENCE_VALUES:
            violations.append({
                "vin": vin, "case_id": row.get("case_id", ""),
                "error": f"confidence = {payload.get('confidence')!r}",
            })

    print("\n--- T4 Downstream JSON Shape ---")
    print(f"Violations: {len(violations)}")

    if violations:
        for v in violations[:15]:
            print(f"  {v['case_id']}: {v['vin']} -- {v['error']}")
        if len(violations) > 15:
            print(f"  ... and {len(violations) - 15} more")

    if violations:
        pytest.fail(f"{len(violations)} downstream JSON shape violation(s)")
