# T-TH-14 — Dual-RPM / delta FaultBox extension to the descriptor

### Goal ###

Extend the harness `FaultBox` + GASLab descriptor builder so an RPM-differential
family can be expressed as a **two-point signature** — an idle box, a 2500-RPM
box, and a per-gas/λ **delta direction** (normalise / persist / rise / fall) —
plus a `dual_rpm_oracle()` that scores a (idle, high) reading pair against it.
This is the prerequisite that lets the harness model the families GASLab v2
T-GV2-6a/6b/6c separate; today the single-point box cannot express them.

### Why (the structural gap) ###

`FaultBox.dimensions` is one idle vector. The v2 contract's discriminating power
for cam_timing (and later oil/mechanical, EGR, catalyst) is the **idle→2500
delta** (`GAS_WIKI §8.9` TEST_RPM_SEPARATION_MATRIX). With one vector the timing
boxes overlap almost completely — this is the **100 % discrimination ceiling**
T-TH-2 reported and the reason the harness structurally under-models exactly the
families v2 is building. The wiki already gives both vectors (06b
`§FAULT_CAM_TIMING_*` idle + 2500 gas_vectors), so the boxes are pinnable now.

### Scope ###

0. **Descriptor dead-field cleanup (absorbed from T-TH-11, 2026-06-05):** remove the
   dead `ctx_secondary_air_injection_active` `FieldRange` from the GASLab descriptor
   builder (`harness/descriptor.py:312`, H-9). Previously scoped in T-TH-11, but
   T-TH-11 is now **blocked behind master-label reconciliation** (`T-MASTER-RECON`);
   this task absorbs the removal so timing-family validation is not stuck behind the
   master-fixture chain. Confirm no test references the field before deletion.
1. **`FaultBox` (backward-compatible):** add
   - `dimensions_high: dict[str, tuple[float, float]] | None = None` — the
     2500-RPM box;
   - `delta_directions: dict[str, str] | None = None` — per-dim direction tag
     drawn from a closed set `{"normalise","persist","rise","fall"}`.
   Single-point families leave both `None` — existing boxes and all of
   T-TH-0/1/2/4 keep working unchanged.
2. **Builder population (timing family only, this task):** fill
   `dimensions_high` + `delta_directions` for `CAM_TIMING_RETARDED_MAP`,
   `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED` from the v2 wiki, replacing
   the current TBD full-envelope placeholders for those three. Cite each box:
   `# wiki: docs/GASLab/wikiNEW/06b_…valvetrain_egr_combustion.md §FAULT_CAM_TIMING_*`
   and `GAS_WIKI §8.9` for the directions. **No invented numbers** — every bound
   comes from the 06b idle/2500 gas_vectors; if a direction is qualitative only,
   tag it from §8.9 prose, do not synthesise a delta magnitude.
3. **`dual_rpm_oracle(box, reading_idle, reading_high) -> bool`** — membership in
   the idle box AND the high box AND consistency with each `delta_direction`.
   Lab-agnostic (lives in the harness core, imports no lab).
4. Tests proving the extension delivers separation the single-point model cannot.

### Success criteria ###

- `test_faultbox_backward_compatible` — a box with `dimensions` only behaves
  exactly as before; `dimensions_high`/`delta_directions` default `None`.
- `test_timing_boxes_have_dual_vectors` — the three CAM_TIMING boxes load with
  both vectors + directions, all cited, all `min ≤ max`.
- `test_dual_rpm_oracle_separates_map_maf_advanced` — three wiki-sourced
  (idle, high) exemplars each match exactly one timing box under
  `dual_rpm_oracle`, where single-point idle-box membership matches ≥ 2 (proves
  the ceiling is broken).
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Named signal/noise consumer ###

The `dual_rpm_oracle` + dual-vector boxes are consumed **in-task** by
`test_dual_rpm_oracle_separates_map_maf_advanced`, and downstream by the
regression fixture (T-TH-10/11) and any re-run of the boundary/overlap
generators against the timing family. The extension ships with that consumer —
not "for later".

### Dependencies / coupling ###

- **Wiki-grounded, so not hard-blocked** on v2 code. Recommended **after
  T-GV2-6a** so the family semantics the oracle encodes are confirmed against the
  landed rule.
- **Decoupled from T-TH-11 (2026-06-05).** T-TH-11 is now blocked behind
  master-label reconciliation (`T-MASTER-RECON`, see harness ledger H-10), so the
  old "run T-TH-11 first" serialisation no longer applies. The
  `ctx_secondary_air_injection_active` removal is **absorbed into this task**
  (Scope step 0). T-TH-14 is therefore the **next runnable harness task** — its
  only prerequisite is the descriptor cleanup it now owns.

### Out of scope ###

- Re-running or modifying the T-TH-1 boundary / T-TH-2 overlap generator modules
  (separate post-v2 re-run tasks). High boxes for non-timing families (oil/
  mechanical arrives with T-GV2-7; EGR/catalyst later). The master fixture
  (T-TH-10) and the master wired gate (T-TH-12). No new lab import in the core.
