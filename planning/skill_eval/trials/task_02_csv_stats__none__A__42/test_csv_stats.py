import tempfile
from pathlib import Path
from csv_stats import compute_stats, write_report


def test_compute_stats():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\nAlice,30,85.5\nBob,25,92.0\nCharlie,35,78.3\n")
        tmp = f.name

    try:
        stats = compute_stats(Path(tmp))
        assert "age" in stats
        assert "score" in stats
        assert stats["age"]["count"] == 3
        assert abs(stats["age"]["mean"] - 30.0) < 0.1
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0
    finally:
        Path(tmp).unlink()


def test_empty_csv():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age\n")
        tmp = f.name
    try:
        stats = compute_stats(Path(tmp))
        assert stats == {}
    finally:
        Path(tmp).unlink()
