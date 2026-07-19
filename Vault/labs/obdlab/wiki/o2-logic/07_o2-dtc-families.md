---
chunk: o2-logic/07_o2-dtc-families
topic: o2-logic
sources:
  - master_o2_sensor_guide.md §7 (common DTC families)
  - master_o2_sensor_guide.md §5 (heater DTCs)
  - Oxygen Sensor Codes - A Complete Guide ...md (lean/rich-code causes; misfire reads lean)
consumer: TrimAnalyticsGate.O2_FAULT_ACTIVE — an active P0130–P0161 sets the gate, COMLab fault_atlas_router suppresses trim verdicts while it is set; DTC codes route through COMLab fault_atlas_router fault-family selection
consumer_status: active
dedup: Oxygen Sensor Codes guide (REF) folded here + into 05; only its unique misfire→false-lean caveat is preserved. O2sensorLogic.md dropped (subset of O2NBvsWB.md).
related: [[05_bias-vs-real-truth-perception]], [[../taxonomy/faultatlas]]
---

# O₂ DTC families

The petrol O₂ DTC catalogue. An active code in the **P0130–P0161** range sets
`TrimAnalyticsGate.O2_FAULT_ACTIVE`, which makes COMLab's `fault_atlas_router`
suppress trim-based verdicts for that sample — a sensor fault corrupts the trim
feedback, so trims are not trustworthy evidence until it clears.

| Code | Definition | Bank/Sensor | Common cause → failure mode |
|---|---|---|---|
| P0130 | O₂ circuit malfunction | B1S1 | Wiring/connector/end-of-life |
| P0131 | O₂ circuit low voltage | B1S1 | Stuck lean → `STUCK_LEAN` (exhaust leak, short-to-ground) |
| P0132 | O₂ circuit high voltage | B1S1 | Stuck rich → `STUCK_RICH` (silicone, short-to-voltage) |
| P0133 | Slow response | B1S1 | Lazy/aged → `SLUGGISH` |
| P0134 | No activity detected | B1S1 | Open circuit/dead → `DEAD` |
| P0135 | Heater circuit | B1S1 | Heater open/short/fuse → `HEATER_FAULT` |
| P0136–P0141 | (same family) | B1S2 | Post-cat — affects catalyst monitor only (see `06`) |
| P0150–P0161 | (same family) | B2 S1/S2 | Bank-2 mirror of P0130–P0141 |
| P0030 / P0036 / P0050 / P0056 | Heater control circuit | B1S1 / B1S2 / B2S1 / B2S2 | Newer codes; same physical fault as P0135/P0141/P0155/P0161 → `HEATER_FAULT` |
| P2A00–P2A03 | A/F (wideband) sensor circuit | by bank/sensor | Wideband equivalents of P013x |

Failure-mode column links each code to the `O2FailureMode` value in
`03_failure-modes-taxonomy`.

## Lean/rich code caveats (practitioner source)

The "rich/lean" codes (P0171–P0175) are **fuel-system** verdicts, not "replace
the O₂ sensor" instructions — the sensor is often healthy and reporting a real
mixture. Route them through the bias-vs-real table (`05`) before condemning the
sensor.

- **Misfire reads lean, not rich.** A misfire dumps *unburned oxygen* into the
  exhaust, so the O₂ sensor reads lean despite the unburned fuel — high exhaust
  O₂ = lean reading. A lean code with a misfire present routes to the misfire
  family, not to a fuel-delivery lean cause. (This is the one routable fact
  unique to the practitioner guide; the rest of its content is covered by §6/§7
  of the spine.)
- A pre-cat exhaust leak causes erratic/false-lean readings — consistent with
  the §05 exhaust-leak caveat.

Citation: DTC catalogue master_o2_sensor_guide.md §7; heater codes §5;
misfire→high-O₂→lean and lean/rich-code framing from "Oxygen Sensor Codes — A
Complete Guide…" (engine-light-help.com). Fault-family routing target:
sources/taxonomy/faultatlas.md.


## Core Entities

- P0130, P0131, P0132, P0133, P0134, P0135, P0136, P0030, P0036, P0050, P0056
- TrimAnalyticsGate.O2_FAULT_ACTIVE, STUCK_LEAN, STUCK_RICH, SLUGGISH, DEAD, HEATER_FAULT
- TrimAnalyticsGate.O2_FAULT_ACTIVE gate + fault_atlas_router (consumer, active)

## Graph relations (explicit)

**P0130** through **P0161** SETS **TrimAnalyticsGate.O2_FAULT_ACTIVE**
**P0131** INDICATES **STUCK_LEAN**
**P0132** INDICATES **STUCK_RICH**
**P0133** INDICATES **SLUGGISH**
**P0134** INDICATES **DEAD**
**P0135** INDICATES **HEATER_FAULT**
**P0136** through **P0141** AFFECT catalyst monitor only
**IGNITION_MISFIRE** READS lean (unburned O2) and routes to misfire family

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
