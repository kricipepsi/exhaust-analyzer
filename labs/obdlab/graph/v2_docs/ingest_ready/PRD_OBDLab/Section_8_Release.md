> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 8 Release · Parent document: PRD_OBDLab.md

## Section 8 — Release

### v2 Scope

All P0 features above. The v2 rework (T-OBDV2-0 through T-OBDV2-11) revived OBDLab as a pure emitter, expanded the payload from 21 to 31 fields, replaced the legacy O2 failure taxonomy with a 4-value consumer-backed classification, added FuelSystemStatus tracking, widened trim bounds to the OBD rail, removed Physics Gate 3, added MAF linearity monitoring, and established the guarded-emitters pattern for forward-registered COMLab consumers (HLD §7).

### Explicitly Deferred (v3 / COMLab Stage 4)

- `dna_view=None` fallback displacement for VE (currently returns `VEValidity.UNKNOWN`, `ve_pct=0.0`).
- Descriptive names for regression fixtures (currently `case_01`–`case_06`).
- Brittle relative-path assumption in `test_dna_view.py` (`../COMLab/docs/wiki/`).
- PID 0x44 `commanded_equivalence_ratio` λ-range bound (currently numeric check only; FU-ECU-2).

### Success Criteria (7)

1. KR1–KR6 all pass in CI.
2. All regression fixtures produce structurally valid `OBDLivePayload` (31 fields).
3. `HIGH_IDLE_LOAD` scan finds zero occurrences in `obdlab/`.
4. `O2FailureMode` scan finds zero occurrences of SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT in `obdlab/`.
5. No cross-lab Python imports (import-isolation audit).
6. `physical_sensor_bounds.json` 12-field drift guard passes.
7. Every payload field has a named consumer (live or forward-registered S4) per HLD §7.

## Graph relations (explicit)

**PRD §8** DESCRIBES **v2 scope** (T-OBDV2-0..11, 21→31 fields, 4-value O2FailureMode, FuelSystemStatus, trim widening, MAF linearity, guarded emitters)
**PRD §8** DESCRIBES **4 deferred items** (dna_view=None VE fallback, regression fixture names, relative-path assumption, FU-ECU-2 λ-range bound)
**PRD §8** ENUMERATES **7 success criteria** (KR1–KR6 + payload field consumer check)
**test_vocabulary.py** VERIFIES **success criteria 3+4** (HIGH_IDLE_LOAD + O2FailureMode scans)
**test_dna_view.py** VERIFIES **success criterion 5** (import isolation)
**test_sensor_bounds.py** VERIFIES **success criterion 6** (12-field drift guard)
