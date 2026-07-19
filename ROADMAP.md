# 4DLab v2 — Roadmap (navigation, not spec)

**Date:** 2026-06-04 · **Source of truth:** `4DLabV2/docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md`
**Read this first** so a fresh session knows the plan before opening any ledger.

## The diagnosis (one line, from the audit)

The engine is **ranking-bound at 51.2%**, not coverage-bound. The tie-breakers it
needs — DTC presence, OBD trim/perception signal, per-vehicle baselines,
trustworthy symptom labels — are **missing from the data, not the code**. So v2
gains come from new *evidence channels* and *research answers*, not more rules or
weight-tuning (weight nudging hits a ~45% reshuffle ceiling — see
[[feedback_scoring_tightening_smell]]).

## Sequencing (user roadmap)

**GASLab → OBDLab → DTCLab**, then **COMLab reworked LAST, registry reconciled
alongside COMLab.** Rationale: COMLab is the prune→rank spine that consumes every
upstream channel; reworking it before the emitters and the research gates are
settled would tune against a moving target. The labs are isolated (JSON-only
boundaries, no cross-lab imports), so each emitter can move to v2 while consumers
stay intentionally divergent until the COMLab stage — this matches the v2 wiki's
"revised first, divergent until consumers catch up" stance.

| Stage | Lab | v2 focus (from audit) | Ledger | Status |
|---|---|---|---|---|
| 1 | **GASLab** | Contract reconcile to 34 (cam-timing split) → then chemistry-discrimination depth for the big gaps: `TIMING_RETARDED` separation (~25% of corpus, 7 families), `mechanical_wear` (0/11, no distinct chemistry), pre-cat `exhaust_leak` vs sample error (7/9 die at the validity gate), idle-vs-2500rpm for catalyst & cam timing. | `4DLabV2/labs/gaslab/tasks/PROGRESS.md` | ✅ done (T-GV2-1..15 complete) |
| 2 | **OBDLab** | First a **scope decision**: revive vs quarantine (>95% NO_FAULT on this corpus). If revived: realistic STFT/LTFT per fault family, `lambda_perception_delta` computability, downstream-O₂ masking signal, Mode $06 discriminators. Prune fields with no signal channel under signal/noise. | `4DLabV2/labs/obdlab/tasks/PROGRESS.md` | ✅ done (revived as emitter; T-OBDV2-* complete) |
| 3 | **DTCLab** | The **#1 leverage** per the audit: DTC-presence reality (64/90 outranked have no DTC) + empirical P-code→family mapping strength; DTC-state weighting (pending/confirmed/permanent), multi-DTC patterns, freeze-frame params. Clear the `T-FX-13` hex-regex contract gap. | `4DLabV2/labs/dtclab/README.md` | ✅ done (Stage 3 closed: T-DTCV2-NOSTART-1 + FIX) |
| 4 | **COMLab + registry** | The ranking spine. Decide architecture: can a hand-tuned additive ranker beat ~55%, or is a learned/statistical/Bayesian-fusion ranker required? Consolidate the **two split registries** (REG-V2 shim vs COMLab-internal). Reconcile registry chemistry vocab + all consumer mirrors here (incl. GASLabV2 T-GV2-2, registry FU-1, `OBD_VOCABULARY §17`). Consider top-2/3 differential output. | `4DLabV2/labs/comlab/README.md` + `registry/REGISTRY_START_HERE.md` | last |

## Research-first gate (run in parallel; resolve before deep Stage-4 work)

The audit (Part 4) argues several questions really ask *"is 85% achievable with
this data at all?"* — answer these before spending heavy engineering chasing it:

1. **DTC presence rate + P-code→family mapping strength** (DTCLab) — the starved
   primary discriminator; if no-DTC is the norm, the architecture needs a
   primary discriminator that doesn't assume a DTC.
2. **`TIMING_RETARDED` family-separation chemistry** (GASLab) — one state, 25%,
   7 families; the largest concentrated discrimination gap.
3. **Is `ecu_fault` separable from real mixture faults at all** (OBDLab + GASLab)
   — decides if the 27 `data-gap (STOP)` cases are recoverable or conceded.
   **Partially answered 2026-06-05** → `ARCHIVE/2026-06-06_v2restructure/4DLabV2/planning/sprints/stage1_gaslab/studies/STUDY_ecu_fault_gas_signatures_merge.md`:
   yes, but only via gas↔OBD divergence at the COMLab fusion layer (GASLab adds no
   gas-only signature). Resolution path = `4DLabV2/labs/gaslab/tasks/TASK_SUITE_ecu_fault_diagnosis.md`
   (5 most common faults; cranking/non_starter still open).
4. **Bayes-optimal ceiling + taxonomy well-posedness** (COMLab) — sets the real
   target before more rules are written.
5. **Operator-symptom predictiveness** (DNALab/VINLab) — the cheapest independent
   channel; quantify its true strength before leaning on the prior.

DNALab/VINLab is not a separate build stage — its outputs feed the COMLab prior;
its research question (#5) is folded into the gate above.

## Governing constraints (unchanged, apply to every stage)

- **Signal/noise:** every field/enum value added to any schema needs a named,
  existing consumer in COMLab analytics or fault-atlas routing. No consumer → it
  doesn't ship. This is the one rule that governs every v2 change.
- **v2 wiki is canonical** for the lab being reworked (e.g. GASLab → `docs/GASLab/wikiNEW/`);
  code reconciles *up to* the wiki. Legacy `v2/`, `v6/`, and v1 wikis are not truth.
- **No cross-lab Python imports;** consumers mirror types locally.
- **Reports in `.md` only.** One task ≤ 50% of a fresh context; both gates clean
  before `done`.

## Pointers

- Audit + research questions: `4DLabV2/docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md`
- Stage-1 ledger: `4DLabV2/labs/gaslab/tasks/PROGRESS.md` (T-GV2-1 emitter; T-GV2-2 deferred to Stage 4)
- Session bootstrap table: `CLAUDE.md` (maps each `<LAB>V2_START_HERE.md`)
- Per-lab v2 ledgers for OBD/DTC are stood up at the start of their stage via the
  `_skills/coding-bootstrap` pattern (mirror the GASLabV2 scaffold).
