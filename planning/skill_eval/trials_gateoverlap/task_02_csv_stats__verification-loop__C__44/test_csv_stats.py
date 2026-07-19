from csv_stats import compute_stats


def test_basic(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("v\n1\n2\n3\n")
    assert compute_stats(p)["v"]["count"] == 3
