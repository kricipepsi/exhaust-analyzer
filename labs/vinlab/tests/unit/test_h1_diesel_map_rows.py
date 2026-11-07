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


def _rows() -> list[dict[str, str]]:
    with MAP.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def test_diesel_keys_carry_diesel() -> None:
    """NEW: all 84 rows of the 27 TecDoc-diesel keys say DIESEL; no other row does."""
    rows = _rows()
    hit = [r for r in rows if (r["brand"], r["engine_code"]) in DIESEL_KEYS]
    assert len(hit) == 84
    assert {r["fuel_system_type"] for r in hit} == {"DIESEL"}
    assert sum(r["fuel_system_type"] == "DIESEL" for r in rows) == 84


def test_diesel_vin_rejected_by_h1() -> None:
    """NEW: a VIN whose VDS resolves to BMW N47D20C is rejected (wiki 10.4)."""
    with pytest.raises(VINDecodeError, match="Fuel type out of scope"):
        decode("WBA3E11009E123456")
