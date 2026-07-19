from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals.  Contained intervals are absorbed."""
    if not intervals:
        return []

    ordered = _sort_by_start(intervals)
    merged = [ordered[0]]

    for current in ordered[1:]:
        _absorb_or_append(merged, current)

    return merged


def _sort_by_start(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    return sorted(intervals, key=lambda iv: iv[0])


def _absorb_or_append(merged: list[tuple[int, int]], current: tuple[int, int]) -> None:
    last = merged[-1]
    if current[0] <= last[1]:
        merged[-1] = (last[0], max(last[1], current[1]))
    else:
        merged.append(current)
