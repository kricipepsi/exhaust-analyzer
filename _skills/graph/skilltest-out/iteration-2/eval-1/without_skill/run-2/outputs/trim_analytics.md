# Trim Analytics Gates

Trim analytics gates suppress or allow downstream trim calculations.

## Canonical Entities

| Entity label | Entity type | Notes |
|--------------|-------------|-------|
| Trim analytics gates | Gate group | Gate group that suppresses or allows downstream trim calculations |
| Downstream trim calculations | Calculation | Calculations controlled by trim analytics gates |
| TrimAnalyticsGate.O2_FAULT_ACTIVE | Trim analytics gate | Canonical enum member for active O2 fault diagnostics |
| TrimAnalyticsGate.FUEL_TRIM_ACTIVE | Trim analytics gate | Canonical enum member for active fuel trim diagnostics |
| SUPPRESS_POST_CAT_TRIM | Legacy label | Legacy documentation value; not a real enum member |
| TrimAnalyticsGate.o2_fault_active | Alias | Migrated-note spelling for TrimAnalyticsGate.O2_FAULT_ACTIVE |
| O2 fault diagnostics | Diagnostic process | Diagnostics allowed or suppressed by TrimAnalyticsGate.O2_FAULT_ACTIVE |
| Fuel trim diagnostics | Diagnostic process | Diagnostics allowed or suppressed by TrimAnalyticsGate.FUEL_TRIM_ACTIVE |

## Available Gates

| Gate label | Meaning | Status |
|------------|---------|--------|
| TrimAnalyticsGate.O2_FAULT_ACTIVE | O2 fault diagnostics are active | Canonical enum member |
| TrimAnalyticsGate.FUEL_TRIM_ACTIVE | Fuel trim diagnostics are active | Canonical enum member |
| SUPPRESS_POST_CAT_TRIM | Legacy post-catalyst trim suppression note | Legacy label, not a real enum member |

## Explicit Relationships

- Trim analytics gates suppress_or_allow Downstream trim calculations.
- TrimAnalyticsGate.O2_FAULT_ACTIVE is_member_of Trim analytics gates.
- TrimAnalyticsGate.FUEL_TRIM_ACTIVE is_member_of Trim analytics gates.
- TrimAnalyticsGate.O2_FAULT_ACTIVE activates O2 fault diagnostics.
- TrimAnalyticsGate.FUEL_TRIM_ACTIVE activates Fuel trim diagnostics.
- TrimAnalyticsGate.o2_fault_active is_alias_of TrimAnalyticsGate.O2_FAULT_ACTIVE.
- SUPPRESS_POST_CAT_TRIM is_legacy_label_for post-catalyst trim suppression.
- SUPPRESS_POST_CAT_TRIM is_not_member_of TrimAnalyticsGate enum.

## Label Normalization

Use TrimAnalyticsGate.O2_FAULT_ACTIVE as the canonical entity label. Treat TrimAnalyticsGate.o2_fault_active as an alias that refers to the same gate entity.
