> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 8 — Release

### v2 Scope

`build_vehicle_dna` composition, session metadata, JSON round-trip, and the
version guard, at `SCHEMA_VERSION = "1.2"`.

### Landed (DNA-family pack — see `tasks/PROGRESS.md`)

- **T-DNA-7 — schema-version bump + round-trip (done).** Bumped `SCHEMA_VERSION`
  `1.0 → 1.1`; `to_json_payload`/`from_json_payload` round-trip every new field landed
  upstream (`load_state` via `symptom_dna`; `rated_rpm` / formalized CoC via `vin_dna`),
  delegating to each producer's serializer. `build_vehicle_dna` now requires `load_state`
  as a triage key and passes it through to `resolve()`. (`fuel_type` stayed a proposal,
  so it is **not** in the round-trip — only the fields the upstream tasks actually
  landed.) Consumer: COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion.
- **T-DNA-10 — `engine_state` wire-value rename (done).** `will_not_start` replaced the
  legacy `won_not_start` across both ends; `SCHEMA_VERSION` bumped `1.1 → 1.2`.

### Dependency note (transitive — resolved)

`build_vehicle_dna` calls `symptomlab.resolve()`, which constructs a `SymptomValidator`.
The live symptom catalog now holds **18** pairs (T-DNA-8), so the `len == 18` invariant
passes and the constructor succeeds — `build_vehicle_dna` is no longer transitively
blocked. DNALab's own code was unchanged by that fix; it landed in SymptomLab.

### Decided

- Legacy non-current-version payload handling: **reject-with-message** (no upgrade-on-read)
  — decided and tested under T-DNA-7; `from_json_payload` raises `ValueError` on any
  `schema_version` ≠ `SCHEMA_VERSION`.

### Success Criteria

1. KR1–KR6 hold.
2. Composition + round-trip pass for a full `VehicleDNA`.
3. Missing triage keys fail fast; version mismatch is rejected.
4. Only in-family imports.

## Graph relations (explicit)

**v2 Scope** DESCRIBES **build_vehicle_dna composition + session metadata + JSON round-trip + version guard** (SCHEMA_VERSION 1.2)
**T-DNA-7** DESCRIBES **schema-version bump 1.0→1.1 + round-trip** (done)
**T-DNA-10** DESCRIBES **engine_state wire-value rename + 1.1→1.2 bump** (done)
**T-DNA-8** DESCRIBES **SymptomValidator(len==18) constructability fix** (transitive — resolved in SymptomLab)
**from_json_payload()** VERIFIES **legacy-payload rejection (reject-with-message)** (decided under T-DNA-7)
