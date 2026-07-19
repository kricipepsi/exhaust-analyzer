# DTC Fault Mapping Reference

This document maps DTC codes to their corresponding failure modes for the
O2 sensor subsystem.

## Fault Table

| DTC Code | Description | Failure Mode |
|----------|-------------|--------------|
| P0131 | O2 Sensor Circuit Low Voltage | STUCK_LEAN |
| P0132 | O2 Sensor Circuit High Voltage | STUCK_RICH |
| P0133 | O2 Sensor Circuit Slow Response | sensor_response_degraded |

The P0131 code indicates the sensor is reading a lean condition. The trim
analytics gate `TrimAnalyticsGate.o2_fault_active` controls when this
diagnostic runs. Note that some older documentation spells this as
`TrimAnalyticsGate.O2_FAULT_ACTIVE` — the casing varies across sources.

## Diagnostic Flow

When P0131 is set, the engine control module checks the downstream O2 sensor
to confirm whether the lean condition is real or sensor-induced.

## Graph relations (explicit)

**P0131** MAPS_TO **STUCK_LEAN**
**P0132** MAPS_TO **STUCK_RICH**
**P0133** MAPS_TO **sensor_response_degraded**
**P0131** GATED_BY **TrimAnalyticsGate.O2_FAULT_ACTIVE**
