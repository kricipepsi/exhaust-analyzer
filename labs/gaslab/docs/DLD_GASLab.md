---
node_type: "dld"
lab: "gaslab"
module: "gaslab"
subsystem: "detailed-design"
implements:
  - "labs/gaslab/gaslab/contracts.py"
  - "labs/gaslab/gaslab/brettschneider.py"
  - "labs/gaslab/gaslab/validity_gates.py"
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
  - "labs/gaslab/gaslab/ontology_loader.py"
  - "labs/gaslab/gaslab/audits.py"
  - "labs/gaslab/gaslab/dna_view.py"
  - "labs/gaslab/gaslab/process.py"
  - "labs/gaslab/gaslab/family_map.py"
  - "labs/gaslab/gaslab/ranking.py"
  - "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py gas_co/gas_hc/gas_o2/lambda_chem"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py lambda_chem/lambda_measured/sample_validity"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py lambda_measured"
  - "comlab: labs/comlab/comlab/schemas/vocabulary.py sample_validity mirror"
drift_guards:
  - "labs/gaslab/tests/unit/test_contracts.py"
  - "labs/gaslab/tests/unit/test_brettschneider.py"
  - "labs/gaslab/tests/unit/test_validity_gates.py"
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_rule_engine_reachability.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_ontology.py"
  - "labs/gaslab/tests/unit/test_validators.py"
  - "labs/gaslab/tests/unit/test_process.py"
  - "labs/gaslab/tests/test_cases.py"
tags: ["gaslab", "detailed-design", "dld"]
source: "labs/gaslab/docs/DLD_GASLab.md"
---

# DLD — GASLab
**Status:** Approved
**PRD Baseline:** PRD_GASLab v2.1
**HLD Reference:** HLD_GASLab v2.1
**Version:** 2.1
**Date:** 2026-06-10
**Change note:** Refreshed to the live package — 34-value `ChemicalSignature`, 13-field `GasLabDnaView`, extended `GasLabContext` (`reading_high`, `fuel_trim`, `lambda_measured`), `GasLabPayload` `lambda_measured` field, new `family_map.py` / `ranking.py` modules, and the restructured `tests/unit` + `tests/generative` tree.

---

## 1. Module Map

```
gaslab/
├── __init__.py          — public exports (process, GasLabContext, contracts, DNA view)
├── contracts.py         — enums, physical constants, I/O models
├── brettschneider.py    — Brettschneider 5-gas lambda formula
├── validity_gates.py    — exhaust gas triangle + dilution gates
├── rule_engine.py       — classify(): definitive overrides + bound matching + resolution
├── resolution.py        — overlap detection, DNA gates, RPM-differential family separation
├── ontology_loader.py   — YAML loader with schema validation
├── audits.py            — collision audit + wiki-drift threshold parser
├── dna_view.py          — GasLabDnaView input model (13 fields)
├── process.py           — public entry point + GasLabContext
├── family_map.py        — ChemicalSignature → canonical fusion family (local mirror)
├── ranking.py           — GASLabSimple top-3 ranking (NOT on the process() path)
└── data/
    └── gas_lab_ontology.yaml
```

`family_map.py` and `ranking.py` exist in the package but are **not** invoked by `process()`. `ranking.py` is the out-of-scope GASLabSimple top-3 path; `family_map.SIGNATURE_TO_FAMILY` is a COMLab-facing convenience mirror used by `test_family_map.py`, not by classification.

---

## 2. `contracts.py`

### Physical Constants

| Name | Value | Source |
|------|-------|--------|
| `Hcv` | `1.85` | `GAS_VOCABULARY §6` — H:C ratio, petrol |
| `AFR_STOICH` | `14.71` | `GAS_VOCABULARY §6` — stoich AFR, petrol |
| `HC_FACTOR` | `0.0025` | `GAS_VOCABULARY §6` — ppm → vol% conversion |

### Enums (`StrEnum`)

**`ChemicalSignature`** — **34** values (`GAS_VOCABULARY §3`):
`NORMAL_OPERATION`, `RICH_MIXTURE`, `LEAN_MIXTURE`, `IGNITION_MISFIRE`, `LEAN_MISFIRE`, `RICH_MISFIRE`, `EXHAUST_AIR_LEAK`, `HIGH_COMBUSTION_TEMP`, `CATALYST_NOT_LIGHTING_OFF`, `CATALYST_OVERWHELMED`, `SAMPLE_INVALID`, `TIMING_OVER_ADVANCED`, `TIMING_RETARDED`, `O2_SENSOR_BIASED_LOW`, `O2_SENSOR_BIASED_HIGH`, `WORN_ENGINE`, `FLAT_CAMSHAFT`, `GDI_INTAKE_VALVE_CARBON`, `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE`, `GDI_HPFP_INTERNAL_SEAL_LEAK`, `WORN_VALVE_SEALS`, `WORN_PISTON_RINGS`, `POA_SIGNATURE`, **`CAM_TIMING_RETARDED_MAP`**, **`CAM_TIMING_RETARDED_MAF`**, **`CAM_TIMING_ADVANCED`**, `EGR_STUCK_CLOSED`, `EGR_STUCK_OPEN`, `VVT_FAILURE`, `EVAP_CANISTER_SATURATED`, `EGR_DILUTION_MISFIRE`, `INCOMPLETE_OXIDATION`, `INCOMPLETE_COMBUSTION`, `COOLANT_LEAK_INTERNAL`

> The three `CAM_TIMING_*` values replace the retired `WRONG_VALVE_TIMING` (v2.1 timing-taxonomy revision, 2026-06-03).

**`LambdaBand`** — 7 values: `HEAVILY_RICH`, `BORDERLINE_RICH`, `STOICHIOMETRIC`, `CATALYST_LIGHT_OFF`, `CATALYST_PEAK_EFFICIENCY`, `BORDERLINE_LEAN`, `HEAVILY_LEAN`

**`SampleValidity`** — 4 values: `VALID`, `BORDERLINE`, `INVALID`, `EXTERNAL_O2_SUSPECT`

**`EngineStateBucket`** — 4 values: `STABILIZED_IDLE`, `REGULATORY_HIGH_IDLE`, `STRESS_IDLE`, `COLD_OPEN_LOOP_INVALID`

**`GasBehavior`** — 6 values (`GAS_VOCABULARY §8`): `POSITIVE_SPIKE`, `POSITIVE_SHIFT`, `NORMAL`, `SUPPRESSED`, `INVERSE_CORRELATION`, `COLLISION`

**`CatalystStatus`** — 4 values (internal-only, `GAS_VOCABULARY §9`): `LIT_AND_WORKING`, `NOT_LIT`, `OVERWHELMED`, `NOT_EVALUABLE`

### `GasReading` (frozen dataclass)

Range bounds enforced in `__post_init__` (`GAS_VOCABULARY §2`); out-of-range raises `ValueError`.

| Field | Type | Constraint |
|-------|------|-----------|
| `hc` | `int` | ppm; `0 ≤ hc ≤ 20 000` |
| `co` | `float` | vol%; `0 ≤ co ≤ 15.0` |
| `co2` | `float` | vol%; `0 ≤ co2 ≤ 22.0` |
| `o2` | `float` | vol%; `0 ≤ o2 ≤ 22.0` |
| `nox` | `int` | ppm; `0 ≤ nox ≤ 5 000` |

### `GasLabPayload` (Pydantic BaseModel, 9 fields)

| Field | Type | COMLab Consumer |
|-------|------|----------------|
| `chemical_state` | `ChemicalSignature` | POA_HISTORY injection (T-FX-3); fault atlas |
| `gas_co` | `float` (0–15) | Stored in COMLab report |
| `gas_hc` | `int` (0–20 000) | Stored in COMLab report |
| `gas_co2` | `float` (0–22) | Stored in COMLab report |
| `gas_o2` | `float` (0–22) | Stored in COMLab report |
| `gas_nox` | `int` (0–5 000) | Stored in COMLab report |
| `lambda_chem` | `float` (0.5–2.5) | Ground-truth λ; delta vs `normalized_obd_lambda` |
| `sample_validity` | `SampleValidity` | Gates downstream trust |
| `lambda_measured` | `float \| None` (0.5–2.0) | Optional directly-measured analyser λ; no-OBD fallback for the perception-contradiction detector (T-FX-7) |

---

## 3. `brettschneider.py`

### `lambda_chem(reading: GasReading, hcv: float | None = None) → float`

```
hc_equiv   = reading.hc × HC_FACTOR          (GAS_VOCABULARY §6)
carbon_sum = co2 + co + hc_equiv
if carbon_sum == 0: return 1.0               (safe sentinel; classify() flags SAMPLE_INVALID)
lambda_4gas = (co2 + co/2 + o2) / carbon_sum
vol_sum = co + co2 + o2
nox_corr = (nox / 1e6) × 0.5 / (vol_sum/100)  if vol_sum > 0 else 0.0
return lambda_4gas + nox_corr
```

`hcv` is accepted but unused (HC weighting captured by `HC_FACTOR`); reserved for non-standard fuels.

---

## 4. `validity_gates.py`

```
triangle_gate(reading) → SampleValidity:
    s = co + co2 + o2
    s < 14   → INVALID
    s > 18   → INVALID
    s > 16   → EXTERNAL_O2_SUSPECT     # (16, 18]
    else     → VALID                   # [14, 16]

dilution_gate(reading) → bool:
    return (co + co2) > 6.0

sample_validity(reading) → SampleValidity:
    v = triangle_gate(reading)
    if v == INVALID: return INVALID
    if not dilution_gate(reading): return INVALID
    return v
```

---

## 5. `dna_view.py` — `GasLabDnaView` (frozen Pydantic, 13 fields)

| Field | Type | Constraints | Purpose |
|-------|------|------------|---------|
| `engine_displacement_liters` | `float` | `> 0` | stored |
| `cylinder_count` | `int` | `1–16` | masking-rule cylinder inference |
| `number_of_banks` | `int` | `1–4` | collision-rule routing |
| `euro_emission_category` | `str` | free text | Euro-scaled CO/HC ceilings |
| `fuel_delivery_type` | `str` | `"GDI"` / `"NON_GDI"` | GDI-gated fault suppression |
| `induction_type` | `str` | `"NA"` / `"forced"` / … | mechanical-wear (POA forced-induction) routing |
| `upstream_o2_type` | `str` | `"wideband"` / `"narrowband"` | O₂-bias signature calibration |
| `has_catalyst` | `bool` | | catalyst-gated suppression + dual-idle logic |
| `egr_equipped` | `bool` | | EGR-gated suppression |
| `target_lambda_v112` | `Optional[float]` | `[0.5, 2.5]` | certified CoC λ centre; `_coc_adjust_normal_bounds` NORMAL λ window `[v112±0.005]` |
| `co_low_idle` | `Optional[float]` | `[0, 15]` | per-vehicle CoC idle CO ceiling; NORMAL CO max |
| `co_high_idle` | `Optional[float]` | `[0, 15]` | per-vehicle CoC 2500 RPM CO ceiling; CAM_MAP rich-CO ceiling **when `confidence == HIGH`** |
| `confidence` | `str` | default `"NONE"` | carried for COMLab; gates only the `co_high_idle` override |

> Changes from v1: `target_lambda_low` + `target_lambda_high` collapsed to the single `target_lambda_v112`; `co_high_idle` added; `secondary_air_equipped` removed (no consumer).

---

## 6. `rule_engine.py`

### `classify(reading, dna, engine_state, ontology, block_test_passed=False, reading_high=None, fuel_trim=None) → tuple[ChemicalSignature, SampleValidity]`

```
Step 1: validity = sample_validity(reading)

Step 2: _definitive_match(...) — first decisive verdict wins, in order:
        a. low-triangle air ingress              → (EXHAUST_AIR_LEAK, EXTERNAL_O2_SUSPECT)
        b. EXTERNAL_O2_SUSPECT leak + fuel_trim   → leak (trim>8) / SAMPLE_INVALID (trim≤8)
        c. validity == INVALID                    → (SAMPLE_INVALID, INVALID)
        d. coolant (87): co2≤12, hc≥300, block_test_passed → COOLANT_LEAK_INTERNAL
        e. masking (85): hc>1000, o2>3, nox<50, inferred_cyl≥1 → IGNITION_MISFIRE
        f. cam-timing (82): hc>1000, o2>2, co>0 → CAM_TIMING_RETARDED_MAF / CAM_TIMING_ADVANCED
                                                   (high-idle confirms when reading_high present)
        g. RPM-differential routes
        h. collision (80): co>0.45, o2>2 → RICH_MISFIRE / EXHAUST_AIR_LEAK
        i. rich-timing (40, needs reading_high) → CAM_TIMING_RETARDED_MAP
        SAMPLE_INVALID and COOLANT_LEAK_INTERNAL are excluded from Step 3.

Step 3: bound matching (_matching_fault_candidates) — faults whose 6-gas signature matches
        AND operating_state == engine_state. DNA-driven bound adjustment:
          NORMAL_OPERATION       → _coc_adjust_normal_bounds (λ window + CO ceiling)
          O2_SENSOR_BIASED_LOW   → _calibrate_o2_bias_low_bounds (wideband)
          O2_SENSOR_BIASED_HIGH  → _calibrate_o2_bias_high_bounds (wideband)

Step 4: apply_differentiators(...) — DNA gates, dna-type/rpm edges, and the full
        RPM-differential family separation (LLD §6) when reading_high is present.

Step 5: rank by _candidate_rank = (signature_type == "catch_all", _specificity);
        no survivors → NORMAL_OPERATION.
```

Helper functions: `_specificity`, `_candidate_rank`, `_is_low_triangle_exhaust_air_leak`, `_is_external_o2_suspect_leak`, `_signature_values`, `_signature_matches`, `_coc_adjust_normal_bounds`, `_calibrate_o2_bias_low_bounds`, `_calibrate_o2_bias_high_bounds`, `_matching_fault_candidates`, `_resolve_candidates`, `_definitive_match`.

---

## 7. `resolution.py`

Public: `find_overlaps(ontology)`, `apply_differentiators(...)`, `is_resolved(candidates)`.

`apply_differentiators(candidates, reading, dna, ontology, engine_state=None, reading_high=None, fuel_trim=None)` applies, in order: `dna_gate` strict filter → `differentiator_edges` (`dna` equality / `rpm_differential` engine_state / `physical_check` informational) → RPM-differential family separation (lean normalisation, cam persist/normalise, lean-vs-cam-MAF exclusion, low-HC misfire pruning, ignition-over-advance promotion, mechanical-wear leaf routing, catalyst dual-idle) → `_append_rpm_routes`.

Euro/CoC helpers: `EuroThresholds` NamedTuple, `_euro_thresholds(dna)`, `_rich_co_ceiling(dna)` (`co_high_idle` override gated by `confidence == "HIGH"`). Family sets: `_CAM_TIMING_SIGNATURES`, `_MISFIRE_FAMILY_SIGNATURES`. `HC_IGNITION_MISFIRE_FLOOR = 1000`.

---

## 8. `ontology_loader.py`

`load_ontology(path=None) → dict` reads `gaslab/data/gas_lab_ontology.yaml`, `yaml.safe_load`, validates the 5 required top-level keys (`version`, `scope`, `validity_gates`, `reasoning_grammar`, `faults`), raises `OntologyLoadError(RuntimeError)` (carrying `path` + `detail`) on any failure.

---

## 9. `audits.py`

`find_uncovered_overlaps(ontology) → list[tuple[str, str]]` — fault pairs overlapping in all 6 gas dimensions with neither `dna_gate` nor `differentiator_edges` (catch-alls and `SAMPLE_INVALID` excluded). `parse_vocabulary_thresholds(vocab_md) → dict` — parses the `### 10.1`–`### 10.7` fenced YAML blocks from `GAS_VOCABULARY.md` for the wiki-drift guard; raises `ValueError` if the table format changes.

---

## 10. `family_map.py`

`CANONICAL_FAMILIES` (frozenset of 13 fusion families mirrored from COMLabSimple) and `SIGNATURE_TO_FAMILY` (exhaustive `ChemicalSignature` → family map across all 34 values). Local mirror, no cross-lab import. Used by `test_family_map.py`, not by `process()`.

---

## 11. `gas_lab_ontology.yaml` Schema

```yaml
version: "1.0"                                # NB: header still reads 32/1.0; carries 34 faults (coder cleanup)
scope: "Petrol 1990-2020 / 5-gas / warm-only"
validity_gates:
  exhaust_gas_triangle: { sum_valid_min: 14.0, sum_valid_max: 16.0, sum_external_o2_max: 18.0 }
  dilution_screen:      { co_plus_co2_floor: 6.0 }
reasoning_grammar:
  collision_rule:    { co_tier_max: 0.45, o2_threshold: 2.0, triangle_sum_threshold: 16.0, hc_max: 100 }
  masking_rule:      { hc_threshold: 1000, o2_threshold: 3.0, nox_threshold: 50 }
  cam_timing_rule:   { hc_threshold: 1000, o2_threshold: 2.0 }     # was wrong_valve_timing_rule
  coolant_intrusion_rule: { co2_threshold: 12.0, hc_threshold: 300.0 }  # priority 87
faults:
  <FAULT_NAME>:
    operating_state: STABILIZED_IDLE
    signature:
      hc:  { min: <int>,   max: <int> }
      co:  { min: <float>, max: <float> }
      co2: { min: <float>, max: <float> }
      o2:  { min: <float>, max: <float> }
      nox: { min: <int>,   max: <int> }
      lambda: { min: <float>, max: <float> }
    [dna_gate: { field: <str>, value: <str|bool> }]
    [requires_dtc: <bool>]
    [differentiator_edges: [{ type: dna|rpm_differential|physical_check, ... }]]
    [signature_type: catch_all]
```

All 34 v1/v2 faults carry `operating_state: STABILIZED_IDLE`; the high-idle (2500 RPM) discriminators run off `reading_high`, not a separate operating state.

---

## 12. Test Coverage

```
tests/
├── conftest.py
├── test_cases.py
├── fixtures/        descriptor.py, synthetic_grid.py, test_synthetic_grid_probes.py
├── unit/            test_brettschneider, test_classify_top3, test_contracts, test_dna_view,
│                    test_family_map, test_ontology, test_process, test_rank_candidates,
│                    test_resolution, test_rule_engine, test_rule_engine_reachability,
│                    test_t_p8_7_hc_discriminator, test_validators, test_validity_gates
└── generative/      test_boundary, test_combinatorial, test_fuzz, test_noise, test_overlap
```

| File | Coverage |
|------|---------|
| `unit/test_brettschneider.py` | Stoich near-unity, 5-gas, rich/stoich/lean sweep, custom `Hcv`, NOx correction |
| `unit/test_contracts.py` | 34 enum values, `GasReading` validation, `GasLabPayload` (incl. `lambda_measured`), constants |
| `unit/test_validity_gates.py` | triangle (VALID/EXT_O2_SUSPECT/INVALID), dilution floor, combined |
| `unit/test_rule_engine.py` | NORMAL, masking + cylinder inference, collision, DNA suppression, SAMPLE_INVALID, cam-timing, tie-break |
| `unit/test_rule_engine_reachability.py` | every one of the 34 signatures reachable by some input |
| `unit/test_resolution.py` | overlaps, GDI vs non-GDI, RPM-differential cam/lean/mechanical/catalyst separation |
| `unit/test_t_p8_7_hc_discriminator.py` | HC-direction discriminator for the timing/misfire family |
| `unit/test_classify_top3.py`, `unit/test_rank_candidates.py` | GASLabSimple ranking path (out-of-scope module) |
| `unit/test_family_map.py` | 34-signature → family map exhaustive + family vocabulary |
| `unit/test_process.py` | end-to-end payload round-trip (idle and idle+high-idle) |
| `unit/test_dna_view.py` | 13 required/optional fields, frozen, validation errors |
| `unit/test_ontology.py` | YAML parses, 34 faults, citations, validity gates match wiki, 6 DNA gates |
| `unit/test_validators.py` | collision audit, masking override, boundary grid, wiki-drift guard, DNA gates, 34-value coverage, catch-all flag |
| `generative/*` | boundary, combinatorial, fuzz, noise, and overlap property suites over the synthetic grid |
