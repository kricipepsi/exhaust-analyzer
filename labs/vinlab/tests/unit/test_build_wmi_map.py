"""T-VINA-12 R3: build_wmi_map picks among several vPIC makes by the registry majority (in-memory inputs only)."""

import csv
import importlib.util
import sqlite3
import sys
from pathlib import Path

import pytest

TOOL = Path(__file__).resolve().parents[2] / "tools" / "build_wmi_map.py"


@pytest.fixture
def tool(monkeypatch, tmp_path):
    # The module refuses to import without VEHICLE_DATA_ROOT (its default petrol CSV lives there).
    monkeypatch.setenv("VEHICLE_DATA_ROOT", str(tmp_path))
    spec = importlib.util.spec_from_file_location("build_wmi_map", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


def _vpic_db(path: Path, wmi_makes: dict[str, list[str]]) -> Path:
    """A minimal vPIC file: the four tables _load_vpic_wmis joins, makes inserted in the given order."""
    conn = sqlite3.connect(str(path))
    conn.executescript(
        "CREATE TABLE Wmi (Id INTEGER PRIMARY KEY, Wmi TEXT, CountryId INTEGER);"
        "CREATE TABLE Wmi_Make (WmiId INTEGER, MakeId INTEGER);"
        "CREATE TABLE Make (Id INTEGER PRIMARY KEY, Name TEXT);"
        "CREATE TABLE Country (Id INTEGER PRIMARY KEY, Name TEXT);"
        "INSERT INTO Country VALUES (1, 'JAPAN');"
    )
    make_ids: dict[str, int] = {}
    for wmi_id, (wmi, makes) in enumerate(wmi_makes.items(), start=1):
        conn.execute("INSERT INTO Wmi VALUES (?, ?, 1)", (wmi_id, wmi))
        for make in makes:
            if make not in make_ids:
                make_ids[make] = len(make_ids) + 1
                conn.execute("INSERT INTO Make VALUES (?, ?)", (make_ids[make], make))
            conn.execute("INSERT INTO Wmi_Make VALUES (?, ?)", (wmi_id, make_ids[make]))
    conn.commit()
    conn.close()
    return path


@pytest.mark.parametrize(
    "makes,registry,expected",
    [
        (["Toyota", "Subaru"], "TOYOTA", "Toyota"),  # JTM: the last make was Subaru
        (["Dodge", "Jeep", "Fiat", "Ram"], "JEEP", "Jeep"),  # ZAC: the last make was Ram
        (["Mercedes-Benz", "Smart"], "MERCEDES BENZ", "Mercedes-Benz"),  # folded names compare equal
    ],
    ids=["Toyota", "Jeep", "Mercedes-Benz"],
)
def test_pick_registry_majority_wins(tool, makes, registry, expected):
    assert tool._pick_vpic_make(makes, registry) == expected


@pytest.mark.parametrize("registry", [None, "KIA"], ids=["no_majority", "majority_not_in_vpic"])
def test_pick_without_majority_keeps_last(tool, registry):
    assert tool._pick_vpic_make(["Toyota", "Lexus", "Subaru"], registry) == "Subaru"


def test_pick_empty_makes(tool):
    assert tool._pick_vpic_make([], "TOYOTA") == ""


def test_load_vpic_wmis_uses_registry_majority(tool, tmp_path):
    db = _vpic_db(tmp_path / "vpic.db", {"JTM": ["Toyota", "Subaru"], "JTE": ["Subaru", "Toyota"]})
    got = tool._load_vpic_wmis(db, {"JTM": "TOYOTA", "JTE": "TOYOTA"})
    assert got["JTM"]["brand"] == "Toyota"
    assert got["JTE"]["brand"] == "Toyota"
    assert got["JTM"]["country"] == "JAPAN"


def test_registry_majority_counts_petrol_vins(tool, tmp_path):
    lines = [
        "E-VIN;D1-Znamka;P13-Vrsta goriva (oznaka)",
        "JTMBD31V005157989;TOYOTA;P",
        "JTMBD31V005157990;TOYOTA;P",
        "JTMBD31V005157991;SUBARU;P",
        "JTMBD31V005157992;SUBARU;D",  # diesel: not counted
        "JTMBD31V005157993;SUBARU;D",
        "JTMBD31V00515799;SUBARU;P",  # 16 characters: not counted
        "JTMBD31V00515798;SUBARU;P",  # 16 characters: not counted (without the filter SUBARU wins 3:2)
        "TMBBD41Z072000001;ŠKODA;P",  # written as the cp1250 byte 0x8A
    ]
    path = tmp_path / "Nio_vozila_1.csv"
    # 0x98 has no cp1250 character: 3 rows read as U+FFFD brands, which must not win JTM
    undefined = b"\r\n".join(b"JTMBD31V00515799%d;\x98\x98;P" % i for i in (4, 5, 6))
    path.write_bytes("\r\n".join(lines).encode("cp1250") + b"\r\n" + undefined)
    assert tool._registry_majority([path]) == {"JTM": "TOYOTA", "TMB": "ŠKODA"}


def test_build_writes_registry_majority_brand(tool, tmp_path):
    db = _vpic_db(tmp_path / "vpic.db", {"JTM": ["Toyota", "Subaru"]})
    petrol = tmp_path / "petrol.csv"
    petrol.write_text("E_VIN;B_first_reg_date\nJTMBD31V005157989;01.03.2005\n", encoding="utf-8")
    out = tmp_path / "wmi.csv"
    assert tool.build(out, db, petrol, registry_make={"JTM": "TOYOTA"}) == 1
    with out.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows == [{"wmi": "JTM", "brand": "Toyota", "country": "JAPAN", "era_hint": "modern"}]
