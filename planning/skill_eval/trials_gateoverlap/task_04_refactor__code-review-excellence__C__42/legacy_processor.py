from __future__ import annotations

_VALID_UNITS = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


def _is_valid(value: float | None, unit: str) -> bool:
    """Return True when a reading is non-null, non-negative and a known unit."""
    if value is None:
        return False
    if value < 0:
        return False
    return unit in _VALID_UNITS


def _summarize_unit(values: list[float]) -> dict[str, float | int]:
    """Return count/avg/max/min for one unit's readings."""
    return {
        "count": len(values),
        "avg": sum(values) / len(values),
        "max": max(values),
        "min": min(values),
    }


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    """Summarise sensor *readings*, flagging values above *threshold*.

    Preserves the original behaviour: invalid = null/negative/unknown-unit.
    """
    valid = 0
    invalid = 0
    by_unit: dict[str, list[float]] = {}
    alerts: list[dict] = []
    for reading in readings:
        value = reading.get("value")
        unit = reading.get("unit", "raw")
        if not _is_valid(value, unit):
            invalid += 1
            continue
        valid += 1
        by_unit.setdefault(unit, []).append(value)
        if value > threshold:
            alerts.append(
                {"sensor_id": reading.get("sensor_id", "unknown"),
                 "value": value, "threshold": threshold}
            )
    summary = {unit: _summarize_unit(values) for unit, values in by_unit.items()}
    return {
        "total_readings": len(readings),
        "valid_readings": valid,
        "invalid_readings": invalid,
        "by_unit": summary,
        "alerts": alerts,
    }
