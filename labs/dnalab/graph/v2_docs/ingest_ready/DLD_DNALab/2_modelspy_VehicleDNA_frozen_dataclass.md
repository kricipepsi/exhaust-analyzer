> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 2. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 2. `models.py` — `VehicleDNA` (frozen dataclass)

Schema governed by `SEMANTIC_CONTRACT.md §4.3`. Five top-level keys (snake_case).

### Field: `session_id`
- **Type**: `str`
- **Format**: `DNA_TX_<10 hex upper>`
- **Owned by**: DNALab
- **Consumed by**: COMLab `OrchestratorInboundRequest.vehicle_dna` session correlation (live)

### Field: `timestamp`
- **Type**: `str`
- **Format**: ISO-8601 UTC `%Y-%m-%dT%H:%M:%SZ`
- **Owned by**: DNALab
- **Consumed by**: COMLab `OrchestratorInboundRequest.vehicle_dna` temporal correlation (live)

### Field: `schema_version`
- **Type**: `str`
- **Value**: module constant `SCHEMA_VERSION = "1.2"`
- **Owned by**: DNALab
- **Consumed by**: COMLab schema-version gate (live); `from_json_payload` mismatch guard (live)
- **Derived from**: T-DNA-7 (1.0→1.1) + T-DNA-10 (1.1→1.2)

### Field: `vin_dna`
- **Type**: `VinDNA`
- **Owned by**: VINLab
- **Consumed by**: COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion (live, via VehicleDNA envelope)
- **Note**: Part A — physical identity

### Field: `symptom_dna`
- **Type**: `SymptomDNA`
- **Owned by**: SymptomLab
- **Consumed by**: COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion (live, via VehicleDNA envelope); COMLab `fault_atlas_router` symptom prior (PROPOSAL — COMLab-A)
- **Note**: Part B — operator symptom

`SCHEMA_VERSION = "1.2"` (module-level). T-DNA-7 bumped it `1.0 → 1.1` (new round-tripped fields); T-DNA-10 bumped it `1.1 → 1.2` (the `engine_state` wire-value rename).

### Classmethods / methods

#### `VehicleDNA.new(vin_dna, symptom_dna, *, session_id=None, timestamp=None, schema_version=SCHEMA_VERSION)`
- **Behaviour**: generates `session_id` (`DNA_TX_` + `uuid4().hex[:10].upper()`) and `timestamp` (`now(UTC)`) when not supplied
- **Owned by**: DNALab
- **Verifies**: session-id prefix `DNA_TX_` + ISO-8601 UTC timestamp format (test_assembly.py)

#### `VehicleDNA.to_json_payload() → dict`
- **Behaviour**: five keys; delegates `vin_dna.to_json()` / `symptom_dna.to_json()`
- **Owned by**: DNALab
- **Delegates to**: VinDNA.to_json(), SymptomDNA.to_json()

#### `VehicleDNA.to_json(**dumps_kwargs) → str`
- **Behaviour**: `json.dumps(to_json_payload(), **kwargs)`
- **Owned by**: DNALab

#### `VehicleDNA.from_json_payload(payload) → VehicleDNA`
- **Behaviour**: version guard + delegated `VinDNA.from_json` / `SymptomDNA.from_json`
- **Owned by**: DNALab
- **Verifies**: schema_version match (ValueError on mismatch); required top-level keys (KeyError on missing)

---

## Graph relations (explicit)

**VehicleDNA** OWNED_BY **DNALab**
**VehicleDNA** CONSUMED_BY **COMLab OrchestratorInboundRequest.vehicle_dna** (live)
**SCHEMA_VERSION "1.2"** CONSUMED_BY **COMLab schema-version gate** (live)
**SCHEMA_VERSION "1.2"** CONSUMED_BY **VehicleDNA.from_json_payload mismatch guard** (live)
**session_id** CONSUMED_BY **COMLab session correlation** (live)
**timestamp** CONSUMED_BY **COMLab temporal correlation** (live)
**vin_dna** OWNED_BY **VINLab**
**symptom_dna** OWNED_BY **SymptomLab**
**symptom_dna** CONSUMED_BY **COMLab fault_atlas_router** (PROPOSAL — COMLab-A, not live)
**VehicleDNA.to_json_payload()** DELEGATES_TO **VinDNA.to_json()**
**VehicleDNA.to_json_payload()** DELEGATES_TO **SymptomDNA.to_json()**
**VehicleDNA.from_json_payload()** VERIFIES **schema_version == SCHEMA_VERSION**
**VehicleDNA.new()** VERIFIES **session-id prefix DNA_TX_** (test_assembly.py)
**VehicleDNA.new()** VERIFIES **ISO-8601 UTC timestamp** (test_assembly.py)
**DLD_DNALab §2** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3**

