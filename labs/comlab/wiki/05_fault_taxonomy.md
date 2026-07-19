---
chunk_id: COMWIKI-05
title: Fault Taxonomy — 30 nodes, 12 families
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: The machine-readable taxonomy table mapping each fault_id to its diagnostic
  fingerprint (family, horizon, gas state, trim direction, DTC pattern), plus the
  gas-state routing map and trim grammar.
entities_defined:
- CONCEPT_TAXONOMY_TABLE
- CONCEPT_GAS_STATES
- RULE_GAS_ROUTE
- RULE_TRIM_GRAMMAR
fault_nodes: 30 (ERR-RM-001..007, ERR-LC-001..007, ERR-MF-001..007, ERR-SF-001..006,
  ERR-EF-001..002, OPTIMAL_HEALTH) — per-node detail authoritative in the frozen comlab/config/kg/*.json;
  this chunk is the taxonomy table over them
related_chunks:
- COMWIKI-02
- COMWIKI-04
- COMWIKI-06
- COMWIKI-07
sources:
- COMLab_HLD.md §5
- COMLab_LLD.md §8
- vocabulary.py FaultFamily
- global_fault_registry.json
- comlab/config/kg/*.json (frozen)
node_type: wiki
lab: comlab
module: comlab
subsystem: fault-taxonomy
implements:
- labs/comlab/comlab/core/fault_atlas_router.py
- labs/comlab/comlab/config/global_fault_registry.json
consumers:
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_GAS_ROUTE / taxonomy-table
  routing'
- 'comlab: labs/comlab/comlab/core/fault_atlas_kg.py fault_id enrichment'
drift_guards:
- labs/comlab/tests/unit/test_fault_atlas_router.py
- labs/comlab/tests/e2e/test_kg_registry_consistency.py
tags:
- comlab
- fault-taxonomy
- wiki
source: labs/comlab/wiki/05_fault_taxonomy.md
---

# Fault Taxonomy — 30 nodes, 12 families

This is the machine-readable taxonomy table for the KG nodes. Each row maps a `fault_id` to its
diagnostic fingerprint. The rule engine (Stage B) reads `cross_domain_matrix` values from
`global_fault_registry.json`; the KG (Stage C) reads enrichment from the **frozen**
`comlab/config/kg/*.json`. The per-node prose that lived in the v1 `ERR-*.md` docs is archived
(`ARCHIVE/2026-06-20_comlab_wiki_v1/`); cite a node as `COMWIKI-05 §FAULT_<id>`.

**12 families:** 6 enumerated below with rows (`rich_mixture`, `lean_condition`, `misfire`,
`sensor_fault`, `ecu_fault`, `no_fault`) + 6 defined in the registry / frozen KG and described in
`COMWIKI-06` (`catalyst_failure`, `exhaust_leak`, `ignition_fault`, `mechanical_wear`,
`cam_timing`, `non_starter`).

## Taxonomy table {#CONCEPT_TAXONOMY_TABLE}

| Fault ID | Fault name | Family | Horizons | Gas chemical state | Trim direction | DTC pattern |
|---|---|---|---|---|---|---|
| ERR-RM-001 | worn_valve_stem_seals | rich_mixture | ALL | IGNITION_MISFIRE / POA_SIGNATURE | negative (LT) | P030X, P0420 |
| ERR-RM-002 | worn_piston_rings | rich_mixture | ALL | POA_SIGNATURE | negative | P030X |
| ERR-RM-003 | leaking_fuel_injector | rich_mixture | ALL | RICH_MIXTURE | strongly negative | P0172, P0175 |
| ERR-RM-004 | evap_purge_valve_stuck_open | rich_mixture | ADAPTIVE/MODERN | RICH_MIXTURE | strongly negative | P0441, P0172 |
| ERR-RM-005 | gdi_hpfp_internal_seal_leak | rich_mixture | MODERN | GDI_HPFP_INTERNAL_SEAL_LEAK | ≤ −23 % | P0172, P2196 |
| ERR-RM-006 | coolant_temp_sensor_bias_cold | rich_mixture | ALL | RICH_MIXTURE | negative | P0116–P0118 |
| ERR-RM-007 | fpr_diaphragm_rupture | rich_mixture | LEGACY/ADAPTIVE | RICH_MIXTURE | negative | P0172 |
| ERR-LC-001 | vacuum_leak_post_maf | lean_condition | ALL | LEAN_MIXTURE | positive | P0171, P0174 |
| ERR-LC-002 | maf_sensor_contaminated | lean_condition | ADAPTIVE/MODERN | LEAN_MIXTURE | positive | P0100–P0103 |
| ERR-LC-003 | fuel_pump_low_pressure | lean_condition | ALL | LEAN_MIXTURE (stress) | positive at stress | P0087, P0171 |
| ERR-LC-004 | clogged_fuel_injector | lean_condition | ALL | LEAN_MIXTURE / LEAN_MISFIRE | positive (bank) | P0171 / P030X |
| ERR-LC-005 | egr_stuck_open | lean_condition | LEGACY | INCOMPLETE_OXIDATION | positive (compensate) | P0401, P0402 |
| ERR-LC-006 | exhaust_leak_pre_upstream_o2 | lean_condition | ALL | EXHAUST_AIR_LEAK | positive | P0130–P0131 |
| ERR-LC-007 | secondary_air_injection_stuck_on | lean_condition | ADAPTIVE/MODERN | LEAN_MIXTURE / EXHAUST_AIR_LEAK | positive | P0410 |
| ERR-MF-001 | coil_on_plug_insulation_arc | misfire | ADAPTIVE/MODERN | IGNITION_MISFIRE | variable (+) | P0300, P030X |
| ERR-MF-002 | spark_plug_carbon_fouled | misfire | ALL | IGNITION_MISFIRE | variable | P0300, P030X |
| ERR-MF-003 | spark_plug_gap_erosion | misfire | ALL | LEAN_MISFIRE | slightly + | P0300 intermittent |
| ERR-MF-004 | ignition_coil_primary_winding_failure | misfire | ALL | IGNITION_MISFIRE | positive | P030X specific |
| ERR-MF-005 | dead_injector_cylinder_misfire | misfire | ALL | LEAN_MISFIRE | positive (lean bank) | P0201–P0208, P030X |
| ERR-MF-006 | low_compression_mechanical_misfire | misfire | ALL | IGNITION_MISFIRE / POA_SIGNATURE | variable | P030X |
| ERR-MF-007 | gdi_intake_valve_carbon_buildup | misfire | ADAPTIVE/MODERN | LEAN_MISFIRE | slightly + | P0300, P0171 |
| ERR-SF-001 | upstream_o2_sensor_lazy_response | sensor_fault | ALL | (perception lag — gas reads true) | oscillating | P0133, P0153 |
| ERR-SF-002 | upstream_o2_sensor_fixed_voltage | sensor_fault | ALL | (perception stuck — gas reads true) | pegged | P0130–P0132, P0136 |
| ERR-SF-003 | maf_sensor_under_reading | sensor_fault | ADAPTIVE/MODERN | LEAN_MIXTURE | positive | P0100–P0103 |
| ERR-SF-004 | map_sensor_calibration_drift | sensor_fault | ALL | LEAN or RICH | + or − | P0105–P0108 |
| ERR-SF-005 | coolant_temp_sensor_stuck_cold | sensor_fault | ALL | RICH_MIXTURE | negative | P0116–P0118 |
| ERR-SF-006 | downstream_o2_sensor_contaminated | sensor_fault | ADAPTIVE/MODERN | (apparent cat failure) | normal | P0420, P0430 |
| ERR-EF-001 | fuel_trim_adaptation_saturated | ecu_fault | ALL | LEAN or RICH | at ±25 % limit | P0171/2/4/5 |
| ERR-EF-002 | closed_loop_fuel_control_disabled | ecu_fault | ALL | (open-loop fixed enrichment) | not tracking | P0140, OL flag |
| OPTIMAL_HEALTH | optimal_health | no_fault | ALL | NORMAL_OPERATION | within ±5 % | none |

> Registry note: `global_fault_registry.json` also retains three legacy v0.1 IDs
> (`ERR-E1-M032`→`ERR-LC-005`, `ERR-E2-I104`→`ERR-MF-001`, `ERR-E3-F501`→`ERR-RM-005`). The
> registry-consolidation task (`OPEN_LEVERS F1`, `COMWIKI-12`) folds the two split registries and
> remaps these rows — a known **+4 cases → 52.7 %** earned gain.

## Gas chemical-state definitions {#CONCEPT_GAS_STATES}

`chemical_state` is the primary routing signal. The full `ChemicalSignature` enum is **34-value**
(GAS_VOCABULARY §21); the values consumed by the taxonomy:

- **NORMAL_OPERATION** — λ 0.97–1.03, HC ≤ 50 ppm, CO ≤ 0.5 %, CO₂ ≥ 14.5 %
- **RICH_MIXTURE** — λ < 0.97, CO > 1.5 %, HC elevated
- **LEAN_MIXTURE** — λ > 1.03, O₂ > 1.5 %, CO ≈ 0
- **IGNITION_MISFIRE** — HC > 300 ppm with λ ≈ 1.0, CO₂ depressed, O₂ elevated
- **LEAN_MISFIRE** — HC elevated, O₂ elevated, λ > 1.03
- **POA_SIGNATURE** — HC very high (> 800 ppm), oil-burn, λ variable
- **EXHAUST_AIR_LEAK** — O₂ ≈ 20 %, λ > 1.30, CO₂ normal (false lean — dilution, not true lean)
- **GDI_HPFP_INTERNAL_SEAL_LEAK** — CO very high (> 5 %), HC very high, λ ≪ 0.95
- **INCOMPLETE_OXIDATION_DILUTION** — moderate HC, CO₂ elevated from recirculated exhaust, mild lean

### Gas-state → fault routing map {#RULE_GAS_ROUTE}

| chemical_state | faults that match |
|---|---|
| NORMAL_OPERATION | OPTIMAL_HEALTH |
| RICH_MIXTURE | ERR-RM-003/004/006/007, ERR-SF-005 |
| LEAN_MIXTURE | ERR-LC-001/002/003/004/007, ERR-SF-003/004, ERR-EF-001 |
| IGNITION_MISFIRE | ERR-RM-001, ERR-MF-001/002/004/006 |
| LEAN_MISFIRE | ERR-LC-004, ERR-MF-003/005/007 |
| POA_SIGNATURE | ERR-RM-001/002, ERR-MF-006 |
| GDI_HPFP_INTERNAL_SEAL_LEAK | ERR-RM-005 |
| EXHAUST_AIR_LEAK | ERR-LC-006/007 |
| EGR_DILUTION / INCOMPLETE_OXIDATION | ERR-LC-005, ERR-MF-003/005/007 |

The crucial property for the rework: **one gas state routes to many faults** (e.g.
`LEAN_MIXTURE` → 8 nodes). Single-snapshot chemistry cannot separate them — that is exactly the
collision set the two-point delta attacks (`COMWIKI-06`, `COMWIKI-11`).

## Trim grammar {#RULE_TRIM_GRAMMAR}

`total_trim_correction_delta` (OBD-derived, replaces raw `shrtft1 + longft1`). **Positive** = ECU
adding fuel (compensating lean); **negative** = pulling fuel (compensating rich).

- ±0–5 % — within closed-loop authority; no fault implied
- ±5–15 % — actively compensating; borderline
- ±15–25 % — strong fault signal; registry threshold for most rules
- > ±25 % — adaptation saturated; `ERR-EF-001`

## Graph relations (explicit)

**CONCEPT_TAXONOMY_TABLE** MAPS **fault_id** TO **family/horizon/gas_state/trim/DTC fingerprint**
**chemical_state** ROUTES_VIA **RULE_GAS_ROUTE** INTO **candidate fault set**
**one gas state → many faults** MOTIVATES **TEST_TWO_POINT (COMWIKI-11)**
**global_fault_registry.json + comlab/config/kg/*.json** ARE **the machine-readable source** (frozen)
**legacy v0.1 IDs** REMAPPED_BY **OPEN_LEVERS F1 (COMWIKI-12)**
**ERR-RM-001** ROUTED-BY **rich_mixture**
**ERR-LC-001** ROUTED-BY **lean_condition**
**ERR-MF-001** ROUTED-BY **misfire**
**ERR-SF-001** ROUTED-BY **sensor_fault**

## Core Entities

- **CONCEPT_TAXONOMY_TABLE** — Mapping of fault_id to family, horizon, gas state, trim, and DTC fingerprint. Consumer: `comlab/core/fault_atlas_router.py`.
- **CONCEPT_GAS_STATES** — Chemical state definitions from GASLab used in the taxonomy. Consumer: `comlab/core/fault_atlas_router.py`.
- **RULE_GAS_ROUTE** — Gas-state to candidate fault routing map. Consumer: `comlab/core/fault_atlas_router.py`.
- **RULE_TRIM_GRAMMAR** — Trim direction and magnitude limits used for secondary scoring. Consumer: `comlab/core/fault_atlas_router.py`.
