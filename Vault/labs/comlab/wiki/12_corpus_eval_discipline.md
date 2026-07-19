---
chunk_id: COMWIKI-12
title: "Corpus Quality, the Achievable Ceiling & Phase-0 Gates"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: "R1 / pack C: data is the binding constraint, not the logic. The measured achievable ceiling is 70–80%, not 85%. Defines the provenance/label-noise/separability/sim-to-real discipline and the cheap, decisive Phase-0 measurements and gates that must report before the big build."
entities_defined: [CONCEPT_CEILING, CONCEPT_LABEL_NOISE, CONCEPT_SEPARABILITY, CONCEPT_SIM_TO_REAL, RULE_ABSTAIN_LOWSUPPORT, GATE_DATA, GATE_CAPTURE, CONCEPT_PHASE0]
related_chunks: [COMWIKI-02, COMWIKI-09, COMWIKI-10, COMWIKI-11, COMWIKI-14]
sources: [REWORK_PLAN_COMLab.md §1/§2/§3.C, AUDIT_ANSWERS_COMLab.md Q2, AUDIT_PART1_CEILING_RESEARCH.md, OPEN_LEVERS_COMLab.md, "research pack C"]
---

# Corpus Quality, the Achievable Ceiling & Phase-0 Gates

## Data is the binding constraint (R1) {#CONCEPT_CEILING}

The ~50 % plateau is **more likely the corpus than the model**: ~250–280 cases, 12 classes,
single-digit minority families, partly synthetic / hand-filled values, ambiguous sentinels
(±127, 999), and one evidence state (`TIMING_RETARDED`, ~25 % of cases) mapping to ~7 families
(pack C exec summary). The audit's triage agrees: a provable irreducible **floor ~9.6 %** (27
`ecu_fault` STOP cases where the signal is absent) and a realistic ceiling in the **70–80 %**
band — **85 % is not reachable on the current four single-point channels** (`AUDIT Q2`). [v2: R1]

This changes both the product target and the engineering target. **Do not chase 85 %** — set the
target from Gate-Data (`COMWIKI-14` human gates).

## Label noise caps the ceiling {#CONCEPT_LABEL_NOISE}

Label noise mechanically caps achievable agreement at **≈ 1 − r** (15 % noise → ~85 % ceiling;
pack C §label-noise). Re-audit labels on the eval subset with **confident-learning / Cleanlab**
and **inter-rater κ reported with raw agreement and class-wise confusion** (never κ alone);
publish the implied ceiling. Gate any "accuracy improved" claim on this subset. [v2: C.Q1]

## Separability & irreducible error {#CONCEPT_SEPARABILITY}

Compute class-overlap, feature–label mutual information, and a **Bayes-error bound** on the eval
subset; quantify the `TIMING_RETARDED` → ~7-family slice (local ceiling ~1/7 ≈ 14 % absent new
signal). This is the quantitative form of audit Q2 and the test of whether R3's delta
(`COMWIKI-11`) is the *only* way past the slice. [v2: C.Q3]

## Sim-to-real gap {#CONCEPT_SIM_TO_REAL}

Before trusting any number from the synthetic corpus, run a **real-only holdout** + a
classifier-two-sample / **MMD test** (synthetic vs real distinguishable above chance → synthetic
is not yet a valid proxy). This is a Gate-Data exit criterion. [v2: C.Q4]

## Sample size, imbalance & abstention {#RULE_ABSTAIN_LOWSUPPORT}

Report **per-family recall with binomial CIs**; do **not certify** families with **< 10 cases**;
treat single-digit families as **anecdotal** — route to the differential, not a hard verdict
(`COMWIKI-10` `RULE_LOWSUPPORT_FLAG`). Resampling cannot create absent separation; flag
minority families as **low-support** in the output. [v2: C.Q5]

## Phase-0 — decide before building {#CONCEPT_PHASE0}

These cost little, need no new data (except Gate-Data, which is the point), and each resolves a
strategic fork. **Nothing in the fusion/calibration/delta build should start before these
report** (REWORK_PLAN §2).

| # | Action | Decides |
|---|---|---|
| **M1** | histogram `winner_score − correct_rule_score` over OUTRANKED | whether **any** bounded discriminator (≤0.10) can work; if most gaps > 0.10, **stop weight-tuning** — only re-architecture or new signal helps. **Highest-value single experiment.** |
| **M2** | count `degradation_mode` (FULL_FUSION vs GAS_DOMINANT) | whether the ceiling is gas-bound (then OBD-side fusion can't move it) |
| **M3** | count valid payloads silently rejected at Stage-A (O₂ enum gap, DTC hex/decimal regex) | free recall recoverable before any rework |
| **F1** | consolidate the two registries (REG-V2 shim ↔ `global_fault_registry`) | known **+4 cases → 52.7 %** earned gain; unblocks the harness |
| **F3** | reconcile dual engine-warmed thresholds (70 °C vs 75 °C — `COMWIKI-04`) | removes inconsistent gating |

### GATE_DATA {#GATE_DATA}

Build a **measured-real, provenance-audited evaluation subset** — provenance flags
(`COMWIKI-02` `CONCEPT_PROVENANCE`: observed / derived / imputed / synthetic / manual-override /
sentinel / out-of-range / saturated); re-audit labels (confident-learning + κ with raw
agreement); estimate Bayes/irreducible error. **Fixes the real accuracy target** and tests the
"data is the constraint" hypothesis. Calibration (`COMWIKI-09`) and any accuracy claim depend on
this subset existing.

### GATE_CAPTURE {#GATE_CAPTURE}

Product/field decision (dominates the delta rework): **can the workflow capture a low-idle +
elevated/stress frame pair?** The GAS/OBD schemas already support it (`COMWIKI-11` §8.1) — this is
a **corpus/workflow population** decision, not a build. **Yes** → the delta rework (R3, highest-
leverage new signal) is real. **No** → record DeltaLab deferred-pending-data; lean on the
fusion/calibration/differential phases only.

**Phase-0 exit = two numbers + two flags:** (a) measured achievable ceiling on a clean eval
subset; (b) the OUTRANKED score-gap distribution; (c) Gate-Capture yes/no; (d) Gate-Data eval
subset exists yes/no.

## Graph relations (explicit)

**CONCEPT_CEILING** IS **70–80 % (not 85 %)** WITH **~9.6 % irreducible floor**
**CONCEPT_LABEL_NOISE** CAPS **agreement at ≈ 1−r**
**GATE_DATA** REQUIRED_BY **CONCEPT_CALIBRATION (COMWIKI-09)** AND **any accuracy claim**
**GATE_CAPTURE** GATES **live value of T-COMV2-DELTA-1 (COMWIKI-11)**
**M1** DECIDES **whether weight-tuning is dead** (skip F2 if gaps > 0.10)
**F1** YIELDS **+4 cases → 52.7 %** earned gain
**RULE_ABSTAIN_LOWSUPPORT** ROUTES **<10-case families** TO **differential (COMWIKI-10)**

## Core Entities

- **CONCEPT_CEILING** — Measured achievable performance ceiling (70-80%) bounded by corpus quality. Consumer: `COMLab validation`.
- **CONCEPT_LABEL_NOISE** — Inter-rater label disagreement capping diagnostic accuracy. Consumer: `COMLab validation`.
- **CONCEPT_SEPARABILITY** — Bayes error bound and mutual information class overlap. Consumer: `COMLab validation`.
- **CONCEPT_SIM_TO_REAL** — Synthetic vs real domain shift verification test. Consumer: `COMLab validation`.
- **RULE_ABSTAIN_LOWSUPPORT** — Low-support family classification routing. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **GATE_DATA** — Measured-real provenance-audited validation subset. Consumer: `COMLab validation`.
- **GATE_CAPTURE** — Workflow decision verifying second operating point availability. Consumer: `COMLab validation`.
- **CONCEPT_PHASE0** — Phase-0 research validation gates. Consumer: `COMLab validation`.
