---
chunk_id: DNAWIKI-12
title: "Assembly contract — build_vehicle_dna()"
lab: dnalab
node_type: wiki
module: dnalab
subsystem: assembly-contract
implements:
  - "labs/dnalab/dnalab/assembly.py"
consumers:
  - "comlab: labs/comlab/comlab/schemas/ingestion.py OrchestratorInboundRequest (inbound assembly)"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state triage)"
drift_guards:
  - "labs/dnalab/tests/unit/test_assembly.py"
  - "labs/dnalab/tests/unit/test_assembly_integration.py"
tags: [dnalab, wiki, assembly-contract]
source: "labs/dnalab/wiki/12_assembly_contract.md"
doc: DNA_WIKI
role: reference-only
status: authoritative
date: 2026-06-12
kg_ingestion: none
mirrors: "dnalab/assembly.py (build_vehicle_dna)"
related_chunks: [DNAWIKI-00, DNAWIKI-10, DNAWIKI-13]
---

# Assembly contract — `build_vehicle_dna()`

**Disposition: reference-only.** Mirrors `dnalab/assembly.py`. The single public entry point
of the lab; carries no measured numbers.

## Signature & contract

```
build_vehicle_dna(vin: str, triage: dict) -> VehicleDNA
```

- `vin` — a 17-char VIN string, passed **verbatim** to `vinlab.decode()`.
- `triage` — a dict that must contain the five required keys below, passed to
  `symptomlab.resolve()`.

## Flow (fail-fast order matters)

```
build_vehicle_dna(vin, triage):
    required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
    missing  = [k for k in required if k not in triage]
    if missing:
        raise SymptomValidationError(...)     # [1] BEFORE any decode work
    physical    = vinlab.decode(vin)          # [2] VinDNA   (Part A) — may raise VINDecodeError
    symptomatic = symptomlab.resolve(         # [3] SymptomDNA (Part B) — may raise SymptomValidationError
        tier_1=triage["tier_1"], tier_2=triage["tier_2"],
        occurs_during=triage["occurs_during"], engine_state=triage["engine_state"],
        load_state=triage["load_state"],
    )
    return VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)   # [4] stamp identity + join
```

The triage-key check runs **first**, so an incomplete triage fails *before* VINLab does the
heavy decode. `free_text_notes` is optional on `SymptomDNA` and is **not** a required triage
key; the current assembly does not forward it (no named consumer — accepted gap).

## Errors

| Raised | When |
|---|---|
| `SymptomValidationError` | a required triage key is missing (raised in assembly, before decode); or the triage selection is itself invalid (raised by `symptomlab.resolve`) |
| `VINDecodeError` | the VIN is invalid or out of scope (raised by `vinlab.decode`) |

## Import boundary (one-way, in-family)

DNALab is the **only** lab that imports siblings, and only in this direction:

```
dnalab  ──imports──▶  vinlab + symptomlab        (the one allowed in-family direction)
dnalab  ──✗ never──▶  comlab / gaslab / obdlab / dtclab
comlab  ──mirrors VehicleDNA locally; imports nothing from dnalab
```

No lab imports DNALab except via this assembly. DNALab imports no COMLab. This keeps each
lab an isolated codebase joined only through typed JSON boundaries.

## Consumer (signal/noise)

The returned `VehicleDNA` is consumed whole by COMLab (`OrchestratorInboundRequest`). Each
field's correctness is the producer's responsibility; DNALab's job is orchestration,
identity stamping, and a clean JSON round-trip (`from_json_payload(to_json_payload(x))`
reconstructs an equal payload).



## Graph relations (explicit)

**build_vehicle_dna()** PRODUCES **VehicleDNA** (combined Part A + Part B + session metadata)
**build_vehicle_dna()** VERIFIES **triage required keys** (tier_1, tier_2, occurs_during, engine_state, load_state)
**build_vehicle_dna()** IMPORTS **vinlab.decode()** (Part A — VIN → VinDNA)
**build_vehicle_dna()** IMPORTS **symptomlab.resolve()** (Part B — triage → SymptomDNA)
**engine_state** CONSUMED_BY **COMLab symptom_router.route_symptom()** (live — T-DNA-10)
**triage key check** RUNS_BEFORE **vinlab.decode()** (fail-fast: incomplete triage never reaches VINLab)
**missing triage keys** RAISE **SymptomValidationError** (raised in assembly, before decode)
**invalid VIN** RAISES **VINDecodeError** (raised by vinlab.decode)
**free_text_notes** IS_NOT forwarded by assembly (no named consumer — accepted gap)
**build_vehicle_dna** VERIFIED_BY **dnalab/tests/unit/test_assembly.py** (11 tests)
**build_vehicle_dna** VERIFIED_BY **dnalab/tests/unit/test_assembly_integration.py** (real-pipeline smoke, env-gated)
**DNALab → VINLab + SymptomLab import** IS_THE only cross-lab import direction (one-way, in-family)

## Core Entities

- `build_vehicle_dna()` — sole public entry point; CONSUMER: COMLab (via VehicleDNA envelope)
- `triage required keys` — tier_1, tier_2, occurs_during, engine_state, load_state; CONSUMER: symptomlab.resolve()
- `engine_state` — triage key; CONSUMER: COMLab symptom_router.route_symptom()
- `SymptomValidationError` — raised on missing/invalid triage; CONSUMER: COMLab error handling
- `VINDecodeError` — raised on invalid VIN; CONSUMER: COMLab error handling
