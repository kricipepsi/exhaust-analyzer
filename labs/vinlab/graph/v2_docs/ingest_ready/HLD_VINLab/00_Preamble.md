> **Context:** VINLab HLD v2.0 (2026-06-12) | Module: VINLab | Section: Preamble | Parent document: HLD_VINLab.md / PRD_VINLab v2.1 / SEMANTIC_CONTRACT section 4.1

# HLD — VINLab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_VINLab v2.0
**Version:** 2.1
**Date:** 2026-06-12

> **Audit note (2026-06-11; refreshed 2026-06-12):** this document is grounded in the
> live `vinlab/` package after the sibling split (T-RM-2-DNA), the enum-field cut-over
> (T-FX-5), the air-metering single-module rework (T-FX-2), and the cylinder-heuristic
> fallback (T-VL-7). Every field, enum, threshold, and code path below is transcribed
> from the shipped source, not from design intent. The DNA-pack data-flow tasks
> (T-DNA-3 `rated_rpm`, T-DNA-4 CoC/emissions, T-DNA-5 `model`, T-DNA-6 `fuel_type`) have
> landed; their dispositions are recorded in §9.

---

## Graph relations (explicit)

**HLD_VINLab.md** DESCRIBES **VINLab HLD v2.0 (2026-06-12)**
**VINLab HLD v2.0 (2026-06-12)** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT section 4.1**
