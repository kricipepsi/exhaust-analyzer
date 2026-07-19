"""Build artifact sanity checks — skipped if vinlab/data/ is empty."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parents[2] / "vinlab" / "data"


def _data_available() -> bool:
    required = ["wmi.csv", "vds_engine_map.csv", "years.csv", "vref.db"]
    return all((DATA_DIR / f).exists() for f in required)


pytestmark = pytest.mark.skipif(
    not _data_available(), reason="vinlab/data/ files not populated"
)


class TestVrefDb:
    def test_engine_ref_has_rows(self):
        """vref.db engine_ref table contains rows (68 as of T-VL-3 build)."""
        conn = sqlite3.connect(str(DATA_DIR / "vref.db"))
        try:
            count = conn.execute("SELECT COUNT(*) FROM engine_ref").fetchone()[0]
            assert count >= 1, "engine_ref table is empty"
        finally:
            conn.close()

    def test_engine_ref_schema(self):
        """engine_ref has the required schema columns."""
        conn = sqlite3.connect(str(DATA_DIR / "vref.db"))
        try:
            cur = conn.execute("PRAGMA table_info(engine_ref)")
            columns = {row[1] for row in cur.fetchall()}
        finally:
            conn.close()
        required = {
            "engine_code", "brand", "displacement_cc", "euro_norm",
            "induction_type", "fuel_delivery_type", "has_egr",
            "o2_type",
        }
        missing = required - columns
        assert not missing, f"Missing columns in engine_ref: {missing}"
        assert "has_secondary_air" not in columns, "has_secondary_air must not be present in engine_ref"

    def test_5fr_equipment_row_is_complete(self):
        """T-VIN-FIX-2: presentation engine has sourced equipment and CoC values."""
        conn = sqlite3.connect(str(DATA_DIR / "vref.db"))
        conn.row_factory = sqlite3.Row
        try:
            row = conn.execute(
                "SELECT * FROM engine_ref WHERE engine_code = '5FR'"
            ).fetchone()
        finally:
            conn.close()

        assert row is not None
        assert row["displacement_cc"] == 1598
        assert row["euro_norm"] == "euro5"
        assert row["has_turbo"] == 1
        assert row["has_gdi"] == 1
        assert row["has_map"] == 1
        assert row["induction_type"] == "TURBOCHARGED"
        assert row["fuel_delivery_type"] == "GDI"
        assert row["o2_type"] == "NB"
        confidence_fields = (
            "target_lambda_v112",
            "target_rpm_u2",
            "idle_rpm_low",
            "co_low_idle",
            "co_high_idle",
            "co_type_approval",
            "hc_type_approval",
            "nox_type_approval",
            "co2_type_approval",
        )
        assert all(row[field] is not None for field in confidence_fields)


class TestWmiCsv:
    def test_header_contains_required_columns(self):
        """wmi.csv first row is a header with required columns."""
        with (DATA_DIR / "wmi.csv").open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            columns = set(reader.fieldnames or [])
        required = {"wmi", "brand", "country", "era_hint"}
        assert required <= columns, f"Missing columns: {required - columns}"

    def test_row_count_reasonable(self):
        """wmi.csv contains thousands of WMI entries."""
        with (DATA_DIR / "wmi.csv").open("r", encoding="utf-8", newline="") as fh:
            count = sum(1 for _ in csv.DictReader(fh))
        assert count > 1000, f"Expected >1000 WMI rows, got {count}"


class TestYearsCsv:
    def test_l_code_has_two_entries(self):
        """Year code 'L' has exactly two rows (1990 ERA_1, 2020 ERA_3)."""
        with (DATA_DIR / "years.csv").open("r", encoding="utf-8", newline="") as fh:
            rows = [r for r in csv.DictReader(fh) if r["year_code"] == "L"]
        assert len(rows) == 2, f"Expected 2 L-code rows, got {len(rows)}"
        eras = {r["era_bucket"] for r in rows}
        assert eras == {"ERA_1", "ERA_3"}, f"Expected ERA_1 + ERA_3, got {eras}"
        years = {int(r["calendar_year"]) for r in rows}
        assert years == {1990, 2020}, f"Expected 1990 + 2020, got {years}"


class TestEngineCodeCoverage:
    def test_engine_code_overlap_exists(self):
        """At least some vds_engine_map.csv engine codes exist in vref.db.

        Full coverage is a known data gap (T-VL-5a): CSV and DB use
        different engine-code formats. Only ~0.6% overlap currently.
        """
        csv_codes: set[str] = set()
        with (DATA_DIR / "vds_engine_map.csv").open("r", encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                ec = row.get("engine_code", "").strip()
                if ec:
                    csv_codes.add(ec)

        conn = sqlite3.connect(str(DATA_DIR / "vref.db"))
        try:
            db_codes = {
                r[0] for r in conn.execute("SELECT engine_code FROM engine_ref")
            }
        finally:
            conn.close()

        overlap = csv_codes & db_codes
        assert len(overlap) > 0, (
            "No engine_code overlap between vds_engine_map.csv and vref.db"
        )
