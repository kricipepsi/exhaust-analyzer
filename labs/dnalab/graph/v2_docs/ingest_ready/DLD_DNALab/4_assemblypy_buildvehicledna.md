> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 4. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 4. `assembly.py` — `build_vehicle_dna`

```python
build_vehicle_dna(vin: str, triage: dict[str, Any]) -> VehicleDNA
```

| Step | Detail |
|------|--------|
| required-key check | `("tier_1", "tier_2", "occurs_during", "engine_state")`; any missing → `SymptomValidationError` |
| Part A | `vinlab.decode(vin)` (imported as `_decode_vin`) — may raise `VINDecodeError` |
| Part B | `symptomlab.resolve(tier_1, tier_2, occurs_during, engine_state)` (imported as `_resolve_symptom`) — may raise `SymptomValidationError` |
| compose | `VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)` |

Imports: `from symptomlab.validator import SymptomValidationError`,
`from symptomlab import resolve as _resolve_symptom`,
`from vinlab import decode as _decode_vin`, `from dnalab.models import VehicleDNA`. These
are the **only** cross-module imports — both in-family.

---

## Graph relations (explicit)

**build_vehicle_dna()** CONSUMES **vinlab.decode(vin)** (Part A, imported as _decode_vin)
**build_vehicle_dna()** CONSUMES **symptomlab.resolve(**triage)** (Part B, imported as _resolve_symptom)
**build_vehicle_dna()** GATED_BY **required triage keys** (tier_1, tier_2, occurs_during, engine_state, load_state)
**SymptomValidationError** PROPAGATED_FROM **symptomlab** (missing triage key)
**VINDecodeError** PROPAGATED_FROM **vinlab** (invalid VIN)
**VehicleDNA.new()** CONSUMES **vin_dna + symptom_dna** (composition after decode + resolve)
**dnalab/assembly.py** DESCRIBES **the only cross-module imports** (both in-family)
