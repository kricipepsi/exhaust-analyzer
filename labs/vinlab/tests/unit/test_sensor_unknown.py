"""T-VINA-15: a vref row that stores neither air sensor (0/0) takes the decoder heuristic, as a NULL row does."""

import pytest

from vinlab.models import Emissions, FuelDeliveryType, InductionType


@pytest.mark.parametrize("vin", ["JF1BH9LJB2G051603", "JTDDR38T200058392"])
def test_real_vin_on_a_zero_zero_row_has_a_sensor(decoder, vin):
    # real VINs whose engine row stores has_maf=0, has_map=0 (MAP_ONLY with no sensor before T-VINA-15)
    arch = decoder.decode_vin_payload(vin).air_metering_architecture
    assert arch.has_maf_sensor or arch.has_map_sensor


@pytest.mark.parametrize("stored", [{"has_maf": 0, "has_map": 0}, {"has_maf": None, "has_map": None}, {}])
def test_zero_zero_equals_unknown(decoder, stored):
    emissions = Emissions()
    got = decoder._derive_air_metering(stored, FuelDeliveryType.PORT_INJECTION, InductionType.NATURALLY_ASPIRATED, emissions)
    want = decoder._derive_air_metering({}, FuelDeliveryType.PORT_INJECTION, InductionType.NATURALLY_ASPIRATED, emissions)
    assert got == want


@pytest.mark.parametrize("stored,maf,map_", [
    ({"has_maf": 1, "has_map": 0}, True, False),
    ({"has_maf": 0, "has_map": 1}, False, True),
    ({"has_maf": 1, "has_map": 1}, True, True),
    ({"has_maf": 0, "has_map": None}, False, False),  # one stated, one unknown: keep the stated 0
])
def test_a_stated_sensor_is_kept(decoder, stored, maf, map_):
    arch, _ = decoder._derive_air_metering(stored, FuelDeliveryType.PORT_INJECTION, InductionType.NATURALLY_ASPIRATED, Emissions())
    assert (arch.has_maf_sensor, arch.has_map_sensor) == (maf, map_)
