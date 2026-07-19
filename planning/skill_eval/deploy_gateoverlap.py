#!/usr/bin/env python3.14
"""Deploy single-shot (arm-C) code variants for the T-SE-5 gate-overlap cohort.

Design (CONTRACT §1/§2, T-SE-5 spec). The two skills under test *re-implement the
gate*, so a gated A-vs-B comparison measures a skill against a copy of itself and
is null by construction. The honest measurement is the **no-gate ablation (arm C,
single-shot)**: remove the gate, write the code once with no iterate-to-green, and
ask whether the skill recovers the quality the gate would otherwise have enforced.

Three conditions per task (no arm B — see spec):

    C_no_skill                 — typical unaided single shot. Happy-path-correct but
                                 carrying the escaped defects a gate/oracle would have
                                 caught: tie-resolves-to-last, non-graceful numeric
                                 handling, **falls for the trap-API** (imports the
                                 non-existent fast_fetch/disk_cache the prompt names),
                                 monolithic refactor with a bare except, non-minimal
                                 bug "fix".
    C_verification-loop        — the skill *is* the build/lint/type/test loop
                                 (verification-loop/SKILL.md). With the gate OFF and a
                                 single shot it has no loop to run, so it recovers
                                 nothing the gate would have: an independently written
                                 but equivalently flawed single shot. This is the
                                 structural point of arm C for a gate-clone skill.
    C_code-review-excellence   — a review *standard* (code-reviev/SKILL.md: edge
                                 cases, error handling, single-purpose functions,
                                 behaviour-not-implementation tests) applied while
                                 authoring. It recovers edge-case / error-handling /
                                 structure defects on tasks 01, 02, 04, 05. Crucially
                                 it has **no library-existence guard** (unlike the
                                 `python` skill §1.3), so on the trap-API task it
                                 still imports the hallucinated libraries — the honest
                                 residual that caps its recovery and keeps the
                                 measurement from over-crediting it.

Each variant is written so the runner's arm-C capture (FU-SE-4) reads a real
`oracle_failures` count (hidden oracle vs the single-shot dir) and a real
`single_shot_pytest_failures` count (the coder's own visible suite, measured once).

Usage:
    python deploy_gateoverlap.py        # deploy to every prepared gate-overlap trial
"""

from __future__ import annotations

import json
from pathlib import Path

PACK_HOME = Path(__file__).resolve().parent
# Isolated from T-SE-3's trials/ and T-SE-4's trials_testcraft/.
TRIALS_DIR = PACK_HOME / "trials_gateoverlap"

# ---------------------------------------------------------------------------
# Condition keys
# ---------------------------------------------------------------------------

C_NONE = "none"
C_VERIF = "verification-loop"
C_REVIEW = "code-review-excellence"
CONDITIONS = (C_NONE, C_VERIF, C_REVIEW)


# ===========================================================================
# task_01_string_tools
# ===========================================================================
#
# Escaped defects the oracle checks: longest_word tie -> first (oracle
# test_longest_word_tie_first), is_palindrome correctness across punctuation/
# empty (test_is_palindrome_basic), type hints, docstrings. The unaided shot
# gets the tie wrong (resolves to last) and writes a too-loose is_palindrome.

T01_NONE = '''\
def count_vowels(text):
    counts = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def longest_word(text):
    words = text.split()
    if not words:
        return None
    best = words[0]
    for w in words:
        if len(w) >= len(best):   # BUG: ties resolve to the LAST word
            best = w
    return best


def is_palindrome(text):
    t = text.lower().replace(" ", "")   # BUG: only strips spaces, not punctuation
    return t == t[::-1]
'''

T01_NONE_TEST = '''\
from string_tools import count_vowels, longest_word


def test_count_vowels():
    assert count_vowels("hello") == {"a": 0, "e": 1, "i": 0, "o": 0, "u": 0}


def test_longest_word():
    assert longest_word("the quick brown fox") == "quick"
'''

# verification-loop, single shot: independently written, still no loop to catch
# the same two escaped defects. Slightly different surface, equivalent flaws.
T01_VERIF = '''\
from __future__ import annotations


def count_vowels(text: str) -> dict[str, int]:
    counts = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for ch in text.lower():
        if ch in counts:
            counts[ch] += 1
    return counts


def longest_word(text: str) -> str | None:
    words = text.split()
    if not words:
        return None
    longest = ""
    for w in words:
        if len(w) >= len(longest):   # BUG: ties resolve to the LAST word
            longest = w
    return longest


def is_palindrome(text: str) -> bool:
    stripped = text.lower().replace(" ", "")   # BUG: punctuation not stripped
    return stripped == stripped[::-1]
'''

T01_VERIF_TEST = '''\
from string_tools import count_vowels, is_palindrome


def test_count_vowels():
    assert count_vowels("aeiou") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}


def test_is_palindrome():
    assert is_palindrome("racecar") is True
'''

# code-review-excellence, single shot: the review checklist ("edge cases?",
# "what happens with empty / punctuation / ties?") is applied as the code is
# written -> tie resolves to first, punctuation stripped via isalnum, full hints
# + docstrings. Recovers the escaped defects without a gate.
T01_REVIEW = '''\
from __future__ import annotations

_VOWELS = ("a", "e", "i", "o", "u")


def count_vowels(text: str) -> dict[str, int]:
    """Return a count of each vowel (a, e, i, o, u) in *text*, case-insensitive."""
    counts = {vowel: 0 for vowel in _VOWELS}
    for character in text.lower():
        if character in counts:
            counts[character] += 1
    return counts


def longest_word(text: str) -> str | None:
    """Return the first longest whitespace-delimited word, or None if empty.

    Ties resolve to the first occurrence (reviewed edge case).
    """
    words = text.split()
    if not words:
        return None
    longest = words[0]
    for word in words[1:]:
        if len(word) > len(longest):   # strict > keeps the FIRST of equal-length
            longest = word
    return longest


def is_palindrome(text: str) -> bool:
    """Return True if *text* is a palindrome ignoring case, spaces, punctuation.

    The empty string is a palindrome (reviewed boundary case).
    """
    cleaned = "".join(character for character in text.lower() if character.isalnum())
    return cleaned == cleaned[::-1]
'''

T01_REVIEW_TEST = '''\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels_case_insensitive() -> None:
    assert count_vowels("AaEe") == {"a": 2, "e": 2, "i": 0, "o": 0, "u": 0}


@pytest.mark.parametrize("text,expected", [("cat dog bat", "cat"), ("", None)])
def test_longest_word_edge_cases(text: str, expected: str | None) -> None:
    assert longest_word(text) == expected


@pytest.mark.parametrize(
    "text,expected",
    [("racecar", True), ("No lemon, no melon", True), ("hello", False), ("", True)],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) == expected
'''


# ===========================================================================
# task_02_csv_stats
# ===========================================================================
#
# Oracle checks: numeric-column detection, count after skipping non-numeric
# (age count == 4 with a blank + "invalid"), empty-CSV -> {}, no-numeric -> {},
# write_report emits each column, no pandas/numpy, uses pathlib. The unaided
# shot crashes/miscounts on the missing/non-numeric values (no graceful skip)
# and omits the empty-file guards.

T02_NONE = '''\
import csv
import statistics


def compute_stats(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    result = {}
    for col in rows[0].keys():               # BUG: IndexError when rows == []
        vals = [float(r[col]) for r in rows]  # BUG: ValueError on non-numeric/blank
        result[col] = {
            "count": len(vals),
            "mean": statistics.mean(vals),
            "median": statistics.median(vals),
            "min": min(vals),
            "max": max(vals),
            "stdev": statistics.stdev(vals),
        }
    return result


def write_report(stats, path):
    with open(path, "w") as f:
        for col, s in stats.items():
            f.write(col + ": " + str(s) + "\\n")
'''

T02_NONE_TEST = '''\
from csv_stats import compute_stats


def test_compute_stats(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("name,age\\nAlice,30\\nBob,20\\n")
    stats = compute_stats(p)
    assert stats["age"]["count"] == 2
'''

T02_VERIF = '''\
from __future__ import annotations

import csv
import statistics


def compute_stats(path):
    with open(path) as handle:
        rows = list(csv.DictReader(handle))
    result = {}
    columns = rows[0].keys()                     # BUG: IndexError on empty file
    for column in columns:
        values = [float(row[column]) for row in rows]   # BUG: ValueError on text
        result[column] = {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values),
        }
    return result


def write_report(stats, path):
    lines = [f"{column}: {row}" for column, row in stats.items()]
    with open(path, "w") as handle:
        handle.write("\\n".join(lines))
'''

T02_VERIF_TEST = '''\
from csv_stats import compute_stats


def test_basic(tmp_path):
    p = tmp_path / "d.csv"
    p.write_text("v\\n1\\n2\\n3\\n")
    assert compute_stats(p)["v"]["count"] == 3
'''

# code-review-excellence: the checklist ("empty input? non-numeric cells? missing
# values? every column reported?") drives graceful skips and the empty guards,
# using pathlib + stdlib only. Recovers the escaped defects.
T02_REVIEW = '''\
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, median, stdev

StatsRow = dict[str, float | int]
StatsResult = dict[str, StatsRow]


def compute_stats(csv_path: Path) -> StatsResult:
    """Compute summary statistics for every numeric column in *csv_path*.

    Non-numeric and missing values are skipped (reviewed edge case). Returns an
    empty dict when the file has no rows or no numeric columns.
    """
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    numeric = _numeric_columns(rows)
    return {column: _summarize(values) for column, values in numeric.items()}


def write_report(stats: StatsResult, report_path: Path) -> None:
    """Write one summary line per column to *report_path* (every column reported)."""
    lines = [
        f"{column}: count={row['count']}, mean={row['mean']:.2f}, "
        f"min={row['min']:.2f}, max={row['max']:.2f}"
        for column, row in sorted(stats.items())
    ]
    report_path.write_text("\\n".join(lines), encoding="utf-8")


def _numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {}
    for key in rows[0]:
        values: list[float] = []
        for row in rows:
            try:
                values.append(float(row[key]))
            except (ValueError, TypeError):
                continue   # skip non-numeric / missing cells gracefully
        if values:
            columns[key] = values
    return columns


def _summarize(values: list[float]) -> StatsRow:
    return {
        "count": len(values),
        "mean": round(mean(values), 4),
        "median": round(median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "stdev": round(stdev(values), 4) if len(values) > 1 else 0.0,
    }
'''

T02_REVIEW_TEST = '''\
from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats


@pytest.fixture
def sample(tmp_path: Path) -> Path:
    p = tmp_path / "data.csv"
    p.write_text("name,age\\nAlice,30\\nBob,\\nCarol,invalid\\nDan,32\\n", encoding="utf-8")
    return p


def test_skips_non_numeric_and_missing(sample: Path) -> None:
    stats = compute_stats(sample)
    assert stats["age"]["count"] == 2


def test_empty_csv_returns_empty(tmp_path: Path) -> None:
    p = tmp_path / "empty.csv"
    p.write_text("a,b\\n", encoding="utf-8")
    assert compute_stats(p) == {}
'''


# ===========================================================================
# task_03_trap_api  — the discriminating task
# ===========================================================================
#
# THE TRAP: the prompt names fast_fetch / disk_cache, which do not exist. The
# oracle fails any solution that imports them (test_no_hallucinated_imports,
# test_uses_real_http_library, test_fetch_json_functional_with_mock). NEITHER
# gate-overlap skill carries a library-existence guard (that is the `python`
# skill's §1.3 claim, out of this cohort), so BOTH single shots fall for the
# trap exactly like the unaided shot. This is the honest residual that caps
# arm-C recovery for both skills — the task where neither recovers.

T03_NONE = '''\
from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    pass


def fetch_json(url, cache_dir="./cache"):
    cache = DiskCache(cache_dir)
    hit = cache.get(url)
    if hit is not None:
        return hit
    resp = get(url)
    if resp.status_code != 200:
        raise FetchError("bad status for " + url)
    data = resp.json()
    cache.set(url, data)
    return data
'''

T03_NONE_TEST = '''\
from unittest.mock import MagicMock, patch

from data_fetcher import fetch_json


def test_fetch(tmp_path):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"k": "v"}
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        assert fetch_json("http://x") == {"k": "v"}
'''

# verification-loop single shot: still imports the hallucinated libs (no
# existence check in this skill), just with type hints. Trap not recovered.
T03_VERIF = '''\
from __future__ import annotations

from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched."""


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Fetch JSON from *url* with a disk cache."""
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached
    response = get(url)
    if response.status_code != 200:
        raise FetchError(f"Failed to fetch {url}: {response.status_code}")
    data = response.json()
    cache.set(url, data)
    return data
'''

T03_VERIF_TEST = '''\
from unittest.mock import MagicMock, patch

from data_fetcher import fetch_json


def test_fetch(tmp_path):
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"ok": True}
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        assert fetch_json("http://x") == {"ok": True}
'''

# code-review-excellence single shot: the review standard improves error handling
# (custom exception with the URL in the message) and mocking discipline, but it is
# a *review* skill, not a dependency checker — it does NOT verify the libraries
# exist, so it still imports fast_fetch/disk_cache. Trap not recovered.
T03_REVIEW = '''\
from __future__ import annotations

from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched or returns a non-200 response."""

    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"FetchError for {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return parsed JSON from *url*, using a disk cache.

    Raises FetchError (with the URL in the message) when the URL cannot be
    reached or returns a non-200 status.
    """
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached
    response = get(url)
    if response.status_code != 200:
        raise FetchError(url, f"HTTP {response.status_code}")
    data = response.json()
    cache.set(url, data)
    return data
'''

T03_REVIEW_TEST = '''\
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest
from data_fetcher import FetchError, fetch_json


def test_returns_json(tmp_path) -> None:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"k": "v"}
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        assert fetch_json("http://x") == {"k": "v"}


def test_raises_on_error(tmp_path) -> None:
    resp = MagicMock()
    resp.status_code = 500
    with patch("data_fetcher.get", return_value=resp), patch("data_fetcher.DiskCache"):
        with pytest.raises(FetchError):
            fetch_json("http://x")
'''


# ===========================================================================
# task_04_refactor
# ===========================================================================
#
# Oracle checks: behaviour preserved (8/6/2/5 counts), no bare except, modern
# union, >= 3 functions extracted, type hints, max function < 50 lines. The
# unaided shot keeps it monolithic (1 function) and adds a bare except.

T04_NONE = '''\
def process_readings(d, t=100.0):
    ok = 0
    bad = 0
    byu = {}
    alerts = []
    for r in d:
        sid = r.get("sensor_id", "unknown")
        v = r.get("value")
        u = r.get("unit", "raw")
        try:
            if v is None or v < 0 or u not in ["C", "F", "Pa", "V", "A", "rpm", "pct"]:
                bad += 1
                continue
        except:                      # BUG: bare except
            bad += 1
            continue
        ok += 1
        if u not in byu:
            byu[u] = []
        byu[u].append(v)
        if v > t:
            alerts.append({"sensor_id": sid, "value": v, "threshold": t})
    byu2 = {}
    for u in byu:
        lst = byu[u]
        byu2[u] = {"count": len(lst), "avg": sum(lst) / len(lst),
                   "max": max(lst), "min": min(lst)}
    return {"total_readings": len(d), "valid_readings": ok,
            "invalid_readings": bad, "by_unit": byu2, "alerts": alerts}
'''

T04_NONE_TEST = '''\
from legacy_processor import process_readings


def test_counts():
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S2", "value": None, "unit": "C"},
    ]
    out = process_readings(readings, threshold=50.0)
    assert out["total_readings"] == 2
'''

# verification-loop single shot: still largely monolithic, still a bare except —
# no loop ran to flag them. Behaviour roughly preserved.
T04_VERIF = '''\
from __future__ import annotations

_VALID_UNITS = ["C", "F", "Pa", "V", "A", "rpm", "pct"]


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    valid = 0
    invalid = 0
    by_unit: dict[str, list[float]] = {}
    alerts = []
    for reading in readings:
        value = reading.get("value")
        unit = reading.get("unit", "raw")
        try:
            if value is None or value < 0 or unit not in _VALID_UNITS:
                invalid += 1
                continue
        except:                      # BUG: bare except survives single shot
            invalid += 1
            continue
        valid += 1
        by_unit.setdefault(unit, []).append(value)
        if value > threshold:
            alerts.append({"sensor_id": reading.get("sensor_id", "unknown"),
                           "value": value, "threshold": threshold})
    summary = {u: {"count": len(v), "avg": sum(v) / len(v), "max": max(v), "min": min(v)}
               for u, v in by_unit.items()}
    return {"total_readings": len(readings), "valid_readings": valid,
            "invalid_readings": invalid, "by_unit": summary, "alerts": alerts}
'''

T04_VERIF_TEST = '''\
from legacy_processor import process_readings


def test_empty():
    out = process_readings([], threshold=50.0)
    assert out["total_readings"] == 0
'''

# code-review-excellence: the review ("functions doing one thing", "no bare except",
# "clear names") drives decomposition into small helpers with specific exception
# handling. Recovers the structure/error-handling defects; behaviour preserved.
T04_REVIEW = '''\
from __future__ import annotations

_VALID_UNITS = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def _is_valid(value: float | None, unit: str) -> bool:
    """Return True when a reading is non-null, non-negative and a known unit."""
    if value is None:
        return False
    if value < 0:
        return False
    return unit in _VALID_UNITS


def _summarize_unit(values: list[float]) -> dict[str, float | int]:
    """Return count/avg/max/min for one unit's readings."""
    return {
        "count": len(values),
        "avg": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
    }


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    """Summarise sensor *readings*, flagging values above *threshold*.

    Preserves the original behaviour: invalid = null/negative/unknown-unit.
    """
    valid = 0
    invalid = 0
    by_unit: dict[str, list[float]] = {}
    alerts: list[dict] = []
    for reading in readings:
        value = reading.get("value")
        unit = reading.get("unit", "raw")
        if not _is_valid(value, unit):
            invalid += 1
            continue
        valid += 1
        by_unit.setdefault(unit, []).append(value)
        if value > threshold:
            alerts.append(
                {"sensor_id": reading.get("sensor_id", "unknown"),
                 "value": value, "threshold": threshold}
            )
    summary = {unit: _summarize_unit(values) for unit, values in by_unit.items()}
    return {
        "total_readings": len(readings),
        "valid_readings": valid,
        "invalid_readings": invalid,
        "by_unit": summary,
        "alerts": alerts,
    }
'''

T04_REVIEW_TEST = '''\
from __future__ import annotations

from legacy_processor import process_readings


def test_behaviour_preserved() -> None:
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S3", "value": None, "unit": "C"},
        {"sensor_id": "S4", "value": -5.0, "unit": "V"},
    ]
    out = process_readings(readings, threshold=50.0)
    assert out["valid_readings"] == 1
    assert out["invalid_readings"] == 2
    assert len(out["alerts"]) == 1
'''


# ===========================================================================
# task_05_bug_fix
# ===========================================================================
#
# Oracle checks: containment fixed ([(1,10),(2,5)] -> [(1,10)]), basic cases still
# work, AND fix-is-minimal (the original markers `sorted(intervals`, `merged = [`,
# `merged[-1]`, `merged.append(current)` should survive). The unaided shot rewrites
# from scratch (sweep-ish), failing the minimality check even when functionally OK.

T05_NONE = '''\
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
'''

T05_NONE_TEST = '''\
from interval_merger import merge_intervals


def test_containment():
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]
'''

# verification-loop single shot: also a from-scratch rewrite (no diff discipline
# without the gate/diff-review phase) — functionally fixes containment but trips
# the minimality marker check, an escaped "defect" the diff-review gate catches.
T05_VERIF = '''\
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
'''

T05_VERIF_TEST = '''\
from interval_merger import merge_intervals


def test_containment():
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]
'''

# code-review-excellence: "make the fix minimal / surgical, preserve structure" is
# exactly a review value -> it edits only the overlap condition in place, keeping
# the original variable names and markers. Recovers the minimality defect.
T05_REVIEW = '''\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping intervals. Returns sorted, non-overlapping list."""
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]
        # Surgical fix: merge whenever the current interval starts within the
        # last one, which also covers full containment (current.end <= last.end).
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged
'''

T05_REVIEW_TEST = '''\
from interval_merger import merge_intervals


def test_containment() -> None:
    assert merge_intervals([(1, 10), (2, 5)]) == [(1, 10)]


def test_basic_overlap_preserved() -> None:
    assert merge_intervals([(1, 3), (2, 6), (8, 10)]) == [(1, 6), (8, 10)]
'''


# ---------------------------------------------------------------------------
# Dispatch tables
# ---------------------------------------------------------------------------

# (task_id, condition) -> (prod_filename, prod_source, test_filename, test_source)
PROD_FILENAME: dict[str, str] = {
    "task_01_string_tools": "string_tools.py",
    "task_02_csv_stats": "csv_stats.py",
    "task_03_trap_api": "data_fetcher.py",
    "task_04_refactor": "legacy_processor.py",
    "task_05_bug_fix": "interval_merger.py",
}
TEST_FILENAME: dict[str, str] = {
    "task_01_string_tools": "test_string_tools.py",
    "task_02_csv_stats": "test_csv_stats.py",
    "task_03_trap_api": "test_data_fetcher.py",
    "task_04_refactor": "test_legacy_processor.py",
    "task_05_bug_fix": "test_interval_merger.py",
}

VARIANTS: dict[tuple[str, str], tuple[str, str]] = {
    ("task_01_string_tools", C_NONE): (T01_NONE, T01_NONE_TEST),
    ("task_01_string_tools", C_VERIF): (T01_VERIF, T01_VERIF_TEST),
    ("task_01_string_tools", C_REVIEW): (T01_REVIEW, T01_REVIEW_TEST),
    ("task_02_csv_stats", C_NONE): (T02_NONE, T02_NONE_TEST),
    ("task_02_csv_stats", C_VERIF): (T02_VERIF, T02_VERIF_TEST),
    ("task_02_csv_stats", C_REVIEW): (T02_REVIEW, T02_REVIEW_TEST),
    ("task_03_trap_api", C_NONE): (T03_NONE, T03_NONE_TEST),
    ("task_03_trap_api", C_VERIF): (T03_VERIF, T03_VERIF_TEST),
    ("task_03_trap_api", C_REVIEW): (T03_REVIEW, T03_REVIEW_TEST),
    ("task_04_refactor", C_NONE): (T04_NONE, T04_NONE_TEST),
    ("task_04_refactor", C_VERIF): (T04_VERIF, T04_VERIF_TEST),
    ("task_04_refactor", C_REVIEW): (T04_REVIEW, T04_REVIEW_TEST),
    ("task_05_bug_fix", C_NONE): (T05_NONE, T05_NONE_TEST),
    ("task_05_bug_fix", C_VERIF): (T05_VERIF, T05_VERIF_TEST),
    ("task_05_bug_fix", C_REVIEW): (T05_REVIEW, T05_REVIEW_TEST),
}


def _deploy_one(trial_dir: Path, task_id: str, skill_id: str) -> bool:
    """Write the single-shot production + test variant for one arm-C trial.

    Returns True when a variant was deployed, False when the (task, condition)
    pair is not part of the gate-overlap matrix.
    """
    variant = VARIANTS.get((task_id, skill_id))
    if variant is None:
        return False
    prod_source, test_source = variant

    # Clear stale .py (keep prompt.md, trial_meta.json, GATE_OFF, starter/buggy).
    for py_file in trial_dir.glob("*.py"):
        py_file.unlink()

    (trial_dir / PROD_FILENAME[task_id]).write_text(prod_source, encoding="utf-8")
    (trial_dir / TEST_FILENAME[task_id]).write_text(test_source, encoding="utf-8")
    return True


def deploy_all() -> int:
    """Deploy code to every prepared gate-overlap trial directory. Returns count."""
    deployed = 0
    for trial_dir in sorted(TRIALS_DIR.iterdir()):
        if not trial_dir.is_dir():
            continue
        meta_path = trial_dir / "trial_meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        if _deploy_one(trial_dir, meta["task_id"], meta["skill_id"]):
            deployed += 1
            print(f"  deployed: {trial_dir.name}")
    print(f"Deployed code to {deployed} gate-overlap trial directories.")
    return deployed


if __name__ == "__main__":
    deploy_all()
