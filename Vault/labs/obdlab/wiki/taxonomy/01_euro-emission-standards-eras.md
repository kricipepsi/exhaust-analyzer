---
chunk: taxonomy/01_euro-emission-standards-eras
topic: taxonomy
sources:
  - various/Vol6.md — Euro 1–6 limits table + three technological eras (1990–2000 / 2000–2010 / 2010–2020)
consumer: DNALab emissions-tier resolution → COMLab fault_atlas era gating. The resolved Euro tier sets which monitors/aftertreatment exist (wideband, GPF, e-thermostat) and which fault families are plausible.
consumer_status: PROPOSAL (era/tier gating not yet a fault_atlas input; names DNALab producer + fault_atlas reader)
provenance: sources/various/Vol6.md — era prose + standards table READABLE; some g/km cells stripped (flagged in formula wiki)
dedup: new — taxonomy pack was empty; complements taxonomy/02 era-case catalogue and sources/taxonomy/faultatlas.md (J2012 P-code families)
---

# Euro emission eras (1990–2020) as a DNA gate

The 1990–2020 fleet splits into three technology eras driven by tightening Euro limits;
the era determines which sensors/aftertreatment a vehicle has, which gates plausible
faults.

- **Era 1 (1990–2000, Euro 1→2):** early OBD-II transition; narrowband O₂; speed-density
  → MAF migration; distributor/early DIS ignition.
- **Era 2 (2000–2010, Euro 3→4):** mature OBD-II + CAN bus; wideband A/F sensors;
  COP ignition; advanced security (immobilisers).
- **Era 3 (2010–2020, Euro 5→6):** GDI + turbo; PM/PN limits introduced; GPF;
  map-controlled electronic thermostats; wastegate/bypass control.

> Euro 1 (Jan 1993) CO limit 2.72 g/km; Euro 2 (Jan 1997) 2.20 g/km; later-tier
> g/km cells were image-stripped in export — the era boundaries + dates survive.

## Logic / consumer
DNALab resolves the Euro tier from VIN/year; COMLab fault_atlas uses it to enable/
disable family branches (e.g. GPF-clog and HPFP faults only Era 3; distributor PIP
only Era 1). Prevents proposing an era-impossible fault. Pairs with EP-DNA-01/02.


## Core Entities

- Euro_Era_1, Euro_Era_2, Euro_Era_3
- DNALab tier resolution -> fault_atlas era gating (PROPOSAL)

## Graph relations (explicit)

**Euro_Era_1** HAS narrowband O2 and speed-density
**Euro_Era_2** HAS wideband and CAN bus
**Euro_Era_3** HAS GDI, GPF, and electronic thermostat
Euro tier RESOLVED_BY DNALab and CONSUMED_BY **fault_atlas** era gating
era gating PREVENTS era-impossible fault routing

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
