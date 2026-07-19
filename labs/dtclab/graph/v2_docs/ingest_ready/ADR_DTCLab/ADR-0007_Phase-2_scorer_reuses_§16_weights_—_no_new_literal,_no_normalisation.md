
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0007: Phase-2 scorer reuses §16 weights — no new literal, no normalisation · Parent document: ADR_DTCLab.md
## ADR-0007: Phase-2 scorer reuses §16 weights — no new literal, no normalisation

**Status:** Accepted

**Context.** COMLab's Bayesian fusion (`combine()`, FU-1) wants ranked `(fault_family, confidence)`
candidates, not raw tags. DTCLab is the natural place to rank DTC evidence, but must not invent a
parallel scoring scheme or pre-empt COMLab's normalisation.

**Decision.** `ranking.py` computes per-family confidence purely from the existing
`DTC_CONFIDENCE_WEIGHTS` (§16) and the §14.2 DNA factors (1.0/0.7/0.5). `rank_candidates` takes the
max contributing weight per family and tags evidence strength via `MatchType`. `classify_top3`
clamps to the unit interval, dedups, and returns the top 3 — with **no sum-1 normalisation** and
**no `LabResult` construction** (those belong to COMLab `combine()` and the Wired adapter `T-DTW-1`).

**Consequences.**
- (+) Single source of truth for weights; no drift between the payload weights and the scorer.
- (+) Clear ownership: DTCLab ranks, COMLab fuses/normalises, Wired adapts.
- (−) The scorer's consumer is the Wired adapter, which must exist for the surface to be live —
  acceptable, it is a named, specced consumer (`T-DTW-1`), not "future use".

**Alternatives considered.** (1) Normalising to sum-1 in DTCLab — rejected: double-normalisation
corrupts the Bayesian fusion. (2) Introducing family/tier confidence ceilings — rejected: adds
unsourced numeric literals (DESIGN §6 forbids it).

---


## Graph relations (explicit)

**ADR-0007** DESCRIBES **DTCLab ADR v1.0**
**ranking.rank_candidates** IMPLEMENTS **ADR-0007** -- no new literal, no normalisation
**test_classify_top3.py** VERIFIES **ADR-0007**
