# V3_C9_REVEAL_CONTRACT_2026-07-06

**Task:** `T-V3-P4-C9-PRE`  **Mode:** DISCLOSE only (read-only pre-author)
**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no
**Machine-readable twin:** `v3/reports/V3_C9_REVEAL_CONTRACT_2026-07-06.json`
(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c9_contract.py`).

This document instances the frozen reveal contract for **C9 — independent healthy-confirm**,
the next pack in the pinned sequence (C2 → C3 → C6 → C5 → C4 → **C9** → C8 → C1 → C7).
It builds nothing and scores nothing; it fixes how C9 discloses thresholds, consumers,
C6 interaction, C3 interaction, FT-8 exposure, column audit, and stay-abstained cases.

---

## 0. Baseline pin

| Artefact | Pinned value |
| --- | --- |
| Yardstick | `V3_YARDSTICK_2026-07-06-C5B` |
| CSV SHA-256 | `c49c17af1182a3eb07056a3fbf27c101378a32f35e375b18b3104d3928d8c7fd` |
| Oracle subset SHA-256 | `3088a7c3…` (unchanged) |
| Scorer | `apps/wired/v7/run_suite.py (hash-locked, untouched)` |
| Named run | `POST_T_V3_P4_C5B` |
| Run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json` |

All C9 sizing references this current post-C5B baseline. If any commit lands first, stop and re-pin before C9-SYNTH/C9A.

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

## 2. C9 producer extraction (cited to `cluster9.1.md` / `value9.md`)

The C9 producer is **OBDLab `HealthConfirmationState`**. It emits
`SYSTEM_HEALTH_CONFIRMED` or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.
The emit thresholds, transcribed read-only from the research answer:

| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |
| --- | --- | --- | --- | --- | --- | --- |
| OBD readiness monitor completeness | Read Mode $01 PID 0x01 | All supported non-continuous monitors = COMPLETE / READY | `SYSTEM_HEALTH_CONFIRMED gate` | `readiness_supported_complete_bool` | standardized (CARB/EPA) | cluster9.1.md §2; SAE J1979 |
| OBD emission-related DTC count | Read Mode $03, Mode $07, and Mode $0A (where supported) | Stored, pending, and permanent DTCs = 0 | `SYSTEM_HEALTH_CONFIRMED gate` | `stored_dtc_count, pending_dtc_count, permanent_dtc_count` | standardized (SAE J1979) | cluster9.1.md §2; SAE J1979 |
| OBD Mode $06 monitor test margins | Read Mode $06 test value and limit for non-continuous monitors | Test value must be inside limit with margin >= 10% of limit range | `SYSTEM_HEALTH_CONFIRMED gate` | `mode06_min_margin_pct` | standardized (regulatory cut) | value9.md §1; cluster9.1.md §2; SAE J1979 |
| OBD warm-up cycles since DTCs cleared | Read Mode $01 PID 0x30 / 0x4D | Warm-up cycles since clear >= 5 | `SYSTEM_HEALTH_CONFIRMED gate` | `warmup_cycles_since_clear` | standardized (EPA/CARB) | value9.md §1; EPA/CARB |
| OBD distance traveled since DTCs cleared | Read Mode $01 PID 0x31 / 0x4E | Distance since clear >= 200 miles | `SYSTEM_HEALTH_CONFIRMED gate` | `miles_since_clear` | standardized (CARB) | value9.md §1; CARB |
| Short-Term Fuel Trim (STFT) | Warm idle and steady 2500 RPM no load | STFT within +/-5% (P10-P90: -4% to +4%) | `SYSTEM_HEALTH_CONFIRMED gate` | `stft_idle_pct, stft_2500_pct` | standardized (OEM/SAE J1979) | value9.md §1; SAE J1979 |
| Long-Term Fuel Trim (LTFT) | Warm idle and steady 2500 RPM no load | LTFT within +/-7% (P10-P90: -6% to +6%) | `SYSTEM_HEALTH_CONFIRMED gate` | `ltft_idle_pct, ltft_2500_pct` | standardized (OEM/SAE J1979) | value9.md §1 (WIDEN); SAE J1979 |
| Fuel trim delta between idle and 2500 RPM | Transition from idle to 2500 RPM | Delta of fuel trim <= +/-5% | `SYSTEM_HEALTH_CONFIRMED gate` | `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct` | manufacturer-typical | value9.md §1; Workshop practice |
| Two-point gas delta: HC | Two-point tailpipe gas capture (idle to 2500 RPM no load) | Delta HC within -10 to +15 ppm | `SYSTEM_HEALTH_CONFIRMED gate` | `gas_delta_hc_ppm` | anecdotal / workshop norm | value9.md §1 (TIGHTEN); EPA/BAR |
| Two-point gas delta: CO | Two-point tailpipe gas capture (idle to 2500 RPM no load) | Delta CO within -0.15 to +0.15% | `SYSTEM_HEALTH_CONFIRMED gate` | `gas_delta_co_pct` | anecdotal / workshop norm | value9.md §1 (TIGHTEN); EPA/BAR |
| Two-point gas delta: CO2 | Two-point tailpipe gas capture (idle to 2500 RPM no load) | Delta CO2 typically positive, within +0.3 to +0.8% | `SYSTEM_HEALTH_CONFIRMED gate` | `gas_delta_co2_pct` | anecdotal / workshop norm | value9.md §1 (SHIFT); EPA/BAR |
| Two-point gas delta: O2 | Two-point tailpipe gas capture (idle to 2500 RPM no load) | Delta O2 within -0.5 to +0.4% | `SYSTEM_HEALTH_CONFIRMED gate` | `gas_delta_o2_pct` | anecdotal / workshop norm | value9.md §1; EPA/BAR |
| Unsupported, incomplete, or marginal OBD health evidence | Any operating state | Any gate check fails or is missing; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `absence of complete OBD/trim/gas-delta confirmation` | physics/regulatory rationale (provenance required) | cluster9.1.md §Bottom Line; V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C9.6 line 67 |

**Producer emit summary:** `SYSTEM_HEALTH_CONFIRMED` requires all supported monitors to be complete,
no DTCs of any type (stored, pending, permanent), Mode $06 margins >= 10%, trims within +/-7% and stable,
and 2-point gas deltas stable. Any deviation, incomplete status, or fresh OBD clear (warm-ups < 5, miles < 200)
produces `SENSOR_HEALTH_UNPROVEN_ABSTAIN` to prevent false-healthy diagnostic leaks.

---

## 3. C9 consumer mapping (named; no edit)

| Family file | Rules | Field each would read | What the C9 state supplies |
| --- | --- | --- | --- |
| `no_fault.json` | **NF-001 / NF-002** | Readiness, DTCs, Mode $06, trims. Gated on C9 state output in C9B. | Positive-health confirmation state. |

Nothing is edited here. The consumer map is for C9-SYNTH/C9A/C9B inheritance.

---

## 4. C6-INTERACTION & C3-INTERACTION DISCLOSURE (mandatory)

### C6-INTERACTION

- **Interaction description:** C6B prunes NF-001/NF-002 when SensorDynamicsState is in decisive sensor-fault states (O2_LAZY_OR_BIASED or MAF_UNDERREAD).
- **Interaction rule:** The C6 sensor-fault prune of NF-001/NF-002 must take precedence over any C9 healthy-confirm boost. If c6_decisive is true, NF-001/NF-002 must remain pruned (return None) to prevent a degraded/lazy sensor from being overridden by a C9 boost.
- **Live shim reference:** integration_shim.py::_score_rule lines 685-691 evaluates c6_decisive and returns None for NF-001/NF-002.

### C3-INTERACTION

C3 control-reference precedence is preserved:

- Live state check: `ControlPlausibilityState.CONTROL_REFERENCE_FAULT` via `integration_shim.py::_control_plausibility_state`.
- Live C3 effect: integration_shim.py::_score_rule boosts EF-001/002/003 and prunes SF-001/002 (unless c6_decisive) when CONTROL_REFERENCE_FAULT is present.
- Required precedence: C3 control-reference faults also prune SF-001/002 under C3 precedence. Since no_fault rules (NF-001/002) require clean OBD health, they are naturally inactive/pruned if any DTC is present, but C3 precedence is preserved: a C3 active control reference fault inherently invalidates any C9 no_fault call.

---

## 5. ALREADY-LIVE-COLUMN AUDIT (mandatory)

- **Total required C9 columns:** 15
- **Already live in schema (4):** `ltft_2500_pct, ltft_idle_pct, stft_2500_pct, stft_idle_pct`
- **Genuinely new ask (11):** `gas_delta_co2_pct, gas_delta_co_pct, gas_delta_hc_ppm, gas_delta_o2_pct, miles_since_clear, mode06_min_margin_pct, pending_dtc_count, permanent_dtc_count, readiness_supported_complete_bool, stored_dtc_count, warmup_cycles_since_clear`

Of the 15 required C9 columns, 4 already exist in the live schema (4 trims from C2B/C5B). The genuinely new ask is shrank to 11 columns. For C9 rows, the live columns exist in the schema but are currently empty/null.

---

## 6. C9 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 11)

**BUILDABLE_NOW-reachable by logic alone: 0**. Every C9 row is residual because
its readiness/DTC/trim/gas-delta columns are empty/null in the live corpus;
logic without values cannot move `top3_family`.

**SCORING_GATED: 11 / 11**, split by residual bucket:

- **DATA_GAP_ACQUISITION_GAP = 10:** CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014.
- **TUNABLE_HELD = 1:** era2_016.

**Oracle-family mix:** `{'misfire': 1, 'no_fault': 10}`. **Current winner family mix:** `{'catalyst_failure': 4, 'ecu_fault': 2, 'no_fault': 1, 'rich_mixture': 1, 'sensor_fault': 3}`.
All cases require C9 columns. **10 + 1 = 11.** ✔

**CODE_LANDED != SCORE_MOVED, stated for C9:** the HealthConfirmationState emit
logic and consumer map above are buildable from `cluster9.1.md`; any top3_family
delta is unobservable until C9-SYNTH/C9A provides values. A pack report must
never present wiring as score movement.

---

## 7. REGRESSION / FT-8 neighbour set (derived live)

A C9 consumer edit touches `no_fault.json` — the no_fault competition group.
The commit must re-audit every case those rules currently pass for a regressed family.
Union of `passes_cases` across all NF rules including the baseline runtime winners =
**17 cases**:

```
CASE-009, CASE-032, CSV-001, CSV-005, EXT-220, EXT-231, PDF-HI-005, PDF-HI-010, YAML-CSV1, YAML-CSV5, YAML-PDF_HI_005, YAML-TC1, case_012, case_028, case_049, era2_016, era3_009
```

**Dual target+neighbour cases (5):** PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-TC1, era2_016.

**NF-regression exposure:** NF rules touch no-fault cases. A C9 boost could resurrect a no_fault verdict on cases that have active sensor or ECU faults. Thus, the live C6B prunes must take precedence.

Rules derived live from the JSON files:

| Rule | Family | Competition group | passes_cases count |
| --- | --- | --- | --- |
| `NF-001` | `no_fault` | `no_fault` | 12 |
| `NF-002` | `no_fault` | `no_fault` | 1 |

---

## 8. Confounder disclosure (C9)

**Source:** `cluster9.1.md` / `cluster9.2.md` + `value9.md`.

| Confounder | Mechanism | Cite |
| --- | --- | --- |
| **Catalyst masking** | A healthy catalyst downstream strongly attenuates emissions, meaning tailpipe gas alone cannot diagnose engine-out or sensor degradation upstream. Separated by requiring complete OBD readiness, DTC absence, and Mode $06 margins rather than tailpipe gas alone. | cluster9.1.md §2; cluster9.2.md §Technical characterization |
| **Lazy oxygen sensor / sensor under-detection** | A degraded O2 sensor transitions slowly, delaying fuel correction without setting a DTC. Clean tailpipe gas masks the latency. Separated by O2 sensor dynamics (transition time < 150 ms, amplitude swing min/max) and fuel trim stability. | cluster9.1.md §2; value9.md §1 |
| **Freshly cleared OBD memory** | BATTERY_DISCONNECT or scan tool clear makes readiness incomplete and DTC count zero, creating a blind spot where active faults are temporarily hidden. Separated by requiring warm-up cycles >= 5 and miles since clear >= 200. | value9.md §1; cluster9.1.md §Bottom Line |
| **Marginal emissions systems** | Components that pass OBD but operate near malfunction limits can be missed. Separated by requiring Mode $06 monitor margins >= 10% of the limit range. | cluster9.1.md §2; value9.md §1 |

**Per-case mimic risk:** C9-SYNTH must use oracle-fault separability, not
current rank, to decide seed bands. For example, `era2_016` (expected misfire) is currently
winning `no_fault` due to clean tailpipe gas; C9-SYNTH must not back-solve it.

**C4 dependency:** C9 is theprove-healthy cluster and is independent of C4, but it is placed next in the sequence (C2 -> C3 -> C6 -> C5 -> C4 -> C9 -> C8 -> C1 -> C7) because C9 is the highest remaining yield research-independent pack.

---

## 9. Grounding-strength table per threshold

| Signal | Threshold | Grounding | Feasibility Tier | Risk note |
| --- | --- | --- | --- | --- |
| OBD readiness monitor completeness | All supported non-continuous monitors = COMPLETE / READY | **standardized (CARB/EPA)** | Tier A: generic OBD-II live data | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| OBD emission-related DTC count | Stored, pending, and permanent DTCs = 0 | **standardized (SAE J1979)** | Tier A: generic OBD-II live data | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| OBD Mode $06 monitor test margins | Test value must be inside limit with margin >= 10% of limit range | **standardized (regulatory cut)** | Tier A: generic OBD-II Mode $06 data | Mode $06 10% margin is a standard regulatory cut, but healthy populations vary widely above it. |
| OBD warm-up cycles since DTCs cleared | Warm-up cycles since clear >= 5 | **standardized (EPA/CARB)** | Tier A: generic OBD-II live data | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| OBD distance traveled since DTCs cleared | Distance since clear >= 200 miles | **standardized (CARB)** | Tier A: generic OBD-II live data | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| Short-Term Fuel Trim (STFT) | STFT within +/-5% (P10-P90: -4% to +4%) | **standardized (OEM/SAE J1979)** | Tier A: generic OBD-II live trims | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| Long-Term Fuel Trim (LTFT) | LTFT within +/-7% (P10-P90: -6% to +6%) | **standardized (OEM/SAE J1979)** | Tier A: generic OBD-II live trims | Readiness, DTC counts, and reset-age counters are SAE/CARB standards; physically and operationally decisive. |
| Fuel trim delta between idle and 2500 RPM | Delta of fuel trim <= +/-5% | **manufacturer-typical** | Tier A: generic OBD-II live trims | Fuel trim delta is highly typical but can vary slightly across speed-density vs MAF architectures. |
| Two-point gas delta: HC | Delta HC within -10 to +15 ppm | **anecdotal / workshop norm** | Tier B: 5-gas two-point capture | Gas deltas are derived from workshop norms; healthy deltas tend to be tight, but no regulatory cut exists. |
| Two-point gas delta: CO | Delta CO within -0.15 to +0.15% | **anecdotal / workshop norm** | Tier B: 5-gas two-point capture | Gas deltas are derived from workshop norms; healthy deltas tend to be tight, but no regulatory cut exists. |
| Two-point gas delta: CO2 | Delta CO2 typically positive, within +0.3 to +0.8% | **anecdotal / workshop norm** | Tier B: 5-gas two-point capture | Gas deltas are derived from workshop norms; healthy deltas tend to be tight, but no regulatory cut exists. |
| Two-point gas delta: O2 | Delta O2 within -0.5 to +0.4% | **anecdotal / workshop norm** | Tier B: 5-gas two-point capture | Gas deltas are derived from workshop norms; healthy deltas tend to be tight, but no regulatory cut exists. |
| Unsupported, incomplete, or marginal OBD health evidence | Any gate check fails or is missing; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | **physics/regulatory rationale (provenance required)** | Abstain fallback | Unsupported/incomplete data defaults to SENSOR_HEALTH_UNPROVEN_ABSTAIN. |

**Weakest-grounded threshold:** The two-point 5-gas deltas are anecdotal/workshop norms
and are subject to baseline analyzer noise.

---

## 10. ABSTAIN_FALLBACK (C9)

If any OBD readiness monitor is incomplete, DTCs are present, Mode $06 margins
are too narrow (<10%), fuel trims are unstable, or OBD history is too recently cleared,
the case **stays abstained** at MARGIN=0.02. Vehicles with unproven health must not be guessed.

---

## Provenance / guardrails

- Read-only: no corpus column added, no producer/consumer wired, no rule/weight
  edit, no yardstick mint, no synthesized values, no abstain-dial change
  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No
  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Sources: `v3/research/research_answers/cluster9.1.md`;
  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C9;
  `labs/comlab/registry/rules/no_fault.json`;
  `labs/comlab/registry/integration_shim.py` for C6/C3 interactions.
- Governs `T-V3-P4-C9-PRE` → `T-V3-P4-C9-SYNTH` → `C9A` → `C9B`.
