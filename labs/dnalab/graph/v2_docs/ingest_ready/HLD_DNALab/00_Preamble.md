> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Preamble · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

# HLD — DNALab (v2)
**Status:** Current (reflects shipped code)
**PRD Baseline:** PRD_DNALab v2.0
**Version:** 2.1
**Date:** 2026-06-12

> **Audit note (2026-06-11; refreshed 2026-06-12):** grounded in the live `dnalab/`
> package. DNALab is the umbrella composer of the DNA family; its design is deliberately
> thin. The schema bump is landed: `SCHEMA_VERSION = "1.2"` (T-DNA-7 → 1.1, T-DNA-10 →
> 1.2), `load_state` flows through `build_vehicle_dna`, and the upstream fields round-trip.

---

## Graph relations (explicit)

**HLD_DNALab v2.1** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.3**
**HLD_DNALab v2.1** DESCRIBES **dnalab package architecture** (DNALab umbrella composer)
**HLD_DNALab v2.1** SUPERSEDES any prior DNALab HLD (first v2 HLD)
