---
chunk_id: COMWIKI-03
title: Vehicle DNA & Candidate Pruning
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: How VehicleDNA projects into three LabDnaViews and gates the candidate fault
  set by hardware before any scoring, plus the polymorphic VE and O2 math that DNA
  selects.
entities_defined:
- CONCEPT_LABDNAVIEW
- RULE_HW_PRUNE
- CONCEPT_VE_POLYMORPH
- CONCEPT_O2_POLYMORPH
- CONCEPT_DNA_CONFIDENCE
related_chunks:
- COMWIKI-02
- COMWIKI-04
- COMWIKI-07
sources:
- COMLab_HLD.md §6
- NewArchProposal.md
- SEMANTIC_CONTRACT.md §3/§6
- COMLab_LLD.md §6
node_type: wiki
lab: comlab
module: comlab
subsystem: hardware-pruning
implements:
- labs/comlab/comlab/core/ecu_hardware_checker.py
- labs/comlab/comlab/schemas/lab_dna_views.py
- labs/comlab/comlab/projection.py
consumers:
- 'comlab: labs/comlab/comlab/core/ecu_hardware_checker.py ECU-hardware digital-lie
  evidence (fault_atlas_router.py:1312, ecu_fault family)'
- 'comlab: labs/comlab/comlab/analytics/delta_engine.py VE polymorph selection'
- 'comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py vin_confidence==NONE
  fatal gate (ERR-ABORT-004)'
drift_guards:
- labs/comlab/tests/unit/test_ecu_hardware_checker.py
- labs/comlab/tests/unit/test_projection.py
tags:
- comlab
- hardware-pruning
- wiki
source: labs/comlab/wiki/03_vehicle_dna_pruning.md
---

# Vehicle DNA & Candidate Pruning

`VehicleDNA` is the vehicle-hardware profile DNALab decodes from the VIN + symptom input. It is
the single source of architectural truth about the vehicle under test. **COMLab reads it; it
never modifies it and never re-derives the horizon from the VIN string** (forbidden, HLD §3).

## The three LabDnaViews {#CONCEPT_LABDNAVIEW}

At Stage-A step 6, COMLab projects the full `VehicleDNA` into three slim, read-only views — each
carrying only the fields relevant to one emitter lab. This keeps the cross-domain matrix
evaluation from depending on the whole DNA blob.

```
VehicleDNA (full)
   ├─► GasLabDnaView   (15 fields) → fuel-chemistry context
   ├─► ObdLabDnaView   (10 fields) → trim & sensor context
   └─► DtcLabDnaView   (11 fields) → routing & code context
```

- **GasLabDnaView** — displacement, cylinder count, banks, euro category, fuel delivery,
  induction, upstream O₂ type, secondary-air, catalyst, EGR, target λ (v1.1.2), CO idle limits,
  confidence, resolved horizon.
- **ObdLabDnaView** — displacement, cylinder count, rated RPM, `stress_idle_rpm_target`, air
  metering strategy, upstream O₂ type, induction, EGR, resolved horizon, confidence.
- **DtcLabDnaView** — make, model, model year, euro category, air metering strategy, resolved
  horizon, particulate filter, catalyst, EGR, secondary-air, confidence.

## Hardware-flag → fault gating {#RULE_HW_PRUNE}

A registry row whose `preconditions` requires a flag the vehicle's DNA does **not** set is
pruned in Stage-B Pass 2 **before** any operator scoring. This is pure candidate elimination —
it cannot create a verdict, only remove impossibilities.

```
fuel_delivery_type = GDI
   └─ enables  ERR-RM-005 (HPFP seal leak), ERR-MF-007 (GDI intake carbon)
   └─ disables ERR-RM-007 (FPR diaphragm — vacuum-referenced FPR is port-injection only)
emissions.egr_equipped = true            └─ enables ERR-LC-005 (EGR stuck open)
emissions.secondary_air_equipped = true  └─ enables ERR-LC-007 (SAI stuck on)
emissions.downstream_o2_present = true   └─ enables ERR-SF-006 + Stage-D cat-efficiency calc
air_metering.has_maf_sensor = true       └─ enables ERR-LC-001, ERR-LC-002, ERR-SF-003
air_metering.has_map_sensor = true       └─ enables ERR-SF-004
induction_type = TURBO/SUPERCHARGED      └─ boost-specific rules + Δ sign inversion (COMWIKI-11)
```

## Polymorphic VE math {#CONCEPT_VE_POLYMORPH}

`air_metering_strategy` changes how `ve_pct` is computed and how COMLab evaluates VE-based
operators. **This is the gate that the reworked delta module also branches on first**
(`COMWIKI-11` `RULE_DELTA_GATE`).

| Strategy | VE source | COMLab implication |
|---|---|---|
| `MAF_ONLY` | MAF g/s → VE | MAF health drives VE; MAF fault = VE anomaly |
| `MAP_ONLY_SPEED_DENSITY` | MAP+RPM+IAT → speed-density VE | MAP drives VE; **a real leak nulls ΔTrim** — route to IAC/throttle, not the leak profile |
| `DUAL_MAF_MAP_CROSSCHECK` | both, cross-checked | MAF↔MAP discrepancy is itself diagnostic; **only here is a VE fault independent evidence** (`T-COMV2-VE-GATE-1`, audit Q5) |

## Polymorphic O₂ normalisation {#CONCEPT_O2_POLYMORPH}

`upstream_o2_type` selects the `normalized_obd_lambda` path used by perception-vs-truth rules:

| upstream_o2_type | normalisation | era |
|---|---|---|
| `NARROWBAND` | switching frequency → λ estimate | ADAPTIVE typical |
| `WIDEBAND_AFR` | λ = AFR / 14.71 | MODERN |
| `WIDEBAND_LAMBDA` | direct λ | MODERN |
| `WIDEBAND_NB_SIM` | switching-pattern decode (T-FX-4) | some MODERN ECUs |
| `NONE` | not available | LEGACY / sensor-deleted |

The **perception-vs-truth axis** compares `normalized_obd_lambda` (what the ECU believes) to GAS
`lambda_chem` (ground truth). When they diverge beyond the era `lambda_tolerance` (0.10 LEGACY /
0.05 ADAPTIVE / 0.02 MODERN — `eras_sensitivity_masks.yaml`, `COMWIKI-04`), a sensor fault or
air-path anomaly is present. Implemented in `core/perception_contradiction.py`. The rework feeds
this divergence into fusion **as a contradiction feature**, not a hard override (`COMWIKI-08`).

## Confidence & degradation {#CONCEPT_DNA_CONFIDENCE}

| VIN confidence | effect |
|---|---|
| `HIGH` | full DNA-relative pruning; all hardware gates active |
| `PARTIAL` | best-guess defaults; `degradation_mode = GAS_DOMINANT`; verdict confidence-capped |
| `NONE` | Stage-A abort (`ERR-ABORT-004`); no verdict |

When confidence is `PARTIAL`, the Stage-C KG enrichment still runs (enrichment is always safe to
display); the uncertainty is in Stage-B scoring, not the enrichment.

## Graph relations (explicit)

**VehicleDNA** PROJECTED_INTO **GasLabDnaView, ObdLabDnaView, DtcLabDnaView**
**RULE_HW_PRUNE** RUNS_BEFORE **RULE_SCORING (COMWIKI-07)**
**air_metering_strategy** SELECTS **CONCEPT_VE_POLYMORPH** AND GATES **RULE_DELTA_GATE (COMWIKI-11)**
**upstream_o2_type** SELECTS **CONCEPT_O2_POLYMORPH**
**VIN confidence = NONE** TRIGGERS **Stage-A abort**

## Core Entities

- **CONCEPT_LABDNAVIEW** — Projection of the full VehicleDNA into three slim, read-only views for each emitter lab. Consumer: `comlab/core/ecu_hardware_checker.py`.
- **RULE_HW_PRUNE** — Candidate fault elimination based on hardware-flag mismatch in DNA. Consumer: `comlab/core/ecu_hardware_checker.py (Stage B Pass 2)`.
- **CONCEPT_VE_POLYMORPH** — Polymorphic volumetric efficiency calculations selected by air metering strategy. Consumer: `comlab/core/ecu_hardware_checker.py and comlab/analytics/delta_engine.py`.
- **CONCEPT_O2_POLYMORPH** — Upstream O₂ sensor normalization chosen by O₂ sensor type. Consumer: `comlab/core/ecu_hardware_checker.py`.
- **CONCEPT_DNA_CONFIDENCE** — Confidence-based degradation logic (HIGH vs PARTIAL vs NONE). Consumer: `comlab/core/ecu_hardware_checker.py and comlab/core/lab_pipeline_aggregator.py`.
