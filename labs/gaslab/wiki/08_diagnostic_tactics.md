---
chunk_id: GASWIKI-08
title: "Diagnostic Tactics & Pre-Test Conditions"
doc: GAS_WIKI
version: v2.0
summary: "Pre-test checklist, lambda-mismatch test, and the weird-gases decision tree — plus the two v2 procedures: the idle→2500 RPM family-separation matrix and the probe-occlusion test for sampling-leak isolation."
covers_v1_sections: [11]
entities_defined: [TEST_PRECONDITIONS, TEST_LAMBDA_MISMATCH, TEST_WEIRD_GASES_TREE, TEST_RPM_SEPARATION_MATRIX, TEST_PROBE_OCCLUSION]
related_chunks: [GASWIKI-04, GASWIKI-05, GASWIKI-06A, GASWIKI-06B, GASWIKI-07]
sources: ["GAS_WIKI.md v1.0 §11", "research q3", "research q7", "research q4"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "diagnostic-tactics"
implements:
  - "labs/gaslab/gaslab/rule_engine.py"
  - "labs/gaslab/gaslab/resolution.py"
  - "labs/gaslab/gaslab/process.py"
consumers:
  - "gaslab: labs/gaslab/gaslab/rule_engine.py dual-reading and block-test path"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py lambda mismatch comparison"
drift_guards:
  - "labs/gaslab/tests/unit/test_rule_engine.py"
  - "labs/gaslab/tests/unit/test_resolution.py"
  - "labs/gaslab/tests/unit/test_process.py"
tags: ["gaslab", "diagnostic-tactics", "wiki"]
source: "labs/gaslab/wiki/08_diagnostic_tactics.md"
---

# 8. Diagnostic Tactics

> **Chunk summary.** The pre-test conditions and the bench tactics GASLab reasoning assumes, including the v2 RPM-differential family-separation matrix and the probe-occlusion sampling-leak test.

## 8.1 Pre-test conditions {#TEST_PRECONDITIONS}

| Check | Reason |
|---|---|
| Engine warm (ECT > 60 °C / past light-off) | Operating envelope; cold samples out of scope |
| 5-gas analyser confirmed (NOₓ channel live) | Operating envelope; no 4-gas fallback |
| Probe seated, no leaks | Triangle gate confirms; otherwise abort (→ TEST_PROBE_OCCLUSION) |
| Analyser zeroed against ambient | Drift skews CO₂ and O₂ |
| Vehicle stabilised at idle ≥ 60 s | OBD trims need time to settle |

## 8.4 Lambda-mismatch test (sensor fraud) {#TEST_LAMBDA_MISMATCH}

Compare λ from GASLab (chemistry) with λ from the ECU's upstream sensor — thresholds at → RULE_LAMBDA_MISMATCH; expected per-fault magnitudes at → CONCEPT_DIVERGENCE_MAGNITUDE.

## 8.5 The "weird gases" decision tree {#TEST_WEIRD_GASES_TREE}

| Symptom | First check | Rationale |
|---|---|---|
| O₂ high + low NOₓ + low CO | Misfire mask | Heat must have been there to make NOₓ |
| O₂ high + high NOₓ | Real lean | Heat present → thin, not unlit |
| CO high + O₂ high | Triangle | Sum > 16 % → ingress; normal → rich misfire |
| HC > 2000 ppm | Cylinder contribution | Likely mechanical / oil |
| All four normal + NOₓ high | EGR / cooling / timing | Engine fine but burning hot |
| Triangle sum > 18 % | Probe not in pipe / engine off | Refuse to diagnose |
| High O₂, low CO, low HC, λ false-lean | STFT + probe occlusion | Distinguish real leak from sampling leak (→ TEST_PROBE_OCCLUSION) |

## 8.9 The idle→2500 RPM family-separation matrix {#TEST_RPM_SEPARATION_MATRIX}

`[v2: q7, q4]` The single most powerful on-site tactic for separating the candidate families is to watch how the five gases and λ move from low idle (~750 RPM) to high idle (2500 RPM). The defining question for each family is **does the signature normalise, persist, or worsen with RPM?**

| Family | Low idle | At 2500 RPM | Separating mechanism |
|---|---|---|---|
| **Lean (vacuum/fuel)** | O₂ > 3 %, CO < 0.1 %, HC 150–400, λ > 1.15 | O₂ < 1 %, CO₂ 14–15 %, HC < 50, λ → 1.0 | A fixed vacuum leak becomes insignificant against metered air at 2500 → **normalises** |
| **Catalyst (failing)** | CO₂ > 12 %, CO 0.5–1.5 %, HC 100–300, λ 0.995–1.005 | same | λ stays perfectly stoich; high CO₂ proves in-cylinder combustion is fine → cat-only fault |
| **Sensor (biased O₂/MAF)** | rich bias: CO > 3 %, O₂ < 0.2 %, λ < 0.85 | CO stays > 3 %, λ < 0.85 | Sensor offsets are flat/continuous → **do not normalise** with RPM |
| **Misfire (electrical)** | HC > 1000, O₂ > 3 %, CO < 0.2 %, CO₂ < 10 % | persists | Raw air+fuel in strict ratio; CO stays low (no combustion in that cylinder) |
| **ECU timing (adv/ret)** | advanced: HC 120–250, CO < 0.2 %, NOₓ ~ 0 | advanced: NOₓ > 1200, λ ~ 1.0, MAP normal | Vacuum stays healthy; λ held at 1.0 by closed loop → no trim corrections |
| **Mechanical (valve/rings)** | burnt valve: HC > 500, O₂ > 2 %, CO₂ < 11 % | burnt valve: HC drops > 50 %, CO₂ rises | Localised fixed leak masked by velocity at speed; jumped cam affects all cylinders continuously |

**Oil-burn sub-cut** (once misfire is ruled out by HC magnitude): **HC drops sharply** at 2500 ⇒ worn valve seals; **HC + CO rise** at 2500 ⇒ worn piston rings; **HC flat, moderate** ⇒ generally worn engine; **HC extreme but λ perfectly stoich, CO ≈ 0** ⇒ turbo turbine-seal oil leak; **NOₓ fails to rise** with high O₂ ⇒ internal coolant/head-gasket leak. See → CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR (GASWIKI-06A).

> Deeper OBD-II isolation for timing faults — DTC correlation (P0016–P0019), Mode `$06` MID/TID, freeze-frame, and in-cylinder pressure waveform (EVO/IVO/IVC phasing) — sits outside GASLab's tailpipe-only emit boundary and is owned by **OBDLab / DTCLab**. GASLab consumes their verdicts as corroboration, not as inputs to `chemical_state`.

## 8.10 The probe-occlusion test (sampling-leak isolation) {#TEST_PROBE_OCCLUSION}

`[v2: q3]` When the analyser shows high O₂ / false-lean λ but the engine runs smoothly and OBD STFT is ≈ 0, suspect a leak in the sampling apparatus rather than the exhaust. **Procedure:** block the probe tip (e.g. with a finger). On an intact system the vacuum pump should stall and the O₂ reading should drop to near 0 %. If O₂ does **not** drop, there is a physical leak in the sampling hose/fittings — the "lean" is an artefact. Pair with the STFT correlation in → CONCEPT_LEAK_VS_SAMPLING before emitting `EXHAUST_AIR_LEAK`.

## Graph relations (explicit)

**TEST_PRECONDITIONS** GATED_BY **warm engine, closed-loop, 60 s stabilised idle**
**TEST_PRECONDITIONS** CONSUMES **engine_state_bucket = STABILIZED_IDLE**
**TEST_LAMBDA_MISMATCH** DETECTS **truth-vs-perception divergence** — Δλ > 0.08 triggers override
**TEST_LAMBDA_MISMATCH** CONSUMES **CONCEPT_DIVERGENCE_MAGNITUDE** per-fault Δλ table
**TEST_LAMBDA_MISMATCH** ROUTES_TO **RULE_LAMBDA_MISMATCH** (GASWIKI-04)
**TEST_WEIRD_GASES_TREE** ROUTES_TO **fault atlas** — narrows candidates by gas pattern direction
**TEST_WEIRD_GASES_TREE** CONSUMED_BY **gaslab.rule_engine._matching_fault_candidates**
**TEST_RPM_SEPARATION_MATRIX** DISAMBIGUATED_BY **idle vs 2500 RPM gas delta** — separates ignition vs cam timing, weak vs dead cat, oil-burn leaf faults
**TEST_RPM_SEPARATION_MATRIX** ROUTES_TO **TEST_DUAL_IDLE_CATALYST** (catalyst arm) and **CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR** (oil-burn arm)
**TEST_RPM_SEPARATION_MATRIX** CONSUMED_BY **gaslab.rule_engine._resolve_candidates** (dual-reading path)
**TEST_PROBE_OCCLUSION** VERIFIES **sample-stream integrity** — blocks probe tip, O₂ must drop to near 0 %
**TEST_PROBE_OCCLUSION** CONFIRMS **CONCEPT_LEAK_VS_SAMPLING** — sampling leak vs real exhaust leak
**TEST_PROBE_OCCLUSION** GATES **FAULT_EXHAUST_AIR_LEAK** — do not emit without probe test passed
**FAULT_IGNITION_MISFIRE** CONSUMES **GasLabDnaView.cylinder_count** via `inferred_misfiring_cylinder_count ≈ O₂ / (21 / N)`

## Core Entities

- **TEST_PRECONDITIONS** — warm engine, closed-loop, 60 s stabilised idle. Gates all gas interpretation. Consumer: `rule_engine.classify` entry guard.
- **TEST_LAMBDA_MISMATCH** — chemistry λ (Brettschneider) vs ECU λ comparison; Δλ thresholds: ≤0.05 proceed, 0.05–0.08 borderline, >0.08 override. Consumer: `RULE_LAMBDA_MISMATCH`.
- **TEST_WEIRD_GASES_TREE** — gas-pattern direction triage narrowing candidates for fault matching. Consumer: `rule_engine._matching_fault_candidates`.
- **TEST_RPM_SEPARATION_MATRIX** — idle vs 2500 RPM comparison: separates ignition vs cam timing, weak vs dead cat, oil-burn leaf faults. Consumer: `rule_engine._resolve_candidates` (dual-reading path with `reading_high`).
- **TEST_PROBE_OCCLUSION** — block probe tip → O₂ must drop ≈ 0 %; if not, sampling apparatus leaks. Consumer: `block_test_passed` parameter in `rule_engine._definitive_match`.
