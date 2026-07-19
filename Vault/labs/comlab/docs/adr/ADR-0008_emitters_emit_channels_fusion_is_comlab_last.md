# ADR-0008: Emitter labs emit channels, not verdicts; fault fusion is COMLab, built last

**Status:** Accepted

**Context.** Many faults need evidence from more than one lab — an `ecu_fault`
needs GAS truth + OBD perception delta; a bank-asymmetry verdict needs per-bank
OBD trims; a no-start discrimination needs DTC Mode-$06 plus freeze-frame. If each
emitter tried to reach a cross-lab verdict, it would need data it does not own and
the labs would couple.

**Decision.** Each emitter lab emits its **own channel/signal** against the frozen
contract and stops there; the **cross-lab fault verdict is COMLab's**, and COMLab
is built **last** (Stage 4) so the emitters and research gates are settled first.
This is operationalised by `CROSS_LAB_DEPENDENCIES.md`: each capability is split
into independent **emitter halves** (land in their lab's stage) plus one
**fusion/consumer half** in COMLab (DEP-1…DEP-10). COMLab's fusion consumers are
**additive and individually gated** by `enable_*` flags on
`fault_atlas_router.execute_triage_loop` (`enable_ecu_fuse`, `enable_bank_fuse`,
`enable_ve_gate`, `enable_fuelsys_gate`, `enable_ecu_hw`, `enable_o2_offset`,
`enable_nostart`, `enable_misfire_loc`, `enable_maf_lin`, `enable_ltft_cell`, …),
so each pair lands without destabilising the others.

**Consequences.**
- Positive: emitters stay simple, single-purpose, and testable against the frozen
  contract; the hard fusion logic lives in one place.
- Positive: the forward registry makes every cross-lab obligation visible and
  un-loseable; the anti-orphan gate (ADR-0003) proves each emitted field is read.
- Negative: a capability is only complete when both halves ship — partial work is
  the norm mid-stage and must be tracked, not assumed done.
- Neutral: COMLab being last means its ADRs formalise decisions the emitters made
  earlier (e.g. ground-truth chemistry, ADR-0007).

**Alternatives considered.**
1. *Let emitters emit cross-lab verdicts.* Rejected — needs data they don't own and
   couples the labs.
2. *A always-on monolithic fusion pass.* Rejected — one failing consumer would
   destabilise all verdicts; the per-evidence `enable_*` gating isolates risk.

**References.** `CROSS_LAB_DEPENDENCIES.md` (DEP registry + stage gates);
`comlab/core/fault_atlas_router.py` (`enable_*` flags, Phase 5);
project `CLAUDE.md` ("emitter labs emit channels, not verdicts").
