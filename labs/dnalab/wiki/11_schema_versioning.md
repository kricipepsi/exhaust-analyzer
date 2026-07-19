---
chunk_id: DNAWIKI-11
title: "Schema versioning & the version guard"
lab: dnalab
node_type: wiki
module: dnalab
subsystem: schema-versioning
implements:
  - "labs/dnalab/dnalab/models.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py check_schema_version (request.metadata.schema_version vs MIN_SUPPORTED_SCHEMA_VERSION; ERR-ABORT-005)"
drift_guards:
  - "labs/dnalab/tests/unit/test_models.py"
tags: [dnalab, wiki, schema-versioning]
source: "labs/dnalab/wiki/11_schema_versioning.md"
doc: DNA_WIKI
role: reference-only
status: authoritative
date: 2026-06-12
kg_ingestion: none
mirrors: "dnalab/models.py (SCHEMA_VERSION, from_json_payload)"
related_chunks: [DNAWIKI-00, DNAWIKI-10, DNAWIKI-12]
---

# Schema versioning & the version guard

**Disposition: reference-only.** Mirrors `SCHEMA_VERSION` and `from_json_payload` in
`dnalab/models.py`. The version token is a **structural constant**, not a measured value —
it needs no wiki citation.

## The token

```python
SCHEMA_VERSION = "1.2"   # module constant in dnalab/models.py
```

`VehicleDNA.new(...)` stamps this onto every payload it builds (callers may override it
explicitly, but the default is `SCHEMA_VERSION`).

## History

| From → To | Task | What changed |
|---|---|---|
| `1.0 → 1.1` | T-DNA-7 | New upstream fields began round-tripping: `load_state` (via `symptom_dna`), `rated_rpm` (via `vin_dna`), and the formalized CoC fields. DNALab added no field of its own — the producers did; the bump records that the joined payload now carries them. |
| `1.1 → 1.2` | T-DNA-10 | The `engine_state` wire value was renamed (`won_not_start` → `will_not_start`). A value-level rename in a producer enum is still a wire-format change, so the umbrella version moved. |

`SCHEMA_VERSION` is the single signal COMLab keys off to distinguish a current `1.2` payload
(new fields + renamed `engine_state` value) from a legacy `1.0`/`1.1` one.

## The version guard (no silent cross-version load)

`from_json_payload` rejects any payload whose `schema_version` does not match — there is
**no upgrade-on-read**:

```
from_json_payload(payload):
    incoming = payload.get("schema_version")
    if incoming != SCHEMA_VERSION:
        raise ValueError(... expected SCHEMA_VERSION, got incoming ...)
    return VehicleDNA(
        session_id=payload["session_id"], timestamp=payload["timestamp"],
        schema_version=payload["schema_version"],
        vin_dna=VinDNA.from_json(payload["vin_dna"]),          # delegated
        symptom_dna=SymptomDNA.from_json(payload["symptom_dna"]),  # delegated
    )
```

- A **version mismatch** raises `ValueError` (decided under T-DNA-7: reject-with-message,
  not coerce).
- A **missing required top-level key** raises `KeyError`.
- Reconstruction of the inner objects is **delegated** to each producer's `from_json` —
  DNALab never re-parses producer fields.

## Forward note (deferred)

The future two-tier output decision (`full` | `basic`, retiring `PARTIAL`) will interact
with this guard: legacy `PARTIAL` payloads would need an explicit reject-or-migrate rule, and
any field move/rename it implies would bump `SCHEMA_VERSION` again. That decision is
marked down only — see `../research/DEFERRED_full_basic_dataset_decision.md` and the VIN
evidence in `93_vin_decode_resolution.md`. **Nothing is decided here.*


## Graph relations (explicit)

**SCHEMA_VERSION** DEFINED_IN **dnalab/models.py** (module constant, "1.2")
**SCHEMA_VERSION** CONSUMED_BY **COMLab schema-version gate** (OrchestratorInboundRequest ingestion — T-DNA-7)
**VehicleDNA.from_json_payload()** VERIFIES **schema_version match** (mismatch raises ValueError)
**VehicleDNA.new()** STAMPS **SCHEMA_VERSION** onto every payload (default, overridable)
**SCHEMA_VERSION "1.2"** RECORDS **wire-format change** (T-DNA-10: engine_state value rename)
**schema_version mismatch** RAISES **ValueError** (reject-with-message, not coerce — T-DNA-7)
**from_json_payload** VERIFIED_BY **dnalab/tests/unit/test_models.py::test_from_json_payload_rejects_wrong_schema_version**
**from_json_payload** VERIFIED_BY **dnalab/tests/unit/test_models.py::test_schema_version_value**
**missing top-level key** RAISES **KeyError** (no silent None-fill)
**inner object reconstruction** DELEGATED_TO **VinDNA.from_json()** AND **SymptomDNA.from_json()**

## Core Entities

- `SCHEMA_VERSION` — module constant "1.2"; CONSUMER: COMLab schema-version gate
- `VehicleDNA.from_json_payload()` — deserialization with strict-match guard; CONSUMER: COMLab ingestion
- `ValueError` — raised on version mismatch; CONSUMER: COMLab compatibility gate
- `T-DNA-7` / `T-DNA-10` — tasks that drove SCHEMA_VERSION bumps
