# DTC Fault Mapping Reference

This document maps DTC codes to their corresponding failure modes for the
O2 sensor subsystem.

## Fault Table

| DTC Code | Description | Failure Mode |
|----------|-------------|--------------|
| P0131 | O2 Sensor Circuit Low Voltage | STUCK_LEAN |
| P0132 | O2 Sensor Circuit High Voltage | STUCK_RICH |
| P0133 | O2 Sensor Circuit Slow Response | sensor_response_degraded |

## Explicit KG Relationships

The DTC codes in the table above define the following fault mappings:

- **DTC P0131 maps to failure mode STUCK_LEAN.** When P0131 is set, the engine
  control module interprets this as a stuck-lean condition on the O2 sensor.

- **DTC P0132 maps to failure mode STUCK_RICH.** When P0132 is set, the engine
  control module interprets this as a stuck-rich condition on the O2 sensor.

- **DTC P0133 maps to failure mode sensor_response_degraded.** When P0133 is set,
  the engine control module interprets this as a degraded response time on the O2
  sensor.

- **DTC P0131 is associated with downstream O2 sensor validation.** When P0131 is
  set, the engine control module checks the downstream O2 sensor to confirm
  whether the lean condition is real or sensor-induced.

## Gate Enum Reference

The trim analytics gate `TrimAnalyticsGate.o2_fault_active` controls when this
O2 diagnostic runs. This same enum member is also spelled as
`TrimAnalyticsGate.O2_FAULT_ACTIVE` in some documentation sources. These two
spellings refer to the same enum member -- only the casing differs across
sources. The canonical name in the shipped enum is `o2_fault_active` (camelCase);
the `O2_FAULT_ACTIVE` (SCREAMING_SNAKE_CASE) form is an alternate casing found in
older documentation.

## Cross-Reference

This document's gate reference (`TrimAnalyticsGate.o2_fault_active`) links to the
enum defined in the Trim Analytics Configuration document
(`trim_analytics.md`). See that document for the full list of TrimAnalyticsGate
enum members and a known documentation bug.

## Diagnostic Flow

When P0131 is set, the engine control module checks the downstream O2 sensor
to confirm whether the lean condition is real or sensor-induced.
