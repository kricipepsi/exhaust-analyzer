---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "fuel-air-routing"
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/05_fuel_air_metering.md"
---
# 05 — Fuel & air metering DTCs

Domain reference. Sources: `cases/DTCcases1.md`, `master_perception_guide.md`,
`DtcDoc.md`. See `00_INDEX.md` for the data-isolation invariant (gas values are
GASLab-owned; this chunk reads DTC + freeze-frame + Mode `$06` only).

---

## 5.1 Intake vacuum leak — unmetered air

Vacuum leak introduces unmetered air downstream of the MAF. PCM correctly
measures less air than is actually entering and enriches accordingly, but the O₂
sensor reports lean exhaust. STFT and LTFT go strongly positive.

**Discriminator:** total fuel trim (STFT + LTFT) strongly positive at idle
(`calculated_load_pct < 30%`) but trends back toward normal at stress idle, as
the unmetered leak becomes a smaller fraction of total airflow. The RPM-dependent
behaviour is the definitive vacuum-leak signature.

- DTC pattern: P0171 (Bank 1 lean), P0174 (Bank 2 lean if post-throttle-body);
  also P2187 / P2189 (system too lean at idle, Bank 1 / Bank 2).
- Freeze frame: low RPM, low CLV.
- Mode `$06`: MID `$13` fuel-system monitor pushing toward maximum allowed limit.

---

## 5.2 Fuel-delivery deficiency — pump and filter

Weak pump / clogged filter supplies adequate volume at idle but fails under high
demand. Trims appear normal at curb idle and only trend lean at stress idle or
highway RPM.

**Discriminator:** trims normal at idle but strongly positive at 3000+ RPM. The
opposite of the vacuum-leak pattern.

- DTC pattern: P0171; P0087 (fuel rail/system pressure too low) when a pressure
  sensor is present.
- Freeze frame: elevated RPM and CLV when P0171 confirms.
- Mode `$06`: misfire counters often show random distribution across all
  cylinders (global lean causing lean misfires).

---

## 5.3 MAF sensor skew — contaminated hot-wire

Contaminated MAF overreports airflow at low velocity and underreports at high
velocity. PCM enriches at idle (negative trims) and leans out at high flow
(positive trims). The "double whammy" signature.

**Discriminator:** LTFT negative at idle, trending positive at stress idle. MAF
baseline: healthy sensor reads ≈ 1 g/s per litre of displacement at curb idle,
scaling to 3–5 g/s/L at stress idle (≈ 4× idle).

- DTC pattern: P0101 (MAF range/performance), P0102/P0103 (circuit low/high).
- Freeze frame: positive total trim at elevated CLV with `absolute_engine_load_pct`
  significantly below expected WOT.

---

## 5.4 Extended metering DTC inventory (v2)

Reference inventory from `DtcDoc.md` ("25 additional DTCs"). Each entry is the
PCM trigger logic, for use when the code appears in a Mode `$03/$07` array. These
are reference DTC semantics; they add no DTCLab contract field.

| DTC | Name | PCM trigger logic |
|---|---|---|
| P0010 | Intake camshaft actuator circuit (B1) | VCT circuit voltage out of calibrated limits |
| P0011 | Intake cam timing over-advanced (B1) | Physical cam timing more advanced than commanded |
| P0012 | Intake cam timing over-retarded (B1) | Cam timing fails to reach commanded advance, stays retarded |
| P0014 | "B" (exhaust) cam timing over-advanced | Exhaust cam timing exceeds target advance |
| P0016 | Crank-cam correlation | Crank/cam signal misalignment > one tooth (≈ 6°) |
| P0102 / P0103 | MAF circuit low / high | MAF signal below min / above max for set time |
| P0106 | MAP range/performance | Manifold pressure not consistent with RPM + throttle |
| P0113 | IAT circuit high | IAT signal indicates implausibly low temp (open/high-resistance) |
| P0116 | ECT range/performance | ECT vs IAT after soak differ by > calibrated value (e.g. 17°C) |
| P0121 | TPS range/performance | TPS voltage does not correlate with MAF / MAP |
| P0128 | Coolant thermostat (below regulating temp) | Engine fails to reach target temp in expected time |
| P0135 | O₂ heater circuit (B1 S1) | Heater current draw indicates open circuit / wrong resistance |
| P0200 | Injector circuit malfunction | No expected voltage drop / inductive kick on a commanded pulse |
| P0219 | Engine overspeed | RPM exceeds manufacturer safety limit |

**Camshaft-correlation note (P0016):** the > 1-tooth / 6° mechanical phase
mismatch is also a non-start trigger (the PCM disables ignition to prevent
valve-to-piston contact) — see chunk `10` era cases (timing-chain jump,
VVT phaser).

## Graph relations (explicit)

**P0171** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0174** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P2187** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P2189** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0087** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0100** through **P0104** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0101** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0102** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0103** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0106** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0113** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0116** ROUTES_TO **DTCRoutingTag.THERMAL_HISTORY**
**P0121** ROUTES_TO **DTCRoutingTag.LEAN_HISTORY**
**P0128** ROUTES_TO **DTCRoutingTag.THERMAL_HISTORY**
**P0135** ROUTES_TO **DTCRoutingTag.O2_HISTORY**
**P0200** ROUTES_TO **DTCRoutingTag.INJECTOR_HISTORY**
**P0219** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**P0010** ROUTES_TO **DTCRoutingTag.VVT_HISTORY**
**P0011** ROUTES_TO **DTCRoutingTag.VVT_HISTORY**
**P0012** ROUTES_TO **DTCRoutingTag.VVT_HISTORY**
**P0014** ROUTES_TO **DTCRoutingTag.VVT_HISTORY**
**P0016** ROUTES_TO **DTCRoutingTag.VVT_HISTORY**
**DTCRoutingTag.LEAN_HISTORY** MAPS_TO **lean_condition** family
**DTCRoutingTag.VVT_HISTORY** MAPS_TO **cam_timing** family
**DTCRoutingTag.INJECTOR_HISTORY** MAPS_TO **mechanical_wear** family
**DTCRoutingTag.THERMAL_HISTORY** MAPS_TO **None** family

## Core Entities

- **P0171** — Confirmed DTC indicating System Too Lean (Bank 1). Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0101** — Confirmed DTC indicating MAF Sensor Performance. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P0016** — Confirmed DTC indicating Crank-Cam Position Correlation. Consumer: `dtclab/config/routing_tag_map.yaml`.

