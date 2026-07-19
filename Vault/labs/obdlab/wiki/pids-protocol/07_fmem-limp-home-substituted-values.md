---
chunk: pids-protocol/07_fmem-limp-home-substituted-values
topic: pids-protocol
sources:
  - Advanced Automotive Fault Diagnosis (Tom Denton, 2nd ed., Elsevier 2006) §5.2.1 (FMEM safe-default example), §5.3.3 component monitoring
  - cardiagnosis (Marić 2013) — "spare program" fallback on O2-sensor failure (../../cardiagnosis_prepped.md §Electronic Engine Management)
consumer: obdlab `analytics_preconditions` — generalise the prerequisite-DTC gate of [[../fuel-trim/14_dtc-enable-criteria-and-blocking-codes]] beyond trim: when a sensor's circuit DTC is active, that sensor's PID is an FMEM substituted default (not a measurement), so demote ANY candidate that reads that PID before fault-atlas routing. Also lowers truth-perception `Perception_Reliability_Index`. The per-PID `value_is_fmem` flag (derived from active circuit DTCs) + its reader ship together (v2 forward-progress).
consumer_status: PROPOSAL
provenance: AdvAutomotiveFaultDiagnosis.txt §5.2.1/5.3.3 — readable prose; cardiagnosis spare-program fallback readable
related: [[06_readiness-monitors-and-absence-of-dtc-trust]], [[../fuel-trim/14_dtc-enable-criteria-and-blocking-codes]], [[../fuel-trim/08_validity-preconditions]], [[../truth-perception/02_lambda-delta-vector-and-scoring]]
dedup: fuel-trim/14's prerequisite-DTC gate is trim-specific (a bad MAF/ECT corrupts the inputs trim is computed from); pids-protocol/06 carries only a one-paragraph FMEM note. THIS chunk is the full, cross-PID generalisation — the *value* analogue of 06's *absence-of-DTC* gate.
---

# FMEM / limp-home: a reported PID value that is not a measurement

## The reliability principle

Chunk `06` qualifies a **missing DTC** (was the monitor ready?). This chunk
qualifies a **present PID value**: when a sensor faults, the PCM does not stop —
it switches to **failure mode effects management (FMEM)** and **substitutes a
safe default value** for that sensor so the car can limp to a workshop. A scan
tool then reports that **default**, which looks like a real reading but is a
fabricated constant. Ingesting an FMEM value as a measurement produces confident,
wrong inferences (e.g. a "normal" MAF that the ECU invented).

Denton §5.2.1 worked example: a P1101 "MAF out of self-test range" makes the
system default to a safe airflow value (FMEM) — sufficient to drive, not a
substitute for a serviceable MAF. cardiagnosis describes the same idea as the ECU
running on a "spare program" (RPM + air-quantity estimate) when the O2 sensor
fails.

## How 4DApp can detect it (no new sensor needed)

FMEM substitution is triggered by a sensor/circuit fault, which almost always
sets a **circuit DTC for that same sensor**. So FMEM is inferable from data
4DApp already ingests:

```text
value_is_fmem(pid) := a circuit/range DTC for pid's sensor is currently active
   e.g. P0101/2/3 (MAF) | P0107/8 (MAP) | P0112/3/7/8 (IAT/ECT)
        P0121/2/3 (TPS)  | P0131-0161 (O2) | P0335/6 (CKP)
   ⇒ the reported PID for that sensor is an FMEM default, not a measurement
```

## The gate (signal-noise)

Reader = `obdlab/obdlab/core/analytics_preconditions.py`:

- For each PID whose sensor has an **active circuit DTC**, set `value_is_fmem`
  and **demote every candidate that reads that PID** (the value is invented).
  This is the prerequisite-DTC gate of `fuel-trim/14` lifted out of the trim
  context and applied to **any** consumer of the PID (VE/air-strategy, rationality,
  ECU-perception delta, etc.).
- Pass the count of FMEM-defaulted PIDs to truth-perception
  `Perception_Reliability_Index` (more FMEM defaults ⇒ lower index).

Per signal/noise the derived `value_is_fmem` flag ships **only** with this reader;
register the generalisation in `comlab/config/proposals/` alongside (or as an
extension of) `fuel-trim/14`'s `prerequisite_dtc_gate` so the two are not two
separate half-gates.

## Caution

A sensor can fail **without** a circuit DTC (e.g. in-range "stuck/biased" fault —
see `o2-logic/03_failure-modes-taxonomy`). FMEM-by-active-DTC catches the common
out-of-range/circuit case only; biased-but-plausible values are handled by the
rationality cross-check (`02_maf-map-tps-rationality-p0068`) and truth-vs-perception
(`../truth-perception`), not by this gate.

Citation: FMEM safe-default substitution and the P1101 MAF example per Denton
§5.2.1; component/circuit monitoring per §5.3.3; spare-program O2 fallback per
cardiagnosis (Marić) Electronic Engine Management section.


## Core Entities

- value_is_fmem, FMEM, prerequisite_dtc_gate, P1101
- analytics_preconditions generalised gate (PROPOSAL)

## Graph relations (explicit)

active circuit DTC for a sensor SETS **value_is_fmem** for its PID
**value_is_fmem** PID IS substituted default, not a measurement
**value_is_fmem** DEMOTES candidates reading that PID
**value_is_fmem** GENERALISES **prerequisite_dtc_gate** beyond trim
**value_is_fmem** count LOWERS **Perception_Reliability_Index**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
