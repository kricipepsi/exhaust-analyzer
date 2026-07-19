---
node_type: "lld"
lab: "gaslab"
module: "gaslab"
subsystem: "low-level-design"
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
  - "dld: labs/gaslab/docs/DLD_GASLab.md"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py lambda/gas analytics"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py sample_validity/lambda aggregation"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py lambda_measured fallback"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
drift_guards:
  - "labs/gaslab/tests/unit/test_contracts.py"
  - "labs/gaslab/tests/unit/test_brettschneider.py"
  - "labs/gaslab/tests/unit/test_validity_gates.py"
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_ontology.py"
  - "labs/gaslab/tests/unit/test_validators.py"
  - "labs/gaslab/tests/unit/test_dna_view.py"
  - "labs/gaslab/tests/unit/test_process.py"
  - "labs/gaslab/tests/unit/test_family_map.py"
  - "labs/gaslab/tests/unit/test_rank_candidates.py"
tags: ["gaslab", "low-level-design", "lld"]
source: "labs/gaslab/docs/LLD_GASLab.md"
---

# LLD — GASLab
**Status:** Approved
**PRD Baseline:** PRD_GASLab v2.1
**HLD / DLD Reference:** HLD_GASLab v2.1 / DLD_GASLab v2.1
**Version:** 2.1
**Date:** 2026-06-10
**Change note:** Refreshed to the live engine — cam-timing rule (renamed from the retired WVT rule) and its high-idle confirmation vectors, `fuel_trim` leak routing, masking cylinder-count inference, Euro-class CO/HC scaling, wideband O₂-bias calibration, and the single-value `target_lambda_v112` CoC window.

Convention: every numeric literal in `gaslab/` carries a `# wiki:` or `# vocab:` comment citing `GAS_WIKI` / `GAS_VOCABULARY`. The literals below are transcribed from source.

---

## 1. Physical Constants

```python
# gaslab/contracts.py
Hcv: float        = 1.85    # vocab: GAS_VOCABULARY §6 — H:C atomic ratio, pump petrol
AFR_STOICH: float = 14.71   # vocab: GAS_VOCABULARY §6 — stoichiometric petrol AFR
HC_FACTOR: float  = 0.0025  # vocab: GAS_VOCABULARY §6 — ppm HC → effective vol% in carbon balance
```

All constants are frozen at module import. None are configurable at runtime. `Hcv` is currently reserved (accepted as a `lambda_chem` override for non-standard fuels, test-only); the HC weighting that matters is captured by `HC_FACTOR`.

---

## 2. Brettschneider Lambda — Exact Implementation

```python
def lambda_chem(reading: GasReading, hcv: float | None = None) -> float:
    hc_equiv   = reading.hc * HC_FACTOR            # vocab: GAS_VOCABULARY §6
    carbon_sum = reading.co2 + reading.co + hc_equiv
    if carbon_sum == 0:
        return 1.0                                 # safe sentinel; classify() flags SAMPLE_INVALID
    lambda_4gas = (reading.co2 + reading.co / 2.0 + reading.o2) / carbon_sum

    volumetric_sum = reading.co + reading.co2 + reading.o2
    if volumetric_sum > 0:
        vol_frac       = volumetric_sum / 100.0
        nox_correction = (reading.nox / 1_000_000.0) * 0.5 / vol_frac  # vocab: GAS_VOCABULARY §6
    else:
        nox_correction = 0.0
    return lambda_4gas + nox_correction
```

**Edge cases:**
- `carbon_sum == 0`: returns `1.0` safe sentinel. The dilution gate (`CO + CO₂ > 6.0`) runs before `classify()`, which independently flags `SAMPLE_INVALID`.
- `volumetric_sum == 0`: NOx correction is skipped (no divide-by-zero); 4-gas lambda returned.
- `nox == 0`: correction term evaluates to 0; 4-gas lambda returned.
- The carbon-balance denominator weights HC by `HC_FACTOR` to preserve **misfire-immunity** (`GAS_WIKI §4.3`): raw fuel + raw air from a dead cylinder stay stoichiometric, so λ ≈ 1.000 even with high HC and high O₂.

---

## 3. Exhaust Gas Triangle — Exact Boundary Values

```python
# validity_gates.py — wiki: GAS_WIKI §6.1
volumetric_sum = co + co2 + o2
volumetric_sum < 14.0   → INVALID
volumetric_sum > 18.0   → INVALID
volumetric_sum > 16.0   → EXTERNAL_O2_SUSPECT   # (16, 18]
otherwise               → VALID                 # [14, 16]

# dilution_gate — wiki: GAS_WIKI §6.2
co + co2 > 6.0          → True (not diluted)
```

**Boundary ownership (inclusive/exclusive):**

| Value | Result |
|-------|--------|
| `s < 14.0` | INVALID |
| `s == 14.0` | VALID (inclusive lower bound) |
| `s == 16.0` | VALID (inclusive upper bound) |
| `s == 16.0001` | EXTERNAL_O2_SUSPECT |
| `s == 18.0` | EXTERNAL_O2_SUSPECT (inclusive upper of suspect range) |
| `s == 18.0001` | INVALID |
| `s > 18.0` | INVALID |

`sample_validity` runs the triangle gate first; if it is INVALID it returns immediately, otherwise a failed dilution gate downgrades the verdict to INVALID. `SampleValidity.BORDERLINE` exists in the enum but is collapsed to VALID by the triangle gate in v1.

---

## 4. Definitive-Override Thresholds (`_definitive_match`, in firing order)

All thresholds come from `gas_lab_ontology.yaml §reasoning_grammar`; the wiki drift guard enforces they match `GAS_VOCABULARY.md` at every CI run. Evaluation is **strictly sequential** — the first rule to return wins.

```python
# 4.0 Low-triangle air ingress (fast path) — wiki: GAS_WIKI §7.7
#   CO+CO2+O2 < 14 AND HC ≤ leak.max AND leak.co.min ≤ CO ≤ leak.co.max AND O2 > leak.o2.min
#   → (EXHAUST_AIR_LEAK, EXTERNAL_O2_SUSPECT)

# 4.1 EXTERNAL_O2_SUSPECT leak + fuel_trim disambiguation (T-GV2-12) — wiki: GAS_WIKI §4.4
#   only when fuel_trim is provided AND 16 < CO+CO2+O2 ≤ 18 AND leak chemistry matches:
#       fuel_trim > 8.0  → (EXHAUST_AIR_LEAK, EXTERNAL_O2_SUSPECT)   # vocab: §10.8
#       else             → (SAMPLE_INVALID, INVALID)

# 4.2 Validity INVALID → (SAMPLE_INVALID, INVALID)

# 4.3 Coolant intrusion (priority 87) — wiki: GAS_WIKI §8.7
COOLANT_CO2_THRESHOLD = 12.0   # vol% — water-vapour dilution floor
COOLANT_HC_THRESHOLD  = 300.0  # ppm  — ethylene-glycol HC flash floor
#   co2 ≤ 12.0 AND hc ≥ 300 AND block_test_passed → COOLANT_LEAK_INTERNAL

# 4.4 Masking rule (priority 85) — wiki: GAS_WIKI §8.4
MASKING_HC_THRESHOLD  = 1000   # ppm
MASKING_O2_THRESHOLD  = 3.0    # vol%
MASKING_NOX_THRESHOLD = 50     # ppm
#   hc > 1000 AND o2 > 3.0 AND nox < 50 →
#     inferred_cyl = round(o2 / (21 / dna.cylinder_count))   # wiki: GAS_WIKI §3.4
#     if inferred_cyl ≥ 1 → IGNITION_MISFIRE
#   (the O2 spike must be consistent with ≥1 dropped cylinder)

# 4.5 Cam-timing rule (priority 82) — wiki: GAS_WIKI §8.6  (was wrong_valve_timing_rule)
CAM_HC_THRESHOLD = 1000  # ppm
CAM_O2_THRESHOLD = 2.0   # vol%
#   hc > 1000 AND o2 > 2.0 AND co > 0 →
#     2.0 ≤ o2 ≤ 4.5 AND 1.08 ≤ λ ≤ 1.18 → CAM_TIMING_RETARDED_MAF (lean branch)
#     1.2 ≤ o2 ≤ 2.5 AND 1.03 ≤ λ ≤ 1.08 → CAM_TIMING_ADVANCED
#   When reading_high is present, the idle verdict only fires if the 2500 RPM
#   vector also matches (see §6). When absent, the idle verdict fires directly.

# 4.6 RPM-differential routes — wiki: GAS_WIKI §7.23.1  (resolution._append_rpm_routes)

# 4.7 Collision rule (priority 80) — wiki: GAS_WIKI §8.5
COLLISION_CO_MAX        = 0.45  # vol% — "normal_with_cat" CO ceiling
COLLISION_O2_THRESHOLD  = 2.0   # vol%
COLLISION_SUM_THRESHOLD = 16.0  # triangle-sum split
COLLISION_HC_MAX        = 100   # ppm — EXHAUST_AIR_LEAK requires HC Normal
#   co > 0.45 AND o2 > 2.0 →
#     sum ≤ 16.0          → RICH_MISFIRE
#     sum > 16.0 AND hc ≤ 100 → EXHAUST_AIR_LEAK
#     sum > 16.0 AND hc > 100 → RICH_MISFIRE
#   (both leak verdicts carry SampleValidity.EXTERNAL_O2_SUSPECT)

# 4.8 Rich-timing branch (priority 40 fallback) — wiki: GAS_WIKI §4.10, §7.24
#   only when reading_high is present AND idle is rich
#     (400 ≤ hc ≤ 1200, 3.5 ≤ co ≤ 7.0, 0.75 ≤ λ ≤ 0.88, o2 ≤ 0.5)
#   AND the 2500 vector matches the Speed-Density partial-normalisation pattern
#       → CAM_TIMING_RETARDED_MAP
```

---

## 5. Specificity Score — Tie-Breaking

```python
_GAS_KEYS = ("hc", "co", "co2", "o2", "nox", "lambda")

def _specificity(name, faults) -> float:
    sig = faults[name]["signature"]
    return sum(sig[g]["max"] - sig[g]["min"] for g in _GAS_KEYS)

def _candidate_rank(name, faults) -> tuple[bool, float]:
    return (faults[name].get("signature_type") == "catch_all", _specificity(name, faults))
```

`min(candidates, key=_candidate_rank)` puts non-catch-all faults ahead of catch-alls, then prefers the narrowest signature. On an exact tie the winner is the first in ontology declaration order — deterministic across Python restarts.

---

## 6. RPM-Differential Family Separation (`resolution.apply_differentiators`)

Only active when `reading_high` is provided. `λᵢ = lambda_chem(reading)`, `λₕ = lambda_chem(reading_high)`.

**Lean normalisation gate (LEAN_MIXTURE):**
```
lean_normalises = reading_high.o2 < 1.0 AND 0.985 ≤ λₕ ≤ 1.015
if not lean_normalises: drop LEAN_MIXTURE
```

**Cam-timing persist/normalise gates** (each drops its own candidate if the 2500 vector fails):

| Candidate | Idle gate | 2500 RPM gate |
|-----------|-----------|---------------|
| `CAM_TIMING_RETARDED_MAF` | `2.0 ≤ o2 ≤ 4.5`, `1.08 ≤ λᵢ ≤ 1.18` | `1.0 ≤ o2 ≤ 2.5`, `1.03 ≤ λₕ ≤ 1.09`, `150 ≤ hc ≤ 400`, `0.10 ≤ co ≤ 0.30`, `150 ≤ nox ≤ 500` (lean **persists**) |
| `CAM_TIMING_ADVANCED` | `250 ≤ hc ≤ 600`, `1.03 ≤ λᵢ ≤ 1.08` | NOx rises & HC falls & CO falls idle→2500; `0.80 ≤ o2 ≤ 1.80`, `1.01 ≤ λₕ ≤ 1.05`, `100 ≤ hc ≤ 300`, `0.15 ≤ co ≤ 0.50`, `300 ≤ nox ≤ 900` |
| `CAM_TIMING_RETARDED_MAP` | `0.75 ≤ λᵢ ≤ 0.88`, `o2 ≤ 0.5` | λₕ > λᵢ (rises toward 1.0; flat rich rejected), CO falls, `o2 ≤ 0.5`, `0.85 ≤ λₕ ≤ 0.95`, `hc ≥ 200` (≤ Euro `hc_2500_ceiling`), `co_ceiling ≤ co ≤ 4.5`, `100 ≤ nox ≤ 400` |

**Lean-vs-cam-MAF mutual exclusion:** if both survive, `lean_normalises` drops `CAM_TIMING_RETARDED_MAF`; `cam_maf_persists` drops `LEAN_MIXTURE`.

**Low-HC misfire pruning:** once a `CAM_TIMING_*` survivor is confirmed and `reading.hc < 1000` (`HC_IGNITION_MISFIRE_FLOOR`), generic misfire-family survivors (`IGNITION_MISFIRE`, `LEAN_MISFIRE`, `RICH_MISFIRE`, `EGR_DILUTION_MISFIRE`, `INCOMPLETE_COMBUSTION`) are dropped as overlap noise; true high-HC misfire remains.

**Ignition over-advance promotion:** a clean idle (`120 ≤ hc ≤ 250`, `0.10 ≤ co ≤ 0.30`, `11.5 ≤ co2 ≤ 13.0`, `0.8 ≤ o2 ≤ 1.5`, `20 ≤ nox ≤ 60`, `1.01 ≤ λᵢ ≤ 1.04`) plus a 2500 NOx-only spike (`nox > 1200`, `1.0 ≤ λₕ ≤ 1.06`, `hc ≤ 100`, `co ≤ 0.45`) appends `TIMING_OVER_ADVANCED`.

**Mechanical-wear family → leaf** (resolves `POA_SIGNATURE` / `WORN_*` co-survivors by idle→2500 HC direction, load-state CO, λₕ, and optional `fuel_trim`):

| Leaf | Key gates |
|------|-----------|
| `WORN_VALVE_SEALS` | `300 ≤ hcᵢ ≤ 500`, `hcₕ ≤ 35` (HC drops sharply), `coₕ ≤ 0.15`, `0.96 ≤ λₕ ≤ 1.0`, fuel_trim in ±8 if present |
| `WORN_PISTON_RINGS` | `100 ≤ hcᵢ ≤ 150`, `hcₕ > 300` (HC rises under load), `coₕ > 0.5`, `λₕ < 0.99`, fuel_trim ≤ −12 if present |
| `WORN_ENGINE` | `150 ≤ hcᵢ ≤ 300`, `150 ≤ hcₕ ≤ 300`, `coₕ ≥ coᵢ`, `1.0 ≤ λₕ ≤ 1.03` |
| `POA_SIGNATURE` | forced induction + `hcᵢ > 500` with clean CO and λ≈1 at both speeds, **or** `hc > 500` at both speeds with `λₕ` outside `[0.95, 1.05]` |

If no leaf matches, the whole mechanical-wear family is dropped.

**Catalyst dual-idle weak-vs-dead** (only when `dna.has_catalyst` and `reading_high` present): requires healthy fuel control (`0.98 ≤ λ ≤ 1.02` at both speeds) or both catalyst states are rejected. A weak-at-idle / working-at-2500 delta keeps `CATALYST_NOT_LIGHTING_OFF`; dead-at-both routes to `CATALYST_OVERWHELMED`.

Finally `_append_rpm_routes` appends ontology-declared `rpm_differential` route targets whose `route_appears_in_states` matches `engine_state`.

---

## 7. DNA Gate — Exact Branch Logic

`apply_differentiators` applies each `dna_gate` **strictly and unconditionally**; the dotted YAML field path resolves to the last segment as a flat attribute on `GasLabDnaView`.

```python
dna_gate = entry.get("dna_gate")
if dna_gate is not None:
    if _resolve_dna_field(dna, dna_gate["field"]) != dna_gate["value"]:
        continue  # suppress this candidate
# differentiator_edges: type "dna" → equality filter; "rpm_differential" → engine_state filter;
#                       type "physical_check" → informational (never filters)
```

`confidence` is **not** consumed by the strict gate. Its one functional use is `_rich_co_ceiling(dna)`: `co_high_idle` overrides the Euro default **only** when `confidence == "HIGH"`.

---

## 8. `GasLabDnaView` Optional / CoC Fields — Edge Cases

```python
target_lambda_v112: Optional[float]  # [0.5, 2.5]; certified CoC λ centre
co_low_idle:        Optional[float]  # [0, 15];   per-vehicle CoC idle CO ceiling
co_high_idle:       Optional[float]  # [0, 15];   per-vehicle CoC 2500 RPM CO ceiling
```

`_coc_adjust_normal_bounds` (rule_engine.py) rewrites `NORMAL_OPERATION` bounds before matching:
- When `target_lambda_v112` is present, the λ window becomes `[v112 − 0.005, v112 + 0.005]`, clamped to `[0.85, 1.15]`; absent → generic ±0.005 window centred on 1.000.
- The CO max is set to the Euro-scaled `co_idle_ceiling`, then overridden by `co_low_idle` when present.

`None` values never raise. The single-value `target_lambda_v112` replaces the old `target_lambda_low` / `target_lambda_high` pair (T-FX-DNA-1 CoC-target absorption, revised in v2.1).

---

## 9. Euro-Class Scaling (`resolution._euro_thresholds`)

```python
class EuroThresholds(NamedTuple):
    co_idle_ceiling: float
    hc_2500_ceiling: int | None

_EURO_THRESHOLDS = {                  # wiki: GASWIKI-02 §2.8
    "1": (4.5, None),
    "2": (0.5, 1200),
    "3": (0.3, 200),
    "4": (0.2, 200),
    "5": (0.2, 200),
}
```

`euro_emission_category` is normalised (upper-cased, `_`/`-`→space) and substring-matched; unknown values default to Euro 4. These ceilings feed the NORMAL_OPERATION CO max and the `CAM_TIMING_RETARDED_MAP` 2500 HC/CO gates.

---

## 10. Wideband O₂-Bias Calibration

When `dna.upstream_o2_type` contains `"wideband"` (case-insensitive), the O₂-sensor-bias signatures are recalibrated before matching:

```python
# _calibrate_o2_bias_low_bounds  — wiki: GASWIKI-05 §7.14
O2_BIAS_LOW.co     = {min: 5.0, max: 8.0}
O2_BIAS_LOW.lambda = {min: 0.77, max: 0.85}
# _calibrate_o2_bias_high_bounds — wiki: GASWIKI-05 §7.15
O2_BIAS_HIGH.lambda = {min: 1.12, max: 1.18}
```

---

## 11. Error Types

| Error | Raised when |
|-------|-------------|
| `OntologyLoadError(RuntimeError)` | YAML missing, malformed, or missing one of the 5 required top-level keys (`version`, `scope`, `validity_gates`, `reasoning_grammar`, `faults`) |
| `ValueError` | `GasReading.__post_init__` range check fails |
| Pydantic `ValidationError` | `GasLabPayload` or `GasLabDnaView` field constraint violated |

---

## 12. Forbidden Patterns (GASLab-specific)

| Pattern | Enforcement |
|---------|-------------|
| `from obdlab import …` / `from dtclab import …` / `from comlab import …` | Import-isolation audit in the validator suite |
| Numeric literals in `gaslab/` without a `# wiki:` / `# vocab:` comment | Code-review gate |
| Adding a field to `GasLabPayload` / `GasLabDnaView` without a named COMLab consumer | Signal/noise rule — field does not ship |
| Diesel-specific logic | `PRD_4D_App.md §5` scope exclusion |
| Adding a DNA field for MAF-vs-MAP metering | No consumer — the gas-direction discriminator carries the split instead |
