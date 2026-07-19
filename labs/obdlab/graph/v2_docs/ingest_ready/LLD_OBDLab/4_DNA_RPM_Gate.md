> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 4 DNA-RPM Gate · Parent document: LLD_OBDLab.md

## 4. DNA-RPM Gate (`core/pid_ingestion_validator.py`)

```python
_DNA_RPM_HEADROOM = 1.05  # wiki: §3 — 5% redline overshoot headroom

# HIGH confidence only, rated_rpm set:
if engine_rpm > rated_rpm * _DNA_RPM_HEADROOM:
    raise PIDValidationError(...)
```

Three-branch confidence: **HIGH** strict (raises), **PARTIAL** logs
`dna_check_downgraded` and falls through to static bounds, **NONE/None** skips
(static `[0, 8000]` only).

## Graph relations (explicit)

**_DNA_RPM_HEADROOM = 1.05** DESCRIBES **5% redline overshoot headroom** (# wiki: §3)
**PIDValidationError** GATED_BY **engine_rpm > rated_rpm × 1.05** (HIGH confidence only)
**VinConfidence.HIGH** CONSUMES **rated_rpm** (strict DNA-RPM ceiling)
**VinConfidence.PARTIAL** CONSUMES **log + fallthrough to static bounds** (non-blocking)
**VinConfidence.NONE** CONSUMES **static [0, 8000] only** (DNA-RPM gate skipped)
**test_pid_ingestion_validator.py** VERIFIES **DNA-RPM three-branch gate** (unit tests)
