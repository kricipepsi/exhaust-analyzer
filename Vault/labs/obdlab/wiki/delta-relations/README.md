---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "delta-vector-scoring"
implements:
  - "labs/obdlab/code/core/ve_engine.py"
consumers:
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — lambda-delta-vector scoring"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py"
drift_guards:
  - "labs/obdlab/tests/unit/test_ve_engine.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/delta-relations/README.md"
---
# chunks/delta-relations/ — index & unhomed-content log


**Date:** 2026-06-07 · **Step:** Phase 2 delta-relations extraction (staging).
**Source of record:** `sources/fuel-trim/FuelTrimW.md` — the readable copy of the
"Fuel Trim Diagnostics Wiki Preparation" HTML report. The HTML export failed the
CLAUDE.md readability gate (formulas + numeric literals were images); `FuelTrimW.md`
restores them as LaTeX/text and **passes** the gate.
**Provenance:** Gemini share https://gemini.google.com/share/23ff406a7345

> **Whole-folder status: STAGING.** Every chunk here is `consumer: PENDING`. The
> named consumer — the COMLab delta-calculation script (SWEEP_MANIFEST §7, FU-2) —
> does not exist. Under the signal/noise rule nothing in this folder ships into the
> engine until FU-2 is specced and a live code path reads ΔTrim. These chunks
> preserve the formulas + magnitudes so that spec can be written against ground truth.

## Chunk set (delta-specific content only)

| Chunk | Concept | ΔTrim signature |
|---|---|---|
| `01_delta-method-and-formula` | ΔTrim definition, idle bands (600–800 / 3500–4500 RPM), improve-vs-worsen axis | — |
| `02_profile-vacuum-leak` | idle +15…+25 % → stress ≈0…+5 % | ΔTrim ≤ −10 % |
| `03_profile-fuel-starvation` | idle ≈0…+5 % → stress +15…+25 % | ΔTrim ≥ +10 % |
| `04_profile-maf-underreport` | idle ≈0…+8 % → stress +15…+30 % | ΔTrim ≥ +10 % |
| `05_profile-exhaust-backpressure` | idle ≈0 % → stress ≤ −12 % | ΔTrim ≤ −10 % |
| `06_architecture-modifiers` | Speed-Density paradox (ΔTrim≈0 for leak) + turbo boost-leak sign inversion | gate before 02–05 |

## Dedup vs the fuel-trim pass

`fuel-trim/04_trim-pattern-decision-tree` carries the **static** idle-vs-2500–3000 RPM
pattern table for live fault-atlas routing (active now). This folder carries the
**quantified ΔTrim** at the 3500–4500 RPM **stress** band for the future delta script
(PENDING). They are complementary, not duplicate: chunk 04 routes; these quantify the
delta the script will compute. Profile 4 (exhaust backpressure) has no row in chunk 04
— it is a delta-only signature.

## Unhomed content in this feeder (NOT chunked — out of delta scope)

`FuelTrimW.md` is rich beyond delta. The following unique, now-readable content was
**deliberately left unhomed** (delta-only scope this session; "deliverables only").
Logged so it is not lost:

| Content | Natural home | Note |
|---|---|---|
| OBD-I↔OBD-II conversion: `Trim% = ((Value−128)/128)×100%`, 0–255 scale, 128 baseline | pids-protocol (PID encoding) | unique formula; image-locked in HTML, readable here |
| KAM & fuel-trim **cell matrix** (RPM×load), VT V8 cell-selection (Cell 0/16/17/33), WOT STFT-freeze | fuel-trim (cell modeling) | explains cell-dependent idle trims |
| VAG **additive/multiplicative** trim (Group 032): `t_inj=t_base±t_add`, `t_inj=t_base×(1±Mult%)`, ±10 % spec | fuel-trim (mfr trim representation) | unique to VAG |
| BMW DME open-loop trim application + AFM cutoff > 4500 RPM | fuel-trim / o2-logic | mfr-specific |
| Gen III LS1 **DTC enabling window** (ECT 50–115 °C, BARO >74 kPa, MAF 5–90 g/s, MAP 26–90 kPa, IAT −20–90 °C, RPM 400–3000, TPS <90 %, VSS <137 km/h, 6 s) | fuel-trim/03 (DTC thresholds) | unique numeric run-condition set |
| EGR / ignition-misfire false-lean / fuel-oil chemistry / flex-fuel trim effects | fuel-trim/04 + o2-logic | partly overlaps existing chunks; static not delta |
| Physical tests (smoke, fuel-pump current ramping, O₂ waveform) | procedure ref | likely not KG-routable |

## Follow-ups

| ID | Item |
|---|---|
| DR-FU-1 | Home the unhomed table above into fuel-trim / pids-protocol / o2-logic passes (esp. the Gen III DTC window and OBD-I conversion formula — both unique + image-locked). |
| FU-2 (existing) | Spec the COMLab delta-calculation script — the consumer that flips every chunk here from PENDING to active. |
| FT-FU-B | Second HTML report `Fuel Trim Diagnostics Across Fault Families/` (169 imgs) still needs a readable `.md` (user to provide) before its gate can pass. |

---

## Volume-sweep additions (2026-06-07 — sources/various/)

| Chunk | Concept | ΔTrim/Δgas | Status |
|---|---|---|---|
| `07_gas-transition-matrix-2speed` | Vol7 25-case 5-gas low→2500 RPM transition matrix (GAS-* IDs) | Δgas side (tailpipe), pairs with 01–05 ΔTrim (OBD side) | PENDING (FU-2) |
| `08_vsum-sample-validity-gate` | Vol7 vsum 14–18 % + CO+CO₂≤6 % dilution gate | sample-validity guard before any Δ/λ | PROPOSAL (GASLab gate) |

⚠ Band conflict reaffirmed: Vol7 stress band = **2500 RPM**; FuelTrimW delta chunks
(01–05) = **3500–4500 RPM**. Reconcile in FU-2 / O2-FU-3 before fusing the two sides.
The Vol7 Brettschneider + vsum **display equations were image-stripped** — values in
prose survive; equations logged in the formula wiki pending list, not reconstructed.


## Core Entities

- delta-relations (staging folder)
- DELTA_TRIM, DELTA_GAS, VSUM
- COMLab delta-calculation script (consumer, PENDING FU-2)

## Graph relations (explicit)

**delta-relations** STAGED_FOR **COMLab delta-calculation script**
**delta-relations** COMPLEMENTS **fuel-trim/04_trim-pattern-decision-tree**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
