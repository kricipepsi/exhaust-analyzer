> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 2 schemas/vocabulary.py — 8 StrEnums · Parent document: DLD_OBDLab.md

## 2. `schemas/vocabulary.py` — 8 StrEnums

All values are wire-format strings consumed across lab boundaries
(`SEMANTIC_CONTRACT.md §4.4`). Renames are breaking changes. Drift-guarded by
`test_vocabulary.py`.

> Doc-bug note: the live module docstring still reads "7 StrEnums" — stale since
> `FuelSystemStatus` was added (T-OBDV2-6) bringing the count to 8. Logged as a
> docstring follow-up (FU-OBD-DOC-3); not fixed here (architect does not edit code).

### Entity: RpmStateBucket (4 members)

- **STABILIZED_IDLE** — Normal warm idle
- **REGULATORY_HIGH_IDLE** — High idle for emissions/diagnostics
- **STRESS_IDLE** — High-idle under load (A/C, alternator)
- **COLD_OPEN_LOOP_INVALID** — Cold engine, analytics frozen

### Entity: O2NormalizationMode (4 members)

- **NARROWBAND_VOLTAGE_TO_LAMBDA** — 3-zone voltage → lambda conversion
- **WIDEBAND_PASSTHROUGH** — Direct ratio passthrough from wideband sensor
- **WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA** — Wideband simulating narrowband voltage
- **O2_CHANNEL_FAULT** — Sentinel for out-of-range O2 input

### Entity: VEValidity (5 members)

- **VALID** — VE cross-check passes under dual-sensor gate
- **FAULT_VE_IDLE_COLLAPSE** — VE < 50% at idle with MAP > 45 kPa
- **FAULT_MAF_CONTAMINATION** — VE < 65% at stress with TFT > 15%
- **FAULT_VE_SENSOR_SKEW** — VE > 90% on NA engine at idle (supersedes Physics Gate 3)
- **UNKNOWN** — Single-sensor or missing inputs; VE evidence suppressed

### Entity: TrimAnalyticsGate (9 members)

- **VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, SEMANTIC_ERROR**

### Entity: NodeMAFStatus (2 members)

- **REAL_SENSOR_FEED** — MAF sensor directly read
- **VIRTUAL_EMULATION** — MAF emulated from MAP (MAP_ONLY branch)

### Entity: NodeMAPStatus (2 members)

- **REAL_SENSOR_FEED** — MAP sensor directly read
- **BACK_CALCULATED** — MAP inferred from MAF (MAF_ONLY branch)

### Entity: FuelSystemStatus (4 members)

- **CL** — Closed loop · **OL** — Open loop · **OL_DRIVE** — Open loop driving · **OL_FAULT** — Open loop fault
- `from_wire()` coerces legacy strings (`Closed_Loop`, `Open_Loop_Cold`, `Open_Loop_Fault`, `Open_Loop_Driving`) and short codes

### Entity: O2FailureMode (4 members)

- **NO_FAULT** — Normal operation · **STUCK_LEAN** — Voltage < 0.10 V · **STUCK_RICH** — Voltage > 0.90 V · **WIDEBAND_OFFSET_CANDIDATE** — Wideband offset detected (proposal EP-OBD-17)

**Changes from v1.0:**
- `VERoutingMode` **removed** — it duplicated `AirMeteringStrategy` (ARCH-2).
- `O2FailureMode` pruned 7 → 4: `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`,
  `HEATER_FAULT` removed (no consumer); `WIDEBAND_OFFSET_CANDIDATE` added
  (T-OBDV2-4 / EP-OBD-17).
- `FuelSystemStatus` **added** (T-OBDV2-6), mirrored from DTC_VOCABULARY §8 — no
  cross-lab import. `from_wire()` coerces legacy strings (`Closed_Loop`,
  `Open_Loop_Cold`, `Open_Loop_Fault`, `Open_Loop_Driving`) and short codes.

`HIGH_IDLE_LOAD` is forbidden throughout `obdlab/` (CI scan in
`test_vocabulary.py`); superseded by `REGULATORY_HIGH_IDLE` / `STRESS_IDLE`.

## Graph relations (explicit)

**schemas/vocabulary.py** ENUMERATES **RpmStateBucket** (4 members) · **O2NormalizationMode** (4) · **VEValidity** (5) · **TrimAnalyticsGate** (9) · **NodeMAFStatus** (2) · **NodeMAPStatus** (2) · **FuelSystemStatus** (4) · **O2FailureMode** (4)
**test_vocabulary.py** VERIFIES **vocabulary.py** (drift guard vs wiki)
**test_vocabulary.py** VERIFIES **HIGH_IDLE_LOAD absent** (codebase scan)
**FuelSystemStatus** MIRRORS_CONTRACT_IN **DTC_VOCABULARY §8** (local copy, no cross-lab import)
**O2FailureMode v2** SUPERSEDES **O2FailureMode v1** (SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT pruned, ARCH-2)
**VERoutingMode** SUPERSEDES **AirMeteringStrategy** (ARCH-2 — duplicate removed)
