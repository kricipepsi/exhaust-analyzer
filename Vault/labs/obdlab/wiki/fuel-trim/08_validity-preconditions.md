---
chunk: fuel-trim/08_validity-preconditions
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §8 (user procedure)
  - master_fuel_trim_guide.md §9 (engine preconditions)
consumer: COMLab `fuel_trim_invalid` gate — when any precondition fails the engine flags fuel_trim_invalid and demotes all trim-derived candidates before fault-atlas routing
consumer_status: active
dedup: canonical precondition list; the closed-loop/ECT/DFCO checks are referenced by 06_trim-rails-and-sentinels
---

# Validity preconditions for trim interpretation

## Capture procedure (4D app user)

1. Confirm closed loop: read `fuel_sys_status` — must equal **CL** (closed loop) for trim
   values to be meaningful. The status is a 4-value enum **`CL` / `OL` / `OL_DRIVE` / `OL_FAULT`**
   (closed loop / open-loop base map / open-loop driving e.g. WOT-decel / open-loop fault). OBDLab
   carries its **own manual-entry dropdown** for this (mirroring DTCLab's `FuelSystemStatus`,
   locally mirrored — no cross-lab import) because a DTC is not always set and DTCLab may not be in
   the session, so loop state cannot depend on DTCLab (audit RQ-D; field `fuel_system_status`,
   `T-OBDV2-6`).
2. Warm engine to ECT ≥ ~80 °C.
3. Record STFT and LTFT for **both banks at idle**.
4. Raise to steady 2500–3000 RPM (or hold 60–80 km/h cruise). Record again.
5. Map the pattern against `04_trim-pattern-decision-tree`.
6. If all trims within ±10 % and both banks match, the fuel-control system is fine
   — look elsewhere (gas chemistry, mechanical, ignition).

## Preconditions the engine validates before consuming trim

The engine must confirm **all** of these; if any fails it raises
`fuel_trim_invalid` and demotes every trim-derived candidate:

- ECT ≥ **70 °C** (cold-start enrichment masks real trims).
- `fuel_sys_status = CL` (closed loop).
- No active **P0130–P0161** (O₂ sensor faults invalidate trims).
- No active **P0335 / P0340** (CKP/CMP failure → batch fire / open loop).
- Time since last `codes_cleared = true`: ≥ **1 drive cycle**.
- WOT not engaged (open-loop power enrichment).
- DFCO not active (fuel cut → no trim update).

**Consumer note.** `fuel_trim_invalid` is the gate every other fuel-trim chunk
sits behind: ranges (`03`), decision tree (`04`), bank comparison (`05`), and
truth-vs-perception (`07`) are only consulted when this gate passes. Pairs with
the rails/sentinel demotions in `06_trim-rails-and-sentinels`.

Citation: ECT/closed-loop/DFCO/WOT preconditions per master_fuel_trim_guide.md §9;
P0130–P0161 / P0335 / P0340 per SAE J2012 / ISO 15031-6.


## Core Entities

- fuel_trim_invalid, FuelSystemStatus.CLOSED_LOOP, FuelSystemStatus.OPEN_LOOP, FuelSystemStatus.OL_DRIVE, FuelSystemStatus.OL_FAULT
- ECT, P0130, P0161, P0335, P0340, DFCO_ACTIVE, WOT_ACTIVE
- COMLab fuel_trim_invalid gate (consumer, active); fuel_system_status field (T-OBDV2-6)

## Graph relations (explicit)

**fuel_trim_invalid** GATES ranges, decision-tree, bank-comparison, and crosscheck chunks
**fuel_sys_status** not **FuelSystemStatus.CLOSED_LOOP** RAISES **fuel_trim_invalid**
**P0130** through **P0161** RAISES **fuel_trim_invalid**
**P0335** and **P0340** RAISE **fuel_trim_invalid**
**DFCO_ACTIVE** SUPPRESSES trim update
**fuel_system_status** dropdown ADDED_BY **T-OBDV2-6**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
