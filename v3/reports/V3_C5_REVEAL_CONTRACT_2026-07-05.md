# V3_C5_REVEAL_CONTRACT_2026-07-05

**Task:** `T-V3-P4-C5-PRE`  **Mode:** DISCLOSE only (read-only pre-author)
**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no
**Machine-readable twin:** `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json`
(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c5_contract.py`).

This document instances the frozen reveal contract for **C5 — lean-condition root cause**,
the next pack in the pinned sequence (C2 → C3 → C6 → **C5** → C4 → …).
It builds nothing and scores nothing; it fixes how C5 discloses thresholds, consumers,
C6 collision, C3 interaction, FT-8 exposure, column audit, and stay-abstained cases.

---

## 0. Baseline pin

| Artefact | Pinned value |
| --- | --- |
| Yardstick | `V3_YARDSTICK_2026-07-05-C6B` |
| CSV SHA-256 | `bf7393688230caf7f15054cc2473343e26351aa72c4615ca83044c7eb12fc0de` |
| Oracle subset SHA-256 | `3088a7c3…` (unchanged) |
| Scorer | `apps/wired/v7/run_suite.py (hash-locked, untouched)` |
| Named run | `POST_T_V3_P4_C6B` |
| Run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json` |

All C5 sizing references this current post-C6B baseline. If any commit lands first, stop and re-pin before C5-SYNTH/C5A.

---

## 1. The reveal contract (cluster-agnostic template — instanced, not re-derived)

| Section | Definition |
| --- | --- |
| **BUILDABLE_NOW** | Producer/consumer logic + thresholds derivable from the cluster research answer; provable by unit tests on synthetic vectors, with no owner data. |
| **SCORING_GATED** | The per-case owner columns still required and which residual case_ids each unlocks; stays abstained until the owner supplies real measured values. |
| **CODE_LANDED_NEQ_SCORE_MOVED** | Explicit separation of producer/consumer logic shipped from top3_family delta. Landing code proves the discriminator is wired; it does not move score until gated data exists. |
| **REGRESSION_FT8** | The neighbour set the consumer edit touches, plus the no-regressed-family audit run on the full corpus at commit time. |
| **ABSTAIN_FALLBACK** | Cases whose discriminating signal the owner cannot supply stay abstained at MARGIN=0.02, never guessed from static idle data. |

---

## 2. C5 producer extraction (cited to `cluster5.md`)

The C5 producer is **OBDLab `LeanRootCauseState`**. It emits
`VACUUM_LEAK_TRIM_PATTERN`, `FUEL_DELIVERY_SHORTFALL`, `MAF_UNDERREAD`, or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.
The emit thresholds, transcribed read-only from the research answer:

| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |
| --- | --- | --- | --- | --- | --- | --- |
| Total fuel trim delta (ΔTFT) between idle and 2500 RPM | Stationary stabilized idle (Maneuver A) transitioning to free-rev mid-RPM hold (Maneuver B) | Positive trims at idle (e.g. TFT >= +15%) that recover by >= 15% at 2500 RPM (e.g. TFT <= +10%) | `VACUUM_LEAK_TRIM_PATTERN` | `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct` | empirical (direction strong; numeric values provisional) | cluster5.md §Signal Evaluation and Discriminative Ranking lines 127-129; §Quantitative Expected Signatures and Decision Matrix lines 155-156 |
| Fuel rail pressure drop and wide-range lambda under WOT | Wide-Open Throttle (WOT) acceleration sweep (Maneuver C) under high load | Fuel rail pressure drop of > 5 psi (35 kPa) below OEM spec, accompanied by wide-range lambda lambda > 1.05 (failure to enrich) | `FUEL_DELIVERY_SHORTFALL` | `fuel_rail_pressure_load_kpa, wideband_lambda_wot` | manufacturer-typical (for 35 kPa drop) / standardized (for lambda > 1.05) | cluster5.md §Signal Evaluation and Discriminative Ranking lines 135-137, 139-141; §Quantitative Expected Signatures and Decision Matrix lines 158-159 |
| Calculated engine load at peak WOT, with positive trims | Wide-Open Throttle (WOT) acceleration sweep (Maneuver C) up to upshift point | Calculated engine load failing to reach OEM typical bounds (Peak Load < 80%) under WOT, while trims run positive | `MAF_UNDERREAD` | `calc_load_wot_pct, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, stft_load_pct, ltft_load_pct` | manufacturer-typical / empirical-inferred | cluster5.md §Signal Evaluation and Discriminative Ranking lines 131-133; §Quantitative Expected Signatures and Decision Matrix line 157; Bottom Line Diagnostic Recommendation line 166 |
| Static-only or idle-only trim evidence | Stationary idle only; absent Maneuver B/C dynamic evidence | Reject static/idle-only trims as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `absence of decisive dynamic 2500 RPM / WOT load / pressure evidence` | physics/regulatory rationale (dynamic multi-point data required) | cluster5.md §Bottom Line Diagnostic Recommendation line 166; V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C5.6 line 53 |

**Producer emit summary:** `VACUUM_LEAK_TRIM_PATTERN` requires positive trims at idle
that recover at 2500 RPM; `FUEL_DELIVERY_SHORTFALL` requires rail pressure drop > 35 kPa
and wide-range lambda > 1.05 under WOT; `MAF_UNDERREAD` requires suppressed peak WOT load < 80%
accompanied by positive trims; static-only trims produce `SENSOR_HEALTH_UNPROVEN_ABSTAIN`,
not a guessed pass/fail.

**Load-bearing subset to size in C5A:** The trims and MAF g/s columns already exist. The genuinely new
columns are load/pressure/lambda at WOT. C5A dry-run must size whether the full column set is load-bearing.

---

## 3. C5 consumer mapping (named; no edit)

| Family file | Rules | Field each would read | What the C5 state supplies |
| --- | --- | --- | --- |
| `lean_condition.json` | **LC-001 / LC-002 / LC-003** | Trims, MAP, MAF g/s. Gated on C5 state output in C5B. | Lean-condition sub-cause state overrides: VACUUM_LEAK_TRIM_PATTERN or MAF_UNDERREAD. |
| `vacuum_leak.json` | **VL-001 / VL-002 / VL-003** | Trims, MAP directly. Gated on C5 state output in C5B. | Optional sub-cause gating. (No active cases expect vacuum_leak). |
| `exhaust_leak.json` | **EL-001** | Trims and DTCs. Reads shared trims. | Used in C4 later to separate exhaust leak from true lean. |

Nothing is edited here. The consumer map is for C5-SYNTH/C5A/C5B inheritance.

---

## 4. C6-MAF-COLLISION & C3-INTERACTION DISCLOSURE (mandatory)

### C6-MAF-COLLISION

- **Collision description:** C6's SensorDynamicsState and C5's LeanRootCauseState can both emit a MAF-underread verdict from the same MAF columns, but attribute it to different families (sensor_fault vs lean_condition).
- **Populations today:** Disjoint: 14 C6 rows vs 10 C5 rows in the current corpus.
- **Disambiguation rule:** C6's sensor-attribution requires its Mode $06/dynamics evidence; C5's requires the trim+load pattern; neither fires on MAF delta alone. When both are present, C5's lean root cause takes precedence over C6's sensor-fault boost to prevent a lean-condition MAF drift from being misclassified as a sensor fault.
- **Integration location:** Lands in integration_shim.py::_score_rule (around lines 608-662), evaluated after the C3 and C6 branches. C5 must prune/suppress C6's sensor-fault boost if the C5 WOT load suppression pattern is present.

### C3-INTERACTION

The live C3B shim now has a control-reference state and a prune/boost branch:

- Producer: `integration_shim.py::_control_plausibility_state lines 540-557` returns `CONTROL_REFERENCE_FAULT` from KOEO MAP/BARO, ground drop, and loaded-voltage gates.
- Effect: integration_shim.py::_score_rule lines 562-569 boosts EF-001/002/003 by +0.10 and prunes SF-001/SF-002 when CONTROL_REFERENCE_FAULT is present.
- C5 future effect: C5 will boost lean_condition consumers (LC-001/LC-002/LC-003) based on LeanRootCauseState: VACUUM_LEAK_TRIM_PATTERN, FUEL_DELIVERY_SHORTFALL, or MAF_UNDERREAD.

**Composition / precedence rule C5B must implement:**
If a future row carries both C3 control-reference columns and C5 lean-condition columns, C3 control-reference pruning must run first. Static-only C5 evidence must preserve abstain/prune behavior to prevent control-reference faults from being misclassified as lean conditions.

---

## 5. ALREADY-LIVE-COLUMN AUDIT (mandatory)

- **Total required C5 columns:** 11
- **Already live in schema (6):** `ltft_2500_pct, ltft_idle_pct, maf_gps_2500, maf_gps_idle, stft_2500_pct, stft_idle_pct`
- **Genuinely new ask (5):** `calc_load_wot_pct, fuel_rail_pressure_load_kpa, ltft_load_pct, stft_load_pct, wideband_lambda_wot`

Of the 11 required C5 columns, 6 already exist in the live schema (4 trims from C2B, 2 MAF from C6B). The genuinely new ask is shrank to 5 columns. For C5 rows, the live columns exist in the schema but are currently empty/null.

---

## 6. C5 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 10)

**BUILDABLE_NOW-reachable by logic alone: 0**. Every C5 row is residual because
its trims/load/pressure discriminators are absent or incomplete on C5 rows in the live corpus;
logic without values cannot move `top3_family`.

**SCORING_GATED: 10 / 10**, split by residual bucket:

- **DATA_GAP_ACQUISITION_GAP = 5:** EXP-N011, EXP-N022, EXP-N029, case_003, case_016.
- **OUTRANKED_HARD = 4:** CSV-113, CSV-114, REAL-004, era1_001.
- **TUNABLE_HELD = 1:** era3_015.

**Oracle-fault mix:** `{'lean_condition': 10}`. **Current winner mix:** `{'catalyst_failure': 3, 'mechanical_wear': 1, 'misfire': 5, 'sensor_fault': 1}`.
All cases require C5 columns. **5 + 4 + 1 = 10.** ✔

**CODE_LANDED != SCORE_MOVED, stated for C5:** the LeanRootCauseState emit
logic and consumer map above are buildable from `cluster5.md`; any top3_family
delta is unobservable until C5-SYNTH/C5A provides values. A pack report must
never present wiring as score movement.

---

## 7. REGRESSION / FT-8 neighbour set (derived live)

A C5 consumer edit touches `lean_condition.json` and `vacuum_leak.json` — both
competition groups. The commit must re-audit every case those rules currently
pass for a regressed family. Union of `passes_cases` across all LC + VL rules
including the C3 lean-bias winners currently passing LC-001/LC-002 =
**68 cases**:

```
CASE-011, CASE-012, CASE-013, CASE-016, CASE-017, CASE-019, CASE-022, CASE-026, CASE-027, CASE-029, CASE-030, CASE-034, CASE-036, CSV-016, CSV-043, CSV-068, CSV-095, CSV-109, CSV-110, CSV-111, CSV-112, ECU-002, EXP-N001, EXP-N002, EXP-N004, EXP-N009, EXP-N011, EXP-N021, EXP-N025, EXP-N030, EXT-201, EXT-202, EXT-204, EXT-205, EXT-207, EXT-208, EXT-213, EXT-214, EXT-215, EXT-218, MECH-003, NEW-vacuum_leak-01, NEW-vacuum_leak-02, NEW-vacuum_leak-03, NEW-vacuum_leak-04, PDF-HI-007, REAL-002, TC-011, YAML-CSV43, YAML-CSV68, YAML-PDF_HI_007, YAML-TC22, case_001, case_003, case_019, case_031, case_032, case_050, era1_005, era1_007, era1_016, era1_018, era2_003, era2_014, era2_017, era3_002, era3_016, era3_019
```

**Dual target+neighbour cases (2):** EXP-N011, case_003.

**LC-regression exposure:** LC rules touch lean-condition cases. Vacuum leak and fuel shortfall rules have high overlap with other clusters (e.g., C3 control-reference lean-bias cases which are now-passing LC-001/LC-002, and C4 exhaust-leak lookalikes). A false boost that regresses these neighbours must be audited.

Rules derived live from the JSON files:

| Rule | Family | Competition group | passes_cases count |
| --- | --- | --- | --- |
| `LC-001` | `lean_condition` | `lean_condition` | 7 |
| `LC-002` | `lean_condition` | `lean_condition` | 3 |
| `LC-003` | `lean_condition` | `lean_condition` | 3 |
| `VL-001` | `vacuum_leak` | `vacuum_leak` | 2 |
| `VL-002` | `vacuum_leak` | `vacuum_leak` | 1 |
| `VL-003` | `vacuum_leak` | `vacuum_leak` | 1 |

---

## 8. Confounder disclosure (C5)

**Source:** `cluster5.md` §Technical Characterization / §Physical Mechanisms + acq-spec §C4.

| Confounder | Mechanism | Cite |
| --- | --- | --- |
| **Exhaust leak pre-O2 (false lean)** | Allows outside air to enter before the upstream O2 sensor via venturi effect, causing false lean lambda but normal engine load and trims. Separated by gas chemistry (high O2) or vacuum-leak/fuel-pressure verification. | cluster5.md §Technical Characterization of the Confusable Set line 37 |
| **Misfire (false lean)** | Unburned oxygen passes directly into the exhaust, causing false lean lambda. Separated by misfire codes (P0300-P0312) or Mode $06 misfire counts. | cluster5.md §Technical Characterization of the Confusable Set line 37 |
| **Speed-Density vs MAF architecture** | Naturally aspirated speed-density vehicles are immune to idle vacuum leak trims; turbocharged speed-density systems show negative trims under boost (boost leak). | cluster5.md §Physical and Thermodynamic Mechanisms of Fault Separation lines 77-83 |
| **C4 exhaust-leak / true-lean overlap** | C4 contains exhaust-leak/lean-condition/sensor-bias lookalikes that share these same C5 trim/load columns. C5-SYNTH must mark cases outside true-lean separability (confounders) as stay-abstained. | V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md lines 106-112 |

**Per-case mimic risk:** C5-SYNTH must use oracle-fault separability, not
current rank, to decide seed bands. `CSV-113, CSV-114, REAL-004, era1_001` are
EGR stuck open lookalikes, currently winning misfire (MF-001). C5-SYNTH must not
back-solve them without proper grounds. `era3_015` PCV pressure sensor drift is TUNABLE_HELD.

**C4 dependency:** C4 is not a new-column ask; its residuals consume the C5 trim/load columns and C6 dynamics columns. Landing C5 is a required prerequisite for C4B.

---

## 9. Grounding-strength table per threshold

| Signal | Threshold | Grounding | Feasibility Tier | Risk note |
| --- | --- | --- | --- | --- |
| Total fuel trim delta (ΔTFT) between idle and 2500 RPM | Positive trims at idle (e.g. TFT >= +15%) that recover by >= 15% at 2500 RPM (e.g. TFT <= +10%) | **empirical (direction strong; numeric values provisional)** | Tier A: generic OBD-II live trims | Direction is strong; local trims at idle recover at 2500, but exact delta % threshold is empirical. |
| Fuel rail pressure drop and wide-range lambda under WOT | Fuel rail pressure drop of > 5 psi (35 kPa) below OEM spec, accompanied by wide-range lambda lambda > 1.05 (failure to enrich) | **manufacturer-typical (for 35 kPa drop) / standardized (for lambda > 1.05)** | Tier A if sensor exposed; Tier C if mechanical gauge required | Pressure drop limit is typical for port-injection; DI rails have higher targets. WOT Load threshold may vary by altitude. |
| Calculated engine load at peak WOT, with positive trims | Calculated engine load failing to reach OEM typical bounds (Peak Load < 80%) under WOT, while trims run positive | **manufacturer-typical / empirical-inferred** | Tier A: generic OBD-II calculated load and trims | Pressure drop limit is typical for port-injection; DI rails have higher targets. WOT Load threshold may vary by altitude. |
| Static-only or idle-only trim evidence | Reject static/idle-only trims as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | **physics/regulatory rationale (dynamic multi-point data required)** | Abstain fallback | Static-only inputs are insufficient; abstain is the intended outcome. |

**Weakest-grounded threshold:** The fuel trim delta (ΔTFT) recovery threshold is empirical.
The Calculated Engine Load threshold (80%) and fuel pressure drop (35 kPa) are OEM-typical
and represent altitude / system pressure variance risks.

---

## 10. ABSTAIN_FALLBACK (C5)

If only static warm-idle trims are supplied, the case **stays abstained** at
MARGIN=0.02. C5 separates on dynamic multi-point data: idle vs 2500 trims, WOT load,
and WOT fuel pressure drop. One static idle point is not a discriminator.

---

## Provenance / guardrails

- Read-only: no corpus column added, no producer/consumer wired, no rule/weight
  edit, no yardstick mint, no synthesized values, no abstain-dial change
  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No
  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Sources: `v3/research/research_answers/cluster5.md`;
  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C5/§C4;
  `labs/comlab/registry/rules/lean_condition.json`, `vacuum_leak.json`;
  `labs/comlab/registry/integration_shim.py` lines 540-569 for C3 interaction.
- Governs `T-V3-P4-C5-PRE` → `T-V3-P4-C5-SYNTH` → `C5A` → `C5B`.
