from interval_merger import merge_intervals


def test_containment():
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]
