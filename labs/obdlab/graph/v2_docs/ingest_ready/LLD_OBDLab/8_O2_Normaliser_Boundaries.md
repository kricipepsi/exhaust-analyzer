> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 8 O2 Normaliser Boundaries · Parent document: LLD_OBDLab.md

## 8. O2 Normaliser Boundaries (`core/o2_normalizer.py`)

Source: `OBDLab_KG_Wiki.md §11.1`.

```python
_ZONE_MIN_VOLTAGE     = 0.10   # min valid narrowband V
_ZONE_LEAN_BOUNDARY   = 0.40   # LEAN upper bound (V)
_ZONE_STOICH_BOUNDARY = 0.50   # STOICH upper bound (V)
_ZONE_MAX_VOLTAGE     = 0.90   # max valid narrowband V

_LAMBDA_LEAN   = 1.05   # 0.10–0.40 V
_LAMBDA_STOICH = 1.00   # 0.41–0.50 V
_LAMBDA_RICH   = 0.95   # 0.51–0.90 V

_LAMBDA_MIN = 0.7   # wideband passthrough floor (§5)
_LAMBDA_MAX = 1.3   # wideband passthrough ceiling (§5)

_LAMBDA_STOICH_TARGET      = 1.0    # wideband offset reference (o2-logic/03)
_WIDEBAND_OFFSET_THRESHOLD = 0.05   # |ratio−1.0| trigger (o2-logic/03 / 08)
```

### Entity: Boundary ownership & fault mapping

- **v == 0.40** → LEAN (λ 1.05)
- **v == 0.41** → STOICH (λ 1.00)
- **v == 0.50** → STOICH (λ 1.00)
- **v == 0.51** → RICH (λ 0.95)
- **v < 0.10** → `O2_CHANNEL_FAULT`, λ clamped 1.05, **STUCK_LEAN**
- **v > 0.90** → `O2_CHANNEL_FAULT`, λ clamped 0.95, **STUCK_RICH**
- **wideband `ratio < 0.7`** → `O2_CHANNEL_FAULT`, clamp 0.7, NO_FAULT
- **wideband `ratio > 1.3`** → `O2_CHANNEL_FAULT`, clamp 1.3, NO_FAULT
- **wideband, warm+CL+not WOT+not DFCO, `|ratio−1.0| > 0.05`** → `WIDEBAND_PASSTHROUGH`, **WIDEBAND_OFFSET_CANDIDATE**

`WIDEBAND_NB_SIM` uses the identical voltage map as narrowband but reports
`WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA` so COMLab can apply the WB-sim trim weight.

## Graph relations (explicit)

**O2Normalizer** ENUMERATES **_ZONE_MIN_VOLTAGE=0.10, _ZONE_LEAN_BOUNDARY=0.40, _ZONE_STOICH_BOUNDARY=0.50, _ZONE_MAX_VOLTAGE=0.90** (# wiki: §11.1)
**O2Normalizer** ENUMERATES **_LAMBDA_LEAN=1.05, _LAMBDA_STOICH=1.00, _LAMBDA_RICH=0.95** (narrowband 3-zone mapping, # wiki: §11.1)
**O2Normalizer** ENUMERATES **_LAMBDA_MIN=0.7, _LAMBDA_MAX=1.3** (wideband passthrough bounds)
**O2Normalizer** ENUMERATES **_WIDEBAND_OFFSET_THRESHOLD=0.05** (|ratio−1.0| trigger, # wiki: o2-logic/03/08)
**O2Normalizer** ENUMERATES **O2_CHANNEL_FAULT** mapping (STUCK_LEAN, STUCK_RICH, wideband OOR clamp)
**COMLab T-COMV2-O2OFFSET-1** CONSUMES **WIDEBAND_OFFSET_CANDIDATE** (S4 forward-reg, proposal EP-OBD-17)
**test_o2_normalizer.py** VERIFIES **O2Normalizer boundaries** (unit tests)
