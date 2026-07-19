> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 5. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 5. Required Triage Keys (`assembly.py`)

```python
required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
```

Checked before the VIN decode. `load_state` joined the required set in T-DNA-7 (and is
passed through to `resolve()`). `free_text_notes` is **not** required (optional on
`SymptomDNA`) and is not forwarded by the assembly.

---

## Graph relations (explicit)

**build_vehicle_dna()** GATED_BY **required triage keys** (tier_1, tier_2, occurs_during, engine_state, load_state)
**load_state** CONSUMED_BY **symptomlab.resolve()** (triage pass-through since T-DNA-7)
**free_text_notes** DESCRIBES **not required, not forwarded** (accepted gap)
**triage pre-check** VERIFIES **fail-fast before VIN decode** (test_assembly.py)
