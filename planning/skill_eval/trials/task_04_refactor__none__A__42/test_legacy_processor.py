from __future__ import annotations

import pytest
from legacy_processor import process_readings


def test_empty_list() -> None:
    result = process_readings([], threshold=50.0)
    assert result["total_readings"] == 0
    assert result["valid_readings"] == 0
    assert result["invalid_readings"] == 0


def test_valid_readings() -> None:
    readings = [
        {"sensor_id": "S1", "value": 25.0, "unit": "C"},
        {"sensor_id": "S2", "value": 30.0, "unit": "C"},
    ]
    result = process_readings(readings, threshold=50.0)
    assert result["valid_readings"] == 2
    assert result["invalid_readings"] == 0


def test_invalid_readings() -> None:
    readings = [
        {"sensor_id": "S1", "value": None, "unit": "C"},
        {"sensor_id": "S2", "value": -5.0, "unit": "C"},
        {"sensor_id": "S3", "value": 10.0, "unit": "mph"},
    ]
    result = process_readings(readings, threshold=50.0)
    assert result["invalid_readings"] == 3


def test_alerts() -> None:
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S2", "value": 50.0, "unit": "F"},
    ]
    result = process_readings(readings, threshold=60.0)
    assert len(result["alerts"]) == 1
    assert result["alerts"][0]["sensor_id"] == "S1"


def test_by_unit_aggregation() -> None:
    readings = [
        {"sensor_id": "S1", "value": 10.0, "unit": "V"},
        {"sensor_id": "S2", "value": 20.0, "unit": "V"},
    ]
    result = process_readings(readings, threshold=100.0)
    assert result["by_unit"]["V"]["count"] == 2
    assert result["by_unit"]["V"]["avg"] == 15.0
    assert result["by_unit"]["V"]["min"] == 10.0
    assert result["by_unit"]["V"]["max"] == 20.0
