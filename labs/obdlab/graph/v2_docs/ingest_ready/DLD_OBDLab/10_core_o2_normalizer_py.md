> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 10 core/o2_normalizer.py · Parent document: DLD_OBDLab.md

## 10. `core/o2_normalizer.py` — `O2Normalizer`

`normalize(pids, dna_view) → (lambda, O2NormalizationMode, O2FailureMode)`.
Branches on `upstream_o2_type` (see HLD §5). The wideband branch additionally
flags `WIDEBAND_OFFSET_CANDIDATE` when warm + closed-loop + not WOT + not DFCO
and `|ratio − 1.0| > 0.05`. Reuses `ECT_WARM_THRESHOLD` and
`WOT_THROTTLE_THRESHOLD` imported from `analytics_preconditions` (single source).

## Graph relations (explicit)

**O2Normalizer.normalize** CONSUMES **upstream_o2_type** (O2 normalisation path)
**O2Normalizer.normalize** CONSUMES **pid_oxygen_sensor_volts** (narrowband path)
**O2Normalizer.normalize** CONSUMES **pid_wideband_equivalence_ratio** (wideband path)
**O2Normalizer.normalize** CONSUMES **ECT_WARM_THRESHOLD** / **WOT_THROTTLE_THRESHOLD** (from analytics_preconditions, single source)
**O2Normalizer.normalize** ENUMERATES **O2NormalizationMode** (NARROWBAND_VOLTAGE_TO_LAMBDA, WIDEBAND_PASSTHROUGH, WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2_CHANNEL_FAULT)
**O2Normalizer.normalize** ENUMERATES **O2FailureMode** (NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE)
**COMLab T-COMV2-O2OFFSET-1** CONSUMES **o2_failure_mode.WIDEBAND_OFFSET_CANDIDATE** (S4 forward-reg, proposal EP-OBD-17)
**test_o2_normalizer.py** VERIFIES **O2Normalizer** (unit tests)
