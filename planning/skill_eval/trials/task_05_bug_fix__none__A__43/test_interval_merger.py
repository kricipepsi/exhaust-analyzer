"""Tests for interval_merger — coder receives this file.

Contains a failing test that exposes the containment bug.
"""

from __future__ import annotations

import pytest

# Coder writes fixed version as interval_merger.py
from interval_merger import merge_intervals


def test_empty() -> None:
    assert merge_intervals([]) == []


def test_single() -> None:
    assert merge_intervals([(5, 10)]) == [(5, 10)]


def test_no_overlap() -> None:
    assert merge_intervals([(1, 2), (3, 4), (5, 6)]) == [(1, 2), (3, 4), (5, 6)]


def test_basic_overlap() -> None:
    assert merge_intervals([(1, 3), (2, 6), (8, 10), (15, 18)]) == [
        (1, 6),
        (8, 10),
        (15, 18),
    ]


def test_unsorted_input() -> None:
    assert merge_intervals([(8, 10), (1, 3), (2, 6)]) == [(1, 6), (8, 10)]


def test_containment() -> None:
    """This test FAILS with the buggy code — containment case."""
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]


def test_containment_multiple() -> None:
    """Multiple contained intervals."""
    assert merge_intervals([(1, 10), (2, 5), (3, 7), (11, 12)]) == [
        (1, 10),
        (11, 12),
    ]


def test_touching_boundaries() -> None:
    """Adjacent intervals (touching at boundary) should merge."""
    assert merge_intervals([(1, 3), (3, 5)]) == [(1, 5)]
