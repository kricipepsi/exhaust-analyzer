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


class TestComputeStats:
    def test_numeric_columns_detected(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_count_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3

    def test_mean(self, sample_csv: Path) -> None:
        assert abs(compute_stats(sample_csv)["age"]["mean"] - 30.0) < 0.1

    def test_empty_csv(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("x,y\n")
            p = Path(f.name)
        try:
            assert compute_stats(p) == {}
        finally:
            p.unlink()


class TestWriteReport:
    def test_output_contains_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            rp = Path(f.name)
        try:
            write_report(stats, rp)
            text = rp.read_text()
            assert "age" in text and "score" in text
        finally:
            rp.unlink()
