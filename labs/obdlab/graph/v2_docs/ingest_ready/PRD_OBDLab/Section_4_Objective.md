> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 4 Objective · Parent document: PRD_OBDLab.md

## Section 4 — Objective

**Business benefit.** Provide ECU-perception data at the same abstraction level as GASLab's chemistry, so COMLab can compute a meaningful delta and route fault hypotheses.

**Customer benefit.** Technicians see validated, unit-normalised OBD data (fuel trims, VE, lambda, MAF linearity) in consistent units with known validity flags — no manual unit conversion, no guessing whether a value is in PSI or kPa.

### Entity: Key Results (6)

- **KR1** — Pipeline processes warm-idle HIGH-confidence DNA payload in < 50 ms on reference hardware
- **KR2** — `OBDLivePayload` structurally valid for all regression fixtures
- **KR3** — Zero cross-lab Python imports (import-isolation audit in `test_dna_view.py`)
- **KR4** — `physical_sensor_bounds.json` 12-field drift guard passes on every CI run (`test_sensor_bounds.py`)
- **KR5** — `O2FailureMode` taxonomy carries exactly 4 values (NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE); no pruned v1 member survives (`test_vocabulary.py`)
- **KR6** — Every payload field has a named consumer (live or forward-registered S4), per signal/noise (HLD §7)

## Graph relations (explicit)

**KR1** VERIFIES **pipeline latency < 50 ms** (warm idle, HIGH DNA)
**KR2** VERIFIES **OBDLivePayload structural validity** (regression fixtures)
**KR3** VERIFIES **0 cross-lab imports** (test_dna_view.py)
**KR4** VERIFIES **12-field drift guard** (test_sensor_bounds.py)
**KR5** VERIFIES **O2FailureMode = 4 values** (test_vocabulary.py scan)
**KR6** VERIFIES **every payload field has named consumer** (signal/noise, HLD §7)
