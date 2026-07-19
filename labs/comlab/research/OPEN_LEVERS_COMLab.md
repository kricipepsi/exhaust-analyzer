# COMLab — open levers (measure-now / fix-now / new questions)

**Author:** architect (4DLab) · **Date:** 2026-06-19
**Status:** analyst notes that surfaced while answering the audit Part 1 + Part 3 COMLab questions. These are **not** in the audit's 10-question packs; they are cheap, mostly internal, and decide where engineering effort should go *before* it is spent. Companion to `AUDIT_ANSWERS_COMLab.md` and `AUDIT_PART1_CEILING_RESEARCH.md`. The radical-rework idea (a cross-lab delta module) is split into its own file: `PROPOSAL_DeltaLab_cross_lab_delta_module.md`.

---

## A. Measure now — cheap experiments that decide strategy

These need no new data and little code; each one resolves a strategic fork.

| # | Question | Why it matters | How to check |
|---|---|---|---|
| **M1** | **What is the score-gap distribution in the OUTRANKED bucket?** For each of the ~82–90 cases, how far does the correct rule lose by? | The two tie-breakers (symptom prior, routing tag) are bounded-additive at **0.10** (`config/symptom_prior.yaml`, `config/tag_discriminator.yaml`). A 0.10 nudge can only rescue a case losing by **< 0.10**. If most gaps exceed 0.10, **no bounded discriminator can ever fix them** — stop tuning weights. This is the empirical, on-corpus answer to COMLab Q1. | Instrument `fault_atlas_router.execute_triage_loop` Phase 5 to log `winner_score − correct_rule_score` for every mislabeled case; histogram it. One run. |
| **M2** | **What fraction of cases run `FULL_FUSION` vs `GAS_DOMINANT`?** | Every OBD-side discriminator the OBDLab research unlocked (bank symmetry, perception delta, VE) only applies in `FULL_FUSION` (`wiki/COMLab_Diagnostic_Logic.md` Degradation Modes). If many cases are gas-only, the ceiling is **gas-bound** and OBD work can't move it. | Count `degradation_mode` over the corpus from existing traces. |
| **M3** | **How many cases are silently rejected at the Stage-A gate by the known contract mismatches** (`T-FX-12` O2 enum missing `WIDEBAND_NB_SIM`; `T-FX-13`/`T-FX-DTCHEX-1` DTC regex decimal-only vs hex)? | These reject *valid* payloads before they ever reach the ranker — invisible recall loss, possibly free to recover. Audit flagged them as "correctness," but nobody counted the cases lost. | Count Stage-A `ERR-ABORT-*` and DTC-validation drops attributable to these two patterns. |
| **M4** | **Of the OUTRANKED cases, how many are true within-ε ties vs decisive losses?** (refinement of M1) | Distinguishes "ranker is almost right, needs a nudge" from "ranker is structurally wrong." Sets whether the fix is a discriminator or a scoring-paradigm change (prompt A). | Same instrumentation as M1, bucketed by gap < 0.05 / 0.05–0.10 / > 0.10. |

**M1 is the highest-value single experiment in this doc** — it tells you whether the project's stated lever ("promote routing tags into rank weight") is mathematically capable of working, before more is invested in it.

---

## B. Fix now — known payoff, not research

| # | Fix | Payoff | Source |
|---|---|---|---|
| **F1** | **Consolidate the two registries** (REG-V2 shim vs COMLab-internal `global_fault_registry`). Rules are stranded across both; the harness never saw the REG-2/5 additions. | **Measured: +4 cases → 52.7 %** (`T-FX-WIRE-2` premeasure, `AUDIT §2 Wave E` + Part 2 takeaway #2). Already a COMLab Stage-4 deliverable — just unbuilt. | audit Part 2; pre-COMLab audit F-01 (out-of-tree `registry` dep). |
| **F2** | **Invert generic-vs-specific base-weight precedence** (see Q-new below) — cap family-level generic rules below specific rules so specificity wins ties by construction. | Directly attacks the OUTRANKED bucket at its mechanism; likely larger than the 0.10 discriminator. **Gate on M1 first** (only worth it if gaps are within reach). | `config/tag_discriminator.yaml` comments (LC-001=1.0, RM-001=1.0 outrank specific rules). |
| **F3** | **Reconcile the dual "engine-warmed" thresholds** — 70 °C (`vocabulary.py:345`, trim-analytics gate) vs 75 °C (`vocabulary.py:195`, `COLD_OPEN_LOOP_INVALID`). | Removes inconsistent gating on borderline-temp cases. Low effort, correctness. | `wiki/COMLab_Diagnostic_Logic.md` Gate 2. |

---

## C. New questions worth answering

- **Q-new-1 — Should generic family rules carry a *lower* score ceiling than specific rules?** The OUTRANKED losses happen because generic rules (`base_weight` 0.95–1.0) outscore specific faults whenever no exact P-code matches (`tag_discriminator.yaml`). The current design breaks ties by "higher `base_weight` wins" (`COMLab_Diagnostic_Logic.md` Scoring) — i.e. the **least specific rule wins the tie**. Inverting that precedence (specificity as a hard ordering, not an additive nudge) is a sharper lever than calibration (Q5) and is testable on-corpus. *(pairs with M1/F2)*

- **Q-new-2 — Is the missing discriminating dimension a *delta*, not a better weight?** The audit's Culprit 4 (families indistinguishable) and the `TIMING_RETARDED`→7-families gap are both **single-snapshot** collisions. The existing OBDLab delta research shows several of these families separate cleanly on the **sign of the change across an RPM step** (e.g. worn rings *intensify*, worn valve seals *clear*). This reframes the ceiling as **snapshot-bound, not ranking-bound**, and is the basis of the DeltaLab proposal. → `PROPOSAL_DeltaLab_cross_lab_delta_module.md`.

- **Q-new-3 — Does the real product workflow capture signals the corpus under-represents?** Symptom density was synthetically enriched 17.8 %→31.7 % (`AUDIT §2 Wave D`); the symptom prior fires on only ~47 cases. If the deployed workflow always captures an operator symptom (and/or a second RPM point — see DeltaLab), several priors/channels are far more valuable than the corpus implies. This is the scope question OBDLab Q10 raised, applied to COMLab's inputs. *(decides how hard to lean on the cheap channels)*

---

## Cross-references

M1/M4 are the on-corpus test of `AUDIT_ANSWERS_COMLab.md` Q1 and Q2 (Bayes ceiling). F1 is the audit Part 2 unclaimed gain. Q-new-2 is developed in `PROPOSAL_DeltaLab_cross_lab_delta_module.md`. None of these duplicates a Part 3 question or a web prompt (A/B/C).
