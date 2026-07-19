> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 6 Target VE Constants for Emulation · Parent document: LLD_OBDLab.md

## 6. Target VE Constants for Emulation (`core/ve_engine.py::_EXPECTED_VE`)

Source: `OBDLab_KG_Wiki.md BP §1.B / §1.C`. Keyed by `(bucket, strategy)`:

### Entity: Target VE per (bucket, strategy) — 6 entries

- **(STABILIZED_IDLE, MAP_ONLY_SPEED_DENSITY)** — 0.65
- **(STABILIZED_IDLE, MAF_ONLY)** — 0.70
- **(REGULATORY_HIGH_IDLE, MAP_ONLY_SPEED_DENSITY)** — 0.80
- **(REGULATORY_HIGH_IDLE, MAF_ONLY)** — 0.82
- **(STRESS_IDLE, MAP_ONLY_SPEED_DENSITY)** — 0.80
- **(STRESS_IDLE, MAF_ONLY)** — 0.82

(v1.0 listed only 4 entries; the current table has all 6 — both strategies cover
`REGULATORY_HIGH_IDLE`.)

## Graph relations (explicit)

**_EXPECTED_VE** ENUMERATES **6 target VE entries** keyed by (bucket, strategy) — # wiki: OBDLab_KG_Wiki.md BP §1.B / §1.C
**_EXPECTED_VE v2** SUPERSEDES **v1.0 table** (4→6 entries, REGULATORY_HIGH_IDLE added for both strategies)
**VEEngine._ve_map_only** CONSUMES **_EXPECTED_VE** (emulated MAF calculation)
**VEEngine._ve_maf_only** CONSUMES **_EXPECTED_VE** (back-calculated MAP)
