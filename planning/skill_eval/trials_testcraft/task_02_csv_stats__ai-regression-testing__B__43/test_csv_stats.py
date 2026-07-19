from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


def test_empty_csv_returns_empty_dict_regression(tmp_path: Path) -> None:
    """GUARD: a header-only CSV must yield {} (empty-rows branch)."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("a,b\n", encoding="utf-8")
    assert compute_stats(csv_file) == {}


def test_no_numeric_columns_returns_empty_regression(tmp_path: Path) -> None:
    """GUARD: a CSV with only text columns yields {} (numeric-filter branch)."""
    csv_file = tmp_path / "text.csv"
    csv_file.write_text("name,city\nAlice,NYC\nBob,LA\n", encoding="utf-8")
    assert compute_stats(csv_file) == {}


def test_missing_value_skipped_not_counted_regression(tmp_path: Path) -> None:
    """GUARD: non-numeric cells are skipped; count reflects only parsed values."""
    csv_file = tmp_path / "gappy.csv"
    csv_file.write_text("v\n10\n\n20\nNA\n30\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    assert stats["v"]["count"] == 3
    assert stats["v"]["min"] == pytest.approx(10.0)
    assert stats["v"]["max"] == pytest.approx(30.0)


def test_single_value_stdev_is_zero_boundary_regression(tmp_path: Path) -> None:
    """GUARD: stdev on one value is 0.0, not a StatisticsError (len>1 branch)."""
    csv_file = tmp_path / "one.csv"
    csv_file.write_text("v\n42\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    assert stats["v"]["count"] == 1
    assert stats["v"]["stdev"] == pytest.approx(0.0)


def test_all_stat_fields_present_parity_regression(tmp_path: Path) -> None:
    """GUARD: every column row carries the full stats contract (no missing field)."""
    csv_file = tmp_path / "full.csv"
    csv_file.write_text("v\n1\n2\n3\n4\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    required = {"count", "mean", "median", "min", "max", "stdev"}
    assert set(stats["v"]) == required


def test_report_written_for_every_column_regression(tmp_path: Path) -> None:
    """GUARD: write_report emits a line per column (no silently dropped column)."""
    csv_file = tmp_path / "two.csv"
    csv_file.write_text("a,b\n1,10\n2,20\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    report = tmp_path / "out.txt"
    write_report(stats, report)
    lines = [ln for ln in report.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) == 2
