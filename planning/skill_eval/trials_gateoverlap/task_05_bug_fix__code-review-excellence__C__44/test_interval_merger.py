from interval_merger import merge_intervals


def test_containment() -> None:
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]


def test_basic_overlap_preserved() -> None:
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]
