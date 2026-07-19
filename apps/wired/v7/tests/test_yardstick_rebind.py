"""Regression tests for the active V3 yardstick hash lock."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

V7_ROOT = Path(__file__).resolve().parents[1]
if str(V7_ROOT) not in sys.path:
    sys.path.insert(0, str(V7_ROOT))

from fl_tasks.score_v3_yardstick import (  # noqa: E402
    ACTIVE_CSV_SHA256,
    ACTIVE_ORACLE_SUBSET_SHA256,
    ACTIVE_SCORER_SHA256,
    DEFAULT_CSV_PATH,
    V3_YARDSTICK_NAME,
    YardstickRefusalError,
    check_hash_lock,
)


def test_active_v3_hash_lock_accepts_current_corpus() -> None:
    """The live post-re-pin corpus matches the active V3 hash tuple."""
    lock = check_hash_lock(DEFAULT_CSV_PATH)

    assert lock["yardstick"] == V3_YARDSTICK_NAME
    assert lock["status"] == "ok"
    assert lock["mismatches"] == []
    assert lock["expected"] == {
        "csv_sha256": ACTIVE_CSV_SHA256,
        "oracle_subset_sha256": ACTIVE_ORACLE_SUBSET_SHA256,
        "scorer_sha256": ACTIVE_SCORER_SHA256,
    }
    assert lock["override_yardstick"] is None


def test_active_v3_hash_lock_refuses_mutated_corpus(tmp_path: Path) -> None:
    """A corpus byte drift that matches neither frozen tuple still refuses."""
    mutated_csv = tmp_path / "cases_petrol_v7_mutated.csv"
    text = DEFAULT_CSV_PATH.read_text(encoding="utf-8")
    mutated_csv.write_text(
        text.replace(
            "cases_petrol_era_v1.csv:era1_001",
            "cases_petrol_era_v1.csv:era1_001_MUTATED",
            1,
        ),
        encoding="utf-8",
    )

    with pytest.raises(YardstickRefusalError, match=V3_YARDSTICK_NAME):
        check_hash_lock(mutated_csv)
