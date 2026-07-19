> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

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

## Graph relations (explicit)

**KR1** VERIFIES **build_vehicle_dna returns VehicleDNA composing valid VinDNA + SymptomDNA**
**KR2** VERIFIES **missing triage keys raise SymptomValidationError before VIN decode**
**KR3** VERIFIES **VehicleDNA round-trip: from_json_payload(to_json_payload(x))**
**KR4** VERIFIES **session_id (DNA_TX_…), ISO-8601 UTC timestamp, schema_version**
**KR5** VERIFIES **from_json_payload raises on schema_version mismatch**
**KR6** VERIFIES **only in-family imports (vinlab, symptomlab); no COMLab import**
