"""Vocabulary drift guard.

Verifies every enum value in dtclab/schemas/vocabulary.py appears verbatim in
DTC_VOCABULARY.md. Drift in either direction fails the test.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from dtclab.schemas import vocabulary as V

VOCAB_PATH = (
    Path(__file__).parent.parent.parent
    / "docs" / "DTC_VOCABULARY.md"
)
VOCAB = VOCAB_PATH.read_text(encoding="utf-8")

DRIFT_CASES = [
    (V.DTCRoutingTag, 17),
    (V.DTCSeverityClass, 4),
    (V.DTCState, 3),
    (V.Mode06MonitorState, 4),
    (V.FuelSystemStatus, 4),
    (V.HistoricalFaultContext, 4),
]


@pytest.mark.parametrize(("enum_cls", "expected_count"), DRIFT_CASES)
def test_wiki_drift_guard(enum_cls, expected_count):
    """Every enum value must appear verbatim in DTC_VOCABULARY.md."""
    members = list(enum_cls)
    assert len(members) == expected_count, (
        f"{enum_cls.__name__} has {len(members)} members; "
        f"expected {expected_count}"
    )
    for member in enum_cls:
        assert member.value in VOCAB, (
            f"{enum_cls.__name__}.{member.name} = {member.value!r} "
            f"not found in DTC_VOCABULARY.md"
        )


def test_dtc_regex_matches_vocab():
    """DTC_REGEX must match DTC_VOCABULARY.md §10 canonical form."""
    assert V.DTC_REGEX == r"^[BCPU][0-3][0-9A-F]{3}$"


def test_bp_regex_is_forbidden():
    """The BP regex form must not appear in any Python source under dtclab/."""
    src_dir = Path(__file__).parent.parent.parent / "dtclab"
    for py_file in src_dir.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert "B-D,P,U" not in text, (
            f"{py_file} contains BP-form regex fragment 'B-D,P,U' — "
            "use the canonical form [BCPU] (DTC_VOCABULARY.md §2.3)"
        )
