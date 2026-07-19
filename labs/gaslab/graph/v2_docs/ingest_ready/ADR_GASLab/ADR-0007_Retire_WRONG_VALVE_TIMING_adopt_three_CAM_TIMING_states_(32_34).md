
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0007: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32 → 34) · Parent document: ADR_GASLab.md
## ADR-0007: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32 → 34)

**Status:** Accepted (2026-06-03)

**Context.** The single `WRONG_VALVE_TIMING` value conflated distinct, separately diagnosable cam-timing states. Source research (the 1990–2010 petrol-timings document) describes five first-class timing states: two ignition (retained) and three cam-system-specific.

**Decision.** Retire `WRONG_VALVE_TIMING` and add `CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, and `CAM_TIMING_ADVANCED`, bringing the contract surface to **34** values. These states are marked `SPECIFIC`, not `DEFINITIVE`: the tailpipe cannot prove cam phase alone. The GASLab enum and ontology are revised first; the canonical `OBD_VOCABULARY.md §17` mirror, `SEMANTIC_CONTRACT.md`, and the COMLab schema are updated in a **coordinated cross-lab change**. Until that lands, the GASLab side is intentionally divergent.

**Consequences.**
- Positive: three separately routable cam-timing diagnoses instead of one ambiguous label.
- Positive: aligns the enum with the five-state timing taxonomy applied across labs later.
- Negative: a temporary, deliberate enum divergence between GASLab (34) and the COMLab-side mirror (32) until the breaking change is coordinated — tracked, not silent.
- Negative: a breaking change per the change protocol; consumers must update together.

**Alternatives considered.**
1. *Keep `WRONG_VALVE_TIMING` and sub-type it with a side field.* Rejected — adds a field with no clean consumer and hides three diagnoses behind one label.
2. *Add the three states but keep `WRONG_VALVE_TIMING` as an alias.* Rejected — leaves a dead enum value and stale routing.

**References.** `wiki/CHANGE_v2.1_timing_taxonomy.md`; `GAS_VOCABULARY §3, §21`; ADR-0008.

---


## Graph relations (explicit)

**ADR-0007: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32 → 34)** DESCRIBES **GASLab ADR v2.1**
**CAM_TIMING_RETARDED_MAP, CAM_TIMING_RETARDED_MAF, CAM_TIMING_ADVANCED** SUPERSEDES **WRONG_VALVE_TIMING** -- 32->34, v2.1 timing taxonomy
**ChemicalSignature** MIRRORS_CONTRACT_IN **OBD_VOCABULARY.md §17** -- intentional 32/34 divergence


