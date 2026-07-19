> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 5. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 5. Serialization & Version Guard

`to_json_payload()` emits the five keys, delegating `vin_dna.to_json()` and
`symptom_dna.to_json()` — DNALab never duplicates field knowledge. `to_json(**kwargs)`
is a thin `json.dumps` over the payload.

`from_json_payload(payload)` is the inverse:

```
incoming = payload.get("schema_version")
if incoming != SCHEMA_VERSION: raise ValueError(...)     # no silent cross-version load
return VehicleDNA(
    session_id=payload["session_id"], timestamp=payload["timestamp"],
    schema_version=payload["schema_version"],
    vin_dna=VinDNA.from_json(payload["vin_dna"]),
    symptom_dna=SymptomDNA.from_json(payload["symptom_dna"]),
)
```

A missing required top-level key raises `KeyError`; a version mismatch raises
`ValueError`. Reconstruction delegates to each model's `from_json`.

---

## Graph relations (explicit)

**VehicleDNA.to_json_payload()** DELEGATES_TO **VinDNA.to_json()**
**VehicleDNA.to_json_payload()** DELEGATES_TO **SymptomDNA.to_json()**
**VehicleDNA.from_json_payload()** GATED_BY **schema_version match** (ValueError on mismatch)
**VehicleDNA.from_json_payload()** GATED_BY **required top-level key presence** (KeyError on missing)
**VehicleDNA.from_json_payload()** DELEGATES_TO **VinDNA.from_json()**
**VehicleDNA.from_json_payload()** DELEGATES_TO **SymptomDNA.from_json()**
**SCHEMA_VERSION** CONSUMED_BY **from_json_payload version guard** (live, models.py)
