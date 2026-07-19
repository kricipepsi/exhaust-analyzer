---
node_type: "wiki"
lab: "dnalab"
module: "dnalab"
subsystem: "vehicle-dna-envelope"
implements:
  - "labs/dnalab/dnalab/models.py"
consumers:
  - "comlab: OrchestratorInboundRequest.vehicle_dna ingestion"
drift_guards:
  - "labs/dnalab/tests/unit/test_models.py"
  - "labs/dnalab/tests/unit/test_vehicledna_roundtrip.py"
tags: [dnalab, finished, wiki]
source: "labs/dnalab/wiki/10_vehicle_dna_envelope.md"
---

# VehicleDNA Envelope — the five-key contract

**Disposition: reference-only.** This page mirrors the `VehicleDNA` dataclass in
`dnalab/models.py` and the §4.3 contract. It carries no measured numbers — only the
structural shape DNALab owns.

## The five top-level keys

`VehicleDNA` is a frozen dataclass whose JSON form is the contract surface COMLab ingests.
It has **exactly five** snake_case top-level keys (`SEMANTIC_CONTRACT.md §4.3`):

| Key | Type | Inner shape owned by |
|---|---|---|
| `session_id` | `str` | DNALab — see `13_session_identity.md` |
| `timestamp` | `str` | DNALab — see `13_session_identity.md` |
| `schema_version` | `str` | DNALab — see `11_schema_versioning.md` |
| `vin_dna` | object | VINLab (`VinDNA`) — see `../../vinlab/wiki/00_index.md` |
| `symptom_dna` | object | SymptomLab (`SymptomDNA`) — see `../../symptomlab/wiki/00_index.md` |

Renaming, adding, or dropping any top-level key is a **breaking contract change** and forces
a `SCHEMA_VERSION` bump.

## Why DNALab re-declares no inner field

DNALab is a **composer** (an assembler, not a decoder/validator/router). Serialization
delegates to each producer so the umbrella never duplicates field knowledge:

```
to_json_payload():
    return {
        "session_id":     self.session_id,
        "timestamp":      self.timestamp,
        "schema_version": self.schema_version,
        "vin_dna":        self.vin_dna.to_json_payload(),      # VINLab owns these fields
        "symptom_dna":    self.symptom_dna.to_json_payload(),  # SymptomLab owns these fields
    }
```

The consequence for this wiki: the physical (Part A) enums and the symptom/environmental
(Part B) vocabulary are **never** restated in `dnalab/` or in these notes. A field that
appears here but not on a producer would be an orphan and a boundary breach. Round-tripped
producer fields (`load_state` via `symptom_dna`, `rated_rpm` via `vin_dna`, the formalized
CoC fields) are present in the payload but **owned by the producers**, never re-declared
here.

## Forbidden in the envelope

| Token | Status |
|---|---|
| any `VinDNA` / `SymptomDNA` inner field re-declared in `dnalab/` | forbidden — delegate to each model's `to_json`/`from_json` |
| routing or physics literals in `dnalab/` | forbidden — DNALab is composition only |
| `fuel_type` in the envelope | not present — stayed a proposal (COMLab-E), not a landed producer field |
| a sixth top-level key | forbidden — exactly five, per §4.3 |

## Consumer (signal/noise)

The whole payload is consumed by COMLab as `OrchestratorInboundRequest.vehicle_dna` (a
local mirror; COMLab imports nothing from DNALab). That single consumer is what justifies
the envelope's existence. Field-level vocabulary tables live in `docs/DNA_VOCABULARY.md`;
the composition flow lives in `12_assembly_contract.md`.



## Graph relations (explicit)

**VehicleDNA** CONSUMED_BY **COMLab OrchestratorInboundRequest.vehicle_dna** (live — T-DNA-7)
**VehicleDNA** COMPOSES **VinDNA** (from VINLab) AND **SymptomDNA** (from SymptomLab)
**VehicleDNA.to_json_payload()** PRODUCES **5-key JSON contract** (session_id, timestamp, schema_version, vin_dna, symptom_dna)
**VehicleDNA 5-key envelope** DEFINED_BY **SEMANTIC_CONTRACT.md §4.3**
**VehicleDNA** VERIFIED_BY **dnalab/tests/unit/test_models.py** (10 tests: construction + serialization)
**VehicleDNA** VERIFIED_BY **dnalab/tests/unit/test_vehicledna_roundtrip.py** (5 tests: full round-trip)
**vin_dna inner fields** OWNED_BY **VINLab** (never re-declared in dnalab/)
**symptom_dna inner fields** OWNED_BY **SymptomLab** (never re-declared in dnalab/)
**fuel_type** IS_NOT present in VehicleDNA (PROPOSAL only — COMLab-E)
**6th top-level key** IS_FORBIDDEN (exactly 5 keys per §4.3)

## Core Entities

- `VehicleDNA` — frozen dataclass, 5-key envelope; CONSUMER: COMLab OrchestratorInboundRequest.vehicle_dna
- `VehicleDNA.to_json_payload()` — serialization to dict; CONSUMER: COMLab ingestion
- `VinDNA` — Part A payload; OWNER: VINLab
- `SymptomDNA` — Part B payload; OWNER: SymptomLab
- `SEMANTIC_CONTRACT.md §4.3` — governing schema spec
