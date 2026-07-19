# Web-research prompt C — synthetic-corpus signal sufficiency & label-noise impact on a fault-diagnosis classifier

> Hand the block below to the research agent **verbatim** — it is self-contained
> and names no codebase, file, or product. This prompt addresses the
> **data-quality / corpus** question (is the dataset the binding constraint?). It is
> independent of prompts A and B and can be researched in parallel.

---

###Role###
Senior research engineer in **dataset quality, label noise, and the statistics of
achievable classifier accuracy**, with working knowledge of fault-diagnosis
datasets, synthetic/simulated-data validation, and class-conditional separability.
Report per the source rules below.

###Context — system under study###
Advise on this system without assuming any implementation:
- A **multi-class fault classifier** for petrol passenger cars (~1990–2010)
  assigning each case to one of **~12 near-exclusive fault families** from a few
  channels (exhaust-gas chemistry, live sensor data, stored fault codes, an
  operator-reported symptom).
- Developed/evaluated against a **small, partly-synthetic ground-truth corpus**:
  ~**250–280 labelled cases**, heavily **class-imbalanced** (largest family ~50
  cases, several only 3–5); some values are **synthetic, hand-filled, or imputed**
  (e.g. medians for missing fields); some columns carry **sentinel/limit values**
  (±127, 999) ambiguous between a real reading and a "no data / saturated" marker; a
  fraction of cases were **hand-curated** by human judgement (dropped as
  "contrived," or added as placeholders); and the **single most common evidence
  state maps to ~7 fault families** (very low separability for that slice).
- Top-1 accuracy has **plateaued near 50 %**, and the team suspects the **corpus,
  not the model**, is the binding constraint — that labels/signals may not be
  trustworthy or separable enough for an ~85 % target to be reachable at all.

###Scope (strict)###
- Primary domain: **automotive fault-diagnosis datasets**, but methods from general
  ML, medical-diagnosis datasets, and industrial fault detection are welcome for the
  statistical questions — **label the domain** of each imported method/figure and
  argue the transfer.
- **Out of scope:** scoring architecture and confidence calibration (covered
  elsewhere). Confine to **data quality, label noise, separability, and what
  accuracy a dataset of this size/quality supports**. Advise on **method and
  feasibility**, not implementation; no code.

###Objective###
Tell the architect, with evidence: whether a corpus of this size and quality can
support a high accuracy target at all, how to measure whether labels and signals are
trustworthy and separable, and how to validate a partly-synthetic diagnostic corpus
— so the team can choose between "fix/expand the data" and "keep engineering the
model."

###Research questions###
Answer each separately, per the source rules below.

1. **Label-noise impact on the ceiling.** How much does mislabeled/noisy ground
   truth **cap achievable top-1 accuracy** on multi-class classification? Give
   quantified relationships (e.g. *X %* noise → approximate ceiling) and the methods
   to **estimate the noise rate** (confident learning / Cleanlab, inter-annotator
   agreement, noise-transition-matrix estimation).

2. **Synthetic, hand-filled, and sentinel values.** What is the documented risk of
   training/tuning on **imputed, fabricated, or sentinel** feature values, and how
   badly can it bias results? What are standard practices to **detect and flag**
   imputed-vs-measured values and ambiguous limit/sentinel codes (±127, 999)? Cite
   missing-data and data-validation literature.

3. **Class separability / minimum signal.** What standard methods quantify whether a
   dataset carries **enough discriminating signal** to separate near-identical
   classes — class-conditional overlap, feature–label mutual information, Bayes-error
   / irreducible-error estimators, and the case where one feature state maps to many
   classes? How is **irreducible error** estimated in practice?

4. **Synthetic vs real data (sim-to-real gap).** What is the **accuracy gap** when a
   diagnostic model built on synthetic/simulated data is evaluated on **real-world**
   data, in automotive or analogous domains? How is a synthetic corpus **validated**
   against a real distribution (distribution-shift tests, real-case holdout,
   adversarial validation)?

5. **Sample size and class imbalance.** For a **~12-class problem with ~250
   heavily-imbalanced cases**, what top-1 accuracy is **statistically supportable**,
   and how tight are confidence intervals on per-family accuracy at single-digit
   counts? How does imbalance **cap minority-class recall**, and what are the
   recognised mitigations and their evidenced limits (resampling, cost-sensitive
   learning, more data)?

###Output format###
- **Executive summary** (≤200 words): can a corpus of this size/quality support a
  high accuracy target, or is the data the binding constraint? — plus the single
  highest-leverage data action.
- **One section per question (1–5):** *Finding* (numbers + ranges, dataset named) ·
  *Evidence/sources* · *Confidence* (High/Med/Low) · *Data gaps / domain-transfer
  caveats*.
- **Diagnostic-checklist table:** check (label-noise rate / imputed-value share /
  separability / sim-to-real / min-per-class N) | how to measure it | threshold or
  rule-of-thumb that signals "data is the constraint" | source.
- **Consolidated source table:** source | type (peer-reviewed / standard / industry
  / dataset / benchmark / anecdotal) | year | domain (automotive / medical / general
  ML) | claim supported | access (free/paid) | link.
- **"Could not be found" list:** sub-points where evidence is thin, absent, or only
  off-domain — state plainly; do not fabricate.

###Source rules###
- Prefer peer-reviewed work, standards bodies, benchmark datasets, and textbook
  methods; label anything anecdotal or vendor-marketing.
- Every quantitative claim carries an **inline citation + working link** and the
  **dataset/task** behind the number; give **ranges**, and distinguish **measured
  results** from **expert estimates**.
- Label every figure imported from a **non-automotive domain** and argue the
  transfer. Where evidence is absent, say so — never invent numbers.
- Work the five questions in order; where sources conflict, **surface it** rather
  than averaging. Finish with the diagnostic-checklist table and a one-line verdict
  on whether the data or the model is the more likely binding constraint at ~50 %
  accuracy on a corpus of this description.
