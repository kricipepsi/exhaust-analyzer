"""Tests for dtclab.core.dtc_ingestion_gate — DTC format validation.

Covers: valid P/B/C/U codes, malformed codes (BP-form, empty, too-short, too-long,
non-alpha class, lowercase), edge cases (empty list, duplicates), invalid mode.
"""

from __future__ import annotations

import pytest

from dtclab.core.dtc_ingestion_gate import DTCFormatError, validate_dtc_list


# -- valid codes ----------------------------------------------------------------

_VALID_CODES = [
    "P0171",
    "P0300",
    "P0301",
    "P0420",
    "B1200",
    "C1000",
    "U0100",
    "P0001",
    "P3999",
    "B3999",
    "C0999",
    "U3999",
    "P34AF",
]


@pytest.mark.parametrize("code", _VALID_CODES)
def test_valid_code_passes(code: str) -> None:
    result = validate_dtc_list([code], mode="$03")
    assert result == [code]


@pytest.mark.parametrize("mode", ["$03", "$07", "$0A"])
def test_all_three_modes_accepted(mode: str) -> None:
    result = validate_dtc_list(["P0171"], mode=mode)
    assert result == ["P0171"]


# -- invalid codes --------------------------------------------------------------

_INVALID_CODES = [
    ("B-D001", "BP-form regex"),
    ("", "empty string"),
    ("   ", "whitespace only"),
    ("P01", "too short"),
    ("P01711", "too long"),
    ("X0171", "invalid system class"),
    ("p0171", "lowercase"),
    ("P 171", "embedded space"),
]


@pytest.mark.parametrize(("code", "_desc"), _INVALID_CODES)
def test_invalid_raises_dtc_format_error(code: str, _desc: str) -> None:
    with pytest.raises(DTCFormatError) as exc_info:
        validate_dtc_list([code], mode="$03")
    assert exc_info.value.code == code
    assert exc_info.value.mode == "$03"


def test_bp_form_explicitly_rejected() -> None:
    """BP-form DTC 'B-D001' must raise DTCFormatError (wiki §2.3 note)."""
    with pytest.raises(DTCFormatError) as exc_info:
        validate_dtc_list(["B-D001"], mode="$07")
    assert "B-D001" in str(exc_info.value)


def test_empty_string_raises() -> None:
    with pytest.raises(DTCFormatError):
        validate_dtc_list([""], mode="$0A")


def test_fails_on_first_invalid() -> None:
    """Validation stops at the first malformed code."""
    with pytest.raises(DTCFormatError) as exc_info:
        validate_dtc_list(["P0171", "BAD", "P0300"], mode="$03")
    assert exc_info.value.code == "BAD"


# -- edge cases -----------------------------------------------------------------


def test_empty_list_ok() -> None:
    result = validate_dtc_list([], mode="$03")
    assert result == []


def test_duplicates_preserved() -> None:
    codes = ["P0171", "P0300", "P0171"]
    result = validate_dtc_list(codes, mode="$03")
    assert result == codes


def test_unknown_mode_raises_valueerror() -> None:
    with pytest.raises(ValueError, match="Unknown OBD mode"):
        validate_dtc_list(["P0171"], mode="$01")


# -- DTCFormatError carries context for UI routing ------------------------------


def test_dtc_format_error_is_valueerror_subclass() -> None:
    assert issubclass(DTCFormatError, ValueError)


def test_dtc_format_error_str_contains_code_and_mode() -> None:
    exc = DTCFormatError("BAD123", "$03")
    msg = str(exc)
    assert "BAD123" in msg
    assert "$03" in msg
