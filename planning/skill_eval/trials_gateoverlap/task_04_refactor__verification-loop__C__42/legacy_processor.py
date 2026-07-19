from __future__ import annotations

_VALID_UNITS = ["C", "F", "Pa", "V", "A", "rpm", "pct"]


def process_readings(readings: list[dict], threshold: float = 100.0) -> dict:
    valid = 0
    invalid = 0
    by_unit: dict[str, list[float]] = {}
    alerts = []
    for reading in readings:
        value = reading.get("value")
        unit = reading.get("unit", "raw")
        try:
            if value is None or value < 0 or unit not in _VALID_UNITS:
                invalid += 1
                continue
        except:                      # BUG: bare except survives single shot
            invalid += 1
            continue
        valid += 1
        by_unit.setdefault(unit, []).append(value)
        if value > threshold:
            alerts.append({"sensor_id": reading.get("sensor_id", "unknown"),
                           "value": value, "threshold": threshold})
    summary = {u: {"count": len(v), "avg": sum(v) / len(v), "max": max(v), "min": min(v)}
               for u, v in by_unit.items()}
    return {"total_readings": len(readings), "valid_readings": valid,
            "invalid_readings": invalid, "by_unit": summary, "alerts": alerts}
