---
node_type: "hld"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "architecture"
implements: []
consumers:
  - "lld: labs/obdlab/docs/LLD_OBDLab.md"
  - "dld: labs/obdlab/docs/DLD_OBDLab.md"
drift_guards: []
tags: [obdlab, finished, hld]
source: "labs/obdlab/docs/HLD_OBDLab.md"
---
# HLD — OBDLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_OBDLab v1.0
**Version:** 2.0
**Date:** 2026-06-10
**Supersedes:** HLD_OBDLab v1.0 (2026-05-22) — pre-revive, 21-field payload, Physics Gate 3 present, exceptions on `ValueError`/`AssertionError`.

> **Audit note (2026-06-10):** this document was rewritten from the live source
> (`obdlab/` package) after the revive-as-emitter rework (T-OBDV2-0 … T-OBDV2-11,
> FIX-1…7, ARCH-1/2, PURGE-1…3). Every field, enum, and threshold below is
> grounded in the shipped code, not the v1.0 design intent.

---

## 1. Responsibility

OBDLab is the **electronic-perception channel** of the 4D petrol diagnostic
pipeline (the L5 live-PID layer). It validates and transforms a raw OBD-II PID
dict into a typed `OBDLivePayload` that represents **the ECU's perception** of
engine state.

OBDLab is an **emitter, not a judge.** It emits its own channels — trims,
normalized lambda, VE, perception-deltas, sensor provenance — and does **not**
produce fault-family verdicts. Cross-referencing OBD perception against GASLab
chemical truth, and rendering the final root-cause verdict, is COMLab's job
(see `KGtopic.md` division-of-labor). This emitter role was ratified in
**T-OBDV2-0 (`revive`, 2026-06-08)**: the >95% NO_FAULT result that prompted the
quarantine review was a **PID-less-corpus artefact**, not a code defect.

Truth-vs-perception: the ECU is *perception*, gas chemistry (GASLab
Brettschneider lambda) is *ground truth*.

---

## 2. Architecture Position

```
COMLab (Stage 4 — decision engine)
  │  builds ObdLabDnaView from the VIN/DNA record
  │  populates freeze_frame_pids from DTCLab before calling OBDLab
  ▼
obdlab.SensorSignalTranslator.translate(raw_user_inputs, dna_view, accumulator?)
  │
  ├─ [1] PIDIngestionValidator        — unit conversion + bounds + DNA-RPM + bank-2 contract
  ├─ [2] compute_bucket               — RPM state (runs BEFORE semantics — F-O7)
  ├─ [3] SemanticConsistencyChecker   — Physics Gates 1/2/4 + thermal + closed-loop
  ├─ [4] VEEngine.compute_ve          — volumetric efficiency (3-branch)
  ├─ [5] O2Normalizer.normalize       — lambda from O2 (3-branch) + O2 failure mode
  ├─ [6] TrimVectorAggregator.aggregate — STFT+LTFT totals + per-bank delta
  ├─ [7] AnalyticsPreconditions.evaluate — trim analytics gate (8 gates)
  └─ inline: lambda_perception_delta, w_theo, sensor_error_delta (guarded)
  │
  OBDLivePayload (31 canonical fields)
  │
  ▼
COMLab consumes the payload as a frozen contract surface (see §7).
```

Zero cross-lab Python imports. OBDLab owns local mirrors of any cross-lab type
it needs (e.g. `FuelSystemStatus`, mirrored from DTC_VOCABULARY §8). Isolation
is enforced by an import audit in the test suite.

---

## 3. Internal Pipeline (7 steps + guarded emitters)

```
raw_user_inputs + ObdLabDnaView (may be None) + LinearityAccumulator (optional)
       │
  [1]  PIDIngestionValidator.validate_and_convert
       │  Unit conversions: _f→_c, _psi→_kpa, _inhg→_kpa, _lbmin→_gps
       │  Bounds check:     12 fields vs physical_sensor_bounds.json §3.1
       │  DNA-RPM gate:     HIGH strict / PARTIAL log-fallthrough / NONE static
       │  Bank-2 contract:  number_of_banks==1 → shrtft2/longft2 must be None
       │  Maps fuel_system_status, validates per_cylinder_misfire_counts & ltft_cell_vector
       │
  [2]  compute_bucket  (state_bucketing.py, rules from obd_translation_rules.yaml)
       │  COLD_OPEN_LOOP_INVALID (priority 1, ECT<75) | STABILIZED_IDLE |
       │  REGULATORY_HIGH_IDLE | STRESS_IDLE   (default → STABILIZED_IDLE)
       │  Computed early so Physics gates can read rpm_state_bucket (F-O7 fix).
       │
  [3]  SemanticConsistencyChecker.evaluate
       │  Thermal gate:    ECT < 75 → override bucket to COLD_OPEN_LOOP_INVALID, engine_warmed=False
       │  Physics_Gate_1:  VSS > 10 AND RPM < 400 → SemanticConsistencyError
       │  Physics_Gate_2:  ECT ≥ 80 AND fuel_status == OL → SemanticConsistencyError
       │  Physics_Gate_4:  trim outside [-127, 127] → SemanticConsistencyError
       │  Closed-loop gate: ECT ≥ 75 AND fuel_status != CL → trim_analytics_suspect (non-blocking)
       │  (Physics_Gate_3 was REMOVED — FIX-1 Option B; superseded by FAULT_VE_SENSOR_SKEW)
       │
  thermal override → analytics_frozen = (bucket == COLD_OPEN_LOOP_INVALID)
       │
  [4]  VEEngine.compute_ve            (frozen → ve_pct=0.0, ve_validity=UNKNOWN)
  [5]  O2Normalizer.normalize         (frozen → normalized_obd_lambda=1.0, NO_FAULT)
  [6]  TrimVectorAggregator.aggregate (frozen → totals 0.0, bank-2/delta None)
       │
  [7]  AnalyticsPreconditions.evaluate  (ALWAYS runs, even when frozen)
       │  8 gates in priority order → TrimAnalyticsGate
       │
  guarded emitters (only when not frozen + guard satisfied):
       │  lambda_perception_delta — WIDEBAND_LINEAR + commanded_equivalence_ratio (PID 0x44)
       │  w_theo / sensor_error_delta — DUAL strategy + two-point accumulator (idle + stress bands)
       │
  ASSEMBLE OBDLivePayload (31 fields)
```

The thermal gate at step [3] freezes steps [4]–[6] (analytics frozen) but step
[7] still runs to populate `trim_analytics_gate`.

---

## 4. VE Routing Architecture

`VEEngine.compute_ve` routes on `ObdLabDnaView.air_metering_strategy`. Three
branches cover the three real petrol sensor configurations:

| Strategy | Sensor config | VE branch | MAF node | MAP node | Validity |
|----------|--------------|-----------|----------|----------|----------|
| `DUAL_MAF_MAP_CROSSCHECK` | Both present | `_ve_dual` | REAL_SENSOR_FEED | REAL_SENSOR_FEED | classified (§6.4) |
| `MAP_ONLY_SPEED_DENSITY` | MAP only | `_ve_map_only` | VIRTUAL_EMULATION | REAL_SENSOR_FEED | UNKNOWN (no independent cross-check) |
| `MAF_ONLY` | MAF only | `_ve_maf_only` | REAL_SENSOR_FEED | BACK_CALCULATED | UNKNOWN (no independent cross-check) |

Only `DUAL_MAF_MAP_CROSSCHECK` yields a cross-checkable VE and therefore a
non-`UNKNOWN` `ve_validity`. In the single-sensor branches the emulated/inferred
value algebraically cancels, so the validity is deliberately `UNKNOWN` — VE is
evidence only under the dual gate (T-OBDV2-2, Q5).

VE formula (speed-density / ideal gas), as implemented in `_calc_ve_standard`:

```
VE(%) = [MAF(g/s) × R(8.314) × (IAT_C + 273.15)]
        / [MAP(kPa) × (RPM/60) × (Disp_L/2) × MM_AIR(28.97)] × 100
```

`ve_pct` is bounded `[0.0, 200.0]` (the 200 ceiling accommodates thermal-shock
steam overshoot). When analytics are frozen or inputs are missing, `ve_pct`
carries the `0.0` sentinel and `ve_validity == UNKNOWN` suppresses all
VE-based router decisions downstream.

---

## 5. O2 Normalisation Architecture

Three sensor types map to two code paths, producing one unified
`normalized_obd_lambda` in `[0.7, 1.3]` plus an `O2FailureMode`:

```
NARROWBAND_0_TO_1V   ─┐
WIDEBAND_NB_SIM      ─┤→ 3-zone voltage→lambda (reads pid_oxygen_sensor_volts)
                       │    0.10–0.40 V → λ 1.05 (LEAN)
                       │    0.41–0.50 V → λ 1.00 (STOICH)
                       │    0.51–0.90 V → λ 0.95 (RICH)
                       │    < 0.10 V → O2_CHANNEL_FAULT, clamp λ 1.05, STUCK_LEAN
                       │    > 0.90 V → O2_CHANNEL_FAULT, clamp λ 0.95, STUCK_RICH

WIDEBAND_LINEAR      ──→ direct passthrough (reads pid_wideband_equivalence_ratio)
                           0.7 ≤ λ ≤ 1.3 → WIDEBAND_PASSTHROUGH
                           out-of-range → O2_CHANNEL_FAULT, clamp to nearest bound
                           warm + closed-loop + not WOT + not DFCO + |λ−1.0| > 0.05
                              → WIDEBAND_OFFSET_CANDIDATE (proposal EP-OBD-17)
```

`O2FailureMode` is now a 4-member taxonomy: `NO_FAULT`, `STUCK_LEAN`,
`STUCK_RICH`, `WIDEBAND_OFFSET_CANDIDATE`. The legacy members
`SLUGGISH`/`DEAD`/`WRONG_CENTERLINE`/`HEATER_FAULT` were pruned (ARCH-2) — they
had no consumer.

The wideband branch only flags `WIDEBAND_OFFSET_CANDIDATE`; it never asserts a
verdict. COMLab `T-COMV2-O2OFFSET-1` (Stage 4) is the named consumer.

---

## 6. Trim Analytics Gate — 8-Gate Priority Chain

`AnalyticsPreconditions.evaluate` returns the first failing gate (priority
order), else `VALID`:

```
Gate 1: coolant_temp_c < 70 (or missing)   → ENGINE_COLD
Gate 2: fuel_system_status != CL            → OPEN_LOOP
Gate 3: active DTC ∈ O2_FAULT_DTCS         → O2_FAULT_ACTIVE
Gate 4: active DTC ∈ {P0335, P0340}        → CKP_CMP_FAULT_ACTIVE
Gate 5: drive_cycles_since_clear < 1        → CODES_RECENTLY_CLEARED
Gate 6: throttle_pos ≥ 90                    → WOT_ACTIVE
Gate 7: dfco_active is True                  → DFCO_ACTIVE
Gate 8: semantic gates not all passed        → SEMANTIC_ERROR
All pass                                      → VALID
```

`O2_FAULT_DTCS` = P0130–P0161 (32 codes). `CKP_CMP_FAULT_DTCS` = {P0335, P0340}.
Both frozensets are maintained locally; keeping them in sync with DTCLab routing
is a COMLab responsibility. The gate **classifies** trim trustworthiness — it
does not suppress payload emission.

---

## 7. COMLab Integration Points

OBDLab emits at Stage 2; COMLab consumes at Stage 4. Several fields are
**frozen-contract surface** with a forward-registered consumer task — emitted
now, read when the COMLab fusion task lands. This is the deliberate
emit-S2 / consume-S4 pattern, kept honest by the signal/noise rule.

| `OBDLivePayload` field | COMLab consumer | Status |
|------------------------|-----------------|--------|
| `normalized_obd_lambda` | Delta vs GASLab `lambda_chem` (ECU vs chemistry) | live route |
| `total_trim_correction_delta` (+`_b2`) | delta_Healing trim computation | live route |
| `per_bank_trim_delta` | `T-COMV2-BANK-FUSE-1` (bank asymmetry) | S4 forward-reg |
| `lambda_perception_delta` | `T-COMV2-ECU-FUSE-1` (ECU perception fusion) | S4 forward-reg |
| `ve_pct` / `ve_validity` | `T-COMV2-VE-GATE-1` (VE-as-evidence gate) | S4 forward-reg |
| `o2_failure_mode` (`WIDEBAND_OFFSET_CANDIDATE`) | `T-COMV2-O2OFFSET-1` | S4 forward-reg |
| `fuel_system_status` | live `analytics_preconditions` + `semantic_consistency_checker`; `T-COMV2-FUELSYS-GATE-1` | live + S4 |
| `intake_air_temp_c` | live in `ve_engine`; `T-COMV2-ECU-HW-1` | live + S4 |
| `throttle_pos_pct` | `T-COMV2-ECU-HW-1` | S4 forward-reg |
| `control_module_voltage_v` | `T-COMV2-VPWR-GATE-1` (electrical pre-check) | S4 forward-reg |
| `per_cylinder_misfire_counts` | `T-COMV2-MISFIRE-LOC-1` | S4 forward-reg |
| `ltft_cell_vector` | `T-COMV2-LTFT-CELL-1` | S4 forward-reg |
| `w_theo` / `sensor_error_delta` | `T-COMV2-MAF-LIN-1` | S4 forward-reg |
| `maf_status` / `map_status` | COMLab evidence weighting | S4 |
| `rpm_state_bucket` / `engine_warmed` | fault-routing + analytics-applicability context | S4 |
| `trim_analytics_gate` | COMLab confidence path (suppress trim findings unless VALID) | S4 |
| `freeze_frame_pids` | ferried through from DTCLab (populated by COMLab pre-call) | passthrough |

> **Cross-lab note:** DTCLab and COMLab have **not yet been reworked**. The S4
> consumer tasks above are registered intent; when DTCLab/COMLab are rebuilt
> they reconcile up to this frozen OBD contract, not the other way around.
> OBDLab is never blocked on COMLab.

---

## 8. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| Pipeline latency | < 50 ms warm idle, HIGH DNA |
| Sensor bounds drift | 0 drift between `physical_sensor_bounds.json` and `OBDLab_KG_Wiki.md §3.1` |
| Import isolation | 0 cross-lab Python imports |
| `HIGH_IDLE_LOAD` token | 0 occurrences in `obdlab/` (superseded by `REGULATORY_HIGH_IDLE`/`STRESS_IDLE`) |
| Numeric literals | every literal in `obdlab/` carries a `# wiki:` citation comment |
| Signal/noise | every payload field has a named, existing-or-proposed consumer |

---

## 9. Known Gaps / Accepted Behaviour

| ID | Description | Status |
|----|-------------|--------|
| `dna_view=None` VE | Returns `VEValidity.UNKNOWN`, `ve_pct=0.0`; degraded-mode, no crash | Accepted |
| `dna_view=None` O2 | Defaults to `NARROWBAND_0_TO_1V`; logged | Accepted |
| FU-ECU-2 | PID 0x44 `commanded_equivalence_ratio` ingested with only a numeric check (no λ-range bound) | Follow-up — bound to be pinned from wiki |
| Anti-orphan (S4) | VE/O2/bank/perception fields read by no **live** COMLab path yet | Expected — closes when S4 consumer tasks land |
| Doc-bug O2-FU-2 | `SUPPRESS_POST_CAT_TRIM` is not a `TrimAnalyticsGate` value (chunk o2-logic/06) | Logged, not an edge |
