from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,score\nAlice,30,85.5\nBob,25,92.0\nCharlie,35,78.3\n",
        encoding="utf-8",
    )
    return csv_file


class TestComputeStats:
    def test_detects_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_count_is_row_count(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3

    def test_mean_is_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["mean"] == pytest.approx(30.0)

    def test_min_and_max(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["min"] == pytest.approx(25.0)
        assert stats["age"]["max"] == pytest.approx(35.0)

    def test_empty_csv_returns_empty(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("name,city\n", encoding="utf-8")
        assert compute_stats(csv_file) == {}

    def test_non_numeric_values_skipped(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "mixed.csv"
        csv_file.write_text("v\n1\nNA\n3\n", encoding="utf-8")
        stats = compute_stats(csv_file)
        assert stats["v"]["count"] == 2
        assert stats["v"]["mean"] == pytest.approx(2.0)


class TestWriteReport:
    def test_report_contains_each_column(self, sample_csv: Path, tmp_path: Path) -> None:
        stats = compute_stats(sample_csv)
        report = tmp_path / "report.txt"
        write_report(stats, report)
        text = report.read_text(encoding="utf-8")
        assert "age:" in text
        assert "score:" in text
