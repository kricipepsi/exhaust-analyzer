# COMLab Rework — Implementation Plan (research-driven)

**Author:** architect (4DLab, Cowork) · **Date:** 2026-06-19 · **Stage:** 4 (COMLab reworked last)
**Synthesises:** research packs **A** (scoring+fusion), **B** (calibration+differential+symptom), **C** (corpus+label-noise), **D** (two-point delta fixtures: `DeltaRes1.md`, `Two-Point Emissions Test Fixture Design.md`), **E** (gas↔OBD cross-reference: `Multi-Sensor Fusion for Automotive Diagnostics.md`, `DeltaRes2.md`) · audit `AUDIT_ANSWERS_COMLab.md` + `AUDIT_PART1_CEILING_RESEARCH.md` · `OPEN_LEVERS_COMLab.md` · `PROPOSAL_DeltaLab_cross_lab_delta_module.md` · ledger `tasks/PROGRESS.md`.

> **How to read this.** §1 states the three things the research *changed* about the rework. §2 is the cheap, decisive work that must run **before** the big build (it can reset the target or kill a workstream). §3 is the **question-by-question** translation of each research finding into a concrete COMLab decision (what changes · named consumer · files · task row). §4 is the target architecture. §5 sequences it onto the existing `PROGRESS.md` rows. §6 is success criteria + what NOT to do. §7 is the decisions only the human/manager can make.
>
> **House rules honoured throughout:** emitter labs emit channels, COMLab fuses; no cross-lab Python imports (mirror types locally); a new field ships only with a **named consumer in the same change**; numeric literals carry a wiki/source citation; reports are `.md`; obsolete files are archived, not deleted; graphs are frozen (query, don't rebuild).

---

## 1. What the research changed — three reframes

The rework is **not** "a better ranker." Three convergent findings move it off that track.

**R1 — Data is the binding constraint, not the logic (from C + audit Q2).**
A corpus of ~250–280 cases, 12 classes, single-digit minority families, partly synthetic/hand-filled values, ambiguous sentinels (±127, 999), and one evidence state (`TIMING_RETARDED`, ~25 % of cases) mapping to ~7 families is **more likely the bottleneck than the model** at the ~50 % plateau (C, exec summary). The audit's own triage agrees: a provable irreducible floor ~9.6 % (27 `ecu_fault` STOP cases where the signal is absent) and a realistic ceiling in the **70–80 %** band — **85 % is not reachable on the current four channels** (`AUDIT_ANSWERS Q2`). Label noise mechanically caps achievable agreement at ≈ 1−r (15 % noise → ~85 % ceiling; C §label-noise), and minority families with 3–5 cases give recall CIs so wide (~15–95 %) they cannot certify anything (C §sample-size). **Implication:** the product target and the engineering target both change (see §3.C, §6).

**R2 — The additive prune-then-rank paradigm has hit its ceiling (from A + audit).**
The OUTRANKED bucket (~82–90 cases, the whole game) loses because a generic rule's higher `base_weight` beats the correct specific rule, and the intended tie-breaker (DTC routing tag, weight 0.10) is **starved — 64/90 carry no DTC** (`AUDIT_PART1 §1.1`). Bounded-additive nudges and coverage rescues have repeatedly moved **0 pp** (`AUDIT §2 Wave E`). A says hand-tuned additive rankers have an inherent ceiling vs calibrated/learned fusion, and that contradiction should be **used as a feature, not a destructive override** (which already measured net-negative, `AUDIT §1.2 Culprit 2`). **Implication:** replace the additive tie-break with **calibrated, conflict-aware late fusion** (§3.A, §4).

**R3 — The missing discriminator is a two-point delta (from D/E + DeltaLab proposal).**
The hardest collisions (`TIMING_RETARDED`→7 families; worn rings vs valve seals; lean vs vacuum-leak vs exhaust-leak) are **single-snapshot** collisions that separate on the **sign of the change across an RPM step** — a discriminator that needs **no DTC** (proposal §1). Both E reports converge: cross-reference the **gas-delta vector** against the **OBD-delta vector** with **conflict-aware fusion**, after temporal alignment and uncertainty weighting (E both, verdicts). **The two-point *contract* already largely exists** in the reworked emitters (GASLab emits an optional `reading_high`/`high_idle_*` 2500-RPM frame; OBDLab already has `STRESS_IDLE` bands + `stress_idle_rpm_target` from VinDNA — see §8); what is single-point is the **populated master corpus**. So the lever is gated not on building plumbing but on the **workflow populating the second frame** (proposal §3, Gate-1). **Implication:** the delta module is a **wiring job**, built default-off; live value is gated on corpus/field population (§3.D/E, §5 Phase 3, §8).

The honest one-line synthesis: **the rework makes the output trustworthy (calibrated differential) regardless of data, adds the one new signal that can raise top-1 (the delta) but only if a second reading is captured, and stops spending effort on weight-tuning that the ledger proves is a dead end.**

---

## 2. Phase 0 — decide before building (cheap, decisive, gating)

These cost little, need no new data (except Gate-Data, which is the point), and each resolves a strategic fork. Nothing in §3–§5 should be *built* before these report.

| # | Action | Decides | Source |
|---|---|---|---|
| **M1** | Histogram `winner_score − correct_rule_score` over the OUTRANKED bucket | Whether **any** bounded discriminator (≤0.10) can ever work. If most gaps > 0.10, stop tuning weights — only re-architecture (R2) or new signal (R3) can help. **Highest-value single experiment.** | `OPEN_LEVERS M1` |
| **M2** | Count `degradation_mode` (`FULL_FUSION` vs `GAS_DOMINANT`) over the corpus | Whether the ceiling is gas-bound (then OBD-side fusion work can't move it) | `OPEN_LEVERS M2` |
| **M3** | Count valid payloads silently rejected at Stage-A (O2 enum gap, DTC hex/decimal regex) | Free recall recoverable before any rework | `OPEN_LEVERS M3` |
| **F1** | Consolidate the two registries (REG-V2 shim ↔ `global_fault_registry`) | Known **+4 cases → 52.7 %** already-earned gain; unblocks the harness | `OPEN_LEVERS F1` |
| **F3** | Reconcile dual "engine-warmed" thresholds (70 °C vs 75 °C) | Removes inconsistent gating; correctness | `OPEN_LEVERS F3` |
| **Gate-Data** | Build a **measured-real, provenance-audited evaluation subset** (flags: observed/derived/imputed/synthetic/manual-override/sentinel/out-of-range); re-audit labels (confident-learning/Cleanlab + inter-rater κ with raw agreement); estimate Bayes/irreducible error | **Fixes the real accuracy target** and tests the §1.3 "data is the constraint" hypothesis | C §1–§3,§5; `AUDIT Q2` |
| **Gate-Capture** | Product/field decision: can the workflow capture a **low-idle + elevated/stress** frame pair? | Whether the **delta rework (R3) is real or deferred**. Dominates everything in Phase 3. | proposal §3, Gate-1 |

**Phase-0 exit = two numbers and two go/no-go flags:** (a) the measured achievable ceiling on a clean eval subset; (b) the OUTRANKED score-gap distribution; (c) Gate-Capture yes/no; (d) Gate-Data eval subset exists yes/no.

---

## 3. Question-by-question → implementation decisions

Each block: **Finding** (research) → **Decision** (COMLab change) → consumer/files/row.

### A — Scoring paradigm & evidence fusion

**A.Q1 — Does the additive ranker have an inherent ceiling? (yes)**
*Finding:* hand-tuned additive weight engines plateau below calibrated/learned fusion on comparable noisy multi-class tasks (A §1); on this corpus the additive tie-break is provably stuck (R2).
*Decision:* freeze the additive ranker as the **fallback** path only. Re-architect Phase 5 of `fault_atlas_router.execute_triage_loop` from "highest additive score wins" to a **calibrated fusion stage** (§4). Do **not** invest further in `base_weight` tuning ("scoring tightening is a smell", `AUDIT §3`). *Files:* `core/fault_atlas_router.py`. *Gate:* M1/M4 first.

**A.Q2 — Use contradiction as a feature, not an override.**
*Finding:* hard override is net-negative (`AUDIT Culprit 2`); A §2 and both E reports say model disagreement should be an explicit input (DS conflict mass / a contradiction feature), never a forced win.
*Decision:* keep `core/perception_contradiction.py` emitting a **contradiction flag** (already does), and feed gas↔OBD agreement/disagreement into the fusion stage as **evidence**, per the E cross-reference logic table (e.g. *gas lean + OBD trim-null → speed-density leak, raise confidence*; §3.E). Conflict **raises** confidence for the fault it implies and is surfaced as a "check sensors" tier when global (E.Q4). *Files:* `core/perception_contradiction.py`, fusion stage.

**A.Q3 — Calibrated/Bayesian fusion vs additive; prevent channel swamping.**
*Finding:* under correlated channels, naive product fusion swamps weak-but-reliable channels (A §3); weight each channel by **measurement uncertainty** (inverse-variance / ignorance mass) so reliability, not raw magnitude, drives the result (E.Q2/Q4).
*Decision:* the fusion stage weights each lab's evidence by its propagated uncertainty (§3.E.Q2) and uses a **conflict-aware combiner** (§3.E.Q4) instead of additive sum or naive Bayes product. The **12** forward-registered `T-COMV2-*` fusion consumers (ECU-FUSE, BANK-FUSE, VE-GATE, … — every row except `DELTA`) become **evidence inputs to this stage**, not independent additive bumps.

### B — Confidence calibration, differential output, symptom prior

**B.Q1 — Make confidence mean a real likelihood.**
*Finding:* today `ConfidenceRating ∈ {HIGH_ASSURANCE, DEGRADED_ASSURANCE, LOW_CERTAINTY}` reflects **evidence-chain completeness, not calibrated correctness** (`AUDIT Q5`). B: map the internal score to a calibrated posterior with **isotonic regression** (enough data) or **Platt** (sparse data); verify with reliability diagrams + ECE + Brier; define tiers as **likelihood-ratio / posterior bands** (BI-RADS/O-RADS pattern), not adjectives.
*Decision:* add a post-hoc **calibration layer** that maps the fused score → calibrated posterior, then to the existing tiers re-defined as posterior/LR bands. **Given the corpus reality (small, imbalanced, noisy — C), prefer Platt/sigmoid or temperature scaling over isotonic** (isotonic overfits the single-digit minority-class bins; sigmoid's extra intercept also helps under imbalance — see §8 web findings), fit on a **minority-stratified** calibration split, and use **conformal prediction** for the differential's finite-sample coverage guarantee rather than trusting a calibrated top-1. **Calibrate on the Gate-Data eval subset** (calibration is meaningless on noisy/synthetic labels — explicit dependency on Phase 0). *Files:* `schemas/vocabulary.py` (tier definitions), fusion-stage calibrator, `wiki/COMLab_Diagnostic_Logic.md`. *Caveat:* until the eval subset exists, tiers are **expert-set priors**, flagged as such.

**B.Q2 — Score and present a ranked differential (top-k).**
*Finding:* top-1→top-3 gap is **+17–33 pp** on comparable diagnostic tasks (B §2); given the taxonomy is **not mutually exclusive** (≥4 colliding pairs, `AUDIT Q10`), a forced top-1 must mislabel a fraction no matter the tuning. The mechanism already exists: `DifferentialSiblingOut` (max 5) populated from `runner_ups = scored[1:4]` (`response.py`).
*Decision:* (1) **score the engine on top-1 AND top-3** (and "any-correct-in-k") in the eval harness — this reframes the achievable target; (2) make the differential the **primary product output** with per-candidate calibrated confidence; (3) keep a single lead verdict for back-compat. *Files:* eval harness/metrics, `core/fault_atlas_router.py` (already emits siblings), `wiki`. *Low code cost; high honesty payoff.*

**B.Q3 — Bound the operator-symptom prior.**
*Finding:* single self-reported symptoms are **weak-to-moderate** evidence (LR ≈ 1–3, rarely >4); cap below "strong" objective evidence (LR >10) (B §3). Today `prior_weight 0.10`, bounded-additive, ~0 false-positive delta but tiny lift (`AUDIT Q8`). `T-COMV2-CTXMOD-1` already plans a **65 % trust cap** + `load_state` context modifier.
*Decision:* keep the symptom as a **bounded prior that breaks ties only**; encode the cap as an LR ceiling (≤ a "moderate" band), discounted further when the symptom is vague/second-hand. Fold into `T-COMV2-CTXMOD-1`. *Files:* `config/symptom_prior.yaml`, `core/symptom_router.py`. *No expansion of symptom influence.*

### C — Corpus quality & label noise (the binding constraint)

**C.Q1 — Label noise caps the ceiling.** *Decision:* re-audit labels on the eval subset (confident-learning + inter-rater κ reported **with** raw agreement and class-wise confusion, never κ alone); publish the implied ceiling (≈1−r). Gate any "accuracy improved" claim on this subset. *(Gate-Data)*

**C.Q2 — Synthetic/imputed/sentinel values bias results.** *Decision:* make **provenance observable** — every non-observed field carries a companion flag (observed/derived/imputed/synthetic/manual-override/sentinel/out-of-range/saturated). Never collapse an ambiguous ±127/999 into a numeric variable during train/eval (confirmed sentinel, `obdlab Q3`). *Files:* `schemas/ingestion.py` (+ provenance flags), corpus pipeline. *This is a corpus/schema task, gated by signal/noise rule: the flags' consumer is the eval harness + the validity gates.*

**C.Q3 — Separability / irreducible error.** *Decision:* compute class-overlap, feature–label mutual information, and a Bayes-error bound on the eval subset; quantify the `TIMING_RETARDED`→~7-family slice (local ceiling ~1/7 ≈ 14 % absent new signal). This **is** the quantitative form of audit Q2 and the test of §1.3. *(Decides whether R3's delta is the only way past the slice.)*

**C.Q4 — Sim-to-real gap.** *Decision:* before trusting any number from the synthetic corpus, run **real-only holdout** + a classifier two-sample / MMD test (synthetic vs real distinguishable above chance → synthetic not yet a valid proxy). *(Gate-Data exit criterion.)*

**C.Q5 — Sample size & imbalance.** *Decision:* report **per-family recall with binomial CIs**; do not certify families with <10 cases; treat single-digit families as **anecdotal** in the product (route to differential, not a hard verdict). Resampling cannot create absent separation — flag minority families as "low-support" in output.

### D + E — Two-point delta and gas↔OBD cross-reference (the new signal)

**D.Q1 — Canonical operating points.** *Decision:* adopt **curb idle + 2500 RPM no-load (two-speed idle)** as the canonical pair (only universally standardised pair across EPA/BAR for 1990–2010, no dyno; `DeltaRes1 Q1`, `Two-Point`). Treat **stress idle ~3750 RPM (ECE R51 / ISO 5130)** as an optional second elevated point for fuel-delivery/mechanical faults (`Two-Point` Δstress). **Pick one canonical pair per signal and cite it — do not silently mix bands** (proposal §5 / `SWEEP_MANIFEST §7`). *Resolves the open band-reconciliation in `T-COMV2-DELTA-1`.*

**D.Q2 — Per-fault two-point signatures + the abstain set.** *Decision:* encode the per-fault Δ table (direction + magnitude + tolerance) from the D reports as fixtures; explicitly encode the **abstain families** whose delta is uninformative — sensor fault, ECU fault, catalyst failure, mechanical wear, non-starter (`DeltaRes1 Q2`, `Two-Point` master table) — so the engine abstains rather than guesses. *Files:* `tests/unit/test_delta_engine.py`, fixture table.

**D.Q3 — Tolerance / noise floor.** *Decision:* encode RSS-derived noise floors as the "within-noise → abstain" thresholds: **±3 % total fuel trim, ±15 ppm HC, ±0.05 % CO, ±0.20 % O₂** (`Two-Point` §noise floor; OBD trim quantization 0.39 %/bit). Each literal carries its source citation. A delta inside the floor is **not diagnostic**.

**D.Q4 — Architecture gates (mandatory, before profiles).** *Decision:* branch on air-metering/induction **before** applying any delta profile — **speed-density (MAP-only) nulls ΔTrim for a real leak** (route to IAC/throttle-angle, not the leak profile); **forced-induction post-turbo leak inverts ΔTrim sign** (≈ −20 % under boost). Applying a profile without gating *creates* misclassifications. *Files:* `analytics/delta_engine.py` (gate first). *Already a hard requirement in `T-COMV2-DELTA-1` risks.*

**D.Q5 — Second-reading validity gates.** *Decision:* both frames must pass: gas-sum/dilution (CO+CO₂ > 6 %, O₂ < 5 %), RPM stability (±100 RPM ≥10 s), warm-up (ECT in band), settle time, closed-loop. Failing → that modality **abstains** (E.Q4 graceful degradation). *Files:* validity-gate table → Stage-A gates.

**D.Q6 / E.Q5 — Datasets & validation (the blocking gap).** *Finding:* **no public dataset** pairs 5-gas + OBD PIDs at ≥2 points per vehicle with a confirmed fault (both E reports, C §sim-to-real). *Decision:* validate the delta module on **synthetic fixtures** (prompt-D master table) for algorithm correctness now; treat diagnostic accuracy as **unvalidated** until a paired/field dataset exists; plan prospective field capture as the only real validation path. *This is why `T-COMV2-DELTA-1` is build-now / live-gated.*

**E.Q1 — Temporal alignment.** *Decision:* hold each operating point **≥15 s** after RPM stabilises; apply a fixed **~10 s lag offset** to gas vs OBD (range 9–13 s, varies with flow); compute deltas from the **last 5 s** of each hold; optional cross-correlation (MAF/MAP vs CO₂/O₂) for per-vehicle lag refinement (`DeltaRes2 Q1`, `Multi-Sensor Fusion Q1`). *Files:* `analytics/delta_engine.py` (alignment pre-step).

**E.Q2 — Normalise + propagate uncertainty.** *Decision:* per channel, `Δ_c = elevated − low`; `σ_Δc = √(σ_low² + σ_elev² + σ_align²)`; standardise to `z_c = Δ_c / σ_Δc` against the per-point healthy baseline. Higher-uncertainty channels contribute less (inverse-variance). This is exactly the **delta-then-normalise-then-fuse** order already established (per-lab delta in native units first, normalise after). **σ source (reality check, §8):** the reworked emitters emit a *categorical* `SampleValidity`, **not** a numeric per-reading σ, so `σ_meas` is taken from **analyzer/scan-tool specs** (±3 % trim, ±15 ppm HC, ±0.05 % CO, ±0.20 % O₂ — D/E) and *gated* by the emitted `SampleValidity` (invalid → that channel abstains, D.Q5). *Files:* `analytics/delta_engine.py`.

**E.Q3 — Agreement/disagreement as the core discriminator.** *Decision:* implement the **cross-reference logic table** (both E reports): agreement → corroborating mass (confidence up, no double-count); disagreement → conflict mass that *maps to a specific fault* (speed-density null, pre-O₂ exhaust leak, MAF under-report, O₂-sensor-stuck → trust gas). *Files:* fusion stage + a checked-in cross-reference table (wiki).

**E.Q4 — Fusion architecture + calibrated joint confidence.** *Finding:* both E reports' top recommendation is **Dempster–Shafer with a conflict-aware rule (PCR5/Yager)** — no training data, handles non-commensurate data + uncertainty + conflict natively, validated in automotive diagnosis; Bayesian inverse-variance log-odds is the simpler fallback; stacking needs the paired dataset we don't have.
*Decision (staged, to avoid over-engineering):*
1. **Start** with **inverse-variance-weighted Bayesian log-odds + an explicit conflict feature** — simplest thing that gives calibrated posteriors and uses conflict (E.Q4 Option B). 
2. **Adopt conflict-aware DS/PCR5** (E.Q4 Option A) where the log-odds form is shown to mishandle high-conflict cases — its thresholds are **expert priors until calibrated** on the Gate-Data subset.
3. **Defer stacking** until a paired/field dataset exists.
Graceful degradation: one modality abstains → fall back to the other with widened confidence; both abstain → "insufficient data." *Files:* fusion stage (new), `core/fault_atlas_router.py`, `core/lab_pipeline_aggregator.py`.

---

## 4. Target architecture (the reworked spine)

```
ingest (+ provenance flags, optional 2nd-frame)            [schemas/ingestion.py]
   │
Stage-A validity gates  per modality  (dilution, RPM, warm, closed-loop)   → modality may ABSTAIN
   │
per-lab per-channel DELTA  (only when 2nd frame present; native units)      [analytics/delta_engine.py]
   ├─ temporal align (gas ~10 s lag, last-5 s window)            E.Q1
   ├─ architecture gate FIRST (speed-density null / turbo inv.)  D.Q4   ← mandatory
   └─ normalise + uncertainty  z_c = Δ_c/σ_Δc                    E.Q2
   │
CONFLICT-AWARE LATE FUSION  (evidence = 13 T-COMV2-* consumers + deltas)    [new fusion stage]
   ├─ agreement → corroborate ; disagreement → conflict-as-feature   A.Q2 / E.Q3
   ├─ inverse-variance weighting (anti-swamping)                      A.Q3
   └─ Bayesian log-odds first → DS/PCR5 where needed                  E.Q4
   │
CALIBRATION  fused score → posterior (isotonic/Platt)  → LR/posterior tiers  B.Q1
   │
RANKED DIFFERENTIAL  top-3 + per-candidate calibrated confidence            B.Q2   [response.py]
        (single lead verdict retained for back-compat)
   │
SINGLE_POINT degradation fallback = today's static additive path (byte-identical when no 2nd frame)
```

The static single-point additive ranker is **retained as a degradation mode**, not deleted — when no second frame and no calibration data exist, the engine behaves as today. The rework is *additive and default-off* at the seams, which is what makes it shippable under the regression-lock rule.

---

## 5. Sequencing onto the existing ledger (`tasks/PROGRESS.md`)

| Phase | Goal | Tasks (existing rows unless "NEW") | Gate |
|---|---|---|---|
| **0 — Measure/Gate** | reset the target; decide delta viability | `OPEN_LEVERS M1–M4` (NEW measure tasks), **F1**, **F3**; **Gate-Data** eval subset (NEW, C-driven); **Gate-Capture** product decision | — |
| **1 — No-regret rework** | honest output, earned gains, no new data | **F1** registry consolidate; **top-k scoring** + differential as product (B.Q2); **calibration layer** scaffold (B.Q1, calibrate later); **symptom cap** via `T-COMV2-CTXMOD-1` (B.Q3) | M1 says weight-tuning dead → skip F2 |
| **2 — Fusion rework** | replace additive tie-break | NEW **fusion-stage** task (A.Q1/Q3, E.Q3/Q4); re-point the 12 `T-COMV2-*` fusion consumers as **evidence inputs** to it; contradiction-as-feature (A.Q2) | needs Phase-0 ceiling + M2 |
| **3 — Delta rework** | the one new signal | **`T-COMV2-DELTA-1`** build behind default-off flag vs prompt-D fixtures; **live activation** + emitter two-point emission (NEW) | **build** anytime; **live** only if Gate-Capture = yes |
| **4 — Eval discipline** | trustworthy numbers | measured-real holdout + sim-to-real test (C.Q4); calibration metrics (ECE/Brier/reliability); per-family CIs (C.Q5) | depends on Gate-Data |

Phases 1, 2, and the *build* of 3 are independent of the data gates and can proceed; **live accuracy gains in 2–3 are capped until Gate-Data and Gate-Capture clear.** The 13 forward-registered consumers stop being additive bumps and become inputs to the Phase-2 fusion stage — that is the structural change that unifies them.

---

## 6. Success criteria & what NOT to do

**Done means (rework-level):**
- The engine reports **top-1 and top-3** (+ any-correct-in-k) on a **measured-real, provenance-audited eval subset**, with **calibrated** confidence (reliability diagram / ECE / Brier shown), per-family **recall CIs**, and abstention on low-support families and within-noise deltas.
- The fusion stage is **grep-confirmed read** in a live path; the single-point path is **byte-identical** when no second frame / no calibration data (regression-locked).
- Every new numeric literal (noise floors, lag, tiers, bands) carries a source citation; every new field has a named consumer in the same change.

**Do NOT:**
- Chase **85 %** on the current corpus — it is below the measured ceiling (R1); set the target from Gate-Data.
- **Weight-tune** the additive ranker (proven 0 pp; "scoring tightening is a smell") — skip F2 unless M1 shows gaps < 0.10.
- Build the delta module **live** before Gate-Capture, or rebuild the corpus inside the delta task (that is the Gate-1 follow-up).
- Add cross-lab imports, emit verdicts from emitter labs, or rebuild any graph.
- Treat synthetic-corpus accuracy as real before the sim-to-real holdout test.

---

## 7. Decisions for the human / manager (the gates)

1. **Gate-Capture (product, dominant):** can the field workflow capture a **second operating-point frame** (low idle + ~2500 RPM, optionally + ~3750 RPM stress)? **The GAS/OBD schemas already support it (§8) — this is a corpus/workflow *population* decision, not a build.** Yes → the delta rework (R3, highest-leverage new signal) is real. No → record DeltaLab deferred-pending-data; lean on Phases 1–2 only.
2. **Target:** accept a **measured ceiling (~70–80 %) + decision-support differential** product, or fund **real data collection** to lift the ceiling? (R1 says you cannot have 85 % on the current four single-point channels.)
3. **Canonical operating-point pair:** confirm **curb idle + 2500 RPM** as canonical (stress idle 3750 as optional second elevated point), so band reconciliation is closed before `T-COMV2-DELTA-1` builds.
4. **Fusion family:** approve the staged path (Bayesian log-odds + conflict feature → DS/PCR5 where needed → stacking only if a paired dataset is funded).

---

## 8. Reconciliation with the reworked emitter labs + web-settled method choices

Added after the first draft, from a reality-check of the **already-reworked** emitter labs (GASLab S1, OBDLab S2, DTCLab S3, DNALab) and two targeted web searches. Three of the four items **correct or sharpen** the draft; none overturns its direction.

**8.1 — The two-point contract already largely exists (corrects R3 / Gate-Capture framing).**
The draft inherited the DeltaLab proposal's "emitters are single-point" shorthand. Codebase reality:
- **GASLab** emits an *optional* second frame: `process.py: reading_high: GasReading | None` ("optional high-idle (2500 RPM) reading, T-GV2-4"), `contracts.py: high_idle_{hc,co,co2,o2,nox,lambda}`, and `dna_view.py: co_low_idle / co_high_idle`. So **Δgas is computable from GASLab's own emitted frames** when the high-idle reading is present.
- **OBDLab** already carries the second operating point: `config/obd_translation_rules.yaml` defines `REGULATORY_HIGH_IDLE` and `STRESS_IDLE` buckets keyed to `stress_idle_rpm_target` (from VinDNA), and `core/sensor_signal_translator.py` "accumulates stabilized and stress idle bands for two-point MAF/MAP linearity checks" (`maf_linearity.py` already computes a two-point non-linearity delta).
- So the **schemas/contracts support two operating points today**; what is single-point is the populated `cases_petrol_master_v6.csv`. **Net:** `T-COMV2-DELTA-1` is correctly a *wiring* task (it says so); Gate-Capture is a **corpus/workflow population** decision, not a plumbing build. The draft's "delta can't lift accuracy because emitters are single-point" was too strong — corrected in R3 and §7.1.

**8.2 — Emitters emit categorical validity, not numeric σ (sharpens E.Q2).**
GASLab emits a `SampleValidity` enum (`contracts.py`, `validity_gates.py`); OBDLab emits `rpm_state_bucket`/`COLD_OPEN_LOOP_INVALID`-style gates. **No lab emits a per-reading numeric uncertainty.** Therefore the inverse-variance fusion weights must take `σ_meas` from **analyzer/scan-tool specifications** (the ±-bands in D/E), and use the emitted `SampleValidity` as a **hard abstain gate**, not as σ. Corrected inline in §3.E.Q2.

**8.3 — DTCLab already produces freeze-frame (fills a draft omission).**
`dtclab/core/freeze_frame_extractor.py` + `data_fusion_sanitizer.py` ingest **Mode $02 freeze frame** (and Mode $06 monitor data) and classify historical fault context. The draft did not name freeze frame. **Decision:** treat freeze frame as a **conditional OBD-side evidence channel — present only when a DTC is stored — fused at the verdict stage, never as a delta input** (it is a single, asynchronous, uncontrolled-operating-point snapshot). Its uses: corroborate/contradict the live delta (confidence adjustment), and catch **intermittent/load-specific faults** the no-load delta cannot reproduce, guarding against false "no-fault." Named consumers already exist: `T-COMV2-NOSTART-1` (FF fuel/spark-cut state) plus the new fusion stage's intermittent-fault branch. Caveat: generic OBD-II stores **one priority frame** (may belong to a higher-priority DTC than the one under investigation — check Mode $02 PID $02), and only on 1996+ vehicles. *This is a new sub-task under Phase 2.*

**8.4 — Web-settled method choices (the two biggest open method decisions).**
- **Calibration under small/imbalanced/noisy labels (sharpens B.Q1):** the literature confirms isotonic regression beats Platt **only with enough examples per class** and is **not** validated for many-minority-class imbalance — it overfits the single-digit-N bins here; **sigmoid/Platt (extra intercept helps under imbalance) or temperature scaling are the safer post-hoc choices**, fit on a minority-stratified split, with **conformal prediction** supplying a finite-sample coverage guarantee for the differential. This is exactly the small-data regime ("Better Classifier Calibration for Small Data Sets").
- **Fusion family without training data (validates the staged path in E.Q4):** current uncertainty-aware late-fusion practice **calibrates each modality first (temperature/isotonic), then fuses** with a menu of rules (max / mean / product-odds / Dempster–Shafer / a learned logistic rule). This confirms **calibrate-per-modality → simple combiner first → conflict-aware DS only where high-conflict cases demand it**, and that DS's well-known high-conflict pathology is real (hence entropy/conflict-aware variants). So the draft's staged recommendation stands, with one ordering refinement: **calibrate before fuse.**

**8.5 — What web research could NOT settle (genuine, still-open gaps).**
Re-searching confirms the gaps the A–E packs already flagged are **genuinely unpublished**, not a search miss: no public dataset pairing 5-gas + OBD PIDs at ≥2 points per vehicle with a confirmed fault; no quantified gas↔OBD conflict thresholds; no peer-reviewed magnitude for the speed-density trim-null. These cannot be closed from the web — only by **field capture** (the Gate-Capture / prospective-validation path). The plan already treats delta accuracy as unvalidated until then; no change needed beyond stating it.

---

*Grounding: `labs/comlab/research/{AUDIT_ANSWERS_COMLab,AUDIT_PART1_CEILING_RESEARCH,OPEN_LEVERS_COMLab,PROPOSAL_DeltaLab_cross_lab_delta_module,deep-research-report,deep-research-reportC,Automotive Diagnostic Fusion Research,DeltaRes1,DeltaRes2,Two-Point Emissions Test Fixture Design,Multi-Sensor Fusion for Automotive Diagnostics}.md`; `labs/comlab/tasks/{PROGRESS.md,T-COMV2-DELTA-1_cross_lab_delta_module.md}`; `labs/comlab/comlab/{core,schemas,config}/…`; `wiki/COMLab_Diagnostic_Logic.md`. Emitter reality: `labs/gaslab/gaslab/{process,contracts,dna_view}.py`, `labs/obdlab/obdlab/{config/obd_translation_rules.yaml,core/sensor_signal_translator.py,core/maf_linearity.py}`, `labs/obdlab/docs/ADR_OBDLab/ADR-0002`, `labs/dtclab/dtclab/core/{freeze_frame_extractor,data_fusion_sanitizer}.py`. Web (§8.4): calibration & late-fusion sources listed in the chat Sources.*
