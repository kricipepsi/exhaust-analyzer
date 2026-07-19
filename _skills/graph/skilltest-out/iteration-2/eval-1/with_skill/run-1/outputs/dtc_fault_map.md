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
`TrimAnalyticsGate.O2_FAULT_ACTIVE` - the casing varies across sources.

## Diagnostic Flow

When P0131 is set, the engine control module checks the downstream O2 sensor
to confirm whether the lean condition is real or sensor-induced.


## Graph relations (explicit)

**P0131** maps_to **STUCK_LEAN**
**P0132** maps_to **STUCK_RICH**
**P0133** maps_to **SENSOR_RESPONSE_DEGRADED**
**P0131 diagnostic** gated_by **TrimAnalyticsGate.O2_FAULT_ACTIVE**
**P0131 diagnostic** confirmed_by **downstream O2 sensor**
**TrimAnalyticsGate.O2_FAULT_ACTIVE** controls **P0131 diagnostic**

## Core Entities

- **P0131** - DTC code; consumer: O2 sensor diagnostic flow.
- **P0132** - DTC code; consumer: O2 sensor diagnostic reference.
- **P0133** - DTC code; consumer: O2 sensor diagnostic reference.
- **STUCK_LEAN** - failure mode; consumer: DTC fault mapping.
- **STUCK_RICH** - failure mode; consumer: DTC fault mapping.
- **SENSOR_RESPONSE_DEGRADED** - failure mode; consumer: DTC fault mapping.
- **TrimAnalyticsGate.O2_FAULT_ACTIVE** - canonical gate label for O2 fault diagnostics; consumer: trim analytics diagnostic gating.
- **downstream O2 sensor** - diagnostic confirmation signal; consumer: P0131 diagnostic flow.