> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 4. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 4. `VehicleDNA` Envelope (`VehicleDNA.new`)

```
VehicleDNA.new(vin_dna, symptom_dna, *, session_id=None, timestamp=None, schema_version=SCHEMA_VERSION):
    session_id = session_id or  "DNA_TX_" + uuid4().hex[:10].upper()
    timestamp  = (timestamp or now(UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return VehicleDNA(session_id, timestamp, schema_version, vin_dna, symptom_dna)
```

Five top-level keys (`§4.3`): `session_id`, `timestamp`, `schema_version`, `vin_dna`,
`symptom_dna`. The dataclass is frozen. `SCHEMA_VERSION` is currently `"1.2"` (T-DNA-7
bumped 1.0→1.1 for the new round-tripped fields; T-DNA-10 bumped 1.1→1.2 for the
`engine_state` wire-value rename).

---

## Graph relations (explicit)

**VehicleDNA.new()** CONSUMES **VinDNA + SymptomDNA** (both halves)
**VehicleDNA** DESCRIBES **five top-level keys** (session_id, timestamp, schema_version, vin_dna, symptom_dna)
**SCHEMA_VERSION "1.2"** CONSUMED_BY **COMLab schema-version gate** (live)
**session_id** OWNED_BY **DNALab** (DNA_TX_ prefix)
**timestamp** OWNED_BY **DNALab** (ISO-8601 UTC)
**VehicleDNA** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3** (five-key contract)
