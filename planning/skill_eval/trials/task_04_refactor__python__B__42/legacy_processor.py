from __future__ import annotations

from dataclasses import dataclass, field

VALID_UNITS: frozenset[str] = frozenset({"C", "F", "Pa", "V", "A", "rpm", "pct"})


@dataclass
class SensorReading:
    sensor_id: str
    value: float | None
    unit: str


@dataclass
class UnitSummary:
    count: int
    avg: float
    max: float
    min: float


@dataclass
class ProcessReport:
    total_readings: int
    valid_readings: int
    invalid_readings: int
    by_unit: dict[str, UnitSummary] = field(default_factory=dict)
    alerts: list[AlertRecord] = field(default_factory=list)


@dataclass
class AlertRecord:
    sensor_id: str
    value: float
    threshold: float


def process_readings(
    readings: list[dict[str, object]],
    threshold: float = 100.0,
) -> dict[str, object]:
    """Process sensor readings and return a summary report.

    Validates each reading, aggregates values by unit, and flags readings
    that exceed *threshold* as alerts.
    """
    parsed = [_parse_reading(r) for r in readings]
    valid = [r for r in parsed if _is_valid(r)]
    invalid_count = len(parsed) - len(valid)
    by_unit = _aggregate_by_unit(valid)
    alerts = [
        AlertRecord(sensor_id=r.sensor_id, value=r.value, threshold=threshold)  # type: ignore[arg-type]
        for r in valid
        if r.value is not None and r.value > threshold
    ]
    return {
        "total_readings": len(readings),
        "valid_readings": len(valid),
        "invalid_readings": invalid_count,
        "by_unit": {u: s.__dict__ for u, s in by_unit.items()},
        "alerts": [a.__dict__ for a in alerts],
    }


def _parse_reading(raw: dict[str, object]) -> SensorReading:
    return SensorReading(
        sensor_id=str(raw.get("sensor_id", "unknown")),
        value=float(raw["value"]) if raw.get("value") is not None else None,
        unit=str(raw.get("unit", "raw")),
    )


def _is_valid(reading: SensorReading) -> bool:
    return (
        reading.value is not None
        and reading.value >= 0
        and reading.unit in VALID_UNITS
    )


def _aggregate_by_unit(readings: list[SensorReading]) -> dict[str, UnitSummary]:
    groups: dict[str, list[float]] = {}
    for r in readings:
        if r.value is not None:
            groups.setdefault(r.unit, []).append(r.value)
    return {
        unit: UnitSummary(
            count=len(values),
            avg=sum(values) / len(values),
            max=max(values),
            min=min(values),
        )
        for unit, values in groups.items()
    }
