from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats


@pytest.fixture
def sample(tmp_path: Path) -> Path:
    p = tmp_path / "data.csv"
    p.write_text("name,age\nAlice,30\nBob,\nCarol,invalid\nDan,32\n", encoding="utf-8")
    return p


def test_skips_non_numeric_and_missing(sample: Path) -> None:
    stats = compute_stats(sample)
    assert stats["age"]["count"] == 2


def test_empty_csv_returns_empty(tmp_path: Path) -> None:
    p = tmp_path / "empty.csv"
    p.write_text("a,b\n", encoding="utf-8")
    assert compute_stats(p) == {}
