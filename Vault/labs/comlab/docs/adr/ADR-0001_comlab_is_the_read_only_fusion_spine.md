# ADR-0001: COMLab is the read-only prune→rank fusion spine

**Status:** Accepted

**Context.** 4DLab has four upstream producers (VINLab/DNALab, GASLab, OBDLab,
DTCLab) and needs exactly one place that combines their outputs into a single
diagnostic verdict for the UI. Two shapes were possible: a thick orchestrator
that re-computes chemistry/trims/lambda to "check" the producers, or a thin
terminal stage that trusts the producers and only fuses. The producers already
own their domain math and validate DNA-relative plausibility on their own input
(post horizontal-DNA flip).

**Decision.** COMLab is the **terminal, read-only fusion spine**. It accepts one
`OrchestratorInboundRequest`, runs a deterministic prune→rank triage against a
flat fault registry, enriches the winner from a passive Knowledge Graph, computes
UI analytics, and emits one `OrchestratorFinalUIOutput`. It **never mutates** any
input (sanitisation produces a derived working dict; the Pydantic inputs are held
by reference and never re-typed — see `lab_pipeline_aggregator.process`), and it
**never re-derives** what a producer already computed (it consumes `lambda_chem`,
`total_trim_correction_delta`, `routing_tags`, `ve_pct`, etc., it does not
recompute them).

**Consequences.**
- Positive: one auditable boundary; the producers stay independently testable and
  COMLab's job is small and deterministic.
- Positive: read-only over inputs makes sessions reproducible and side-effect-free
  (no persistent state — see DLD §2.3).
- Negative: COMLab's verdict quality is bounded by producer quality; a producer
  bug surfaces here, so the cross-lab contract and anti-orphan checks matter.
- Neutral: COMLab adds exactly one synthetic signal of its own — the `POA_HISTORY`
  routing tag injected from `chemical_state == POA_SIGNATURE` — and nothing else.

**Alternatives considered.**
1. *Thick orchestrator that re-validates producer math.* Rejected — duplicates
   domain logic across labs, couples release cycles, and reproduces the bugs it
   means to catch.
2. *Multiple fusion points (per-pair fusers).* Rejected — disperses the single
   "one verdict" responsibility and makes the final answer non-deterministic.

**References.** `wiki/01_role_boundaries_fusion_spine.md`; `COMLab_HLD.md` §1, §3;
`comlab/core/lab_pipeline_aggregator.py`; `README.md` (lab role).
