> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 1. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 1. Schema Version (`models.py`)

```python
SCHEMA_VERSION = "1.2"          # source: SEMANTIC_CONTRACT.md §4.3
```

The single coordinating constant. `from_json_payload` rejects any payload whose
`schema_version` differs (`ValueError`). T-DNA-7 bumped this `1.0 → 1.1` once upstream
field tasks landed; T-DNA-10 bumped it `1.1 → 1.2` for the `engine_state` wire-value
rename (`won_not_start` → `will_not_start`).

---

## Graph relations (explicit)

**SCHEMA_VERSION = "1.2"** OWNED_BY **dnalab/models.py**
**SCHEMA_VERSION** CONSUMED_BY **VehicleDNA.from_json_payload() mismatch guard** (live)
**SCHEMA_VERSION** CONSUMED_BY **COMLab generation detection** (live)
**SCHEMA_VERSION** DERIVED_FROM **T-DNA-7 (1.0→1.1) + T-DNA-10 (1.1→1.2)**
**SCHEMA_VERSION** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3**
