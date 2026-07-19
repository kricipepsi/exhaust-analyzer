# Web-research prompt E — cross-referencing 5-gas-analyser and OBD scan-tool two-point deltas for a petrol fault-diagnosis engine

> Hand the block below to the research agent **verbatim** — it is self-contained
> and names no codebase, file, or product. It covers the **cross-referencing /
> fusion** question only: given a *chemical* delta vector (5-gas) and an
> *electronic* delta vector (OBD scan-tool), each measured across the same
> operating-point step, **how to combine them into the most reliable diagnosis**.
> Single-point and per-fault two-point delta signatures are assumed already known
> (prior work) — do **not** re-derive them here.

---

###Role###
Senior research engineer in **multi-sensor / multi-modal data fusion** and
**automotive emissions + OBD-II diagnostics**, with working knowledge of
measurement science (time-series alignment, sensor latency, uncertainty
propagation, calibration). Report per the source rules below.

###Context — system under study###
Advise on this system without assuming any implementation:
- A fault-diagnosis engine for **petrol passenger cars, ~1990–2010** that reads
  **two independent subsystems at the same stationary operating points**:
  1. a **5-gas tailpipe analyser** — CO, CO₂, O₂, HC, NOx, computed λ; slow
     NDIR/electrochemical bench (~1–2 Hz), with exhaust transport delay and
     calibrated accuracy bands;
  2. an **OBD-II scan tool** — STFT/LTFT, O₂-sensor switching/voltage, MAP,
     IAC/throttle angle, RPM, ECT; generic PIDs with ~100–400 ms variable latency
     and fuel-trim quantization ≈ 0.39 %/bit.
- Readings are taken at **≥2 operating points** — a low/curb idle and an elevated
  point (standardised **2500 RPM** and/or an ECE R51 / ISO 5130 **"stress" idle**
  ~3750 RPM) — so **each subsystem yields a delta vector** across each transition
  (Δelevated−low, Δstress−low, Δstress−elevated).
- The two delta vectors are **heterogeneous** (different units, noise floors,
  sample rates, latency), **partially redundant** (both respond to one root cause —
  e.g. a lean fault lifts fuel trim *and* tailpipe O₂), and **sometimes contradict**
  (e.g. a speed-density MAP-only vacuum leak gives an OBD trim delta ≈ 0 while the
  gas O₂/λ delta reads lean — the **disagreement itself is diagnostic**).

###Objective###
Tell the architect, with evidence, **how to cross-reference the 5-gas delta vector
against the OBD scan-tool delta vector** — aligning, normalising, and fusing them —
to produce the **single most reliable fault ranking with calibrated confidence**,
using gas↔OBD **agreement as corroboration** and **disagreement as an informative
feature** rather than noise.

###Scope (strict)###
- Population: **petrol passenger cars, ~1990–2010**, EU + North America; flag any
  era/region mismatch.
- **Out of scope:** diesel, hybrid, EV, post-~2012 fleets; and **re-deriving
  per-fault single- or two-point signatures** (assumed known). Methods from general
  multi-sensor fusion, clinical multi-modal diagnosis, and industrial process
  monitoring are welcome — **label the domain transfer**.
- Advise on **method and architecture**, not implementation; no code.

###Research questions###
Answer each separately, per the source rules below.

1. **Temporal alignment of two unequal streams across an operating-point step.**
   How should a slow gas-bench reading (transport delay, ~1–2 Hz, exhaust transit
   lag) be aligned with scan-tool PIDs (100–400 ms variable latency, 0.39 %
   quantization) so the gas-delta and OBD-delta refer to the **same stabilised
   state**? Cover settle-time/lag-compensation rules, cross-correlation / time-warp
   alignment, and how long to hold each point before the delta is trustworthy.

2. **Normalising heterogeneous deltas and propagating uncertainty.** How to put a
   gas delta (%/ppm) and a trim delta (%) on a **comparable scale** before fusion —
   z-scoring against the per-point healthy baseline, dimensionless ratios,
   per-channel standardisation — and how to **propagate each channel's measurement
   uncertainty into its delta** (error propagation / root-sum-square) so fusion
   weights reflect real reliability, not raw magnitude.

3. **Agreement vs disagreement as the core discriminator.** What principled methods
   let the engine (a) **corroborate** when the gas-delta and OBD-delta agree (raise
   confidence without double-counting two correlated views of one root cause), and
   (b) **use gas↔OBD disagreement as an explicit feature** — including cases where
   the contradiction *identifies* the fault or architecture (speed-density MAP leak:
   OBD trim null, gas lean)? Tie to evidence-fusion theory (Bayesian, Dempster–
   Shafer conflict mass, conflict-aware operators, stacking) but specific to **two
   delta modalities**.

4. **Fusion architecture and calibrated joint confidence.** How to combine the two
   delta vectors into a **ranked fault hypothesis with calibrated confidence** —
   weighted log-likelihood / log-odds aggregation, cross-modal Bayesian update,
   learned stacking over the two modalities. How should the scheme handle a modality
   that **abstains** (no usable delta) or **fails a validity gate**, and how does
   corroboration vs contradiction map onto the reported confidence?

5. **Paired gas + OBD multi-point ground truth and validation.** Do any public or
   commercial datasets pair **tailpipe 5-gas AND scan-tool PIDs at ≥2 operating
   points for the same vehicle with a confirmed fault**? If not, how is a
   cross-referenced delta model **validated** without one — synthetic generation,
   expert-elicited priors, leave-one-fault-out cross-validation, adversarial
   checks? List datasets with access terms.

###Output format###
- **Executive summary** (≤200 words): can cross-referencing the two delta vectors
  beat either modality alone, and what is the single highest-leverage method?
- **One section per question (1–5):** *Finding* (numbers + units + ranges,
  dataset/protocol named) · *Evidence/sources* · *Confidence* (High/Med/Low) ·
  *Data gaps / domain-transfer caveats*.
- **Cross-reference logic table:** gas-delta pattern | OBD-delta pattern |
  agreement/contradiction | diagnostic interpretation | confidence effect | source.
- **Fusion-method table:** method (RSS-weighted vote / Bayesian update / DS
  conflict-aware / stacking-logistic / learned) | what it buys | cost / when it
  fails | evidence it beats single-modality on a comparable task | maturity.
- **Consolidated source table:** source | type (peer-reviewed / standard / I-M
  program / dataset / industry / anecdotal) | year | domain (automotive / general
  fusion / clinical / process) | claim supported | access (free/paid) | link.
- **"Could not be found" list:** sub-points where evidence is thin, absent, or only
  off-domain — state plainly; do not fabricate.

###Source rules###
- Prefer standards bodies (SAE/ISO/UNECE), government/I-M-program docs, peer-reviewed
  work, and OEM service data; label anything anecdotal or vendor-marketing.
- Every quantitative claim carries an **inline citation + working link** and the
  **dataset/protocol** behind it; give **ranges with units**, distinguish
  **measured** from **expert estimates**, and note **era/region** applicability
  (flag anything outside 1990–2010 petrol). Where evidence is absent, say so —
  never invent a value.
- Label every method imported from a **non-automotive domain** and argue the
  transfer. Work the questions in order; where sources conflict, **surface it**
  rather than averaging. Finish with the cross-reference logic table and a one-line
  verdict on the highest-leverage cross-referencing method.
