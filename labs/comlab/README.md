# labs/comlab — COMLab v2 + registry (Stage 4, LAST)

**Role:** the prune→rank **decision spine** that consumes every upstream channel; houses analytics +
fault-atlas routing. The registry is reconciled **alongside** COMLab here.
**Build stage:** 4 — reworked **last**, so the emitters and research gates are settled first.
**Architecture decision (deferred to stage start):** additive hand-tuned ranker vs learned/Bayesian
fusion; consolidate the two split registries; consider top-2/3 differential output.
**Code origin (Q-A / D1):** fork of v1 `COMLab/` (+ `registry/`); v1 archived once built and green.
**Boundary:** COMLab **mirrors** each lab's types locally — no cross-lab Python imports.

**Lands here at Stage 4:** the deferred consumer reconciliations — `T-GV2-2` (ChemicalSignature mirror),
`FU-1` (registry `schema_v2` 32→34 + `cam_timing.json`), `FU-4` (wired/projection reconcile), D2 repoint.

_Status: built + green (Stage 4 closed 2026-06-25). Tested and verified._
