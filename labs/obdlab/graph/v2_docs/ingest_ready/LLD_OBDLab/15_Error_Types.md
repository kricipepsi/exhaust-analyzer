> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 15 Error Types · Parent document: LLD_OBDLab.md

## 15. Error Types

### Entity: OBDLab error hierarchy

- **PIDValidationError (ObdLabError)** — raised when: bounds violation; DNA-RPM HIGH breach; bank-2 null contract; non-numeric PID; invalid fuel-status / misfire / cell-vector input
- **SemanticConsistencyError (ObdLabError)** — raised when: Physics_Gate_1 / 2 / 4 violation
- **Pydantic `ValidationError`** — raised when: `OBDLivePayload` field-constraint violation at assembly

## Graph relations (explicit)

**PIDValidationError** DERIVED_FROM **ObdLabError** (unified root, FIX-5)
**SemanticConsistencyError** DERIVED_FROM **ObdLabError** (unified root, FIX-5)
**PIDValidationError** DESCRIBES **bounds violation, DNA-RPM HIGH breach, bank-2 null contract, non-numeric PID, invalid fuel-status/misfire/cell-vector**
**SemanticConsistencyError** DESCRIBES **Physics_Gate_1/2/4 violation**
**Pydantic ValidationError** DESCRIBES **OBDLivePayload field-constraint violation at assembly**
**COMLab except ObdLabError** CONSUMES **ObdLabError hierarchy** (single catch)
