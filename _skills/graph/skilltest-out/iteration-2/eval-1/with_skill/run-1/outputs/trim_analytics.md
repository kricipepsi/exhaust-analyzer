# Trim Analytics Gates

Trim analytics gates suppress or allow downstream trim calculations.

## Available Gates

| Gate | Meaning |
|------|---------|
| TrimAnalyticsGate.O2_FAULT_ACTIVE | O2 fault diagnostics are active |
| TrimAnalyticsGate.FUEL_TRIM_ACTIVE | Fuel trim diagnostics are active |
| SUPPRESS_POST_CAT_TRIM | Legacy note: this value appears in old docs but is not a real enum member |

The shipped enum uses `TrimAnalyticsGate.O2_FAULT_ACTIVE`. Some migrated notes
still spell this value as `TrimAnalyticsGate.o2_fault_active`.


## Graph relations (explicit)

**TrimAnalyticsGate** enumerates **TrimAnalyticsGate.O2_FAULT_ACTIVE**
**TrimAnalyticsGate** enumerates **TrimAnalyticsGate.FUEL_TRIM_ACTIVE**
**TrimAnalyticsGate.O2_FAULT_ACTIVE** describes **O2 fault diagnostics**
**TrimAnalyticsGate.FUEL_TRIM_ACTIVE** describes **Fuel trim diagnostics**
**TrimAnalyticsGate** gates **downstream trim calculations**
**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (legacy documentation note)

## Core Entities

- **TrimAnalyticsGate** - shipped enum; consumer: trim analytics gates.
- **TrimAnalyticsGate.O2_FAULT_ACTIVE** - canonical enum value; consumer: O2 fault diagnostic gating.
- **TrimAnalyticsGate.FUEL_TRIM_ACTIVE** - canonical enum value; consumer: fuel trim diagnostic gating.
- **downstream trim calculations** - gated calculation target; consumer: trim analytics.
- **SUPPRESS_POST_CAT_TRIM** - legacy non-enum note; consumer: documentation bug filtering.