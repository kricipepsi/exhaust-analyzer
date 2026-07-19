> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 10 Analytics Preconditions · Parent document: LLD_OBDLab.md

## 10. Analytics Preconditions (`core/analytics_preconditions.py`)

```python
ECT_WARM_THRESHOLD     = 70   # Gate 1 — coolant warm (°C), §9
WOT_THROTTLE_THRESHOLD = 90   # Gate 6 — WOT throttle (%), §9
```

```python
O2_FAULT_DTCS = frozenset({          # 32 codes, §9
    P0130–P0135,   # B1S1
    P0136–P0141,   # B1S2
    P0142–P0149,   # (continuous range to P0161)
    P0150–P0155,   # B2S1
    P0156–P0161,   # B2S2
})
CKP_CMP_FAULT_DTCS = frozenset({"P0335", "P0340"})  # CKP / CMP circuit
```

(The codeset is the literal contiguous range `P0130`…`P0161` = 32 entries.)
Maintained locally; COMLab keeps them in sync with DTCLab routing.

Gate 6 reads `throttle_pos` from the PID dict; Gate 2 reads `fuel_system_status`
(falling back to `fuel_sys_status`), coerced via `FuelSystemStatus.from_wire`.

## Graph relations (explicit)

**AnalyticsPreconditions** ENUMERATES **ECT_WARM_THRESHOLD=70, WOT_THROTTLE_THRESHOLD=90** (# wiki: §9)
**AnalyticsPreconditions** ENUMERATES **O2_FAULT_DTCS** (32 codes, P0130–P0161, local frozenset)
**AnalyticsPreconditions** ENUMERATES **CKP_CMP_FAULT_DTCS** ({P0335, P0340}, local frozenset)
**O2_FAULT_DTCS** MIRRORS_CONTRACT_IN **DTCLab routing** (sync responsibility: COMLab)
**Gate 2** CONSUMES **fuel_system_status** (falls back to fuel_sys_status, coerced via FuelSystemStatus.from_wire)
**Gate 6** CONSUMES **throttle_pos** (from PID dict)
**test_analytics_preconditions.py** VERIFIES **AnalyticsPreconditions** (unit tests)
