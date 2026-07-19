"""Decoder isolation tests using controlled lab-local mini data."""

from __future__ import annotations

from collections.abc import Callable, Generator
from pathlib import Path

import pytest

from vinlab import _get_decoder, decode


@pytest.fixture(autouse=True)
def _clear_decoder_cache() -> Generator[None]:
    yield
    _get_decoder.cache_clear()


def test_same_mini_data_dir_returns_cached_instance(mini_data_dir: Path) -> None:
    d1 = _get_decoder(mini_data_dir)
    d2 = _get_decoder(mini_data_dir)

    assert d1 is d2


def test_different_mini_data_dirs_return_independent_instances(
    tmp_path: Path,
    make_mini_data_dir: Callable[[Path], Path],
) -> None:
    d1 = _get_decoder(make_mini_data_dir(tmp_path / "one"))
    d2 = _get_decoder(make_mini_data_dir(tmp_path / "two"))

    assert d1 is not d2


def test_decode_uses_mini_data_dir_without_packaged_data(mini_data_dir: Path) -> None:
    dna = decode("VF1CB05CF25935016", data_dir=mini_data_dir)

    assert dna.vin == "VF1CB05CF25935016"
    assert dna.make == "Renault"
    assert dna.model_year == 2002  # source: mini_data/years.csv row year_code=2.
    assert dna.engine_displacement_liters == 1.149  # source: mini_data/seed.sql D4F row.
    assert dna.cylinder_count == 4  # source: mini_data/vds_engine_map.csv D4F row.
    assert dna.fuel_delivery_type == "PORT_INJECTION"
    assert dna.induction_type == "NATURALLY_ASPIRATED"
    assert dna.euro_emission_category == "EURO_4"
    assert dna.resolved_horizon == "HORIZON_ADAPTIVE"
    assert dna.stress_idle_rpm_target == 3500  # characterization: adaptive fallback branch.
    assert dna.emissions.upstream_o2_type == "WIDEBAND_AFR"
    assert dna.air_metering_strategy == "MAF_ONLY"
    assert dna.rated_rpm == 5500  # source: mini_data/seed.sql D4F row.
    assert dna.confidence == "HIGH"
