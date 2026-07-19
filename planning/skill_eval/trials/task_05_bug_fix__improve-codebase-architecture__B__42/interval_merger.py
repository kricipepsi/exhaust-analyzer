from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping and contained intervals.  Returns sorted non-overlapping list."""
    if not intervals:
        return []
    ordered = sorted(intervals, key=lambda iv: iv[0])
    result = [ordered[0]]
    for iv in ordered[1:]:
        prev = result[-1]
        if iv[0] <= prev[1]:
            result[-1] = (prev[0], max(prev[1], iv[1]))
        else:
            result.append(iv)
    return result
