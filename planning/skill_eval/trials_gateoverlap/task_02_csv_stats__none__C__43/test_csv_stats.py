from csv_stats import compute_stats


def test_compute_stats(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("name,age\nAlice,30\nBob,20\n")
    stats = compute_stats(p)
    assert stats["age"]["count"] == 2
