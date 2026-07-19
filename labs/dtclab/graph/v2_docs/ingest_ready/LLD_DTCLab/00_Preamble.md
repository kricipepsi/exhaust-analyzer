
> **Context:** DTCLab LLD v2.0 (2026-06-11) · Module: DTCLab · Section: Preamble · Parent document: LLD_DTCLab.md · HLD / DLD Reference: HLD_DTCLab v2.0 / DLD_DTCLab v2.0
# LLD — DTCLab
**Status:** Approved
**PRD Baseline:** PRD_DTCLab v2.0
**HLD / DLD Reference:** HLD_DTCLab v2.0 / DLD_DTCLab v2.0
**Version:** 2.0
**Date:** 2026-06-11

Convention: every numeric literal carries a `# wiki: <source> §<section>` comment in code.

> **v2.0 reconciliation note.** Reconciled to shipped `dtclab/`. Material changes from v1.0:
> the DNA gate dispatch is `_check_high_confidence_gate` with three named gates (no
> `secondary_air_equipped`, §7); `RoutingTagMapper.map` returns enum-definition order via a
> comprehension (§8); the Phase-2 scorer boundaries are added (§16).

---


## Graph relations (explicit)

**LLD_DTCLab.md** DESCRIBES **DTCLab LLD v2.0**
**DTCLab LLD v2.0** MIRRORS_CONTRACT_IN **DLD_DTCLab v2.0**
