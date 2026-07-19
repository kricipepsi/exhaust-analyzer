> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 1 Physical Constants · Parent document: LLD_OBDLab.md

## 1. Physical Constants (`core/ve_engine.py`)

```python
MM_AIR:   float = 28.97   # wiki: §10.1 — molar mass dry air, g/mol
R_GAS:    float = 8.314   # wiki: §10.1 — universal gas constant, J/(mol·K)
K_OFFSET: float = 273.15  # wiki: §10.1 — °C → K offset
```

`core/maf_linearity.py` carries its own constants (different formula family):

```python
R:           float = 0.287   # wiki: research/chunks/pids-protocol/05 — specific gas constant air, kJ/(kg·K)
CONSTANT_120: float = 120.0  # wiki: research/chunks/pids-protocol/05 — 4-stroke/60s factor
K_OFFSET:    float = 273.15  # wiki: research/chunks/pids-protocol/05
PERCENT_MULT: float = 100.0  # wiki: research/chunks/pids-protocol/05
```

## Graph relations (explicit)

**ve_engine.py** ENUMERATES **MM_AIR=28.97, R_GAS=8.314, K_OFFSET=273.15** (physical constants, # wiki: §10.1)
**maf_linearity.py** ENUMERATES **R=0.287, CONSTANT_120=120.0, K_OFFSET=273.15, PERCENT_MULT=100.0** (different formula family, # wiki: research/chunks/pids-protocol/05)
**VEEngine._calc_ve_standard** CONSUMES **MM_AIR, R_GAS, K_OFFSET** (VE formula inputs)
**calculate_w_theo** CONSUMES **R=0.287, CONSTANT_120, K_OFFSET** (MAF linearity formula inputs)
