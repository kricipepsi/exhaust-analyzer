> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 2. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 2. Architecture Position

```
app composition layer (VIN string + triage dict)
  │  dnalab.build_vehicle_dna(vin, triage)
  ▼
dnalab.assembly.build_vehicle_dna
  │  [1] check required triage keys      else SymptomValidationError (before decode)
  │  [2] vinlab.decode(vin)              → VinDNA        (Part A)   — may raise VINDecodeError
  │  [3] symptomlab.resolve(**triage)    → SymptomDNA    (Part B)   — may raise SymptomValidationError
  │  [4] VehicleDNA.new(vin_dna, symptom_dna)
  ▼
VehicleDNA  (session_id, timestamp, schema_version, vin_dna, symptom_dna)
  │  to_json_payload() / from_json_payload()
  ▼
COMLab OrchestratorInboundRequest.vehicle_dna  (separate codebase; mirrors VehicleDNA)
```

Imports flow one way (`dnalab → vinlab + symptomlab`); no lab imports DNALab except via
this assembly, and DNALab imports no COMLab.

---

## Graph relations (explicit)

**dnalab.build_vehicle_dna()** ROUTES_TO **vinlab.decode()** (Part A — VinDNA)
**dnalab.build_vehicle_dna()** ROUTES_TO **symptomlab.resolve()** (Part B — SymptomDNA)
**VehicleDNA** ROUTES_TO **COMLab OrchestratorInboundRequest.vehicle_dna** (downstream ingestion)
**VehicleDNA.to_json_payload() / from_json_payload()** DESCRIBES **the serialization bridge to COMLab**
