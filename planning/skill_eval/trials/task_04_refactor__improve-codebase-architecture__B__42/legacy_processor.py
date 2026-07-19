from __future__ import annotations

from typing import Any

_VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def process_readings(readings: list[dict[str, Any]], threshold: float = 100.0) -> dict[str, Any]:
    """Return a summary report for a batch of sensor readings.

    All processing logic lives behind this single public entry-point.
    """
    valid = [r for r in readings if _is_valid(r)]
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": len(readings) - len(valid),
        "by_unit": _unit_stats(valid),
        "alerts": _alerts(valid, threshold),
    }


# ---- internal: changing one rule touches exactly one function ----

def _is_valid(reading: dict[str, Any]) -> bool:
    value = reading.get("value")
    if value is None or not isinstance(value, (int, float)) or value < 0:
        return False
    return reading.get("unit", "raw") in _VALID_UNITS


def _alerts(readings: list[dict[str, Any]], threshold: float) -> list[dict[str, Any]]:
    return [
        {"sensor_id": r.get("sensor_id", "unknown"), "value": r["value"], "threshold": threshold}
        for r in readings
        if r["value"] > threshold
    ]


def _unit_stats(readings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        groups.setdefault(str(r["unit"]), []).append(float(r["value"]))
    return {
        unit: {
            "count": len(vals),
            "avg": sum(vals) / len(vals),
            "max": max(vals),
            "min": min(vals),
        }
        for unit, vals in groups.items()
    }
