> **Context:** DNALab DLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 1. · Parent document: DLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 1. Module Map

```
dnalab/
├── __init__.py     ← public surface: build_vehicle_dna, VehicleDNA
├── assembly.py     ← build_vehicle_dna() orchestration
└── models.py       ← VehicleDNA dataclass + SCHEMA_VERSION + round-trip
```

The umbrella has no config, no data, no overlays — it is pure composition. Field
knowledge lives in `vinlab.models.VinDNA` and `symptomlab.models.SymptomDNA`; DNALab
delegates to both.

`__init__.py` exports `build_vehicle_dna` and `VehicleDNA`
(`__all__ = ["build_vehicle_dna", "VehicleDNA"]`).

---

## Graph relations (explicit)

**dnalab package** DESCRIBES **three modules** (__init__.py, assembly.py, models.py)
**dnalab/__init__.py** EXPORTS **build_vehicle_dna + VehicleDNA** (__all__ explicit)
**dnalab/assembly.py** CONSUMES **vinlab + symptomlab** (in-family imports only)
**dnalab/models.py** DESCRIBES **VehicleDNA dataclass + SCHEMA_VERSION + round-trip**
