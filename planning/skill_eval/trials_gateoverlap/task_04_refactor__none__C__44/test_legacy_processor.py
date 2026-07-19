from legacy_processor import process_readings


def test_counts():
    readings = [
        {"sensor_id": "S1", "value": 75.0, "unit": "C"},
        {"sensor_id": "S2", "value": None, "unit": "C"},
    ]
    out = process_readings(readings, threshold=50.0)
    assert out["total_readings"] == 2
