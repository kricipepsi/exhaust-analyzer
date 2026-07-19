from __future__ import annotations

import pytest
from legacy_processor import process_readings


class DescribeProcessReadings:
    def test_empty_readings(self) -> None:
        result = process_readings([], threshold=50.0)
        assert result["total_readings"] == 0
        assert result["valid_readings"] == 0

    def test_valid_readings(self) -> None:
        readings = [
            {"sensor_id": "S1", "value": 25.0, "unit": "C"},
            {"sensor_id": "S2", "value": 30.0, "unit": "C"},
        ]
        result = process_readings(readings, threshold=50.0)
        assert result["valid_readings"] == 2

    def test_invalid_none_value(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": None, "unit": "C"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_invalid_negative(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": -5.0, "unit": "C"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        result = process_readings(
            [{"sensor_id": "S1", "value": 10.0, "unit": "mph"}], threshold=50.0
        )
        assert result["invalid_readings"] == 1

    def test_alerts_flag_above_threshold(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 75.0, "unit": "C"},
            {"sensor_id": "B", "value": 40.0, "unit": "C"},
        ]
        result = process_readings(readings, threshold=60.0)
        assert len(result["alerts"]) == 1
        assert result["alerts"][0]["sensor_id"] == "A"

    def test_by_unit_aggregation(self) -> None:
        readings = [
            {"sensor_id": "S1", "value": 10.0, "unit": "V"},
            {"sensor_id": "S2", "value": 20.0, "unit": "V"},
        ]
        result = process_readings(readings, threshold=100.0)
        v = result["by_unit"]["V"]
        assert v["count"] == 2
        assert v["avg"] == 15.0
        assert v["min"] == 10.0
        assert v["max"] == 20.0
