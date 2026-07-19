---
node_type: "prd"
lab: "gaslab"
module: "gaslab"
subsystem: "requirements"
implements: []
consumers:
  - "hld: labs/gaslab/docs/HLD_GASLab.md"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py GasLabPayload boundary"
drift_guards: []
tags: ["gaslab", "requirements", "prd"]
source: "labs/gaslab/docs/PRD_GASLab.md"
---

# PRD — GASLab
**Status:** Approved
**Version:** 2.1
**Date:** 2026-06-10
**Scope:** Petrol-only, v2 — Exhaust gas chemistry analysis module
**Change note:** Contract surface 32 → **34** `ChemicalSignature` values (v2.1 timing-taxonomy revision); **dual-RPM** input (L1 idle + optional L2 high-idle / 2500 RPM) for RPM-differential fault separation; 13-field DNA view.

---

## Section 1 — Summary

GASLab is the exhaust gas chemistry analysis module of 4DApp. It accepts one or two 5-gas analyser readings (idle, plus an optional high-idle / 2500 RPM reading) of HC, CO, CO₂, O₂, and NOx, plus a typed vehicle DNA view, computes the Brettschneider lambda as ground truth, gates sample validity, and classifies the reading into one of **34** `ChemicalSignature` values. The output `GasLabPayload` is consumed by COMLab as the chemistry ground-truth layer (L1/L2) of the 4DApp diagnostic pipeline.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| GASLab Owner | Module Owner | Brettschneider formula, 34-fault ontology, validity gates, RPM-differential separation |
| COMLab Team | Integration Consumer | Reads `GasLabPayload`; injects `POA_HISTORY` on `POA_SIGNATURE`; mirrors the enum |
| 4DApp Engineering Lead | Architecture | Signal/noise rule, cross-lab JSON contract |

---

## Section 3 — Background

**Context.** A 5-gas exhaust analyser measures CO, HC, CO₂, O₂, and NOx in the exhaust stream. These five gases encode the combustion event more completely than the ECU alone. The Brettschneider equation (1983) derives an air-fuel lambda value from this chemistry that is independent of the ECU's fuel-trim perception.

**Why now.** The 34-fault ontology (`gas_lab_ontology.yaml`, mirrored by the `ChemicalSignature` enum) is complete. The v2.1 timing-taxonomy revision retired the single `WRONG_VALVE_TIMING` value and replaced it with three system-specific cam-timing states (`CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED`), seating five timing states (two ignition + three cam) as first-class entries. A synthetic boundary-permutation grid plus a generative property suite (boundary / combinatorial / fuzz / noise / overlap) covers the fault signature space.

**What recently became possible.** Adding the optional **high-idle (2500 RPM) reading** unlocked RPM-differential discriminators that separate faults whose single-point idle signatures overlap — cam timing vs vacuum lean, weak vs dead catalyst, and the mechanical-wear family leaves — without inventing DNA fields that would have no consumer.

---

## Section 4 — Objective

**Business benefit.** Provide chemistry ground truth that overrides ECU perception when the two diverge — eliminating the "DTC says lean, gas says rich" diagnostic dead end.

**Customer benefit.** Technicians receive a single chemical signature label (e.g. `IGNITION_MISFIRE`, `EGR_STUCK_OPEN`, `CAM_TIMING_RETARDED_MAF`) derived from first principles, not from ECU heuristics.

**Key Results:**

- **KR1:** GASLab correctly classifies ≥ 95% of synthetic boundary-grid samples in CI (`tests/fixtures/synthetic_grid.py` + `tests/generative/`).
- **KR2:** Zero cross-lab Python imports (enforced by the import-isolation audit in the validator suite).
- **KR3:** All 34 `ChemicalSignature` values are reachable (verified by `test_rule_engine_reachability.py`): 6 via DNA gate, 1 via `requires_dtc`, 3 catch-all, 2 via reasoning-grammar gate (`SAMPLE_INVALID` from the validity gate, `COOLANT_LEAK_INTERNAL` from the coolant rule), the 3 `CAM_TIMING_*` via the cam-timing rule + RPM-differential gates, and the remainder via direct bound matching.
- **KR4:** Wiki drift guard (`parse_vocabulary_thresholds`) keeps ontology numeric thresholds in sync with `GAS_VOCABULARY.md §10` in every CI run.

---

## Section 5 — Market Segment

**Exhaust chemistry specialist / advanced workshop technician:** professionals who use a 5-gas analyser alongside an OBD scanner and need a tool that translates raw gas concentrations into a named fault without memorising Brettschneider thresholds or the 34-fault ontology — and who can take a second reading at 2500 RPM when the idle picture is ambiguous.

---

## Section 6 — Value Proposition

- **Jobs addressed:** chemical fault classification, lambda ground-truth computation, sample quality validation, RPM-differential separation of overlapping faults.
- **Gains created:** named fault output (`ChemicalSignature`) replaces manual gas-reading interpretation. DNA-gated suppression (e.g. catalyst faults only on catalyst-equipped vehicles) eliminates false positives automatically. The optional high-idle reading resolves faults that look identical at idle.
- **Pains relieved:** removes the manual cross-reference between gas readings and the vocabulary document. The exhaust gas triangle validity gate prevents diagnosis from a diluted or contaminated sample.
- **Competitive advantage:** 34-fault ontology with explicit overlap resolution, priority overrides, RPM-differential discriminators, and a generative test grid. The fault space is fully enumerated, not heuristic.

---

## Section 7 — Solution

### Key Features (all P0 unless noted)

- P0: Brettschneider 5-gas lambda computation with NOx correction.
- P0: Exhaust gas triangle validity gate (14 ≤ CO+CO₂+O₂ ≤ 16 → VALID).
- P0: Dilution screen (CO+CO₂ > 6.0 vol% → sample not diluted).
- P0: 34-fault ontology loaded from `gas_lab_ontology.yaml` with version control.
- P0: Priority-override rules (coolant 87, masking 85, cam-timing 82, collision 80, rich-timing 40).
- P0: DNA-gated fault suppression (6 gates: `has_catalyst` × 2, `fuel_delivery_type` × 2, `egr_equipped` × 2).
- P0: Dual-RPM input (`reading_high`) with RPM-differential family separation (cam timing, lean-vs-cam, catalyst weak-vs-dead, mechanical-wear leaves).
- P0: Per-vehicle CoC overrides — `target_lambda_v112` λ window, Euro-scaled CO/HC ceilings, wideband O₂-bias calibration.
- P0: `fuel_trim` context input for EXTERNAL_O2_SUSPECT leak disambiguation and mechanical-wear routing.
- P0: Specificity-based tie-breaking (narrowest signature wins; catch-alls last).
- P0: `GasLabPayload` Pydantic output model (9 fields, including `lambda_measured` for the no-OBD fallback).

### Technology

- Python ≥ 3.11 (project runs 3.14). Pydantic ≥ 2. PyYAML. No cross-lab imports.
- Package: `gaslab`, standalone `pyproject.toml`.
- Entry point: `gaslab.process.process(reading, context) → GasLabPayload`, where `context: GasLabContext` carries `dna`, `engine_state`, and optional `reading_high`, `fuel_trim`, `lambda_measured`, `block_test_passed`.

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| `Hcv = 1.85` is the correct H:C ratio for petrol | `test_brettschneider.py` stoich-unity test vs `GAS_VOCABULARY.md` |
| Bound matching is scoped to `STABILIZED_IDLE`; high-idle enters via `reading_high` | Per-fault `operating_state: STABILIZED_IDLE`; RPM-differential gates consume `reading_high` |
| All 6 DNA-gated faults and every added field have a named COMLab consumer | `test_validators.py` DNA-gate count test + signal/noise review |
| The three `CAM_TIMING_*` states need no MAF/MAP DNA field | Split carried by the gas-direction discriminator; no field without a consumer |

---

## Section 8 — Release

### v2.1 Scope

All P0 features above. Bound matching scoped to `STABILIZED_IDLE`; the high-idle reading is an optional second input that unlocks RPM-differential separation.

### Shipped since v1.0

- Timing taxonomy 32 → 34 (`WRONG_VALVE_TIMING` retired; 3 `CAM_TIMING_*` added).
- Dual-RPM input and RPM-differential family separation.
- Per-vehicle CoC `target_lambda_v112` window, Euro-class CO/HC scaling, wideband O₂-bias calibration.
- `lambda_measured` payload field (T-FX-7 no-OBD fallback).

### Explicitly Deferred (v2+)

- Cross-lab enum mirror: `OBD_VOCABULARY.md §17` / COMLab schema still at 32 — the breaking change is intentionally divergent until coordinated.
- Full `differentiator_edges` resolution of the near-identical triplet at single-point idle (`FLAT_CAMSHAFT` ↔ `O2_SENSOR_BIASED_LOW` ↔ `WORN_PISTON_RINGS`).
- `REGULATORY_HIGH_IDLE` / `STRESS_IDLE` as first-class operating states.

### Success Criteria

1. KR1–KR4 all pass in CI.
2. `test_ontology.py` confirms 34 faults, 6 DNA-gated entries, 1 `requires_dtc`, 3 catch-alls.
3. `test_rule_engine_reachability.py` confirms all 34 signatures are reachable.
4. `test_validators.py` wiki-drift guard passes.
