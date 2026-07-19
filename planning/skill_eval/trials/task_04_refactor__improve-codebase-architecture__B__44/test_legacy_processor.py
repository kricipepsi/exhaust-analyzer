from __future__ import annotations

import pytest
from legacy_processor import process_readings


class TestProcessReadings:
    def test_empty(self) -> None:
        r = process_readings([])
        assert r["total_readings"] == 0

    def test_valid(self) -> None:
        readings = [{"sensor_id": "S", "value": 1.0, "unit": "C"}]
        r = process_readings(readings)
        assert r["valid_readings"] == 1

    def test_invalid_none(self) -> None:
        r = process_readings([{"sensor_id": "S", "value": None, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        r = process_readings([{"sensor_id": "S", "value": 1.0, "unit": "mph"}])
        assert r["invalid_readings"] == 1

    def test_alerts(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 80.0, "unit": "C"},
            {"sensor_id": "B", "value": 10.0, "unit": "C"},
        ]
        r = process_readings(readings, threshold=50.0)
        assert len(r["alerts"]) == 1

    def test_unit_aggregation(self) -> None:
        readings = [
            {"sensor_id": "X", "value": 10.0, "unit": "V"},
            {"sensor_id": "Y", "value": 30.0, "unit": "V"},
        ]
        r = process_readings(readings, threshold=100.0)
        assert r["by_unit"]["V"]["count"] == 2
