from __future__ import annotations

VALID_UNITS = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    """Process sensor readings and return a summary with alerts."""
    valid = _filter_valid(readings)
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": len(readings) - len(valid),
        "by_unit": _summarise_by_unit(valid),
        "alerts": _find_alerts(valid, threshold),
    }


# ---- validation ----

def _filter_valid(readings: list[dict]) -> list[dict]:
    return [r for r in readings if _is_valid_reading(r)]


def _is_valid_reading(reading: dict) -> bool:
    value = reading.get("value")
    unit = reading.get("unit", "raw")
    if value is None or value < 0:
        return False
    return unit in VALID_UNITS


# ---- alerts ----

def _find_alerts(readings: list[dict], threshold: float) -> list[dict]:
    return [
        {
            "sensor_id": r.get("sensor_id", "unknown"),
            "value": r["value"],
            "threshold": threshold,
        }
        for r in readings
        if r["value"] > threshold
    ]


# ---- unit aggregation ----

def _summarise_by_unit(readings: list[dict]) -> dict[str, dict]:
    groups = _group_by_unit(readings)
    return {unit: _describe(values) for unit, values in groups.items()}


def _group_by_unit(readings: list[dict]) -> dict[str, list[float]]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        groups.setdefault(r["unit"], []).append(r["value"])
    return groups


def _describe(values: list[float]) -> dict:
    return {
        "count": len(values),
        "avg": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
    }
