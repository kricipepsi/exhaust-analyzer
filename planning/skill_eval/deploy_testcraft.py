#!/usr/bin/env python3.14
"""Deploy code variants for the T-SE-4 test-craft cohort.

Design (CONTRACT §2/§3, T-SE-4 spec): the test-craft skills (`python-testing`,
`ai-regression-testing`) claim to improve the **test suite** the coder writes —
not the production code. So for each subset task the *production module is held
byte-identical across all three arms*; only the test suite varies. That isolates
the skill's effect on the cohort's primary metric, `mutation_score`: identical
production code exposes identical mutants, and the kill ratio then reflects the
test suite alone.

Arms:
    A (baseline)            — shallow happy-path suite: a few asserts, no
                              parametrization, no edge/error coverage.
    B (python-testing)      — TDD craft: parametrized cases, fixtures, edge cases,
                              behavioural (not implementation-coupled) asserts.
    B (ai-regression-testing) — regression/escaped-defect focus: tests named after
                              the defect they guard, boundary/None/error-path
                              asserts, output-shape parity checks.

Each suite is written to import the fixed production module and to pass green on
the unmutated code (the mutation baseline requirement enforced by runner.py).

Usage:
    python deploy_testcraft.py        # deploy to every prepared test-craft trial
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

PACK_HOME = Path(__file__).resolve().parent
# Isolated from T-SE-3's trials/ — see orchestrator_testcraft.py.
TRIALS_DIR = PACK_HOME / "trials_testcraft"

# ---------------------------------------------------------------------------
# Fixed production modules (identical across arms within a task)
# ---------------------------------------------------------------------------

PROD_STRING_TOOLS = '''\
from __future__ import annotations

VOWELS: frozenset[str] = frozenset({"a", "e", "i", "o", "u"})


def count_vowels(text: str) -> dict[str, int]:
    """Count each vowel (a, e, i, o, u) in *text*, case-insensitive."""
    result: dict[str, int] = {vowel: 0 for vowel in sorted(VOWELS)}
    for character in text.casefold():
        if character in result:
            result[character] += 1
    return result


def longest_word(text: str) -> str | None:
    """Return the first longest whitespace-delimited word, or None if empty."""
    words = text.split()
    if not words:
        return None
    return max(words, key=len)


def is_palindrome(text: str) -> bool:
    """Return True if *text* reads the same forwards and backwards.

    Case, whitespace and punctuation are ignored; the empty string is a
    palindrome.
    """
    cleaned = "".join(character for character in text.casefold() if character.isalnum())
    return cleaned == cleaned[::-1]
'''

PROD_CSV_STATS = '''\
from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, median, stdev

StatsRow = dict[str, float | int]
StatsResult = dict[str, StatsRow]


def compute_stats(csv_path: Path) -> StatsResult:
    """Compute summary statistics for every numeric column in *csv_path*.

    Non-numeric and missing values are skipped. Returns an empty dict when the
    file has no rows or no numeric columns.
    """
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {}
    numeric_columns = _extract_numeric_columns(rows)
    return {column: _column_stats(values) for column, values in numeric_columns.items()}


def write_report(stats: StatsResult, report_path: Path) -> None:
    """Write a one-line-per-column summary of *stats* to *report_path*."""
    lines: list[str] = []
    for column, row in sorted(stats.items()):
        lines.append(
            f"{column}: count={row['count']}, mean={row['mean']:.2f}, "
            f"median={row['median']:.2f}, min={row['min']:.2f}, "
            f"max={row['max']:.2f}, stdev={row['stdev']:.2f}"
        )
    report_path.write_text("\\n".join(lines), encoding="utf-8")


def _extract_numeric_columns(rows: list[dict[str, str]]) -> dict[str, list[float]]:
    columns: dict[str, list[float]] = {}
    for key in rows[0]:
        values: list[float] = []
        for row in rows:
            try:
                values.append(float(row[key]))
            except (ValueError, TypeError):
                pass
        if values:
            columns[key] = values
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
'''

PROD_DATA_FETCHER = '''\
from __future__ import annotations

import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen


class FetchError(RuntimeError):
    """Raised when a URL cannot be fetched or its response is not valid JSON."""

    def __init__(self, url: str, reason: str) -> None:
        self.url = url
        super().__init__(f"FetchError for {url!r}: {reason}")


def fetch_json(url: str, cache_dir: str = "./cache") -> dict:
    """Return parsed JSON from *url*, using a file-based disk cache.

    On a cache hit the cached value is returned. On a miss the URL is fetched
    and stored before returning. Raises :exc:`FetchError` when the URL cannot be
    reached or its body is not valid JSON.
    """
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
        raise FetchError(url, f"invalid JSON: {exc}") from exc

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _cache_key(url: str) -> str:
    """Return a filesystem-safe cache filename for *url*."""
    safe = "".join(character if character.isalnum() else "_" for character in url)
    return f"{safe}.json"
'''

PROD_BY_TASK: dict[str, tuple[str, str]] = {
    # task_id -> (production filename, production source)
    "task_01_string_tools": ("string_tools.py", PROD_STRING_TOOLS),
    "task_02_csv_stats": ("csv_stats.py", PROD_CSV_STATS),
    "task_03_trap_api": ("data_fetcher.py", PROD_DATA_FETCHER),
}

# ---------------------------------------------------------------------------
# task_01 test suites
# ---------------------------------------------------------------------------

T01_TEST_ARM_A = '''\
from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels():
    assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}


def test_longest_word():
    assert longest_word("the quick brown fox") == "quick"


def test_is_palindrome():
    assert is_palindrome("racecar") is True
'''

T01_TEST_ARM_B_PYTESTING = '''\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


class TestCountVowels:
    def test_normal_text(self) -> None:
        assert count_vowels("Hello World") == {"a": 0, "e": 1, "i": 0, "o": 2, "u": 0}

    def test_case_insensitive(self) -> None:
        assert count_vowels("AaEeIiOoUu") == {"a": 2, "e": 2, "i": 2, "o": 2, "u": 2}

    def test_empty_input(self) -> None:
        assert count_vowels("") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

    def test_no_vowels(self) -> None:
        assert count_vowels("rhythm") == {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}


class TestLongestWord:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("the quick brown fox jumps", "quick"),
            ("cat dog bat", "cat"),
            ("singleword", "singleword"),
            ("aa bb cc", "aa"),
        ],
    )
    def test_returns_first_longest(self, text: str, expected: str) -> None:
        assert longest_word(text) == expected

    def test_empty_returns_none(self) -> None:
        assert longest_word("") is None

    def test_whitespace_only_returns_none(self) -> None:
        assert longest_word("   \\t\\n ") is None


class TestIsPalindrome:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("racecar", True),
            ("A man a plan a canal Panama", True),
            ("No lemon, no melon", True),
            ("hello", False),
            ("ab", False),
            ("a", True),
            ("", True),
        ],
    )
    def test_palindrome_cases(self, text: str, expected: bool) -> None:
        assert is_palindrome(text) == expected
'''

T01_TEST_ARM_B_AIREGRESSION = '''\
from __future__ import annotations

import pytest
from string_tools import count_vowels, is_palindrome, longest_word


def test_count_vowels_returns_all_five_keys_regression() -> None:
    """GUARD: result must always carry all five vowel keys, even on no match."""
    result = count_vowels("xyz")
    assert set(result) == {"a", "e", "i", "o", "u"}


def test_count_vowels_case_fold_boundary_regression() -> None:
    """GUARD: uppercase vowels must be counted (casefold path)."""
    assert count_vowels("AEIOU") == {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1}


def test_longest_word_empty_returns_none_not_empty_string_regression() -> None:
    """GUARD: empty input must return None, not '' (the None branch)."""
    assert longest_word("") is None
    assert longest_word("   ") is None


def test_longest_word_tie_keeps_first_regression() -> None:
    """GUARD: ties resolve to the first occurrence, not the last."""
    assert longest_word("cat dog bat") == "cat"


def test_is_palindrome_empty_is_true_boundary_regression() -> None:
    """GUARD: the empty string is a palindrome (boundary input)."""
    assert is_palindrome("") is True


def test_is_palindrome_non_palindrome_is_false_regression() -> None:
    """GUARD: a clear non-palindrome must be False (no always-True drift)."""
    assert is_palindrome("hello") is False
    assert is_palindrome("ab") is False


@pytest.mark.parametrize("text", ["racecar", "A man a plan a canal Panama"])
def test_is_palindrome_known_true_cases_regression(text: str) -> None:
    """GUARD: known palindromes stay True across punctuation/space stripping."""
    assert is_palindrome(text) is True
'''

# ---------------------------------------------------------------------------
# task_02 test suites
# ---------------------------------------------------------------------------

T02_TEST_ARM_A = '''\
from pathlib import Path

from csv_stats import compute_stats


def test_compute_stats(tmp_path: Path):
    csv_file = tmp_path / "d.csv"
    csv_file.write_text("name,age\\nAlice,30\\nBob,20\\n")
    stats = compute_stats(csv_file)
    assert "age" in stats
'''

T02_TEST_ARM_B_PYTESTING = '''\
from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    csv_file = tmp_path / "data.csv"
    csv_file.write_text(
        "name,age,score\\nAlice,30,85.5\\nBob,25,92.0\\nCharlie,35,78.3\\n",
        encoding="utf-8",
    )
    return csv_file


class TestComputeStats:
    def test_detects_numeric_columns(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert set(stats) == {"age", "score"}

    def test_count_is_row_count(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["count"] == 3

    def test_mean_is_correct(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["mean"] == pytest.approx(30.0)

    def test_min_and_max(self, sample_csv: Path) -> None:
        stats = compute_stats(sample_csv)
        assert stats["age"]["min"] == pytest.approx(25.0)
        assert stats["age"]["max"] == pytest.approx(35.0)

    def test_empty_csv_returns_empty(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "empty.csv"
        csv_file.write_text("name,city\\n", encoding="utf-8")
        assert compute_stats(csv_file) == {}

    def test_non_numeric_values_skipped(self, tmp_path: Path) -> None:
        csv_file = tmp_path / "mixed.csv"
        csv_file.write_text("v\\n1\\nNA\\n3\\n", encoding="utf-8")
        stats = compute_stats(csv_file)
        assert stats["v"]["count"] == 2
        assert stats["v"]["mean"] == pytest.approx(2.0)


class TestWriteReport:
    def test_report_contains_each_column(self, sample_csv: Path, tmp_path: Path) -> None:
        stats = compute_stats(sample_csv)
        report = tmp_path / "report.txt"
        write_report(stats, report)
        text = report.read_text(encoding="utf-8")
        assert "age:" in text
        assert "score:" in text
'''

T02_TEST_ARM_B_AIREGRESSION = '''\
from __future__ import annotations

from pathlib import Path

import pytest
from csv_stats import compute_stats, write_report


def test_empty_csv_returns_empty_dict_regression(tmp_path: Path) -> None:
    """GUARD: a header-only CSV must yield {} (empty-rows branch)."""
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("a,b\\n", encoding="utf-8")
    assert compute_stats(csv_file) == {}


def test_no_numeric_columns_returns_empty_regression(tmp_path: Path) -> None:
    """GUARD: a CSV with only text columns yields {} (numeric-filter branch)."""
    csv_file = tmp_path / "text.csv"
    csv_file.write_text("name,city\\nAlice,NYC\\nBob,LA\\n", encoding="utf-8")
    assert compute_stats(csv_file) == {}


def test_missing_value_skipped_not_counted_regression(tmp_path: Path) -> None:
    """GUARD: non-numeric cells are skipped; count reflects only parsed values."""
    csv_file = tmp_path / "gappy.csv"
    csv_file.write_text("v\\n10\\n\\n20\\nNA\\n30\\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    assert stats["v"]["count"] == 3
    assert stats["v"]["min"] == pytest.approx(10.0)
    assert stats["v"]["max"] == pytest.approx(30.0)


def test_single_value_stdev_is_zero_boundary_regression(tmp_path: Path) -> None:
    """GUARD: stdev on one value is 0.0, not a StatisticsError (len>1 branch)."""
    csv_file = tmp_path / "one.csv"
    csv_file.write_text("v\\n42\\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    assert stats["v"]["count"] == 1
    assert stats["v"]["stdev"] == pytest.approx(0.0)


def test_all_stat_fields_present_parity_regression(tmp_path: Path) -> None:
    """GUARD: every column row carries the full stats contract (no missing field)."""
    csv_file = tmp_path / "full.csv"
    csv_file.write_text("v\\n1\\n2\\n3\\n4\\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    required = {"count", "mean", "median", "min", "max", "stdev"}
    assert set(stats["v"]) == required


def test_report_written_for_every_column_regression(tmp_path: Path) -> None:
    """GUARD: write_report emits a line per column (no silently dropped column)."""
    csv_file = tmp_path / "two.csv"
    csv_file.write_text("a,b\\n1,10\\n2,20\\n", encoding="utf-8")
    stats = compute_stats(csv_file)
    report = tmp_path / "out.txt"
    write_report(stats, report)
    lines = [ln for ln in report.read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) == 2
'''

# ---------------------------------------------------------------------------
# task_03 test suites (HTTP mocked — no real network)
# ---------------------------------------------------------------------------

T03_TEST_ARM_A = '''\
from unittest.mock import MagicMock, patch

from data_fetcher import fetch_json


def test_fetch_returns_data(tmp_path):
    payload = b'{"key": "value"}'
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    with patch("data_fetcher.urlopen", return_value=response):
        result = fetch_json("http://example.com/api", cache_dir=str(tmp_path))
    assert result == {"key": "value"}
'''

T03_TEST_ARM_B_PYTESTING = '''\
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from data_fetcher import FetchError, fetch_json


def _mock_response(payload: bytes) -> MagicMock:
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


class TestFetchJson:
    def test_returns_parsed_json_on_miss(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"key": "value"}')
        with patch("data_fetcher.urlopen", return_value=response):
            result = fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        assert result == {"key": "value"}

    def test_writes_cache_on_miss(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"n": 1}')
        with patch("data_fetcher.urlopen", return_value=response):
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        cached = list(tmp_path.glob("*.json"))
        assert len(cached) == 1
        assert json.loads(cached[0].read_text(encoding="utf-8")) == {"n": 1}

    def test_cache_hit_skips_network(self, tmp_path: Path) -> None:
        response = _mock_response(b'{"first": true}')
        with patch("data_fetcher.urlopen", return_value=response) as opener:
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
            fetch_json("http://example.com/api", cache_dir=str(tmp_path))
        assert opener.call_count == 1

    def test_url_error_raises_fetch_error(self, tmp_path: Path) -> None:
        from urllib.error import URLError

        with patch("data_fetcher.urlopen", side_effect=URLError("down")):
            with pytest.raises(FetchError):
                fetch_json("http://example.com/api", cache_dir=str(tmp_path))
'''

T03_TEST_ARM_B_AIREGRESSION = '''\
from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import pytest
from data_fetcher import FetchError, fetch_json


def _mock_response(payload: bytes) -> MagicMock:
    response = MagicMock()
    response.read.return_value = payload
    response.__enter__.return_value = response
    response.__exit__.return_value = False
    return response


def test_url_error_raises_fetch_error_regression(tmp_path: Path) -> None:
    """GUARD: unreachable URL raises FetchError, not a bare URLError (error path)."""
    with patch("data_fetcher.urlopen", side_effect=URLError("unreachable")):
        with pytest.raises(FetchError):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_fetch_error_message_carries_url_regression(tmp_path: Path) -> None:
    """GUARD: FetchError message includes the offending URL (diagnosability)."""
    with patch("data_fetcher.urlopen", side_effect=URLError("nope")):
        with pytest.raises(FetchError, match="http://x/api"):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_invalid_json_raises_fetch_error_regression(tmp_path: Path) -> None:
    """GUARD: a 200 body that is not JSON raises FetchError, not JSONDecodeError."""
    response = _mock_response(b"not json at all")
    with patch("data_fetcher.urlopen", return_value=response):
        with pytest.raises(FetchError):
            fetch_json("http://x/api", cache_dir=str(tmp_path))


def test_cache_hit_does_not_call_network_regression(tmp_path: Path) -> None:
    """GUARD: second call hits cache; urlopen must not be called twice (cache path)."""
    response = _mock_response(b'{"v": 1}')
    with patch("data_fetcher.urlopen", return_value=response) as opener:
        fetch_json("http://x/api", cache_dir=str(tmp_path))
        fetch_json("http://x/api", cache_dir=str(tmp_path))
    assert opener.call_count == 1


def test_cache_roundtrip_returns_same_value_regression(tmp_path: Path) -> None:
    """GUARD: cached read returns the same payload the miss path wrote (parity)."""
    response = _mock_response(b'{"v": 7}')
    with patch("data_fetcher.urlopen", return_value=response):
        first = fetch_json("http://x/api", cache_dir=str(tmp_path))
    # Second call: no network patched in -> must come from cache or it would error.
    second = fetch_json("http://x/api", cache_dir=str(tmp_path))
    assert first == second == {"v": 7}
'''

# ---------------------------------------------------------------------------
# Dispatch table: (task_id, arm, skill_id) -> test source
# ---------------------------------------------------------------------------

TEST_BY_KEY: dict[tuple[str, str, str], str] = {
    ("task_01_string_tools", "A", "none"): T01_TEST_ARM_A,
    ("task_01_string_tools", "B", "python-testing"): T01_TEST_ARM_B_PYTESTING,
    ("task_01_string_tools", "B", "ai-regression-testing"): T01_TEST_ARM_B_AIREGRESSION,
    ("task_02_csv_stats", "A", "none"): T02_TEST_ARM_A,
    ("task_02_csv_stats", "B", "python-testing"): T02_TEST_ARM_B_PYTESTING,
    ("task_02_csv_stats", "B", "ai-regression-testing"): T02_TEST_ARM_B_AIREGRESSION,
    ("task_03_trap_api", "A", "none"): T03_TEST_ARM_A,
    ("task_03_trap_api", "B", "python-testing"): T03_TEST_ARM_B_PYTESTING,
    ("task_03_trap_api", "B", "ai-regression-testing"): T03_TEST_ARM_B_AIREGRESSION,
}

TEST_FILENAME: dict[str, str] = {
    "task_01_string_tools": "test_string_tools.py",
    "task_02_csv_stats": "test_csv_stats.py",
    "task_03_trap_api": "test_data_fetcher.py",
}


def _deploy_one(trial_dir: Path, task_id: str, arm: str, skill_id: str) -> bool:
    """Write the fixed production module + arm-specific test suite into *trial_dir*.

    Returns True when a variant was deployed, False when the key is not part of
    the test-craft matrix.
    """
    prod = PROD_BY_TASK.get(task_id)
    test_source = TEST_BY_KEY.get((task_id, arm, skill_id))
    if prod is None or test_source is None:
        return False

    prod_name, prod_source = prod
    # Clear stale .py files (keep prompt.md, trial_meta.json, GATE markers).
    for py_file in trial_dir.glob("*.py"):
        py_file.unlink()

    (trial_dir / prod_name).write_text(prod_source, encoding="utf-8")
    (trial_dir / TEST_FILENAME[task_id]).write_text(test_source, encoding="utf-8")
    return True


def deploy_all() -> int:
    """Deploy code to every prepared test-craft trial directory. Returns count."""
    deployed = 0
    for trial_dir in sorted(TRIALS_DIR.iterdir()):
        if not trial_dir.is_dir():
            continue
        meta_path = trial_dir / "trial_meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text())
        if _deploy_one(trial_dir, meta["task_id"], meta["arm"], meta["skill_id"]):
            deployed += 1
            print(f"  deployed: {trial_dir.name}")
    print(f"Deployed code to {deployed} test-craft trial directories.")
    return deployed


_DISPATCH: Callable[[], int] = deploy_all

if __name__ == "__main__":
    deploy_all()
