from __future__ import annotations


def merge_intervals(intervals):
    if not intervals:
        return []
    pts = sorted(intervals)
    out = []
    cur_start, cur_end = pts[0]
    for s, e in pts[1:]:                      # full rewrite: not a surgical fix
        if s <= cur_end:
            cur_end = max(cur_end, e)
        else:
            out.append((cur_start, cur_end))
            cur_start, cur_end = s, e
    out.append((cur_start, cur_end))
    return out
