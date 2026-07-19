---
chunk: ecu-diagnosis/09_control-module-voltage
topic: ecu-diagnosis
sources:
  - proposals/AddObdFields.md §Part 2.2 — Control Module Voltage (PID 0x42 / VPWR)
  - proposals/DataFlow.md — ΔVPWR delta logic
  - proposals/extracted/EP-OBD-IN-04_control-module-voltage-pid.md
consumer: COMLab `perception_contradiction.py` electrical-health pre-check (T-COMV2-VPWR-GATE-1) — suppress/down-weight sensor-fault routing when the PCM rail is out of band; `ΔVPWR` signatures feed the alternator-AC-ripple node (EP-FA-05).
consumer_status: PROPOSAL (EP-OBD-IN-04 — field + consumer ship together)
refines: upstream of ecu-diagnosis/06 (5 V-regulator rail collapse) and ecu-diagnosis/02 (capacitor leakage / AC ripple) — VPWR is the *measured supply read* that those internal-rail faults manifest behind. Charging-side faults route to EP-FA-05.
---

# Control-module voltage (VPWR, PID 0x42)

Supply voltage at the PCM pins. Every sensor reference is built on a clean DC rail, so a low, high,
or ripply rail **shifts stoichiometric points and sensor references before any air/fuel sensor is at
fault**. VPWR must be ruled out first or the engine blames the wrong subsystem (e.g. false
processor-class codes such as P0606 on some ECUs).

## Static thresholds

| Rail | Reading | Interpretation |
|---|---|---|
| Healthy | ~13.5–14.7 V running | clean reference |
| **Low** | `< 12.0 V` (esp. `< 11.5 V` with unstable trim) | charging/ground fault — flag **before** sensor-fault routing |
| **High** | `> 15.0 V` (system `> 15.5 V`) | over-charging; AC ripple corrupts references |

## Δ-signature (low → high idle sweep)

- `ΔVPWR < −1.0 V` under revs ⇒ alternator/regulator **diode** fault (rail sags as load rises).
- `ΔVPWR > +2.5 V` (system `> 15.5 V`) ⇒ **over-charging**; ripple injects noise into sensor
  references → routes to the alternator-AC-ripple node (`EP-FA-05`).

## Consumer / code path

OBDLab emits the scalar `control_module_voltage_v` (no verdict). COMLab's electrical-health
pre-check reads it and **down-weights/suppresses** sensor-fault candidates when the rail is out of
band, so a charging fault is not mis-routed as an O₂/MAF fault. AC ripple itself is *inferred*
downstream from ΔVPWR — VPWR is a scalar read, not a waveform.

Citation: 12.0/15.0 V bands and ΔVPWR signatures per AddObdFields §Part 2.2 + DataFlow.md; false
P0606-class behaviour per OEM service literature. Consumer PROPOSAL — EP-OBD-IN-04
(`perception_contradiction` electrical pre-check) + EP-FA-05 (alternator ripple node).


## Core Entities

- control_module_voltage_v, VPWR, DELTA_VPWR, P0606
- COMLab perception_contradiction electrical pre-check (T-COMV2-VPWR-GATE-1), EP-FA-05

## Graph relations (explicit)

**OBDLab** EMITS **control_module_voltage_v** (PID 0x42)
**control_module_voltage_v** CONSUMED_BY **COMLab electrical-health pre-check**
**VPWR** below 12.0V SUPPRESSES sensor-fault routing
**DELTA_VPWR** above +2.5V ROUTES_TO **EP-FA-05** alternator-ripple node
**VPWR** out-of-band CAUSES false **P0606**
**control_module_voltage_v** REFINES_CONTEXT_FOR **VREF_RAIL_COLLAPSE** and **ECU_CAPACITOR_LEAK**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
