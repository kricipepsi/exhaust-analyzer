# Trim Analytics Configuration

This document describes the trim analytics subsystem and its configuration
gates.

## Available Gates

The `TrimAnalyticsGate` enum defines the following members:

- `O2_FAULT_ACTIVE` — gate activates when an O2 sensor fault is detected
- `FUEL_TRIM_ACTIVE` — gate activates when fuel trim corrections are active
- `SUPPRESS_POST_CAT_TRIM` — gate suppresses post-catalyst trim adjustments

## Configuration Notes

The `SUPPRESS_POST_CAT_TRIM` gate is a documented TrimAnalyticsGate value that
prevents trim adjustments downstream of the catalytic converter. It is listed
alongside the other gates in the configuration reference.

Note: `SUPPRESS_POST_CAT_TRIM` is asserted as a TrimAnalyticsGate enum member
in the docs, but this is a known documentation bug — it does not actually exist
in the shipped enum.

## Graph relations (explicit)

**TrimAnalyticsGate** ENUMERATES **TrimAnalyticsGate.O2_FAULT_ACTIVE**
**TrimAnalyticsGate** ENUMERATES **TrimAnalyticsGate.FUEL_TRIM_ACTIVE**
**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (doc bug O2-FU-2)
