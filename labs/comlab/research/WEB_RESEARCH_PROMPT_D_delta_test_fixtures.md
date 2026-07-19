# Web-research prompt D — ground-truth fixtures for a two-operating-point (delta-based) fault-diagnosis test suite

> Hand the block below to the research agent **verbatim** — it is self-contained
> and names no codebase, file, or product. It is **scoped to test-suite
> construction**: it assumes single-operating-point per-fault signatures are already
> known, and asks only for what a **two-point (delta)** test suite needs — canonical
> operating points, full-taxonomy two-point signatures, tolerances, validity gating,
> and real paired datasets.

---

###Role###
Senior automotive emissions-and-diagnostics researcher with expertise in
**two-speed / loaded-mode tailpipe tests** (two-speed idle, ASM 2525/5015, IM240),
**fuel-trim and 5-gas behaviour across operating points**, and **measurement
repeatability/uncertainty** of scan-tool and gas-analyser readings. Report per the
source rules below.

###Context — system under study###
Advise on the system the test suite is for, without assuming any implementation:
- A fault-diagnosis engine for **petrol passenger cars, ~1990–2010** classifying a
  case into one of **~12 fault families** (lean/vacuum leak, rich, misfire, sensor
  fault, ECU/perception fault, catalyst failure, exhaust leak, ignition fault,
  mechanical wear, cam-/valve-timing, non-starter, no-fault).
- It diagnoses on the **change between two operating points** — a low/curb idle and
  an elevated/"stress" point — not a single snapshot, across three channels: **5-gas
  chemistry** (CO, CO₂, O₂, HC, plus NOx and computed λ), **fuel trims** (STFT/LTFT,
  per bank), and **O₂-sensor behaviour** (switching frequency, voltage bias,
  downstream response).
- Each test fixture needs: a **fault label**, a **low-point frame**, an
  **elevated-point frame**, the **expected delta** (direction + magnitude +
  tolerance) per channel, and a **verdict** (or explicit "abstain — no usable
  delta").

###Scope (strict)###
- Population: **petrol passenger cars, ~1990–2010**, EU + North America. Flag any
  era/region mismatch.
- **Do not re-derive single-point fault signatures** — assumed known. Confine to
  what a **two-point/delta** suite needs: operating-point definitions, the *change*
  across the step, tolerances, validity, and paired datasets.
- **Out of scope:** diesel, hybrid, EV, post-~2012 fleets. Advise on **test
  ground-truth and protocol**, not implementation; no code.

###Objective###
Produce the reference data to author **trustworthy two-point fixtures**: canonical
operating points to capture, expected per-fault delta signatures across the *full*
taxonomy (including families with no usable delta), realistic
tolerance/repeatability bands, validity criteria for the second reading, and real
paired datasets to validate against — enough for a test author to write a fixture
table with defensible expected values and pass/fail thresholds.

###Research questions###
Answer each separately, per the source rules below.

1. **Canonical operating points.** What standardized two-speed / loaded-mode points
   does the industry define — two-speed idle (curb idle + ~2500 RPM no-load), ASM
   2525/5015, IM240 cruise — with exact RPM and load definitions? Which low +
   elevated pair is the most defensible canonical choice for *delta* diagnosis on
   1990–2010 petrol, and how do signatures shift for a different elevated band (e.g.
   2500 vs 3500–4500 RPM)?

2. **Full-taxonomy two-point signatures.** For **each** fault family above (and the
   healthy baseline), give expected **fuel-trim, 5-gas, and O₂** values at **both**
   points and the resulting **delta sign + magnitude** per channel. Identify
   families that produce **no usable delta** (engine should abstain) and any family
   pair separable **only** by the delta, not by either snapshot alone.

3. **Delta tolerance / repeatability.** What is the **test-retest repeatability and
   measurement uncertainty** of fuel-trim and 5-gas readings at a held elevated RPM
   (warm, stabilised)? Give the ± band a fixture should encode and the threshold
   below which a delta is **within noise** (not diagnostic).

4. **Architecture-dependent nulls and sign inversions.** Confirm and quantify cases
   where the expected delta **nulls or inverts** with engine architecture — the
   **speed-density (MAP-only) vacuum-leak paradox** (trim shift ≈ 0 for a real leak)
   and the **forced-induction post-turbo leak** (trim sign inverts negative). These
   are negative/gating fixtures testing that the engine branches on architecture
   *before* applying a delta profile.

5. **Second-reading sample validity.** What criteria must hold at the **elevated
   reading** for the delta to be trustworthy — gas-sum/dilution checks, RPM
   stability, warm-up state, time-to-stabilise? These define the suite's
   **invalid-capture rejection** fixtures.

6. **Real paired datasets.** Do public or commercial datasets pair a **low-idle and
   an elevated-RPM reading** for the *same vehicle* with a confirmed fault (I/M
   records, ASM archives, published studies, dynamometer datasets)? List them with
   access terms, so fixtures can be validated against a real distribution.

###Output format###
- **Executive summary** (≤200 words): can a defensible two-point fixture set be built
  from available evidence, what is the recommended canonical operating-point pair,
  and where are the biggest ground-truth gaps?
- **One section per question (1–6):** *Finding* (numbers + units + ranges,
  protocol/dataset named) · *Evidence/sources* · *Confidence* (High/Med/Low) · *Data
  gaps / era-region caveats*.
- **Master fixture table:** fault family | low-point frame (trim / 5-gas / O₂) |
  elevated-point frame | Δ per channel (sign + magnitude) | tolerance band |
  architecture gate | abstain? (Y/N) | source.
- **Validity-gate table:** check (gas sum / dilution / RPM stability / warm-up /
  settle time) | threshold | channel it applies to | source.
- **Consolidated source table:** source | type (peer-reviewed / standard / I-M
  program / dataset / industry / anecdotal) | year | region | claim supported |
  access (free/paid) | link.
- **"Could not be found" list:** families, points, or tolerances where evidence is
  thin or absent — state plainly; do not fabricate.

###Source rules###
- Prefer standards bodies (SAE/ISO), government/I-M-program docs, peer-reviewed work,
  and OEM service data; label anything anecdotal.
- Every quantitative claim carries an **inline citation + working link** and the
  **test protocol or dataset** behind it; give **ranges with units**, distinguish
  **measured** from **expert estimates**, and note **era/region** applicability (flag
  anything outside 1990–2010 petrol). Where evidence is absent, say so — never invent
  a fixture value.
- Work the six questions in order — pin the canonical points (Q1) first, since every
  later signature and tolerance is relative to them. Where sources conflict
  (especially the elevated band), **surface it** and state which choice each figure
  assumes. Finish with the master fixture table and a one-line readiness verdict: can
  the suite be authored now, or is a specific ground-truth gap blocking it?
