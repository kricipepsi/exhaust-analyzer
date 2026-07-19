---
node_type: "hld"
lab: "gaslab"
module: "gaslab"
subsystem: "architecture"
implements: []
consumers:
  - "lld: labs/gaslab/docs/LLD_GASLab.md"
  - "dld: labs/gaslab/docs/DLD_GASLab.md"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
drift_guards: []
tags: ["gaslab", "architecture", "hld"]
source: "labs/gaslab/docs/HLD_GASLab.md"
---

# HLD — GASLab
**Status:** Approved
**PRD Baseline:** PRD_GASLab v2.1
**Version:** 2.1
**Date:** 2026-06-10
**Change note:** Refreshed to the live code surface — contract widened 32 → **34** `ChemicalSignature` values (`WRONG_VALVE_TIMING` retired; `CAM_TIMING_RETARDED_MAP` / `CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED` added, per the v2.1 timing-taxonomy revision); GASLab now accepts an **optional second (high-idle / 2500 RPM) reading** plus `fuel_trim` for RPM-differential separation; `GasLabDnaView` slimmed to **13 fields** (`target_lambda_v112` single-value window replaces the old low/high pair; `co_high_idle` added; `secondary_air_equipped` removed).

---

## 1. Responsibility

GASLab accepts one or two 5-gas exhaust readings (idle, plus an optional high-idle / 2500 RPM reading) and a vehicle DNA view, computes the Brettschneider lambda as ground truth, validates sample quality, and classifies the reading into one of **34** `ChemicalSignature` values. It emits a typed `GasLabPayload` consumed by COMLab.

Brettschneider lambda is the **ground truth**; the ECU's perception is the thing it overrides, never the other way round. GASLab has **zero** knowledge of OBDLab, DTCLab, or COMLab internals — the only coupling is the typed JSON boundary.

---

## 2. Architecture Position

```
COMLab
  │  constructs GasLabDnaView from VIN record (13-field slice)
  │  supplies GasReading (idle) + GasLabContext
  │    └ context may carry: reading_high (2500 RPM), fuel_trim,
  │      lambda_measured, block_test_passed, engine_state
  ▼
gaslab.process.process(reading, context)
  │
  ├─ brettschneider.lambda_chem()      — λ ground truth (5-gas, NOx-corrected)
  ├─ validity_gates.sample_validity()  — triangle + dilution gate
  ├─ rule_engine.classify()            — 34-fault classification (idle ± high-idle)
  │     └─ resolution.apply_differentiators()
  └─ GasLabPayload
  │
  ▼
COMLab consumes:
  chemical_state   → POA_HISTORY injection (T-FX-3) + fault-atlas routing
  lambda_chem      → ground-truth λ vs ECU's normalized_obd_lambda
  lambda_measured  → no-OBD fallback for perception-contradiction detector (T-FX-7)
  sample_validity  → trust gate for downstream aggregation
```

The isolation (no `from obdlab …` / `from dtclab …`) is enforced by the import-isolation audit in the validator test suite. COMLab mirrors the types it needs locally rather than importing GASLab.

---

## 3. Internal Pipeline

```
GasReading (idle) [+ reading_high 2500 RPM] + GasLabContext
       │
  [1]  Load ontology (gas_lab_ontology.yaml)
       │  • 34 fault entries with 6-gas signature bounds
       │  • 6 DNA-gated + 1 requires_dtc entry
       │  • catch-all entries (VVT_FAILURE, EVAP_CANISTER_SATURATED, POA_SIGNATURE)
       │  • validity-gate thresholds + reasoning-grammar thresholds
       │
  [2]  Validity gates (validity_gates.py)
       │  triangle_gate:  CO + CO₂ + O₂ in [14, 16] → VALID
       │                  (16, 18]               → EXTERNAL_O2_SUSPECT
       │                  < 14 or > 18           → INVALID
       │  dilution_gate:  CO + CO₂ > 6.0         → not diluted
       │  combined:       INVALID → SAMPLE_INVALID (halt)
       │
  [3]  Definitive overrides (rule_engine._definitive_match) — first to fire wins
       │  low-triangle air ingress              → EXHAUST_AIR_LEAK
       │  EXTERNAL_O2_SUSPECT leak + fuel_trim   → EXHAUST_AIR_LEAK (trim > 8) /
       │                                           SAMPLE_INVALID (trim ≤ 8)   (T-GV2-12)
       │  validity INVALID                       → SAMPLE_INVALID
       │  priority 87: Coolant rule              → COOLANT_LEAK_INTERNAL (gated by block_test_passed)
       │  priority 85: Masking rule              → IGNITION_MISFIRE (with cylinder-count inference)
       │  priority 82: Cam-timing rule           → CAM_TIMING_RETARDED_MAF / CAM_TIMING_ADVANCED
       │                                           (high-idle vector confirms when reading_high present)
       │  RPM-differential routes                → engine_state-dependent
       │  priority 80: Collision rule            → RICH_MISFIRE / EXHAUST_AIR_LEAK
       │  priority 40: Rich-timing branch        → CAM_TIMING_RETARDED_MAP (needs reading_high)
       │
  [4]  Bound matching (ontology signatures)
       │  faults where reading is within all 6 gas bounds AND operating_state == engine_state
       │  NORMAL_OPERATION λ/CO bounds CoC-adjusted from DNA
       │    (target_lambda_v112 window; co_low_idle / Euro-scaled CO ceiling)
       │  O2_SENSOR_BIASED_LOW/HIGH bounds calibrated for wideband upstream sensors
       │  SAMPLE_INVALID + COOLANT_LEAK_INTERNAL excluded (grammar-gated only)
       │
  [5]  Differentiator + RPM-family resolution (resolution.py)
       │  dna_gate:            strict — fuel_delivery_type, has_catalyst, egr_equipped
       │  dna-type edges:      field equality checks
       │  rpm_differential:    idle→2500 behaviour (normalise / persist / NOx-rise)
       │    • lean-vs-cam-MAF mutual exclusion
       │    • cam-timing persist/normalise gates (MAP / MAF / ADVANCED)
       │    • low-HC misfire pruning when timing confirmed
       │    • catalyst dual-idle weak-vs-dead routing
       │    • mechanical-wear family → leaf (WORN_VALVE_SEALS / WORN_PISTON_RINGS /
       │      WORN_ENGINE / POA_SIGNATURE)
       │
  [6]  Candidate rank — (catch_all last, lowest Σ range widths)
       │  Tie → ontology declaration order; no candidates → NORMAL_OPERATION
       │
  GasLabPayload (9 fields)
```

---

## 4. Knowledge Base

`gas_lab_ontology.yaml` is the sole source of fault signatures. It is versioned (`version:` key) and carries `validity_gates`, `reasoning_grammar`, and the 34 `faults`. The `parse_vocabulary_thresholds()` drift guard in the validator suite keeps all numeric thresholds in sync with `GAS_VOCABULARY.md §10`. Changing a threshold in the YAML without updating the wiki breaks CI.

**34 fault entries by category:**

| Category | Faults |
|----------|--------|
| Normal | `NORMAL_OPERATION` |
| Lambda band | `LEAN_MIXTURE`, `RICH_MIXTURE` |
| Misfire | `IGNITION_MISFIRE`, `LEAN_MISFIRE`, `RICH_MISFIRE`, `EGR_DILUTION_MISFIRE`, `INCOMPLETE_COMBUSTION` |
| Cam timing (new in v2.1) | `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED` |
| Ignition timing | `TIMING_OVER_ADVANCED`, `TIMING_RETARDED` |
| Catalyst (DNA-gated) | `CATALYST_NOT_LIGHTING_OFF`, `CATALYST_OVERWHELMED`, `INCOMPLETE_OXIDATION` |
| Air/vacuum | `EXHAUST_AIR_LEAK`, `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` |
| O2 sensor | `O2_SENSOR_BIASED_LOW`, `O2_SENSOR_BIASED_HIGH` |
| EGR (DNA-gated) | `EGR_STUCK_CLOSED`, `EGR_STUCK_OPEN` |
| GDI (DNA-gated) | `GDI_INTAKE_VALVE_CARBON`, `GDI_HPFP_INTERNAL_SEAL_LEAK` |
| Combustion quality | `HIGH_COMBUSTION_TEMP` |
| Mechanical | `FLAT_CAMSHAFT`, `WORN_PISTON_RINGS`, `WORN_VALVE_SEALS`, `WORN_ENGINE` |
| Cooling | `COOLANT_LEAK_INTERNAL` |
| Catch-all | `VVT_FAILURE`, `EVAP_CANISTER_SATURATED`, `POA_SIGNATURE` |
| Invalid | `SAMPLE_INVALID` (ontology entry; emitted by the validity gate, excluded from bound matching) |

`WRONG_VALVE_TIMING` is **retired** — replaced by the three `CAM_TIMING_*` states, which the tailpipe can only mark `SPECIFIC` (not `DEFINITIVE`): gas chemistry cannot prove cam *phase* alone, so the MAP/MAF split rides a gas-direction discriminator corroborated by OBD trims and (downstream) CKP/CMP correlation.

---

## 5. DNA-Gate Architecture

In the v1/v2 pipeline the DNA gate is applied **strictly and unconditionally**: a fault is suppressed whenever its gate field does not match the DNA view. The `GasLabDnaView.confidence` field (`HIGH` / `PARTIAL` / `NONE`) is carried and forwarded to COMLab and is **not** consumed by the strict gate. It *is* read in one narrow place — the rich-CO ceiling for the `CAM_TIMING_RETARDED_MAP` branch uses the per-vehicle `co_high_idle` **only when `confidence == "HIGH"`** (otherwise the Euro-scaled default applies). There is no broad HIGH/PARTIAL/NONE branching in `apply_differentiators`.

6 DNA-gated faults in the ontology:

| Fault | Gate field | Gate value |
|-------|-----------|-----------|
| `CATALYST_NOT_LIGHTING_OFF` | `has_catalyst` | `true` |
| `CATALYST_OVERWHELMED` | `has_catalyst` | `true` |
| `GDI_INTAKE_VALVE_CARBON` | `fuel_delivery_type` | `"GDI"` |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | `fuel_delivery_type` | `"GDI"` |
| `EGR_STUCK_CLOSED` | `egr_equipped` | `true` |
| `EGR_STUCK_OPEN` | `egr_equipped` | `true` |

The three `CAM_TIMING_*` states are deliberately **not** DNA-gated: there is no DNA field for MAF-vs-MAP air metering, and inventing one would add a field with no consumer (signal/noise violation). The split is carried by the gas-direction discriminator instead.

---

## 6. Dual-RPM Input (L1 idle + L2 high-idle)

`GasLabContext.reading_high` carries an optional second reading at 2500 RPM. When present it unlocks the **RPM-differential discriminators** that separate faults whose single-point idle signatures overlap:

- **Lean vs cam-MAF:** a vacuum/fuel lean *normalises* toward λ≈1 at 2500 RPM; a retarded-cam (MAF) lean *persists*.
- **Cam-timing family:** MAP (rich, partially normalising), MAF (lean, persisting), ADVANCED (rough idle + idle λ-offset, NOx rising / HC falling at 2500).
- **Ignition over-advance vs cam:** clean idle with a NOx-only 2500 spike is ignition timing, not cam timing.
- **Catalyst weak-vs-dead:** a weak cat is healthy at 2500 but degraded at idle; a dead cat is degraded at both.
- **Mechanical wear:** the idle→2500 HC change direction routes the `POA_SIGNATURE` / `WORN_*` family to a specific leaf.

When `reading_high` is absent the engine still classifies on the idle reading alone, but the RPM-differential branches are skipped.

---

## 7. COMLab Integration Points

| `GasLabPayload` field | COMLab consumer |
|----------------------|----------------|
| `chemical_state` | `POA_HISTORY` injection into DTCLab routing_tags when `== POA_SIGNATURE` (T-FX-3); fault-atlas routing |
| `lambda_chem` | Ground-truth lambda; COMLab computes delta vs `OBDLivePayload.normalized_obd_lambda` |
| `lambda_measured` | Optional directly-measured analyser λ; no-OBD fallback for the perception-contradiction detector (T-FX-7) |
| `sample_validity` | Gates whether chemistry data is trustworthy for downstream aggregation |
| `gas_co`, `gas_hc`, `gas_co2`, `gas_o2`, `gas_nox` | Stored in COMLab report |

`family_map.SIGNATURE_TO_FAMILY` mirrors the COMLabSimple canonical-family vocabulary (13 families) locally, mapping each of the 34 signatures to a fusion family. It is a local mirror, not a cross-lab import.

---

## 8. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Boundary coverage | ≥ 95% of the synthetic boundary grid correctly classified (CI generative suite) |
| Import isolation | 0 cross-lab Python imports |
| Schema drift | 0 enum drift between ontology and `GAS_VOCABULARY.md` |
| Determinism | Same inputs → same output always (frozen models, no I/O on the hot path) |

---

## 9. Known Gaps

| ID | Description | Status |
|----|-------------|--------|
| Cross-lab enum mirror | `OBD_VOCABULARY.md §17` / COMLab schema still at 32; GASLab side intentionally divergent until the coordinated breaking change lands | Tracked |
| T-P5-1b | Near-identical triplet `FLAT_CAMSHAFT` ↔ `O2_SENSOR_BIASED_LOW` ↔ `WORN_PISTON_RINGS` — resolved at single-point idle only; full differentiator edges still v2 | Partially addressed via RPM-differential |
| Ontology header | `gas_lab_ontology.yaml` header comment still reads "32 fault entries / version 1.0" while it carries 34 — code-side cleanup, not a doc concern | Tracked (coder) |
| `REGULATORY_HIGH_IDLE` / `STRESS_IDLE` scope | Ontology `operating_state` still `STABILIZED_IDLE` for all faults; high-idle enters via `reading_high` discriminators, not as a separate operating state | v2 |
