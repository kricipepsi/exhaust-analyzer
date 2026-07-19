# Task: Bug Fix — Interval Merger

**Difficulty:** Medium · **Type:** Real-adjacent (bug fix) · **Primary axes:** first-pass pytest failures, iterations-to-green, rubric (error-handling/test-meaningfulness)

## Prompt

The provided `interval_merger.py` has a bug. The module implements `merge_intervals`:

```python
def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals. Returns sorted, non-overlapping list."""
    ...
```

Given `[(1, 3), (2, 6), (8, 10), (15, 18)]`, the expected output is
`[(1, 6), (8, 10), (15, 18)]` — intervals (1,3) and (2,6) overlap and merge
into (1,6).

The bug: the function works for the example above but **fails when an interval
is completely contained within another** — e.g., `[(1, 10), (2, 5)]` should
return `[(1, 10)]` but the current code returns `[(1, 10), (2, 5)]`.

The provided `test_interval_merger.py` has a failing test that exposes this case.

## Steps

1. Read `interval_merger.py` and `test_interval_merger.py`.
2. Run `pytest test_interval_merger.py -v` to confirm the failure.
3. Fix the bug with minimal code change.
4. Run tests again to confirm all pass.
5. Do NOT rewrite the module from scratch — the fix should be surgical.

## Requirements

- All existing tests pass
- The containment-edge-case test passes
- No behavior change for already-working cases
- The fix is minimal (not a rewrite)

## Output

Write the fixed `interval_merger.py` in the working directory. Do NOT modify
`test_interval_merger.py` — the tests are the oracle.
