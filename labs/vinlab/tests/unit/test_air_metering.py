"""Tests for air_metering classification module — all 4 (has_maf, has_map) combinations."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from vinlab.overlay.air_metering import classify_air_metering


class TestClassifyAirMetering:
    def test_both_sensors(self) -> None:
        result = classify_air_metering(has_maf=True, has_map=True)
        assert result.primary_load_calculation == "HYBRID_MAF_MAP"
        assert result.strategy_label == "DUAL_MAF_MAP_CROSSCHECK"

    def test_maf_only(self) -> None:
        result = classify_air_metering(has_maf=True, has_map=False)
        assert result.primary_load_calculation == "MAF_ONLY"
        assert result.strategy_label == "MAF_ONLY"

    def test_map_only(self) -> None:
        result = classify_air_metering(has_maf=False, has_map=True)
        assert result.primary_load_calculation == "MAP_ONLY"
        assert result.strategy_label == "MAP_ONLY_SPEED_DENSITY"

    def test_neither_sensor(self) -> None:
        result = classify_air_metering(has_maf=False, has_map=False)
        assert result.primary_load_calculation == "MAP_ONLY"
        assert result.strategy_label == "MAP_ONLY_SPEED_DENSITY"

    def test_returns_frozen_dataclass(self) -> None:
        result = classify_air_metering(has_maf=True, has_map=True)
        with pytest.raises(FrozenInstanceError):
            result.primary_load_calculation = "MUTATED"  # pyright: ignore[reportAttributeAccessIssue]


class TestDecoderIntegration:
    def test_contract_round_trip_identical(self) -> None:
        from vinlab import decode

        dna = decode("VF1CB05CF25935016")
        j = dna.to_json_payload()
        assert "primary_load_calculation" in j["air_metering_architecture"]
        assert "air_metering_strategy" in j
        assert j["air_metering_strategy"] == dna.air_metering_strategy
        assert (
            j["air_metering_architecture"]["primary_load_calculation"]
            == dna.air_metering_architecture.primary_load_calculation
        )
