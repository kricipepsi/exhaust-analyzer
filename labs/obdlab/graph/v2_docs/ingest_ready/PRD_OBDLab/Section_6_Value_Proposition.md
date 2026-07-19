> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 6 Value Proposition · Parent document: PRD_OBDLab.md

## Section 6 — Value Proposition

- **Jobs addressed:** PID validation, unit conversion, VE computation, O2 lambda normalisation, fuel-trim aggregation, trim analytics validity gating, O2 failure mode classification, MAF linearity monitoring, per-cylinder misfire counting.
- **Gains created:** `total_trim_correction_delta` (STFT+LTFT) is computed and validated in one call. `ve_validity` (VEValidity enum) tells COMLab immediately whether VE is trustworthy. `per_bank_trim_delta` exposes bank-to-bank asymmetry. `lambda_perception_delta` quantifies ECU-vs-commanded deviation. `w_theo` and `sensor_error_delta` provide MAF linearity evidence from a two-point (idle + stress) accumulator. Cold-engine state is detected and frozen gracefully.
- **Pains relieved:** Eliminates manual unit conversion (°F, PSI, inHg, lb/min). Bank-2 null contract enforcement prevents silent downstream errors on single-bank engines. OBD-rail trim bounds (±127, per T-W-6) preserve sensor-fault signalling that narrower nominal bounds would discard.
- **Competitive advantage:** 3-branch VE routing handles MAF-only, MAP-only, and dual-sensor strategies. O2 normalisation supports narrowband voltage, wideband linear, and wideband NB-sim sensors in one module. MAF linearity monitoring adds an independent sensor-health channel. The emitter-only stance means OBDLab ships evidence without coupling to COMLab's verdict logic.

## Graph relations (explicit)

**OBDLab** DESCRIBES **9 jobs addressed** (PID validation → misfire counting)
**OBDLivePayload** DESCRIBES **key gains** (trim_delta, ve_validity, per_bank_trim_delta, lambda_perception_delta, w_theo, sensor_error_delta)
**PIDIngestionValidator** DESCRIBES **pains relieved** (manual unit conversion elimination, bank-2 null contract)
**VEEngine / O2Normalizer / maf_linearity** DESCRIBES **competitive advantage** (3-branch VE, 3-mode O2, MAF linearity, emitter-only stance)
