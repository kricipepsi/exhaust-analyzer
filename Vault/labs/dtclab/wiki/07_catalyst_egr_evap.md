---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "emissions-routing"
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/07_catalyst_egr_evap.md"
---
# 07 — Catalyst, EGR & EVAP DTCs

Domain reference. Sources: `cases/DTCcases1.md`, predecessor wiki §18,
`DtcDoc.md`, and Denton §5.3.6 / §5.3.11 via ANALYSIS §A5. See `00_INDEX.md`.

---

## 7.1 Catalyst efficiency — P0420 / P0430

Catalyst efficiency is measured by oxygen storage capacity (OSC). The post-cat O₂
sensor should show slow, stable voltage when the catalyst buffers the rapid
upstream oscillation. If post-cat switching frequency approaches pre-cat
frequency, OSC has dropped.

**Enable conditions** (all must hold):

- ECT ≥ 70°C
- Steady 2000 – 3000 RPM
- Closed loop (`fuel_system_status = CL`)
- No active misfire DTCs (P0300 – P0312)
- No active mixture DTCs (P0171 / P0172 / P0174 / P0175)
- ≥ 1 drive cycle since `codes_cleared`

A P0420 stored when any of these were not met is suspect.

**Pre/post-O₂ correlation (v2 corroboration).** Denton §5.3.6 pins the mechanism:
a healthy catalyst stores oxygen and keeps the downstream sensor quiet; as OSC
degrades the **downstream sensor begins to mirror the upstream**. The classic
monitor needs cruise data — but the **4DLab-viable form is the idle/stress-idle
post-cat behaviour cross-checked against GASLab post-cat chemistry**, not the
drive-cycle correlation. This corroborates the existing downstream-O₂ masking
model (`T-OBDV2-3`); the chemistry side is GASLab-owned. Source: ANALYSIS §A5.

**Mode `$06` early warning:** MID `$21` (Bank 1 catalyst) TID `$81` (OSC test). A
value near the minimum limit indicates a degrading catalyst before P0420 confirms.

**Physical inspection thresholds** (technician-facing, not DTCLab-evaluated):

| Test | Pass | Fail |
|---|---|---|
| Idle backpressure | < 1.5 psi | ≥ 1.5 psi |
| 2500 RPM backpressure | < 3.0 psi | ≥ 3.0 psi |
| Snap-throttle peak | ≤ 5 psi | > 5 psi |
| IR delta (outlet − inlet) | ≥ 20°C | < 20°C |

---

## 7.2 EGR valve malfunction — P0400 – P0409

EGR stuck open at idle introduces inert exhaust gas into the intake, causing
rough idle, low MAF, high STFT. EGR stuck closed at stress idle produces no
change in MAP when EGR is commanded open. Mode `$06` MID `$3B` tracks flow values
and position feedback. A test value at minimum limit indicates the valve is not
moving or passages are clogged.

In the extreme, an EGR valve stuck wide open at cold start admits enough inert
gas to fall below the oxygen threshold for ignition — a rough-crank no-start
(`DtcDoc.md` Era-1 case 6: P1404, MAP ≈ 28 inHg / no vacuum). See chunk `10`.

---

## 7.3 EVAP system — leak & purge DTCs (v2)

The EVAP system captures fuel vapours and purges them into the engine. Reference
DTC semantics (`DtcDoc.md`):

| DTC | Name | PCM trigger |
|---|---|---|
| P0440 | EVAP system malfunction | Generic system fault |
| P0441 | EVAP incorrect purge flow | No vacuum present when purge commanded open |
| P0442 | EVAP small leak | Vacuum/pressure decay test detects small leak |
| P0446 | EVAP vent control circuit | Electrical fault in vent-valve solenoid circuit |
| P0455 | EVAP gross leak | Large leak / open vapour path |
| P0456 | EVAP very small leak | Decay test detects leak as small as 0.020″ |

**EVAP leak-size pin (v2).** Denton: the leak-detection threshold tightened by
era — **1 mm (0.040″) for 1996–1999**, **0.5 mm (0.020″) for post-2000**. The
EVAP monitor is also readiness-constrained (temperature + fuel-fill window), so a
"no EVAP fault" on a Not-Ready monitor is untested — see chunk `01` readiness
gate. Source: ANALYSIS §D.

**Purge-stuck-open ⇒ rich shift.** A saturated canister or a purge valve stuck
open floods the intake with raw vapour, driving trims negative and producing a
secondary P0172/P0175 — at the extreme an AFR below 9:1 that prevents starting
(`DtcDoc.md` Era-3 case 29: P0455 + P0172).

## Graph relations (explicit)

**P0420** ROUTES_TO **DTCRoutingTag.CATALYST_HISTORY**
**P0430** ROUTES_TO **DTCRoutingTag.CATALYST_HISTORY**
**P0400** through **P0409** ROUTES_TO **DTCRoutingTag.EGR_HISTORY**
**P1404** ROUTES_TO **DTCRoutingTag.EGR_HISTORY**
**P0440** through **P0459** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**P0441** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**P0442** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**P0446** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**P0455** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**P0456** ROUTES_TO **DTCRoutingTag.EVAP_HISTORY**
**DTCRoutingTag.CATALYST_HISTORY** MAPS_TO **catalyst_failure** family
**DTCRoutingTag.CATALYST_HISTORY** GATED_BY **emissions.has_catalyst = true**
**DTCRoutingTag.EGR_HISTORY** GATED_BY **emissions.egr_equipped = true**
**DTCRoutingTag.EGR_HISTORY** MAPS_TO **None** family
**DTCRoutingTag.EVAP_HISTORY** MAPS_TO **None** family

## Core Entities

- **P0420** — Confirmed DTC indicating Catalyst System Efficiency Below Threshold (Bank 1). Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0401** — Confirmed DTC indicating EGR Flow Insufficient Detected. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0455** — Confirmed DTC indicating EVAP System Gross Leak Detected. Consumer: `dtclab/config/routing_tag_map.yaml`.


