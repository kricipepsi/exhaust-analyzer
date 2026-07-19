# Proposal — DeltaLab: a cross-lab delta module as COMLab's primary discriminator

**Author:** architect (4DLab) · **Date:** 2026-06-19 · **Status:** proposal (radical-rework candidate)
**Origin:** user idea (a module that computes deltas across the three emitter labs) + the existing, already-researched delta work in `labs/obdlab/research/chunks/delta-relations/` (6 ΔTrim chunks + a 25-case 2-speed Δgas matrix + ΔO₂ feeders), whose named-but-unbuilt consumer is the **"COMLab delta-calculation script (FU-2)."**

> **One-line thesis:** the engine is **snapshot-bound, not ranking-bound.** The fault families that collide in the corpus collide because they are read at **one operating point**. Most of them separate on the **sign of the change across an RPM step**. A delta module turns that change into a new, DTC-independent primary discriminator — the one channel the audit says is missing.

---

## 1. Why this attacks the actual ceiling

The audit's two hardest culprits are both single-snapshot problems:

- **Culprit 4 (families indistinguishable):** `mechanical_wear`, `exhaust_leak`, `ignition_fault`, several `ecu_fault` share static signatures with misfire/lean. The OBDLab delta research shows they **diverge under an RPM step**: worn piston rings **intensify** (oil burn scales with blow-by + ring speed) while worn valve seals **clear** (vacuum drop stops guide pull) — *both read "elevated HC" at idle* (`delta-relations/07_gas-transition-matrix-2speed`). Only `sign(Δgas)` resolves them.
- **`TIMING_RETARDED` → 7 families** (the single biggest discrimination gap, ~25 % of cases): a static state that maps to many families is precisely what a delta dimension disambiguates.
- **Culprit 1 (DTC-starved ranking, 64/90 outranked have no code):** deltas need **no stored DTC** — they are computed from two live readings. A delta discriminator is the "primary discriminator that does not assume a DTC exists" the audit explicitly calls for.

This is the rare lever that adds **genuinely new discriminating signal** rather than re-weighting old signal — which the ledger shows is the only thing that ever moved accuracy (the +1.4 pp from the DNA channel; everything since is ≤ +4 cases). It directly tests the audit's §1.3 verdict that "the next gains are a data problem."

## 2. What is already in place (so this is a wiring job, not a green field)

- **Research is done and quantified (PENDING consumer only):** ΔTrim formula + per-fault profiles (`delta-relations/01–06`), the 2-speed Δgas matrix (`07`), ΔO₂ feeders (switch-freq Δf, bias ΔV, downstream transfer-index — `SWEEP_MANIFEST §7`). All carry `consumer: PENDING (COMLab delta-calculation script, FU-2)`.
- **Isolation contract already settled:** "the per-state frame is produced by GASLab/OBDLab/DTCLab; the **cross-state Δ math is COMLab**" (`delta-relations/07`). Emitters stay **stateless** → respects the no-cross-lab-imports rule and "emitters emit channels, not verdicts."
- **COMLab scaffolding already exists:** `STRESS_IDLE` (3500–4500) and `REGULATORY_HIGH_IDLE` (2200–2800) enum buckets (`schemas/vocabulary.py:212–213`); `stress_idle_rpm_target` in the input + VIN-DNA schema (`schemas/ingestion.py:105`, `schemas/lab_dna_views.py:57`); `co_low_idle` (`lab_dna_views.py:43`); a deferred `promote_stress_idle` routing candidate (`core/symptom_router.py:11`); and `FAULT_MAF_CONTAMINATION = "VE < 65% at STRESS_IDLE + positive total trim"` (`vocabulary.py:348`) — the schema already *anticipates* a second operating point.
- **Cross-channel delta math already lives in COMLab** (single-speed): `lambda_perception_delta` and `total_trim_correction_delta` (`core/perception_contradiction.py`, `core/lab_pipeline_aggregator.py`). DeltaLab generalises this from "delta between channels at one speed" to "delta within a channel across two speeds."

## 3. The hard constraint — surfaced, not buried

**The master corpus is single-point.** Each case carries one `engine_rpm` / `rpm_state_bucket` (`schemas/ingestion.py`). The two-speed data exists only in the research matrices (25 Δgas cases; the FuelTrimW ΔTrim profiles), **not** in the 281-case `cases_petrol_master_v6.csv`.

**Consequence:** a delta module **cannot lift accuracy on the current corpus** — there is no second reading to difference. DeltaLab is therefore inseparable from a **data-capture decision**: the field workflow must record a second operating point (a "blip to ~2500 RPM" 5-gas + PID frame). That is exactly the audit's central claim made actionable — *the binding constraint is the data, and the delta dimension is the missing data.* If the product cannot capture a second point, this proposal should **not** be built (it would be a speculative field with no consumer, which the signal/noise rule forbids).

So the proposal is explicitly **two-gated**:
- **Gate 1 (product/data):** can the workflow capture a low-idle + stress-idle frame pair? If no → stop; record as deferred.
- **Gate 2 (engineering):** if yes → build the module below.

## 4. Design sketch (if both gates pass)

```
GASLab ─┐  per-state 5-gas frame @ {low_idle, stress_idle}
OBDLab ─┼─►  DeltaLab (COMLab stage, stateless emitters)
DTCLab ─┘      ├─ ΔTrim   = TotalTrim(stress) − TotalTrim(low)        [01–05]
               ├─ Δgas    = {ΔHC, ΔCO, ΔCO₂, ΔO₂, Δλ} across step     [07]
               ├─ ΔO₂     = {Δf_switch, ΔV_bias, ΔTI_downstream}      [O2logic]
               ├─ ΔDTC    = maturation/freeze-frame state change      [DTC side]
               └─ architecture gate (BEFORE profiles) ──────────────  [06]
                     • speed-density (MAP-only): ΔTrim≈0 for a real leak → route to IAC/MAP-at-idle, NOT profile 02
                     • forced induction: post-turbo leak inverts ΔTrim sign (−20% STFT) → flip verdict
                          │
                          ▼
        delta_signature  →  fault_atlas_router Phase 5 as a PRIMARY rank term
                            (static single-point signature becomes the FALLBACK,
                             used in a new SINGLE_POINT degradation mode)
```

**Scoring inversion (the "radical" part):** today the ranker scores static signatures and breaks ties with 0.10 priors. DeltaLab inverts the hierarchy — **delta-signatures score first**; static signatures become the degraded-mode fallback (a new `SINGLE_POINT` sibling to `GAS_DOMINANT`). This is what makes it a rework rather than another additive nudge.

**Signal/noise consumer (rule compliance):** the new delta fields' named consumer is `fault_atlas_router.execute_triage_loop` Phase 5 (the rank step) — concrete, in a live path. This is exactly what flips the `delta-relations` chunks from `PENDING` to active and closes FU-2.

## 5. Risks / tradeoffs (must be designed for)

- **Band reconciliation (open in research):** stress band is **2500 RPM** (Δgas matrix, O2logic) vs **3500–4500** (ΔTrim FuelTrimW) vs **2500–3000** (fuel-trim/04). FU-2 must pick one canonical pair or define per-signal bands — *do not silently mix* (`SWEEP_MANIFEST §7` warning).
- **Architecture modifiers are mandatory gates, not options:** the speed-density paradox **nulls** ΔTrim for a real leak and forced induction **inverts** its sign (`delta-relations/06`). Applying the profiles without gating on air-metering/induction would *create* misclassifications.
- **Corpus rebuild:** validating DeltaLab needs a two-point corpus. Cost is real; pairs with web prompt C (synthetic-corpus validation) and OBDLab Q10 (will the product capture this).
- **Capture noise:** a hand-held second reading at unstable RPM is noisier than a single curb-idle snapshot; the sample-validity gate (`delta-relations/08` vsum 14–18 %) must run on *both* frames.

## 6. Recommendation

Pursue in this order, cheapest first:
1. **Run OPEN_LEVERS M1** (score-gap distribution) and **F1** (registry consolidation, +1.5 pp known) — they cost little and may reset the target.
2. **Answer Gate 1** (can the workflow capture two operating points?). This is a product question and it dominates everything else — it is the same decision as "is the constraint the data?"
3. **If Gate 1 is yes:** spec FU-2 / DeltaLab as above. The research is ready; it is the highest-leverage path to *new* signal and the only proposal here that structurally defeats Culprit 4. **If Gate 1 is no:** record DeltaLab as deferred-pending-data and lean on the M1/F1/F2 ranking fixes instead.

---

*Grounding: `labs/obdlab/research/chunks/delta-relations/01,06,07`, `labs/obdlab/research/SWEEP_MANIFEST.md §7`, `labs/comlab/comlab/schemas/{vocabulary.py,ingestion.py,lab_dna_views.py}`, `labs/comlab/comlab/core/{perception_contradiction.py,lab_pipeline_aggregator.py,symptom_router.py}`, `wiki/COMLab_Diagnostic_Logic.md`, audit Part 1 §1.2 (Culprits 1 & 4) + §1.3.*
