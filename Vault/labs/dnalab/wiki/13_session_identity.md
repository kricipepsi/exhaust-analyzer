---
node_type: "wiki"
lab: "dnalab"
module: "dnalab"
subsystem: "session-identity"
implements:
  - "labs/dnalab/dnalab/models.py"
consumers:
  - "comlab: session correlation"
drift_guards:
  - "labs/dnalab/tests/unit/test_assembly.py"
  - "labs/dnalab/tests/unit/test_models.py"
tags: [dnalab, finished, wiki]
source: "labs/dnalab/wiki/13_session_identity.md"
---

# Session identity — `session_id` & `timestamp` formats

**Disposition: reference-only.** Mirrors `VehicleDNA.new` in `dnalab/models.py`. These are
**format constants**, not measured values — they need no wiki citation.

## The two identity fields

| Element | Format | Example |
|---|---|---|
| `session_id` | `DNA_TX_` + 10 upper-hex chars (`uuid4().hex[:10].upper()`) | `DNA_TX_8849201AB3` |
| `timestamp` | ISO-8601 UTC, second precision (`%Y-%m-%dT%H:%M:%SZ`) | `2026-06-11T09:10:00Z` |

## Generation rule

```
VehicleDNA.new(vin_dna, symptom_dna, *, session_id=None, timestamp=None,
               schema_version=SCHEMA_VERSION):
    sid = session_id or  "DNA_TX_" + uuid4().hex[:10].upper()
    ts  = (timestamp  or now(UTC)).strftime("%Y-%m-%dT%H:%M:%SZ")
    return VehicleDNA(sid, ts, schema_version, vin_dna, symptom_dna)
```

A caller-supplied `session_id` / `timestamp` is used **verbatim**; otherwise both are
auto-generated. The `DNA_TX_` prefix lets the orchestrator recognise a DNA-family session
id at a glance and correlate the payload with the rest of the pipeline.

## Consumer (signal/noise)

`session_id` and `timestamp` exist so COMLab (and the app composition layer) can correlate
this payload with the rest of a diagnostic run. That correlation is the named consumer; no
other meaning is attached to either field.



## Graph relations (explicit)

**session_id** CONSUMED_BY **COMLab session correlation** (correlate payload with pipeline run)
**timestamp** CONSUMED_BY **COMLab session correlation** (ISO-8601 UTC, second precision)
**VehicleDNA.new()** PRODUCES **session_id** (DNA_TX_ + 10 upper-hex chars, auto-generated)
**VehicleDNA.new()** PRODUCES **timestamp** (current UTC, %Y-%m-%dT%H:%M:%SZ format)
**session_id FORMAT** IS **DNA_TX_<10-UPPER-HEX>** (uuid4().hex[:10].upper())
**timestamp FORMAT** IS **ISO-8601 UTC second-precision** (%Y-%m-%dT%H:%M:%SZ)
**caller-supplied session_id/timestamp** ACCEPTED verbatim (no re-generation)
**DNA_TX_ prefix** ENABLES **COMLab DNA-family session recognition**
**VehicleDNA.new** VERIFIED_BY **dnalab/tests/unit/test_models.py::test_new_constructs_successfully**
**VehicleDNA.new** VERIFIED_BY **dnalab/tests/unit/test_models.py::test_explicit_session_id_and_timestamp**
**session_id** VERIFIED_BY **dnalab/tests/unit/test_assembly.py::test_session_id_format**

## Core Entities

- `session_id` — DNA_TX_<10-HEX> session identifier; CONSUMER: COMLab session correlation
- `timestamp` — ISO-8601 UTC timestamp; CONSUMER: COMLab session correlation
- `VehicleDNA.new()` — factory with auto-generated identity fields; CONSUMER: build_vehicle_dna()
