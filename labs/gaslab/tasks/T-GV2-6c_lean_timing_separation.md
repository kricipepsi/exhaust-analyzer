# T-GV2-6c — Lean-condition vs timing separation (idle→2500 persist/normalise)

### Goal ###

Separate a genuine `LEAN_MIXTURE` (vacuum/fuel lean that **normalises** toward
2500 RPM) from a timing case that merely *looks* lean at idle
(`CAM_TIMING_RETARDED_MAF`, which **persists** lean across the RPM band), inside
the `lean_condition` family, using the idle→2500 differential.

### Premise (verified — read before authoring/altering) ###

- A LEAN_MIXTURE normalise check **already exists** at
  `GASLab/gaslab/resolution.py:247-251`: it prunes `LEAN_MIXTURE` from survivors
  unless `reading_high.o2 < 1.0` and `0.985 ≤ λ(reading_high) ≤ 1.015`
  (normalises). **Do not duplicate it.**
- T-GV2-6a retains `CAM_TIMING_RETARDED_MAF` only when it is lean at idle **and
  persists** at 2500. So the two halves of the discriminator already live in 6a
  (persist ⇒ keep timing) and L247 (normalise ⇒ keep lean).
- The **residual** unresolved case is **co-survival**: both `LEAN_MIXTURE` and
  `CAM_TIMING_RETARDED_MAF` (and/or `HIGH_COMBUSTION_TEMP` / `EGR_STUCK_CLOSED`,
  which also map to `lean_condition`) survive together. That mutual-exclusion is
  this task's only scope.

### Steps ###

1. In `apply_differentiators`, after 6a and the L247 LEAN check: if both a
   persisting-lean timing candidate and `LEAN_MIXTURE` survive, enforce
   mutual exclusion by the **normalise-vs-persist direction** already computed —
   normalising ⇒ keep `LEAN_MIXTURE`, drop timing; persisting ⇒ keep timing,
   drop `LEAN_MIXTURE`. Reuse the existing λ/O₂ normalise predicate; do not add a
   second threshold set.
   - Any literal reused carries its existing citation
     (`# wiki: docs/GASLab/wikiNEW/GAS_WIKI.md §8.9`,
     `06b §FAULT_CAM_TIMING_RETARDED_MAF`). No new literal unless the wiki gives
     one; if it gives a range not a delta, pin it in scope confirmation.
2. Tests in `GASLab/tests/test_rule_engine.py`.

### Success criteria ###

- `test_normalising_lean_keeps_lean_mixture_drops_timing`.
- `test_persisting_lean_keeps_timing_drops_lean_mixture`.
- `test_lean_family_no_cosurvival_unchanged` — when only one lean candidate is
  present, behaviour is unchanged (no regression).
- All existing GASLab tests (173+) pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

`lean_condition`-family `ChemicalSignature` routing → COMLab `chemical_state`
(GASWIKI-08 / 06b). **No new field, no new enum.**

### Harness compatibility ###

- **No schema-surface change** ⇒ harness descriptor / box table untouched; no
  fixture invalidation.
- Discriminator is **RPM-differential** (two-point), which the single-point box
  oracle cannot model — validated by gaslab pytest now and the **dual-RPM
  descriptor extension** + regression fixture later (harness pack). Lands cleanly
  alongside 6b: both edit the same `apply_differentiators` region, so they
  **serialise** (6c blocked-by 6a; run after 6b to avoid two sessions editing the
  same block).

### Out of scope ###

- 6a's timing-retention and the existing L247 LEAN check (reuse, do not rewrite).
- misfire precedence (6b), mechanical_wear (T-GV2-7), EGR chemistry (owned
  elsewhere). No new DNA field, no enum change, no `ranking.py` change.
