# ADR 0002 — DNALab Is the Only Lab That Imports Other Labs

## Status

Accepted

## Date

2026-05-17

## Context

The 4DLab platform has multiple labs: VINLab, SymptomLab, DNALab, COMLab, OBDLab, DTCLab, and GasLab. DNALab's job is to compose `VinDNA` (from VINLab) and `SymptomDNA` (from SymptomLab) into `VehicleDNA`. Every other lab — COMLab routing logic, OBDLab mode selection, DTCLab DTC interpretation, GasLab exhaust analysis — consumes `VehicleDNA` as a plain JSON payload. If other labs were allowed to import `vinlab` or `symptomlab` Python packages directly, the dependency graph would become tangled, each lab's test suite would need a live VIN decoder, and the offline constraint (no network at runtime) would be harder to enforce at the boundary.

## Decision

**DNALab** is the only lab in 4DLab that imports the `vinlab` and `symptomlab` Python packages. All other labs (COMLab, OBDLab, DTCLab, GasLab) consume `VehicleDNA` through its JSON serialization — never through a Python import of `dnalab`, `vinlab`, or `symptomlab`.

## Consequences

- **Positive:** The import graph is a single directed edge: VINLab → DNALab ← SymptomLab, and DNALab → JSON → all downstream labs. Each downstream lab can be built and tested against static JSON fixtures without pulling in the VIN decoder's data files.
- **Positive:** The offline constraint (zero MySQL, zero network at VINLab runtime) is enforced at a single seam — DNALab's `build_vehicle_dna()` — rather than needing to be re-audited in every downstream module.
- **Negative:** Downstream labs must deserialize `VehicleDNA` from JSON rather than receiving a typed Python object. This shifts the type-checking burden to the JSON contract (`SEMANTIC_CONTRACT.md` §4.3), which must remain stable.

## Sources

- `DNALab/README.md` — "DNALab is the only lab in 4DLab that does import other labs" (line 5)
- `dnalab/assembly.py` — imports `vinlab` and `symptomlab` (lines 7–8)
- `dnalab/models.py` — imports `VinDNA`, `AirMeteringArchitecture`, `Emissions` from `vinlab.models` and `SymptomDNA`, `EnvironmentalConditions` from `symptomlab.models` (lines 15–20)
- `SymptomLab/README.md` — "routing logic … lives in COMLab, not here" (line 5), establishing that downstream labs do not import SymptomLab
