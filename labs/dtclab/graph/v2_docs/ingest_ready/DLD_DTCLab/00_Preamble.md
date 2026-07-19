
> **Context:** DTCLab DLD v2.0 (2026-06-11) · Module: DTCLab · Section: Preamble · Parent document: DLD_DTCLab.md · HLD Reference: HLD_DTCLab v2.0
# DLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**HLD Reference:** HLD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

> **v2.0 reconciliation note.** Reconciled to the shipped `dtclab/` package. Material
> changes from v1.0: `DTCRoutingTag` is **18** members (drop `SAI_HISTORY`; add
> `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE`); `DtcEmissionsView` has **3**
> fields; **5** DNA-gated YAML entries; new package-root modules `family_map.py` and
> `ranking.py` documented (§15–§16).

---


## Graph relations (explicit)

**DLD_DTCLab.md** DESCRIBES **DTCLab DLD v2.0**
**DTCLab DLD v2.0** MIRRORS_CONTRACT_IN **HLD_DTCLab v2.0**
