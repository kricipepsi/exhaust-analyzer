> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 7 VE Validity Classification · Parent document: LLD_OBDLab.md

## 7. VE Validity Classification (`core/ve_engine.py::_classify_validity`)

Source: `OBDLab_KG_Wiki.md §6.4`. Thresholds:

```python
_CUTOFF_VE_COLLAPSE       = 50.0  # VE% — idle collapse floor
_CUTOFF_MAP_COLLAPSE      = 45.0  # MAP kPa — must exceed for collapse trigger (BP §2)
_CUTOFF_VE_CONTAMINATION  = 65.0  # VE% — MAF contamination floor
_CUTOFF_TFT_CONTAMINATION = 15.0  # TFT% — contamination requires trim above this
_CUTOFF_VE_SKEW           = 90.0  # VE% — sensor skew ceiling
```

### Entity: VE validity fault triggers

- **FAULT_VE_IDLE_COLLAPSE** — `bucket==STABILIZED_IDLE AND ve<50 AND map>45`
- **FAULT_MAF_CONTAMINATION** — `bucket∈{STRESS_IDLE, REGULATORY_HIGH_IDLE} AND ve<65 AND tft>15`
- **FAULT_VE_SENSOR_SKEW** — `bucket==STABILIZED_IDLE AND ve>90 AND induction==NATURALLY_ASPIRATED`
- **VALID** — otherwise

`FAULT_VE_SENSOR_SKEW` is the replacement for the removed Physics_Gate_3
(FIX-1 Option B). When `total_trim_correction_delta` is not yet on the dict,
`_classify_validity` recomputes TFT from `shrtft1 + longft1`.

## Graph relations (explicit)

**_classify_validity** ENUMERATES **_CUTOFF_VE_COLLAPSE=50.0, _CUTOFF_MAP_COLLAPSE=45.0, _CUTOFF_VE_CONTAMINATION=65.0, _CUTOFF_TFT_CONTAMINATION=15.0, _CUTOFF_VE_SKEW=90.0** (# wiki: §6.4)
**_classify_validity** ENUMERATES **FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW, VALID** (4 fault triggers)
**FAULT_VE_SENSOR_SKEW** SUPERSEDES **Physics_Gate_3** (FIX-1 Option B, NA VE ceiling)
**_classify_validity** CONSUMES **induction_type** (NATURALLY_ASPIRATED check for FAULT_VE_SENSOR_SKEW)
**_classify_validity** CONSUMES **total_trim_correction_delta** (or recomputes from shrtft1+longft1)
**test_ve_engine.py** VERIFIES **_classify_validity** (unit tests)
