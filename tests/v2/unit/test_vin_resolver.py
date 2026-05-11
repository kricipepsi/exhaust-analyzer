"""Unit tests for engine/v2/vin/ — VIN resolver, data lint, confidence levels."""

from __future__ import annotations

import json
import pathlib

import pytest

from engine.v2.vin import resolve
from engine.v2.vin.prior_context import EngineDNA


# ── invalid VIN format ─────────────────────────────────────────────────────


def test_invalid_format_short_vin():
    """VIN shorter than 17 chars returns confidence='none'."""
    result = resolve("WVWZZZ1K")
    assert result.confidence == "none"
    assert result.source == "unknown"


def test_invalid_format_invalid_chars():
    """VIN with invalid characters returns confidence='none'."""
    result = resolve("INVALID___VIN1234")
    assert result.confidence == "none"


def test_invalid_format_empty():
    """Empty VIN returns confidence='none'."""
    result = resolve("")
    assert result.confidence == "none"


def test_invalid_format_lowercase_valid_structure():
    """Lowercase VIN with valid structure is still normalized and resolved."""
    result = resolve("wvwzzz1kzaw123456")
    assert result.confidence == "high"


# ── happy-path VINs ────────────────────────────────────────────────────────


def test_happy_path_vw_bse():
    """WVWZZZ1KZAW123456 resolves to VW BSE with high confidence."""
    result = resolve("WVWZZZ1KZAW123456")
    assert result.confidence == "high"
    assert result.make == "VOLKSWAGEN"
    assert result.engine_code == "BSE"


def test_happy_path_bmw_b38():
    """WBA8E9C50GK647890 resolves to BMW B38B15A with high confidence."""
    result = resolve("WBA8E9C50GK647890")
    assert result.confidence == "high"
    assert result.make == "BMW"
    assert result.engine_code == "B38B15A"


def test_happy_path_porsche_cyp():
    """WAUZZZ4G0CN012345 resolves to Porsche CYP with high confidence."""
    result = resolve("WAUZZZ4G0CN012345")
    assert result.confidence == "high"
    assert result.make == "PORSCHE"
    assert result.engine_code == "CYP"


# ── partial confidence (WMI only) ──────────────────────────────────────────


def test_partial_confidence_wmi_only():
    """A VIN with valid WMI but engine code not in DNA returns partial."""
    result = resolve("VF1AAAAA123456789")
    assert result.confidence == "partial"
    assert result.make is not None
    assert result.engine_code is None


# ── EngineDNA dataclass ────────────────────────────────────────────────────


def test_engine_dna_unknown_sentinel():
    """EngineDNA.unknown() returns sentinel with confidence='none'."""
    dna = EngineDNA.unknown()
    assert dna.confidence == "none"
    assert dna.source == "unknown"


def test_engine_dna_partial_factory():
    """EngineDNA.partial() returns WMI-only result."""
    dna = EngineDNA.partial("RENAULT")
    assert dna.confidence == "partial"
    assert dna.make == "RENAULT"


def test_engine_dna_from_dna_row():
    """EngineDNA.from_dna_row() builds from a dict."""
    row = {
        "manufacturer": "TEST",
        "engine_code": "TST123",
        "displacement_l": 2.0,
        "cylinders": 4,
        "induction": "na",
        "injection": "mpfi",
        "fuel_type": "petrol",
        "o2_arch": "narrowband",
    }
    dna = EngineDNA.from_dna_row(row)
    assert dna.confidence == "high"
    assert dna.make == "TEST"
    assert dna.engine_code == "TST123"


# ── petrol-only data lint (R12) ────────────────────────────────────────────


def test_petrol_only_data_lint():
    """All 1,978 rows in engine_dna.json must have fuel_type='petrol' (R12)."""
    dna_path = (
        pathlib.Path(__file__).resolve().parent.parent.parent.parent
        / "engine" / "v2" / "vin" / "data" / "engine_dna.json"
    )
    rows = json.loads(dna_path.read_text(encoding="utf-8"))
    non_petrol = [
        r["engine_code"] for r in rows if r.get("fuel_type") != "petrol"
    ]
    assert not non_petrol, f"R12 violation: non-petrol rows in engine_dna.json: {non_petrol[:5]}"
    assert len(rows) == 1978, f"Expected 1978 rows, got {len(rows)}"
