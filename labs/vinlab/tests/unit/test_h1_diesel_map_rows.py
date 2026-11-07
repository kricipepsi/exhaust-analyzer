"""H1 petrol guard on the shipped engine map (T-VINA-6, F-C6-5).

source: TecDoc 1Q2019 EngineType "Diesel" for every engine id of these 27 (brand, engine_code) keys, joined through the
T-VINA-13a extractor's tiers (C:/4DApp/recheck/T-VINA-6/nonpetrol.csv); wiki 10_decode_scope_rules.md section 10.4.
"""
import csv
from pathlib import Path

import pytest

from vinlab import decode
from vinlab.decoder import VINDecodeError

MAP = Path(__file__).resolve().parents[2] / "vinlab" / "data" / "vds_engine_map.csv"
DIESEL_KEYS = {
    ("BMW", "306D2"), ("BMW", "306D3"), ("BMW", "306D5"), ("BMW", "N47D20C"), ("CITROEN", "9HY"),
    ("HYUNDAI", "D4BH"), ("IVECO", "8140.43"), ("KIA", "D3FA"), ("KIA", "D4EA-F"), ("KIA", "D4FA"), ("KIA", "D4FB"),
    ("KIA", "D4FE"), ("KIA", "D4HA"), ("KIA", "D4HB"), ("KIA", "D4HC"), ("KIA", "J3"), ("MAZDA", "F6JA"),
    ("MAZDA", "R2"), ("MAZDA", "WL"), ("NISSAN", "ZD30"), ("PEUGEOT", "8140.43S"), ("PEUGEOT", "T8A"),
    ("TOYOTA", "1CD-FTV"), ("TOYOTA", "1KZ-TE"), ("VOLKSWAGEN", "ANJ"), ("VOLKSWAGEN", "JP"), ("VOLVO", "D4204T"),
}

ROWS_PER_KEY = {
    ("BMW", "306D2"): 1,
    ("BMW", "306D3"): 1,
    ("BMW", "306D5"): 1,
    ("BMW", "N47D20C"): 1,
    ("CITROEN", "9HY"): 1,
    ("HYUNDAI", "D4BH"): 1,
    ("IVECO", "8140.43"): 2,
    ("KIA", "D3FA"): 5,
    ("KIA", "D4EA-F"): 1,
    ("KIA", "D4FA"): 4,
    ("KIA", "D4FB"): 6,
    ("KIA", "D4FE"): 1,
    ("KIA", "D4HA"): 2,
    ("KIA", "D4HB"): 3,
    ("KIA", "D4HC"): 2,
    ("KIA", "J3"): 4,
    ("MAZDA", "F6JA"): 1,
    ("MAZDA", "R2"): 28,
    ("MAZDA", "WL"): 11,
    ("NISSAN", "ZD30"): 1,
    ("PEUGEOT", "8140.43S"): 1,
    ("PEUGEOT", "T8A"): 1,
    ("TOYOTA", "1CD-FTV"): 1,
    ("TOYOTA", "1KZ-TE"): 1,
    ("VOLKSWAGEN", "ANJ"): 1,
    ("VOLKSWAGEN", "JP"): 1,
    ("VOLVO", "D4204T"): 1,
}


def _rows() -> list[dict[str, str]]:
    with MAP.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_diesel_keys_carry_diesel() -> None:
    """NEW: all 84 rows of the 27 TecDoc-diesel keys say DIESEL; no other row does."""
    rows = _rows()
    hit = [r for r in rows if (r["brand"], r["engine_code"]) in DIESEL_KEYS]
    assert len(hit) == 84
    per_key: dict[tuple[str, str], int] = {}
    for r in hit:
        per_key[(r["brand"], r["engine_code"])] = per_key.get((r["brand"], r["engine_code"]), 0) + 1
    assert per_key == ROWS_PER_KEY
    assert {r["fuel_system_type"] for r in hit} == {"DIESEL"}
    assert sum(r["fuel_system_type"] == "DIESEL" for r in rows) == 84


@pytest.mark.parametrize("vin", [
    "WBA3E11009E123456",  # synthetic: VDS resolves to BMW N47D20C
    "JT111GJ9000023441",  # real registry VIN: Toyota 1KZ-TE
])
def test_diesel_vin_rejected_by_h1(vin: str) -> None:
    """NEW: a VIN whose VDS resolves to a TecDoc-diesel key is rejected (wiki 10.4)."""
    with pytest.raises(VINDecodeError, match="Fuel type out of scope"):
        decode(vin)


@pytest.mark.parametrize("vin", [
    "WBA4W9C5ZLYYYYYYY",  # BMW B58B30 (petrol), same brand as four diesel keys
    "WVWZZZ1KZAP012480",  # Volkswagen BSE (petrol), same brand as two diesel keys
])
def test_petrol_vin_still_decodes(vin: str) -> None:
    """NEW (revision 02): a petrol VIN of a brand with diesel keys still decodes."""
    assert decode(vin).make
