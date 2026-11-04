"""Tests for tools/extract_tecdoc_1q2019.py (T-VINA-13a).

Every test runs on a synthetic TecDoc 1Q2019 fixture under tmp_path: a fake
<root>/1Q2019/ with the 5 tables the tool reads and a minimal db.sql that
carries their real column lists. No test reads D:/.
"""

from __future__ import annotations

import csv
import importlib.util
import re
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "extract_tecdoc_1q2019.py"

COLUMNS = {
    "engines": [
        "id", "InternalID", "manufacturer", "SalesDescription", "HasLinkitem",
        "Description", "From", "To", "CanBeDisplayed",
    ],
    "manufacturers": [
        "id", "Matchcode", "IsVGL", "Description", "IsPassengerCar",
        "IsCommercialVehicle", "IsEngine", "IsMotorbike", "IsAxle",
        "IsTransporter", "IsCVManufacturerID", "CanBeDisplayed",
    ],
    "items_atributes": [
        "item_id", "AttributeGroup", "AttributeType", "DisplayTitle",
        "DisplayValue", "IsPassengerCar", "IsCommercialVehicle", "IsEngine",
        "IsMotorbike", "IsAxle", "IsTransporter", "IsCVManufacturerID",
        "HasLink", "IsValidForCurrentCountry", "ParentLinkitem",
        "LinkitemType", "CanBeDisplayed",
    ],
    "passengercars": [
        "id", "InternalID", "Model", "ManufacturerMatchcode", "ManufacturerId",
        "From", "To", "Description", "FullDescription", "CanBeDisplayed",
    ],
    "passengercars_link_engines": ["car_id", "engine_id"],
}

MANUFACTURERS = {"1": "RENAULT", "2": "BMW", "3": "KIA", "4": "VW", "6": "PEUGEOT"}

# engine id -> (manufacturer id, Description, attributes)
PETROL_NA = {
    "EngineType": "Petrol Engine",
    "Capacity": "1598 ccm",
    "NumberOfCylinders": "4",
    "FuelMixture": "Intake Manifold Injection/ Carburettor",
    "ChargeType": "Naturally Aspirated Engine",
    "EngineConstruction": "Straight",
    "CylinderConstruction": "DOHC",
}
ENGINES = {
    "10": ("1", "Z7W 712", {**PETROL_NA, "Capacity": "2849 ccm", "NumberOfCylinders": "6",
                            "EngineConstruction": "V", "CylinderConstruction": "SOHC/OHC",
                            "EmissionNorm": "Euro 2"}),
    "20": ("2", "M52 B20 (206S4)", {**PETROL_NA, "Capacity": "1991 ccm", "NumberOfCylinders": "6"}),
    "21": ("6", "106 (XN1)", dict(PETROL_NA)),
    "30": ("3", "G4FC", dict(PETROL_NA)),
    "40": ("4", "AXQ", {**PETROL_NA, "FuelMixture": "Direct Injection", "ChargeType": "Turbo/Intercooler"}),
    "50": ("1", "F4R 700", dict(PETROL_NA)),
    "51": ("1", "F4R 704", {**PETROL_NA, "Capacity": "1595 ccm"}),
    "52": ("1", "F2N 700", dict(PETROL_NA)),
    "53": ("1", "F2N 704", dict(PETROL_NA)),
    "54": ("1", "H4J 700", dict(PETROL_NA)),
    "55": ("1", "H4J 704", {k: v for k, v in PETROL_NA.items() if k != "ChargeType"}),
    "60": ("1", "K9K 700", {**PETROL_NA, "EngineType": "Diesel"}),
    "70": ("2", "N52 B30 A", dict(PETROL_NA)),
    "80": ("1", "D4F 712", dict(PETROL_NA)),
    "91": ("2", "M57", {**PETROL_NA, "EngineType": "Diesel"}),
    "92": ("2", "M57 X (EXX)", dict(PETROL_NA)),
}
SHORT_ROW_ENGINE = "80"  # written with 8 fields instead of 9

# car id -> (From, To); links car -> engine
CARS = {
    "100": ("2004-09-01", "0000-00-00"),
    "101": ("2006-03-01", "2011-06-01"),
    "102": ("1997-01-01", "2001-05-01"),
    "103": ("1999-01-01", "2003-08-01"),
}
LINKS = [("100", "70"), ("101", "70"), ("102", "10"), ("103", "10")]

MAP_HEADER = [
    "brand", "vds_full", "pos_8_only", "engine_code", "engine_displacement",
    "cylinder_count", "engine_configuration", "fuel_system_type", "majority_share",
]
MAP_ROWS = [
    ("RENAULT", "Z7W-712"),
    ("BMW", "N52B30A*"),
    ("HYUNDAI", "G4FC"),
    ("BMW", "206S4"),
    ("PEUGEOT", "106"),
    ("PEUGEOT", "XN1"),
    ("VOLKSWAGEN", "AXQ"),
    ("RENAULT", "F4R"),
    ("RENAULT", "F2N"),
    ("RENAULT", "K9K700"),
    ("BMW", "N52B30A"),
    ("RENAULT", "D4F712"),
    ("BMW", "M57"),
    ("BMW", "M52B20"),
    ("RENAULT", "H4J"),
]


def _write_tsv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        for row in rows:
            fh.write("\t".join(row) + "\r\n")


def _attr_row(item_id: str, attr_type: str, value: str) -> list[str]:
    row = dict.fromkeys(COLUMNS["items_atributes"], "0")
    row.update(item_id=item_id, AttributeGroup="Engine", AttributeType=attr_type,
               DisplayTitle=attr_type, DisplayValue=value, IsEngine="1",
               ParentLinkitem="0", LinkitemType="Engine")
    return [row[c] for c in COLUMNS["items_atributes"]]


def _write_map(path: Path, rows: list[tuple[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(MAP_HEADER)
        for brand, code in rows:
            writer.writerow([brand, "X", "", code, "", "", "", "", ""])


def _make_root(base: Path) -> Path:
    src = base / "1Q2019"
    (src / "install_database").mkdir(parents=True)
    ddl = []
    for table, cols in COLUMNS.items():
        body = ",\n".join(f"  `{c}` varchar(255) DEFAULT NULL" for c in cols)
        ddl.append(f"CREATE TABLE `{table}` (\n{body},\n  KEY `IX_{table}` (`{cols[0]}`)\n) ENGINE=InnoDB;\n")
    (src / "install_database" / "db.sql").write_text("\n".join(ddl), encoding="utf-8")
    _write_tsv(src / "manufacturers.csv", [
        [mid, name, "0", name, "1", "0", "1", "0", "0", "0", "0", "1"]
        for mid, name in MANUFACTURERS.items()
    ])
    engines = []
    for eid, (mid, desc, _attrs) in ENGINES.items():
        row = [eid, eid, mid, desc, "1", desc, "0000-00-00", "0000-00-00", "1"]
        engines.append(row[:-1] if eid == SHORT_ROW_ENGINE else row)
    _write_tsv(src / "engines.csv", engines)
    _write_tsv(src / "items_atributes.csv", [
        _attr_row(eid, t, v) for eid, (_m, _d, attrs) in ENGINES.items() for t, v in attrs.items()
    ])
    _write_tsv(src / "passengercars.csv", [
        [cid, cid, "1", "X", "1", frm, to, "car", "car", "1"] for cid, (frm, to) in CARS.items()
    ])
    _write_tsv(src / "passengercars_link_engines.csv", [list(link) for link in LINKS])
    return base


@pytest.fixture(scope="module")
def tool():
    spec = importlib.util.spec_from_file_location("extract_tecdoc_1q2019", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses resolves the module through sys.modules
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def run(tool, tmp_path, capsys):
    root = _make_root(tmp_path / "dbs")
    map_path = tmp_path / "map.csv"
    _write_map(map_path, MAP_ROWS)

    def _run(out_name: str = "out.csv", map_file: Path = map_path):
        out = tmp_path / out_name
        assert tool.main(["--dbs-root", str(root), "--map", str(map_file), "--out", str(out)]) == 0
        stdout = capsys.readouterr().out
        with out.open(encoding="utf-8", newline="") as fh:
            rows = {(r["brand"], r["engine_code"]): r for r in csv.DictReader(fh)}
        return rows, stdout, out

    return _run


def _no_row(stdout: str) -> dict[str, int]:
    m = re.search(r"^no_row other_manufacturer=(\d+) non_petrol=(\d+) no_code=(\d+)$", stdout, re.M)
    assert m, stdout
    return dict(zip(("other_manufacturer", "non_petrol", "no_code"), map(int, m.groups())))


def test_t0_exact_hit(run):
    rows, _, _ = run()
    row = rows[("RENAULT", "Z7W-712")]
    assert row["match_tier"] == "T0"
    assert row["status"] == "OK"
    assert row["tecdoc_engine_ids"] == "10"
    assert row["displacement_cc"] == "2849"
    assert row["is_v_engine"] == "1"
    assert row["valvetrain_type"] == "SOHC"
    assert row["euro_norm"] == "euro2"


def test_t1_paren_alias_hit_and_no_digit_head_key(run):
    rows, stdout, _ = run()
    row = rows[("BMW", "206S4")]
    assert row["match_tier"] == "T1"
    assert row["tecdoc_description"] == "M52 B20 (206S4)"
    assert rows[("PEUGEOT", "XN1")]["match_tier"] == "T1"
    # C1: the all-digit head token of `106 (XN1)` is not a key.
    assert ("PEUGEOT", "106") not in rows
    assert _no_row(stdout)["no_code"] == 2  # PEUGEOT 106 here, D4F712 (its row is skipped short)


def test_other_manufacturer_miss(run):
    rows, stdout, _ = run()
    assert ("HYUNDAI", "G4FC") not in rows
    assert _no_row(stdout)["other_manufacturer"] == 1


def test_alias_table_hit(run):
    rows, _, _ = run()
    row = rows[("VOLKSWAGEN", "AXQ")]
    assert row["match_tier"] == "T0A"
    assert row["fuel_delivery_type"] == "GDI"
    assert row["has_gdi"] == "1"
    assert row["induction_type"] == "TURBOCHARGED"
    assert row["has_turbo"] == "1"


def test_ambiguity_blanks_disagreeing_field_and_family(run):
    rows, _, _ = run()
    amb = rows[("RENAULT", "F4R")]
    assert amb["status"] == "AMBIGUOUS"
    assert amb["tecdoc_engine_ids"] == "50;51"
    assert amb["displacement_cc"] == ""
    assert amb["induction_type"] == "NATURALLY_ASPIRATED"
    fam = rows[("RENAULT", "F2N")]
    assert fam["status"] == "FAMILY"
    assert fam["displacement_cc"] == "1598"
    assert fam["tecdoc_description"] == "F2N 700;F2N 704"


def test_non_petrol_excluded(run):
    rows, stdout, _ = run()
    assert ("RENAULT", "K9K700") not in rows
    assert _no_row(stdout)["non_petrol"] == 2  # K9K700 here, M57 in the petrol-order test


def test_years_from_cars_with_open_end(run):
    rows, _, _ = run()
    open_end = rows[("BMW", "N52B30A")]
    assert (open_end["my_start"], open_end["my_end"], open_end["n_cars"]) == ("2004", "", "2")
    closed = rows[("RENAULT", "Z7W-712")]
    assert (closed["my_start"], closed["my_end"], closed["n_cars"]) == ("1997", "2003", "2")


def test_short_row_skipped_and_counted(run):
    rows, stdout, _ = run()
    assert ("RENAULT", "D4F712") not in rows
    assert re.search(r"^table engines: rows 15, skipped 1 \(field count != 9\)$", stdout, re.M), stdout
    assert re.search(r"^table manufacturers: rows 5, skipped 0 ", stdout, re.M), stdout


def test_deterministic(run, tmp_path):
    _, _, first = run("a.csv")
    _, _, second = run("b.csv")
    assert first.read_bytes() == second.read_bytes()
    reversed_map = tmp_path / "map_reversed.csv"
    _write_map(reversed_map, MAP_ROWS[::-1])
    _, _, third = run("c.csv", reversed_map)
    assert third.read_bytes() == first.read_bytes()
    lines = third.read_text(encoding="utf-8").splitlines()
    assert lines[1].startswith("BMW,206S4,T1,OK,20,")
    assert lines[-1].startswith("VOLKSWAGEN,AXQ,T0A,OK,40,")


def test_fold_matches_vinlab(tool):
    from vinlab.db.tecdoc_query import _normalise_code
    from vinlab.decoder import _fold_brand

    for raw in ("Citroën", "LAND ROVER", "Mercedes-Benz", "ŠKODA", "BMW I"):
        assert tool._fold_brand(raw) == _fold_brand(raw)
    for raw in ("N52B30A*", "z7w-712", "M52 B20 (206S4)"):
        assert tool._normalise_code(raw) == _normalise_code(raw)


def test_petrol_order_diesel_t0_blocks_petrol_t1(run):
    rows, stdout, _ = run()
    # T0 `M57` is diesel; T1 `M57 X (EXX)` is petrol. The tier is chosen first.
    assert ("BMW", "M57") not in rows
    assert _no_row(stdout)["non_petrol"] == 2


def test_t1_whole_part_before_parentheses_hit(run):
    rows, _, _ = run()
    # Correction 02 (a): `M52 B20 (206S4)` also yields the whole-part key `M52B20`.
    row = rows[("BMW", "M52B20")]
    assert row["match_tier"] == "T1"
    assert row["tecdoc_engine_ids"] == "20"


def test_ambiguity_blank_field_disagrees(run):
    rows, _, _ = run()
    # Correction 02 (b): engine 55 states no ChargeType, so the ids do not agree on induction.
    row = rows[("RENAULT", "H4J")]
    assert row["status"] == "AMBIGUOUS"
    assert row["tecdoc_engine_ids"] == "54;55"
    assert row["induction_type"] == ""
    assert row["has_turbo"] == ""
    assert row["displacement_cc"] == "1598"
