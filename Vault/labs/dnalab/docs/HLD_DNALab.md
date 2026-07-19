---
node_type: "hld"
lab: "dnalab"
module: "dnalab"
subsystem: "architecture"
implements: []
consumers:
  - "lld: labs/dnalab/docs/LLD_DNALab.md"
  - "dld: labs/dnalab/docs/DLD_DNALab.md"
  - "comlab: OrchestratorInboundRequest.vehicle_dna ingestion"
drift_guards: []
tags: [dnalab, finished, hld]
source: "labs/dnalab/docs/HLD_DNALab.md"
---
# HLD — DNALab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_DNALab v2.0
**Version:** 2.1
**Date:** 2026-06-12

> **Audit note (2026-06-11; refreshed 2026-06-12):** grounded in the live `dnalab/`
> package. DNALab is the umbrella composer of the DNA family; its design is deliberately
> thin. The schema bump is landed: `SCHEMA_VERSION = "1.2"` (T-DNA-7 → 1.1, T-DNA-10 →
> 1.2), `load_state` flows through `build_vehicle_dna`, and the upstream fields round-trip.

---

## 1. Responsibility

DNALab is the **assembly** of the DNA family. It composes `VinDNA` (Part A, VINLab) and
`SymptomDNA` (Part B, SymptomLab) plus session metadata into one `VehicleDNA` — the
contract-shaped payload COMLab ingests. It is a **composer, not a decoder/validator/
router**: each producer owns its own correctness; DNALab orchestrates, stamps identity,
and guarantees the joined payload round-trips. `VehicleDNA`'s schema is governed by
`SEMANTIC_CONTRACT.md §4.3`.

DNALab is the **only** lab that imports siblings: `dnalab → vinlab + symptomlab` (the one
allowed in-family direction). It does not import COMLab; COMLab mirrors `VehicleDNA`.

---

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

## 3. Composition Flow (`build_vehicle_dna`)

```
build_vehicle_dna(vin, triage):
    required = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
    missing  = [k for k in required if k not in triage]
    if missing: raise SymptomValidationError(...)        # fail fast, before the heavy decode
    physical    = vinlab.decode(vin)                      # VinDNA
    symptomatic = symptomlab.resolve(                     # SymptomDNA
        tier_1=triage["tier_1"], tier_2=triage["tier_2"],
        occurs_during=triage["occurs_during"], engine_state=triage["engine_state"],
        load_state=triage["load_state"],
    )
    return VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)
```

The triage-key check runs **first**, so an incomplete triage fails before VINLab does any
decode work. `free_text_notes` is not in the required set (it is optional on
`SymptomDNA`); the current assembly does not forward it (see §8).

---

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

## 6. Downstream Integration Point (consumer)

| `VehicleDNA` | Consumer | Status |
|--------------|----------|--------|
| whole payload | COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion | live mirror |
| `schema_version` | COMLab distinguishes the current `1.2` payload (new fields + renamed `engine_state` value) from legacy `1.0`/`1.1` | landed (T-DNA-7 → 1.1, T-DNA-10 → 1.2) |

> **Cross-lab note:** COMLab mirrors `VehicleDNA` and reconciles up to the §4.3 contract.
> DNALab is never blocked on COMLab; the version field is the signal COMLab keys off.

---

## 7. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Top-level contract keys | exactly 5 (`§4.3`) |
| Import direction | one-way `dnalab → vinlab + symptomlab`; no COMLab import |
| Round-trip fidelity | `from_json_payload(to_json_payload(x))` reconstructs an equal payload |
| Fail-fast | incomplete triage raises before the VIN decode |
| Version safety | cross-version load raises, never silently coerces |
| Signal/noise | every field has a named consumer (COMLab ingestion) |

---

## 8. Known Gaps / Accepted Behaviour

| ID | Description | Status |
|----|-------------|--------|
| T-DNA-7 | `SCHEMA_VERSION` bumped `1.0 → 1.1`; new upstream fields (`load_state`, `rated_rpm`, formalized CoC) round-trip via each producer's `to_json`/`from_json`; `load_state` is now a required `build_vehicle_dna` triage key passed through to `resolve()` | Done |
| `free_text_notes` | optional on `SymptomDNA`; the assembly does not forward it (it is not a `build_vehicle_dna` triage key) | Accepted (no named consumer) |
| Legacy-payload path | `from_json_payload` rejects any non-matching version (no upgrade-on-read); decided under T-DNA-7 | Decided (reject-with-message) |
| Transitive block | `build_vehicle_dna` → `symptomlab.resolve` → `SymptomValidator(len==18)` — the live catalog is now 18 pairs (T-DNA-8), so the validator constructs cleanly | Resolved (T-DNA-8) |
