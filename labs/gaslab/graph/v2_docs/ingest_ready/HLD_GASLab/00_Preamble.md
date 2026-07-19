# HLD — GASLab
**Status:** Approved
**PRD Baseline:** PRD_GASLab v2.1
**Version:** 2.1
**Date:** 2026-06-10
**Change note:** Refreshed to the live code surface — contract widened 32 → **34** `ChemicalSignature` values (`WRONG_VALVE_TIMING` retired; `CAM_TIMING_RETARDED_MAP` / `CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED` added, per the v2.1 timing-taxonomy revision); GASLab now accepts an **optional second (high-idle / 2500 RPM) reading** plus `fuel_trim` for RPM-differential separation; `GasLabDnaView` slimmed to **13 fields** (`target_lambda_v112` single-value window replaces the old low/high pair; `co_high_idle` added; `secondary_air_equipped` removed).

---


> **Context:** GASLab HLD v2.1 (2026-06-10) · Module: GASLab · Section: HLD_GASLab — Preamble · Parent document: HLD_GASLab.md

## Graph relations (explicit)

**HLD_GASLab — Preamble** DESCRIBES **GASLab HLD v2.1**

