from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals into a sorted, non-overlapping list.

    Intervals are closed [start, end].  Overlapping and contained intervals
    are merged into their enclosing interval.

    >>> merge_intervals([(1, 3), (2, 6), (8, 10)])
    [(1, 6), (8, 10)]
    >>> merge_intervals([(1, 10), (2, 5)])   # containment
    [(1, 10)]
    """
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda iv: iv[0])
    merged: list[tuple[int, int]] = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last_start, last_end = merged[-1]
        cur_start, cur_end = current

        if cur_start <= last_end:
            # Overlap or containment — take the wider end boundary
            merged[-1] = (last_start, max(last_end, cur_end))
        else:
            merged.append(current)

    return merged
