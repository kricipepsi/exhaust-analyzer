# T-GV2-6a — Cam/Ignition Timing RPM-Differential Separation

### Goal ###

Separate the five timing states from each other using the **idle→2500 RPM
differential**, replacing the current single-point 2500-RPM range checks for the
`CAM_TIMING_*` family with the wiki's normalisation-direction discriminators, and
adding the ignition-timing-vs-cam-timing distinction.

Today `apply_differentiators` (`GASLab/gaslab/resolution.py` ~L254-289) prunes
`CAM_TIMING_RETARDED_MAP` / `_MAF` / `CAM_TIMING_ADVANCED` using only
`reading_high` **single-point** bounds; it never compares idle vs 2500. The wiki
defines the real discriminator as the idle→2500 *behaviour*
(`TEST_RPM_SEPARATION_MATRIX`, GASWIKI-08 / `GAS_WIKI §4` L207):

- **`CAM_TIMING_RETARDED_MAP`** (Speed-Density over-fuel): rich at idle
  (λ 0.85-0.95), **partially normalises toward 2500** (λ moves toward 1.0, CO
  falls) as vacuum recovers; a sensor/fuelling rich-bias stays flat.
  (`06b_…valvetrain_egr_combustion.md` §FAULT_CAM_TIMING_RETARDED_MAP, L737)
- **`CAM_TIMING_RETARDED_MAF`**: lean-direction at idle (λ 1.03-1.09),
  **persists** at 2500 (no normalisation). (proposal L66-72; 06b)
- **`CAM_TIMING_ADVANCED`**: mild-lean rough idle, no SD/MAF inversion; at 2500
  **HC/CO fall and NOₓ rises**. (06b §FAULT_CAM_TIMING_ADVANCED, L749)
- **`TIMING_OVER_ADVANCED`** (ignition): **clean idle + NOₓ-only high-idle
  spike** — NOT the rough-idle + idle-λ-offset of the cam family.
  (`05_fault_atlas_part_a.md` / 06b §FAULT_TIMING_OVER_ADVANCED, L594)
- **`TIMING_RETARDED`** (ignition): retained ignition state — high HC / low NOₓ,
  distinct from the cam family.

### Steps ###

1. In `apply_differentiators` add idle→2500 delta checks (use **both** `reading`
   and `reading_high`) for the timing block:
   - MAP retained only if rich idle **and** partial normalisation toward 2500
     (λ rises toward 1.0; CO falls); reject if flat.
   - MAF retained only if lean idle **and** persists at 2500 (no normalisation).
   - ADVANCED retained only if NOₓ rises idle→2500 **and** HC/CO fall.
   - Separate ignition `TIMING_OVER_ADVANCED` (clean idle + NOₓ-only 2500 spike)
     from cam `CAM_TIMING_ADVANCED` (rough idle + idle λ-offset).
   - Every numeric literal carries a `# wiki: docs/GASLab/wikiNEW/06b…` (or §4)
     citation.
2. Tests in `GASLab/tests/test_rule_engine.py` per success criteria.

### Success criteria ###

- `test_cam_map_partial_normalisation_retained` and
  `test_cam_map_flat_rich_rejected`.
- `test_cam_maf_persists_lean_retained` and `test_cam_maf_normalising_rejected`.
- `test_cam_advanced_nox_rise_retained`.
- `test_ignition_over_advanced_clean_idle_not_cam`.
- All existing GASLab tests (173+) pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)
- `GASLab/tests/test_resolution.py` (MODIFY — **only if** the CHI-1 CAM_MAP
  fixtures live there; architect-authorised 2026-06-05) — task-forced fixture
  touch: update the **idle vector** of the breaking CHI-1 CAM_MAP cases to the
  06b rich-idle vector (HC 400–1200, CO 3.5–7.0, O₂ < 0.5, λ 0.75–0.88) so the
  new idle-side gate is satisfied. **Constraint:** the edit changes the idle
  vector only and must preserve CHI-1's actual assertion — the `co_high_idle`
  override of the high-idle rich-CO lower bound. If keeping CHI-1 green requires
  weakening the idle gate, STOP — that is a real conflict, not a fixture fix.

### Signal/noise consumer ###

The five timing `ChemicalSignature` values (already in the enum since T-GV2-1)
route to COMLab `chemical_state` / fault-atlas (GASWIKI-06B). **No new field or
enum value**; MAP/MAF stays `dna_gate: none` (there is no MAF/MAP DNA field — the
RPM differential *is* the discriminator). `reading_high` is already plumbed
(T-GV2-4). No orphan introduced.

### Out of scope ###

- mechanical_wear/oil routing (T-GV2-7); catalyst (T-GV2-5, done); sensor-bias
  calibration (T-GV2-10); misfire precedence (T-GV2-6b); lean/ecu
  (T-GV2-6c/6d).
- No new DNA field, no enum change, no `ranking.py` priority change (priority is
  6b's job).
- The δ for "partial normalisation": if 06b/§4 give **ranges, not deltas**, the
  coder pins exact bounds from the wiki in scope confirmation — **do not invent
  a delta**.
