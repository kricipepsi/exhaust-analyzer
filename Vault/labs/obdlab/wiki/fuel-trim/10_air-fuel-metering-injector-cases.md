---
chunk: fuel-trim/10_air-fuel-metering-injector-cases
topic: fuel-trim
sources:
  - FuelTrimFamilies.md §"Fault Family 1: P01xx and P02xx" (cases 1–9)
consumer: COMLab fault_atlas_router routing into lean_condition / rich_mixture / sensor_fault / misfire families (ERR-LC-001/003, ERR-SF-003/004/005, ERR-MF-005). Three mechanisms are new-fault PROPOSALS (register in comlab/config/proposals/): maf_circuit_ground_open_failsafe, thermostat_stuck_open_closedloop_delay, injector_thermal_intermittent.
consumer_status: MIXED (active families + 3 proposals)
provenance: sources/fuel-trim/FuelTrimFamilies.md
related: [[09_fault-family-case-matrix]], [[04_trim-pattern-decision-tree]], [[07_trim-vs-gas-chemistry-crosscheck]]
---

# P01xx/P02xx — air & fuel metering, thermal, injector circuits

Mechanism detail behind matrix rows 1–9. Each pairs a trim signature with the
*discriminating test* that confirms it.

## Unmetered-air vs fuel-delivery (the idle→RPM split)

- **Intake vacuum leak (row 1, ERR-LC-001).** Both banks lean: STFT +15 / LTFT +25
  at idle, collapsing to 0 / +5 at 2500 RPM. The leak is a large fraction of idle
  airflow but negligible at high flow: `lim(ṁ_leak/ṁ_total)→0`. Confirm with smoke
  test, throttle body blocked.
- **Restricted fuel filter (row 2, ERR-LC-003 signature).** Mirror image vs RPM:
  normal at idle (+2/+5), climbs to +25/+25 under load as demand outruns supply.
  Pressure drops 58→25 PSI under acceleration; pump *current* normal (5.2 A) rules
  out the pump motor. **Proposal:** split a `fuel_delivery_restriction` discriminator
  from `fuel_pump_low_pressure` — same trim signature, different component, and the
  current-normal + pressure-drop pair distinguishes them.

## MAF / MAP sensor faults (RPM-independent, both banks)

- **MAF circuit ground open (row 3) — PROPOSAL.** Open ground → 0 Hz output → PCM
  drops to **speed-density failsafe**, default lookup → runs **rich**, STFT both
  banks −22 %. P0102 sets *with* rich P0172/P0175. Distinct from `ERR-SF-003`
  (MAF under-reading, which trends lean): a *circuit-open failsafe* inverts the
  expected direction. Register `maf_circuit_ground_open_failsafe`; consumer =
  fault_atlas sensor_fault routing keyed on (P0102 + negative both-bank trim).
- **MAP over-reporting (row 4, ERR-SF-004).** Sensor reads pressure too high → PCM
  computes too-wide base pulse → over-fuels → −14 % idle. Bench-test vacuum-decay
  shows output high at every vacuum step. Maps to `map_sensor_calibration_drift`.

## Thermal inputs forcing enrichment

- **Open ECT (row 5, ERR-SF-005/RM-006).** Thermistor open → locked −40 °C → PCM
  believes sub-zero → heavy enrichment → rich P0172, trims read 0/0 because the
  system stays effectively open-loop/failsafe. Confirm: bridge harness → ECT jumps
  >121 °C (wiring intact, sensor bad).
- **Thermostat stuck open (row 6, P0128) — PROPOSAL.** Coolant never reaches the
  ~82 °C regulating threshold, so closed-loop monitors are **delayed**; PCM holds
  cold enrichment (+14 %). No existing node covers "closed-loop never qualifies
  because ECT stays low." Register `thermostat_stuck_open_closedloop_delay`;
  consumer = analytics_preconditions (ENGINE_COLD persistence) + fault_atlas. This
  is also a precondition interaction — see `14`/`08`.

## Injector faults (single-bank / single-cylinder)

- **Injector open circuit (row 7, ERR-MF-005).** Dead cylinder pumps air → false
  lean on its bank → STFT B1 +15 %, B2 normal. P0201 + misfire P0301. Coil reads
  OL vs ~12 Ω healthy.
- **GDI injector high-resistance (row 8).** 62 Ω vs 10–16 Ω healthy → won't open
  fully at high rail pressure → lean misfire B1 +10 %. Swap-and-shift confirms
  (code follows the injector). Refine `dead_injector_cylinder_misfire` with a
  high-resistance sub-case.
- **Temperature-intermittent injector (row 9) — PROPOSAL.** Cold: coil OL → misfire,
  STFT +18 % cold-bias; warm: thermal expansion reconnects, 14.2 Ω, runs clean.
  Symptom is *cold-only* and self-clears warm — a temporal signature no current node
  carries. Register `injector_thermal_intermittent`; consumer = fault_atlas keyed
  on (cold-start positive single-bank STFT that normalises when warm).

Citation: FuelTrimFamilies.md cases 1–9 (trim values, discriminating tests,
component specs). Node IDs per comlab/config registry + kg families.


## Core Entities

- P0102, P0172, P0128, P0201, P0301
- VACUUM_LEAK, FUEL_STARVATION, MAF_UNDERREPORT, MAP_OVERREPORT, THERMOSTAT_STUCK_OPEN
- INJECTOR_OPEN_CIRCUIT, GDI_INJECTOR_HIGH_RESISTANCE, INJECTOR_THERMAL_INTERMITTENT
- fault_atlas_router (consumer; 3 PROPOSAL splits)

## Graph relations (explicit)

**P0102** plus **P0172** INDICATES **MAF_UNDERREPORT** ground-open failsafe
**MAP_OVERREPORT** PRODUCES_NEGATIVE **LTFT**
**THERMOSTAT_STUCK_OPEN** DELAYS closed-loop and HOLDS **ENGINE_COLD** enrichment
**P0201** plus **P0301** INDICATES **INJECTOR_OPEN_CIRCUIT**
**INJECTOR_OPEN_CIRCUIT** PRODUCES false-lean single-bank **POSITIVE_TRIM**
**INJECTOR_THERMAL_INTERMITTENT** PRODUCES cold-only single-bank **POSITIVE_TRIM**
**fuel_delivery_restriction** REFINES **ERR-LC-003**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
