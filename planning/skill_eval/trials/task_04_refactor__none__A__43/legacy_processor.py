from __future__ import annotations

VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(
    readings: list[dict],
    threshold: float = 100.0,
) -> dict:
    valid_count = 0
    invalid_count = 0
    by_unit: dict[str, list[float]] = {}
    alerts: list[dict] = []

    for reading in readings:
        sensor_id = reading.get("sensor_id", "unknown")
        value = reading.get("value")
        unit = reading.get("unit", "raw")

        if value is None or value < 0 or unit not in VALID_UNITS:
            invalid_count += 1
            continue

        valid_count += 1
        by_unit.setdefault(unit, []).append(value)

        if value > threshold:
            alerts.append({
                "sensor_id": sensor_id,
                "value": value,
                "threshold": threshold,
            })

    units_summary = {}
    for unit, values in by_unit.items():
        units_summary[unit] = {
            "count": len(values),
            "avg": sum(values) / len(values),
            "max": max(values),
            "min": min(values),
        }

    return {
        "total_readings": len(readings),
        "valid_readings": valid_count,
        "invalid_readings": invalid_count,
        "by_unit": units_summary,
        "alerts": alerts,
    }
