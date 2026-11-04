"""T-VINA-2: Mercedes-Benz and smart VINs with a numeric type code carry no year at position 10."""

import pytest

TYPE_CODE_VINS = [
    "WDB1240261A102470",  # W124, type 124.026
    "WDD1690321J749046",  # W169, type 169.032
    "WDD1770441J098476",  # W177, type 177.044
    "VSA63823413020157",  # Vito W638 (Spain), T-VINA-17
    "WDF63981313372460",  # Vito/Viano W639, registered 2008, T-VINA-17
    "WMX1903771A004607",  # AMG GT C190, registered 2016, T-VINA-17
    "4JG1631541A010177",  # ML W163, European form, registered 1998, T-VINA-17
    "VDB2010181F956777",  # W201, registered 1993, T-VINA-17
]

NORTH_AMERICAN_VINS = [
    ("WDBED30DXLB097097", 1990),  # letters at 4-9: the year code L
    ("WDBSK74F75F093354", 2005),  # the year code 5
    ("WME01MC011H080963", 2001),  # smart, letters at 4-9: the year code 1
    ("4JGBF71EX7A107518", 2007),  # US-built ML, letters at 4-9: the year code 7, T-VINA-17
]


@pytest.mark.parametrize("vin", TYPE_CODE_VINS)
def test_type_code_vin_has_no_year(decoder, vin):
    assert decoder.decode_vin_payload(vin).model_year is None


@pytest.mark.parametrize("vin,year", NORTH_AMERICAN_VINS)
def test_north_american_form_keeps_the_year(decoder, vin, year):
    assert decoder.decode_vin_payload(vin).model_year == year


def test_other_wmis_keep_position_10(decoder):
    # VF1CB05CF25935016: Renault, year code 2 (out of this row: Renault is not in the type-code set)
    assert decoder.decode_vin_payload("VF1CB05CF25935016").model_year == 2002


def test_type_code_set_is_the_measured_one():
    from vinlab.decoder import _TYPE_CODE_WMIS

    assert _TYPE_CODE_WMIS == frozenset(
        {"WDB", "WDC", "WDD", "WME", "W1K", "W1N", "VSA", "WDF", "WMX", "4JG", "VDB"}
    )


def test_numeric_positions_outside_the_set_keep_the_year(decoder):
    # VF1 is not in the set, so digits at 4-9 do not suppress the year: code 2 is 2002
    assert decoder._resolve_year("VF11234562A123456", {})[0] == 2002
