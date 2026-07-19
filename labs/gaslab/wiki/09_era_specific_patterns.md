---
chunk_id: GASWIKI-09
title: "Era-Specific Fault Patterns (1990–2010)"
doc: GAS_WIKI
version: v2.0
summary: "Common tailpipe faults by era for the 1990–2010 scope: Era 1 (1990–2000, mechanical / early OBD-II) and Era 2 (2000–2010, electronic / Euro 3–5). Each fault maps to a chemical_state; era context primarily sets prior probability for COMLab routing."
covers_v1_sections: [12]
entities_defined: [CONCEPT_ERA1, CONCEPT_ERA2]
related_chunks: [GASWIKI-05, GASWIKI-06A, GASWIKI-06B]
sources: ["GAS_WIKI.md v1.0 §12.1–12.2", "data/CommonFaults.md"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "era-thresholds"
implements:
  - "labs/gaslab/gaslab/dna_view.py"
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
consumers:
  - "gaslab: labs/gaslab/gaslab/rule_engine.py _coc_adjust_normal_bounds"
  - "gaslab: labs/gaslab/gaslab/resolution.py _euro_thresholds"
drift_guards:
  - "labs/gaslab/tests/unit/test_dna_view.py"
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
tags: ["gaslab", "era-thresholds", "wiki"]
source: "labs/gaslab/wiki/09_era_specific_patterns.md"
---

# 9. Era-Specific Fault Patterns (1990–2010)

> **Chunk summary.** Common faults seen at the tailpipe per era within the 1990–2010 scope. Each maps to a `chemical_state` in the atlas; the era context mainly affects prior probability for COMLab routing. **The 2010–2020 "Era 3" patterns are out of scope and are not carried into v2.**

## 9.1 Era 1: 1990–2000 (Mechanical / early OBD-II) {#CONCEPT_ERA1}

Source: `data/CommonFaults.md` Era 1.

| Fault | Gas pattern | `chemical_state` |
|---|---|---|
| Stuck-open EGR valve | CO₂ down, O₂ up, HC up; rough idle | `EGR_STUCK_OPEN` |
| Blown head gasket (coolant → cylinder) | White sweet smoke; O₂ spikes; NOₓ suppressed | `COOLANT_LEAK_INTERNAL` (or `SAMPLE_INVALID` if water in line) |
| Leaky / stuck-open FPR | CO > 6 %, HC up, O₂ → 0 | `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` |
| Worn distributor cap / rotor | HC > 2000 ppm, O₂ spikes, CO low | `IGNITION_MISFIRE` |
| Clogged fuel filter | Lean misfire under load; O₂ + HC up, CO down | `LEAN_MISFIRE` |
| Lazy O₂ sensor (silica coating) | Alternating rich/lean waves | `O2_SENSOR_BIASED_*` |
| Vacuum leak (manifold gasket / hoses) | Lean at idle (O₂ up, CO low); normalises at higher RPM | `LEAN_MIXTURE` |
| Failed ceramic cat | Pre- = post-cat readings | `CATALYST_OVERWHELMED` |
| Worn carb / TB jets | Persistent rich baseline | `RICH_MIXTURE` |
| Stuck-closed thermostat | High fixed CO (3–5 %), high HC; never reaches closed loop | `RICH_MIXTURE` (cold-running) |
| Thermostat stuck open (chronic under-temp) `[v2.2: casesextra]` | Persistent **mild** rich at **both** idle and 2500 RPM (**no speed delta**, λ ≈ 0.97); ECT < 75 °C after a long drive; CO₂ suppressed (13.0–13.5 %); P0128, STFT/LTFT negative | `RICH_MIXTURE` (cold-running) |
| Slipped timing belt / chain (1 tooth) | Deep vacuum drop; HC + O₂ elevated | `CAM_TIMING_RETARDED_MAP` (Speed-Density) / `CAM_TIMING_RETARDED_MAF` (MAF) |
| Burnt exhaust valve | Periodic cyclic HC pulses | `WORN_ENGINE` |
| Defective cold-start injector | Normal idle; heavy rich-stumble on hot restarts | `RICH_MIXTURE` (transient) |
| Clogged PCV | High HC + CO at idle, oil consumption | `POA_SIGNATURE` |
| Worn piston rings | High HC at speed, slight CO | `WORN_PISTON_RINGS` |
| Cracked exhaust manifold | False lean on O₂; ECU dumps fuel; high CO + high O₂ | `EXHAUST_AIR_LEAK` |
| MAF contamination | Under-reports air; lean under load | `LEAN_MIXTURE` |
| Weak ignition coil (DIS) | HC bursts > 3000 ppm under load | `IGNITION_MISFIRE` |

*(Items that are not gas-diagnosable at the tailpipe — defective TPS/IAC transients — are noted in the source but are not GASLab outputs.)*

## 9.2 Era 2: 2000–2010 (Electronic / Euro 3–5) {#CONCEPT_ERA2}

Source: `data/CommonFaults.md` Era 2.

| Fault | Gas pattern | `chemical_state` |
|---|---|---|
| Primary cat efficiency failure (P0420) | Pre-cat = post-cat O₂ switching | `CATALYST_OVERWHELMED` |
| Stuck-open EVAP purge valve | Randomly rich at idle, self-correcting at cruise | `EVAP_CANISTER_SATURATED` |
| ETB carbon buildup | Erratic idle gas ratios; transient lean surges | (transient) |
| COP internal insulation arc | Single-cylinder misfire; HC steps up by N | `IGNITION_MISFIRE` |
| HO2S heater circuit failure | Drops out of closed loop at extended idle | `O2_SENSOR_BIASED_*` |
| EGR cooler carbon plugging | Massive NOₓ spike on highway cruise | `EGR_STUCK_CLOSED` |
| Early GDI carbon deposition | Restricted CO₂; random idle misfires | `GDI_INTAKE_VALVE_CARBON` |
| VVT solenoid sludge | NOₓ spikes during decel / high-load transitions | `VVT_FAILURE` |
| Leaking fuel injector pintle | Single cylinder rich; tailpipe CO elevated | `RICH_MIXTURE` (bank-specific) |
| Defective MAP sensor calibration | Continuous rich across operating range | `RICH_MIXTURE` |
| Swirl flap / IMRC actuator failure | Air starvation at high RPM | `RICH_MIXTURE` (load-dependent) |
| ECT resistance drift (reads colder) | Engine stays rich during warmup | `RICH_MIXTURE` |
| Alternator diode failure (AC ripple) | Erratic readings; clean gases but P0300 set | `IGNITION_MISFIRE` (ghost — see → RULE_LAMBDA_MISMATCH) |
| Loose dipstick / oil cap | Lean shift at idle; clamping PCV restores | `LEAN_MIXTURE` |
| Intercooler hose split (turbo) | Massive rich during accel; black smoke | `RICH_MIXTURE` (boost) |
| Defective CKP sync loss | Intermittent high-RPM misfires; HC spikes | `IGNITION_MISFIRE` |
| Fuel pump driver module under-volt | Extreme lean drop-out under high load | `LEAN_MIXTURE` |
| GDI HPFP internal seal leak (late-era GDI) | Permanent rich trim shift; high CO at warm idle | `GDI_HPFP_INTERNAL_SEAL_LEAK` |
| Turbo turbine-seal oil leak (e.g. DISI 2007–09) | Extreme tailpipe HC, stoich λ, CO ≈ 0 | `POA_SIGNATURE` (turbo-seal sub-mode) |

> Diesel-only after-treatment (DPF, SCR, DEF, LNT) and post-2010 Euro 6/7 chemistry are excluded by the operating envelope.

## Graph relations (explicit)

**CONCEPT_ERA1** DESCRIBES **Euro 1–2 vehicles (1990–1998)** — no-cat / early-cat era
**CONCEPT_ERA1** SCALES **fault thresholds** per Euro 1/2 emission limits
**CONCEPT_ERA2** DESCRIBES **Euro 3–5 vehicles (1998–2010)** — OBD-II, wideband sensors, VVT, early GDI
**CONCEPT_ERA2** SCALES **fault thresholds** per Euro 3/4/5 emission limits
**CONCEPT_ERA1** CONSUMED_BY **euro_emission_category** from **GasLabDnaView** (Euro 1–2 range)
**CONCEPT_ERA2** CONSUMED_BY **euro_emission_category** from **GasLabDnaView** (Euro 3–5 range)
**Era 1 fault table** MAPS_TO **EGR_STUCK_OPEN**, **COOLANT_LEAK_INTERNAL**, **SAMPLE_INVALID**, **VACUUM_REGULATOR_DIAPHRAGM_RUPTURE**, **IGNITION_MISFIRE**, **LEAN_MISFIRE**, **O2_SENSOR_BIASED_***, **LEAN_MIXTURE**, **CATALYST_OVERWHELMED**, **RICH_MIXTURE**, **CAM_TIMING_RETARDED_MAP**, **CAM_TIMING_RETARDED_MAF**, **WORN_ENGINE**, **POA_SIGNATURE**, **WORN_PISTON_RINGS**, **EXHAUST_AIR_LEAK**
**Era 2 fault table** MAPS_TO **CATALYST_OVERWHELMED**, **EVAP_CANISTER_SATURATED**, **IGNITION_MISFIRE**, **O2_SENSOR_BIASED_***, **EGR_STUCK_CLOSED**, **GDI_INTAKE_VALVE_CARBON**, **VVT_FAILURE**, **RICH_MIXTURE**, **GDI_HPFP_INTERNAL_SEAL_LEAK**, **POA_SIGNATURE**, **LEAN_MIXTURE**
**Alternator diode failure** (Era 2) ROUTES_TO **RULE_LAMBDA_MISMATCH** — ghost misfire from AC ripple

## Core Entities

- **CONCEPT_ERA1** — Euro 1–2 (1990–1998): no-cat / early-cat era, CO ceiling 4.5 % → 0.5 %. Consumer: `euro_emission_category` DNA field → `rule_engine._coc_adjust_normal_bounds`.
- **CONCEPT_ERA2** — Euro 3–5 (1998–2010): OBD-II, wideband, VVT, early GDI. Consumer: `euro_emission_category` DNA field → `rule_engine._coc_adjust_normal_bounds`.
