> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 8. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 8. Known Gaps / Accepted Behaviour

| ID | Description | Status |
|----|-------------|--------|
| T-DNA-7 | `SCHEMA_VERSION` bumped `1.0 → 1.1`; new upstream fields (`load_state`, `rated_rpm`, formalized CoC) round-trip via each producer's `to_json`/`from_json`; `load_state` is now a required `build_vehicle_dna` triage key passed through to `resolve()` | Done |
| `free_text_notes` | optional on `SymptomDNA`; the assembly does not forward it (it is not a `build_vehicle_dna` triage key) | Accepted (no named consumer) |
| Legacy-payload path | `from_json_payload` rejects any non-matching version (no upgrade-on-read); decided under T-DNA-7 | Decided (reject-with-message) |
| Transitive block | `build_vehicle_dna` → `symptomlab.resolve` → `SymptomValidator(len==18)` — the live catalog is now 18 pairs (T-DNA-8), so the validator constructs cleanly | Resolved (T-DNA-8) |

## Graph relations (explicit)

**T-DNA-7** DESCRIBES **SCHEMA_VERSION bump 1.0→1.1 + round-trip** (done)
**free_text_notes** DESCRIBES **optional SymptomDNA field not forwarded by assembly** (accepted gap — no named consumer)
**Legacy-payload path** DESCRIBES **reject-with-message on version mismatch** (decided under T-DNA-7)
**Transitive block** DESCRIBES **SymptomValidator(len==18) constructability** (resolved by T-DNA-8)
