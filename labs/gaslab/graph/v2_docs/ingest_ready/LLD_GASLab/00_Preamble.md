# LLD — GASLab
**Status:** Approved
**PRD Baseline:** PRD_GASLab v2.1
**HLD / DLD Reference:** HLD_GASLab v2.1 / DLD_GASLab v2.1
**Version:** 2.1
**Date:** 2026-06-10
**Change note:** Refreshed to the live engine — cam-timing rule (renamed from the retired WVT rule) and its high-idle confirmation vectors, `fuel_trim` leak routing, masking cylinder-count inference, Euro-class CO/HC scaling, wideband O₂-bias calibration, and the single-value `target_lambda_v112` CoC window.

Convention: every numeric literal in `gaslab/` carries a `# wiki:` or `# vocab:` comment citing `GAS_WIKI` / `GAS_VOCABULARY`. The literals below are transcribed from source.

---


> **Context:** GASLab LLD v2.1 (2026-06-10) · Module: GASLab · Section: LLD_GASLab — Preamble · Parent document: LLD_GASLab.md

## Graph relations (explicit)

**LLD_GASLab — Preamble** DESCRIBES **GASLab LLD v2.1**

