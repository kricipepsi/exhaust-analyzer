---
node_type: wiki
lab: dtclab
module: dtclab
subsystem: fault-ranking
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py routing-tag discriminator rank step"
drift_guards:
  - "labs/dtclab/tests/unit/test_classify_top3.py"
  - "labs/dtclab/tests/unit/test_rank_candidates.py"
tags: [dtclab, wiki, fault-ranking]
source: "labs/dtclab/wiki/12_ranking_discriminator.md"
---
# 12 — Ranking discriminator: prevalence, fan-out & priority

This chunk closes the DTC10 "starved discriminator" questions: how often a DTC is
even present (Q1), how reliably a generic code points to one family (Q2), which
manufacturer codes are usable without per-OEM databases (Q3), and how to pick the
primary code among several (Q10). The monitor-maturation skew (Q9) lives with the
lifecycle in `01_dtc_state_lifecycle.md §1.4`.

**Provenance:** web-research synthesis in `DTCanswers.md` / `DTCansw2.md`
(2026-06-11, 1990–2010 / Euro 1–5 petrol, SAE J1979) reconciled against the
internal `DTCLab/cases/` corpus (n = 90). All figures here are **reference
material** (no new contract field); they inform the existing COMLab rank/route
step, they do not add schema. See `00_INDEX.md §2`.

---

## 12.1 DTC prevalence at intake (Q1) — the discriminator is starved

A stored DTC is the *exception*, not the rule, on this fleet. Published workshop
data puts ~**60–65%** of emissions/driveability faults as a confirmed (MIL-on)
DTC at intake; the rest are pending-only or no-code. The internal corpus is far
more starved:

| Code status at intake | Published industry avg | Corpus count (n = 90) | Corpus share | Primary driver |
|---|---|---|---|---|
| Confirmed DTC (MIL-on) | 60 – 65% | 21 | 23.3% | Two-trip monitor matured, or one-trip circuit/rationality failure |
| Pending only (MIL-off) | 15 – 20% | 5 | 5.6% | Intermittent / single-trip fail of a two-trip monitor / interrupted cycle |
| **No stored code (MIL-off)** | 15 – 20% | **64** | **71.1%** | Mechanical faults (compression loss, minor vacuum leak, restricted injector) or memory clears |

**Why so many no-code cases.** The ECM diagnostic executive needs specific enable
criteria and thresholds before a monitor runs and matures a fault. Mechanical
faults often produce severe driveability symptoms *long before* tripping an OBD
threshold — e.g. compression loss, sticking EGR, or a post-MAF intake tear can
degrade combustion without crossing a circuit-voltage limit or the **+25% LTFT**
limit needed to set P0171.

**Routing implication (consumer).** This corroborates the chunk `04` thesis: with
~71% of corpus cases code-less, the rank step **cannot lean on DTC presence** — it
must weight fuel-trim, freeze-frame, and Mode `$06` evidence as first-class, and
treat a present DTC as a bonus discriminator, not a precondition. The 64/90 figure
is the same one DTC10 flagged as the core problem.

---

## 12.2 Downstream-artifact mechanics — a stored code is often a symptom

When a code *is* present it is frequently a **downstream artifact** of an upstream
fault, not the root cause. The classic chain: a primary misfire (P030x) pumps
unburned fuel + raw O₂ past the upstream sensor → ECM reads lean, drives trims to
the positive limit → **P0171**; the same raw charge combusts on the catalyst →
overheating → **P0420**. Both the lean and catalyst codes are artifacts of the
misfire.

| Stored downstream DTC | Typical upstream root cause | Artifact frequency | Propagation mechanism |
|---|---|---|---|
| P0171 / P0174 (lean) | Misfire (P030x) or exhaust leak | Moderate (~30%) | Unburned O₂ fools the upstream sensor; exhaust venturi draws atmospheric air |
| P0420 / P0430 (catalyst) | Upstream misfire (P030x) or rich bias (P0172) | High (~40%) | Exothermic combustion of raw fuel sinters the substrate |
| P0101 (MAF perf.) | Downstream vacuum leak or sticking EGR | Low–moderate (~20%) | Calculated-load vs measured-air-mass divergence from unmetered air |

This is *why* §12.6 ranks upstream sensor/source codes above downstream outcomes,
and why chunk `02.4.2` prefers the misfire reading when P030x co-occurs with a
lean code.

---

## 12.3 Generic-code fan-out matrix (Q2) — how weak each code is

A code's discriminating power is its **fan-out**: the spread of real root causes
behind it. Low fan-out ⇒ near-1:1 with a subsystem (strong). High fan-out ⇒ an
"outcome" code spanning many causes (weak — needs freeze-frame / idle-vs-stress
tie-breakers, ECT ≥ 75 °C, RPM).

| Generic DTC | Root-cause distribution (industry) | Corpus cases (of 21) | Corpus share | Discriminator strength |
|---|---|---|---|---|
| **P0171 / P0174** (lean) | Vacuum leak **45%**, MAF contamination **30%**, fuel pressure/delivery **15%**, pre-O₂ exhaust leak **10%** | 6 | 28.6% | **High fan-out — weak.** High trim at idle that corrects at 3500 RPM ⇒ vacuum leak |
| **P0300 / P030x** (misfire) | Secondary ignition **55%**, fuel injection/delivery **25%**, mechanical (compression/valves) **15%**, EGR/vacuum **5%** | 8 | 38.1% | **Moderate.** Per-cylinder P0301–P0308 + Mode `$06` counts localise it |
| **P0420** (catalyst) | Substrate failure **65%**, upstream misfire/trim bias **25%**, downstream-O₂ drift **8%**, calibration **2%** | 4 | 19.0% | **High fan-out — outcome code.** Post-cat O₂ mirroring pre-cat confirms true substrate failure |
| **P0401 / P0402** (EGR flow) | Carbon-blocked passages **60%**, vacuum solenoid/modulator **25%**, transducer drift (DPFE/temp) **15%** | 2 | 9.5% | **Low fan-out — discriminating (~1:1 with EGR).** Commanded-vs-actual EGR position divergence |
| **P0101** (MAF perf.) | Dirty/contaminated MAF **50%**, downstream intake leak **35%**, sensor hardware **15%** | 1 | 4.8% | **Moderate — rationality.** Signal out of range vs calculated volumetric efficiency |

(Corpus cases sum to 21 confirmed-DTC cases.) **Split rule for the outcome codes
(P0171, P0420):** trim strongly positive (**+25%**) at curb idle but correcting
toward nominal (**< +10%**) at ~3500 RPM ⇒ vacuum leak (load dilutes the unmetered
leak); trim flat-or-worse with RPM ⇒ fuel-delivery deficiency or under-reporting
MAF.

---

## 12.4 Manufacturer P1xxx usability without per-OEM databases (Q3)

Under SAE J2012 the 2nd digit governs the code: `0` = generic, `1` =
manufacturer-specific. P1xxx codes generally vary by make/model/year, so they are
**unusable generically** — *except* a small cohort that reached de-facto
cross-OEM consistency in 1990–2010 and can be hard-coded:

| Stable P1xxx | Meaning | Cross-OEM coverage | Maps to |
|---|---|---|---|
| **P1000** | OBD-II monitor status / drive cycle incomplete (status flag, not a fault) | Ford, Jaguar, Mazda, Land Rover | System-status family — readiness incomplete |
| **P1260** | Theft detected — vehicle immobilised (PATS handshake failed) | Ford, Mazda, Jaguar (PATS) | Security/immobiliser — explains a non-start (chunk `10`) |
| **P1101** | MAF out of self-test (KOEO/KOER) range | GM, Ford, Opel | Air-metering family — MAF rationality |

```
P1000 ──> System status      ──> Emissions readiness incomplete
P1260 ──> Security/immobiliser ──> PATS key-handshake failure
P1101 ──> Air metering        ──> MAF signal out of rationality range
```

**Everything else is unstable.** e.g. P1404 = EGR closed-position error on GM/
Chrysler but a different circuit entirely on European/Asian makes — interpreting
it generically routes the tech to the wrong component.

**Feasibility verdict (Q3):** implementing P1xxx generically is **unfeasible**
except the restricted Ford-Mazda-Jaguar PATS/readiness subset plus P1101 above,
where the mapping is functionally standardized. P1260 is the highest-value entry —
it turns an unexplained non-start into an immediate immobiliser verdict.

---

## 12.5 Primary-code priority hierarchy (Q10)

Two layers govern which of several simultaneous codes is "primary."

**Layer 1 — the ECM's own freeze-frame priority (SAE J1979, Mode `$02`).** Only one
freeze frame is stored, so the executive ranks who owns it:

- **Priority 1 (highest):** fuel-system monitors (P0171/P0174…) **and** misfire
  monitors (P0300/P030x).
- **Priority 2:** all other non-continuous emissions monitors (EGR, catalyst,
  EVAP, O₂).

A Priority-1 event **overwrites** a stored Priority-2 freeze frame; an equal-
priority later event does **not** overwrite (the earliest high-priority event is
preserved). So the freeze frame itself is a clue to the primary fault.

**Layer 2 — the professional five-tier hierarchy** (root-level → downstream):

| Rank | Fault family | Basis | Representative codes |
|---|---|---|---|
| 1 | Severe safety / catalyst-damage | Flashing MIL ⇒ immediate stop, protect the catalyst | P0300 (Type A misfire — chunk `06`) |
| 2 | Module power, ground & comms | Bad ECM voltage / bus failure skews every reading | U0100 (lost comms), P0562 (low system voltage) |
| 3 | Sensor circuit hard faults (CCM) | A shorted/open circuit must be fixed before its rationality means anything | P0102 (MAF low), P0112 (IAT low), P0117 (ECT low) |
| 4 | Systemic air/fuel rationality | Loop-level feedback across the bank | P0171/P0174 (lean), P0101 (MAF perf.) |
| 5 | Downstream outcomes / non-continuous | Post-combustion/tank results; prone to false positives | P0420 (catalyst), P0401 (EGR flow), P0442 (EVAP) |

**Tie-breaks within a tier** (apply in order):

1. **Freeze-frame anchor** — the code holding the Mode `$02` freeze frame is the
   earliest matured failure; anchor to it.
2. **Confirmed `$03` > pending `$07`** — a matured code outranks an intermittent
   single-trip one.
3. **Upstream sensor > downstream outcome** — with both an air/fuel sensor code
   and an emissions outcome code (e.g. P0101 + P0171), treat the upstream sensor
   code as primary; the outcome follows from the bad sensor data.

**Worked chain** (resolve top-down; fixing rank 1 collapses the artifacts):

```
        P0300 (Misfire — Priority 1)
                  │  raw fuel + unburned O₂ enter exhaust
                  ▼
        P0171 (Lean — tier 4)
                  │  exothermic overload of the catalyst
                  ▼
        P0420 (Catalyst — tier 5)
```

**Consumer.** This ordering + tie-break set is the convention the COMLab rank step
adopts to pick the primary code and demote artifacts; it consolidates the
fragments previously scattered across chunks `01` (state), `02.4.2` (misfire-mask),
`06.4` (Type A escalation), and `10` (immobiliser-first).

## Graph relations (explicit)

**P1000** INDICATES **readiness incomplete**
**P1101** INDICATES **MAF out of self-test range**
**P1260** INDICATES **immobiliser lockout**
**Priority 1** OVERWRITES **Priority 2** freeze-frame
**misfire** outranks **lean_condition** (downstream artifact rule)
**misfire** outranks **catalyst_failure** (downstream artifact rule)
**lean_condition** outranks **catalyst_failure** (downstream artifact rule)
**Layer 2 priority hierarchy** RANKS **misfire** ABOVE **ecu_fault** ABOVE **sensor_fault** ABOVE **lean_condition** ABOVE **catalyst_failure**
**Tie-breaks** RESOLVES **simultaneous DTCs**

## Core Entities

- **P1000** — Manufacturer DTC indicating OBD-II monitor status incomplete. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **P1101** — Manufacturer DTC indicating MAF sensor out of self-test range. Consumer: `dtclab/config/routing_tag_map.yaml`.
- **Layer 2 priority hierarchy** — Five-tier professional ordering for selecting primary DTC. Consumer: COMLab rank/route step.

