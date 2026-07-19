# T-GV2-9 — Induction-Type Signatures Consumer (`induction_type`)

### Goal ###

Wire the orphan DNA field `induction_type` (`GASLab/gaslab/dna_view.py` L33 —
read in **0** code paths today) to its wiki-named consumers (§1.4 L83: "unlocks
forced-induction NOₓ signatures; turbo-seal oil sub-mode"):

1. **Turbo-seal POA sub-mode**, gated on `induction_type == "forced"`: the
   `TURBO_SEAL_OIL_LEAK` presentation — extreme tailpipe HC (~720 ppm),
   **perfectly stoichiometric λ (1.000), CO ≈ 0** (oil cracks in the hot
   exhaust, combustion intact) — routes to `POA_SIGNATURE` (turbo-seal sub-mode)
   **only** when forced-induction.
   (`06a_fault_atlas_oil_mechanical.md` L699 / L1175; `GAS_WIKI §7.23`)
2. **Forced-induction NOₓ** handling where the wiki specifies a forced-induction
   NOₓ shift.

### Steps ###

1. In the POA / oil routing add an `induction_type == "forced"` gate for the
   turbo-seal sub-mode per 06a §6A.1. **Do not duplicate** the non-forced oil
   routing (T-GV2-7's `WORN_VALVE_SEALS` / `WORN_PISTON_RINGS` / `WORN_ENGINE`
   HC-direction logic). Each literal carries a `# wiki:
   docs/GASLab/wikiNEW/06a…` citation.
2. Tests per criteria.

### Success criteria ###

- `test_turbo_seal_submode_gated_on_forced` — extreme HC + stoich λ + ~0 CO with
  `induction_type="forced"` → `POA_SIGNATURE` (turbo-seal); the **same gases**
  with `naturally_aspirated` → not turbo-seal.
- All existing GASLab tests pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

`induction_type` → turbo-seal POA sub-mode gate (+ forced-induction NOₓ) →
`POA_SIGNATURE` routing / fault-atlas (GASWIKI-06A §7.23). **Anti-orphan gate:**
`grep induction_type` must show a live read in `resolution.py` after this task.

### Out of scope ###

- Non-forced oil/mechanical HC-direction routing and `cylinder_count` misfire
  math (both T-GV2-7).
- Candidate new enum values (`HEAD_GASKET_OIL_BREACH`, `TURBO_SEAL_OIL_LEAK`)
  stay deferred to `CONCEPT_PROPOSED_ENUM_ADDITIONS` — route to the existing
  `POA_SIGNATURE`. No new field/enum.

### Sequencing note (architect) ###

This task and **T-GV2-7 share the POA routing block**. To avoid a merge churn,
T-GV2-9 is **Blocked by T-GV2-7** (run the non-forced oil routing first, then add
the forced gate on top). The forced-induction NOₓ part alone does not depend on
T-GV2-7, but the shared file makes serialising the safer choice.
