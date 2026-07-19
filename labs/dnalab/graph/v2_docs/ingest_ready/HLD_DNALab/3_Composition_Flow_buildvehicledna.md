> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 3. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 3. Composition Flow (`build_vehicle_dna`)

```
build_vehicle_dna(vin, triage):
    required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
    missing  = [k for k in required if k not in triage]
    if missing: raise SymptomValidationError(...)        # fail fast, before the heavy decode
    physical    = vinlab.decode(vin)                      # VinDNA
    symptomatic = symptomlab.resolve(                     # SymptomDNA
        tier_1=triage["tier_1"], tier_2=triage["tier_2"],
        occurs_during=triage["occurs_during"], engine_state=triage["engine_state"],
        load_state=triage["load_state"],
    )
    return VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)
```

The triage-key check runs **first**, so an incomplete triage fails before VINLab does any
decode work. `free_text_notes` is not in the required set (it is optional on
`SymptomDNA`); the current assembly does not forward it (see §8).

---

## Graph relations (explicit)

**build_vehicle_dna()** GATED_BY **required triage keys** (tier_1, tier_2, occurs_during, engine_state, load_state)
**build_vehicle_dna()** CONSUMES **vinlab.decode(vin)** (Part A)
**build_vehicle_dna()** CONSUMES **symptomlab.resolve(**triage)** (Part B)
**SymptomValidationError** GATED_BY **missing triage key check** (fail-fast before decode)
**VehicleDNA.new()** CONSUMES **vin_dna + symptom_dna** (composition)
