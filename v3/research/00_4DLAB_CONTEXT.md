# 4DLab — System Context for Discriminating-Measurement Research

*Provide this document to the research agent alongside any single cluster brief. It is
self-contained: it describes the diagnostic system, its inputs, and exactly why certain faults
are unseparable today, so the agent can target the right measurement. It contains no proprietary
code — only the domain model you are helping improve.*

> **Search guard — read before doing any web research.** "4DLab" is the **internal project
> name** of the automotive diagnostic engine described below. It is **not a public institution,
> product, or research group** — do **not** web-search the string "4DLab", "4D Lab", or
> "4D laboratory", and ignore any external result about a "4D lab" (e.g. cardiovascular/MRI
> imaging labs, materials or microscopy "4D" facilities). They are unrelated name collisions.
> Your research target is **only** the petrol-engine measurement-discrimination question posed
> in the paired cluster brief. Search for the automotive/emissions subject matter (SAE/ISO/EPA/
> CARB standards, PIDs, Mode $06, gas analysis) — never for the system's name.

---

## 1. What 4DLab is

4DLab is a **rule-based fault-diagnosis engine for petrol (spark-ignition) engines**. A
technician captures a measurement set from a vehicle; the engine classifies the vehicle into
**one fault family** (and, going forward, a ranked short-list of likely families). It is not an
ML black box — it is a transparent pipeline of specialist modules ("labs") feeding a fusion
stage that prunes, ranks, and fuses the evidence into a verdict.

The engine today sits at roughly **50% single-verdict accuracy** across all fault families. An
internal root-cause analysis proved this is **not** a software or rule-coverage problem: it is a
**measurement-discrimination limit**. Several fault families produce *overlapping* signatures in
the inputs the engine actually receives, so no rule can separate them — the separating
information is physically absent from the measurement. The purpose of this research is to
identify the **additional, practically-acquirable measurements** that would restore that
separation, family by family.

## 2. The pipeline and the four input channels

```
  technician captures ─┐
                       ▼
  ┌──────── EMITTER LABS (each emits a validated signal channel, never a verdict) ────────┐
  │  GASLab   → tailpipe 5-gas chemistry, collapsed to ONE chemical-state label           │
  │  OBDLab   → live-PID data: fuel trims (STFT/LTFT), volumetric efficiency, lambda,      │
  │             sensor-health perception                                                   │
  │  DTCLab   → stored/pending/permanent DTCs, freeze-frame, Mode $06 on-board monitors    │
  │  DNALab / VINLab → vehicle hardware identity (engine, injection type, EGR, catalyst,   │
  │             cylinder count, era); SymptomLab → driver-reported symptom + environment   │
  └────────────────────────────────────────────┬─────────────────────────────────────────┘
                                                ▼
                               COMLab  =  prune → rank → fuse
                          (the only module that reads all channels)
                                                ▼
                            ranked fault verdict → (v3: top-3 differential + abstain)
```

**Load-bearing boundary:** emitter labs emit *signals*, never cross-lab fault verdicts. GASLab
says "the chemistry looks `LEAN_MIXTURE`"; OBDLab says "the trim is at its positive limit"; only
COMLab turns the combined evidence into a fault family.

## 3. What each channel actually carries

**GASLab — exhaust 5-gas at warm idle.** Five measured gases, with normative warm-idle bands:

| Gas | Meaning | Warm-idle normal (working catalyst) | Diagnostic note |
|---|---|---|---|
| **HC** (ppm) | unburned fuel | ≤ 35 ppm (≤ 50 tolerable); pre-cat healthy ≤ 100 | spikes on misfire, lean misfire, leakage past valves/rings, oil burning, EGR over-dilution. Heavy *oil* HC reads low on NDIR — oil consumption can look smaller than it is. |
| **CO** (%) | partial-oxidation product | 0.1–0.45% | one-way rich indicator: CO ≈ 0 does **not** prove lean, but CO > ~1.5% guarantees rich. |
| **CO2** (%) | complete-combustion product | 14.5–16.0% | efficiency "north star"; peaks at λ≈1.0; anything disturbing combustion drops it. |
| **O2** (%) | leftover oxygen | low single digits | rises with lean, misfire, or air ingress (exhaust leak). |
| **NOx** (ppm) | high-temperature product | varies | high combustion temp; low NOx + high HC + high O2 is a classic misfire/masking pattern. |

GASLab collapses these five numbers into **one** `chemical_state` label drawn from ~34 possible
states (e.g. `NORMAL_OPERATION`, `RICH_MIXTURE`, `LEAN_MIXTURE`, `IGNITION_MISFIRE`,
`EXHAUST_AIR_LEAK`, `WORN_PISTON_RINGS`, `WORN_VALVE_SEALS`, `COOLANT_LEAK_INTERNAL`,
`CAM_TIMING_RETARDED_MAP`, `VVT_FAILURE`, `CATALYST_OVERWHELMED`, `POA_SIGNATURE` (a deliberate
catch-all), `SAMPLE_INVALID`). The single label is the unit of information passed downstream.

**OBDLab — live engine data.** Short- and long-term fuel trims (STFT/LTFT), volumetric
efficiency, a lambda/air-fuel perception, and sensor-health checks. In much of the real corpus
this channel is **absent or sparse** — many cases arrive with gas only.

**DTCLab — stored diagnostics.** Confirmed/pending/permanent DTCs, freeze-frame (the captured
conditions at the time a code set), and **Mode $06** on-board monitor test results (e.g. catalyst
monitor, oxygen-sensor monitor, misfire counts per cylinder). Also frequently sparse or empty.

**DNALab / VINLab / SymptomLab — vehicle identity + symptom.** Decodes the VIN into hardware
architecture: engine family, **injection type (GDI vs port)**, **EGR-equipped or not**,
**catalyst present or not**, cylinder count, and emissions era. This gates which faults are even
possible. SymptomLab carries the driver-reported symptom and environmental context.

## 4. The fault families the engine classifies into

`rich_mixture`, `lean_condition`, `misfire`, `ignition_fault`, `catalyst_failure`,
`sensor_fault`, `ecu_fault`, `exhaust_leak`, `mechanical_wear`, `cam_timing`, `non_starter`,
and `no_fault` (healthy).

## 5. The core problem: the input modality does not separate confusable families

The dominant real-world input is **a single warm-idle 5-gas snapshot plus whatever DTCs happen
to be stored** — often with no live trims, no freeze-frame, and no Mode $06. Many fault families
collapse to the **same** single-snapshot signature, so the engine cannot tell them apart. The
system's own analysis names the specific gaps:

- **Mechanical wear has no distinct single-snapshot chemistry** — worn rings / valve seals / low
  compression overlap ignition misfire and a generic rich/`POA` signature. This is the single
  largest concentrated gap (~a quarter of the hard corpus).
- **Catalyst masking** — a clean tailpipe *downstream* of a healthy catalyst cannot exonerate
  the engine on gas alone; it needs OBD/freeze-frame corroboration.
- **Cam-timing / VVT and oil-burn sub-modes need an RPM dual-reading** — they don't express in a
  single idle sample.
- **O2-sensor bias needs fuel trims** to confirm; gas alone can't.
- **Non-starter** suppresses gas and live-OBD (a non-running engine has no warm idle); it must be
  decided from DTC Mode $06 + freeze-frame cut-state.
- **ECU/control faults** disperse — the gas snapshot shows the downstream symptom, not the
  control-system root cause.

A key system principle: **a single evidence channel is never allowed to claim certainty**
(confidence is capped well below 1.0 for gas-only reads), precisely because of these overlaps.

## 6. The most promising known discriminator: a two-point (RPM-step) reading

The system's analysis converges on one especially powerful idea: the hardest collisions —
timing-retarded fanning into ~7 families, worn rings vs valve seals, lean vs vacuum-leak vs
exhaust-leak — **separate on the *sign and magnitude of the change across an RPM step***, not on
any single static reading. The proposed canonical maneuver is a **two-speed reading: curb idle +
2500 RPM no-load** — the pair standardized across EPA / BAR I/M practice for ~1990–2010 vehicles,
requiring no dynamometer. An optional elevated **stress idle (~3750 RPM, per ECE R51 / ISO 5130)**
helps fuel-delivery and mechanical faults. Architecture must be gated first: e.g. a speed-density
(MAP-only) engine nulls the trim-delta for a real vacuum leak, and a post-turbo leak inverts the
trim-delta sign under boost — so the air-metering type must be known before a delta profile is
applied. Some families (sensor, ECU, catalyst, mechanical, non-starter) have a delta that is
*uninformative* and should **abstain rather than guess**.

This RPM-step idea is a hypothesis the research should **validate, quantify, and extend** — not
assume correct. Where a two-point gas/trim delta genuinely separates a cluster, give the expected
direction, magnitude, and a usable threshold, with citations.

## 7. What v3 is doing, and where this research fits

v3 reshapes the verdict from a single forced guess into a **ranked top-3 differential with
honest abstention**. That alone recovers most cases where the right answer was the discarded
runner-up. But a residual set of families is **blocked by the measurement** — the correct answer
isn't even computable from the inputs. **Those blocked families are the subject of this
research.** Each cluster brief names a specific confusable set and asks: *what additional,
practically-acquirable measurement would separate it?* Acceptable equipment baselines, expected
signatures, feasibility, and citations are specified per brief.

## 8. Equipment baseline to assume

Assume the technician already has: a **5-gas analyzer** (HC/CO/CO2/O2/NOx) capable of a steady
warm-idle reading, and a **generic OBD-II scan tool** (Mode $01 live PIDs, Mode $02 freeze-frame,
Mode $03/$07 DTCs, Mode $06 monitors) on OBD-II-era vehicles. Treat anything beyond this (second
gas probe, pressure transducer, lab-grade transient gas bench, in-cylinder pressure, scope) as an
**incremental cost** to be justified by the discrimination it buys. Petrol engines only.
