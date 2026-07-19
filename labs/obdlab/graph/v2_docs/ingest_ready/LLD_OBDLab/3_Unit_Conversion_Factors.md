> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 3 Unit Conversion Factors · Parent document: LLD_OBDLab.md

## 3. Unit Conversion Factors (`core/pid_ingestion_validator.py`)

Source: `OBDLab_KG_Wiki.md §3.2`. `{alternate_suffix: (canonical_suffix, fn)}`.

```python
"_f"     → "_c":   (v - 32.0) * 5.0 / 9.0   # °F → °C
"_psi"   → "_kpa": v * 6.895                # psi → kPa
"_inhg"  → "_kpa": v * 3.386                # inHg → kPa
"_lbmin" → "_gps": v * 7.559                # lb/min → g/s
```

Canonical key wins: if both `coolant_temp_c` and `coolant_temp_f` are present,
the `_c` value is kept and `_f` dropped.

## Graph relations (explicit)

**PIDIngestionValidator._apply_unit_conversions** ENUMERATES **4 unit conversion factors** (_f→_c, _psi→_kpa, _inhg→_kpa, _lbmin→_gps)
**PIDIngestionValidator._apply_unit_conversions** CONSUMES **canonical-key precedence** (canonical suffix wins, alternate dropped)
**test_pid_ingestion_validator.py** VERIFIES **unit conversion accuracy** (all 4 factors)
