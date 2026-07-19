> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 3. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 3. `models.py` — `from_json_payload` contract

```python
incoming = payload.get("schema_version")
if incoming != SCHEMA_VERSION:
    raise ValueError(f"schema_version mismatch: expected {SCHEMA_VERSION!r}, got {incoming!r}")
return VehicleDNA(
    session_id=payload["session_id"],          # KeyError if absent
    timestamp=payload["timestamp"],
    schema_version=payload["schema_version"],
    vin_dna=VinDNA.from_json(payload["vin_dna"]),
    symptom_dna=SymptomDNA.from_json(payload["symptom_dna"]),
)
```

### Failure: `schema_version` ≠ `SCHEMA_VERSION`
- **Exception**: `ValueError`
- **Message**: `schema_version mismatch: expected '1.2', got '<incoming>'`
- **Gated by**: `from_json_payload` version guard (live, models.py)

### Failure: missing required top-level key
- **Exception**: `KeyError`
- **Gated by**: `from_json_payload` key presence check (live, models.py)

### Failure: invalid `vin_dna` / `symptom_dna` shape
- **Exception**: propagated from each model's `from_json` (`KeyError` / `SymptomValidationError`)
- **Gated by**: VinDNA.from_json / SymptomDNA.from_json

---

## Graph relations (explicit)

**VehicleDNA.from_json_payload()** GATED_BY **schema_version mismatch guard** (ValueError)
**VehicleDNA.from_json_payload()** GATED_BY **required top-level key presence** (KeyError)
**VehicleDNA.from_json_payload()** DELEGATES_TO **VinDNA.from_json()**
**VehicleDNA.from_json_payload()** DELEGATES_TO **SymptomDNA.from_json()**
**ValueError** ENUMERATES **schema_version mismatch failure mode**
**KeyError** ENUMERATES **missing required key failure mode**
**DLD_DNALab §3** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3**

