> **Context:** DNALab BDD_DNALab v2 (2026-06-12) · Module: DNALab · Section: Traceability · Parent document: BDD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Traceability summary

| Behaviour area | Primary test module |
|----------------|---------------------|
| Composition happy path | `test_assembly.py` |
| Contract keys | `test_assembly.py` |
| Round-trip | `test_vehicledna_roundtrip.py`, `test_assembly.py` |
| Version guard | `test_models.py`, `test_assembly.py` |
| Fail-fast / propagation | `test_assembly.py` |
| Fixtures | `conftest.py` |

## Graph relations (explicit)

**test_assembly.py** VERIFIES **composition happy path + contract keys + version guard + fail-fast**
**test_vehicledna_roundtrip.py** VERIFIES **JSON round-trip**
**test_models.py** VERIFIES **VehicleDNA model + version guard**
**conftest.py** VERIFIES **fixture consistency**
