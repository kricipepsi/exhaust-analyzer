> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Traceability summary | Parent document: BDD_VINLab.md / shipped unit tests

## Traceability summary

| Behaviour area | Primary location |
|----------------|------------------|
| End-to-end decode | `decode()` / `decode_vin_payload`, `tests/fixtures/` |
| Structural validation | `pre_clean_vin`, length/charset guards |
| Checksum + bypass | `validate_vin_checksum` |
| WMI / year resolution | `_resolve_wmi`, `_resolve_year` |
| Scope guards (H1/H2) | `_is_non_petrol`, year bound |
| Engine resolution | `_resolve_engine` |
| Overlays | `overlay/air_metering`, `horizon`, `stress_rpm`, `switches`, `cylinder_heuristic` |
| Confidence grading | decoder flag collection |
| Isolation / SQL | DNA-family boundary, `db/tecdoc_query.py` |

## Graph relations (explicit)

**Traceability summary** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
**labs/vinlab/tests/unit/test_contract_conformance.py** VERIFIES **Traceability summary**
