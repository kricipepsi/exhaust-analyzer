# V3_C6_REVEAL_CONTRACT_2026-07-05

**Task:** `T-V3-P4-C6-PRE`  **Mode:** DISCLOSE only (read-only pre-author)
**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no
**Machine-readable twin:** `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json`
(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_c6_contract.py`).

This document instances the frozen reveal contract for **C6 — sensor fault under-detection**,
the next pack in the pinned sequence (C2 → C3 → **C6** → C5 → C4 → …).
It builds nothing and scores nothing; it fixes how C6 discloses thresholds, consumers,
C3 interaction, FT-8 exposure, and stay-abstained cases.

---

## 0. Baseline pin

| Artefact | Pinned value |
| --- | --- |
| Yardstick | `V3_YARDSTICK_2026-07-05-C3B` |
| CSV SHA-256 | `9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283` |
| Oracle subset SHA-256 | `3088a7c3…` (unchanged) |
| Scorer | `apps/wired/v7/run_suite.py (hash-locked, untouched)` |
| Named run | `POST_T_V3_P4_C3B` |
| Run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json` |

All C6 sizing references this current post-C3B baseline. If any commit lands first, stop and re-pin before C6-SYNTH/C6A.

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

## 2. C6 producer extraction (cited to `cluster6.md`)

The C6 producer is **OBDLab `SensorDynamicsState`**. It emits
`O2_LAZY_OR_BIASED`, `MAF_UNDERREAD`, or `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.
The emit thresholds, transcribed read-only from the research answer:

| Signal | Maneuver | Threshold | Verdict | Evidence field(s) | Grounding | Cite |
| --- | --- | --- | --- | --- | --- | --- |
| Mode $06 oxygen-sensor monitor margin | Warm closed loop; retrieve Mode $06 current result and min/max limits | Use the ECU's stored min/max acceptable band; low or exceeded margin to the vehicle-specific limit emits O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `mode06_o2_response_margin_pct` | standardized-transport / manufacturer-specific numeric limit | cluster6.md §Question One Answer lines 114-115; §Question Four Answer line 155; Candidate Signature Table line 171 |
| Forced rich→lean / lean→rich O2 response timing | Stabilize at about 2500 rpm no-load; decel fuel cut for rich→lean; controlled return/enrichment for lean→rich | Prefer vehicle Mode $06/OEM limit; absent that, longer-than-expected transition is positive evidence. Research names the direction, not a fleet-wide millisecond fail line; 849 ms / <150 ms examples must not be treated as universal. | `O2_LAZY_OR_BIASED` | `o2_rich_to_lean_ms, o2_lean_to_rich_ms` | manufacturer-typical (direction strong, universal ms bound weak) | cluster6.md §Question Three Answer lines 147-151; §Question Four Answer line 157; Candidate Signature Table line 172 |
| MAF actual vs calculated airflow plausibility | Warm idle and steady 2500 rpm no-load; compare measured MAF to modeled airflow | Sustained measured-MAF shortfall greater than roughly 10-15% versus modeled airflow at BOTH points emits MAF_UNDERREAD | `MAF_UNDERREAD` | `maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, calc_airflow_gps_2500` | empirical-inferred (component accuracy anchored; vehicle threshold provisional) | cluster6.md §Question One Answer lines 117-118; §Question Three Answer line 149; §Question Four Answer line 161; Candidate Signature Table line 174 |
| Static-only O2/MAF evidence | Single static O2 voltage, AFR, or MAF value only | Static-only values are rejected as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `absence of decisive dynamic Mode $06/O2 timing/MAF plausibility evidence` | physics/regulatory rationale (dynamic inconsistency required) | cluster6.md §Question One Answer lines 126-129; V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C6.6 line 93 |

**Producer emit summary:** `O2_LAZY_OR_BIASED` requires decisive dynamic
O2 evidence (Mode $06 margin or active response timing); `MAF_UNDERREAD`
requires sustained >10–15% measured-MAF shortfall versus modeled airflow at
both warm idle and 2500 rpm; static-only O2/MAF values produce
`SENSOR_HEALTH_UNPROVEN_ABSTAIN`, not a guessed pass/fail.

**Load-bearing subset to size in C6A:** Mode $06 margin + the two MAF delta
columns may be enough for many rows; exact rich↔lean millisecond columns are
stronger when Mode $06 is absent/equivocal. C6A must ladder these scenarios
instead of committing all 9 columns blindly.

---

## 3. C6 consumer mapping (named; no edit)

| Family file | Rules | Field each would read | What the C6 state supplies |
| --- | --- | --- | --- |
| `sensor_fault.json` | **SF-005 / SF-008 / SF-001 / SF-002** | `mode06_o2_response_margin_pct`, `o2_rich_to_lean_ms`, `o2_lean_to_rich_ms`, MAF actual-vs-calculated deltas and source g/s columns | Dynamic sensor under-detection evidence: lazy/biased O2 or under-reading MAF. |
| `no_fault.json` | **NF-001 / NF-002** | Same C6 columns, but healthy margins/response/no-MAF-shortfall | Healthy-vs-under-detected split; protects clean rows from false sensor-fault boosts. |

Nothing is edited here. The consumer map is for C6-SYNTH/C6A/C6B inheritance.

---

## 4. C3-INTERACTION DISCLOSURE (mandatory)

The live C3B shim now has a control-reference state and a prune/boost branch:

- Producer: `integration_shim.py::_control_plausibility_state lines 540-557` returns `CONTROL_REFERENCE_FAULT` from KOEO MAP/BARO, ground drop, and loaded-voltage gates.
- Effect: integration_shim.py::_score_rule lines 562-569 boosts EF-001/002/003 by +0.10 and prunes SF-001/SF-002 when CONTROL_REFERENCE_FAULT is present.
- C6 future effect: C6 will boost sensor/no-fault consumers from SensorDynamicsState: O2_LAZY_OR_BIASED, MAF_UNDERREAD, or SENSOR_HEALTH_UNPROVEN_ABSTAIN.
- Today: C3 columns and C6 columns are disjoint in the current corpus.

**Composition / precedence rule C6B must implement:**
If a future row carries both C3 control-reference columns and C6 sensor-dynamics columns, C3 control-reference pruning must run first for SF-001/SF-002. Only a decisive C6 dynamic sensor fault may re-enable/boost sensor rules; static-only C6 evidence must preserve abstain/prune behavior. This prevents a control-reference fault from being relabelled as a lazy O2 sensor.

This interaction is disclosed now because SF-001/SF-002 are in both surfaces:
C3 prunes them when a control-reference fault is decisive; C6 may later boost
sensor rules when sensor-dynamics evidence is decisive. Static-only C6 evidence
must abstain and must not undo a C3 prune.

---

## 5. C6 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 14)

**BUILDABLE_NOW-reachable by logic alone: 0**. Every C6 row is residual because
its dynamic O2/MAF discriminator is absent from the live corpus; logic without
values cannot move `top3_family`.

**SCORING_GATED: 14 / 14**, split by residual bucket:

- **DATA_GAP_ACQUISITION_GAP = 3:** CASE-045, CASE-048, YAML-TC46.
- **OUTRANKED_HARD = 6:** CASE-014, EXT-229, EXT-230, YAML-CSV25, case_046, era1_006.
- **TUNABLE_HELD = 5:** CSV-025, EXP-N020, PDF-4G-05, TC-046, era2_012.

**Oracle-fault mix:** `{'misfire': 1, 'sensor_fault': 13}`. **Current winner mix:** `{'catalyst_failure': 1, 'lean_condition': 2, 'misfire': 3, 'no_fault': 6, 'rich_mixture': 1, 'sensor_fault': 1}`.
All cases require: `mode06_o2_response_margin_pct, o2_rich_to_lean_ms, o2_lean_to_rich_ms, maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500, calc_airflow_gps_idle, calc_airflow_gps_2500`. **3 + 6 + 5 = 14.** ✔

**CODE_LANDED != SCORE_MOVED, stated for C6:** the SensorDynamicsState emit
logic and consumer map above are buildable from `cluster6.md`; any top3_family
delta is unobservable until C6-SYNTH/C6A provides values. A pack report must
never present wiring as score movement.

---

## 6. REGRESSION / FT-8 neighbour set (derived live)

A C6 consumer edit touches `sensor_fault.json` and `no_fault.json` — both
competition groups. The commit must re-audit every case those rules currently
pass for a regressed family. Union of `passes_cases` across all SF + NF rules =
**33 cases**:

```
CASE-009, CASE-014, CSV-001, CSV-005, CSV-025, EXP-N006, EXP-N015, EXP-N020, EXP-N028, EXT-219, EXT-220, EXT-229, EXT-230, EXT-231, PDF-HI-005, PDF-HI-010, TC-046, YAML-CSV25, YAML-CSV5, YAML-PDF_HI_005, YAML-TC1, YAML-TC46, case_004, case_009, case_012, case_025, case_026, case_028, case_037, case_039, case_041, case_046, case_049
```

**Dual target+neighbour cases (9):** CASE-014, CSV-025, EXP-N020, EXT-229, EXT-230, TC-046, YAML-CSV25, YAML-TC46, case_046.

**NF-regression exposure:** NF rules touch healthy/no-fault cases. A false C6 boost that regresses NF-001/NF-002 is high-cost because it turns a healthy case into a fault.

Rules derived live from the JSON files:

| Rule | Family | Competition group | passes_cases count |
| --- | --- | --- | --- |
| `SF-001` | `sensor_fault` | `sensor_fault` | 5 |
| `SF-002` | `sensor_fault` | `sensor_fault` | 3 |
| `SF-003` | `sensor_fault` | `sensor_fault` | 3 |
| `SF-004` | `sensor_fault` | `sensor_fault` | 1 |
| `SF-005` | `sensor_fault` | `sensor_fault` | 3 |
| `SF-006` | `sensor_fault` | `sensor_fault` | 1 |
| `SF-007` | `sensor_fault` | `sensor_fault` | 3 |
| `SF-008` | `sensor_fault` | `sensor_fault` | 5 |
| `NF-001` | `no_fault` | `no_fault` | 12 |
| `NF-002` | `no_fault` | `no_fault` | 1 |

---

## 7. Confounder disclosure (C6)

**Source:** `cluster6.md` §Question Three/Four Answers + acq-spec §C4.

| Confounder | Mechanism | Cite |
| --- | --- | --- |
| **Upstream exhaust leak or intake tract disconnection** | Cluster6 pre-gate requires no obvious upstream exhaust leak or intake tract disconnection. Either can distort O2 or airflow plausibility and mimic lazy-O2/MAF-underread behavior. | cluster6.md §Question Three Answer line 145 |
| **MAF architecture / speed-density vehicle** | If no MAF is fitted, the MAF_UNDERREAD branch is not applicable; the case needs O2 dynamics or abstain, not an invented MAF comparison. | cluster6.md §Question Three Answer line 145 and flow lines 215-220 |
| **Wideband versus switching O2 architecture** | If the upstream sensor is wideband, cross-count logic is not applicable; Mode $06/OEM limits or appropriate active dynamics must drive the decision. | cluster6.md §Question Three Answer line 145 |
| **C4 exhaust-leak / true-lean overlap** | C4 consumes these same C6 O2/MAF dynamics columns to separate exhaust leak, true lean, and biased-O2 lookalikes. C6-SYNTH must mark cases outside sensor/no-fault separability as stay-abstained candidates. | V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md lines 106-112 |

**Per-case mimic risk:** C6-SYNTH must use oracle-fault separability, not
current rank, to decide seed bands. `PDF-4G-05` is an explicit lookalike:
oracle `misfire`, current `sensor_fault`; C6 must not back-solve it into a
sensor pass. Sensor-vs-no_fault rows have high NF regression exposure.

**C4 dependency:** C4B consumes the C6 O2/MAF dynamics columns; landing C6 unblocks half of C4B's column ask but does not itself decide C4.

---

## 8. Grounding-strength table per threshold

| Signal | Threshold | Grounding | Feasibility Tier | Risk note |
| --- | --- | --- | --- | --- |
| Mode $06 oxygen-sensor monitor margin | Use the ECU's stored min/max acceptable band; low or exceeded margin to the vehicle-specific limit emits O2_LAZY_OR_BIASED | **standardized-transport / manufacturer-specific numeric limit** | Tier A: generic OBD-II Mode $06 where exposed | Strong transport standard; numeric pass/fail limit remains vehicle-specific. |
| Forced rich→lean / lean→rich O2 response timing | Prefer vehicle Mode $06/OEM limit; absent that, longer-than-expected transition is positive evidence. Research names the direction, not a fleet-wide millisecond fail line; 849 ms / <150 ms examples must not be treated as universal. | **manufacturer-typical (direction strong, universal ms bound weak)** | Tier A if ECU monitor decisive; Tier C if scope timing required | Direction is strong; do not freeze a universal millisecond threshold. |
| MAF actual vs calculated airflow plausibility | Sustained measured-MAF shortfall greater than roughly 10-15% versus modeled airflow at BOTH points emits MAF_UNDERREAD | **empirical-inferred (component accuracy anchored; vehicle threshold provisional)** | Tier A if PID set available; otherwise Tier C modeled-airflow support | Provisional producer-tuning risk; validate 10-15% band on real vehicles. |
| Static-only O2/MAF evidence | Static-only values are rejected as a separator; emit SENSOR_HEALTH_UNPROVEN_ABSTAIN | **physics/regulatory rationale (dynamic inconsistency required)** | Abstain fallback | Static-only inputs are insufficient; abstain is the intended outcome. |

**Weakest-grounded threshold:** the MAF >10–15% actual-vs-calculated shortfall
is empirical-inferred. The O2 monitor framework is stronger, but its numeric
limit is vehicle-specific; do not launder example values such as 849 ms or <150 ms
into a universal fleet threshold.

---

## 9. ABSTAIN_FALLBACK (C6)

If only static O2/MAF values are supplied, the row **stays abstained** at
MARGIN=0.02. C6 separates on dynamic inconsistency: Mode $06 monitor margin,
active O2 response timing, or two-point MAF plausibility. One warm-idle static
sensor value is not a discriminator.

---

## Provenance / guardrails

- Read-only: no corpus column added, no producer/consumer wired, no rule/weight
  edit, no yardstick mint, no synthesized values, no abstain-dial change
  (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No
  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Sources: `v3/research/research_answers/cluster6.md`;
  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C6/§C4;
  `labs/comlab/registry/rules/sensor_fault.json`, `no_fault.json`;
  `labs/comlab/registry/integration_shim.py` lines 540-569 for C3 interaction.
- Governs `T-V3-P4-C6-SYNTH` → `C6A` → `C6B`.
