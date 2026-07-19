"""Interval merger with a containment bug.

THIS IS THE BUGGY VERSION the coder receives as starting code.
The coder fixes it and writes the result as `interval_merger.py`.
"""

from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals.

    Args:
        intervals: List of (start, end) intervals.

    Returns:
        Sorted, non-overlapping list of merged intervals.

    Examples:
        >>> merge_intervals([(1, 3), (2, 6), (8, 10)])
        [(1, 6), (8, 10)]
    """
    if not intervals:
        return []

    # Sort by start time
    sorted_intervals = sorted(intervals, key=lambda x: x[0])

    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]

        # BUG: only checks if current.start <= last.end (partial overlap)
        # Missing: containment case where current.end <= last.end
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged
