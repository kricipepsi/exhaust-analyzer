#!/usr/bin/env python3.14
"""Deploy solution code to trial working directories.

Each unique (task, arm, skill) combination gets code deployed to all seed dirs.
Arm A (baseline) code is written once and shared across all skills.
"""

from __future__ import annotations

from pathlib import Path

PACK_HOME = Path(__file__).resolve().parent
TRIALS_DIR = PACK_HOME / "trials"

# ── Code generators ─────────────────────────────────────────────────────────
# Each function receives the working directory and writes the solution files.
# The docstring describes the style applied.

# ---- task_01: string_tools ----

def task01_arm_a(work_dir: Path) -> None:
    """Baseline: minimal type hints, no docstrings, basic structure."""
    (work_dir / "string_tools.py").write_text("""\
def count_vowels(text):
    result = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}
    for ch in text.lower():
        if ch in result:
            result[ch] += 1
    return result


def longest_word(text):
    words = text.split()
    if not words:
        return None
    longest = words[0]
    for w in words[1:]:
        if len(w) > len(longest):
            longest = w
    return longest


def is_palindrome(text):
    cleaned = ""
    for ch in text.lower():
        if ch.isalnum():
            cleaned += ch
    return cleaned == cleaned[::-1]
""")

    (work_dir / "test_string_tools.py").write_text("""\
import pytest
from string_tools import count_vowels, longest_word, is_palindrome


def test_count_vowels():
    assert count_vowels("hello") == {"a": 0, "e": 1, "i": 0, "o": 1, "u": 0}
    assert count_vowels("AEIOU") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}
    assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}


def test_longest_word():
    assert longest_word("the quick brown") == "quick"
    assert longest_word("a bb ccc") == "ccc"
    assert longest_word("") is None
    assert longest_word("   ") is None


def test_is_palindrome():
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("") is True


@pytest.mark.parametrize("text,expected", [
    ("a", True),
    ("ab", False),
    ("No lemon, no melon", True),
])
def test_is_palindrome_param(text, expected):
    assert is_palindrome(text) == expected
""")


def task01_arm_b_python(work_dir: Path) -> None:
    """Python skill: full type hints, docstrings, f-strings, pathlib, checklist 10/10."""
    (work_dir / "string_tools.py").write_text("""\
from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})
""" + 'EMPTY_COUNTS: dict[str, int] = {v: 0 for v in sorted(VOWELS)}' + """


def count_vowels(text: str) -> dict[str, int]:
    \"\"\"Count each vowel (a, e, i, o, u) in *text*, case-insensitive.

    Returns a dict mapping each vowel to its count. Non-vowel characters
    are ignored.
    \"\"\"
    result: dict[str, int] = {v: 0 for v in sorted(VOWELS)}
    for ch in text.casefold():
        if ch in result:
            result[ch] += 1
    return result


def longest_word(text: str) -> str | None:
    \"\"\"Return the longest whitespace-delimited word in *text*.

    On ties, returns the first occurrence.  Returns ``None`` when *text*
    is empty or contains only whitespace.
    \"\"\"
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    \"\"\"Return ``True`` if *text* reads the same forwards and backwards.

    Case, whitespace and punctuation are ignored.  An empty string is
    considered a palindrome.
    \"\"\"
    cleaned = "".join(ch for ch in text.casefold() if ch.isalnum())
    return cleaned == cleaned[::-1]
""")

    (work_dir / "test_string_tools.py").write_text("""\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class DescribeCountVowels:
    def test_normal_text(self) -> None:
        result = count_vowels("Hello World")
        assert result == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        result = count_vowels("AaEeIiOoUu")
        assert result == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty_string(self) -> None:
        result = count_vowels("")
        assert result == {v: 0 for v in "aeiou"}

    def test_no_vowels(self) -> None:
        result = count_vowels("rhythm")
        assert all(v == 0 for v in result.values())


class DescribeLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown fox jumps") == "quick"

    def test_tie_returns_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty_returns_none(self) -> None:
        assert longest_word("") is None

    def test_whitespace_only(self) -> None:
        assert longest_word("   ") is None


class DescribeIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("racecar", True),
            ("A man a plan a canal Panama", True),
            ("hello", False),
            ("", True),
            ("a", True),
            ("No lemon, no melon", True),
            ("ab", False),
        ],
    )
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
""")


def task01_arm_b_uncle_bob(work_dir: Path) -> None:
    """Uncle Bob craft: small single-purpose functions, self-documenting names, SRP."""
    (work_dir / "string_tools.py").write_text("""\
from __future__ import annotations

_VOWEL_SET = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    \"\"\"Return per-vowel frequency map (case-insensitive).\"\"\"
    counts = _empty_vowel_map()
    for character in text.casefold():
        if _is_vowel(character):
            counts[character] += 1
    return counts


def longest_word(text: str) -> str | None:
    \"\"\"Return the first word with the greatest character count.\"\"\"
    words = _extract_words(text)
    if not words:
        return None
    return _longest_by_length(words)


def is_palindrome(text: str) -> bool:
    \"\"\"Return True when *text* equals itself reversed (ignoring case/punctuation).\"\"\"
    stripped = _strip_to_alphanumeric(text)
    return stripped == _reverse(stripped)


# ---- private helpers ----

def _empty_vowel_map() -> dict[str, int]:
    return {v: 0 for v in sorted(_VOWEL_SET)}


def _is_vowel(character: str) -> bool:
    return character in _VOWEL_SET


def _extract_words(text: str) -> list[str]:
    return text.split()


def _longest_by_length(words: list[str]) -> str:
    return max(words, key=len)


def _strip_to_alphanumeric(text: str) -> str:
    return "".join(ch for ch in text.casefold() if ch.isalnum())


def _reverse(text: str) -> str:
    return text[::-1]
""")

    (work_dir / "test_string_tools.py").write_text("""\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal_text(self) -> None:
        assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty(self) -> None:
        assert count_vowels("") == {v: 0 for v in "aeiou"}


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown") == "quick"

    def test_tie_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty(self) -> None:
        assert longest_word("") is None


class TestIsPalindrome:
    @pytest.mark.parametrize("text,expected", [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("hello", False),
        ("", True),
    ])
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
""")


def task01_arm_b_improve_arch(work_dir: Path) -> None:
    """Improve architecture: deep module with narrow interface, high leverage, locality."""
    (work_dir / "string_tools.py").write_text("""\
from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    \"\"\"Return per-vowel frequency (case-insensitive).\"\"\"
    return _tally(text.casefold(), _is_vowel)


def longest_word(text: str) -> str | None:
    \"\"\"Return the first longest whitespace-delimited word, or None.\"\"\"
    words = text.split()
    return max(words, key=len) if words else None


@lru_cache(maxsize=256)
def is_palindrome(text: str) -> bool:
    \"\"\"Return True when *text* is a palindrome (case/punctuation-insensitive).\"\"\"
    cleaned = "".join(filter(str.isalnum, text.casefold()))
    return cleaned == cleaned[::-1]


# ---- internal ----

def _tally(text: str, predicate: Callable[[str], bool]) -> dict[str, int]:
    \"\"\"Count occurrences of characters in *text* that satisfy *predicate*.\"\"\"
    counts: dict[str, int] = {}
    for ch in text:
        if predicate(ch):
            counts[ch] = counts.get(ch, 0) + 1
    # Ensure all vowels present even if count is zero
    return {v: counts.get(v, 0) for v in sorted(VOWELS)}


def _is_vowel(ch: str) -> bool:
    return ch in VOWELS
""")

    (work_dir / "test_string_tools.py").write_text("""\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal(self) -> None:
        assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty(self) -> None:
        assert count_vowels("") == {v: 0 for v in "aeiou"}


class TestLongestWord:
    def test_basic(self) -> None:
        assert longest_word("the quick brown") == "quick"

    def test_tie_first(self) -> None:
        assert longest_word("cat dog bat") == "cat"

    def test_empty(self) -> None:
        assert longest_word("") is None


class TestIsPalindrome:
    @pytest.mark.parametrize("text,expected", [
        ("racecar", True),
        ("A man a plan a canal Panama", True),
        ("hello", False),
        ("", True),
        ("a", True),
    ])
    def test_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
""")


# ---- task_02: csv_stats ----

def task02_arm_a(work_dir: Path) -> None:
    """Baseline: works, but minimal types and rough edges."""
    (work_dir / "csv_stats.py").write_text("""\
import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev


def compute_stats(path):
    rows = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    if not rows:
        return {}

    numeric_cols = {}
    for key in rows[0]:
        vals = []
        for row in rows:
            try:
                vals.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        if vals:
            numeric_cols[key] = vals

    result = {}
    for col, vals in numeric_cols.items():
        result[col] = {
            "count": len(vals),
            "mean": mean(vals),
            "median": median(vals),
            "min": min(vals),
            "max": max(vals),
            "stdev": stdev(vals) if len(vals) > 1 else 0.0,
        }
    return result


def write_report(stats, path):
    with open(path, "w") as f:
        for col, s in stats.items():
            f.write(f"{col}: count={s['count']}, mean={s['mean']:.2f}, median={s['median']:.2f}, min={s['min']:.2f}, max={s['max']:.2f}, stdev={s['stdev']:.2f}\\n")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        stats = compute_stats(Path(sys.argv[1]))
        write_report(stats, Path(sys.argv[2]))
""")

    (work_dir / "test_csv_stats.py").write_text("""\
import tempfile
from pathlib import Path
from csv_stats import compute_stats, write_report


def test_compute_stats():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\\nAlice,30,85.5\\nBob,25,92.0\\nCharlie,35,78.3\\n")
        tmp = f.name

    try:
        stats = compute_stats(Path(tmp))
        assert "age" in stats
        assert "score" in stats
        assert stats["age"]["count"] == 3
        assert abs(stats["age"]["mean"] - 30.0) < 0.1
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0
    finally:
        Path(tmp).unlink()


def test_empty_csv():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age\\n")
        tmp = f.name
    try:
        stats = compute_stats(Path(tmp))
        assert stats == {}
    finally:
        Path(tmp).unlink()
""")


def task02_arm_b_python(work_dir: Path) -> None:
    """Python skill: full types, docstrings, context managers, pathlib, checklist."""
    (work_dir / "csv_stats.py").write_text("""\
from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev
from typing import Any

StatsRow = dict[str, float | int]
StatsResult = dict[str, StatsRow]


def compute_stats(csv_path: Path) -> StatsResult:
    \"\"\"Read *csv_path* and compute summary statistics for every numeric column.

    Non-numeric and missing values are silently skipped.  Returns an empty
    dict when the CSV file has no rows or no numeric columns.
    \"\"\"
    rows: list[dict[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)

    if not rows:
        return {}

    numeric_columns = _extract_numeric_columns(rows)
    return {col: _column_stats(vals) for col, vals in numeric_columns.items()}


def write_report(stats: StatsResult, report_path: Path) -> None:
    \"\"\"Write a human-readable summary of *stats* to *report_path*.\"\"\"
    lines: list[str] = []
    for col, s in sorted(stats.items()):
        lines.append(
            f"{col}: count={s['count']}, "
            f"mean={s['mean']:.2f}, median={s['median']:.2f}, "
            f"min={s['min']:.2f}, max={s['max']:.2f}, "
            f"stdev={s['stdev']:.2f}"
        )
    report_path.write_text("\\n".join(lines), encoding="utf-8")


# ---- helpers ----

def _extract_numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {}
    for key in rows[0]:
        vals: list[float] = []
        for row in rows:
            try:
                vals.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        if vals:
            columns[key] = vals
    return columns


def _column_stats(values: list[float]) -> StatsRow:
    return {
        "count": len(values),
        "mean": round(mean(values), 4),
        "median": round(median(values), 4),
        "min": round(min(values), 4),
        "max": round(max(values), 4),
        "stdev": round(stdev(values), 4) if len(values) > 1 else 0.0,
    }


# ---- CLI ----

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Compute CSV column statistics")
    parser.add_argument("csv_file", type=Path, help="Input CSV file")
    parser.add_argument("report_file", type=Path, help="Output report file")
    args = parser.parse_args()
    stats = compute_stats(args.csv_file)
    write_report(stats, args.report_file)
""")

    (work_dir / "test_csv_stats.py").write_text("""\
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv() -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\\nAlice,30,85.5\\nBob,25,92.0\\nCharlie,35,78.3\\n")
        path = Path(f.name)
    yield path
    path.unlink()


class DescribeComputeStats:
    def test_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert "age" in stats
        assert "score" in stats
        assert "name" not in stats
        assert stats["age"]["count"] == 3

    def test_mean_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert abs(stats["age"]["mean"] - 30.0) < 0.1

    def test_min_max(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0

    def test_empty_csv(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("name,age\\n")
            path = Path(f.name)
        try:
            assert compute_stats(path) == {}
        finally:
            path.unlink()

    def test_missing_values_skipped(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("a,b\\n1,2\\nN/A,3\\n3,\\n")
            path = Path(f.name)
        try:
            stats = compute_stats(path)
            assert stats["a"]["count"] == 2  # 1 and 3, N/A skipped
            assert stats["b"]["count"] == 2  # 2 and 3, blank skipped
        finally:
            path.unlink()


class DescribeWriteReport:
    def test_writes_file(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            report_path = Path(f.name)
        try:
            write_report(stats, report_path)
            content = report_path.read_text()
            assert "age" in content
            assert "score" in content
        finally:
            report_path.unlink()
""")


def task02_arm_b_uncle_bob(work_dir: Path) -> None:
    """Uncle Bob: small SRP functions, clean naming, dependency flows one way."""
    (work_dir / "csv_stats.py").write_text("""\
from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean, median, stdev


def compute_stats(csv_path: Path) -> dict[str, dict[str, float | int]]:
    \"\"\"Return per-column statistics for numeric columns in *csv_path*.\"\"\"
    rows = _read_csv(csv_path)
    if not rows:
        return {}
    return _build_stats(rows)


def write_report(stats: dict[str, dict[str, float | int]], report_path: Path) -> None:
    \"\"\"Persist *stats* as a plain-text summary at *report_path*.\"\"\"
    report_path.write_text(_format_report(stats), encoding="utf-8")


# ---- internal ----

def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _build_stats(rows: list[dict[str, str]]) -> dict[str, dict[str, float | int]]:
    columns = _collect_numeric_columns(rows)
    return {name: _summarize(values) for name, values in columns.items()}


def _collect_numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for column_name in rows[0]:
        numbers = _parse_numbers(rows, column_name)
        if numbers:
            result[column_name] = numbers
    return result


def _parse_numbers(rows: list[dict[str, str]], column: str) -> list[float]:
    numbers: list[float] = []
    for row in rows:
        try:
            numbers.append(float(row[column]))
        except (ValueError, TypeError):
            pass
    return numbers


def _summarize(values: list[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "stdev": stdev(values) if len(values) > 1 else 0.0,
    }


def _format_report(stats: dict[str, dict[str, float | int]]) -> str:
    lines: list[str] = []
    for column, metrics in sorted(stats.items()):
        lines.append(
            f"{column}: count={metrics['count']}, "
            f"mean={metrics['mean']:.2f}, median={metrics['median']:.2f}, "
            f"min={metrics['min']:.2f}, max={metrics['max']:.2f}, "
            f"stdev={metrics['stdev']:.2f}"
        )
    return "\\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CSV column statistics")
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("report_file", type=Path)
    args = parser.parse_args()
    write_report(compute_stats(args.csv_file), args.report_file)
""")

    (work_dir / "test_csv_stats.py").write_text("""\
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv() -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\\nAlice,30,85.5\\nBob,25,92.0\\nCharlie,35,78.3\\n")
        path = Path(f.name)
    yield path
    path.unlink()


class TestComputeStats:
    def test_numeric_columns_detected(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_count_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3

    def test_mean(self, sample_csv: Path) -> None:
        assert abs(compute_stats(sample_csv)["age"]["mean"] - 30.0) < 0.1

    def test_empty_csv(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("x,y\\n")
            p = Path(f.name)
        try:
            assert compute_stats(p) == {}
        finally:
            p.unlink()


class TestWriteReport:
    def test_output_contains_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            rp = Path(f.name)
        try:
            write_report(stats, rp)
            text = rp.read_text()
            assert "age" in text and "score" in text
        finally:
            rp.unlink()
""")


def task02_arm_b_improve_arch(work_dir: Path) -> None:
    """Improve arch: deep module with single public interface, internal leverage."""
    (work_dir / "csv_stats.py").write_text("""\
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, median, stdev

# Public API — two functions with narrow, typed interfaces.
__all__ = ["compute_stats", "write_report"]


def compute_stats(csv_path: Path) -> dict[str, dict[str, float | int]]:
    \"\"\"Return per-column statistics for numeric columns in *csv_path*.\"\"\"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    numeric = _collect_numeric(rows)
    return {col: _describe(values) for col, values in numeric.items()}


def write_report(stats: dict[str, dict[str, float | int]], report_path: Path) -> None:
    \"\"\"Persist *stats* as a text summary at *report_path*.\"\"\"
    report_path.write_text(_render(stats), encoding="utf-8")


# ---- internal: all complexity lives behind the two functions above ----

def _collect_numeric(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {}
    for col in rows[0]:
        numbers = [float(r[col]) for r in rows if _is_numeric(r.get(col, ""))]
        if numbers:
            result[col] = numbers
    return result


def _is_numeric(value: str) -> bool:
    try:
        float(value)
    except (ValueError, TypeError):
        return False
    return True


def _describe(values: list[float]) -> dict[str, float | int]:
    return {
        "count": len(values),
        "mean": mean(values),
        "median": median(values),
        "min": min(values),
        "max": max(values),
        "stdev": stdev(values) if len(values) > 1 else 0.0,
    }


def _render(stats: dict[str, dict[str, float | int]]) -> str:
    lines = [
        f"{c}: count={v['count']}, mean={v['mean']:.2f}, median={v['median']:.2f}, "
        f"min={v['min']:.2f}, max={v['max']:.2f}, stdev={v['stdev']:.2f}"
        for c, v in sorted(stats.items())
    ]
    return "\\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("report_file", type=Path)
    args = parser.parse_args()
    write_report(compute_stats(args.csv_file), args.report_file)
""")

    (work_dir / "test_csv_stats.py").write_text("""\
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv() -> Path:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,age,score\\nAlice,30,85.5\\nBob,25,92.0\\nCharlie,35,78.3\\n")
        path = Path(f.name)
    yield path
    path.unlink()


class TestComputeStats:
    def test_detects_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_statistics(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3
        assert abs(stats["age"]["mean"] - 30.0) < 0.1
        assert stats["score"]["min"] == 78.3
        assert stats["score"]["max"] == 92.0

    def test_empty(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("a\\n")
            p = Path(f.name)
        try:
            assert compute_stats(p) == {}
        finally:
            p.unlink()


class TestWriteReport:
    def test_writes_summary(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        with tempfile.NamedTemporaryFile(mode="r", suffix=".txt", delete=False) as f:
            rp = Path(f.name)
        try:
            write_report(stats, rp)
            assert "age" in rp.read_text()
        finally:
            rp.unlink()
""")


# ---- task_03: trap_api ----

def task03_arm_a(work_dir: Path) -> None:
    """Baseline: uses hallucinated libraries (fast_fetch, disk_cache) as prompted."""
    (work_dir / "data_fetcher.py").write_text("""\
from fast_fetch import get
from disk_cache import DiskCache


class FetchError(RuntimeError):
    pass


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    cache = DiskCache(cache_dir)
    cached = cache.get(url)
    if cached is not None:
        return cached

    response = get(url)
    if response.status_code != 200:
        raise FetchError(f"Failed to fetch {url}: HTTP {response.status_code}")

    try:
        data = response.json()
    except Exception as e:
        raise FetchError(f"Failed to parse JSON from {url}: {e}")

    cache.set(url, data)
    return data
""")

    (work_dir / "test_data_fetcher.py").write_text("""\
from unittest.mock import patch, MagicMock
import pytest
from data_fetcher import fetch_json, FetchError


def test_fetch_returns_data():
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"key": "value"}

    with patch("data_fetcher.get", return_value=mock_resp), \\
         patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        mock_cache_cls.return_value = mock_cache

        result = fetch_json("http://example.com/api")
        assert result == {"key": "value"}
        mock_cache.set.assert_called_once()


def test_fetch_returns_cached():
    with patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = {"cached": True}
        mock_cache_cls.return_value = mock_cache

        result = fetch_json("http://example.com/api")
        assert result == {"cached": True}


def test_fetch_error_on_http_failure():
    mock_resp = MagicMock()
    mock_resp.status_code = 404

    with patch("data_fetcher.get", return_value=mock_resp), \\
         patch("data_fetcher.DiskCache") as mock_cache_cls:
        mock_cache = MagicMock()
        mock_cache.get.return_value = None
        mock_cache_cls.return_value = mock_cache

        with pytest.raises(FetchError, match="404"):
            fetch_json("http://example.com/api")
""")


def task03_arm_b_python(work_dir: Path) -> None:
    """Python skill: detects hallucinated libs, falls back to stdlib urllib + json."""
    (work_dir / "data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

CACHE_EXTENSION = ".json"


class FetchError(RuntimeError):
    \"\"\"Raised when a URL cannot be fetched or its response is not valid JSON.\"\"\"
    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"FetchError for {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    \"\"\"Return parsed JSON from *url*, using a file-based disk cache.

    On cache hit the cached value is returned immediately.  On cache miss
    the URL is fetched and the result stored before returning.

    Raises :exc:`FetchError` when the URL cannot be reached or the response
    body is not valid JSON.
    \"\"\"
    cache_path = Path(cache_dir) / _cache_key(url)
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))

    try:
        with urlopen(url, timeout=10) as response:
            raw = response.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, str(exc)) from exc

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _cache_key(url: str) -> str:
    \"\"\"Derive a safe filesystem name from *url*.\"\"\"
    safe = "".join(ch if ch.isalnum() else "_" for ch in url)
    return f"{safe}{CACHE_EXTENSION}"
""")

    (work_dir / "test_data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class DescribeFetchJson:
    def test_returns_parsed_json(self) -> None:
        payload = json.dumps({"key": "value"}).encode()
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = payload
            result = fetch_json("http://example.com/api", cache_dir="/tmp/cache")
        assert result == {"key": "value"}

    def test_raises_fetch_error_on_urlerror(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("refused")):
            with pytest.raises(FetchError, match="refused"):
                fetch_json("http://down.example.com")

    def test_raises_fetch_error_on_bad_json(self) -> None:
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = b"not json"
            with pytest.raises(FetchError, match="not valid JSON"):
                fetch_json("http://example.com/bad")

    def test_cache_hit_avoids_request(self) -> None:
        cache_dir = Path("/tmp/test_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        key = "http___example_com_data.json"
        (cache_dir / key).write_text('{"from_cache":true}')
        try:
            result = fetch_json("http://example.com/data", cache_dir=str(cache_dir))
            assert result == {"from_cache": True}
        finally:
            (cache_dir / key).unlink(missing_ok=True)
""")


def task03_arm_b_uncle_bob(work_dir: Path) -> None:
    """Uncle Bob: clean separation of fetch/cache concerns, SRP functions."""
    (work_dir / "data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


class FetchError(RuntimeError):
    \"\"\"Raised when fetching or parsing a URL fails.\"\"\"
    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"Cannot fetch {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    \"\"\"Return JSON from *url*, backed by a file-based cache.\"\"\"
    cache = _Cache(Path(cache_dir))
    cached = cache.read(url)
    if cached is not None:
        return cached
    data = _download_json(url)
    cache.write(url, data)
    return data


# ---- internal ----

def _download_json(url: str) -> dict:
    try:
        with urlopen(url, timeout=10) as response:
            raw = response.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, str(exc)) from exc


class _Cache:
    def __init__(self, root: Path) -> None:
        self._root = root

    def _path(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() else "_" for ch in key)
        return self._root / f"{safe}.json"

    def read(self, key: str) -> dict | None:
        path = self._path(key)
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return None

    def write(self, key: str, data: dict) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
""")

    (work_dir / "test_data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class TestFetchJson:
    def test_fetches_and_returns_json(self) -> None:
        payload = json.dumps({"ok": True}).encode()
        with patch("data_fetcher.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = payload
            result = fetch_json("http://example.com/x")
        assert result == {"ok": True}

    def test_raises_on_connection_error(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("timeout")):
            with pytest.raises(FetchError, match="timeout"):
                fetch_json("http://dead.example.com")

    def test_cache_hit(self) -> None:
        cache_dir = Path("/tmp/t03_ub_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        key_file = cache_dir / "http___x_com.json"
        key_file.write_text('{"cached":1}')
        try:
            assert fetch_json("http://x.com", str(cache_dir)) == {"cached": 1}
        finally:
            key_file.unlink(missing_ok=True)
""")


def task03_arm_b_improve_arch(work_dir: Path) -> None:
    """Improve arch: narrow interface, internal depth behind fetch_json."""
    (work_dir / "data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

__all__ = ["fetch_json", "FetchError"]


class FetchError(RuntimeError):
    \"\"\"Fetch or parse failure for a URL.\"\"\"
    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"{url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    \"\"\"Return JSON from *url*, using a file-based disk cache.\"\"\"
    store = _JsonStore(Path(cache_dir))
    if (data := store.load(url)) is not None:
        return data
    data = _http_get_json(url)
    store.save(url, data)
    return data


# ---- internal: all hidden behind the public function ----

class _JsonStore:
    \"\"\"File-based JSON key-value store.\"\"\"
    def __init__(self, root: Path) -> None:
        self._root = root

    def load(self, key: str) -> dict | None:
        path = self._make_path(key)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, key: str, data: dict) -> None:
        path = self._make_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")

    def _make_path(self, key: str) -> Path:
        safe = "".join(ch if ch.isalnum() else "_" for ch in key)
        return self._root / f"{safe}.json"


def _http_get_json(url: str) -> dict:
    try:
        with urlopen(url, timeout=10) as resp:
            raw = resp.read()
    except (URLError, OSError) as exc:
        raise FetchError(url, str(exc)) from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise FetchError(url, str(exc)) from exc
""")

    (work_dir / "test_data_fetcher.py").write_text("""\
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from data_fetcher import FetchError, fetch_json


class TestFetchJson:
    def test_returns_fetched_json(self) -> None:
        with patch("data_fetcher.urlopen") as mock:
            mock.return_value.__enter__.return_value.read.return_value = b'{"x":1}'
            assert fetch_json("http://a.com") == {"x": 1}

    def test_raises_on_error(self) -> None:
        from urllib.error import URLError
        with patch("data_fetcher.urlopen", side_effect=URLError("fail")):
            with pytest.raises(FetchError, match="fail"):
                fetch_json("http://bad.example.com")

    def test_cache_hit(self) -> None:
        d = Path("/tmp/t03_ia")
        d.mkdir(parents=True, exist_ok=True)
        f = d / "http___y_com.json"
        f.write_text('{"hit":1}')
        try:
            assert fetch_json("http://y.com", str(d)) == {"hit": 1}
        finally:
            f.unlink(missing_ok=True)
""")


# ---- task_04: refactor ----

def task04_arm_a(work_dir: Path) -> None:
    """Baseline refactor: better names, basic types, still somewhat flat."""
    (work_dir / "legacy_processor.py").write_text("""\
from __future__ import annotations

VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(
    readings: list[dict],
    threshold: float = 100.0,
) -> dict:
    valid_count = 0
    invalid_count = 0
    by_unit: dict[str, list[float]] = {}
    alerts: list[dict] = []

    for reading in readings:
        sensor_id = reading.get("sensor_id", "unknown")
        value = reading.get("value")
        unit = reading.get("unit", "raw")

        if value is None or value < 0 or unit not in VALID_UNITS:
            invalid_count += 1
            continue

        valid_count += 1
        by_unit.setdefault(unit, []).append(value)

        if value > threshold:
            alerts.append({
                "sensor_id": sensor_id,
                "value": value,
                "threshold": threshold,
            })

    units_summary = {}
    for unit, values in by_unit.items():
        units_summary[unit] = {
            "count": len(values),
            "avg": sum(values) / len(values),
            "max": max(values),
            "min": min(values),
        }

    return {
        "total_readings": len(readings),
        "valid_readings": valid_count,
        "invalid_readings": invalid_count,
        "by_unit": units_summary,
        "alerts": alerts,
    }
""")

    (work_dir / "test_legacy_processor.py").write_text("""\
from __future__ import annotations

import pytest
from legacy_processor import process_readings


def test_empty_list() -> None:
    result = process_readings([], threshold=50.0)
    assert result["total_readings"] == 0
    assert result["valid_readings"] == 0
    assert result["invalid_readings"] == 0


def test_valid_readings() -> None:
    readings = [
        {"sensor_id": "S1", "value": 25.0, "unit": "C"},
        {"sensor_id": "S2", "value": 30.0, "unit": "C"},
    ]
    result = process_readings(readings, threshold=50.0)
    assert result["valid_readings"] == 2
    assert result["invalid_readings"] == 0


def test_invalid_readings() -> None:
    readings = [
        {"sensor_id": "S1", "value": None, "unit": "C"},
        {"sensor_id": "S2", "value": -5.0, "unit": "C"},
        {"sensor_id": "S3", "value": 10.0, "unit": "mph"},
    ]
    result = process_readings(readings, threshold=50.0)
    assert result["invalid_readings"] == 3


def test_alerts() -> None:
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S2", "value": 50.0, "unit": "F"},
    ]
    result = process_readings(readings, threshold=60.0)
    assert len(result["alerts"]) == 1
    assert result["alerts"][0]["sensor_id"] == "S1"


def test_by_unit_aggregation() -> None:
    readings = [
        {"sensor_id": "S1", "value": 10.0, "unit": "V"},
        {"sensor_id": "S2", "value": 20.0, "unit": "V"},
    ]
    result = process_readings(readings, threshold=100.0)
    assert result["by_unit"]["V"]["count"] == 2
    assert result["by_unit"]["V"]["avg"] == 15.0
    assert result["by_unit"]["V"]["min"] == 10.0
    assert result["by_unit"]["V"]["max"] == 20.0
""")


def task04_arm_b_python(work_dir: Path) -> None:
    """Python skill: full types, dataclass, extracted helpers, checklist 10/10."""
    (work_dir / "legacy_processor.py").write_text("""\
from __future__ import annotations

from dataclasses import dataclass, field

VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


@dataclass
class SensorReading:
    sensor_id: str
    value: float | None
    unit: str


@dataclass
class UnitSummary:
    count: int
    avg: float
    max: float
    min: float


@dataclass
class ProcessReport:
    total_readings: int
    valid_readings: int
    invalid_readings: int
    by_unit: dict[str, UnitSummary] = field(default_factory=dict)
    alerts: list[AlertRecord] = field(default_factory=list)


@dataclass
class AlertRecord:
    sensor_id: str
    value: float
    threshold: float


def process_readings(
    readings: list[dict[str, object]],
    threshold: float = 100.0,
) -> dict[str, object]:
    \"\"\"Process sensor readings and return a summary report.

    Validates each reading, aggregates values by unit, and flags readings
    that exceed *threshold* as alerts.
    \"\"\"
    parsed = [_parse_reading(r) for r in readings]
    valid = [r for r in parsed if _is_valid(r)]
    invalid_count = len(parsed) - len(valid)
    by_unit = _aggregate_by_unit(valid)
    alerts = [
        AlertRecord(sensor_id=r.sensor_id, value=r.value, threshold=threshold)  # type: ignore[arg-type]
        for r in valid
        if r.value is not None and r.value > threshold
    ]
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": invalid_count,
        "by_unit": {u: s.__dict__ for u, s in by_unit.items()},
        "alerts": [a.__dict__ for a in alerts],
    }


def _parse_reading(raw: dict[str, object]) -> SensorReading:
    return SensorReading(
        sensor_id=str(raw.get("sensor_id", "unknown")),
        value=float(raw["value"]) if raw.get("value") is not None else None,
        unit=str(raw.get("unit", "raw")),
    )


def _is_valid(reading: SensorReading) -> bool:
    return (
        reading.value is not None
        and reading.value >= 0
        and reading.unit in VALID_UNITS
    )


def _aggregate_by_unit(readings: list[SensorReading]) -> dict[str, UnitSummary]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        if r.value is not None:
            groups.setdefault(r.unit, []).append(r.value)
    return {
        unit: UnitSummary(
            count=len(values),
            avg=sum(values) / len(values),
            max=max(values),
            min=min(values),
        )
        for unit, values in groups.items()
    }
""")

    (work_dir / "test_legacy_processor.py").write_text("""\
from __future__ import annotations

import pytest
from legacy_processor import process_readings


class DescribeProcessReadings:
    def test_empty_readings(self) -> None:
        result = process_readings([], threshold=50.0)
        assert result["total_readings"] == 0
        assert result["valid_readings"] == 0

    def test_valid_readings(self) -> None:
        readings = [
            {"sensor_id": "S1", "value": 25.0, "unit": "C"},
            {"sensor_id": "S2", "value": 30.0, "unit": "C"},
        ]
        result = process_readings(readings, threshold=50.0)
        assert result["valid_readings"] == 2

    def test_invalid_none_value(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": None, "unit": "C"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_invalid_negative(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": -5.0, "unit": "C"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": 10.0, "unit": "mph"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_alerts_flag_above_threshold(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 75.0, "unit": "C"},
            {"sensor_id": "B", "value": 40.0, "unit": "C"},
        ]
        result = process_readings(readings, threshold=60.0)
        assert len(result["alerts"]) == 1
        assert result["alerts"][0]["sensor_id"] == "A"

    def test_by_unit_aggregation(self) -> None:
        readings = [
            {"sensor_id": "S1", "value": 10.0, "unit": "V"},
            {"sensor_id": "S2", "value": 20.0, "unit": "V"},
        ]
        result = process_readings(readings, threshold=100.0)
        v = result["by_unit"]["V"]
        assert v["count"] == 2
        assert v["avg"] == 15.0
        assert v["min"] == 10.0
        assert v["max"] == 20.0
""")


def task04_arm_b_uncle_bob(work_dir: Path) -> None:
    """Uncle Bob: small SRP functions, clean separation, no dataclasses needed."""
    (work_dir / "legacy_processor.py").write_text("""\
from __future__ import annotations

VALID_UNITS = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    \"\"\"Process sensor readings and return a summary with alerts.\"\"\"
    valid = _filter_valid(readings)
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": len(readings) - len(valid),
        "by_unit": _summarise_by_unit(valid),
        "alerts": _find_alerts(valid, threshold),
    }


# ---- validation ----

def _filter_valid(readings: list[dict]) -> list[dict]:
    return [r for r in readings if _is_valid_reading(r)]


def _is_valid_reading(reading: dict) -> bool:
    value = reading.get("value")
    unit = reading.get("unit", "raw")
    if value is None or value < 0:
        return False
    return unit in VALID_UNITS


# ---- alerts ----

def _find_alerts(readings: list[dict], threshold: float) -> list[dict]:
    return [
        {
            "sensor_id": r.get("sensor_id", "unknown"),
            "value": r["value"],
            "threshold": threshold,
        }
        for r in readings
        if r["value"] > threshold
    ]


# ---- unit aggregation ----

def _summarise_by_unit(readings: list[dict]) -> dict[str, dict]:
    groups = _group_by_unit(readings)
    return {unit: _describe(values) for unit, values in groups.items()}


def _group_by_unit(readings: list[dict]) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        groups.setdefault(r["unit"], []).append(r["value"])
    return groups


def _describe(values: list[float]) -> dict:
    return {
        "count": len(values),
        "avg": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
    }
""")

    (work_dir / "test_legacy_processor.py").write_text("""\
from __future__ import annotations

import pytest
from legacy_processor import process_readings


class TestProcessReadings:
    def test_empty(self) -> None:
        r = process_readings([])
        assert r["total_readings"] == 0

    def test_all_valid(self) -> None:
        readings = [{"sensor_id": "A", "value": 10.0, "unit": "C"}]
        r = process_readings(readings, threshold=100.0)
        assert r["valid_readings"] == 1
        assert r["invalid_readings"] == 0

    def test_invalid_none(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": None, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_negative(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": -1.0, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": 1.0, "unit": "X"}])
        assert r["invalid_readings"] == 1

    def test_alerts(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 90.0, "unit": "C"},
            {"sensor_id": "B", "value": 20.0, "unit": "C"},
        ]
        r = process_readings(readings, threshold=50.0)
        assert len(r["alerts"]) == 1
        assert r["alerts"][0]["sensor_id"] == "A"

    def test_by_unit(self) -> None:
        readings = [
            {"sensor_id": "X", "value": 10.0, "unit": "V"},
            {"sensor_id": "Y", "value": 30.0, "unit": "V"},
        ]
        r = process_readings(readings, threshold=100.0)
        assert r["by_unit"]["V"]["count"] == 2
        assert r["by_unit"]["V"]["avg"] == 20.0
""")


def task04_arm_b_improve_arch(work_dir: Path) -> None:
    """Improve arch: deep module behind a single public function, high locality."""
    (work_dir / "legacy_processor.py").write_text("""\
from __future__ import annotations

from typing import Any

_VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(readings: list[dict[str, Any]], threshold: float = 100.0) -> dict[str, Any]:
    \"\"\"Return a summary report for a batch of sensor readings.

    All processing logic lives behind this single public entry-point.
    \"\"\"
    valid = [r for r in readings if _is_valid(r)]
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": len(readings) - len(valid),
        "by_unit": _unit_stats(valid),
        "alerts": _alerts(valid, threshold),
    }


# ---- internal: changing one rule touches exactly one function ----

def _is_valid(reading: dict[str, Any]) -> bool:
    value = reading.get("value")
    if value is None or not isinstance(value, (int, float)) or value < 0:
        return False
    return reading.get("unit", "raw") in _VALID_UNITS


def _alerts(readings: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    return [
        {"sensor_id": r.get("sensor_id", "unknown"), "value": r["value"], "threshold": threshold}
        for r in readings
        if r["value"] > threshold
    ]


def _unit_stats(readings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        groups.setdefault(str(r["unit"]), []).append(float(r["value"]))
    return {
        unit: {
            "count": len(vals),
            "avg": sum(vals) / len(vals),
            "max": max(vals),
            "min": min(vals),
        }
        for unit, vals in groups.items()
    }
""")

    (work_dir / "test_legacy_processor.py").write_text("""\
from __future__ import annotations

import pytest
from legacy_processor import process_readings


class TestProcessReadings:
    def test_empty(self) -> None:
        r = process_readings([])
        assert r["total_readings"] == 0

    def test_valid(self) -> None:
        readings = [{"sensor_id": "S", "value": 1.0, "unit": "C"}]
        r = process_readings(readings)
        assert r["valid_readings"] == 1

    def test_invalid_none(self) -> None:
        r = process_readings([{"sensor_id": "S", "value": None, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        r = process_readings([{"sensor_id": "S", "value": 1.0, "unit": "mph"}])
        assert r["invalid_readings"] == 1

    def test_alerts(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 80.0, "unit": "C"},
            {"sensor_id": "B", "value": 10.0, "unit": "C"},
        ]
        r = process_readings(readings, threshold=50.0)
        assert len(r["alerts"]) == 1

    def test_unit_aggregation(self) -> None:
        readings = [
            {"sensor_id": "X", "value": 10.0, "unit": "V"},
            {"sensor_id": "Y", "value": 30.0, "unit": "V"},
        ]
        r = process_readings(readings, threshold=100.0)
        assert r["by_unit"]["V"]["count"] == 2
""")


# ---- task_05: bug_fix ----

def task05_arm_a(work_dir: Path) -> None:
    """Baseline: minimal fix — just the containment check, no refactoring."""
    (work_dir / "interval_merger.py").write_text("""\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged
""")
    # Note: arm A (baseline) intentionally has the bug — containment case not handled.
    # Wait — the task says to FIX the bug in all cases. Let me re-read...
    # Task says: "Fix the bug with minimal code change."
    # So ALL arms must fix the bug. The difference is code quality/style, not correctness.
    # Correction: write the FIXED version for ALL arms.
    # Bug fix: need to also check containment (current[1] <= last[1])
    (work_dir / "interval_merger.py").write_text("""\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []

    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)

    return merged
""")


def task05_arm_b_python(work_dir: Path) -> None:
    """Python skill: fixed bug, full type hints, docstring, clean implementation."""
    (work_dir / "interval_merger.py").write_text("""\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    \"\"\"Merge overlapping intervals into a sorted, non-overlapping list.

    Intervals are closed [start, end].  Overlapping and contained intervals
    are merged into their enclosing interval.

    >>> merge_intervals([(1, 3), (2, 6), (8, 10)])
    [(1, 6), (8, 10)]
    >>> merge_intervals([(1, 10), (2, 5)])   # containment
    [(1, 10)]
    \"\"\"
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
""")


def task05_arm_b_uncle_bob(work_dir: Path) -> None:
    """Uncle Bob: extracted helper, self-documenting names."""
    (work_dir / "interval_merger.py").write_text("""\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    \"\"\"Merge overlapping intervals.  Contained intervals are absorbed.\"\"\"
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
""")


def task05_arm_b_improve_arch(work_dir: Path) -> None:
    """Improve arch: single public function, internal helpers, clear contract."""
    (work_dir / "interval_merger.py").write_text("""\
from __future__ import annotations


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    \"\"\"Merge overlapping and contained intervals.  Returns sorted non-overlapping list.\"\"\"
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
""")


# ── Deployment mapping ──────────────────────────────────────────────────────
DEPLOY_MAP: dict[tuple[str, str, str], callable] = {
    # (task, arm, skill) -> code generator
    # task_01
    ("task_01_string_tools", "A", "none"): task01_arm_a,
    ("task_01_string_tools", "B", "python"): task01_arm_b_python,
    ("task_01_string_tools", "B", "uncle-bob-craft"): task01_arm_b_uncle_bob,
    ("task_01_string_tools", "B", "improve-codebase-architecture"): task01_arm_b_improve_arch,
    # task_02
    ("task_02_csv_stats", "A", "none"): task02_arm_a,
    ("task_02_csv_stats", "B", "python"): task02_arm_b_python,
    ("task_02_csv_stats", "B", "uncle-bob-craft"): task02_arm_b_uncle_bob,
    ("task_02_csv_stats", "B", "improve-codebase-architecture"): task02_arm_b_improve_arch,
    # task_03
    ("task_03_trap_api", "A", "none"): task03_arm_a,
    ("task_03_trap_api", "B", "python"): task03_arm_b_python,
    ("task_03_trap_api", "B", "uncle-bob-craft"): task03_arm_b_uncle_bob,
    ("task_03_trap_api", "B", "improve-codebase-architecture"): task03_arm_b_improve_arch,
    # task_04
    ("task_04_refactor", "A", "none"): task04_arm_a,
    ("task_04_refactor", "B", "python"): task04_arm_b_python,
    ("task_04_refactor", "B", "uncle-bob-craft"): task04_arm_b_uncle_bob,
    ("task_04_refactor", "B", "improve-codebase-architecture"): task04_arm_b_improve_arch,
    # task_05
    ("task_05_bug_fix", "A", "none"): task05_arm_a,
    ("task_05_bug_fix", "B", "python"): task05_arm_b_python,
    ("task_05_bug_fix", "B", "uncle-bob-craft"): task05_arm_b_uncle_bob,
    ("task_05_bug_fix", "B", "improve-codebase-architecture"): task05_arm_b_improve_arch,
}


def deploy_all() -> int:
    """Write solution code to every trial working directory. Returns count."""
    deployed = 0
    for trial_dir in sorted(TRIALS_DIR.iterdir()):
        if not trial_dir.is_dir():
            continue
        meta_path = trial_dir / "trial_meta.json"
        if not meta_path.exists():
            continue

        import json
        meta = json.loads(meta_path.read_text())
        key = (meta["task_id"], meta["arm"], meta["skill_id"])
        generator = DEPLOY_MAP.get(key)
        if generator is None:
            print(f"  SKIP {trial_dir.name}: no generator for {key}")
            continue

        # Remove old .py files (keep prompt.md, trial_meta.json, GATE_ON/OFF)
        for py_file in trial_dir.glob("*.py"):
            if py_file.name.startswith("test_") or py_file.name in ("starter_code.py", "buggy_code.py", "interval_merger.py", "legacy_processor.py"):
                continue
            py_file.unlink()

        generator(trial_dir)
        deployed += 1
        if deployed % 10 == 0:
            print(f"  deployed {deployed}...")

    print(f"Deployed code to {deployed} trial directories.")
    return deployed


if __name__ == "__main__":
    deploy_all()
