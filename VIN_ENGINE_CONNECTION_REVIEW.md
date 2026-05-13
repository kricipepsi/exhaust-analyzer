# VIN → Engine Connection Review

**Date:** 2026-05-11  
**Question:** Do values resolved by the VIN module (induction, o2_arch, injection, spec_idle_gps, known_issues, etc.) actually reach the diagnostic engine and influence the workflow?

---

## Short Answer

**Partially — and with a critical gap in the vref.db miss path.**

The VIN module resolves rich engine specs into `EngineDNA`. The engine uses **exactly two fields** from it: `engine_code` and `displacement_l`. Everything else — induction type, injection type, o2 architecture, spec_idle_gps, cylinders, intercooler, known_issues — is resolved by the VIN module, displayed in the UI sidebar, and then **silently discarded** before the diagnostic pipeline starts.

The pipeline's ground truth for tech flags and thresholds is `vref.db`, not `engine_dna.json`. These are two separate databases that have no overlap and no reconciliation path.

---

## The Two Databases

| Database | Rows | What it contains | Who reads it |
|---|---|---|---|
| `engine/v2/vref.db` | **68** | tech_mask flags, o2_type, target_lambda_v112, target_rpm_u2 | `dna_core.load_dna()` exclusively |
| `engine/v2/vin/data/engine_dna.json` | **1,978** | induction, injection, o2_arch, cylinders, intercooler, spec_idle_gps, known_issues | VIN resolver → UI sidebar only |

68 rows vs 1,978 rows. **Any engine not in vref.db falls back to all-zeros tech_mask**, regardless of what VIN DNA knows about it.

---

## Data Flow Trace

### What `dna_core.load_dna()` actually takes from VIN:

```python
# dna_core.py lines 137–142 — the complete VIN handoff
if vin_dna.confidence == "high":
    engine_code = vin_dna.engine_code or engine_code        # ← taken
    displacement_cc = int(round(vin_dna.displacement_l * 1000))  # ← taken
elif vin_dna.confidence == "partial":
    engine_code = vin_dna.engine_code or engine_code        # ← taken
```

That's it. Then it queries vref.db by `engine_code`. Everything else on `EngineDNA` is never read.

### What `DNAOutput` carries downstream:

| `DNAOutput` field | Source | Notes |
|---|---|---|
| `engine_state` | OBD/FF ECT + RPM | Not from VIN |
| `era_bucket` | vref.db (or MY fallback) | |
| `tech_mask` (has_vvt, has_gdi, has_turbo, is_v_engine, has_egr, has_secondary_air) | **vref.db only** | VIN `induction`/`injection` ignored |
| `o2_type` (NB/WB) | **vref.db only** | VIN `o2_arch` ignored |
| `target_lambda_v112` | **vref.db only** | Not in engine_dna.json |
| `target_rpm_u2` | **vref.db only** | Not in engine_dna.json |
| `confidence_ceiling` | vref.db hit/miss | |

---

## What VIN Resolves But the Engine Never Sees

### 1. `induction` (na / turbo / super / twincharged) — NOT connected

**EngineDNA** has `induction` (e.g. `"turbo"`).  
**DNAOutput** has `tech_mask["has_turbo"]` — but this comes only from vref.db.

**Impact:** When vref.db misses (the common case — only 68 entries), `has_turbo = False` regardless of VIN DNA. This means:
- Boost-related fault nodes in `kg_engine` are vetoed by tech_mask even for turbo engines
- The arbitrator and gas_lab have no induction context
- No threshold adjustment for turbo-specific lambda targets or HC baselines

**What should happen:** When vref.db misses and VIN DNA says `induction="turbo"`, the fallback tech_mask should set `has_turbo=True`. Same for `is_v_engine` (VIN DNA has `cylinders` — V6/V8 can be inferred).

### 2. `o2_arch` (narrowband / wideband) — NOT connected

**EngineDNA** has `o2_arch` (e.g. `"wideband"`).  
**DNAOutput** has `o2_type` ("NB"/"WB") — from vref.db only. Falls back to `"NB"` on miss.

**Impact:** `o2_type` is currently carried in `DNAOutput` but not consumed by any downstream module (gas_lab and arbitrator don't gate on it). However, the architecture intends it to influence O2 symptom interpretation — wideband O2 sensors have a different voltage range and switching behaviour than narrowband. When `o2_type` defaults to "NB" on a wideband vehicle, any future O2-arch-gated logic will produce wrong results. This is a **latent bug** when that logic is added.

### 3. `injection` (mpfi / gdi / tsi) — NOT connected

**EngineDNA** has `injection`.  
**DNAOutput** has `tech_mask["has_gdi"]` — from vref.db only.

**Impact:** GDI engines have systematically higher baseline HC (~30–50% above MPFI at idle) due to wall-wetting and stratified charge. The gas_lab HC threshold (`_HC_MISFIRE_PPM = 600 ppm`) is flat — it does not adjust for injection type. A GDI engine in normal operation can trigger `SYM_HC_HIGH` at readings that are clinically normal for that technology. VIN DNA knows it's GDI; the engine does not.

### 4. `known_issues` — NOT connected

**EngineDNA** has `known_issues` — a curated list of high-prevalence faults for that engine code.  
**Nothing in the pipeline reads this.**

**Impact:** These represent prior probability adjustments — a known high-prevalence fault should have a higher prior weight during scoring. The faults.yaml has a `prior` field per fault; known_issues could populate or boost it. Currently the curated data exists but produces no diagnostic effect.

**Example from engine_dna.json:**
```json
{ "engine_code": "N20B20", "known_issues": ["timing_chain_stretch", "vanos_fault"] }
```
These never reach the KG engine's prior weighting.

### 5. `spec_idle_gps` — NOT connected

**EngineDNA** has `spec_idle_gps` (expected idle exhaust mass-flow, e.g. 2.74 g/s for a 1.37L engine).  
**Nothing in the pipeline reads this.**

**Potential use:** Cross-check against MAF-derived mass flow if OBD MAF is present. Significant deviation from spec_idle_gps at idle indicates intake leak, restricted airflow, or MAF sensor fault — a useful L3 cross-channel signal.

### 6. `cylinders` — NOT connected

**EngineDNA** has `cylinders`.  
The engine does not use this anywhere. It could inform:
- V-engine detection (4 vs 6/8 cylinders + layout): V6/V8 → `is_v_engine` heuristic when vref.db misses
- Misfire probability per-cylinder context

---

## What IS Working Correctly

| Connection | Status |
|---|---|
| VIN `engine_code` → vref.db lookup → `tech_mask` | ✅ Works (when engine_code is in vref.db) |
| VIN `engine_code` → vref.db lookup → `target_lambda_v112` → gas_lab baseline deviation | ✅ Works |
| VIN `engine_code` → vref.db lookup → `tech_mask` → kg_engine tech/era veto | ✅ Works |
| VIN `displacement_l` → `displacement_cc` → `_compute_breathing_efficiency` in digital_parser | ✅ Works |
| VIN display in UI sidebar (make, engine_code, induction, displacement) | ✅ Works (UI only) |

---

## The Core Problem

The VIN module and the vref.db pipeline are **two parallel knowledge bases with no reconciliation path.** They overlap on `engine_code` (the join key), but diverge everywhere else:

- vref.db has `target_lambda_v112`, `target_rpm_u2` — critical thresholds the VIN module doesn't carry
- engine_dna.json has `induction`, `injection`, `o2_arch`, `known_issues` — rich context the vref.db doesn't carry

When vref.db hits (68 rows), the pipeline is correctly informed.  
When vref.db misses (the majority of real-world engines), the pipeline runs on all-zeros tech_mask and generic thresholds — despite the VIN module having resolved meaningful spec data that could partially recover the situation.

---

## Recommended Fixes, In Priority Order

### Fix A — VIN fallback bridge (highest impact, low effort)

When vref.db misses and VIN DNA has `confidence="high"`, use VIN DNA fields to populate the fallback tech_mask:

```python
# dna_core.py — in the vref.db miss branch
if row is None:
    tech_mask = {flag: False for flag in _TECH_FLAG_NAMES}
    # Bridge VIN DNA into fallback tech_mask
    if vin_dna is not None and vin_dna.confidence == "high":
        if vin_dna.induction in ("turbo", "super", "twincharged"):
            tech_mask["has_turbo"] = True
        if vin_dna.injection in ("gdi", "tsi"):
            tech_mask["has_gdi"] = True
        if vin_dna.o2_arch == "wideband":
            o2_type = "WB"
        # V-engine heuristic from cylinders
        if vin_dna.cylinders in (6, 8, 10, 12):
            tech_mask["is_v_engine"] = True
```

**This alone eliminates the most damaging vref.db miss degradation with ~15 lines of code.**

### Fix B — known_issues → prior boost

Pass `vin_dna.known_issues` into `ResolutionContext` and, in `resolve_conflicts`, apply a prior multiplier to faults in the known_issues list before the sort step. This requires:
1. Adding `known_issues: list[str]` to `ResolutionContext`
2. Adding a boost step (e.g. ×1.3) in `_build_result` for matched fault IDs

### Fix C — GDI HC threshold adjustment

In `gas_lab._detect_gas_symptoms`, accept an optional `has_gdi: bool` parameter (already available from `DNAOutput.tech_mask`) and adjust `_HC_MISFIRE_PPM` accordingly (e.g. 900 ppm for GDI vs 600 ppm for MPFI). This is a one-line threshold change once the flag is wired through.

### Fix D — spec_idle_gps MAF cross-check

In `arbitrator.py` or `digital_parser.py`, add a cross-check: if OBD MAF is present and `spec_idle_gps` is known, compare at idle RPM. Significant deviation fires a symptom (e.g. `SYM_MAF_IDLE_DEVIATION`). Requires `spec_idle_gps` to be added to `DNAOutput` or passed separately.

---

## Summary

The VIN lookup module works correctly as a **UI enrichment tool** — it displays make, engine code, displacement, and induction type in the sidebar. But as a **diagnostic enrichment tool**, it stops at the vref.db lookup boundary. The 1,978-row engine_dna.json is essentially unused by the engine. Fix A (the fallback bridge) is the highest-ROI change: it makes every engine not in vref.db a significantly better-diagnosed case.
