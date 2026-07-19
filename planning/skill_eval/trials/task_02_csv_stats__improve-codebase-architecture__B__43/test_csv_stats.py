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
    def test_detects_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_statistics(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3
        assert abs(stats["age"]["mean"] - 30.0) < 0.1
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0

    def test_empty(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("a\n")
            p = Path(f.name)
        try:
            assert compute_stats(p) == {}
        finally:
            p.unlink()


class TestWriteReport:
    def test_writes_summary(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            rp = Path(f.name)
        try:
            write_report(stats, rp)
            assert "age" in rp.read_text()
        finally:
            rp.unlink()
