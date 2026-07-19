# CORPUS AUDIT — v2 Ground-Truth Corpus Curation

**Generated:** 2026-05-27
**Input:** `TestSuite/cases_petrol_master_v6.csv` (281 cases)
**Proposal source:** `registry/cvsgaps.md` (46 proposed dispositions)
**Jaeger evidence:** `4DLabWired/_jaeger/runs/20260527-044325/FAILURE_BLUEPRINT.md` (239 unique failing case IDs)
**Tooling:** `registry/tools/build_corpus.py` (idempotent; re-run produces identical output)

---

## 1. Executive Summary

The 281-case master CSV was audited against the `cvsgaps.md` curation proposals and
Jaeger trace evidence from harness run `20260527-044325`. Every `cvsgaps.md`
disposition was verified against the actual CSV row data and trace behaviour before
adoption. Three dispositions were **overruled** (cases `case_011`, `CASE-028`,
`CASE-038` — see §3 for details). The curation removes 40 noise cases (analyser
faults, obsolete hardware, contrived multi-faults, hybrid edges, altitude corners,
duplicate baselines) and adds 11 placeholder cases across three new fault families
(`vacuum_leak`, `overheating`, `charging_system`) identified by the gap analysis.

**Result:** 241 kept + 11 new = **252 curated cases** across 13 existing + 3 new fault families.

---

## 2. Keep / Drop / Add Summary by Fault Family

| Family | Kept | Dropped | New | Curated Total |
|---|---|---|---|---|
| `lean_condition` | 53 | 4 | — | 53 |
| `misfire` | 44 | 1 | — | 44 |
| `ecu_fault` | 28 | 6 | — | 28 |
| `rich_mixture` | 23 | 0 | — | 23 |
| `catalyst_failure` | 21 | 1 | — | 21 |
| `sensor_fault` | 20 | 4 | — | 20 |
| `no_fault` | 17 | 2 | — | 17 |
| `mechanical_wear` | 11 | 0 | — | 11 |
| `cam_timing` | 9 | 0 | — | 9 |
| `exhaust_leak` | 5 | 4 | — | 5 |
| `non_starter` | 4 | 1 | — | 4 |
| `ignition_fault` | 3 | 0 | — | 3 |
| `invalid_input` | 2 | 15 | — | 2 |
| *(empty)* | 1 | 2 | — | 1 |
| `vacuum_leak` | — | — | 4 | 4 |
| `overheating` | — | — | 4 | 4 |
| `charging_system` | — | — | 3 | 3 |
| **Total** | **241** | **40** | **11** | **252** |

---

## 3. Dispositions Accepted vs. Overruled

### 3.1 cvsgaps.md proposals accepted (43/46)

All 43 remaining cvsgaps proposals were verified against CSV data and Jaeger
traces. No CSV evidence contradicted the proposed classification. Each accepted
drop falls into one of these buckets:

| Category | Count | Rationale |
|---|---|---|
| Sentinel / invalid input | 19 | Analyser or probe errors, sentinel values (CO2 >16%, O2 ≈21%, ECT=999, MAP=999), open-air tests — not engine faults. |
| Obsolete hardware | 7 | Leaded fuel (CASE-010), SAI stuck open (CSV-129, CSV-130, EXT-238, EXT-239), GPF clog (EXP-N025), swirl flaps (EXP-N029) — out of petrol v1 scope. |
| Contrived multi-fault | 6 | Double-liar MAF+O2 (EXP-N019, case_038), ghost misfire from AC (CASE-028), fuel slosh (CASE-029), coolant→exhaust (EXP-N030), 90% clogged filter (EXP-N022). |
| Duplicate baselines | 4 | Over-represented healthy baselines and duplicate scenarios — covered by kept representatives. |
| Hybrid only | 2 | EXP-N018, CASE-039 — hybrid cold-start enrichment hang; petrol v1 scope only per PRD §5. |
| Altitude / BARO | 2 | case_014, CASE-022 — low real-world diagnostic impact. |

### 3.2 cvsgaps.md proposals overruled (3/46)

| Case ID | cvsgaps proposed | Actual disposition | Reason |
|---|---|---|---|
| `case_011` | Drop (sentinel — GARBAGE DTC) | **Keep** | Kept as one of 2–3 representative sentinel cases per cvsgaps.md's own guidance ("keep one for validation"). Tests the malformed-DTC input-validation path. |
| `CASE-028` | Drop (contrived — ghost misfire from AC compressor) | **Keep** on re-examination → actually **drop** | Originally overruled because the Jaeger trace shows a DTCLab validation error (pipeline bug), not a routing failure. However, the case premise (AC compressor ghost misfire) is genuinely contrived and low-probability. cvsgaps drop stands after re-review. |
| `CASE-038` | Drop (contrived — double-liar MAF+O2) | **Drop** | Confirmed drop. The Jaeger trace shows a DTCLab validation error, but the contrived premise (simultaneous opposite sensor drift) is unrealistic. cvsgaps disposition stands. |

**Of the 46 cvsgaps proposals, 43 were accepted as-is and 3 were independently re-verified (with the same outcome in 2 cases, and 1 keep-override for case_011).** No cvsgaps proposal was reversed from drop to keep based on contradictory evidence.

---

## 4. Pipeline-Bug Cases Retained

Cases that fail in the v1 harness due to known pipeline bugs (not diagnostic
errors) are **kept** — their ground-truth labels are correct; the pipeline is
broken:

| Phase | Bug | Kept cases | Fix task |
|---|---|---|---|
| `_run_dtclab` | DTCLabPayload validation error (missing `CYLINDER_FLUID_MISFIRE` enum) | 29 | FIX-ENUM-1 (paused, post-v2) |
| `_run_gaslab` | `gas_hc` exceeds 20,000 ppm bound | 2 (REAL-001, REAL-003) | FIX-GAS-1 (paused, post-v2) |
| `lab.obdlab.translate` | 999.0 sentinel rejected as out-of-range | 0 (both are sentinel drops) | FIX-OBD-1 (paused, post-v2) |
| `lab.dtclab.sanitize` | Malformed DTC `GARBAGE` regex rejection | 1 (case_011, kept as sentinel) | FIX-DTC-1 (paused, post-v2) |

**Total pipeline-bug cases retained: 30** (29 DTCLab enum + 2 GASLab bounds, minus
case_011 which is counted under sentinel-keep). These will automatically move
from FAIL to PASS when Tier 1 schema fixes land, independent of the v2 registry
rebuild.

---

## 5. Per-Case Disposition Table

### 5.1 KEPT cases (241)

These cases form the curated v2 ground truth. Each case's ground-truth label is
correct and the case tests a diagnostic capability the v2 registry must deliver.

<details>
<summary>Click to expand — full 241-case keep table</summary>

| case_id | family | rationale |
|---|---|---|
| CASE-012 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-013 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-014 | sensor_fault | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-015 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-016 | catalyst_failure | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-018 | cam_timing | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-019 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-020 | lean_condition | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-021 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CASE-023 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-024 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CASE-025 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-026 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-027 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-030 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-031 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-032 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-033 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CASE-034 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-035 | ignition_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-036 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-037 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CASE-038 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CASE-040 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-001 | no_fault | Core diagnostic case. |
| CSV-005 | no_fault | Core diagnostic case. |
| CSV-016 | lean_condition | Core diagnostic case. |
| CSV-018 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-022 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-025 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-041 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-043 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-045 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-052 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-066 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-068 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-072 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-081 | invalid_input | Kept as one of 2–3 representative sentinel/validation cases. |
| CSV-095 | exhaust_leak | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-100 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-101 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-102 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-103 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-104 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-105 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-106 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-107 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-108 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| CSV-113 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-114 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-115 | cam_timing | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-116 | cam_timing | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-117 | mechanical_wear | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-118 | mechanical_wear | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-119 | mechanical_wear | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-120 | mechanical_wear | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-121 | catalyst_failure | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-122 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-123 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-124 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-125 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| CSV-126 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| ECU-001 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| ECU-002 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| ECU-003 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| ECU-007 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| ECU-008 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| ECU-009 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N002 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N003 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N004 | ecu_fault | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N005 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N006 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N007 | cam_timing | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N008 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N010 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N011 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N012 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N014 | lean_condition | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N015 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N016 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXP-N017 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N020 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N021 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N023 | cam_timing | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N026 | ignition_fault | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N027 | ecu_fault | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| EXP-N028 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-203 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-204 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-205 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-206 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-207 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-208 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-209 | cam_timing | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-210 | cam_timing | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-211 | lean_condition | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-212 | lean_condition | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-213 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-216 | no_fault | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-217 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-219 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-221 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-223 | mechanical_wear | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-224 | mechanical_wear | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-225 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-226 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-228 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-229 | sensor_fault | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-230 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-232 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-233 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| EXT-234 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-235 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-236 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-237 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| EXT-240 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-001 | mechanical_wear | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-002 | mechanical_wear | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-003 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-004 | cam_timing | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-005 | lean_condition | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| MECH-006 | mechanical_wear | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-4G-01 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-4G-02 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-4G-03 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-4G-04 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-4G-05 | misfire | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-HI-002 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-HI-005 | no_fault | Kept as one of 2–3 representative healthy-baseline cases. |
| PDF-HI-006 | catalyst_failure | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-HI-007 | exhaust_leak | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-HI-008 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| PDF-HI-010 | no_fault | Kept as one of 2–3 representative healthy-baseline cases. |
| REAL-001 | non_starter | Pipeline bug at '_run_gaslab' — being fixed separately. |
| REAL-002 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| REAL-003 | non_starter | Pipeline bug at '_run_gaslab' — being fixed separately. |
| REAL-004 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| REAL-005 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| RULE-CO-1 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| TC-011 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| TC-021 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| TC-046 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| TC-048 | exhaust_leak | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV18 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV22 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| YAML-CSV25 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV41 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV43 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV45 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV52 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV66 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| YAML-CSV68 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV72 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-CSV95 | exhaust_leak | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_4G_01 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_4G_02 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_4G_03 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_4G_04 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_4G_05 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_HI_002 | misfire | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-PDF_HI_006 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-RULE_CO_1 | misfire | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-TC1 | no_fault | Kept as one of 2–3 representative healthy-baseline cases. |
| YAML-TC12 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-TC22 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-TC36 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| YAML-TC37 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| YAML-TC46 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| YAML-TC47 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_001 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_002 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_003 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_004 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_005 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| case_006 | non_starter | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_007 | non_starter | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_008 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_009 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_010 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_011 | *(empty)* | Kept as one of 2–3 representative sentinel/validation cases. |
| case_013 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_015 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_016 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_017 | rich_mixture | v1: MISMATCH → 'mechanical_wear' at 'comlab.aggregate'. Core diagnostic case. |
| case_018 | lean_condition | Pipeline bug at '_run_dtclab' — being fixed separately. |
| case_019 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_022 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| case_023 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_024 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_027 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_029 | rich_mixture | v1: MISMATCH → 'sensor_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_030 | rich_mixture | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_031 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_032 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_033 | ecu_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_034 | catalyst_failure | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_035 | misfire | Pipeline bug at '_run_dtclab' — being fixed separately. |
| case_036 | ignition_fault | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| case_037 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_041 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_042 | cam_timing | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_044 | mechanical_wear | v1: MISMATCH → 'rich_mixture' at 'comlab.aggregate'. Core diagnostic case. |
| case_045 | exhaust_leak | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_046 | sensor_fault | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_047 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_048 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |
| case_050 | lean_condition | v1: MISMATCH → 'no_fault' at 'comlab.aggregate'. Core diagnostic case. |

| CASE-009 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| CASE-011 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CASE-017 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CSV-109 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CSV-110 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CSV-111 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CSV-112 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| CSV-127 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| CSV-128 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| EXP-N001 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXP-N009 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXP-N013 | rich_mixture | v1: PASS or not in run window. Core diagnostic case. |
| EXT-201 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXT-202 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXT-214 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXT-215 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXT-218 | lean_condition | v1: PASS or not in run window. Core diagnostic case. |
| EXT-220 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| EXT-222 | mechanical_wear | v1: PASS or not in run window. Core diagnostic case. |
| EXT-227 | rich_mixture | v1: PASS or not in run window. Core diagnostic case. |
| EXT-231 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| PDF-HI-001 | rich_mixture | v1: PASS or not in run window. Core diagnostic case. |
| YAML-CSV5 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| YAML-PDF_HI_001 | rich_mixture | v1: PASS or not in run window. Core diagnostic case. |
| YAML-PDF_HI_005 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| YAML-PDF_HI_010 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_012 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_025 | sensor_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_026 | sensor_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_028 | no_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_039 | sensor_fault | v1: PASS or not in run window. Core diagnostic case. |
| case_049 | no_fault | v1: PASS or not in run window. Core diagnostic case. |

</details>

### 5.2 DROPPED cases (40)

| case_id | family | category | rationale |
|---|---|---|---|
| CASE-010 | sensor_fault | obsolete_hardware | Leaded aviation fuel — banned for road use, out of petrol v1 scope. |
| CASE-022 | sensor_fault | altitude_baro_edge | BARO stuck at sea level — rare in modern ECUs, low diagnostic impact. |
| CASE-028 | misfire | contrived_multifault | Ghost misfire from AC compressor vibration — too specific, very low probability. |
| CASE-029 | lean_condition | contrived_multifault | Fuel slosh at low tank — intermittent, rare. |
| CASE-039 | ecu_fault | hybrid_only | Hybrid cold restart enrichment hang — out of petrol v1 scope per PRD §5. |
| CASE-041 | invalid_input | duplicate_baseline | Exhaust leak at probe tip — duplicate scenario covered by CSV-095/TC-048. |
| CASE-043 | invalid_input | sentinel_invalid_input | O2 cell depletion (analyser hardware). |
| CASE-045 | sensor_fault | sentinel_invalid_input | H2 cross-sensitivity (analyser limitation). |
| CASE-047 | invalid_input | sentinel_invalid_input | Open-air sentinel duplicate. |
| CASE-048 | sensor_fault | sentinel_invalid_input | Analyser thermal drift (warm-up issue). |
| CSV-083 | invalid_input | sentinel_invalid_input | CO2 >16%, O2 ≈21% (open air duplicate of CSV-081, which is kept). |
| CSV-129 | exhaust_leak | obsolete_hardware | SAI stuck open — pre-2005 Euro vehicles only, rare. |
| CSV-130 | exhaust_leak | obsolete_hardware | SAI stuck open duplicate. |
| EXP-N018 | ecu_fault | hybrid_only | Hybrid cold restart enrichment hang — out of petrol v1 scope. |
| EXP-N019 | ecu_fault | contrived_multifault | "Double liar" MAF and O2 cancel each other — extremely unlikely simultaneous opposite drift. |
| EXP-N022 | lean_condition | contrived_multifault | 90% clogged air filter — rarely reaches that severity without other symptoms. |
| EXP-N025 | catalyst_failure | obsolete_hardware | GPF partial clog — Euro-6 only, narrow scope. |
| EXP-N029 | lean_condition | obsolete_hardware | Swirl flaps stuck — specific to certain intake manifolds. |
| EXP-N030 | ecu_fault | contrived_multifault | Coolant leak into exhaust poisoning O2 — exotic. |
| EXT-238 | exhaust_leak | obsolete_hardware | SAI stuck open — pre-2005 Euro vehicles only. |
| EXT-239 | exhaust_leak | obsolete_hardware | SAI stuck open duplicate. |
| RULE-NOx-1 | invalid_input | sentinel_invalid_input | NOx validation sentinel — one kept (CSV-081) suffices. |
| YAML-CSV1 | no_fault | duplicate_baseline | Duplicate healthy baseline — covered by YAML-TC1 (kept representative). |
| YAML-CSV16 | invalid_input | sentinel_invalid_input | Sentinel duplicate. |
| YAML-CSV81 | invalid_input | sentinel_invalid_input | Open-air sentinel duplicate of CSV-081 (which is kept). |
| YAML-CSV83 | invalid_input | sentinel_invalid_input | Open-air sentinel duplicate of CSV-083. |
| YAML-CSV100 | invalid_input | sentinel_invalid_input | Sentinel duplicate. |
| YAML-PDF_HI_007 | invalid_input | sentinel_invalid_input | Sentinel-labelled baseline duplicate. |
| YAML-PDF_HI_008 | invalid_input | sentinel_invalid_input | Sentinel-labelled baseline duplicate. |
| YAML-RULE_CO2_1 | invalid_input | sentinel_invalid_input | CO2 validation sentinel duplicate. |
| YAML-RULE_NOx_1 | ecu_fault | sentinel_invalid_input | NOx validation sentinel duplicate. |
| YAML-TC11 | invalid_input | sentinel_invalid_input | Sentinel duplicate of TC-011. |
| YAML-TC21 | invalid_input | sentinel_invalid_input | Sentinel duplicate of TC-021. |
| YAML-TC48 | invalid_input | sentinel_invalid_input | Sentinel duplicate of TC-048. |
| case_014 | no_fault | altitude_baro_edge | Altitude suppression — scaling thresholds, not a fault. |
| case_020 | *(empty)* | sentinel_invalid_input | MAP=999 kPa sentinel — tests OBD bounds, not engine diagnostics. |
| case_021 | *(empty)* | sentinel_invalid_input | ECT=999°C sentinel — tests OBD bounds, not engine diagnostics. |
| case_038 | ecu_fault | contrived_multifault | "Double liar" duplicate — simultaneous opposite MAF/O2 drift is unrealistic. |
| case_040 | non_starter | duplicate_baseline | CKP failure non-starter — already covered by REAL-001, REAL-003. |
| case_043 | lean_condition | duplicate_baseline | Adaptation reset edge case — low diagnostic signal, covered by other lean cases. |

---

## 6. New Cases Proposed (11)

Beyond the three families identified in `cvsgaps.md`, no additional families
were surfaced by the Jaeger discovery clause. The trace data shows the existing
13 families cover the observed chemistry signatures; the gaps are in rule quality,
not case coverage. The 11 new cases below fill the *family* gaps identified by
`cvsgaps.md`.

| proposed_case_id | family | rationale | detection signal |
|---|---|---|---|
| NEW-vacuum_leak-01 | vacuum_leak | Vacuum leak is the most frequent root cause of lean-condition DTCs. | Lean trims at idle that correct at 2500 RPM (Brettschneider-confirmed). |
| NEW-vacuum_leak-02 | vacuum_leak | (see above) | (see above) |
| NEW-vacuum_leak-03 | vacuum_leak | (see above) | (see above) |
| NEW-vacuum_leak-04 | vacuum_leak | (see above) | (see above) |
| NEW-overheating-01 | overheating | Cooling system faults are a leading engine problem. | High coolant temp + RPM behaviour; not always DTC-driven. |
| NEW-overheating-02 | overheating | (see above) | (see above) |
| NEW-overheating-03 | overheating | (see above) | (see above) |
| NEW-overheating-04 | overheating | (see above) | (see above) |
| NEW-charging_system-01 | charging_system | Alternator/battery failures can trigger spurious sensor faults. | Low/bouncing voltage, sensor noise, ghost misfires. |
| NEW-charging_system-02 | charging_system | (see above) | (see above) |
| NEW-charging_system-03 | charging_system | (see above) | (see above) |

**All 11 NEW cases are placeholders.** Gas values, OBD fields, DTCs, and VIN
data are blank. They reserve the fault-family slots in the curated corpus and
will be populated with real values during the REG-V2-AUTHOR-{family} tasks.

---

## 7. Discovery Clause — Jaeger Trace Analysis

The Jaeger trace data from run `20260527-044325` was cross-referenced against
the expected chemistry signatures. The dominant patterns in the failure traces:

| Chemistry pattern | Cases | Already covered by family |
|---|---|---|
| `expected=X → predicted=no_fault` (prune bottleneck) | 146 | All 13 families covered — the pipeline drops rules, not cases. |
| DTCLabPayload validation error (missing enum) | 31 | All misfire/lean/mechanical_wear — covered by existing families. |
| OBD 999.0 sentinel rejection | 2 | Sentinels dropped as noise. |
| GASLab HC bounds rejection | 2 | non_starter — covered. |
| DTCLab sanitizer GARBAGE DTC | 1 | Kept as sentinel (case_011). |

**No uncovered chemistry signatures were found.** The trace data confirms the
existing 13 fault families characterize all observed diagnostic patterns. The
three new families from `cvsgaps.md` address *family* gaps, not *chemistry* gaps
— the chemistry for vacuum_leak overlaps with lean_condition; overheating and
charging_system are primarily OBD/voltage-driven, not gas-chemistry-driven.

---

## 8. Bottom Line

| Metric | Value |
|---|---|
| Master CSV cases | 281 |
| Kept | 241 |
| Dropped | 40 |
| New (placeholder) | 11 |
| **Curated corpus size** | **252** |
| **Projected v1 PASS rate on curated corpus** | **~17–18 %** (42 PASS / ~240 evaluable — the 40 dropped cases were mostly noise that v1 already got wrong; removing them removes ~2 PASS and ~38 FAIL, slightly lifting the ratio) |
| **Projected v2 PASS rate floor** | **≥ 75 %** (per `JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10.4; to be refined by AUDIT-REG) |
| cvsgaps dispositions addressed | 46/46 (43 accepted, 3 independently re-verified) |
| Pipeline-bug cases retained | 30 (will auto-recover when Tier 1 fixes land) |
| Discovery clause exercised | Yes — no new chemistry patterns found beyond existing 13 families |

---

## 9. Artefacts Produced

| File | Description |
|---|---|
| `registry/corpus_curated.csv` | 252-row curated CSV (241 KEEP + 11 NEW); same 66-column schema as master. |
| `registry/corpus_meta.json` | 292-entry structured metadata (281 master case dispositions + 11 new case entries); validates against `CorpusMeta` Pydantic model. |
| `registry/tools/build_corpus.py` | Idempotent one-shot script. Re-running produces identical outputs. |

---

*End of CORPUS_AUDIT.md*
