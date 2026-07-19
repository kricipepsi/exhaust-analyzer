---
node_type: "prd"
lab: "dnalab"
module: "dnalab"
subsystem: "requirements"
implements: []
consumers:
  - "hld: labs/dnalab/docs/HLD_DNALab.md"
  - "comlab: OrchestratorInboundRequest.vehicle_dna ingestion (T-DNA-7)"
drift_guards: []
tags: [dnalab, finished, prd]
source: "labs/dnalab/docs/PRD_DNALab.md"
---
# PRD — DNALab
**Status:** Approved
**Version:** 2.1
**Date:** 2026-06-12
**Scope:** Petrol-only, v2 — DNA assembly module (VehicleDNA composer)

---

## Section 1 — Summary

DNALab is the **assembly** of the DNA family. It composes Part A (`VinDNA`, from VINLab)
and Part B (`SymptomDNA`, from SymptomLab) plus session metadata into one `VehicleDNA` —
the unified, contract-shaped payload COMLab ingests as its independent prior. The single
public entry point is `dnalab.build_vehicle_dna(vin, triage) → VehicleDNA`.

DNALab is the only lab in the DNA family that imports the others: the one allowed
in-family direction is `dnalab → vinlab + symptomlab`. It imports no COMLab. `VehicleDNA`'s
schema is governed by `SEMANTIC_CONTRACT.md §4.3`.

DNALab is a **composer, not a decoder and not a router.** It does not decode VINs (VINLab
does) or validate symptoms (SymptomLab does) or route faults (COMLab does). It orchestrates
the two producers, stamps session identity, and guarantees the combined payload
round-trips through JSON cleanly.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| DNALab Owner | Module Owner | `build_vehicle_dna` orchestration, `VehicleDNA` schema + versioning, JSON round-trip |
| VINLab Owner | In-family Producer | Supplies `VinDNA` (Part A) via `vinlab.decode()` |
| SymptomLab Owner | In-family Producer | Supplies `SymptomDNA` (Part B) via `symptomlab.resolve()` |
| COMLab Team | Integration Consumer | Ingests `VehicleDNA` as `OrchestratorInboundRequest.vehicle_dna`; mirrors the types |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; schema versioning; one-way in-family import boundary |

---

## Section 3 — Background

**Context.** The 4D engine wants the symptom/identity prior as a single packet: the
physical hardware (from the VIN) and the operator's complaint (from triage), stamped with
a session id and timestamp so the orchestrator can correlate it with the rest of the
pipeline. Assembling these in the UI or in COMLab would scatter the composition logic and
the schema-version contract.

**Why now.** With VINLab and SymptomLab split into independent sibling modules
(T-RM-2-DNA), there needs to be exactly one place that knows how to call both and join
their outputs under the §4.3 contract. DNALab is that place — a thin, deterministic
orchestrator with a versioned envelope.

**What recently became possible.** Both producers expose clean, typed APIs
(`vinlab.decode`, `symptomlab.resolve`) and JSON round-trip (`to_json`/`from_json`).
DNALab composes them, delegating serialization to each model so the umbrella never
duplicates field knowledge. The `schema_version` field makes the combined payload
self-describing for COMLab.

---

## Section 4 — Objective

**Business benefit.** One call produces the complete, versioned symptom/identity prior —
the cheapest independent channel into COMLab — with a stable JSON contract.

**Customer benefit.** The app gathers a VIN and a triage selection and gets back a single
correlatable record; the technician never assembles anything by hand.

**Key Results:**

- **KR1:** `build_vehicle_dna(vin, triage)` returns a `VehicleDNA` composing a valid
  `VinDNA` and `SymptomDNA`.
- **KR2:** Missing triage keys (`tier_1`, `tier_2`, `occurs_during`, `engine_state`)
  raise `SymptomValidationError` **before** the VIN is decoded.
- **KR3:** A `VehicleDNA` round-trips: `from_json_payload(to_json_payload(x))` reconstructs
  an equal payload.
- **KR4:** Every payload carries a `session_id` (`DNA_TX_…`), an ISO-8601 UTC
  `timestamp`, and a `schema_version`.
- **KR5:** `from_json_payload` raises on a `schema_version` mismatch (no silent
  cross-version load).
- **KR6:** Only in-family imports (`vinlab`, `symptomlab`); no COMLab import.

---

## Section 5 — Market Segment

**Internal integration surface.** DNALab's "customer" is the COMLab orchestrator and the
app composition layer. Its value is a single, versioned, round-trippable payload that
upstream UI code and downstream COMLab both agree on.

---

## Section 6 — Value Proposition

- **Jobs addressed:** producer orchestration, session stamping, schema versioning, JSON
  round-trip.
- **Gains created:** one `build_vehicle_dna()` call; fail-fast on incomplete triage
  before the (heavier) VIN decode; a self-describing versioned envelope.
- **Pains relieved:** no composition logic duplicated in the UI or COMLab; serialization
  is delegated to each model, so field changes in VINLab/SymptomLab don't require DNALab
  edits (only a version bump when the shape changes).
- **Competitive advantage:** the umbrella stays thin and deterministic; the contract
  surface (`§4.3`) is exactly five top-level keys, and the version field lets COMLab
  distinguish payload generations cleanly.

---

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

| # | Field | Type | Notes |
|---|-------|------|-------|
| 1 | `session_id` | `str` | `DNA_TX_<10 hex upper>` (auto if not supplied) |
| 2 | `timestamp` | `str` | ISO-8601 UTC `YYYY-MM-DDTHH:MM:SSZ` |
| 3 | `schema_version` | `str` | `SCHEMA_VERSION` (currently `"1.2"`) |
| 4 | `vin_dna` | `VinDNA` | Part A (from VINLab) |
| 5 | `symptom_dna` | `SymptomDNA` | Part B (from SymptomLab) |

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| The two producers own their own validation | DNALab pre-checks only triage-key presence; field validity is VINLab/SymptomLab's job |
| `VehicleDNA` shape is contract-owned (`§4.3`) | five top-level keys; `from_json_payload` raises on mismatch |
| Version moves in lockstep with producer field changes | `SCHEMA_VERSION` bumps were the T-DNA-7 (→1.1) and T-DNA-10 (→1.2) coordinating tasks |

---

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
