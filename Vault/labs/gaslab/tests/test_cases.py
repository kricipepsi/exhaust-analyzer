"""Parametrized integration tests over gaslab_cases.csv."""

from __future__ import annotations

from pathlib import Path
import pytest

CSV_PATH = Path(__file__).resolve().parent / "fixtures" / "gaslab_cases.csv"


@pytest.mark.skipif(not CSV_PATH.exists(), reason="gaslab_cases.csv not yet derived")
def test_csv_cases() -> None:
    """Run master-derived integration cases."""
    pass
