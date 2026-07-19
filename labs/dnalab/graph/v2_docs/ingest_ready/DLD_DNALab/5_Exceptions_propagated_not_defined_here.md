> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 5. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 5. Exceptions (propagated, not defined here)

DNALab defines no exception types of its own. It surfaces:

### Exception: `SymptomValidationError`
- **Origin**: symptomlab
- **When**: missing triage key; invalid pair/environmental value
- **Propagated via**: build_vehicle_dna triage pre-check + symptomlab.resolve()

### Exception: `VINDecodeError` (+ `ChassisNumberError`)
- **Origin**: vinlab
- **When**: malformed/out-of-scope VIN
- **Propagated via**: build_vehicle_dna → vinlab.decode()

### Exception: `ValueError`
- **Origin**: dnalab `from_json_payload`
- **When**: `schema_version` mismatch
- **Gated by**: SCHEMA_VERSION constant ("1.2")

### Exception: `KeyError`
- **Origin**: dnalab `from_json_payload`
- **When**: missing required top-level key

---

## Graph relations (explicit)

**SymptomValidationError** PROPAGATED_FROM **symptomlab** (build_vehicle_dna)
**VINDecodeError** PROPAGATED_FROM **vinlab** (build_vehicle_dna)
**ValueError** OWNED_BY **dnalab from_json_payload** (schema_version mismatch)
**KeyError** OWNED_BY **dnalab from_json_payload** (missing required key)
**dnalab** DESCRIBES **zero exception types of its own** (propagation-only)
**DLD_DNALab §5** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3**

