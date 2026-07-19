from pathlib import Path

from csv_stats import compute_stats


def test_compute_stats(tmp_path: Path):
    csv_file = tmp_path / "d.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,20\n")
    stats = compute_stats(csv_file)
    assert "age" in stats
