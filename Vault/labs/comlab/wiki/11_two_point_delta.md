---
chunk_id: COMWIKI-11
title: "Two-Point Delta & the Gas↔OBD Cross-Reference"
doc: COM_WIKI
version: v2.1
date: 2026-06-21
status: authoritative
summary: "R3 / packs D+E: the one new signal that can raise top-1 — the sign and magnitude of change across an RPM step, cross-referenced between the gas-delta and OBD-delta vectors with conflict-aware fusion. Canonical operating points, per-fault signatures + abstain set, noise floors, mandatory architecture gates, validity gates, temporal alignment, and uncertainty propagation. Built default-off; live value gated on a populated second frame. v2.1 adds §CONCEPT_DELTA_BANDS — the COMLab-local mirror of every numeric profile band the delta engine applies, so the engine's thresholds have a COMLab source of truth, not only OBDLab's research tree."
entities_defined: [TEST_TWO_POINT, CONCEPT_OPERATING_POINTS, RULE_DELTA_GATE, RULE_CROSSREF, CONCEPT_NOISE_FLOOR, CONCEPT_DELTA_ABSTAIN, CONCEPT_DELTA_BANDS, CONCEPT_TEMPORAL_ALIGN, CONCEPT_DELTA_UNCERTAINTY]
related_chunks: [COMWIKI-03, COMWIKI-06, COMWIKI-08, COMWIKI-12, COMWIKI-13]
sources: [REWORK_PLAN_COMLab.md §3.D/§3.E/§8, PROPOSAL_DeltaLab_cross_lab_delta_module.md, "DeltaRes1.md", "DeltaRes2.md", "Two-Point Emissions Test Fixture Design.md", "Multi-Sensor Fusion for Automotive Diagnostics.md", tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md]
---

# Two-Point Delta & the Gas↔OBD Cross-Reference

## The reframe (R3)

The hardest collisions — `TIMING_RETARDED` → ~7 families; worn rings vs valve seals; lean vs
vacuum-leak vs exhaust-leak — are **single-snapshot collisions** that separate on the **sign of
the change across an RPM step**, a discriminator that needs **no DTC** (proposal §1). Both pack-E
reports converge: cross-reference the **gas-delta vector** against the **OBD-delta vector** with
**conflict-aware fusion**, after temporal alignment and uncertainty weighting.

**The two-point contract already largely exists** (REWORK_PLAN §8.1): GASLab emits an optional
2500-RPM frame (`reading_high`, `high_idle_*`); OBDLab carries `REGULATORY_HIGH_IDLE` /
`STRESS_IDLE` buckets keyed to `stress_idle_rpm_target` and already computes a two-point MAF/MAP
linearity delta. **What is single-point is the populated master corpus.** So `T-COMV2-DELTA-1` is
a **wiring job, built default-off**; the single-point path stays byte-identical when no second
frame is present. **Live value is gated on Gate-Capture** (`COMWIKI-12`).

## Canonical operating points {#CONCEPT_OPERATING_POINTS}

Adopt **curb idle + 2500 RPM no-load (two-speed idle)** as the canonical pair — the only
universally standardised pair across EPA/BAR for 1990–2010, no dyno (`DeltaRes1 Q1`,
`Two-Point`). Treat **stress idle ~3750 RPM (ECE R51 / ISO 5130)** as an *optional* second
elevated point for fuel-delivery / mechanical faults. **Pick one canonical pair per signal and
cite it — never silently mix bands** (proposal §5). This resolves the open band reconciliation in
`T-COMV2-DELTA-1`. [v2: D.Q1]

## Architecture gates FIRST — mandatory {#RULE_DELTA_GATE}

Branch on air-metering / induction **before** applying any delta profile. Applying a profile
without gating *creates* misclassifications:

- **Speed-density (MAP-only) nulls ΔTrim for a real leak** → route to IAC / throttle-angle, not
  the leak profile (`COMWIKI-03` VE polymorph).
- **Forced-induction post-turbo leak inverts ΔTrim sign** (≈ −20 % under boost).

This is a hard requirement in the `T-COMV2-DELTA-1` risks. *Files:* `analytics/delta_engine.py`
(gate before profile). [v2: D.Q4]

## Per-fault signatures & the abstain set {#CONCEPT_DELTA_ABSTAIN}

Encode the per-fault Δ table (direction + magnitude + tolerance) from the pack-D reports as
fixtures. Explicitly encode the **abstain families** whose delta is uninformative — **sensor
fault, ECU fault, catalyst failure, mechanical wear, non-starter** (`DeltaRes1 Q2`, `Two-Point`
master table) — so the engine **abstains rather than guesses**. *Files:*
`tests/unit/test_delta_engine.py`, fixture table.

## Per-fault profile bands — COMLab-local mirror {#CONCEPT_DELTA_BANDS}

> **Single-lab isolation.** These are the COMLab source of truth for every numeric band the delta
> engine applies — a maintainer verifies them here, not in another lab's research tree. Each row
> records its `delta-relations/NN` **provenance**, which is history, not a runtime dependency.
> This section mirrors the literals in `analytics/delta_engine.py`; if the code and this table ever
> disagree, that is a drift bug to reconcile (architect). (Added 2026-06-21.)

**Validation frames** (which RPM bucket each channel is differenced at):
`ΔTrim @ STRESS_IDLE` (3500–4500 RPM, *prov* delta-relations/01) · `Δgas / ΔO₂ @ REGULATORY_HIGH_IDLE`
(~2500 RPM, *prov* /07).

### ΔTrim profile thresholds (% trim) {#CONCEPT_DELTA_BANDS_TRIM}

| Profile | ΔTrim across step | Low-idle starting band | Prov |
|---|---|---|---|
| Vacuum leak | `≤ −10` | `+15 … +25` | delta-relations/02 |
| Fuel starvation | `≥ +10` | `0 … +5` | delta-relations/03 |
| MAF under-report | `≥ +10` | `0 … +8` | delta-relations/04 |
| Exhaust backpressure | `≤ −10` (elevated `≤ −12`) | `≈ 0` at low idle | delta-relations/05 |

### Δgas profile thresholds (HC/NOx ppm · λ) {#CONCEPT_DELTA_BANDS_GAS}

| Profile | Band | Prov |
|---|---|---|
| Worn piston rings | `ΔHC ≥ +100` (15→180) | delta-relations/07 |
| Worn valve seals | `ΔHC ≤ −50` (120→15) | delta-relations/07 |
| Flat cam (breathing misfire) | elevated `O₂ ≥ ~2.5` | delta-relations/07 |
| EGR stuck-closed | `ΔNOx ≥ +800` (1500→2800) | delta-relations/07 |
| Rich (attenuating) | `Δλ ≥ +0.05` | delta-relations/07 |

### Architecture gate (mandatory, runs before any profile) {#CONCEPT_DELTA_BANDS_ARCH}

Speed-density (MAP-only) **nulls** ΔTrim for a real leak; forced-induction post-turbo leak
**inverts** ΔTrim sign (`≈ −20 % STFT` under boost). *Prov* delta-relations/06. (Concept: §RULE_DELTA_GATE.)

### Validity gate (% volume, second frame) {#CONCEPT_DELTA_BANDS_VALIDITY}

Valid sample `vsum 14 … 18 %`; dilution fail if `CO+CO₂ ≤ 6 %`. *Prov* delta-relations/08.
(Concept: §TEST_TWO_POINT.)

### Confidence caps {#CONCEPT_DELTA_BANDS_CONF}

Two-point delta primary-axis confidence `0.92` (*prov* delta-relations/01); architecture-unknown
cap `0.70` (*prov* delta-relations/06).

## Noise floor — within-noise → abstain {#CONCEPT_NOISE_FLOOR}

RSS-derived noise floors are the "within-noise → not diagnostic" thresholds (each literal carries
its source citation; `Two-Point` §noise floor; OBD trim quantization 0.39 %/bit):

| Channel | Noise floor | Source |
|---|---|---|
| total fuel trim | **±3 %** | Two-Point §noise floor / OBD 0.39 %/bit |
| HC | **±15 ppm** | Two-Point §noise floor |
| CO | **±0.05 %** | Two-Point §noise floor |
| O₂ | **±0.20 %** | Two-Point §noise floor |

A delta inside the floor is **not diagnostic** → that channel abstains. [v2: D.Q3]

## Second-reading validity gates {#TEST_TWO_POINT}

Both frames must pass, or that modality abstains (E.Q4 graceful degradation):

- gas-sum / dilution: `CO+CO₂ > 6 %`, `O₂ < 5 %`
- RPM stability: ±100 RPM for ≥10 s
- warm-up: ECT in band
- settle time observed; closed-loop active

Failing → modality abstains (feeds the fusion abstain path, `COMWIKI-08`). *Files:* validity-gate
table → Stage-A gates. [v2: D.Q5]

## Temporal alignment {#CONCEPT_TEMPORAL_ALIGN}

Hold each operating point **≥15 s** after RPM stabilises; apply a fixed **~10 s lag offset** to
gas vs OBD (range 9–13 s, varies with flow); compute deltas from the **last 5 s** of each hold;
optional cross-correlation (MAF/MAP vs CO₂/O₂) for per-vehicle lag refinement (`DeltaRes2 Q1`,
`Multi-Sensor Fusion Q1`). *Files:* `analytics/delta_engine.py` (alignment pre-step). [v2: E.Q1]

## Normalise + propagate uncertainty {#CONCEPT_DELTA_UNCERTAINTY}

Per channel: `Δ_c = elevated − low`; `σ_Δc = √(σ_low² + σ_elev² + σ_align²)`; standardise to
`z_c = Δ_c / σ_Δc` against the per-point healthy baseline. Higher-uncertainty channels contribute
less (inverse-variance — `COMWIKI-08` `FUSE_INV_VARIANCE`). This is the established
**delta-then-normalise-then-fuse** order (per-lab delta in native units first, normalise after).
`σ_meas` comes from analyzer/scan-tool specs (the noise-floor bands above) gated by the emitted
`SampleValidity` (invalid → abstain), since no lab emits a numeric σ (REWORK_PLAN §8.2).
[v2: E.Q2]

## Gas↔OBD cross-reference logic {#RULE_CROSSREF}

Agreement/disagreement between the two delta vectors is the **core discriminator** (both E
reports). A checked-in cross-reference table maps each pattern to an action:

| Δgas | ΔOBD | Interpretation | Action |
|---|---|---|---|
| lean | trim ≈ null (speed-density) | real leak the MAP can't see | raise leak confidence; route IAC/throttle |
| agree (both lean) | both lean | corroboration | confidence up, **no double-count** |
| lean | MAF under-reports | MAF bias | route `ERR-SF-003` / `ERR-LC-002` |
| gas ≈ stoich | O₂ stuck | sensor lies | **trust gas**, route sensor_fault |
| pre-O₂ exhaust leak | false-lean O₂ | dilution | route `ERR-LC-006` |

Agreement → corroborating mass; disagreement → **conflict mass that maps to a specific fault**
(fed to fusion as a feature, `COMWIKI-08` `FUSE_CONTRADICTION`). *Files:* fusion stage + a
checked-in cross-reference table (this wiki). [v2: E.Q3]

## Validation status — the blocking gap

There is **no public dataset** pairing 5-gas + OBD PIDs at ≥2 points per vehicle with a confirmed
fault (both E reports, pack C). So: validate the delta module on **synthetic fixtures**
(prompt-D master table) for **algorithm correctness now**; treat **diagnostic accuracy as
unvalidated** until a paired/field dataset exists; plan prospective field capture as the only real
validation path. This is why `T-COMV2-DELTA-1` is **build-now / live-gated**. [v2: D.Q6/E.Q5/§8.5]

## Graph relations (explicit)

**TEST_TWO_POINT** SEPARATES **RULE_COLLISION_SET (COMWIKI-06)** WHERE Δ informative
**RULE_DELTA_GATE** RUNS_BEFORE **any delta profile** (speed-density null / turbo inversion)
**CONCEPT_DELTA_ABSTAIN** ABSTAINS_FOR **sensor/ecu/catalyst/mechanical_wear/non_starter**
**CONCEPT_NOISE_FLOOR** within-floor → **non-diagnostic abstain**
**RULE_CROSSREF** FEEDS **FUSE_CONTRADICTION (COMWIKI-08)** as conflict-as-feature
**T-COMV2-DELTA-1** BUILT **default-off**; LIVE_GATED_ON **GATE_CAPTURE (COMWIKI-12)**
**delta diagnostic accuracy** UNVALIDATED UNTIL **paired/field dataset**

## Core Entities

- **TEST_TWO_POINT** — Dual-speed-idle operating point test (idle vs 2500 RPM). Consumer: `comlab/analytics/delta_engine.py`.
- **CONCEPT_OPERATING_POINTS** — Curb idle + 2500 RPM + 3750 RPM stress idle. Consumer: `comlab/analytics/delta_engine.py`.
- **RULE_DELTA_GATE** — Architecture-flag routing gating before applying delta profile. Consumer: `comlab/analytics/delta_engine.py`.
- **RULE_CROSSREF** — Gas vs OBD delta vector cross-reference logic. Consumer: `comlab/analytics/delta_engine.py (proposed)`.
- **CONCEPT_NOISE_FLOOR** — RSS-derived noise thresholds for delta diagnostics. Consumer: `comlab/analytics/delta_engine.py`.
- **CONCEPT_DELTA_ABSTAIN** — List of families whose delta signature is uninformative. Consumer: `comlab/analytics/delta_engine.py`.
- **CONCEPT_DELTA_BANDS** — COMLab-local thresholds for trim and gas delta profiles. Consumer: `comlab/analytics/delta_engine.py`.
- **CONCEPT_TEMPORAL_ALIGN** — Hold times and exhaust lag alignment logic. Consumer: `comlab/analytics/delta_engine.py`.
- **CONCEPT_DELTA_UNCERTAINTY** — Z-score normalization propagating measurement uncertainty. Consumer: `comlab/analytics/delta_engine.py`.
