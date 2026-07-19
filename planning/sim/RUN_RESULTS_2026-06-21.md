# T-SIM-1 — 5FR oil-burn simulation run results

**Run date:** 2026-06-21  
**Vehicle:** Citroën 5FR / EP6CDT, VIN `VF7SA5FR8AW511081`  
**Result artifact:** `planning/sim/oil_burn_5fr_results.json`

## Run result

Both the JSON data pass and the Jaeger-traced pass exited with code 0.

```text
RESULT: 5/5 routed to expected fault (ALL GREEN)
[json] wrote C:\Workspace\planning\sim\oil_burn_5fr_results.json
[trace] spans flushed to Jaeger.
```

## Routing table

| Case | Gas state | B1S2 signature | Verdict | Pass |
|---|---|---|---|---|
| Worn piston rings | `WORN_PISTON_RINGS` | `FIXED_NEGATIVE` | `MW-001` | PASS |
| Worn valve stem seals | `WORN_VALVE_SEALS` | `TRANSIENT_NEGATIVE` | `MW-002` | PASS |
| Blown head gasket (oil→cyl) | `COOLANT_LEAK_INTERNAL` | `NEUTRAL` | `MW-003` | PASS |
| PCV stuck open | `POA_SIGNATURE` | `DIVERGENT` | `MW-008` | PASS |
| Turbo turbine-seal leak | `POA_SIGNATURE` | `DFCO_NEGATIVE` | `MW-009` | PASS |

## Demand ranking

| Rank | Demand | Case | Verdict | Demand reason |
|---|---:|---|---|---|
| 1= | 4.0 | PCV stuck open | `MW-008` | Ambiguous POA family; requires simultaneous upstream-positive/downstream-negative split |
| 1= | 4.0 | Turbo turbine-seal leak | `MW-009` | Ambiguous POA family; requires DFCO fuel-cut capture decoupled from combustion |
| 3 | 3.5 | Worn piston rings | `MW-001` | Requires post-cat B1S2 trim; historic low-idle-HC rule conflict |
| 4 | 2.0 | Worn valve stem seals | `MW-002` | Requires post-cat B1S2 trim |
| 5 | 1.0 | Blown head gasket (oil→cyl) | `MW-003` | Gas chemistry only |

## Jaeger confirmation

Jaeger UI and query API were reachable at `http://localhost:16686`.
Exactly **5 traces** were visible under service `wiredv2-oil-case`. Each trace contained one
`oil_case_<id>` root span with direct `gas_state`, `post_cat_trim`, and `verdict` child spans.

## Parity check

PASS — all five gas states, B1S2 signatures, verdicts, confidence values, and demand scores match:

- `planning/OIL_CASE_SIGNATURES_5FR.md`
- `planning/sim/OIL_BURN_5FR_SIM_RESULTS.md`

The JSON contains one result per case and each result includes `verdict`, `confidence`,
`demand_score`, and `demand_reasons`.
