"""T-VINA-5: the five WMIs that wmi.csv gave to the wrong make (F-C6-2), and the engine-map keys they share."""

import re
from pathlib import Path

import pytest

from vinlab import VINDecodeError

# The real VINs quoted in labs/vinlab/*.md|*.csv: the same corpus as audit/scratch/C6/c6_lib.py::real_vins.
LAB_DIR = Path(__file__).resolve().parents[2]
VIN_RE = re.compile(r"\b[A-HJ-NPR-Z0-9]{17}\b")

TRUE_MAKE_VINS = [
    ("WDB1290601F037844", "MERCEDES-BENZ"),  # R129 SL, real OPSI VIN (was "Maybach")
    ("KMHBF31SPMU250917", "HYUNDAI"),  # 1991 Sonata, real OPSI VIN (was "Genesis")
    ("JSAEAB35S00110744", "SUZUKI"),  # 1.3 Swift, real OPSI VIN (was "Kawasaki")
    ("JN1BCAN1480756536", "NISSAN"),  # 2008 Note 1.4, real OPSI VIN (was "Datsun")
    ("SAXXNNAZRWD148244", "ROVER"),  # 1998 Rover, real OPSI VIN (was "Sterling Motor Car")
]

# P3 (task T-VINA-5): decoded VINs per WMI, and engine-resolved VINs before the fix.
DECODED = {"WDB": 26, "KMH": 40, "JSA": 19, "JN1": 10, "SAX": 9}
RESOLVED_FLOOR = {"WDB": 25, "KMH": 40, "JSA": 19, "JN1": 8, "SAX": 9}

# Keys where the wrong-brand row and the right-brand row disagree; the winner is the Nio files 1+2 vote
# (tie -> right-brand row). Votes are (wrong-row code : right-row code).
CONFLICT_WINNERS = [
    ("WDB", "MERCEDES-BENZ", "20102", "102962"),  # wrong row, 28:7
    ("WDB", "MERCEDES-BENZ", "24523", "266.940"),  # right row, 42:213
    ("KMH", "HYUNDAI", "BT51H", "G4EA"),  # wrong row, 753:1
    ("KMH", "HYUNDAI", "VF21M", "G4DGL"),  # right row, tie 1:1
    ("JSA", "SUZUKI", "FTA03", "G16B"),  # wrong row, 172:2
    ("JSA", "SUZUKI", "EAK35", "G13BA310796"),  # right row, tie 1:1
    ("JN1", "NISSAN", "BCAN1", "GA14"),  # wrong row, 20:1
    ("JN1", "NISSAN", "BAAN1", "QG15"),  # right row, 56:61
    ("SAX", "ROVER", "XWYLM", "D16Z2"),  # wrong row, 7:1 (no key went to the right row)
]


def _real_vins(wmi: str) -> list[str]:
    vins: set[str] = set()
    for path in sorted(LAB_DIR.glob("*.md")) + sorted(LAB_DIR.glob("*.csv")):
        vins |= set(VIN_RE.findall(path.read_text(errors="ignore")))
    return sorted(v for v in vins if v.startswith(wmi))


@pytest.mark.parametrize("vin,make", TRUE_MAKE_VINS, ids=[v[:3] for v, _ in TRUE_MAKE_VINS])
def test_real_vin_decodes_true_make(decoder, vin, make):
    assert decoder.decode_vin_payload(vin).make == make


@pytest.mark.parametrize("wmi", sorted(DECODED))
def test_engine_resolved_not_below_base(decoder, wmi):
    decoded = resolved = 0
    for vin in _real_vins(wmi):
        try:
            dna = decoder.decode_vin_payload(vin)
        except VINDecodeError:
            continue
        decoded += 1
        row = decoder._resolve_engine(dna.vin, dna.make, [])
        if row and row.get("engine_code"):
            resolved += 1
    assert decoded == DECODED[wmi], f"{wmi}: decoded {decoded}, P3 {DECODED[wmi]}"
    assert resolved >= RESOLVED_FLOOR[wmi], f"{wmi}: resolved {resolved}/{decoded}, floor {RESOLVED_FLOOR[wmi]}"


@pytest.mark.parametrize(
    "wmi,brand,vds,engine_code", CONFLICT_WINNERS, ids=[f"{b}_{v}" for _, b, v, _ in CONFLICT_WINNERS]
)
def test_conflict_key_winner(decoder, wmi, brand, vds, engine_code):
    row = decoder._resolve_engine(f"{wmi}{vds}000000000", brand, [])
    assert row is not None
    assert row["engine_code"] == engine_code
