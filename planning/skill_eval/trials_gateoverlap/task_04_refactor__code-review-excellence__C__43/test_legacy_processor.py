from __future__ import annotations

from legacy_processor import process_readings


def test_behaviour_preserved() -> None:
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S3", "value": None, "unit": "C"},
        {"sensor_id": "S4", "value": -5.0, "unit": "V"},
    ]
    out = process_readings(readings, threshold=50.0)
    assert out["valid_readings"] == 1
    assert out["invalid_readings"] == 2
    assert len(out["alerts"]) == 1
