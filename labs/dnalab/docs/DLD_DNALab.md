---
node_type: dld
lab: dnalab
module: dnalab
subsystem: detailed-design
implements:
  - "labs/dnalab/dnalab/__init__.py"
  - "labs/dnalab/dnalab/assembly.py"
  - "labs/dnalab/dnalab/models.py"
consumers:
  - "comlab: labs/comlab/comlab/core/horizon_context_injector.py from_vehicle_dna (VehicleDNA.vin_dna read)"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py check_schema_version (request.metadata.schema_version vs MIN_SUPPORTED_SCHEMA_VERSION; ERR-ABORT-005)"
drift_guards:
  - "labs/dnalab/tests/unit/test_assembly.py"
  - "labs/dnalab/tests/unit/test_models.py"
  - "labs/dnalab/tests/unit/test_vehicledna_roundtrip.py"
tags: [dnalab, dld, detailed-design]
source: "labs/dnalab/docs/DLD_DNALab.md"
---

# DLD — DNALab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_DNALab v2.0
**HLD Reference:** HLD_DNALab v2.1
**Version:** 2.1
**Date:** 2026-06-12

> Grounded in the live `dnalab/` package as of 2026-06-12 (`SCHEMA_VERSION = "1.2"`,
> `load_state` flows through `build_vehicle_dna`).

---

## 1. Module Map

```
dnalab/
├── __init__.py     ← public surface: build_vehicle_dna, VehicleDNA
├── assembly.py     ← build_vehicle_dna() orchestration
└── models.py       ← VehicleDNA dataclass + SCHEMA_VERSION + round-trip
```

The umbrella has no config, no data, no overlays — it is pure composition. Field
knowledge lives in `vinlab.models.VinDNA` and `symptomlab.models.SymptomDNA`; DNALab
delegates to both.

`__init__.py` exports `build_vehicle_dna` and `VehicleDNA`
(`__all__ = ["build_vehicle_dna", "VehicleDNA"]`).

---

## 2. `models.py` — `VehicleDNA` (frozen dataclass)

Schema governed by `SEMANTIC_CONTRACT.md §4.3`. Five top-level keys (snake_case).

| # | Field | Type | Notes |
|---|-------|------|-------|
| 1 | `session_id` | `str` | `DNA_TX_<10 hex upper>` |
| 2 | `timestamp` | `str` | ISO-8601 UTC `%Y-%m-%dT%H:%M:%SZ` |
| 3 | `schema_version` | `str` | module constant `SCHEMA_VERSION` |
| 4 | `vin_dna` | `VinDNA` | Part A |
| 5 | `symptom_dna` | `SymptomDNA` | Part B |

`SCHEMA_VERSION = "1.2"` (module-level). T-DNA-7 bumped it `1.0 → 1.1` (new round-tripped fields); T-DNA-10 bumped it `1.1 → 1.2` (the `engine_state` wire-value rename).

### Classmethods / methods

| Member | Behaviour |
|--------|-----------|
| `new(vin_dna, symptom_dna, *, session_id=None, timestamp=None, schema_version=SCHEMA_VERSION)` | generates `session_id` (`DNA_TX_` + `uuid4().hex[:10].upper()`) and `timestamp` (`now(UTC)`) when not supplied |
| `to_json_payload() → dict` | five keys; delegates `vin_dna.to_json()` / `symptom_dna.to_json()` |
| `to_json(**dumps_kwargs) → str` | `json.dumps(to_json_payload(), **kwargs)` |
| `from_json_payload(payload) → VehicleDNA` | version guard + delegated `VinDNA.from_json` / `SymptomDNA.from_json` |

---

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

| Failure | Exception |
|---------|-----------|
| `schema_version` ≠ `SCHEMA_VERSION` | `ValueError` |
| missing required top-level key | `KeyError` |
| invalid `vin_dna` / `symptom_dna` shape | propagated from each model's `from_json` (`KeyError` / `SymptomValidationError`) |

---

## 4. `assembly.py` — `build_vehicle_dna`

```python
build_vehicle_dna(vin: str, triage: dict[str, Any]) -> VehicleDNA
```

| Step | Detail |
|------|--------|
| required-key check | `("tier_1", "tier_2", "occurs_during", "engine_state")`; any missing → `SymptomValidationError` |
| Part A | `vinlab.decode(vin)` (imported as `_decode_vin`) — may raise `VINDecodeError` |
| Part B | `symptomlab.resolve(tier_1, tier_2, occurs_during, engine_state)` (imported as `_resolve_symptom`) — may raise `SymptomValidationError` |
| compose | `VehicleDNA.new(vin_dna=physical, symptom_dna=symptomatic)` |

Imports: `from symptomlab.validator import SymptomValidationError`,
`from symptomlab import resolve as _resolve_symptom`,
`from vinlab import decode as _decode_vin`, `from dnalab.models import VehicleDNA`. These
are the **only** cross-module imports — both in-family.

---

## 5. Exceptions (propagated, not defined here)

DNALab defines no exception types of its own. It surfaces:

| Exception | Origin | When |
|-----------|--------|------|
| `SymptomValidationError` | symptomlab | missing triage key; invalid pair/environmental value |
| `VINDecodeError` (+ `ChassisNumberError`) | vinlab | malformed/out-of-scope VIN |
| `ValueError` | dnalab `from_json_payload` | `schema_version` mismatch |
| `KeyError` | dnalab `from_json_payload` | missing required top-level key |

---

## 6. Test Coverage (current)

| Area | File |
|------|------|
| Composition + contract keys | `tests/test_assembly.py` (`TestBuildVehicleDNA`, `TestSchemaVersion`) |
| `VehicleDNA` model | `tests/test_models.py` |
| JSON round-trip | `tests/test_vehicledna_roundtrip.py` |
| Fixtures | `tests/conftest.py` (`sample_vin`, `sample_triage`, `sample_dna`, `invalid_vin`) |

`test_assembly.py` asserts the five top-level keys, `schema_version == "1.2"`, the VinDNA
required-key superset, the SymptomDNA exact-4-key set, round-trip equality, session-id
prefix `DNA_TX_`, ISO-8601 UTC timestamp, and exception propagation for invalid VIN /
missing-triage-key / invalid-triage.

> The `sample_triage` fixture uses `tier_2 = "black_smoke"` — a pair present in the live
> 18-pair catalog — and supplies `load_state` (a required triage key since T-DNA-7).
> `SymptomValidator` construction now passes the `len == 18` invariant (catalog reconciled
> by T-DNA-8), so these tests build the validator cleanly.

---

## 7. Related docs (granular ADRs)

The lab also carries per-decision records under `docs/adr/` (0001 naming-contract,
0002 dnalab-only-importer, 0003 string-typed-enum-fields, 0004 enum-typed-fields) and a
rework/answerability audit under `docs/audits/`. `ADR_DNALab.md` (this set) consolidates
the lab-level decisions; the granular records remain authoritative for their specifics.
