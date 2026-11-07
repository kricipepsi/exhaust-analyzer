"""T-VINA-7b (F-C6-7): the check-digit bypass follows the ISO 3780 region (vin[0]), not the wmi.csv country text.

Tags: NEW fails on the base (country-text bypass); PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

# Real OPSI VINs the country-text rule rejected (blank country rows): ZAZ 1995 and Tata.
REAL_NON_NA = ["XTE110216S0313054", "MAT6002719PL01425"]


@pytest.mark.parametrize("vin", REAL_NON_NA)
def test_real_non_na_vin_skips_the_check_digit(decoder, vin):
    """NEW: a non-NA VIN whose wmi.csv country is blank passes the gate (it was 'checksum validation failed')."""
    assert decoder.validate_vin_checksum(vin) is True


def test_non_na_wmi_outside_the_country_sets_skips(decoder):
    """NEW: NM0 (filed as TURKEY, not in the country sets) with a wrong check digit passes on the region rule."""
    assert decoder.wmi_index["NM0"]["country"] == "TURKEY"
    vin = "NM0GE9F7?D1234567"
    wrong = next(d for d in "123456789" if d != _true_digit(vin.replace("?", "0")))
    assert decoder.validate_vin_checksum(vin.replace("?", wrong)) is True


def test_country_bypass_is_kept_for_na_plants_of_european_makers(decoder):
    """PIN: 1FA is filed as GERMANY; its wrong digit still passes (4JG/5UX/3VW registry VINs carry non-NHTSA digits).
    A US WMI filed as USA (1FM) with a wrong digit fails."""
    assert decoder.wmi_index["1FA"]["country"] == "GERMANY"
    assert decoder.validate_vin_checksum("1FAFP34P23W123456") is True
    assert decoder.wmi_index["1FM"]["country"] == "UNITED STATES (USA)"
    assert decoder.validate_vin_checksum("1FMFP34P13W123456") is False


_VALUES = {**{str(d): d for d in range(10)}, **dict(zip("ABCDEFGH", range(1, 9))), **dict(zip("JKLMN", range(1, 6))),
           "P": 7, "R": 9, **dict(zip("STUVWXYZ", range(2, 10)))}
_WEIGHTS = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)


def _true_digit(vin: str) -> str:
    """The NHTSA mod-11 check digit, computed here independently of the decoder."""
    r = sum(_VALUES[c] * w for c, w in zip(vin, _WEIGHTS)) % 11
    return "X" if r == 10 else str(r)


@pytest.mark.parametrize(("first", "checked"), [("1", True), ("5", True), ("6", False), ("J", False), ("W", False)])
def test_region_boundary(decoder, first, checked):
    """NEW for 6, J, W (WMIs 6HG/JHG/WHG are not in wmi.csv); PIN for 1HG (USA) and 5HG: a wrong check digit fails
    only in the North American codes 1-5."""
    vin = first + "HGCM826?3A004352"
    true = _true_digit(vin.replace("?", "0"))
    wrong = next(d for d in "123456789" if d != true)
    assert decoder.validate_vin_checksum(vin.replace("?", true)) is True
    assert decoder.validate_vin_checksum(vin.replace("?", wrong)) is (not checked)


def test_dummy_zero_on_na_vin_is_kept(decoder):
    """PIN: an NA VIN with '0' at position 9 passes (293 registry VINs: NA-built cars sold in Europe)."""
    assert decoder.validate_vin_checksum("1HGCM82603A004352") is True
