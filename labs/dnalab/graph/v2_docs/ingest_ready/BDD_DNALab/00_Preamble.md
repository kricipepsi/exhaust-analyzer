> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Preamble · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

# BDD — DNALab (v2)

**Status:** Current (scenarios grounded in the live test suite)
**Reference:** HLD_DNALab v2.1 / DLD_DNALab v2.1 / LLD_DNALab v2.1
**Date:** 2026-06-12

Behaviour specification for DNALab's single public behaviour: **compose a VIN + triage
into a versioned, round-trippable `VehicleDNA`**. Scenarios are declarative; the truth is
`tests/` (`test_assembly.py`, `test_models.py`, `test_vehicledna_roundtrip.py`).

Ubiquitous language: *compose* = run `build_vehicle_dna()`; *envelope* = the five-key
`VehicleDNA`; *round-trip* = `from_json_payload(to_json_payload(x))`.

---

## Graph relations (explicit)

**BDD_DNALab v2** MIRRORS_CONTRACT_IN **HLD_DNALab v2.1 + DLD_DNALab v2.1 + LLD_DNALab v2.1**
**BDD_DNALab v2** DESCRIBES **behaviour specification for build_vehicle_dna()** (single public behaviour)
**BDD_DNALab v2** VERIFIES **all scenarios grounded in live test suite** (tests/)
