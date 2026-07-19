---
node_type: wiki
lab: gaslab
module: semantic-vocabulary
subsystem: gas-enums-thresholds
implements:
  - "labs/gaslab/gaslab/contracts.py"
  - "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"
consumers:
  - "gaslab: labs/gaslab/gaslab/contracts.py ChemicalSignature/GasLabPayload"
  - "gaslab: labs/gaslab/gaslab/audits.py parse_vocabulary_thresholds"
  - "comlab: labs/comlab/comlab/schemas/vocabulary.py enum mirror"
drift_guards:
  - "labs/gaslab/tests/unit/test_contracts.py"
  - "labs/gaslab/tests/unit/test_ontology.py"
  - "labs/gaslab/tests/unit/test_validators.py"
tags: [vocabulary, gas, semantic, finished]
source: "labs/gaslab/docs/GAS_VOCABULARY.md"
---

# GAS Vocabulary Wiki

**Purpose:** the authoritative vocabulary GASLab uses internally and exposes to COMLab. Every enum, canonical gas name, numeric threshold, and DNA-derived bound in the GASLab codebase derives from this file.

**Status:** v2.2 (2026-06-10). Companion to the GAS wiki v2 — the **chunked set** (`wiki/00_index.md` … `11_sources_appendices.md`); the single-file `GAS_WIKI.md` mirror was retired to ARCHIVE on 2026-06-10. Wiki is the reasoning grammar; this is the contract layer. Supersedes v1.1 (2026-05-23). See §21 change log.

**Scope:** petrol vehicles 1990 – 2010 (Euro 1 – Euro 5), manually-entered analyser data — no live OBD streaming. 5-gas analysers only. (Scope narrowed from 1990–2020 on 2026-06-03; post-2010 "modern"/Euro 6-7 chemistry is out of scope.)

**Anchored to:**

- `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` — boundary protocol; reserves the names `VinDNA` / `SymptomDNA` / `VehicleDNA` / `GasLabPayload`.
- `COMLab/docs/wiki/OBD_VOCABULARY.md` §17 — the canonical `ChemicalSignature` enum (still 32-value upstream; the GASLab side is now 34-value after the v2.1 timing-taxonomy revision — see §3, mirror update pending).
- GAS wiki chunks (`wiki/00_index.md` … `11_…md`) — section-cited throughout (e.g. `GASWIKI-02 §2.3`). The retired single-file `GAS_WIKI.md` is no longer a citation target.

---

## 1. Standards anchored

This vocabulary aligns GASLab with the chemistry and emissions standards used in the rest of 4DLab.

| Standard | Scope | Used here for |
|---|---|---|
| **Brettschneider/Spindt equation** | Lambda from chemistry | §6 — `lambda_chem` definition |
| **SAE J1979 / J1979DA** | OBD-II PID definitions | Cross-reference to OBD vocab when comparing chem-λ vs ECU-λ |
| **SAE J2012** | DTC code structure | Cross-reference for fault signature → DTC mapping (DTCLab owns) |
| **EU Type Approval / Euro 1–7** | Emissions class limits | §4.7 in wiki — threshold scaling by `euro_emission_category` |
| **UK MOT (catalyst-equipped petrol)** | Pass-fail concentration limits | §13.1.3 in wiki |
| **BAR Two-Speed Idle (SAE J1667)** | 2500-RPM test point | RPM bucket alignment with `OBD_VOCABULARY.md` §3 |

---

## 2. Canonical gas identifiers

The names GASLab uses across code, schemas, and the rule engine. These are the contract surface — drift breaks everything.

| 4DLab canonical name | Description | Unit | Range (analyser envelope) | Source |
|---|---|---|---|---|
| `gas_hc` | Hydrocarbons (unburned fuel) | ppm | 0 – 20 000 | NDIR ~3.4 µm |
| `gas_co` | Carbon monoxide (partial oxidation) | vol % | 0 – 15 | NDIR ~4.7 µm |
| `gas_co2` | Carbon dioxide (complete combustion) | vol % | 0 – 22 | NDIR ~4.3 µm |
| `gas_o2` | Oxygen (free, un-reacted) | vol % | 0 – 22 | Electrochemical / paramagnetic |
| `gas_nox` | Oxides of nitrogen (thermal NO) | ppm | 0 – 5 000 | Electrochemical (5-gas only) |
| `lambda_chem` | Brettschneider lambda from chemistry | dimensionless | 0.5 – 2.5 | derived; see §6 |
| `volumetric_sum` | CO + CO₂ + O₂ | vol % | 0 – 22 | derived; triangle gate input |
| `afr_chem` | `lambda_chem × 14.71` | dimensionless | 7.4 – 36.8 | derived; petrol stoich |

**Naming convention:** the `gas_` prefix on raw analyser inputs distinguishes them from derived metrics. `lambda_chem` carries the `_chem` suffix because the ECU's perception lambda (`normalized_obd_lambda`) is owned by OBDLab — same concept, different source, never to be confused.

### 2.1 The internal `GasReading` dataclass

```python
@dataclass(frozen=True)
class GasReading:
    """Five raw analyser inputs. All fields required (no 4-gas fallback)."""
    hc:  int      # ppm   (gas_hc)
    co:  float    # vol % (gas_co)
    co2: float    # vol % (gas_co2)
    o2:  float    # vol % (gas_o2)
    nox: int      # ppm   (gas_nox)
```

Internal field names use the short form (`hc`, `co`, `co2`, `o2`, `nox`) for ergonomics. The canonical `gas_*` names are used on the wire (`GasLabPayload`) and in YAML rules.

---

## 3. `ChemicalSignature` — the 34-value contract enum

Single source of truth: `OBD_VOCABULARY.md` §17. Repeated here so GASLab can declare it without importing COMLab (per `SEMANTIC_CONTRACT.md` §1 — no cross-lab imports except DNALab).

> **v2.1 timing-taxonomy revision (2026-06-03):** `WRONG_VALVE_TIMING` is retired and replaced by three system-specific cam-timing values — `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED` — bringing the surface to 34. The GASLab side is revised first; the canonical `OBD_VOCABULARY.md §17` mirror, `SEMANTIC_CONTRACT.md`, and the COMLab schema must be updated in a coordinated cross-lab change (see §21 and the wiki follow-ups). Until that lands, this enum and the §17 mirror are intentionally divergent.

```python
from enum import StrEnum

class ChemicalSignature(StrEnum):
    """The single canonical fault label emitted by GASLab.

    The value populated into GasLabPayload.chemical_state.
    Mirror of OBD_VOCABULARY.md §17.
    """
    NORMAL_OPERATION                   = "NORMAL_OPERATION"
    RICH_MIXTURE                       = "RICH_MIXTURE"
    LEAN_MIXTURE                       = "LEAN_MIXTURE"
    IGNITION_MISFIRE                   = "IGNITION_MISFIRE"
    LEAN_MISFIRE                       = "LEAN_MISFIRE"
    RICH_MISFIRE                       = "RICH_MISFIRE"
    EXHAUST_AIR_LEAK                   = "EXHAUST_AIR_LEAK"
    HIGH_COMBUSTION_TEMP               = "HIGH_COMBUSTION_TEMP"
    CATALYST_NOT_LIGHTING_OFF          = "CATALYST_NOT_LIGHTING_OFF"
    CATALYST_OVERWHELMED               = "CATALYST_OVERWHELMED"
    SAMPLE_INVALID                     = "SAMPLE_INVALID"
    TIMING_OVER_ADVANCED               = "TIMING_OVER_ADVANCED"
    TIMING_RETARDED                    = "TIMING_RETARDED"
    O2_SENSOR_BIASED_LOW               = "O2_SENSOR_BIASED_LOW"
    O2_SENSOR_BIASED_HIGH              = "O2_SENSOR_BIASED_HIGH"
    WORN_ENGINE                        = "WORN_ENGINE"
    FLAT_CAMSHAFT                      = "FLAT_CAMSHAFT"
    GDI_INTAKE_VALVE_CARBON            = "GDI_INTAKE_VALVE_CARBON"
    VACUUM_REGULATOR_DIAPHRAGM_RUPTURE = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"
    GDI_HPFP_INTERNAL_SEAL_LEAK        = "GDI_HPFP_INTERNAL_SEAL_LEAK"
    WORN_VALVE_SEALS                   = "WORN_VALVE_SEALS"
    WORN_PISTON_RINGS                  = "WORN_PISTON_RINGS"
    POA_SIGNATURE                      = "POA_SIGNATURE"
    CAM_TIMING_RETARDED_MAP            = "CAM_TIMING_RETARDED_MAP"
    CAM_TIMING_RETARDED_MAF            = "CAM_TIMING_RETARDED_MAF"
    CAM_TIMING_ADVANCED                = "CAM_TIMING_ADVANCED"
    EGR_STUCK_CLOSED                   = "EGR_STUCK_CLOSED"
    EGR_STUCK_OPEN                     = "EGR_STUCK_OPEN"
    VVT_FAILURE                        = "VVT_FAILURE"
    EVAP_CANISTER_SATURATED            = "EVAP_CANISTER_SATURATED"
    EGR_DILUTION_MISFIRE               = "EGR_DILUTION_MISFIRE"
    INCOMPLETE_OXIDATION               = "INCOMPLETE_OXIDATION"
    INCOMPLETE_COMBUSTION              = "INCOMPLETE_COMBUSTION"
    COOLANT_LEAK_INTERNAL              = "COOLANT_LEAK_INTERNAL"
```

### 3.1 Per-value DNA gate summary

| Value | DNA gate (must be true to emit) | Source — wiki §7 |
|---|---|---|
| `NORMAL_OPERATION` | none | 7.1 |
| `RICH_MIXTURE` | none | 7.2 |
| `LEAN_MIXTURE` | none | 7.3 |
| `IGNITION_MISFIRE` | none (cylinder math needs `cylinder_count`) | 7.4 |
| `LEAN_MISFIRE` | none | 7.5 |
| `RICH_MISFIRE` | none | 7.6 |
| `EXHAUST_AIR_LEAK` | none | 7.7 |
| `HIGH_COMBUSTION_TEMP` | none | 7.8 |
| `CATALYST_NOT_LIGHTING_OFF` | `emissions.has_catalyst = true` | 7.9 |
| `CATALYST_OVERWHELMED` | `emissions.has_catalyst = true` | 7.10 |
| `SAMPLE_INVALID` | none (chemistry-pure) | 7.11 |
| `TIMING_OVER_ADVANCED` | none | 7.12 |
| `TIMING_RETARDED` | none | 7.13 |
| `O2_SENSOR_BIASED_LOW` | none | 7.14 |
| `O2_SENSOR_BIASED_HIGH` | none | 7.15 |
| `WORN_ENGINE` | none | 7.16 |
| `FLAT_CAMSHAFT` | none | 7.17 |
| `GDI_INTAKE_VALVE_CARBON` | `fuel_delivery_type = GDI` | 7.18 |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` | none (FPR is universal) | 7.19 |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | `fuel_delivery_type = GDI` | 7.20 |
| `WORN_VALVE_SEALS` | none (any engine) | 7.21 |
| `WORN_PISTON_RINGS` | none (any engine) | 7.22 |
| `POA_SIGNATURE` | none | 7.23 |
| `CAM_TIMING_RETARDED_MAP` | none (gas-direction discriminator; load-calc system is not a DNA field) | 6B (7.24) |
| `CAM_TIMING_RETARDED_MAF` | none (gas-direction discriminator; load-calc system is not a DNA field) | 6B (7.24) |
| `CAM_TIMING_ADVANCED` | none | 6B (7.24) |
| `EGR_STUCK_CLOSED` | `emissions.egr_equipped = true` | 7.25 |
| `EGR_STUCK_OPEN` | `emissions.egr_equipped = true` | 7.26 |
| `VVT_FAILURE` | none | 7.27 |
| `EVAP_CANISTER_SATURATED` | none | 7.28 |
| `EGR_DILUTION_MISFIRE` | `requires_dtc: true` (ontology-level gate; not a dna_gate — resolution.py does not consume `requires_dtc` in v1) | 7.29 |
| `INCOMPLETE_OXIDATION` | none | 7.30 |
| `INCOMPLETE_COMBUSTION` | none | 7.31 |
| `COOLANT_LEAK_INTERNAL` | none | 7.32 |

When DNA confidence is `PARTIAL` or `NONE`, the gated values fall out of the candidate set unless DNA still confirms the equipment. See wiki §10 for the full scope-shrinkage table.

---

## 4. `LambdaBand` enum

Discretised λ regions consumed by downstream reasoning. Source: wiki §5.6, §4.4.

```python
class LambdaBand(StrEnum):
    HEAVILY_RICH             = "HEAVILY_RICH"             # λ < 0.92
    BORDERLINE_RICH          = "BORDERLINE_RICH"          # 0.92 – 0.97
    STOICHIOMETRIC           = "STOICHIOMETRIC"           # 0.97 – 1.03
    CATALYST_LIGHT_OFF       = "CATALYST_LIGHT_OFF"       # 0.98 – 1.02 (sub-band)
    CATALYST_PEAK_EFFICIENCY = "CATALYST_PEAK_EFFICIENCY" # 0.995 – 1.005 (sub-band)
    BORDERLINE_LEAN          = "BORDERLINE_LEAN"          # 1.03 – 1.07
    HEAVILY_LEAN             = "HEAVILY_LEAN"             # > 1.07
```

**Note on overlap:** `CATALYST_LIGHT_OFF` and `CATALYST_PEAK_EFFICIENCY` are sub-bands of `STOICHIOMETRIC`. The discretiser returns the **narrowest matching band** — peak takes priority over light-off, light-off over stoich.

### 4.1 Discretiser thresholds

| Band | Lower (≥) | Upper (<) |
|---|---|---|
| `HEAVILY_RICH` | -∞ | 0.92 |
| `BORDERLINE_RICH` | 0.92 | 0.97 |
| `STOICHIOMETRIC` | 0.97 | 1.03 |
| `CATALYST_LIGHT_OFF` | 0.98 | 1.02 |
| `CATALYST_PEAK_EFFICIENCY` | 0.995 | 1.005 |
| `BORDERLINE_LEAN` | 1.03 | 1.07 |
| `HEAVILY_LEAN` | 1.07 | +∞ |

---

## 5. `SampleValidity` enum

Triangle-gate verdict. Source: wiki §6.

```python
class SampleValidity(StrEnum):
    VALID                = "VALID"                # CO+CO2+O2 in [14, 16]
    BORDERLINE           = "BORDERLINE"           # in [14, 15] or [15.5, 16]
    INVALID              = "INVALID"              # < 14 or > 18 — halts evaluation
    EXTERNAL_O2_SUSPECT  = "EXTERNAL_O2_SUSPECT"  # in (16, 18] — warn but continue
```

The `BORDERLINE` value is reserved for future use when stricter validity is needed; v1 collapses borderline into `VALID` for evaluation purposes but the enum value is declared so the contract is stable.

---

## 6. Lambda from chemistry — formal definition

```
       [CO₂] + [CO]/2 + [O₂] + (Hcv/4 · [CO₂]/([CO₂]+[CO])) · [CO₂]
λ  =  ─────────────────────────────────────────────────────────────
                       [CO₂] + [CO] + [HC]
```

Constants:

| Symbol | Value | Notes |
|---|---|---|
| `Hcv` | 1.85 | Hydrogen-to-carbon atomic ratio for pump petrol |
| `AFR_stoich` | 14.71 | Stoichiometric petrol AFR (kg air / kg fuel) |

NOₓ adds a small O₂-equivalence term (~0.05 % per 1 000 ppm); on a 5-gas analyser it is included directly via the standard Brettschneider modification:

```
λ_5gas = λ_4gas  +  (NOₓ_ppm / 1e6) × 0.5 / volumetric_sum_fraction
```

Implementation lives in `gaslab/brettschneider.py` (when the new code lands). The function is pure: same five inputs → same output, no side effects.

### 6.1 Edge cases

| Condition | Behaviour |
|---|---|
| All gases ≈ 0 | λ undefined; caller must check triangle first |
| HC very high, CO₂ low | λ stays balanced (misfire-immune property) |
| O₂ near 20.9 %, others ≈ 0 | λ → ∞; triangle gate catches this earlier |
| 4-gas reading (NOₓ missing) | **Reject** — operating envelope requires 5-gas |

### 6.2 Reliability and uncertainty band (v2)

`λ_chem` is an exhaust-gas **mass balance** — a property of the *sample*, not a direct measure of in-cylinder combustion. Reliability is governed by sample-stream integrity, not the formula. Source: wiki §2.4 (GASWIKI-02); research q1, q2.

| Reliability driver | Band / value | Notes |
|---|---|---|
| Headline equation accuracy (clean inputs) | ~ ± 1 % | de-facto industry standard |
| Calibrated analyser repeatability | ± 0.05 – 0.10 absolute λ | a drifted O₂ cell breaks the calc |
| Exhaust/sampling air leak swing | 0.05 – 0.15 (5–15 % false-lean) | the "ground-truth killer"; resolve via STFT + probe-occlusion |
| Misfire | λ stays ≈ 1.0 (misfire-immune) | read HC/O₂, not λ |

`modified_brettschneider` (HC carbon factor 12 vs 6) is **noted but not adopted** — current `hc_equiv = hc * 0.0025` NDIR scaling is the v2 production method.

---

## 7. `EngineStateBucket` enum — alignment with OBD vocabulary

GASLab consumes a bucket label from the UI, identical to OBDLab's RPM bucket vocabulary (`OBD_VOCABULARY.md` §3.3). Repeated here so GASLab is independently complete:

```python
class EngineStateBucket(StrEnum):
    STABILIZED_IDLE          = "STABILIZED_IDLE"
    REGULATORY_HIGH_IDLE     = "REGULATORY_HIGH_IDLE"
    STRESS_IDLE              = "STRESS_IDLE"
    COLD_OPEN_LOOP_INVALID   = "COLD_OPEN_LOOP_INVALID"
```

| Bucket | RPM band | Load | GASLab use |
|---|---|---|---|
| `STABILIZED_IDLE` | 650 – 900 | < 30 % | Default; all of §7 atlas is calibrated here |
| `REGULATORY_HIGH_IDLE` | 2200 – 2800 | 15 – 40 % | UK MOT 2500-RPM point; CO + HC tighter limits |
| `STRESS_IDLE` | 3500 – 4500 (VIN) | 40 – 60 % | Clinical diagnostic; required for RPM-differential signatures (§7.18, §7.21, §7.22) |
| `COLD_OPEN_LOOP_INVALID` | any | any | **Rejected** — outside GASLab operating envelope (warm engines only) |

A `COLD_OPEN_LOOP_INVALID` input causes GASLab to emit `chemical_state = SAMPLE_INVALID` with reason "engine not warm enough for valid sample".

---

## 8. `Gas_Behavior` — directional pattern language

Used by the rule engine to express directional facts (not numeric thresholds). Source: `gas_lab_dataset.yaml` §enums.

```python
class GasBehavior(StrEnum):
    POSITIVE_SPIKE       = "POSITIVE_SPIKE"        # fast massive rise
    POSITIVE_SHIFT       = "POSITIVE_SHIFT"        # slow elevated reading
    NORMAL               = "NORMAL"
    SUPPRESSED           = "SUPPRESSED"            # forced flat-line low
    INVERSE_CORRELATION  = "INVERSE_CORRELATION"   # seesaw pattern
    COLLISION            = "COLLISION"             # physically-impossible co-elevation
```

Used in YAML rule bodies (e.g., `gas_co.behavior: COLLISION` implies "high concurrent with another high"); the engine matches against bucket thresholds defined in §10.

---

## 9. `CatalystStatus` — inferred cat state

GASLab can emit a derived view of catalyst health alongside `chemical_state`. Source: wiki §9.

```python
class CatalystStatus(StrEnum):
    LIT_AND_WORKING   = "LIT_AND_WORKING"
    NOT_LIT           = "NOT_LIT"
    OVERWHELMED       = "OVERWHELMED"
    NOT_EVALUABLE     = "NOT_EVALUABLE"   # when has_catalyst is false or unknown
```

Today this field is **internal** — it is not part of `GasLabPayload` v1. It may be added in a future contract revision.

`LIT_AND_WORKING` describes the **catalyst**, not the engine. A healthy cat can mask a rich or lean engine upstream of it; see GASWIKI-07 §7.8 `CONCEPT_HEALTHY_CAT_MASKING`. Do not add a new `CatalystStatus` member for masking — the masking cat is still lit and working.

---

## 10. Per-gas numeric thresholds — the rule-engine baseline

Threshold tables consumed by the rule engine. The baseline values below apply to **Euro 4 petrol, 4-cyl, naturally aspirated, working three-way cat, warm at `STABILIZED_IDLE`**. Wiki §4.7 documents the scaling rules; DNA fields override per vehicle when `confidence = HIGH`.

### 10.1 `gas_hc` (ppm)

```yaml
thresholds:
  normal_with_cat:        { max: 35 }
  normal_borderline:      { min: 35,  max: 100 }
  normal_without_cat:     { max: 250 }
  minor_inefficiency:     { min: 50,  max: 250 }
  real_combustion_fault:  { min: 250, max: 800 }
  lean_misfire_range:     { min: 200, max: 600 }
  severe_misfire:         { min: 800, max: 2000 }
  ignition_misfire_floor: { min: 1000 }
  mechanical_or_dead_cat: { min: 2000 }
```

### 10.2 `gas_co` (vol %)

```yaml
thresholds:
  normal_with_cat:        { min: 0.1, max: 0.45 }
  cat_not_lit_band:       { min: 0.5, max: 0.9 }
  mild_rich:              { min: 0.5, max: 1.5 }
  clear_rich:             { min: 1.5, max: 3.0 }
  very_rich:              { min: 3.0 }
```

The threshold used by the collision rule (§8.5 in wiki) is `tier_max` — the upper bound of the *currently active* DNA-scaled tier. For Euro 4 + cat that is `0.45`; for Euro 1 no-cat it is `1.5`.

### 10.3 `gas_co2` (vol %)

```yaml
thresholds:
  peak_efficiency:        { min: 14.5, max: 16.0 }
  cat_not_lit_band:       { min: 13.5, max: 14.5 }
  no_cat_minimum:         { min: 13.0 }
  combustion_deficit:     { min: 11.0, max: 13.0 }
  severe_failure:         { max: 11.0 }
  total_quench:           { max: 5.0 }
```

### 10.4 `gas_o2` (vol %)

```yaml
thresholds:
  normal_post_cat:        { max: 0.35 }
  normal_pre_cat:         { min: 0.5, max: 1.5 }
  cat_not_lit_band:       { min: 0.3, max: 0.7 }
  mild_lean:              { min: 1.5, max: 4.0 }
  severe_lean_or_misfire: { min: 4.0 }
```

### 10.5 `gas_nox` (ppm)

```yaml
thresholds:
  normal_idle:            { max: 100 }
  elevated_idle:          { min: 100,  max: 500 }
  high_idle:              { min: 500,  max: 1500 }
  high_load_normal:       { min: 500,  max: 1500 }
  high_combustion_temp:   { min: 1500 }
  misfire_suppression:    { max: 50 }
```

### 10.6 `volumetric_sum` (vol %)

```yaml
thresholds:
  sample_invalid_low:     { max: 14.0 }
  borderline_low:         { min: 14.0, max: 15.0 }
  normal:                 { min: 15.0, max: 16.0 }
  external_o2_suspect:    { min: 16.0, max: 18.0 }
  sample_invalid_high:    { min: 18.0 }
```

### 10.7 `lambda_chem` (dimensionless)

```yaml
thresholds:
  heavily_rich:                { max: 0.92 }
  borderline_rich:             { min: 0.92,  max: 0.97 }
  stoichiometric:              { min: 0.97,  max: 1.03 }
  catalyst_light_off:          { min: 0.98,  max: 1.02 }
  catalyst_peak_efficiency:    { min: 0.995, max: 1.005 }
  borderline_lean:             { min: 1.03,  max: 1.07 }
  heavily_lean:                { min: 1.07 }
```

### 10.8 `fuel_trim` (%) — RPM-differential discriminator only

Fuel trim is a **perception/DNA-context** signal, not a 5-gas analyser channel.
These bands exist solely to give the §7.23.1 RPM-differential discriminator a
vocabulary home for its trim column; they are read at the **2500 RPM / high-idle**
state, not the §10 `STABILIZED_IDLE` baseline. Values inherited from the wiki
RPM matrices — no new numbers.

```yaml
thresholds:
  stable_band:        { min: -8.0, max: 8.0 }   # wiki §7.21 (worn valve seals) + §7.16 (generalised wear): trims stay within normal closed-loop band
  negative_load_cut:  { max: -12.0 }            # wiki §7.22 (worn piston rings): ECU cuts fuel hard under load as oil-as-fuel enters via PCV
```

> HC change-direction bands for the same discriminator reuse §10.1: a sharp drop
> to `normal_with_cat` (≤ 35 ppm) at 2500 RPM ⇒ worn valve seals; a rise into
> `real_combustion_fault` (> 250 ppm) that persists ⇒ worn piston rings. No new
> HC band is introduced.

### 10.9 `chemical_efficiency` and `oxygen_usage` (derived combustion-integrity metrics)

`chemical_efficiency` is a **derived** dimensionless metric, computed from existing analyser channels (`gas_co2` + `gas_co`). It is not a new analyser channel and is not part of `GasLabPayload` v1. Source: GASWIKI-02 §2.10; `EP-GAS-03`; formula-wiki F-GAS-04.

```yaml
chemical_efficiency:
  formula: "gas_co2 / (gas_co2 + gas_co)"
  inputs: [gas_co2, gas_co]
  unit: dimensionless
  thresholds:
    healthy:             { min: 0.95 }
    combustion_deficit:  { max: 0.95 }
```

`oxygen_usage` is the qualitative O₂-vs-CO discriminator behind the misfire-vs-rich split. It reuses the §10.2 CO and §10.4 O₂ bands; no new numeric threshold is introduced. Source: GASWIKI-02 §2.10; formula-wiki F-GAS-05.

```yaml
oxygen_usage:
  inputs: [gas_o2, gas_co, gas_hc]
  unit: qualitative
  rules:
    misfire: "high O2 + high HC/CO"
    pure_rich: "high CO + near-zero O2"
  thresholds: "reuse gas_co §10.2 and gas_o2 §10.4; no new numeric ratio"
```

---

## 11. DNA-derived per-vehicle bound overrides

When `GasLabDnaView.confidence = HIGH` and the OEM lookup populated CoC empirical targets, the per-vehicle bounds override the defaults in §10. Source: wiki §4.7 + §10.

| DNA field | Replaces in defaults | Notes |
|---|---|---|
| `target_lambda_v112` | `peak_efficiency` λ centre | Center the ± 0.005 window on this value |
| `co_low_idle` | `normal_with_cat.max` (CO) | Per-vehicle CoC limit |
| `co_high_idle` | `mild_rich.max` at 2500 RPM | Per-vehicle 2-speed-idle limit |
| `co_type_approval` | `clear_rich.min` | Type-approval ceiling |
| `hc_type_approval` | `real_combustion_fault.min` | Type-approval HC ceiling |
| `nox_type_approval` | `high_combustion_temp.min` | Type-approval NOₓ ceiling |
| `engine_displacement_liters` | mass-emission conversion | Reserved — not used (concentrations only) |
| `fuel_type` *(v2, context-only)* | nothing — does **not** move any bound | E5/E10/winter-blend annotation; lower idle HC/CO with ethanol. May *widen* `NORMAL_OPERATION` bounds slightly but **must not** relax the triangle gate. Source: wiki §2.9; research q9 |
| `altitude_band` *(v2, context-only)* | nothing | λ math is altitude-invariant (mass balance). Annotates the diagnosis only. Source: wiki §2.9; research q9 |

When the DNA field is `None`, the default from §10 is used. The rule engine logs which value (per-vehicle vs default) was applied so the diagnosis is traceable.

**v2 gate-integrity rule:** neither `fuel_type` nor `altitude_band` may relax `volumetric_sum.sample_invalid_low` (14.0) or any validity gate. Ethanol/altitude shifts are absorbed by re-validation (OBD trims, probe-occlusion test), never by widening a sample-integrity boundary.

---

## 12. The `GasLabPayload` contract — what COMLab sees

Single source of truth: `SEMANTIC_CONTRACT.md` §4.4. Reproduced here so GASLab can validate its own output without importing COMLab:

```jsonc
{
  "chemical_state":  "RICH_MIXTURE",   // §3 ChemicalSignature
  "gas_co":          4.5,               // vol %
  "gas_hc":          650,               // ppm
  "gas_co2":         9.5,               // vol %   (added v1.1, 2026-05-19)
  "gas_o2":          0.1,               // vol %
  "gas_nox":         15,                // ppm     (added v1.1, 2026-05-19)
  "lambda_chem":     0.82,              // dimensionless
  "sample_validity": "VALID",           // §5 SampleValidity
  "lambda_measured": null,              // optional directly-measured analyser λ (added 2026-06; T-FX-7)
  "high_idle_hc":     170,               // ppm, optional (added for high-idle delta, MW-008/009)
  "high_idle_co":     0.1,               // vol %, optional
  "high_idle_co2":    15.0,              // vol %, optional
  "high_idle_o2":     0.2,               // vol %, optional
  "high_idle_nox":    45,                // ppm, optional
  "high_idle_lambda": 0.99               // dimensionless, optional
}
```

### 12.1 Pydantic schema (proposed for `gaslab/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional

class GasLabPayload(BaseModel):
    """Output fragment GASLab hands to COMLab."""
    chemical_state:  ChemicalSignature
    gas_co:          float = Field(..., ge=0.0, le=15.0)
    gas_hc:          int   = Field(..., ge=0,  le=20_000)
    gas_co2:         float = Field(..., ge=0.0, le=22.0)
    gas_o2:          float = Field(..., ge=0.0, le=22.0)
    gas_nox:         int   = Field(..., ge=0,  le=5_000)
    lambda_chem:     float = Field(..., ge=0.5, le=2.5)
    sample_validity: SampleValidity
    lambda_measured: float | None = Field(default=None, ge=0.5, le=2.0)  # optional directly-measured analyser λ
    high_idle_hc:     Optional[int]   = Field(default=None, ge=0, le=20_000)
    high_idle_co:     Optional[float] = Field(default=None, ge=0.0, le=15.0)
    high_idle_co2:    Optional[float] = Field(default=None, ge=0.0, le=22.0)
    high_idle_o2:     Optional[float] = Field(default=None, ge=0.0, le=22.0)
    high_idle_nox:    Optional[int]   = Field(default=None, ge=0, le=5_000)
    high_idle_lambda: Optional[float] = Field(default=None, ge=0.5, le=2.5)
```

> **`lambda_measured` (added 2026-06).** Optional directly-measured analyser λ, passed through from `GasLabContext.lambda_measured`. **Named consumer:** COMLab perception-contradiction detector — the no-OBD fallback path (T-FX-7). When OBD is present COMLab uses `lambda_chem` vs `normalized_obd_lambda`; without OBD it falls back to `lambda_measured`. The field is now live in `gaslab/contracts.py`; the v1 model in this section has been brought in line.

Range bounds match the analyser measurement envelope from §2. The Pydantic validator at COMLab will reject payloads outside these bounds — which means GASLab must never emit one. (See §13 invariant 4.)

**Cross-lab follow-up required.** This widening is a contract change. `COMLab/comlab/schemas/ingestion.py::GasLabPayload` (the Pydantic model COMLab declares) and `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` §4.4 must be updated to add `gas_co2` and `gas_nox` with matching ranges before GASLab is wired to COMLab. Tracked here, not done here, because those files are owned by COMLab.

### 12.2 Fields **not** in the payload (intentional)

- `lambda_band` — derivable from `lambda_chem`; not transmitted.
- `inferred_misfiring_cylinder_count` — emitted as a warning string when `chemical_state = IGNITION_MISFIRE`, not as a structured field.
- `catalyst_light_off_status` — see §9 above; internal only in v1.

---

## 13. Invariants the GASLab code must enforce

1. **Five inputs always.** No 4-gas fallback path. Missing NOₓ → reject upstream.
2. **Triangle first.** No `chemical_state` other than `SAMPLE_INVALID` may be emitted unless `sample_validity` is `VALID`, `BORDERLINE`, or `EXTERNAL_O2_SUSPECT`.
3. **Single chemical state.** GASLab returns exactly one `chemical_state`; ambiguity is collapsed by rule priority (the rule engine has named overrides — see wiki §8.4–§8.6).
4. **Output never exceeds Pydantic bounds.** The values in `GasLabPayload` are pre-validated against §12.1 ranges before emission. If the rule engine would produce out-of-bound values, that is a code bug.
5. **DNA gates are honoured.** A `ChemicalSignature` value with a DNA gate in §3.1 cannot be emitted unless the gate evaluates to `true` against the current `GasLabDnaView`.
6. **No COMLab imports.** GASLab declares its own enums (this file is the spec). COMLab independently mirrors them in `comlab/schemas/vocabulary.py`. Two independent declarations of the same StrEnum are intentional — JSON values are the cross-lab contract, not Python classes.
7. **Confidence-shrunk scope is enforced before rules fire.** If DNA confidence is `PARTIAL`/`NONE`, the candidate-set restriction from wiki §10 is applied first; rules for gated values are skipped, not just suppressed at output.

---

## 14. Rule engine priority levels (informative)

Source: `gas_lab_dataset.yaml` v2.3 (edges section). Higher priority wins.

| Priority | Rule class | Examples |
|---|---|---|
| 95 | Validity gate | `rule_sample_invalid` (triangle outside [14, 18]) |
| 92 | External-O₂ warning | `rule_external_oxygen_warning` (16 < triangle ≤ 18) |
| 85 | Named override — misfire mask | `rule_ignition_misfire` |
| 82 | Named override — cam timing (lean/persistent: retarded-MAF, advanced) | `rule_wrong_valve_timing` (routes to `CAM_TIMING_*`; rule id retained pending cross-lab rename) |
| 80 | Collision rules | `rule_rich_misfire_collision`, `rule_collision_downstream_ingress` |
| 70 | Mixture rules | `rule_rich_mixture`, `rule_lean_mixture` |
| 60 | Sub-class rules | `rule_lean_misfire`, sensor bias |
| 50 | RPM-differential signatures | valve seals, piston rings, GDI carbon |
| 40 | Mechanical and other | cam-timing fallback (incl. retarded-MAP rich case), worn engine, flat cam |
| 30 | Catalyst classes | not-lighting-off, overwhelmed |
| 20 | Equipment-gated | EGR stuck closed/open, VVT, EVAP |
| 10 | Default | `NORMAL_OPERATION` |

The engine evaluates rules in descending priority order. Once `chemical_state` is set, lower-priority rules may still raise warnings but must not overwrite it.

---

## 15. Internal vs. emitted vocabulary — summary table

| Term | Used internally | In `GasLabPayload` | Source |
|---|---|---|---|
| `gas_hc`, `gas_co`, `gas_co2`, `gas_o2`, `gas_nox` | yes | yes (all five, as of v1.1) | §2 |
| `lambda_chem` | yes | yes | §6 |
| `volumetric_sum` | yes | no (derivable) | §2, §10.6 |
| `chemical_efficiency` | yes | no (derivable) | §10.9 |
| `oxygen_usage` | yes | no (derivable) | §10.9 |
| `ChemicalSignature` | yes | yes (`chemical_state`) | §3 |
| `LambdaBand` | yes | no | §4 |
| `SampleValidity` | yes | yes | §5 |
| `EngineStateBucket` | yes (input) | no | §7 |
| `GasBehavior` | yes (rule grammar) | no | §8 |
| `CatalystStatus` | yes | no in v1 | §9 |
| `inferred_misfiring_cylinder_count` | yes | as warning string | §6 wiki |

---

## 16. Cross-lab vocabulary alignment

Three terms are reserved by `SEMANTIC_CONTRACT.md` §2. GASLab uses these as opaque tokens — it does not coin its own variants.

| Concept | Reserved name | Where GASLab encounters it |
|---|---|---|
| Physical vehicle profile from VIN | `VinDNA` | as input projected into `GasLabDnaView` |
| User-reported symptom triage | `SymptomDNA` | not consumed by GASLab today |
| Combined Part A + Part B + session meta | `VehicleDNA` | not consumed directly; only the projected view |
| COMLab inbound payload | `OrchestratorInboundRequest` | not consumed by GASLab (one-way: GASLab → COMLab) |
| GASLab output fragment | `GasLabPayload` | the contract surface |

Avoid synonyms in code, docs, and tests.

---

## 17. Sources

Vocabulary terms in this document trace to these files:

| File | Contributes |
|---|---|
| `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` | All cross-lab boundary names; `GasLabPayload` schema |
| `COMLab/docs/wiki/OBD_VOCABULARY.md` §17 | `ChemicalSignature` enum (canonical; GASLab side now 34-value — §17 mirror update pending, see §3) |
| `COMLab/docs/wiki/OBD_VOCABULARY.md` §3 | `EngineStateBucket` alignment |
| `labs/gaslab/wiki/` (chunks `00`–`11`) | All numeric thresholds, behaviour bands, fault patterns (canonical chunked wiki; single-file `GAS_WIKI.md` retired 2026-06-10) |
| `GASLab/data/gas_lab_dataset.yaml` v2.3 | Existing executable spec — used as numeric reference |
| `GASLab/data/gas_lab_wiki.md` v1.2 | Prior wiki — synthesised into the new wiki |
| `GASLab/data/master_gas_guide.md` | Per-gas reasoning grammar |
| `GASLab/data/gasrules1.md` | Crypton tables; AFR / λ relationship |
| `GASLab/data/CommonFaults.md` | Era-specific fault context (informative — not vocabulary) |

---

## 18. Change protocol

Vocabulary changes follow the same protocol as `SEMANTIC_CONTRACT.md` §10:

1. **Backwards-compatible additions** (new enum values, new threshold tiers, new optional DNA fields) bump the wiki minor version (e.g. `v1.0` → `v1.1`).
2. **Breaking changes** (enum value renames, threshold semantics changes, contract field renames) bump the major version (e.g. `v1.x` → `v2.0`) and require coordinated COMLab schema update.
3. **All changes** must be reflected in both the GAS wiki **chunks** (`wiki/00`–`11`) and `GAS_VOCABULARY.md` in the same commit. Drift between them is a defect. (The single-file `GAS_WIKI.md` mirror was retired to ARCHIVE on 2026-06-10, so there is no longer a third copy to keep in sync.)

---

## 19. λ-divergence magnitude reference (v2)

Quantified expected divergence between chemistry λ (ground truth) and ECU-perceived λ, per fault. Feeds the truth-vs-perception detector (wiki §4.11–4.12, GASWIKI-04). Source: research q6. These are **informative priors**, not thresholds — the gate threshold stays Δλ > 0.08.

| Scenario | Δλ magnitude | Tailpipe reality |
|---|---|---|
| Ignition misfire (ECU chases O₂ spike) | up to ≈ 0.24 | actual λ 0.76–0.85 (rich) |
| O₂-sensor poisoning / signal bias | 0.15 – 0.23 | actual λ 0.77–0.85, CO 5–8 % |
| Upstream exhaust air leak | 0.05 – 0.10 | actual λ ≈ 0.95 vs reported 1.00 |
| Wideband calibration-resistor damage (late-era) | 0.12 – 0.18 | erratic over/under-report |


## 20. Oil-burn sub-modes & proposed enum additions (v2)

`[v2: q4]` Five field-documented oil-ingestion modes (wiki §6A.1, GASWIKI-06A). Per the v2 enum decision they emit existing values now; candidate new values are recorded for a future coordinated contract revision and are **not emittable today**.

| Field case | v2 emit (existing value) | Live registry rule ID | Candidate v2.x value | Gate if added |
|---|---|---|---|---|
| Worn piston rings | `WORN_PISTON_RINGS` | `MW-001` | — (exists) | none |
| Degraded valve-stem seals | `WORN_VALVE_SEALS` | `MW-002` | — (exists) | none |
| Stuck-open PCV | `POA_SIGNATURE` (clogged-PCV sub-mode) | `MW-008` | `PCV_STUCK_OPEN` | none |
| Head-gasket oil-to-cylinder breach | `COOLANT_LEAK_INTERNAL` (oil breach) | `MW-003` | `HEAD_GASKET_OIL_BREACH` | none |
| Worn turbo turbine seals | `POA_SIGNATURE` (turbo-seal sub-mode) | `MW-009` | `TURBO_SEAL_OIL_LEAK` | `induction_type = forced` |

New vocabulary terms introduced (annotation strings only, not enum members): `oilburn_submode`, `pcv_stuck_open_submode`, `turbo_seal_submode`, `head_gasket_oil_breach_submode`. They are surfaced in the warnings stream, not in `GasLabPayload.chemical_state`.

Verdicts for PCV and turbocharger seals are determined on the live path by the registry rules `MW-008` and `MW-009` via the integration shim, utilizing the resolved `high_idle_hc`, `high_idle_co`, and `high_idle_lambda` targets.

## 21. Change log

| Version | Date | Change |
|---|---|---|
| v1.0 | 2026-05-19 | Initial new-build vocabulary |
| v1.1 | 2026-05-23 | `gas_co2`/`gas_nox` added to payload; `fuel_trim` discriminator §10.8 |
| **v2.0** | **2026-06-03** | **Scope narrowed to 1990–2010 (Euro 1–5).** Added: Brettschneider reliability/uncertainty band (§6.2); `fuel_type`/`altitude_band` context-only DNA fields (§11) with gate-integrity rule; λ-divergence magnitude reference (§19); oil-burn sub-modes + proposed enum additions (§20). The 32-value `ChemicalSignature` contract is **unchanged** (frozen); new oil-burn cases map to existing values. |
| **v2.1** | **2026-06-03** | **Timing-taxonomy revision (source: `q1&7/Advanced Engineering Analysis of Petrol Engine Timings (1990–2010)`).** Retired `WRONG_VALVE_TIMING`; added system-specific cam-timing values `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED` (§3). Contract surface 32 → **34**. Consumer: COMLab `chemical_state` routing / fault-atlas (06B). This is a **breaking enum change** (§18.2) requiring a coordinated update of `OBD_VOCABULARY.md §17`, `SEMANTIC_CONTRACT.md`, the COMLab schema, and `resolution.py` rule bindings — those land in a later cross-lab session. |
| **v2.2** | **2026-06-10** | **Combustion-integrity derived metrics.** Added `chemical_efficiency = CO₂/(CO₂+CO)` and qualitative `oxygen_usage` O₂-vs-CO discriminator (§10.9), with internal-vs-emitted rows (§15). No `ChemicalSignature` value, payload field, enum, or 34-value contract surface changed. |
| (concept) | 2026-06-10 | **Healthy-catalyst masking limitation.** Added GASWIKI-07 §7.8 `CONCEPT_HEALTHY_CAT_MASKING` plus the §9 `CatalystStatus` caveat: `LIT_AND_WORKING` names the catalyst state, not an engine-health verdict. `Catalyst_Masking_Rich` remains a COMLab candidate named in prose, not a GASLab `ChemicalSignature` value. No enum member, threshold, payload field, or 34-value contract surface changed. |
| (doc) | 2026-06-10 | **Single-file `GAS_WIKI.md` mirror retired to ARCHIVE.** The chunked set (`wiki/00`–`11`) is now the sole canonical wiki form; references updated in §Status, §Anchored-to, §17 sources, and the §18.3 no-drift rule. No vocabulary member, threshold, or contract surface changed (no version bump). |

---

*End of vocabulary. Use this document as the import target for every Python enum and every numeric threshold in the GASLab codebase.*
