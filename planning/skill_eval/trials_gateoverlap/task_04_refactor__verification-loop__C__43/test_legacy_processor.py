from legacy_processor import process_readings


def test_empty():
    out = process_readings([], threshold=50.0)
    assert out["total_readings"] == 0
