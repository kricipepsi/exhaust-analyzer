# CHEMISTRY COVERAGE — GASLab State × Fault Family Matrix

**Generated:** 2026-05-27
**Inputs:**
- `registry/corpus_curated.csv` (252 cases, 16 fault families)
- `registry/CORPUS_AUDIT.md` (AUDIT-CORPUS deliverable — per-family case counts)
- `registry/REGISTRY_AUDIT.md` (AUDIT-REG deliverable — v1 rule inventory, chemistry states)
- `GASLab/gaslab/contracts.py` (34-value `ChemicalSignature` enum)
- `COMLab/comlab/config/global_fault_registry.json` (53 v1 rules, chemistry-gated)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md` (per-phase chemistry distribution in 239 failing traces)

**Methodology note:** The curated corpus (`corpus_meta.json`) stores per-case fault-family labels but not per-case GASLab chemistry states — those are emitted at runtime. Cell counts in this matrix are **inferred** from three sources: (a) Jaeger trace data for the 239 failing cases (aggregate chemistry distributions from the capability analysis), (b) v1 rule `gas_lab_state` gating — each rule's chemistry→family intent, and (c) domain knowledge of which chemistry signatures correspond to which fault families per GAS_VOCABULARY.md. Cells marked **[J]** are trace-confirmed from Jaeger representative cases; cells marked **[R]** are mapped from v1 rule registrations; cells marked **[D]** are domain-inferred from the GASLab vocabulary. Exact per-case chemistry-state data requires running GASLab against all 252 curated cases (out of scope for this read-only audit).

---

## 1. Executive Summary

The v1 architecture gates every rule on a hard-coded `gas_lab_state` — only 11 unique chemistry states appear across all 53 rules. The GASLab `ChemicalSignature` enum defines **34 values**, meaning 23 chemistry states have zero executable rules regardless of case volume. The two most common chemistry signatures in failing traces — `TIMING_RETARDED` (64 cases, ~25% of the curated corpus) and `SAMPLE_INVALID` (17 cases) — have **zero matching v1 rules**, guaranteeing 100% prune on every case that produces them.

The matrix below exposes the full 34 × 16 coverage landscape. Every cell with a non-zero case count and zero v1 rules is a coverage gap the v2 registry must close. The three new fault families (`vacuum_leak`, `overheating`, `charging_system`) are OBD/voltage-driven rather than chemistry-driven and appear as a separate analysis block below the main matrix. The prioritized authoring order in §6 ranks families by case volume, chemistry coverage gap severity, and presence/absence of v1 rule infrastructure.

---

## 2. Chemistry States Observed in the Curated Corpus

The 34 GASLab `ChemicalSignature` values fall into four tiers based on corpus evidence:

### Tier A — Chemistry states with Jaeger-confirmed presence AND v1 rules (11 states)

These are the only chemistry states that can route through v1. Combined they cover an estimated 120–140 of the 252 curated cases.

| Chemistry State | Est. Cases in Corpus | v1 Rules | Primary Families Addressed |
|---|---|---|---|
| `LEAN_MIXTURE` | ~30 | 4 (ERR-LC-001, 003, 004×2) | lean_condition |
| `LEAN_MISFIRE` | ~15 | 3 (ERR-LC-004, MF-003, MF-005, MF-007) | lean_condition, misfire |
| `RICH_MIXTURE` | ~25 | 5 (ERR-RM-003..007) | rich_mixture |
| `RICH_MISFIRE` | ~5 | 1 (ERR-MF-002) | misfire |
| `IGNITION_MISFIRE` | ~20 | 6 (ERR-E2-I104, IF-001..003, MF-002, MF-004, MF-006, CT-002) | misfire, ignition_fault, cam_timing |
| `INCOMPLETE_COMBUSTION` | ~7 | 3 (ERR-MW-001, MW-005, NS-004) | mechanical_wear, non_starter |
| `CATALYST_OVERWHELMED` | ~15 | 5 (ERR-CF-001..004, CF-005 subset) | catalyst_failure |
| `CATALYST_NOT_LIGHTING_OFF` | ~3 | 1 (ERR-CF-007) | catalyst_failure |
| `NORMAL_OPERATION` | ~15 | 4 (ERR-CF-005, EL-004, CT-005, SF-001×2, SF-002) | catalyst_failure, exhaust_leak, cam_timing, sensor_fault |
| `EXHAUST_AIR_LEAK` | ~8 | 5 (ERR-EL-001..003, EL-005, EL-006) | exhaust_leak |
| `POA_SIGNATURE` | ~5 | 3 (ERR-CF-006, RM-001, RM-002) | catalyst_failure, rich_mixture |

### Tier B — Chemistry states with Jaeger-confirmed presence but ZERO v1 rules (2 states)

These are the single largest coverage gap. Combined, they account for ~81 cases (~32% of the curated corpus) that are guaranteed to prune in v1.

| Chemistry State | Est. Cases in Corpus | v1 Rules | Primary Families Addressed |
|---|---|---|---|
| `TIMING_RETARDED` | **~64** [J] | **0** | lean_condition, catalyst_failure, sensor_fault, cam_timing, misfire, ecu_fault, mechanical_wear |
| `SAMPLE_INVALID` | **~17** [J] | **0** | misfire (DTCLab enum crash cases), lean_condition, rich_mixture, no_fault |

### Tier C — Chemistry states with v1 rules but uncertain Jaeger presence (8 states)

These have rule registrations but their actual emission frequency in the curated corpus is not directly measured. They account for the remaining chemistry-gated rules.

| Chemistry State | v1 Rules | Intended Families |
|---|---|---|
| `INCOMPLETE_OXIDATION` | 1 (ERR-E1-M032, starter — no KG node) | lean_condition (EGR-specific) |
| `WORN_PISTON_RINGS` | 1 (ERR-MW-003) | mechanical_wear |
| `WORN_VALVE_SEALS` | 1 (ERR-MW-004) | mechanical_wear |
| `WORN_ENGINE` | 1 (ERR-MW-006) | mechanical_wear |
| `WRONG_VALVE_TIMING` | 2 (ERR-CT-001, CT-003) | cam_timing |
| `VVT_FAILURE` | 2 (ERR-CT-003, CT-004) | cam_timing |
| `COOLANT_LEAK_INTERNAL` | 1 (ERR-MW-002) | mechanical_wear |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | 1 (ERR-E3-F501) | rich_mixture (GDI only) |

### Tier D — Chemistry states in GASLab vocabulary with no v1 rules and no Jaeger-confirmed presence (11 states)

These are defined in `ChemicalSignature` but neither appear in Jaeger traces nor have v1 rules. They may appear in future test cases or represent edge conditions outside the curated corpus scope.

| Chemistry State | Notes |
|---|---|
| `HIGH_COMBUSTION_TEMP` | May appear in NOx-heavy cases; no current corpus evidence |
| `TIMING_OVER_ADVANCED` | Related to `TIMING_RETARDED`; no current corpus evidence |
| `O2_SENSOR_BIASED_LOW` | Related to `NORMAL_OPERATION` sensor_fault rules (ERR-SF-001 perception flag) |
| `O2_SENSOR_BIASED_HIGH` | Related to `NORMAL_OPERATION` sensor_fault rules (ERR-SF-001 perception flag) |
| `FLAT_CAMSHAFT` | Mechanical; may overlap with cam_timing |
| `GDI_INTAKE_VALVE_CARBON` | GDI-specific; may overlap with lean_condition / misfire |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` | May overlap with rich_mixture |
| `EGR_STUCK_CLOSED` | May overlap with lean_condition |
| `EGR_STUCK_OPEN` | Already covered by `INCOMPLETE_OXIDATION` path |
| `EVAP_CANISTER_SATURATED` | May overlap with rich_mixture |
| `EGR_DILUTION_MISFIRE` | May overlap with misfire |

---

## 3. Full Chemistry × Fault Family Matrix

Rows = GASLab chemistry states (34). Columns = 13 existing fault families + 3 new families (16 total). Cells show estimated curated case counts. Zero means no case in the curated corpus carries that chemistry AND is labelled with that family. Empty cells with notes indicate the chemistry→family mapping is domain-plausible but uncounted.

**Legend:** [J] = Jaeger trace-confirmed · [R] = v1 rule registration · [D] = domain inference · **0** = confirmed zero (no cases) · `—` = not applicable (chemistry/family mismatch)

### 3.1 Tier A — Chemistry states with v1 rule coverage (11 rows)

| Chemistry State ↓ / Family → | lean_cond | misfire | ecu_fault | rich_mix | catalyst | sensor | no_fault | mech_wear | cam_timing | exhaust | non_start | ignition | invalid | vacuum | overheat | charge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `LEAN_MIXTURE` [R] | **~25** [J] | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `LEAN_MISFIRE` [R] | ~5 [R] | **~10** [R] | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `RICH_MIXTURE` [R] | — | — | — | **~22** [R] | — | — | — | — | — | — | — | — | — | — | — | — |
| `RICH_MISFIRE` [R] | — | **~5** [R] | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `IGNITION_MISFIRE` [R] | — | **~12** [R] | — | — | — | — | — | — | ~3 [R] | — | — | **~3** [R] | — | — | — | — |
| `INCOMPLETE_COMBUSTION` [R] | — | — | — | — | — | — | — | **~5** [R] | — | — | **~2** [R] | — | — | — | — | — |
| `CATALYST_OVERWHELMED` [R] | — | — | — | — | **~15** [R] | — | — | — | — | — | — | — | — | — | — | — |
| `CATALYST_NOT_LIGHTING_OFF` [R] | — | — | — | — | **~3** [R] | — | — | — | — | — | — | — | — | — | — | — |
| `NORMAL_OPERATION` [R] | — | — | — | — | ~3 [R] | **~4** [R] | ~2 [D] | — | ~1 [R] | ~2 [R] | — | — | — | — | — | — |
| `EXHAUST_AIR_LEAK` [R] | — | — | — | — | — | — | — | — | — | **~6** [R] | — | — | — | — | — | — |
| `POA_SIGNATURE` [R] | — | — | — | ~3 [R] | ~2 [R] | — | — | — | — | — | — | — | — | — | — | — |

### 3.2 Tier B — Chemistry states with zero v1 rules (HIGH PRIORITY GAPS, 2 rows)

| Chemistry State ↓ / Family → | lean_cond | misfire | ecu_fault | rich_mix | catalyst | sensor | no_fault | mech_wear | cam_timing | exhaust | non_start | ignition | invalid | vacuum | overheat | charge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `TIMING_RETARDED` [J] | **~15** [J] | ~8 [J] | ~10 [J] | ~5 [D] | **~10** [J] | ~8 [J] | ~2 [D] | ~3 [D] | ~3 [D] | — | — | — | — | — | — | — |
| `SAMPLE_INVALID` [J] | ~3 [J] | **~10** [J] | ~2 [J] | ~2 [J] | — | — | — | — | — | — | — | — | — | — | — | — |

The `TIMING_RETARDED` row is the single largest coverage gap in the entire registry. 64 curated cases produce this chemistry — it is the most common GASLab emission — yet zero v1 rules accept it. These 64 cases are distributed across 7 fault families, with lean_condition, catalyst_failure, and ecu_fault being the most common labels. The v2 registry MUST include `TIMING_RETARDED` as a gating evidence tier for at minimum lean_condition, catalyst_failure, sensor_fault, and ecu_fault families.

The `SAMPLE_INVALID` row covers cases where GASLab's triangle-gate rejects the sample as unphysical (CO+CO2+O2 outside [14,16]). 10 of the 17 cases are misfire cases currently crashing at DTCLab validation (they will route to comlab.aggregate after FIX-ENUM-1). The v2 registry should treat `SAMPLE_INVALID` as suggestive evidence rather than a hard gate — it signals a measurement anomaly, not a diagnostic conclusion.

### 3.3 Tier C — Chemistry states with v1 rules, uncertain trace presence (8 rows)

| Chemistry State ↓ / Family → | lean_cond | misfire | ecu_fault | rich_mix | catalyst | sensor | no_fault | mech_wear | cam_timing | exhaust | non_start | ignition | invalid | vacuum | overheat | charge |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `INCOMPLETE_OXIDATION` [R] | ~1 [R] | — | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| `WORN_PISTON_RINGS` [R] | — | — | — | — | — | — | — | **~3** [R] | — | — | — | — | — | — | — | — |
| `WORN_VALVE_SEALS` [R] | — | — | — | — | — | — | — | **~2** [R] | — | — | — | — | — | — | — | — |
| `WORN_ENGINE` [R] | — | — | — | — | — | — | — | **~2** [R] | — | — | — | — | — | — | — | — |
| `WRONG_VALVE_TIMING` [R] | — | — | — | — | — | — | — | — | **~5** [R] | — | — | — | — | — | — | — |
| `VVT_FAILURE` [R] | — | — | — | — | — | — | — | — | **~5** [R] | — | — | — | — | — | — | — |
| `COOLANT_LEAK_INTERNAL` [R] | — | — | — | — | — | — | — | **~1** [R] | — | — | — | — | — | — | — | — |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` [R] | — | — | — | ~1 [R] | — | — | — | — | — | — | — | — | — | — | — | — |

### 3.4 Tier D — No rules, no confirmed trace presence (11 rows)

These 11 chemistry states have no v1 rules and no Jaeger-confirmed emission in the curated corpus. They are recorded for completeness; the v2 schema should accommodate them as the evidence-tier vocabulary without requiring per-state rules at authoring time. Any that appear in future case additions (e.g., `GDI_INTAKE_VALVE_CARBON` for GDI-specific lean_condition cases) will already have a schema slot.

| Chemistry State | Plausible Families (domain) | v2 Action |
|---|---|---|
| `HIGH_COMBUSTION_TEMP` | catalyst_failure, sensor_fault | Schema slot only |
| `TIMING_OVER_ADVANCED` | cam_timing, mechanical_wear | Schema slot only |
| `O2_SENSOR_BIASED_LOW` | sensor_fault (O2 perception) | Covered by v1 ERR-SF-001 perception_flag path |
| `O2_SENSOR_BIASED_HIGH` | sensor_fault (O2 perception) | Covered by v1 ERR-SF-001 perception_flag path |
| `FLAT_CAMSHAFT` | cam_timing, mechanical_wear | Schema slot only |
| `GDI_INTAKE_VALVE_CARBON` | lean_condition, misfire | Schema slot; may need rule if GDI cases added |
| `VACUUM_REGULATOR_DIAPHRAGM_RUPTURE` | rich_mixture | Schema slot only |
| `EGR_STUCK_CLOSED` | lean_condition | Schema slot only |
| `EGR_STUCK_OPEN` | lean_condition | Covered by INCOMPLETE_OXIDATION path |
| `EVAP_CANISTER_SATURATED` | rich_mixture | Schema slot only |
| `EGR_DILUTION_MISFIRE` | misfire | Schema slot only |

---

## 4. Gap Analysis

### 4.1 Families with zero chemistry coverage for observed signatures

| Family | Curated Cases | Chemistry States with Rules | Chemistry States with ZERO Rules (but cases exist) | Severity |
|---|---|---|---|---|
| `ecu_fault` | **28** | **0** | TIMING_RETARDED (~10), SAMPLE_INVALID (~2) | **CRITICAL** — third-largest family, zero executable rules. Both KG nodes are orphans. |
| `lean_condition` | 53 | 5 (LEAN_MIXTURE, LEAN_MISFIRE) | TIMING_RETARDED (~15), SAMPLE_INVALID (~3) | **HIGH** — largest family by case count; 15+ cases produce TIMING_RETARDED chemistry that no rule accepts. |
| `catalyst_failure` | 21 | 7 | TIMING_RETARDED (~10) | **HIGH** — 10+ cases produce TIMING_RETARDED; v1 CATALYST_OVERWHELMED gate misses marginal catalyst degradation. |
| `sensor_fault` | 20 | 3 (NORMAL_OPERATION only) | TIMING_RETARDED (~8) | **HIGH** — 4 of 6 KG nodes are orphans; only O2 sensor faults executable. |
| `misfire` | 44 | 10 | SAMPLE_INVALID (~10), TIMING_RETARDED (~8) | **MEDIUM** — most rules exist but 30 cases are DTCLab-crashed (will recover); SAMPLE_INVALID cases need chemistry-agnostic routing. |
| `cam_timing` | 9 | 5 | TIMING_RETARDED (~3) | **MEDIUM** — 4 of 5 rules require vvt_equipped precondition; non-VVT engines have 1 rule. |
| `mechanical_wear` | 11 | 6 | TIMING_RETARDED (~3) | **LOW** — most chemistries covered; cross-family confusion (lean vs mechanical) is a competition issue, not a coverage gap. |
| `rich_mixture` | 23 | 7 | SAMPLE_INVALID (~2) | **LOW** — rules exist and cover RICH_MIXTURE + POA_SIGNATURE; GDI path is narrow but exists. |
| `ignition_fault` | 3 | 3 | — | **LOW** — small family; all 3 rules require DTC match. |
| `exhaust_leak` | 5 | 6 | — | **LOW** — more rules than cases; chemistry gating mismatches rather than absence. |
| `non_starter` | 4 | 1 | — | **LOW** — 2 pipeline-bug cases recover post FIX-GAS-1. |
| `no_fault` | 17 | — | — | **N/A** — healthy baseline; correct default-to-no_fault behavior. |
| `invalid_input` | 2 | 0 | — | **EXPECTED** — sentinel cases; validation-only, not diagnostic. |

### 4.2 Chemistries with zero matching rules (ordered by case impact)

| Rank | Chemistry State | Est. Cases Affected | Families Blocked | v2 Action |
|---|---|---|---|---|
| 1 | `TIMING_RETARDED` | **~64** | 7 families | Add as evidence-tier entry for lean_condition, catalyst_failure, sensor_fault, ecu_fault, misfire, cam_timing, mechanical_wear. This is the #1 v2 authoring priority. |
| 2 | `SAMPLE_INVALID` | **~17** | 4 families | Treat as suggestive evidence (measurement anomaly signal) rather than a gate. Route to invalid_input when isolated; route to misfire/lean/rich when accompanied by DTCs. |
| 3 | All 11 Tier D states | 0 (no confirmed cases) | 0 | Schema slots only — define them in the v2 evidence-tier vocabulary without per-state rules. |

### 4.3 Families with only one chemistry signature (solo-survivor risk)

| Family | Chemistry States with Rules | Solo-Survivor Risk |
|---|---|---|
| `ecu_fault` | **0** | **CRITICAL** — no chemistry signature at all; must be DTC-driven or OBD-driven in v2. |
| `non_starter` | 1 (INCOMPLETE_COMBUSTION) | **HIGH** — single rule (ERR-NS-004) at base_weight 0.60. No competing paths. |
| `ignition_fault` | 1 (IGNITION_MISFIRE) | **MEDIUM** — all 3 rules share the same chemistry state; differentiated only by DTC and OBD thresholds. |
| `rich_mixture` | 3 (RICH_MIXTURE, POA_SIGNATURE, GDI_HPFP) | **LOW** — three distinct chemistry paths; competition exists. |
| `lean_condition` | 2 (LEAN_MIXTURE, LEAN_MISFIRE) | **LOW** — but both are lean variants; TIMING_RETARDED adds a third path in v2. |

### 4.4 The new families — chemistry-independent

The three new fault families from `cvsgaps.md` (`vacuum_leak`, `overheating`, `charging_system`) are primarily OBD/voltage-driven rather than gas-chemistry-driven:

| Family | Chemistry Overlap | Detection Signal | v2 Strategy |
|---|---|---|---|
| `vacuum_leak` (4 placeholder cases) | Shares LEAN_MIXTURE chemistry with `lean_condition` | Lean trims at idle that correct at 2500 RPM (Brettschneider-confirmed) | Competing rule: LEAN_MIXTURE + trim correction at 2500 RPM → vacuum_leak vs lean_condition. The RPM-dependent trim pattern is the differentiator. |
| `overheating` (4 placeholder cases) | May produce NORMAL_OPERATION or HIGH_COMBUSTION_TEMP | High coolant temp + RPM behaviour; not always DTC-driven | Primarily OBD-driven: ect_c > threshold + RPM pattern. Chemistry may be normal if overheating is mechanical (stuck thermostat), or elevated NOx if combustion-temp-driven. |
| `charging_system` (3 placeholder cases) | No direct chemistry signature | Low/bouncing voltage, sensor noise, ghost misfires | Voltage-driven: OBD voltage PID + sensor noise pattern. May trigger ghost misfire chemistry via sensor artifacts. |

These families require OBD-evidence-tier rules rather than chemistry-gated rules. Their presence in the matrix is noted but their case counts are not chemistry-assigned.

---

## 5. Cross-Reference: REGISTRY_AUDIT.md §2.2 v1 Chemistry States

REGISTRY_AUDIT.md §2.2 lists 19 v1 chemistry states with rule registrations. Below is the mapping of each v1 state to the curated corpus families it currently addresses vs. families it SHOULD also address per the Jaeger evidence.

| v1 Chemistry State | Currently Addresses (v1) | Should Also Address (Jaeger evidence) | Gap Type |
|---|---|---|---|
| `LEAN_MIXTURE` | lean_condition | — | None (correct mapping) |
| `LEAN_MISFIRE` | lean_condition, misfire | — | None (correct mapping) |
| `RICH_MIXTURE` | rich_mixture | — | None (correct mapping) |
| `RICH_MISFIRE` | misfire | — | None (correct mapping) |
| `IGNITION_MISFIRE` | misfire, ignition_fault, cam_timing | — | None (correct mapping) |
| `INCOMPLETE_OXIDATION` | lean_condition (EGR) | — | Single stale rule (ERR-E1-M032, no KG node) — needs v2 rewrite |
| `INCOMPLETE_COMBUSTION` | mechanical_wear, non_starter | — | None (correct mapping) |
| `CATALYST_OVERWHELMED` | catalyst_failure | — | None (correct mapping) |
| `CATALYST_NOT_LIGHTING_OFF` | catalyst_failure | — | None (correct mapping) |
| `NORMAL_OPERATION` | catalyst_failure, exhaust_leak, cam_timing, sensor_fault | no_fault (healthy baselines should route here explicitly) | Overloaded — 4 families share one chemistry state; needs v2 competition groups |
| `EXHAUST_AIR_LEAK` | exhaust_leak | — | None (correct mapping) |
| `POA_SIGNATURE` | catalyst_failure, rich_mixture | — | None (correct mapping) |
| `WORN_PISTON_RINGS` | mechanical_wear | sensor_fault, catalyst_failure (cases labelled these families produce this chemistry) | Cross-family confusion — chemistry→family mapping is not 1:1 |
| `WORN_VALVE_SEALS` | mechanical_wear | — | None (correct mapping) |
| `WORN_ENGINE` | mechanical_wear | — | None (correct mapping) |
| `WRONG_VALVE_TIMING` | cam_timing | — | None (correct mapping) |
| `VVT_FAILURE` | cam_timing | — | None (correct mapping) |
| `COOLANT_LEAK_INTERNAL` | mechanical_wear | — | None (correct mapping) |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | rich_mixture | — | None (correct mapping, GDI-only) |

**Two critical v1 states missing from the list above** (they exist in GASLab's `ChemicalSignature` enum but have zero rules):

| Missing State | Jaeger Cases | Families Affected |
|---|---|---|
| `TIMING_RETARDED` | ~64 | lean_condition, catalyst_failure, sensor_fault, ecu_fault, misfire, cam_timing, mechanical_wear |
| `SAMPLE_INVALID` | ~17 | misfire, lean_condition, rich_mixture, ecu_fault |

These two states alone account for **~81 of 239 failing cases (33.9%)** and are the first gap the v2 registry must close.

---

## 6. Prioritized REG-V2-AUTHOR-{family} Task Order

Ordered by: (1) case volume in curated corpus, (2) chemistry coverage gap severity, (3) whether the family is new (no v1 rules exist). Each row includes a one-line justification.

| Priority | Task ID | Family | Curated Cases | Chemistry Gap Severity | New Family? | Justification |
|---|---|---|---|---|---|---|
| **1** | REG-V2-AUTHOR-lean_condition | `lean_condition` | 53 | **HIGH** — TIMING_RETARDED (~15 cases) unserved; largest family by volume | No | Largest case volume + the most common chemistry (TIMING_RETARDED) has zero rules for this family. Authoring lean_condition rules first establishes the v2 evidence-tier pattern that all subsequent families follow. |
| **2** | REG-V2-AUTHOR-ecu_fault | `ecu_fault` | 28 | **CRITICAL** — zero chemistry states, zero executable rules | No | Third-largest family with zero working rules. Both KG nodes are orphans. Must be DTC-driven or OBD-driven in v2 — this is the hardest family to author and should be tackled early while context is fresh. |
| **3** | REG-V2-AUTHOR-misfire | `misfire` | 44 | **MEDIUM** — SAMPLE_INVALID (~10 cases) + TIMING_RETARDED (~8) unserved; 30 DTCLab-crashed cases will auto-recover | No | Second-largest family; 30 of 44 cases will enter the router after FIX-ENUM-1. Needs SAMPLE_INVALID-aware rules and chemistry-agnostic DTC-driven paths. |
| **4** | REG-V2-AUTHOR-catalyst_failure | `catalyst_failure` | 21 | **HIGH** — TIMING_RETARDED (~10 cases) unserved; CATALYST_OVERWHELMED gate misses marginal degradation | No | CATALYST_OVERWHELMED is a late-stage signature; v2 needs marginal-catalyst rules that fire on less severe chemistry. |
| **5** | REG-V2-AUTHOR-sensor_fault | `sensor_fault` | 20 | **HIGH** — 4 of 6 KG nodes are orphans; TIMING_RETARDED (~8) unserved; only O2 sensor faults executable | No | Needs MAF, MAP, ECT, downstream-O2 rules reactivated from orphan KG nodes. O2 perception-flag path (ERR-SF-001) is a good v2 evidence-tier template. |
| **6** | REG-V2-AUTHOR-rich_mixture | `rich_mixture` | 23 | **LOW** — rules exist; SAMPLE_INVALID (~2 cases) + GDI-only path narrow | No | Best-covered family in v1. v2 work is primarily: add TIMING_RETARDED awareness for rich→retarded overlap cases, and ensure competition groups with lean_condition for ambiguous signatures. |
| **7** | REG-V2-AUTHOR-mechanical_wear | `mechanical_wear` | 11 | **LOW** — most chemistries covered; cross-family confusion with lean_condition | No | Cross-family competition is the main v2 task (WORN_PISTON_RINGS routes to mechanical_wear but cases are labelled sensor_fault/catalyst_failure). |
| **8** | REG-V2-AUTHOR-cam_timing | `cam_timing` | 9 | **MEDIUM** — TIMING_RETARDED (~3) + vvt_equipped precondition restricts 4 of 5 rules | No | Non-VVT path needs expansion. VVT_FAILURE rules need competition with mechanical_wear. |
| **9** | REG-V2-AUTHOR-exhaust_leak | `exhaust_leak` | 5 | **LOW** — more rules than cases; chemistry gating mismatches | No | Reduce from 6 rules to 2-3 with broader chemistry acceptance. ERR-EL-004 (NORMAL_OPERATION, weight 0.55) is a false-positive risk on healthy cases. |
| **10** | REG-V2-AUTHOR-non_starter | `non_starter` | 4 | **HIGH** — single rule (ERR-NS-004, weight 0.60); solo survivor | No | Needs at least one competing rule. 2 of 4 cases will recover post FIX-GAS-1; the other 2 need chemistry-agnostic cranking-signature detection. |
| **11** | REG-V2-AUTHOR-ignition_fault | `ignition_fault` | 3 | **MEDIUM** — solo chemistry state (IGNITION_MISFIRE); all 3 rules require DTC match | No | Small family; v2 work is adding DTC-less ignition-fault detection (e.g., high HC + normal CO at idle without misfire DTC). |
| **12** | REG-V2-AUTHOR-vacuum_leak | `vacuum_leak` | 4 (new) | **N/A** — new family | **Yes** | OBD-driven: LEAN_MIXTURE chemistry + trim correction at 2500 RPM. Competing rule with lean_condition. 4 placeholder cases need populating. |
| **13** | REG-V2-AUTHOR-overheating | `overheating` | 4 (new) | **N/A** — new family | **Yes** | OBD-driven: ect_c + RPM pattern. May produce NORMAL_OPERATION or HIGH_COMBUSTION_TEMP chemistry. 4 placeholder cases need populating. |
| **14** | REG-V2-AUTHOR-charging_system | `charging_system` | 3 (new) | **N/A** — new family | **Yes** | Voltage-driven: OBD voltage PID + sensor noise pattern. No direct chemistry signature. 3 placeholder cases need populating. |

**Authoring dependency note:** REG-V2-SCHEMA must land before any REG-V2-AUTHOR-* task. The schema defines the evidence-tier vocabulary (definitive / suggestive / gating), competition group structure, and confidence-ceiling fields that every family authoring task references. The three new families (vacuum_leak, overheating, charging_system) are placed at positions 12-14 because (a) they have zero existing KG nodes to reference, (b) their placeholder cases need populating during authoring, and (c) the evidence-tier patterns should be proven on existing families first.

---

## 7. Bottom Line

| Metric | Value |
|---|---|
| GASLab chemistry states defined (`ChemicalSignature` enum) | 34 |
| Chemistry states with ≥1 v1 rule | 11 |
| Chemistry states with zero v1 rules | 23 (68%) |
| Chemistry states with zero rules AND confirmed Jaeger presence | **2 (TIMING_RETARDED, SAMPLE_INVALID)** |
| Cases producing TIMING_RETARDED (est.) | **~64 (25% of curated corpus)** |
| Cases producing SAMPLE_INVALID (est.) | **~17 (7% of curated corpus)** |
| Families with zero chemistry coverage | **1 (ecu_fault — 28 cases, 11% of corpus)** |
| Families with solo chemistry state | 3 (ecu_fault=0, non_starter=1, ignition_fault=1) |
| KG nodes that are unreachable orphans | 12 of 58 (21%) |
| v2 authoring tasks required | 14 (13 existing families + 3 new, minus invalid_input) |
| Chemistry-independent families (OBD/voltage-driven) | 3 (vacuum_leak, overheating, charging_system) |

The v2 registry's primary task is clear: replace 11 hard-coded chemistry gates with a 34-slot evidence-tier vocabulary where every chemistry state is a weighted signal, not a mandatory key. The two highest-impact authoring priorities are (1) lean_condition rules that accept TIMING_RETARDED chemistry, and (2) ecu_fault rules that operate on DTC + OBD evidence without requiring a chemistry state at all.

The cutover gate from v1 to v2 (per `JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10.4) requires v2 PASS count >= v1 PASS count on the curated corpus before v1 retires. This matrix is the authoring specification that every REG-V2-AUTHOR-{family} task references to ensure v2 clears that gate.

**Note on sentinel cases:** One curated case (`case_011`, GARBAGE DTC) has an empty `expected_top_fault_family` — it is a validation-only sentinel kept per cvsgaps.md guidance. It does not appear in the chemistry matrix because it tests input validation, not diagnostic routing.

---

*End of CHEMISTRY_COVERAGE.md*
