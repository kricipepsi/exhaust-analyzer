"""T-VINA-1: the model year is read within the 1990-2010 scope (F-C6-3, F-C6-8)."""
from __future__ import annotations

import pytest
from vinlab.decoder import _YEAR_MAX, _YEAR_MIN, VINDecodeError


def test_scope_is_1990_to_2010():
    assert (_YEAR_MIN, _YEAR_MAX) == (1990, 2010)


@pytest.mark.parametrize("vin", ["101ZZZZZZLZZZZZZZ", "102ZZZZZZLZZZZZZZ"])
def test_l_is_1990_for_every_era_hint(decoder, vin):
    assert decoder.decode_vin_payload(vin).model_year == 1990


@pytest.mark.parametrize("code,year", [("Y", 2000), ("1", 2001), ("9", 2009), ("A", 2010)])
def test_scope_edges_decode(decoder, code, year):
    assert decoder.decode_vin_payload(f"102ZZZZZZ{code}ZZZZZZZ").model_year == year


@pytest.mark.parametrize("code", list("BCDEFGHJK"))
def test_codes_after_2010_are_out_of_scope(decoder, code):
    with pytest.raises(VINDecodeError, match="1990-2010"):
        decoder.decode_vin_payload(f"102ZZZZZZ{code}ZZZZZZZ")


def test_l_is_1990_whatever_the_row_order(decoder, monkeypatch):
    reversed_rows = list(reversed(decoder.year_index["L"]))
    assert [r["calendar_year"] for r in reversed_rows] == ["2020", "1990"]
    monkeypatch.setitem(decoder.year_index, "L", reversed_rows)
    assert decoder.decode_vin_payload("102ZZZZZZLZZZZZZZ").model_year == 1990
