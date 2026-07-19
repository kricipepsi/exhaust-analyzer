# DTC Fault Mapping Reference

## Canonical Entities

| Entity label | Entity type | Notes |
|--------------|-------------|-------|
| DTC P0131 | Diagnostic trouble code | O2 Sensor Circuit Low Voltage |
| DTC P0132 | Diagnostic trouble code | O2 Sensor Circuit High Voltage |
| DTC P0133 | Diagnostic trouble code | O2 Sensor Circuit Slow Response |
| FailureMode.STUCK_LEAN | Failure mode | Lean-condition sensor failure mode |
| FailureMode.STUCK_RICH | Failure mode | Rich-condition sensor failure mode |
| FailureMode.sensor_response_degraded | Failure mode | Slow or degraded O2 sensor response |
| O2 sensor subsystem | Vehicle subsystem | Subsystem covered by this DTC fault map |
| Downstream O2 sensor | Sensor | Sensor checked by the engine control module |
| Engine control module | Controller | Controller that validates DTC P0131 |
| TrimAnalyticsGate.O2_FAULT_ACTIVE | Trim analytics gate | Canonical gate label used by the shipped enum |
| TrimAnalyticsGate.o2_fault_active | Alias | Alias for TrimAnalyticsGate.O2_FAULT_ACTIVE found in migrated or older notes |

## Fault Table

| DTC code | Description | Failure mode |
|----------|-------------|--------------|
| DTC P0131 | O2 Sensor Circuit Low Voltage | FailureMode.STUCK_LEAN |
| DTC P0132 | O2 Sensor Circuit High Voltage | FailureMode.STUCK_RICH |
| DTC P0133 | O2 Sensor Circuit Slow Response | FailureMode.sensor_response_degraded |

## Explicit Relationships

- DTC P0131 maps_to_failure_mode FailureMode.STUCK_LEAN.
- DTC P0132 maps_to_failure_mode FailureMode.STUCK_RICH.
- DTC P0133 maps_to_failure_mode FailureMode.sensor_response_degraded.
- DTC P0131 belongs_to_subsystem O2 sensor subsystem.
- DTC P0132 belongs_to_subsystem O2 sensor subsystem.
- DTC P0133 belongs_to_subsystem O2 sensor subsystem.
- TrimAnalyticsGate.O2_FAULT_ACTIVE controls_diagnostic DTC P0131.
- TrimAnalyticsGate.O2_FAULT_ACTIVE controls_diagnostic DTC P0132.
- TrimAnalyticsGate.O2_FAULT_ACTIVE controls_diagnostic DTC P0133.
- TrimAnalyticsGate.o2_fault_active is_alias_of TrimAnalyticsGate.O2_FAULT_ACTIVE.
- DTC P0131 indicates_condition lean condition.
- Engine control module checks_sensor Downstream O2 sensor.
- Engine control module validates_condition lean condition.
- Downstream O2 sensor participates_in_subsystem O2 sensor subsystem.

## Diagnostic Flow

When DTC P0131 is set, the Engine control module checks the Downstream O2 sensor to confirm whether the lean condition is real or sensor-induced. The canonical gate label for this diagnostic relationship is TrimAnalyticsGate.O2_FAULT_ACTIVE.
