> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 7 — Solution

### Key Features (all P0)

- P0: **Composition** — `build_vehicle_dna(vin, triage)` calls `vinlab.decode(vin)` and
  `symptomlab.resolve(**triage)` and joins them via `VehicleDNA.new(...)`.
- P0: **Triage pre-validation** — required keys (`tier_1`, `tier_2`, `occurs_during`,
  `engine_state`) checked first; missing → `SymptomValidationError`.
- P0: **Session metadata** — `session_id = DNA_TX_<10 hex, upper>`; `timestamp` ISO-8601
  UTC; `schema_version`.
- P0: **JSON round-trip** — `to_json_payload()` / `from_json_payload()` delegate to each
  model's `to_json` / `from_json`.
- P0: **Version guard** — `from_json_payload` raises `ValueError` on a `schema_version`
  mismatch and `KeyError` on a missing required top-level key.

### Technology

- Python 3.14. Package `dnalab`, standalone `pyproject.toml`. Imports `vinlab` +
  `symptomlab` (in-family). No COMLab import.
- Entry point: `dnalab.build_vehicle_dna(vin, triage)`. Exceptions propagate from the
  producers: `vinlab.VINDecodeError`, `symptomlab.SymptomValidationError`.

### `VehicleDNA` fields (5, contract §4.3)

#### Field: `session_id`
- **Type**: `str`
- **Format**: `DNA_TX_<10 hex upper>` (auto if not supplied)
- **Owned by**: DNALab
- **Consumed by**: COMLab session correlation (live)

#### Field: `timestamp`
- **Type**: `str`
- **Format**: ISO-8601 UTC `YYYY-MM-DDTHH:MM:SSZ`
- **Owned by**: DNALab
- **Consumed by**: COMLab temporal correlation (live)

#### Field: `schema_version`
- **Type**: `str`
- **Value**: `SCHEMA_VERSION` (currently `"1.2"`)
- **Owned by**: DNALab
- **Consumed by**: COMLab schema-version gate (live); VehicleDNA.from_json_payload mismatch guard (live)

#### Field: `vin_dna`
- **Type**: `VinDNA`
- **Source**: Part A (from VINLab)
- **Owned by**: VINLab
- **Consumed by**: COMLab ingestion (live, via VehicleDNA envelope)

#### Field: `symptom_dna`
- **Type**: `SymptomDNA`
- **Source**: Part B (from SymptomLab)
- **Owned by**: SymptomLab
- **Consumed by**: COMLab ingestion (live, via VehicleDNA envelope); COMLab fault_atlas_router symptom prior (PROPOSAL — COMLab-A)

### Assumptions

#### Assumption: Producers own their own validation
- **Validation**: DNALab pre-checks only triage-key presence; field validity is VINLab/SymptomLab's job
- **Verifies**: build_vehicle_dna triage pre-check (test_assembly.py)

#### Assumption: VehicleDNA shape is contract-owned
- **Validation**: five top-level keys; `from_json_payload` raises on mismatch
- **Verifies**: SEMANTIC_CONTRACT §4.3

#### Assumption: Version moves in lockstep with producer field changes
- **Validation**: `SCHEMA_VERSION` bumps were the T-DNA-7 (→1.1) and T-DNA-10 (→1.2) coordinating tasks
- **Verifies**: ADR-0007 coordinated schema-bump rule

---

## Graph relations (explicit)

**build_vehicle_dna()** CONSUMES **vinlab.decode(vin) + symptomlab.resolve(**triage)** (P0 composition)
**build_vehicle_dna()** GATED_BY **triage pre-validation** (P0 — missing keys → SymptomValidationError)
**VehicleDNA.new()** CONSUMES **session_id + timestamp + schema_version** (P0 session metadata)
**VehicleDNA.to_json_payload() / from_json_payload()** DELEGATES_TO **each model's to_json / from_json** (P0 round-trip)
**VehicleDNA.from_json_payload()** GATED_BY **schema_version guard** (P0 — ValueError on mismatch)
**VehicleDNA** DESCRIBES **five fields** (session_id, timestamp, schema_version, vin_dna, symptom_dna)
**SCHEMA_VERSION** DERIVED_FROM **T-DNA-7 (→1.1) + T-DNA-10 (→1.2)** (coordinating tasks)
