---
chunk: taxonomy/02_era-fault-case-catalogue
topic: taxonomy
sources:
  - various/Vol4.md — 30 era/make no-start + driveability cases
  - various/Vol6.md — chronological fault cases by era
  - various/Vol8.md — comparative powertrain failures 1990–2020 (misfire/DTC focus)
consumer: COMLab fault_atlas make/era priors — a prior-probability layer that weights candidates by the vehicle's era + manufacturer known-failure patterns (e.g. Ford FPDM corrosion, Chrysler TIPM relay, BMW HPFP/Valvetronic).
consumer_status: PROPOSAL (make/era prior layer not in v2; names fault_atlas consumer)
provenance: sources/various/Vol4.md/Vol6.md/Vol8.md — case prose + DTC tables READABLE (Vol4 has surviving LaTeX); some Vol6 standards cells stripped
dedup: new; the named failures map onto sources/taxonomy/faultatlas.md J2012 families (P01xx–P06xx)
---

# Era / make fault-case catalogue (priors)

A library of era- and manufacturer-specific known failures, usable as a prior layer
over the standards-based J2012 routing (sources/taxonomy/faultatlas.md).

## Representative entries (full set in Vol4/Vol6/Vol8)

- **Era 1:** GM Passlock/Passkey security no-start; Ford TFI PIP & PATS; CKP VR thermal
  dropout; Honda PGM-FI main-relay solder; Toyota NE/G pickup-coil; FPR diaphragm rupture.
- **Era 2:** Ford FPDM corrosion; Chrysler TIPM internal-relay; Volvo/Magneti-Marelli
  ETM; BMW N54 HPFP; Nissan CKP/CMP solder; VW/Audi 2.0T TSI timing-chain jump; Toyota
  A/F heater cold-start lock-out.
- **Era 3:** GM GDI high-resistance injector & FRP voltage drift; VW TSI intake-valve
  carbon; Hyundai/Kia Theta II CKP internal short; Ford EcoBoost diverter-valve rupture;
  Mazda SkyActiv purge-solenoid stuck open.

## Logic / consumer
Each entry ties a (make, era, symptom) tuple to a J2012 family + the discriminating
Mode-06/FF or gas signature (cross-ref pids-protocol/01). COMLab fault_atlas can apply
these as priors to rank candidates — a forward-progress proposal, not a live node yet.


## Core Entities

- era-make priors, J2012 families
- fault_atlas make/era prior layer (PROPOSAL)

## Graph relations (explicit)

**era-make-priors** WEIGHT **fault_atlas** candidates
each (make, era, symptom) MAPS_TO a J2012 family
**era-fault-case-catalogue** PAIRS_WITH **pids-protocol/01** Mode06/FF

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
