from __future__ import annotations

import pytest
from legacy_processor import process_readings


class TestProcessReadings:
    def test_empty(self) -> None:
        r = process_readings([])
        assert r["total_readings"] == 0

    def test_all_valid(self) -> None:
        readings = [{"sensor_id": "A", "value": 10.0, "unit": "C"}]
        r = process_readings(readings, threshold=100.0)
        assert r["valid_readings"] == 1
        assert r["invalid_readings"] == 0

    def test_invalid_none(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": None, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_negative(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": -1.0, "unit": "C"}])
        assert r["invalid_readings"] == 1

    def test_invalid_unit(self) -> None:
        r = process_readings([{"sensor_id": "A", "value": 1.0, "unit": "X"}])
        assert r["invalid_readings"] == 1

    def test_alerts(self) -> None:
        readings = [
            {"sensor_id": "A", "value": 90.0, "unit": "C"},
            {"sensor_id": "B", "value": 20.0, "unit": "C"},
        ]
        r = process_readings(readings, threshold=50.0)
        assert len(r["alerts"]) == 1
        assert r["alerts"][0]["sensor_id"] == "A"

    def test_by_unit(self) -> None:
        readings = [
            {"sensor_id": "X", "value": 10.0, "unit": "V"},
            {"sensor_id": "Y", "value": 30.0, "unit": "V"},
        ]
        r = process_readings(readings, threshold=100.0)
        assert r["by_unit"]["V"]["count"] == 2
        assert r["by_unit"]["V"]["avg"] == 20.0
