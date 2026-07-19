"""Shared fixtures for VINLab tests."""

from __future__ import annotations

import csv
import shutil
import sqlite3
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from vinlab.models import Horizon
from vinlab.decoder import RobustVINDecoder

DATA_DIR = Path(__file__).parent.parent / "vinlab" / "data"
MINI_DATA_SOURCE = Path(__file__).parent / "fixtures" / "mini_data"
SPECIMENS_CSV = (
    Path(__file__).parent.parent.parent.parent.parent.parent
    / "vehicle-data"
    / "petrol_vin"
    / "vehicles_petrol_specimens.csv"
)


def _data_available() -> bool:
    """Check that all required data files exist."""
    required = ["wmi.csv", "vds_engine_map.csv", "years.csv", "vref.db"]
    return all((DATA_DIR / f).exists() for f in required)


@pytest.fixture(scope="session")
def data_dir() -> Path:
    """Path to vinlab/data/. Skip all tests if data files are missing."""
    if not _data_available():
        pytest.skip("vinlab/data/ files not populated — run build scripts first")
    return DATA_DIR


@pytest.fixture(scope="session")
def decoder(data_dir: Path) -> RobustVINDecoder:
    """Module-scoped decoder instance loaded once per test session."""
    return RobustVINDecoder(data_dir)


CSV_CASES_PATH = Path(__file__).parent.parent.parent.parent.parent.parent / \
    "cases" / "csv" / "cases_petrol_master_v6.csv"
# Resolves to: C:\Users\muto\claude\4DApp\cases\csv\cases_petrol_master_v6.csv
# from labs/vinlab root: 4DApp/4DLab/4DLabV2/labs/vinlab/tests/conftest.py
#   → ../../../../../../cases/csv/... = 6 parent hops (v2 is one level deeper than v1)


@pytest.fixture(scope="session")
def csv_cases() -> list[dict]:
    """All rows from cases_petrol_master_v6.csv as list of dicts.

    Skips if the CSV is not found (e.g., CI without the cases folder).
    """
    if not CSV_CASES_PATH.exists():
        pytest.skip(f"CSV not found: {CSV_CASES_PATH}")
    with CSV_CASES_PATH.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture(scope="session")
def sample_vins() -> list[str]:
    """Up to 20 distinct VINs from vehicles_petrol_specimens.csv with non-empty engine_code."""
    if not SPECIMENS_CSV.exists():
        return []
    vins: list[str] = []
    with SPECIMENS_CSV.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter=";"):
            vin = row.get("E_VIN", "").strip()
            engine_code = row.get("P15_engine_code", "").strip()
            if vin and engine_code and len(vin) == 17:
                vins.append(vin)
                if len(vins) >= 20:
                    break
    return vins


def _build_mini_data_dir(tmp_path: Path) -> Path:
    """Build a controlled VINLab data_dir from checked-in mini fixture sources."""
    out = tmp_path / "mini_data"
    shutil.copytree(MINI_DATA_SOURCE, out)
    db_path = out / "vref.db"
    seed_sql = (out / "seed.sql").read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(seed_sql)
    return out


@pytest.fixture
def make_mini_data_dir() -> Callable[[Path], Path]:
    return _build_mini_data_dir


@pytest.fixture
def mini_data_dir(tmp_path: Path, make_mini_data_dir: Callable[[Path], Path]) -> Path:
    return make_mini_data_dir(tmp_path)


@pytest.fixture
def make_stress_profile() -> Callable[..., dict[str, Any]]:
    def _builder(**overrides: object) -> dict[str, Any]:
        profile: dict[str, Any] = {
            "euro": "EURO_3",
            "induction": "NATURALLY_ASPIRATED",
            "fuel_delivery": "PORT_INJECTION",
            "displacement": 1.6,
            "horizon": Horizon.ADAPTIVE,
        }
        profile.update(overrides)
        return profile

    return _builder


@pytest.fixture
def make_switch_profile() -> Callable[..., dict[str, Any]]:
    def _builder(**overrides: object) -> dict[str, Any]:
        profile: dict[str, Any] = {
            "year": 2000,
            "fuel_delivery": "PORT_INJECTION",
            "o2_type_hint": "",
        }
        profile.update(overrides)
        return profile

    return _builder
