# Noise Characterization Report

**Date:** 2026-06-07  
**Seed:** 42  
**Distribution:** uniform  
**Amplitude levels (fraction of box width):** [0.0, 0.1, 0.25, 0.5, 1.0]  
**Samples per level:** 100  
**Boxes characterized:** 34  

> **Characterization, not a gate.** This report measures how far a reading can drift from a box centroid before the classifier changes its label. No degradation threshold is asserted. Retention is measured against each box's *observed centroid label* (not its signature) so the overlap ceiling (T-TH-2) is not conflated with noise brittleness.

Characterization of **34 box(es)** across amplitude levels [0.0, 0.1, 0.25, 0.5, 1.0] (uniform, seed=42, 100 samples/level).  
Mean retention at amplitude 1.0: **57.1%**.  
**30 box(es)** classify their own centroid as a different signature (overlap artifact — see `T-TH-2_overlap_report.md`); retention is still measured against the observed baseline label.

## Aggregate degradation curve

| Amplitude | Mean retention % | Boxes fully retained | Boxes fully collapsed |
|---|---|---|---|
| 0.0 | 100.0 | 34 | 0 |
| 0.1 | 93.0 | 22 | 0 |
| 0.25 | 83.4 | 12 | 0 |
| 0.5 | 73.2 | 0 | 0 |
| 1.0 | 57.1 | 0 | 0 |

## Per-box retention

| Box | Baseline label | a=0.0 | a=0.1 | a=0.25 | a=0.5 | a=1.0 | brittle? |
|---|---|---|---|---|---|---|---|
| CAM_TIMING_ADVANCED | SAMPLE_INVALID ⚠ | 100% | 100% | 100% | 93% | 94% |  |
| CAM_TIMING_RETARDED_MAF | SAMPLE_INVALID ⚠ | 100% | 100% | 98% | 91% | 93% |  |
| CAM_TIMING_RETARDED_MAP | SAMPLE_INVALID ⚠ | 100% | 100% | 97% | 94% | 91% |  |
| CATALYST_NOT_LIGHTING_OFF | VVT_FAILURE ⚠ | 100% | 100% | 100% | 99% | 88% |  |
| CATALYST_OVERWHELMED | NORMAL_OPERATION ⚠ | 100% | 74% | 46% | 21% | 15% | yes |
| COOLANT_LEAK_INTERNAL | SAMPLE_INVALID ⚠ | 100% | 100% | 100% | 91% | 96% |  |
| EGR_DILUTION_MISFIRE | SAMPLE_INVALID ⚠ | 100% | 100% | 96% | 90% | 89% |  |
| EGR_STUCK_CLOSED | HIGH_COMBUSTION_TEMP ⚠ | 100% | 100% | 100% | 73% | 6% |  |
| EGR_STUCK_OPEN | NORMAL_OPERATION ⚠ | 100% | 92% | 50% | 27% | 13% |  |
| EVAP_CANISTER_SATURATED | SAMPLE_INVALID ⚠ | 100% | 100% | 100% | 93% | 85% |  |
| EXHAUST_AIR_LEAK | SAMPLE_INVALID ⚠ | 100% | 100% | 100% | 94% | 93% |  |
| FLAT_CAMSHAFT | TIMING_RETARDED ⚠ | 100% | 48% | 41% | 40% | 8% | yes |
| GDI_HPFP_INTERNAL_SEAL_LEAK | NORMAL_OPERATION ⚠ | 100% | 90% | 42% | 22% | 16% | yes |
| GDI_INTAKE_VALVE_CARBON | SAMPLE_INVALID ⚠ | 100% | 90% | 82% | 86% | 96% |  |
| HIGH_COMBUSTION_TEMP | HIGH_COMBUSTION_TEMP | 100% | 100% | 100% | 65% | 7% |  |
| IGNITION_MISFIRE | SAMPLE_INVALID ⚠ | 100% | 100% | 98% | 92% | 95% |  |
| INCOMPLETE_COMBUSTION | SAMPLE_INVALID ⚠ | 100% | 100% | 98% | 93% | 96% |  |
| INCOMPLETE_OXIDATION | SAMPLE_INVALID ⚠ | 100% | 100% | 97% | 93% | 88% |  |
| LEAN_MISFIRE | SAMPLE_INVALID ⚠ | 100% | 98% | 84% | 94% | 96% |  |
| LEAN_MIXTURE | SAMPLE_INVALID ⚠ | 100% | 83% | 75% | 91% | 92% |  |
| NORMAL_OPERATION | TIMING_RETARDED ⚠ | 100% | 57% | 44% | 44% | 9% | yes |
| O2_SENSOR_BIASED_HIGH | O2_SENSOR_BIASED_HIGH | 100% | 100% | 100% | 98% | 9% |  |
| O2_SENSOR_BIASED_LOW | VVT_FAILURE ⚠ | 100% | 100% | 100% | 66% | 45% |  |
| POA_SIGNATURE | SAMPLE_INVALID ⚠ | 100% | 100% | 96% | 91% | 93% |  |
| RICH_MISFIRE | SAMPLE_INVALID ⚠ | 100% | 100% | 100% | 98% | 90% |  |
| RICH_MIXTURE | INCOMPLETE_OXIDATION ⚠ | 100% | 87% | 32% | 12% | 1% | yes |
| SAMPLE_INVALID | SAMPLE_INVALID | 100% | 100% | 99% | 94% | 96% |  |
| TIMING_OVER_ADVANCED | HIGH_COMBUSTION_TEMP ⚠ | 100% | 100% | 100% | 62% | 8% |  |
| TIMING_RETARDED | TIMING_RETARDED | 100% | 100% | 100% | 87% | 12% |  |
| VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | NORMAL_OPERATION ⚠ | 100% | 94% | 44% | 28% | 16% | yes |
| VVT_FAILURE | SAMPLE_INVALID ⚠ | 100% | 100% | 99% | 95% | 94% |  |
| WORN_ENGINE | VVT_FAILURE ⚠ | 100% | 94% | 76% | 44% | 33% |  |
| WORN_PISTON_RINGS | TIMING_RETARDED ⚠ | 100% | 55% | 51% | 46% | 20% |  |
| WORN_VALVE_SEALS | SAMPLE_INVALID ⚠ | 100% | 100% | 92% | 81% | 58% |  |

## Brittle boxes (retention < 50% at amplitude 0.25)

These signatures lose their baseline label fastest under noise — the least field margin. Source citations let the architect target wiki/box refinement.

- **RICH_MIXTURE** — 32% retained at a=0.25  
  _GAS_WIKI §7.2; GAS_VOCABULARY §10.2 clear_rich_
- **FLAT_CAMSHAFT** — 41% retained at a=0.25  
  _GAS_WIKI §7.17; GAS_VOCABULARY §10.1-10.5_
- **GDI_HPFP_INTERNAL_SEAL_LEAK** — 42% retained at a=0.25  
  _GAS_WIKI §7.20; GAS_VOCABULARY §10.2 very_rich §3.1 dna_gate (same gas as VAC; differentiated by fuel_delivery_type=GDI)_
- **NORMAL_OPERATION** — 44% retained at a=0.25  
  _GAS_WIKI §7.1; GAS_VOCABULARY §10.1-10.5_
- **VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** — 44% retained at a=0.25  
  _GAS_WIKI §7.19; GAS_VOCABULARY §10.2 very_rich_
- **CATALYST_OVERWHELMED** — 46% retained at a=0.25  
  _GAS_WIKI §7.10; GAS_VOCABULARY §10.5 elevated_idle §3.1 dna_gate_

## Overlap caveat

The following boxes classify their own centroid as a *different* signature. This is an overlap artifact (see `T-TH-2_overlap_report.md`), not a noise finding. Retention for these boxes is measured against the observed baseline label, marked ⚠ in the per-box table:

- **CAM_TIMING_ADVANCED** → centroid classifies as `SAMPLE_INVALID`
- **CAM_TIMING_RETARDED_MAF** → centroid classifies as `SAMPLE_INVALID`
- **CAM_TIMING_RETARDED_MAP** → centroid classifies as `SAMPLE_INVALID`
- **CATALYST_NOT_LIGHTING_OFF** → centroid classifies as `VVT_FAILURE`
- **CATALYST_OVERWHELMED** → centroid classifies as `NORMAL_OPERATION`
- **COOLANT_LEAK_INTERNAL** → centroid classifies as `SAMPLE_INVALID`
- **EGR_DILUTION_MISFIRE** → centroid classifies as `SAMPLE_INVALID`
- **EGR_STUCK_CLOSED** → centroid classifies as `HIGH_COMBUSTION_TEMP`
- **EGR_STUCK_OPEN** → centroid classifies as `NORMAL_OPERATION`
- **EVAP_CANISTER_SATURATED** → centroid classifies as `SAMPLE_INVALID`
- **EXHAUST_AIR_LEAK** → centroid classifies as `SAMPLE_INVALID`
- **FLAT_CAMSHAFT** → centroid classifies as `TIMING_RETARDED`
- **GDI_HPFP_INTERNAL_SEAL_LEAK** → centroid classifies as `NORMAL_OPERATION`
- **GDI_INTAKE_VALVE_CARBON** → centroid classifies as `SAMPLE_INVALID`
- **IGNITION_MISFIRE** → centroid classifies as `SAMPLE_INVALID`
- **INCOMPLETE_COMBUSTION** → centroid classifies as `SAMPLE_INVALID`
- **INCOMPLETE_OXIDATION** → centroid classifies as `SAMPLE_INVALID`
- **LEAN_MISFIRE** → centroid classifies as `SAMPLE_INVALID`
- **LEAN_MIXTURE** → centroid classifies as `SAMPLE_INVALID`
- **NORMAL_OPERATION** → centroid classifies as `TIMING_RETARDED`
- **O2_SENSOR_BIASED_LOW** → centroid classifies as `VVT_FAILURE`
- **POA_SIGNATURE** → centroid classifies as `SAMPLE_INVALID`
- **RICH_MISFIRE** → centroid classifies as `SAMPLE_INVALID`
- **RICH_MIXTURE** → centroid classifies as `INCOMPLETE_OXIDATION`
- **TIMING_OVER_ADVANCED** → centroid classifies as `HIGH_COMBUSTION_TEMP`
- **VACUUM_REGULATOR_DIAPHRAGM_RUPTURE** → centroid classifies as `NORMAL_OPERATION`
- **VVT_FAILURE** → centroid classifies as `SAMPLE_INVALID`
- **WORN_ENGINE** → centroid classifies as `VVT_FAILURE`
- **WORN_PISTON_RINGS** → centroid classifies as `TIMING_RETARDED`
- **WORN_VALVE_SEALS** → centroid classifies as `SAMPLE_INVALID`

