from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv() -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\nAlice,30,85.5\nBob,25,92.0\nCharlie,35,78.3\n")
        path = Path(f.name)
    yield path
    path.unlink()


class DescribeComputeStats:
    def test_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert "age" in stats
        assert "score" in stats
        assert "name" not in stats
        assert stats["age"]["count"] == 3

    def test_mean_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert abs(stats["age"]["mean"] - 30.0) < 0.1

    def test_min_max(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0

    def test_empty_csv(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age\n")
            path = Path(f.name)
        try:
            assert compute_stats(path) == {}
        finally:
            path.unlink()

    def test_missing_values_skipped(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("a,b\n1,2\nN/A,3\n3,\n")
            path = Path(f.name)
        try:
            stats = compute_stats(path)
            assert stats["a"]["count"] == 2  # 1 and 3, N/A skipped
            assert stats["b"]["count"] == 2  # 2 and 3, blank skipped
        finally:
            path.unlink()


class DescribeWriteReport:
    def test_writes_file(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            report_path = Path(f.name)
        try:
            write_report(stats, report_path)
            content = report_path.read_text()
            assert "age" in content
            assert "score" in content
        finally:
            report_path.unlink()
