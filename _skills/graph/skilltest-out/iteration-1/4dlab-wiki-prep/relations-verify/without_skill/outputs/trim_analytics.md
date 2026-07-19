# Trim Analytics Configuration

This document describes the trim analytics subsystem and its configuration
gates.

## Available Gates

The `TrimAnalyticsGate` enum defines the following members:

- `O2_FAULT_ACTIVE` -- gate activates when an O2 sensor fault is detected
- `FUEL_TRIM_ACTIVE` -- gate activates when fuel trim corrections are active

## Explicit KG Relationships

- **TrimAnalyticsGate.O2_FAULT_ACTIVE is a member of enum TrimAnalyticsGate.**
  This gate activates the O2 diagnostic when an O2 sensor fault is detected.
  In some DTC-related documentation this same member is referenced using the
  alternate casing `TrimAnalyticsGate.o2_fault_active` -- both strings identify
  the same enum member.

- **TrimAnalyticsGate.FUEL_TRIM_ACTIVE is a member of enum TrimAnalyticsGate.**
  This gate activates when fuel trim corrections are active.

## Known Documentation Bug

The enum member `SUPPRESS_POST_CAT_TRIM` is documented alongside the other
TrimAnalyticsGate members in the configuration reference. The documentation
states that this gate suppresses post-catalyst trim adjustments downstream of the
catalytic converter. However, **this is a known documentation bug:**
`SUPPRESS_POST_CAT_TRIM` does not actually exist in the shipped enum. It is a
phantom member -- present in the docs, absent from the compiled code.

This doc bug is explicitly tagged here so that a knowledge graph extractor can:
1. Avoid creating a spurious entity node for `SUPPRESS_POST_CAT_TRIM` as a real
   TrimAnalyticsGate member.
2. Link it instead as a `documentation_bug` annotation on the TrimAnalyticsGate
   entity.

## Cross-Reference

The `O2_FAULT_ACTIVE` gate controls the O2 sensor diagnostics described in the
DTC Fault Mapping Reference (`dtc_fault_map.md`). See that document for the
DTC-to-failure-mode mappings that trigger this gate.
