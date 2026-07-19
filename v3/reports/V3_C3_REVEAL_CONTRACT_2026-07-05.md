# V3_C3_REVEAL_CONTRACT_2026-07-05

**Task:** `T-V3-P4-C3-PRE`  **Mode:** DISCLOSE only (read-only pre-author)
**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no
**Machine-readable twin:** `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json`
(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c3_contract.py`).

This document instances the **frozen reveal contract** for **C3 — ECU/control-system
fault**, the next pack in the pinned sequence (C2 → **C3** → C6 → C5 → C4 → …).
It builds nothing and scores nothing; it fixes *how* the C3 pack discloses.

---

## 0. Baseline pin

| Artefact | Pinned value |
| --- | --- |
| Yardstick | `V3_YARDSTICK_2026-07-05` |
| CSV SHA-256 | `3df2e8cbd82a866c3b8f12a72fdee837ac35cc1f09a19db65a10baa499282ddc` |
| Oracle subset SHA-256 | `3088a7c3…` (unchanged) |
| Scorer | `apps/wired/v7/run_suite.py` (hash-locked, untouched) |
| Named run | `POST_T_V3_P4_C2B` |
| Run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json` |

All sizing in this pack references THIS baseline. The C4A dry-run predates C2B
and is known-stale — do not copy its numbers.

---

## 1. The reveal contract (cluster-agnostic template — instanced, not re-derived)

| Section | Definition |
| --- | --- |
| **BUILDABLE_NOW** | Producer/consumer logic + thresholds derivable from the cluster research answer; provable by unit tests on synthetic vectors, with no owner data. |
| **SCORING_GATED** | The per-case owner columns still required and which residual `case_id`s each unlocks; stays abstained until the owner supplies real measured values (no synthetic stand-in). |
| **CODE_LANDED != SCORE_MOVED** | Explicit separation of "producer/consumer logic shipped" from "`top3_family` delta." Landing code proves the discriminator is wired; it does NOT move the score until gated data arrives. Never report the first as the second. |
| **REGRESSION / FT-8** | The neighbour set the consumer edit touches (rules in the same family file + shared `competition_group` + their `passes_cases`), plus the no-regressed-family audit run on the full corpus at commit time. |
| **ABSTAIN_FALLBACK** | Cases whose discriminating signal the owner cannot supply stay abstained (MARGIN=0.02 dial), never guessed from the idle snapshot. |

---

## 2. C3 producer extraction (cited to `cluster3_prepped.md`)

The C3 producer is one state — **OBDLab `ControlPlausibilityState`**. It emits
`CONTROL_REFERENCE_FAULT` when electrical/reference or gas-vs-OBD divergence
gates pass. The emit thresholds, transcribed read-only from the research answer:

| Signal | Maneuver | Threshold | Verdict | Producer state | Grounding | Cite (`cluster3_prepped.md`) |
| --- | --- | --- | --- | --- | --- | --- |
| Gas-to-OBD Divergence (Δλ) | Warm engine idle (750 RPM), 60 s closed-loop window | **Δλ = \|λ_OBD − λ_tailpipe\| ≥ 0.05** | `CONTROL_REFERENCE_FAULT` (gas-vs-OBD disagree) | OBDLab ControlPlausibilityState | **empirical-anecdotal** | §Quantitative Diagnostic Signature Mapping line 183 |
| Adaptive Fuel Trim Limits (LTFT railed) | Dynamic cruise (1500–2500 RPM) | **LTFT ≥ +25% or ≤ −25%** with un-correlated tailpipe chemistry | `CONTROL_REFERENCE_FAULT` (trims at correction limit) | OBDLab ControlPlausibilityState | manufacturer-typical | §Quantitative Diagnostic Signature Mapping line 184 |
| KOEO MAP-vs-BARO Correlation | KOEO (0 RPM), ignition ON | **\|P_MAP − P_BARO\| ≥ 5 kPa** | `CONTROL_REFERENCE_FAULT` (static pressure split) | OBDLab ControlPlausibilityState | manufacturer-typical | §Quantitative Diagnostic Signature Mapping line 185 |
| DLC Signal Ground drop | Idle under high electrical load | **ΔV_gnd > 0.20 V** | `CONTROL_REFERENCE_FAULT` (ground offset) | OBDLab ControlPlausibilityState | **standardized** | §Quantitative Diagnostic Signature Mapping line 186 |
| Ground Path Voltage Drop | Idle under high electrical load | **ΔV > 0.10 V** (ground joint) or **> 0.20 V** (wire/cable) | `CONTROL_REFERENCE_FAULT` (chassis/engine ground degradation) | OBDLab ControlPlausibilityState | **standardized** | §Quantitative Diagnostic Signature Mapping line 187 |
| Active Overrides Response | Bidirectional fuel override at idle (+25% / −12.5%) | **O2 voltage delta < 0.1 V** under ±25% fuel command steps | `CONTROL_REFERENCE_FAULT` (sensor unresponsive to fuel command) | OBDLab ControlPlausibilityState | manufacturer-typical | §Quantitative Diagnostic Signature Mapping line 188 |

**Producer emit summary (what C3-SYNTH seeds, C3A simulates, C3B commits):**
the ControlPlausibilityState emits `CONTROL_REFERENCE_FAULT` when ANY of the
above thresholds fires — each is an independent gate. The corpus columns are:
`koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v,
gas_obd_lambda_delta, lambda_perception_delta, bidirectional_fuel_response_ok_bool`.

> **Producer-tuning risk flagged:** the gas-vs-OBD divergence threshold
> (`Δλ ≥ 0.05`) is **empirical-anecdotal** — it is not a standardized OEM
> constant and should be confirmed against real vehicle data before committing.
> The voltage-drop thresholds (0.10 V / 0.20 V) are standardized DMM
> conventions. The ±25% trim limit is manufacturer-typical but not universal.
> The bidirectional response threshold (< 0.1 V) is manufacturer-typical.

---

## 3. C3 consumer mapping (named; no edit)

| Family file | Rules | Field each reads today | What the C3 state would supply |
| --- | --- | --- | --- |
| `ecu_fault.json` | **EF-001 / EF-002 / EF-003** | `obd_evidence` `longft1`/`shrtft1` (trim saturation); `dtc_evidence` ECU-fault DTCs | The `CONTROL_REFERENCE_FAULT` producer state supplies the gas-vs-OBD divergence, ground voltage, and MAP/BARO delta that these rules currently lack — they fire only on trim saturation + DTC pattern. |
| `sensor_fault.json` | **SF-001 / SF-002** | `obd_evidence` `lambda_perception_delta`, `o2_voltage`; perception flags `O2_SENSOR_BIASED_HIGH` / `O2_SENSOR_BIASED_LOW` | The C3 state gates SF-001/SF-002 for cases where ECU control dispersion *presents* as sensor bias — separates a true lazy/biased O2 sensor from an ECU ground-offset that merely *looks* like sensor bias. |

This is the mapping the **commit** (`C3B`) will make. Nothing is edited here.

---

## 4. C3 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 22)

**BUILDABLE_NOW-reachable by logic alone: 0** (expected — say so). Every C3 case
is residual precisely because its discriminating column (KOEO pressure, ground
voltage, gas-vs-OBD divergence, bidirectional response) is absent from the corpus;
logic without values cannot move it.

**SCORING_GATED: 22 / 22**, split by residual bucket:

- **OUTRANKED_HARD = 18:** CSV-041, CSV-045, CSV-123, CSV-124, ECU-001, ECU-009,
  EXP-N002, EXP-N004, EXP-N005, EXP-N018, EXP-N019, EXT-221, TC-021,
  YAML-CSV41, YAML-CSV45, YAML-TC47, case_001, case_013.
- **PRODUCER_GAP_SIGNAL_REQUIRED = 3:** CSV-125, CSV-126, YAML-RULE_NOx_1.
- **CLASSIFIER_FIXABLE_REROUTED = 1:** CASE-039 (rerouted from
  CLASSIFIER_FIXABLE by T-V3-P4-0A; broad EGR/POA neighbour risk prevents a
  safe classifier fix — honest path is ECU/control signal).

Every one requires the columns `koeo_map_baro_delta_kpa, module_voltage_loaded_v,
dlc_signal_ground_drop_v, gas_obd_lambda_delta, lambda_perception_delta,
bidirectional_fuel_response_ok_bool`. **18 + 3 + 1 = 22.** ✔

**CODE_LANDED != SCORE_MOVED, stated for C3:** the producer emit rule and consumer
wiring above are BUILDABLE_NOW from `cluster3_prepped.md` and unit-testable on
synthetic control-plausibility vectors — that is *code landed*. Any `top3_family`
delta on these 22 (*score moved*) is **unobservable until the owner supplies real
values**. A pack report must never present the first as the second.

---

## 5. REGRESSION / FT-8 neighbour set (derived live from the two rule files)

A C3 consumer edit touches the `ecu_fault` and `sensor_fault` family files —
both `competition_group`s. The commit must re-audit every case those rules
currently pass for a regressed family. Union of `passes_cases` across all 5 EF +
8 SF rules = **48 cases**:

```
CASE-014, CSV-025, CSV-041, CSV-043, CSV-045, CSV-072, CSV-123, CSV-124,
CSV-125, CSV-126, ECU-001, ECU-002, ECU-003, ECU-009, EXP-N002, EXP-N004,
EXP-N005, EXP-N006, EXP-N015, EXP-N020, EXP-N027, EXP-N028, EXT-219,
EXT-221, EXT-229, EXT-230, TC-021, TC-046, YAML-CSV25, YAML-CSV41,
YAML-CSV43, YAML-CSV45, YAML-CSV72, YAML-TC22, YAML-TC46, YAML-TC47,
case_001, case_004, case_009, case_013, case_025, case_026, case_027,
case_033, case_037, case_039, case_041, case_046
```

**Shared-neighbour caveat (named now):** many of these are already-passing
non-C3 cases inside the same competition groups. **18 cases are BOTH C3 targets
and regression-sensitive neighbours** — they appear in both the C3 target set and
the `passes_cases` union:

```
CSV-041, CSV-045, CSV-123, CSV-124, CSV-125, CSV-126, ECU-001, ECU-009,
EXP-N002, EXP-N004, EXP-N005, EXT-221, TC-021, YAML-CSV41, YAML-CSV45,
YAML-TC47, case_001, case_013
```

A C3 gate that tightens or re-weights EF/SF rules could regress the 30 non-target
neighbours — so FT-8 in `C3A`/`C3B` must run the **full corpus** and show
**no regressed family**, not just re-check the 22 targets.

Note the 4 C3 target cases NOT in the neighbour set (EXP-N018, EXP-N019,
EXT-221, CASE-039) — EXP-N018 and EXP-N019 have EF-003 as expected rule but are
outranked; EXT-221 appears above (it IS in the set); CASE-039 was rerouted from
classifier-fixable and has no EF/SF rule passing it currently.

---

## 6. Confounder disclosure (C3)

**Source:** `cluster3_prepped.md` §Conditions Under Which Signatures May Fail.

The C3 gas-vs-OBD divergence discriminator can produce **false negatives** (miss a
real control fault) when the vehicle has a co-existing physical fault that
independently shifts the exhaust chemistry:

| Confounder | Mechanism | Mimic risk for C3 |
| --- | --- | --- |
| **Upstream exhaust system leaks** | Outside air drawn in causes excess O2 at the sensor; both tailpipe gas and OBD trims agree on lean — no gas-vs-OBD divergence. The Δλ test fails to trigger. | A real ECU ground offset would be masked if the same vehicle also has an exhaust leak. |
| **Severe cylinder misfires** | The misfiring cylinder pumps raw O2 and unburned fuel; the sensor drops, ECU drives trims positive. Tailpipe shows high O2 + elevated HC — can mimic a sensor bias fault. | A real ECU fault producing the *same* trim pattern as a misfire would be indistinguishable from the misfire confounder. |

**Per-case mimic risk:** All 22 C3 cases have `expected_family = ecu_fault`. None of
the 22 have `predicted_family` = `exhaust_leak` or `misfire` — so the *current* engine
routing does not suggest a co-existing physical confounder. However, the structural
mimic risk means C3-SYNTH should flag any case where the oracle fault description
suggests physical exhaust-stream contamination rather than a pure ECU/wiring fault, and
mark those as stay-abstained candidates.

---

## 7. Grounding-strength table per threshold

| Signal | Threshold | Grounding | Feasibility Tier | Risk note |
| --- | --- | --- | --- | --- |
| Gas-to-OBD Divergence (Δλ) | Δλ ≥ 0.05 | **empirical-anecdotal** | Tier B: 5-gas analyzer | **PRODUCER-TUNING RISK** — not a standardized/OEM constant; confirm against real data |
| Adaptive Fuel Trim Limits | LTFT ≥ +25% or ≤ −25% | manufacturer-typical | Tier A: Generic OBD-II | Well-grounded |
| KOEO MAP-vs-BARO Correlation | \|P_MAP − P_BARO\| ≥ 5 kPa | manufacturer-typical | Tier A: Generic OBD-II | Well-grounded |
| DLC Signal Ground drop | ΔV_gnd > 0.20 V | **standardized** | Tier C: DMM / breakout box | Well-grounded |
| Ground Path Voltage Drop | ΔV > 0.10 V / > 0.20 V | **standardized** | Tier C: DMM | Well-grounded |
| Active Overrides Response | O2 delta < 0.1 V under ±25% steps | manufacturer-typical | Tier C: Bidirectional scan tool | Well-grounded |

**Weakest-grounded threshold:** Δλ ≥ 0.05 (empirical-anecdotal). This is the primary
mathematical discriminator for C3 and its grounding comes from practitioner experience,
not from a published OEM specification or SAE standard. It is a producer-tuning
parameter — not a firm constant. C3-SYNTH must tag it as anecdotal and C3A must size
the commit around tolerance for this threshold drifting.

---

## 8. ABSTAIN_FALLBACK (C3)

If no KOEO plausibility or voltage/divergence data are supplied for a case, it
**stays abstained** at the current dial (MARGIN=0.02); a single warm-idle gas
snapshot cannot separate ECU/control faults from true chemistry deviations.
Cases the owner cannot measure are never guessed.

---

## Provenance / guardrails

- Read-only: no corpus column added, no producer/consumer wired, no rule/weight
  edit, no re-score, no yardstick mint, no synthesized values, no abstain-dial
  change (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No
  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Sources: `v3/research/research_answers/cluster3_prepped.md`;
  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C3;
  `labs/comlab/registry/rules/ecu_fault.json`, `sensor_fault.json` (query
  only); governs `v3/v3_tasks/T-V3-P4-C3-SYNTH_seed_data.md` (+ forthcoming
  `C3A`/`C3B`) and every later cluster pair.
