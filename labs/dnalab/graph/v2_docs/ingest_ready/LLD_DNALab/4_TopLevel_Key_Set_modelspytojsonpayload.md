> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 4. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 4. Top-Level Key Set (`models.py::to_json_payload`)

```python
{"session_id", "timestamp", "schema_version", "vin_dna", "symptom_dna"}
```

Exactly five snake_case keys (`§4.3`). `vin_dna` / `symptom_dna` are produced by each
model's `to_json()` — DNALab never enumerates their inner fields.

---

## Graph relations (explicit)

**to_json_payload()** DESCRIBES **exactly five keys** (session_id, timestamp, schema_version, vin_dna, symptom_dna)
**to_json_payload()** DELEGATES_TO **vin_dna.to_json()**
**to_json_payload()** DELEGATES_TO **symptom_dna.to_json()**
**VehicleDNA** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3** (five-key set)
