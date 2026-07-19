> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 7. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

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

## Graph relations (explicit)

**Top-level contract keys == 5** VERIFIES **SEMANTIC_CONTRACT §4.3** (live)
**Import direction one-way** VERIFIES **dnalab → vinlab + symptomlab only** (live, ADR-0002)
**Round-trip fidelity** VERIFIES **from_json_payload(to_json_payload(x)) == x** (test_assembly.py, test_vehicledna_roundtrip.py)
**Fail-fast** VERIFIES **triage check before VIN decode** (test_assembly.py)
**Version safety** VERIFIES **cross-version load raises, never silently coerces** (test_models.py)
**Signal/noise** VERIFIES **every field has a named consumer** (COMLab ingestion, live)
