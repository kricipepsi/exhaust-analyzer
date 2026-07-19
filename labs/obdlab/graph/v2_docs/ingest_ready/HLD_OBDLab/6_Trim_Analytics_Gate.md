> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 6 Trim Analytics Gate — 8-Gate Priority Chain · Parent document: HLD_OBDLab.md

## 6. Trim Analytics Gate — 8-Gate Priority Chain

`AnalyticsPreconditions.evaluate` returns the first failing gate (priority
order), else `VALID`:

### Entity: TrimAnalyticsGate priority chain

- **Gate 1: ENGINE_COLD** — `coolant_temp_c < 70` (or missing) · Condition: coolant temperature below warm threshold
- **Gate 2: OPEN_LOOP** — `fuel_system_status != CL` · Condition: fuel system not in closed loop
- **Gate 3: O2_FAULT_ACTIVE** — active DTC ∈ `O2_FAULT_DTCS` · Condition: O2 sensor DTC active (P0130–P0161, 32 codes)
- **Gate 4: CKP_CMP_FAULT_ACTIVE** — active DTC ∈ {P0335, P0340} · Condition: CKP/CMP circuit fault active
- **Gate 5: CODES_RECENTLY_CLEARED** — `drive_cycles_since_clear < 1` · Condition: codes cleared recently
- **Gate 6: WOT_ACTIVE** — `throttle_pos ≥ 90` · Condition: wide-open throttle
- **Gate 7: DFCO_ACTIVE** — `dfco_active is True` · Condition: deceleration fuel cut-off active
- **Gate 8: SEMANTIC_ERROR** — semantic gates not all passed · Condition: physics consistency failure
- **VALID** — all gates passed

`O2_FAULT_DTCS` = P0130–P0161 (32 codes). `CKP_CMP_FAULT_DTCS` = {P0335, P0340}.
Both frozensets are maintained locally; keeping them in sync with DTCLab routing
is a COMLab responsibility. The gate **classifies** trim trustworthiness — it
does not suppress payload emission.

## Graph relations (explicit)

**AnalyticsPreconditions.evaluate** ENUMERATES **TrimAnalyticsGate** (9 values: ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, SEMANTIC_ERROR, VALID)
**O2_FAULT_DTCS** ENUMERATES **P0130–P0161** (32 codes, local frozenset)
**CKP_CMP_FAULT_DTCS** ENUMERATES **P0335, P0340** (local frozenset)
**COMLab** CONSUMES **trim_analytics_gate** (confidence path — suppress trim findings unless VALID)
**O2_FAULT_DTCS** MIRRORS_CONTRACT_IN **DTCLab routing** (sync responsibility: COMLab)
