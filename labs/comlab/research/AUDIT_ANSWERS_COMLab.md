# COMLab audit questions — researched answers

**Author:** architect (4DLab) · **Date:** 2026-06-19
**Question source:** `docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md` → COMLab § (Q1–Q10).
**Method:** Each question was classified as **web-researchable** (external method/benchmark knowledge the codebase cannot hold) or **internal** (answerable from this repo's docs, config, and corpus triage, with web confirmation only if in doubt). Web-researchable questions are routed to two thematic prompts — `WEB_RESEARCH_PROMPT_A_scoring_and_fusion.md` (scoring paradigm + evidence fusion) and `WEB_RESEARCH_PROMPT_B_calibration_and_differential.md` (confidence calibration, differential output, symptom-prior magnitude); internal questions are answered here with inline file citations.

---

## Classification summary

| Q | Topic | Bucket | Where answered |
|---|---|---|---|
| Q1 | hand-tuned additive vs learned ranker; comparable engine accuracy | **web** | prompt A §1 |
| Q2 | Bayes-optimal ceiling on this corpus | **internal** | below |
| Q3 | contradiction-as-discriminator without destructive override | **web** | prompt A §2 |
| Q4 | calibrated-likelihood / Bayesian fusion vs additive | **web** | prompt A §3 |
| Q5 | confidence calibration → real likelihood-ratio tiers | **web** | prompt B §1 (+ internal state note below) |
| Q6 | minimal additional evidence to break family ties; is it available | **internal** | below |
| Q7 | top-2/top-3 differential vs single verdict | **web** | prompt B §2 (+ internal state note below) |
| Q8 | magnitude of the operator-symptom prior | **web** | prompt B §3 (+ internal state note below) |
| Q9 | precision/recall of loosening the prune gate on this corpus | **internal** | below |
| Q10 | is the fault-family taxonomy well-posed (MECE) | **internal** | below |

Prompt **A** = `WEB_RESEARCH_PROMPT_A_scoring_and_fusion.md` (Q1, Q3, Q4); prompt **B** = `WEB_RESEARCH_PROMPT_B_calibration_and_differential.md` (Q5, Q7, Q8). The six web-routed questions ask *what other systems/methods achieve* — knowledge the repo cannot contain. Q5/Q7/Q8 also have a concrete **internal current-state** that is recorded below so the research answer can be calibrated against what the engine does today.

---

## Q2 — Bayes-optimal accuracy ceiling given the corpus's actual signal content *(internal)*

**Answer: the corpus's own failure triage implies the ceiling is well below the 85 % target with the evidence currently collected — there is a hard irreducible-error floor of ~9–10 %, and a realistic ceiling in the ~70–80 % band unless new evidence channels are added.** This is an estimate from the engine's own triage, not a formal Bayes-error computation (which the web prompt §1/§3 supports methodologically).

Reasoning from the latest in-scope triage (`AUDIT … §1.1`, sourced from `diag/DIAG_SUMMARY.md` and the REG triage):

- **Irreducible floor — `data-gap (STOP)`: ~27 `ecu_fault` cases.** The discriminating signal (`lambda_perception_delta`, trim divergence) is **absent** from the data — OBDLab emits `NO_FAULT` across all of them (`AUDIT §1.2 Culprit 2`). No model can recover these from the collected evidence. On a ~281-case corpus that is ~9.6 % of cases that are *provably* unrecoverable → a naive ceiling of ~90 %.
- **Additional under-determination — Culprit 4.** `mechanical_wear`, `exhaust_leak`, `ignition_fault`, `non_starter`, and several `ecu_fault` cases "share chemistry/DTC signatures with louder families (misfire, lean) and lose every tie" (`AUDIT §1.2 Culprit 4`). These are not all recoverable either: where two families are genuinely indistinguishable with the four collected channels, the Bayes-optimal classifier must still err on a fraction. Per-family scores show this is sizeable: `catalyst_failure` 11/22, `sensor_fault` 10/24, `exhaust_leak` 7/9 dying at the validity gate.
- **The OUTRANKED bucket (~82–90 cases) is the swing factor.** These have the correct rule present (so they are *not* irreducible), but **64/90 carry no DTC** (`AUDIT §1.2 Culprit 1`), so the primary tie-breaker is starved. How many are truly separable vs genuinely under-determined is exactly the Bayes-error question — and it is the difference between a ~70 % and a ~85 % ceiling.

**Conclusion for the architect:** the honest internal read is that **85 % is not reachable on this corpus with the four current channels** — the irreducible floor plus the indistinguishable-family fraction caps it lower. This matches the audit's own one-sentence diagnosis: the binding constraint is the **data/signal channels, not the engine logic** (`AUDIT §4`). Before more ranking engineering is spent, the formal estimate (Bayes-error / irreducible-error estimation method — web prompt §1, §3) should be run on the corpus to fix the real target. **Sources:** `AUDIT §1.1, §1.2 (Culprit 2 + 4), §4`.

---

## Q6 — Minimal additional evidence that breaks shared-signature ties, and is it ever available? *(internal synthesis)*

**Answer: for each colliding pair the minimal tie-breaker is known from the per-channel research already done — but for the dominant error mode (no-DTC OUTRANKED cases) it is structurally *unavailable*, which is why porting rules moved 0 pp.** The tie-breakers, by collision:

| Colliding families | Minimal evidence that breaks the tie | Available on this corpus? |
|---|---|---|
| **misfire vs mechanical_wear** | per-cylinder contribution / relative-compression + HC pattern; oil-burn (`POA`) markers route to mechanical_wear (`tag_discriminator.yaml: POA_HISTORY → mechanical_wear`) | partial — POA tag yes; per-cylinder contribution **not a payload field** |
| **lean vs vacuum-leak vs exhaust-leak** | idle→2500 RPM fuel-trim shift (vacuum leak trim →0 at RPM; restriction worsens) — quantified in `obdlab/research/AUDIT_ANSWERS_OBDLab.md Q2`; pre-cat air leak = low CO + high O₂ + low HC (GASLab) | partial — needs a 2-speed sample; single warm-idle snapshot often can't |
| **ecu_fault (perception) vs genuine mixture fault** | `lambda_perception_delta` (ECU λ vs Brettschneider λ) + per-bank trim symmetry — `obdlab/research/AUDIT_ANSWERS_OBDLab.md Q1` | **no** for the 27 STOP cases — OBDLab emits `NO_FAULT`; the signal is absent |
| **sensor_fault (lazy/biased/dead O₂)** | O₂ switch-rate / amplitude / response-time, and bank-specificity | partial — scan-tool O₂ metrics are not all payload fields today |
| **cam_timing vs generic misfire** | idle-vs-2500 gas signature + VVT codes (`VVT_HISTORY → cam_timing`); symptom `poor_acceleration → cam_timing` prior | partial — VVT code rarely present; symptom prior is weak (see Q8) |

**The structural finding:** the engine's primary rank discriminator is the DTC routing tag (`tag_discriminator.yaml`, weight 0.10), but **64 of 90 OUTRANKED cases carry no DTC at all** (`AUDIT §1.2 Culprit 1`), so the minimal tie-breaker that *would* work is absent in the majority of the cases that need it. This is why `T-FX-REG-2` rescued 37/44 PRUNED cases yet accuracy did not move — the rescued rule simply gets outranked, with no surviving signal to break the tie (`AUDIT §2 Wave E`). **The minimal evidence exists in principle, is documented per-channel, and is unavailable in practice for the dominant error mode.** **Sources:** `comlab/comlab/config/tag_discriminator.yaml`, `obdlab/research/AUDIT_ANSWERS_OBDLab.md Q1–Q3`, `AUDIT §1.2 (Culprit 1, 4), §2 (Wave E)`.

---

## Q9 — Precision/recall tradeoff of loosening the prune gate on this corpus *(internal)*

**Answer: loosening the prune gate buys recall that does not convert to accuracy — the recovered candidates are outranked, so net precision is ~unchanged while false-positive risk rises.** This is measured, not hypothetical:

- The gate prunes in three passes — **horizon**, **hardware (missing_evidence)**, and **chemistry** (`comlab/comlab/core/fault_atlas_router.py: _prune_candidates`, reasons `horizon` / `missing_evidence` / `chemistry`; `wiki/COMLab_Diagnostic_Logic.md` Stage B). `candidates_out` has been observed as low as 6 (`AUDIT §3 COMLab-Q9`).
- The natural "loosen the gate" experiment was already run as coverage expansion: `T-FX-REG-2` added 24 coverage rules and **rescued 37/44 PRUNED cases → accuracy stayed at 51.2 %** (`AUDIT §2 Wave E`). Recall on the never-surfaced bucket went up; top-1 accuracy did not, because the rescued rule loses the rank.
- `T-FX-REG-4` re-measure: **0 delta, bottleneck simply shifted PRUNED → OUTRANKED** (`AUDIT §2 Wave E`). So the gate is not the binding constraint; loosening it relocates the loss rather than removing it.

**Conclusion:** on *this* corpus the prune gate is already near the right operating point — it occasionally drops the correct rule (a real recall cost), but tightening or loosening it reshuffles between the PRUNED and OUTRANKED buckets without net accuracy gain. The precision risk of loosening (more low-base-weight candidates surviving to be wrongly promoted by the 0.10 discriminator/prior) is not worth the recall, because the recovered cases cannot win the rank anyway. The lever is the **rank step**, not the gate. **Sources:** `comlab/comlab/core/fault_atlas_router.py`, `wiki/COMLab_Diagnostic_Logic.md` (Stage B), `AUDIT §2 (Wave E), §3 COMLab-Q9`.

---

## Q10 — Is the fault-family taxonomy well-posed (mutually exclusive, collectively exhaustive)? *(internal)*

**Answer: collectively exhaustive — yes (a `no_fault` sink + an `invalid_input`/abort path close the space); mutually exclusive — no. Several families overlap by construction, and that overlap is a real cap on accuracy, not a labelling accident.**

The live taxonomy is **12 `FaultFamily` enum values** (`comlab/comlab/schemas/vocabulary.py: FaultFamily`): `lean_condition, rich_mixture, misfire, sensor_fault, ecu_fault, catalyst_failure, exhaust_leak, ignition_fault, mechanical_wear, cam_timing, non_starter, no_fault`, plus `invalid_input` in the KG (`comlab/comlab/config/kg/`). These route onto the **8-family SAE J2012 / ISO 15031-6 P-code backbone** (`comlab/comlab/config/proposals/taxonomy_backbone.md`).

**Collectively exhaustive: yes.** `no_fault` absorbs "all diagnostics pass," `invalid_input` + the Stage-A fatal gates (`ERR-ABORT-001/002/004`, `wiki/COMLab_Diagnostic_Logic.md`) absorb un-diagnosable sessions, and `OPTIMAL_HEALTH` is the default when no row scores. Nothing falls outside the label set.

**Mutually exclusive: no — and the overlaps are structural:**

- **`exhaust_leak` ⊂ `lean_condition` symptom-space** — a pre-cat leak presents as false-lean; `tag_discriminator.yaml` maps both `EGR_HISTORY` and EVAP leakage onto families that collide with lean (`EVAP_HISTORY → lean_condition`).
- **`mechanical_wear` is a catch-all** — `tag_discriminator.yaml` routes five distinct tags (`POA_HISTORY`, `IDLE_CONTROL_HISTORY`, `THERMAL_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, and parts of `KNOCK`) into `mechanical_wear`, which means it overlaps misfire, sensor, and cooling-system causes rather than being a crisp family.
- **`sensor_fault` vs `ecu_fault`** — both are "perception is wrong"; the boundary is *where* the error originates (sensor/harness vs PCM), which is exactly the truth-vs-perception axis the corpus cannot always measure (Q2, Q6).
- **`misfire` vs `ignition_fault` vs `cam_timing`** — all three can present the same incomplete-combustion gas signature; the registry itself notes "severe cam/crank misalignment … reads as partial burn" (`global_fault_registry.json` cam-timing string).

**Conclusion for the architect:** the taxonomy is *exhaustive and standards-anchored* but **not mutually exclusive** — at least four family pairs share a signature with the collected evidence, which means a forced single-label verdict must mislabel a fraction of cases no matter how the ranker is tuned (this is the taxonomy-level half of the Q2 ceiling). The MECE defect is foundational, not cosmetic; the two clean responses are (a) merge or explicitly hierarchy-nest the colliding families, or (b) emit a **ranked differential** rather than forcing one label (see Q7). **Sources:** `comlab/comlab/schemas/vocabulary.py (FaultFamily)`, `comlab/comlab/config/kg/`, `comlab/comlab/config/proposals/taxonomy_backbone.md`, `comlab/comlab/config/tag_discriminator.yaml`, `global_fault_registry.json`, `wiki/COMLab_Diagnostic_Logic.md`, `AUDIT §1.2 Culprit 4`.

---

## Internal current-state notes for the web-routed questions

These do not answer Q5/Q7/Q8 (the *knowledge gap* is external — see the web prompt) but they pin what the engine does **today**, so the research can be calibrated against it.

- **Q5 (confidence tiers).** The engine emits `ConfidenceRating ∈ {HIGH_ASSURANCE, DEGRADED_ASSURANCE, LOW_CERTAINTY}` (`comlab/comlab/schemas/vocabulary.py: ConfidenceRating`). **These reflect evidence-chain completeness/degradation, not a calibrated diagnostic likelihood ratio** — i.e. they answer "how many labs reported cleanly," not "how likely is this verdict correct." The audit's "scoring tightening is a smell" memo (`AUDIT §3 COMLab-Q5`) is the symptom of this: nudging weights reshuffles ranks without changing a meaningful confidence. Prompt B §1 asks for the calibration method to convert scores into real likelihood-ratio tiers.

- **Q7 (top-k differential).** The output path **already carries a top-3 differential**: `DifferentialSiblingOut` with `confidence_score` and `differential_siblings: list[...] (max_length=5)` in `comlab/comlab/schemas/response.py`, populated from `runner_ups = scored[1:4]` ("at most 3", HLD §4.2 step 8) in `comlab/comlab/core/fault_atlas_router.py`. So the *mechanism* exists; what is open is the **metric/product** question — whether to score against top-k (which would change the accuracy target materially, given the MECE overlaps in Q10) and the documented user value of doing so. Prompt B §2.

- **Q8 (symptom-prior magnitude).** Currently `prior_weight: 0.10`, bounded-additive, applied only when the reported symptom is non-blank, mapping e.g. `running_rough → misfire` (90 % purity, 42/281 cases) (`comlab/comlab/config/symptom_prior.yaml`). It fires on ~47/281 cases with **0 false-positive delta** but tiny lift (`AUDIT §2 Wave D`). DNALab researched the *empirical predictiveness* of symptoms (`dnalab/research/WEB_RESEARCH_PROMPT_symptom_prior_and_vin_decode.md`); the COMLab-specific open question is the **magnitude** other decision-support systems assign a self-report and how to bound it — prompt B §3.

---

## Coverage check

All 10 COMLab audit questions are accounted for: **Q2, Q6, Q9, Q10** answered internally above; **Q1, Q3, Q4** routed to `WEB_RESEARCH_PROMPT_A_scoring_and_fusion.md` and **Q5, Q7, Q8** to `WEB_RESEARCH_PROMPT_B_calibration_and_differential.md` (with Q5/Q7/Q8 internal current-state pinned above). No question is dropped or deferred without a destination.
