> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 6. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

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

## Graph relations (explicit)

**test_assembly.py::TestBuildVehicleDNA** VERIFIES **build_vehicle_dna composition + contract keys**
**test_assembly.py::TestSchemaVersion** VERIFIES **SCHEMA_VERSION == "1.2"**
**test_models.py** VERIFIES **VehicleDNA model + version guard**
**test_vehicledna_roundtrip.py** VERIFIES **JSON round-trip fidelity**
**conftest.py** VERIFIES **fixture consistency** (sample_vin, sample_triage, sample_dna, invalid_vin)
**27 tests across 4 modules** VERIFIES **full dnalab contract surface**
