> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 5 core/exceptions.py · Parent document: DLD_OBDLab.md

## 5. `core/exceptions.py`

```python
class ObdLabError(Exception): ...                       # unified root (FIX-5)
class PIDValidationError(ObdLabError): ...
class SemanticConsistencyError(ObdLabError): ...
```

**Changed from v1.0:** the hierarchy was reparented from stdlib bases
(`ValueError` / `AssertionError`) to a single `ObdLabError` root so COMLab's
fusion error-handling path can catch the whole family with one `except`.

## Graph relations (explicit)

**ObdLabError** OWNED_BY **OBDLab** (unified root, FIX-5)
**PIDValidationError** DERIVED_FROM **ObdLabError** (bounds, DNA-RPM, bank-2 contract, non-numeric PID, invalid fuel-status/misfire/cell-vector)
**SemanticConsistencyError** DERIVED_FROM **ObdLabError** (Physics_Gate_1/2/4 violation)
**ObdLabError v2** SUPERSEDES **ValueError/AssertionError** (v1.0 stdlib bases reparented, FIX-5)
**COMLab except ObdLabError** CONSUMES **ObdLabError hierarchy** (single-parent catch)
