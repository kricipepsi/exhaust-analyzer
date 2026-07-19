# T-GV2-7 — POA / oil-mechanical leaf routing (idle→2500 HC-direction)

### Goal ###

Resolve the `POA_SIGNATURE` **catch-all** (and co-surviving `mechanical_wear`
candidates) to a **specific leaf** — `WORN_VALVE_SEALS`, `WORN_PISTON_RINGS`,
`WORN_ENGINE`, or *stay* `POA_SIGNATURE` — using the idle→2500 **HC change
direction** + load-state CO + λ, per the wiki's single RPM-differential
discriminator (06A §6A.1, `CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR`).

### Premise (verified — read before authoring/altering) ###

- Mechanical-wear candidates (`POA_SIGNATURE`, `WORN_*`) are produced by
  **box-table matching** in `rule_engine._matching_fault_candidates` from the
  ontology `faults` signatures, then refined in
  `resolution.apply_differentiators` — the **same region** 6a/6b/6c use. This
  task's routing belongs in `apply_differentiators`, after the existing timing /
  misfire / lean blocks. **No candidate-generation change.**
- `POA_SIGNATURE` is `CATCH_ALL` (ranked last by `_candidate_rank`); `WORN_*` are
  `mechanical_wear` (`family_map.py:44-51`). All four enum values already exist —
  **no enum change.**
- `COOLANT_LEAK_INTERNAL` (false-lean head-gasket case) is **grammar-gated** in
  `rule_engine._definitive_match` (block-test, 06B) — **out of scope here**;
  reference only.
- The discriminator needs the high-idle reading; `reading_high` is already
  threaded into `apply_differentiators` (used by 6a). **No new input.**

### Steps ###

1. In `apply_differentiators`, after the lean co-survival block and **only when
   `reading_high is not None`**, add a `mechanical_wear` leaf router that fires
   when `POA_SIGNATURE` (and/or a co-surviving `WORN_*`) is present. Route by the
   06A §6A.1 table — HC@idle band, HC direction idle→2500, CO@2500, λ — each
   literal cited `# wiki: docs/GASLab/wikiNEW/06a_fault_atlas_oil_mechanical.md
   §CONCEPT_RPM_DIFFERENTIAL_DISCRIMINATOR` (or the named `FAULT_*` entry):

   | Route to | HC @ idle | HC @ 2500 | direction | CO @ 2500 | λ |
   |---|---|---|---|---|---|
   | `WORN_VALVE_SEALS` | 300–500 (rich offset) | ≤ 35 | **↓ sharp** | low | 0.96 → ~1.0 |
   | `WORN_PISTON_RINGS` | 100–150 | > 300 | **↑ stays elevated** | > 0.5 % | → < 0.99 |
   | `WORN_ENGINE` | 150–300 | ~ unchanged | **flat (no cleanup)** | slight ↑ | 1.0–1.03 |
   | *stay* `POA_SIGNATURE` | > 500 | > 500 (persists) | **flat, high** | variable | λ mismatch |

   Precedence is the wiki's: sharp HC drop ⇒ valve seals; HC rising/elevated with
   CO > 0.5 % under load ⇒ rings; moderate flat HC, no cleanup, no λ mismatch ⇒
   worn engine; HC > 500 persisting both states with λ mismatch ⇒ leave on POA.
   Reuse `lambda_chem`; **invent no number** — if the wiki gives a band not a
   delta, pin it in scope confirmation, do not synthesise a magnitude.
2. Tests in `GASLab/tests/test_rule_engine.py`.

### Success criteria ###

- `test_poa_routes_to_worn_valve_seals_on_sharp_hc_dropoff`.
- `test_poa_routes_to_worn_piston_rings_on_rising_hc_loaded_co`.
- `test_poa_routes_to_worn_engine_on_flat_hc_no_cleanup`.
- `test_poa_stays_on_severe_persistent_hc_lambda_mismatch`.
- `test_mechanical_single_candidate_unchanged` — one wear candidate, no
  `reading_high`, behaviour unchanged (no regression).
- All existing GASLab tests (185+) pass; inner loop clean on each edited file
  (`ruff` → `pyright` → `pytest -x -q`).

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

`mechanical_wear`-family `ChemicalSignature` routing → COMLab `chemical_state`
/ fault-atlas routing (GASWIKI-06A). **No new field, no new enum.** Unblocks
**T-GV2-9** (induction-type turbo-seal POA sub-mode) and **T-GV2-14**
(bank-asymmetry), which share this POA block.

### Harness compatibility ###

No schema-surface change ⇒ descriptor / box table untouched; no fixture
invalidation. The discriminator is RPM-differential (two-point) — validated by
gaslab pytest now and by the dual-RPM oracle (harness **T-TH-14**) later.

### Scope boundaries (explicit — surfaced for owner) ###

- **`cylinder_count` masking math is NOT in this task.** The old ledger one-liner
  bundled "implements `cylinder_count` misfire math," but `cylinder_count`
  (`dna_view.py:29`) is a **misfire-family** concern (the masking-rule cylinder
  inference, 05A) — a *different family* from POA/oil-mechanical, and folding it
  in would breach one-task-≤50% and mix two families. It is **carved out** to a
  separate task (see ledger follow-up FU-CYL). `cylinder_count` is currently an
  **orphan** (read in 0 live paths) — flag, not fix, here.
- **`GDI_INTAKE_VALVE_CARBON` (06A) is out of scope.** It is a GDI-gated
  *normalise* case (lean-look idle that clears at 2500), which shares the
  normalise/persist axis already handled for lean/cam — author separately to
  avoid overlap churn. Reference only.
- `COOLANT_LEAK_INTERNAL` false-lean routing (06B, grammar-gated); turbo-seal
  sub-mode (needs `induction_type`, T-GV2-9). No `ranking.py` change.
