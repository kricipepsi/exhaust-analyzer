# Web-research prompt B — confidence calibration, differential output & self-report priors for a multi-channel automotive fault-diagnosis engine

> Hand the block below to the research agent **verbatim** — it is self-contained
> and names no codebase, file, or product. This is **prompt 2 of 2**: what the
> engine outputs and how confident it should sound (calibration, single-verdict vs
> ranked differential, weight of a self-reported symptom). Scoring and fusion are
> in companion prompt A.

---

###Role###
Senior research engineer in **diagnostic decision-support**, **confidence
calibration**, and **human-facing diagnostic UX**, with working knowledge of
automotive (OBD-II petrol) fault diagnosis and clinical decision-support. Report
per the source rules below.

###Context — system under study###
Advise on this system without assuming any implementation:
- A fault-diagnosis engine for **petrol passenger cars, ~1990–2010** that fuses
  **four channels** — exhaust-gas chemistry; live sensor data (fuel trims, O₂,
  load); stored trouble codes; and an **operator-reported primary symptom** — into
  a most-likely fault over **~12 near-exclusive fault families**. Several family
  pairs **share a signature**, so a single forced verdict must mislabel some cases.
- The engine currently: emits **one winning verdict plus up to three runner-up
  "differential" candidates**, but is scored on **top-1** only; reports a
  **confidence label reflecting evidence completeness** (how many channels
  reported), **not** a calibrated probability of being correct; and applies a
  **small fixed additive prior for a non-blank reported symptom** (too small to
  override strong objective evidence) whose magnitude was set by intuition.

###Scope (strict)###
- Population: **petrol passenger cars, ~1990–2010**, EU + North America.
- **Out of scope:** diesel, hybrid, EV, post-~2012 fleets. Clinical decision-support
  evidence is welcome for the calibration and self-report questions — just label the
  domain transfer. Advise on **method and metric**, not implementation; no code.

###Objective###
Tell the architect, with published evidence: (a) how to make the confidence label
mean a real likelihood of being correct, (b) whether to score and present a ranked
differential instead of a single verdict, and (c) how strongly a self-reported
symptom should weigh and how to bound it.

###Research questions###
Answer each separately, per the source rules below.

1. **Confidence calibration to real likelihood.** How should a diagnostic engine
   map an internal score to a **calibrated confidence** (true posterior / likelihood
   ratio)? Cover Platt scaling, isotonic regression, temperature scaling, conformal
   prediction, and the verification metrics (reliability diagrams, ECE, Brier).
   Separately: how do established frameworks define **discrete confidence tiers**
   (definitive / probable / possible, or likelihood-ratio bands) so a tier means a
   real LR, not an arbitrary threshold?

2. **Single verdict vs ranked differential (top-k).** When does diagnostic
   decision-support output a **ranked differential (top-2/3)** instead of one
   answer, and what is the evidence for doing so? Give the typical **top-1 vs top-3
   accuracy gap** on comparable tasks, how **top-k / "any-correct-in-k"** is defined,
   and any evidence on user/technician value and trust for a ranked differential vs
   a single forced verdict.

3. **Magnitude of a self-reported-symptom prior.** In clinical and automotive
   decision-support, **how much weight** does a self-reported symptom carry vs
   objective test evidence, and how is it **bounded** against over-trust? Give any
   published likelihood ratios / prior strengths for self-reports, methods for
   **capping** their influence (break ties, not override strong evidence), and how
   unreliable self-reports (false/vague/misattributed) should discount that weight.

###Output format###
- **Executive summary** (≤200 words): how should this engine express confidence,
  should it present a differential, and how far can a self-reported symptom be
  trusted?
- **One section per question (1–3):** *Finding* (numbers + ranges, dataset named) ·
  *Evidence/sources* · *Confidence* (High/Med/Low) · *Data gaps / domain-transfer
  caveats*.
- **Tier-definition table:** confidence tier | likelihood-ratio/posterior band it
  maps to | calibration method that produces it | source.
- **Consolidated source table:** source | type (peer-reviewed / standard / industry
  / dataset / benchmark / anecdotal) | year | domain (automotive / medical /
  general) | claim supported | access (free/paid) | link.
- **"Could not be found" list:** sub-points where evidence is thin, absent, or only
  off-domain — state plainly; do not fabricate.

###Source rules###
- Prefer peer-reviewed work, standards bodies, benchmark datasets, and textbook
  methods; label anything anecdotal or vendor-marketing.
- Every quantitative claim carries an **inline citation + working link** and the
  **task/dataset** behind the number; give **ranges**, and distinguish **measured
  results** from **expert estimates**.
- Label every figure imported from a **non-automotive domain** (clinical especially)
  and argue the transfer. Where evidence is absent, say so — never invent numbers.
- Work the questions in order; where sources conflict, **surface it** rather than
  averaging. Finish with the tier table and a one-line verdict on whether the
  highest-leverage change is calibration, a differential output, or a re-bounded
  symptom prior.
