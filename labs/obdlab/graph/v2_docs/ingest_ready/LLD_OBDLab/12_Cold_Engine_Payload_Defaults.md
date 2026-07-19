> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 12 Cold-Engine Payload Defaults · Parent document: LLD_OBDLab.md

## 12. Cold-Engine Payload Defaults (`core/sensor_signal_translator.py`)

When the thermal gate fires (`rpm_bucket == COLD_OPEN_LOOP_INVALID`,
`analytics_frozen = True`):

```python
ve_pct                       = 0.0
maf_status                   = NodeMAFStatus.REAL_SENSOR_FEED
map_status                   = NodeMAPStatus.REAL_SENSOR_FEED
ve_validity                  = VEValidity.UNKNOWN
normalized_obd_lambda        = 1.0
o2_failure_mode              = O2FailureMode.NO_FAULT
total_trim_correction_delta  = 0.0
total_trim_correction_delta_b2 = None
per_bank_trim_delta          = None
```

`AnalyticsPreconditions` still runs and populates `trim_analytics_gate`
(it will return `ENGINE_COLD`). Not configurable in v1.

## Graph relations (explicit)

**SensorSignalTranslator.translate** GATED_BY **thermal freeze** (analytics_frozen = True when COLD_OPEN_LOOP_INVALID)
**thermal freeze defaults** ENUMERATES **ve_pct=0.0, normalized_obd_lambda=1.0, total_trim_correction_delta=0.0, o2_failure_mode=NO_FAULT, ve_validity=UNKNOWN** (safe stoichiometric defaults)
**trim_analytics_gate** DERIVED_FROM **ENGINE_COLD** (when thermal gate fires, preconditions still evaluate)
**test_pipeline_smoke.py** VERIFIES **cold-engine defaults** (integration)
