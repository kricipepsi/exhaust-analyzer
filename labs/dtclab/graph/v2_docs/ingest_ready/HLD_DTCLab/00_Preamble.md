
> **Context:** DTCLab HLD v2.0 (2026-06-11) · Module: DTCLab · Section: Preamble · Parent document: HLD_DTCLab.md · PRD Baseline: PRD_DTCLab v2.0
# HLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

> **v2.0 reconciliation note.** This revision reconciles the HLD to the shipped
> `dtclab/` package (AST ground truth, June 2026). Changes from v1.0: the routing
> surface is **18** `DTCRoutingTag` values (not 17 — `SAI_HISTORY` was never shipped;
> `COOLANT_SYSTEM_MALFUNCTION` and `CYLINDER_FLUID_MISFIRE` are added); `DtcEmissionsView`
> carries **3** flags (no `secondary_air_equipped`); the routing map has **5** DNA-gated
> entries (not 6); and the **Phase-2 scorer** (`ranking.py`) and **family map**
> (`family_map.py`) are now documented.

---


## Graph relations (explicit)

**HLD_DTCLab.md** DESCRIBES **DTCLab HLD v2.0**
**DTCLab HLD v2.0** MIRRORS_CONTRACT_IN **PRD_DTCLab v2.0**
