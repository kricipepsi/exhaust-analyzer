from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals into a sorted, non-overlapping list."""
    if not intervals:
        return []
    ordered = sorted(intervals)
    result: list[tuple[int, int]] = [ordered[0]]
    for start, end in ordered[1:]:
        prev_start, prev_end = result[-1]
        if start <= prev_end:
            result[-1] = (prev_start, max(prev_end, end))   # rewrite, markers gone
        else:
            result.append((start, end))
    return result
