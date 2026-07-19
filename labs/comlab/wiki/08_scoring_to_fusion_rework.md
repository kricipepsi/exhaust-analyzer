---
chunk_id: COMWIKI-08
title: "From Additive Scoring to Conflict-Aware Late Fusion"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: "R2 of the rework: the additive prune-then-rank tie-break has hit its ceiling; replace Stage-B's 'highest additive score wins' with a calibrated, conflict-aware late-fusion stage. The 13 forward-registered T-COMV2-* consumers become evidence inputs to this stage, not independent additive bumps."
entities_defined: [FUSE_CONFLICT_AWARE, FUSE_INV_VARIANCE, FUSE_CONTRADICTION, FUSE_LOGODDS, FUSE_DS_PCR5, CONCEPT_EVIDENCE_INPUTS]
related_chunks: [COMWIKI-07, COMWIKI-09, COMWIKI-11, COMWIKI-13]
sources: [REWORK_PLAN_COMLab.md §3.A/§3.E/§4, AUDIT_PART1_CEILING_RESEARCH.md, OPEN_LEVERS_COMLab.md, "research packs A + E", tasks/PROGRESS.md]
---

# From Additive Scoring to Conflict-Aware Late Fusion

## Why the additive ranker is replaced (R2)

The OUTRANKED bucket (~82–90 cases — the whole game) loses because a generic rule's higher
`base_weight` beats the correct specific rule, and the intended tie-breaker (the DTC routing tag,
weight 0.10) is **starved**: 64/90 OUTRANKED cases carry no DTC (`AUDIT Part 1 §1.1`). Two
ledger-proven facts bound the additive paradigm:

- Bounded-additive nudges and coverage rescues moved **0 pp** (`AUDIT §2 Wave E`).
- A hard contradiction *override* measured **net-negative** (`AUDIT §1.2 Culprit 2`).

Pack A confirms hand-tuned additive weight engines have an **inherent ceiling** below
calibrated/learned fusion on comparable noisy multi-class tasks. **Decision:** freeze the
additive ranker as the **fallback (`SINGLE_POINT`) path only** and re-architect Stage-B Phase 5
(`fault_atlas_router.execute_triage_loop`) from "highest additive score wins" to a **calibrated
fusion stage**. Do **not** invest further in `base_weight` tuning ("scoring tightening is a
smell", `AUDIT §3`) — skip weight-tuning unless `OPEN_LEVERS M1` shows score-gaps < 0.10
(`COMWIKI-12`). *Files:* `core/fault_atlas_router.py`, new fusion stage. [v2: A.Q1]

## The conflict-aware late-fusion stage {#FUSE_CONFLICT_AWARE}

The new stage takes per-channel evidence and combines it into a calibrated posterior, using
disagreement as information rather than discarding or overriding it.

```
evidence (13 T-COMV2-* consumers + per-lab deltas)
   ├─ agreement  → corroborating mass        (confidence up, no double-count)   A.Q2 / E.Q3
   ├─ disagreement → conflict mass mapped to a specific fault                   E.Q3
   ├─ inverse-variance weighting (anti-swamping)                                A.Q3
   └─ Bayesian log-odds first  →  DS/PCR5 where high-conflict cases demand it   E.Q4
   ▼
fused score → CALIBRATION (COMWIKI-09) → RANKED DIFFERENTIAL (COMWIKI-10)
```

### Inverse-variance weighting — prevent channel swamping {#FUSE_INV_VARIANCE}

Under correlated channels, naive product fusion swamps weak-but-reliable channels (A §3). Each
lab's evidence is weighted by its **measurement uncertainty** so reliability, not raw magnitude,
drives the result (E.Q2/Q4).

**σ source (reality check, REWORK_PLAN §8.2):** the reworked emitters emit a *categorical*
`SampleValidity` / gate enum, **not** a numeric per-reading σ. So `σ_meas` is taken from
**analyzer/scan-tool specifications** (the ±-bands in `COMWIKI-11`) and the emitted validity enum
is used as a **hard abstain gate** (invalid → that channel abstains), never as σ. [v2: §8.2]

### Contradiction as a feature, not an override {#FUSE_CONTRADICTION}

`core/perception_contradiction.py` already emits a contradiction flag. The rework feeds gas↔OBD
agreement/disagreement into the fusion stage as **evidence** (per the cross-reference logic table,
`COMWIKI-11` `RULE_CROSSREF`): a conflict **raises** confidence for the fault it implies (e.g.
*gas lean + OBD trim-null → speed-density leak*) and is surfaced as a global "check sensors" tier
only when it cannot be localised (E.Q4). It is **never** a forced win — that was the net-negative
override. [v2: A.Q2]

### Combiner: staged, to avoid over-engineering {#FUSE_LOGODDS}{#FUSE_DS_PCR5}

1. **Start** with **inverse-variance-weighted Bayesian log-odds + an explicit conflict feature** —
   the simplest form that yields calibrated posteriors and uses conflict (E.Q4 Option B).
2. **Adopt conflict-aware Dempster–Shafer (PCR5/Yager)** only where the log-odds form is shown to
   mishandle high-conflict cases (E.Q4 Option A). DS handles non-commensurate data + uncertainty +
   conflict natively and needs no training data, but has a known high-conflict pathology — hence
   the conflict-aware rule. Its thresholds are **expert priors until calibrated** on the Gate-Data
   subset (`COMWIKI-12`).
3. **Defer stacking** until a paired/field dataset exists.

Web-settled ordering refinement (REWORK_PLAN §8.4): **calibrate each modality first, then fuse**.
*Graceful degradation:* one modality abstains → fall back to the other with widened confidence;
both abstain → "insufficient data." *Files:* new fusion stage, `core/fault_atlas_router.py`,
`core/lab_pipeline_aggregator.py`. [v2: E.Q4]

## The 13 evidence inputs (forward-registered consumers) {#CONCEPT_EVIDENCE_INPUTS}

The structural change that unifies the rework: the `T-COMV2-*` rows stop being independent
additive bumps and become **evidence inputs to the fusion stage**. They are forward-registered in
`tasks/PROGRESS.md` (each is the named reader that closes anti-orphan on an emitted field at
Stage-4 close). Full register with code paths + proposal IDs: `COMWIKI-13`.

| Consumer | Fuses | Verdict it informs |
|---|---|---|
| `T-COMV2-ECU-FUSE-1` | OBD `lambda_perception_delta` + bank symmetry + GAS `lambda_chem` | ecu_fault (perception vs reality) |
| `T-COMV2-BANK-FUSE-1` | OBD `per_bank_trim_delta` (±5 % bound) | bank-asymmetry |
| `T-COMV2-VE-GATE-1` | OBD `ve_pct`/`ve_validity`/`air_metering_strategy` | VE fault (independent only when DUAL_MAF_MAP) |
| `T-COMV2-O2OFFSET-1` | OBD `WIDEBAND_OFFSET_CANDIDATE` + GAS `lambda_chem` | wideband-calibration sensor_fault |
| `T-COMV2-NOSTART-1` | DTC Mode-06 monitor-aborted + FF cut-state | security-lockout vs mechanical no-start |
| `T-COMV2-FUELSYS-GATE-1` | OBD `fuel_system_status` (CL/OL/OL_FAULT) | gate trim routing when not closed-loop |
| `T-COMV2-ECU-HW-1` | OBD IAT/TPS/ECT + bank symmetry | internal-ECU "digital-lie" fault |
| `T-COMV2-VPWR-GATE-1` | OBD `control_module_voltage_v` | suppress sensor-fault routing on bad rail |
| `T-COMV2-MISFIRE-LOC-1` | OBD `per_cylinder_misfire_counts` | single-cylinder vs global starvation |
| `T-COMV2-MAF-LIN-1` | OBD `w_theo` + `sensor_error_delta` | ERR-LC-002 vs open-circuit P0102 |
| `T-COMV2-LTFT-CELL-1` | OBD `ltft_cell_vector` | idle-only / part-throttle / global lean |
| `T-COMV2-CTXMOD-1` | SymptomLab `load_state` | symptom-prior context modifier (cap 65 %) |
| `T-COMV2-DELTA-1` | per-state two-point frames → `delta_signature` | the new primary-rank discriminator (`COMWIKI-11`) |

## Graph relations (explicit)

**RULE_SCORING (COMWIKI-07)** REPLACED_BY **FUSE_CONFLICT_AWARE**
**13 T-COMV2-\* consumers** ARE **CONCEPT_EVIDENCE_INPUTS** TO **FUSE_CONFLICT_AWARE** (not additive bumps)
**FUSE_INV_VARIANCE** USES **analyzer-spec σ** GATED_BY **SampleValidity enum** (not numeric σ)
**FUSE_CONTRADICTION** FEEDS **conflict as evidence** (never a forced override)
**FUSE_LOGODDS** PRECEDES **FUSE_DS_PCR5** (adopt DS only on high-conflict cases)
**fusion output** CALIBRATED_BY **COMWIKI-09** THEN **CONCEPT_DIFFERENTIAL (COMWIKI-10)**
**additive ranker** FROZEN_AS **SINGLE_POINT fallback**

## Core Entities

- **FUSE_CONFLICT_AWARE** — Late fusion combiner stage for multi-channel evidence. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **FUSE_INV_VARIANCE** — Measurement uncertainty scaling for Bayesian evidence combining. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **FUSE_CONTRADICTION** — Gas vs OBD sensor disagreement treated as diagnostic evidence. Consumer: `comlab/core/perception_contradiction.py`.
- **FUSE_LOGODDS** — Bayesian log-odds combiner stage for posterior calculation. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **FUSE_DS_PCR5** — Dempster-Shafer Yager combiner for high-conflict scenarios. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
- **CONCEPT_EVIDENCE_INPUTS** — The 13 evidence signals mapped into conflict-aware fusion. Consumer: `comlab/core/lab_pipeline_aggregator.py (proposed)`.
