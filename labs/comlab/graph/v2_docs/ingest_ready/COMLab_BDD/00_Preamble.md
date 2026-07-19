
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Preamble · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
# BDD — COMLab

**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-21
**Authored from:** `_skills/doc/BDD.md` (Gherkin Given/When/Then, declarative, one behaviour per scenario)
**Code baseline:** COMLab v2 as-built (`labs/comlab/comlab/`)

These are **executable specifications** for COMLab's observable behaviour at its
two public boundaries: `core/lab_pipeline_aggregator.LabPipelineAggregator.process()`
(the full pipeline) and `core/fault_atlas_router.FaultAtlasRouter.route()` (Stage
B→E). Each scenario is declarative — it states what the fusion spine does for a
given inbound request, never how. Every feature names the test module(s) that
exercise it, so the scenarios stay honest against `pytest`. Numeric values are
illustrative of the documented bands (see LLD / ADRs); they are not new thresholds.

**Scope reminder (ADR-0004):** petrol 1990–2010, Euro 1–5. Post-2010 Euro 6+
technology (SAI, GPF/DPF, LSPI) is out of scope — there are no scenarios for it
because there are no fields for it.

A shared vocabulary used throughout:

- **A request** = one `OrchestratorInboundRequest` (vehicle DNA + gas/OBD/DTC
  payloads + symptom DNA).
- **The verdict** = the `diagnostic_verdict` block of `OrchestratorFinalUIOutput`
  (fault id/name/family, confidence, remediation, siblings).
- **The directive** = the `LabRoutingDirective` from `symptom_router.route_symptom`.
- **A horizon** = `HORIZON_LEGACY` / `HORIZON_ADAPTIVE` / `HORIZON_MODERN`,
  pre-resolved by DNALab.

---


## Graph relations (explicit)

**COMLab_BDD.md** DESCRIBES **COMLab BDD v1.0**
**COMLab BDD v1.0** MIRRORS_CONTRACT_IN **COMLab HLD v2.0**
