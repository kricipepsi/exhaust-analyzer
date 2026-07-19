---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "ignition-misfire-routing"
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
  - "labs/dtclab/dtclab/core/freeze_frame_extractor.py"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
  - "labs/dtclab/tests/unit/test_freeze_frame_extractor.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/06_ignition_misfire.md"
---
# 06 — Ignition & misfire DTCs

Domain reference. Sources: `cases/DTCcases1.md`, `cases/FF+$06DS.md`,
`DtcDoc.md`, and Denton §5.3.9 via
`AdvAutomotiveFaultDiagnosis_ANALYSIS.md` §A4. See `00_INDEX.md`.

---

## 6.1 Secondary ignition breakdown — coil-on-plug arcing

Coil insulation degrades with heat cycling. At low cylinder pressure (idle),
arcing may not occur. Under load, the same insulation fails. Misfires absent at
idle, appear at stress idle or under acceleration.

- DTC pattern: P0301–P0312 (cylinder-specific, up to 12-cylinder); coil-circuit
  P0351/P0352.
- Mode `$06` misfire counters (MID `$A1`–`$A9`, per-cylinder CID) record every
  event. A cylinder showing high count while others show near-zero isolates the
  fault before P030x crosses threshold.

---

## 6.2 Ignition-timing interpretation

| `ignition_advance_deg` | Interpretation |
|---|---|
| 5 – 15° BTDC at curb idle | Normal |
| 25 – 40° BTDC at 4000 RPM | Normal |
| < 15° BTDC at 4000 RPM + knock retard active | PCM reacting to detonation — investigate fuel octane, carbon buildup, cooling |
| `< −10°` | Flag `ff_timing_retard_severe` — persistent knock, retarded cam phaser, enrichment fault |

**Knock DTCs (v2 reference):** P0327 (knock sensor 1 circuit low) sets when knock
sensor voltage falls below the minimum threshold during operation; P0324 (knock
control system error) is a communication/processing fault in the knock control
module. Source: `DtcDoc.md`.

---

## 6.3 Ghost misfire rule

If misfire counters increment but `total_trim_correction_delta` and wideband
lambda are both normal, suspect alternator AC ripple corrupting the ignition
primary signal. **Check charging-system ripple before replacing coils or plugs.**
(Cross-lab note: ripple measurement is OBDLab; DTCLab supplies the misfire
counts.) A mechanical analogue exists: dual-mass-flywheel play and crank-speed
jitter can register as P0300 with perfect tailpipe chemistry (`DtcDoc2.md`
EXP-N016) — the misfire is an artefact of crank-speed noise, not combustion loss.

---

## 6.4 Misfire severity model — Type A / Type B **[PROPOSAL]**

> **Signal/noise:** v2-new. Consumer named below; full disposition in
> `11_proposals_register.md`. Source: Denton §5.3.9 via ANALYSIS §A4. 4DLab is
> idle-centric, so the ~45%-at-idle catalyst-damage threshold and the Type-A
> flashing-MIL distinction are directly usable.

The OBD misfire monitor grades severity into two classes, by misfire *rate*:

| Class | Meaning | MIL behaviour |
|---|---|---|
| **Type A** | Catalyst-damaging misfire rate | MIL **flashes at 1 Hz** while active |
| **Type B** | Emissions-exceeding (1.5× limit) misfire rate over a drive cycle | MIL steady (stored) |

The damaging rate is **load-dependent**: ≈ **45% misfire at neutral idle**
falling to ≈ **5% at 80% load / 4000 RPM**. EU monitors misfire **≤ 4500 RPM**.
A re-flag under "similar conditions" means **±375 RPM, ±20% load, same warm-up
state**. (All figures Denton §5.3.9.)

**Proposed contract:** a `misfire_severity_class` enum (`TYPE_A` / `TYPE_B` /
`NONE`) derived from MIL-flash state + per-cylinder Mode `$06` counts against the
idle-relevant ~45% rate; and an escalation flag `catalyst_damage_imminent` when
Type A is active (already referenced in non-start chunk `10` for the
flashing-MIL / flooded-catalyst case).

**Named consumer + code path:** COMLab misfire-severity fusion — the fault-atlas
escalates a Type A (flashing-MIL) misfire to `CRITICAL_IMMEDIATE_STOP` routing
(catalyst protection), above a Type B steady code. Pairs with the unallocated
OBDLab misfire promotion (`EP-OBD-IN-07`, `T-OBDV2-9/10`); GASLab
`COMBUSTION_FAIL` is the chemistry-truth side that corroborates it.

---

## 6.5 Misfire chemistry cross-reference (reverse-lookup only)

For COMLab's bidirectional check: a misfire expels the entire unburned charge, so
λ can stay ≈ 1.00 while HC spikes (800–2000 ppm) and O₂ rises by ≈ 21% ÷ N
cylinders (one dead cylinder on a 4-cyl ≈ 5.25% O₂). This gas view is **owned by
GASLab**; DTCLab supplies only the misfire counts and codes. Full table in
chunk `09`.

## Graph relations (explicit)

**P0300** through **P0312** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**P0351** through **P0358** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**P0335** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**P0340** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**P0327** ROUTES_TO **DTCRoutingTag.KNOCK_HISTORY**
**P0324** ROUTES_TO **DTCRoutingTag.KNOCK_HISTORY**
**DTCRoutingTag.MISFIRE_HISTORY** MAPS_TO **misfire** family
**DTCRoutingTag.KNOCK_HISTORY** MAPS_TO **ignition_fault** family
**ignition_advance_deg** < -10° TRIGGERES **ff_timing_retard_severe**
**misfire_severity_class** (proposed) ENUMERATES **TYPE_A**, **TYPE_B**, **NONE**
**TYPE_A** misfire (proposed) TRIGGERES **catalyst_damage_imminent** (proposed)
**catalyst_damage_imminent** (proposed) ESCALATES_TO **CRITICAL_IMMEDIATE_STOP**

## Core Entities

- **P0300** — Confirmed DTC indicating Random/Multiple Cylinder Misfire Detected. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **ff_timing_retard_severe** — Symptom flag set when ignition timing is retarded below -10°. Consumer: `dtclab/core/freeze_frame_extractor.py`.
- **misfire_severity_class** — Proposed enum classifying misfires by damage threat (Type A vs B). Status: PROPOSAL. Consumer: COMLab misfire fusion.
- **catalyst_damage_imminent** — Proposed escalation flag triggered by active Type A misfire. Status: PROPOSAL. Consumer: COMLab routing.

