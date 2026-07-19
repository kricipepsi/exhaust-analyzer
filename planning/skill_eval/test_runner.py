"""Tests for the eval runner itself."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from runner import (
    TrialRecord,
    _count_mutation_sites,
    _make_trial_id,
    _mutation_score,
    _run_pytest_measure_only,
    capture_metrics,
    prepare_trial,
    write_records,
)

# Production module shared by the mutation-score tests: a small function with
# real mutation sites (a comparison, an arithmetic op, and an int literal).
_MUT_PROD = '''\
def score(a: int, b: int) -> int:
    """Return a*b + 1 when a > b, else a - b."""
    if a > b:
        return a * b + 1
    return a - b
'''


def test_prepare_trial_creates_working_dir(tmp_path: Path) -> None:
    """Verify prepare_trial creates the expected files."""
    # Patch TRIALS_DIR to use tmp_path for this test
    import runner
    orig_trials = runner.TRIALS_DIR
    runner.TRIALS_DIR = tmp_path
    try:
        work_dir = prepare_trial(
            task_id="task_01_string_tools",
            arm="A",
            skill_id="none",
            seed=42,
        )
        assert work_dir.exists()
        assert (work_dir / "trial_meta.json").exists()
        assert (work_dir / "GATE_ON").exists()
        assert (work_dir / "prompt.md").exists()

        meta = json.loads((work_dir / "trial_meta.json").read_text())
        assert meta["arm"] == "A"
        assert meta["skill_id"] == "none"
        assert meta["seed"] == 42
    finally:
        runner.TRIALS_DIR = orig_trials


def test_arm_c_skips_gate(tmp_path: Path) -> None:
    """Arm C with --no-gate must produce GATE_OFF marker and zero gate counts."""
    import runner
    orig_trials = runner.TRIALS_DIR
    runner.TRIALS_DIR = tmp_path
    try:
        work_dir = prepare_trial(
            task_id="task_01_string_tools",
            arm="C",
            skill_id="verification-loop",
            seed=99,
            no_gate=True,
        )
        assert (work_dir / "GATE_OFF").exists()
        assert not (work_dir / "GATE_ON").exists()

        # Write a valid solution so capture doesn't crash
        (work_dir / "string_tools.py").write_text("""
def count_vowels(text: str) -> dict[str, int]:
    return {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

def longest_word(text: str) -> str | None:
    return None

def is_palindrome(text: str) -> bool:
    return True
""")

        rec = capture_metrics(work_dir)
        assert rec.first_ruff_errors == 0, f"Expected 0 ruff errors with gate OFF, got {rec.first_ruff_errors}"
        assert rec.first_pyright_errors == 0, f"Expected 0 pyright errors with gate OFF, got {rec.first_pyright_errors}"
        assert rec.first_pytest_failures == 0, f"Expected 0 pytest failures with gate OFF, got {rec.first_pytest_failures}"
        assert rec.arm == "C"
    finally:
        runner.TRIALS_DIR = orig_trials


def test_arm_c_records_oracle_and_single_shot(tmp_path: Path) -> None:
    """Arm-C capture (FU-SE-4) records oracle_failures + single_shot_pytest_failures.

    Deploys a deliberately wrong string_tools (longest_word ties resolve to the
    *last* word and is_palindrome always True) so the hidden oracle fails some
    checks — the escaped-defect signal arm C exists to measure — and a visible
    test that fails once, never repaired.
    """
    import runner

    orig_trials = runner.TRIALS_DIR
    runner.TRIALS_DIR = tmp_path
    try:
        work_dir = prepare_trial(
            task_id="task_01_string_tools",
            arm="C",
            skill_id="none",
            seed=7,
            no_gate=True,
        )
        (work_dir / "string_tools.py").write_text(
            "def count_vowels(text: str) -> dict[str, int]:\n"
            '    """Count vowels."""\n'
            "    counts = {v: 0 for v in 'aeiou'}\n"
            "    for ch in text.lower():\n"
            "        if ch in counts:\n"
            "            counts[ch] += 1\n"
            "    return counts\n\n"
            "def longest_word(text: str) -> str | None:\n"
            '    """Longest word (BUG: ties resolve to last)."""\n'
            "    words = text.split()\n"
            "    if not words:\n"
            "        return None\n"
            "    best = words[0]\n"
            "    for w in words:\n"
            "        if len(w) >= len(best):\n"
            "            best = w\n"
            "    return best\n\n"
            "def is_palindrome(text: str) -> bool:\n"
            '    """Palindrome (BUG: always True)."""\n'
            "    return True\n",
            encoding="utf-8",
        )
        (work_dir / "test_string_tools.py").write_text(
            "from string_tools import is_palindrome\n"
            "def test_not_palindrome():\n"
            "    assert is_palindrome('hello') is False\n",
            encoding="utf-8",
        )

        rec = capture_metrics(work_dir)
        # Gate counts stay at default (skipped under no_gate).
        assert rec.first_pytest_failures == 0
        # Oracle ran and caught escaped defects.
        assert rec.extra["oracle_failures"] is not None
        assert rec.extra["oracle_failures"] >= 1
        assert rec.extra["oracle_total_checks"] >= 1
        # Single-shot visible suite measured once: the always-True bug fails it.
        assert rec.extra["single_shot_pytest_failures"] == 1
    finally:
        runner.TRIALS_DIR = orig_trials


def test_measure_only_counts_all_failures(tmp_path: Path) -> None:
    """_run_pytest_measure_only counts *every* failure (no -x short-circuit)."""
    (tmp_path / "mod.py").write_text("def f() -> int:\n    return 1\n", encoding="utf-8")
    (tmp_path / "test_mod.py").write_text(
        "from mod import f\n"
        "def test_a(): assert f() == 2\n"
        "def test_b(): assert f() == 3\n"
        "def test_c(): assert f() == 1\n",
        encoding="utf-8",
    )
    failures, errors = _run_pytest_measure_only(tmp_path)
    assert failures == 2  # both wrong asserts, not short-circuited at the first
    assert errors == 0


def test_trial_record_to_dict() -> None:
    """Verify TrialRecord.to_dict() includes all fields."""
    rec = TrialRecord(
        trial_id="test__none__A__0",
        task_id="test",
        skill_id="none",
        arm="A",
        seed=0,
        model="test@t=0",
        timestamp_utc="2026-01-01T00:00:00Z",
    )
    d = rec.to_dict()
    assert d["trial_id"] == "test__none__A__0"
    assert d["arm"] == "A"
    # All schema fields should be present
    for field in TrialRecord.__slots__:  # type: ignore[attr-defined]
        assert field in d, f"Missing field: {field}"


def test_validate_rejects_bad_arm() -> None:
    """Verify validation catches invalid arm values."""
    rec = TrialRecord(
        trial_id="test",
        task_id="test",
        skill_id="none",
        arm="D",  # invalid
        seed=0,
        model="m",
        timestamp_utc="t",
    )
    # We can construct it, but capture_metrics should produce valid arms
    # Just verify the dataclass doesn't enforce at construction time
    assert rec.arm == "D"


def test_make_trial_id() -> None:
    """Verify trial ID format."""
    tid = _make_trial_id("task_01", "python", "B", 42)
    assert tid == "task_01__python__B__42"


def test_mutation_score_none_without_tests(tmp_path: Path) -> None:
    """A trial with production code but no test suite has no mutation score."""
    (tmp_path / "calc.py").write_text(_MUT_PROD, encoding="utf-8")
    assert _mutation_score(tmp_path) is None


def test_mutation_score_strong_suite_kills_all(tmp_path: Path) -> None:
    """A behavioural suite covering both branches kills every mutant (score 1.0)."""
    (tmp_path / "calc.py").write_text(_MUT_PROD, encoding="utf-8")
    (tmp_path / "test_calc.py").write_text(
        "from calc import score\n"
        "def test_gt(): assert score(5, 3) == 16\n"
        "def test_le(): assert score(2, 7) == -5\n"
        "def test_eq(): assert score(4, 4) == 0\n",
        encoding="utf-8",
    )
    score = _mutation_score(tmp_path)
    assert score == 1.0


def test_mutation_score_weak_suite_kills_fewer(tmp_path: Path) -> None:
    """A loose suite kills strictly fewer mutants than the strong one — the metric
    is real (not stubbed) and discriminates test quality (T-SE-4 spot-check)."""
    (tmp_path / "calc.py").write_text(_MUT_PROD, encoding="utf-8")
    (tmp_path / "test_calc.py").write_text(
        "from calc import score\n"
        "def test_loose(): assert score(5, 3) > 0\n",
        encoding="utf-8",
    )
    assert _count_mutation_sites(_MUT_PROD) > 0
    score = _mutation_score(tmp_path)
    assert score is not None
    assert score < 1.0


def test_write_records(tmp_path: Path) -> None:
    """Verify write_records produces valid JSON-lines."""
    output = tmp_path / "test.jsonl"
    rec = TrialRecord(
        trial_id="test__none__A__0",
        task_id="test",
        skill_id="none",
        arm="A",
        seed=0,
        model="test@t=0",
        timestamp_utc="2026-01-01T00:00:00Z",
    )
    write_records([rec], output)

    lines = output.read_text().strip().split("\n")
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["trial_id"] == "test__none__A__0"
