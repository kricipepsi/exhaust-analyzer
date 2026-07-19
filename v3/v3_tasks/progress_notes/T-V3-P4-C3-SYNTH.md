# T-V3-P4-C3-SYNTH — progress note

**Task:** seed provisional synthetic C3 (ECU/control-system fault) data for the 22 C3
cases — research-grounded, web-corroborated, tolerance-wide, grounding-tagged,
`synthetic=true`, side file only.
**Date:** 2026-07-05 · **Coder:** Claude Code · **Mode:** STRICT (dual-gate)
**Skills loaded:** wired-python, wired-verification-loop, wired-code-review, wired-signal-pack.
**Governs / governed by:** [[T-V3-P4-C3-PRE]] (reveal contract) → this seed → [[T-V3-P4-C3A]]
(dry-run) → C3B (commit).

## What shipped (all new, under `v3/` only)
- `v3/gen_c3_synth_seed.py` — deterministic generator. Reads **one** live file read-only
  (`apps/wired/v7/data/cases_petrol_v7.csv`) for each case's oracle `expected_fault_code`.
  Samples the six C3 control-plausibility columns from the web-validated band table keyed on
  that **oracle code**. PRNG seeded from SHA-256 of `case_id` (no wall-clock / unseeded
  randomness). All writes under `v3/`.
- `v3/data/c3_synthetic_seed_2026-07-05.csv` — 22 cases × 6 C3 columns, `synthetic=true`.
- `v3/data/c3_synthetic_seed_2026-07-05.json` — manifest: per-case values, band_id,
  oracle_fault_code + fault_name, grounding tags, citations, no-back-solve note, research
  limits.
- `v3/reports/V3_C3_SYNTH_BANDS_2026-07-05.md` — per-column research-vs-web-vs-band-used
  table, 6 citations, σ tolerance table, per-case table, separability split.

## Key modelling decision (surfaced, not hidden)
All 22 C3 cases share `expected_fault_family = ecu_fault`, so the family is NOT a usable band
discriminator. The generator keys on the finer **`expected_fault_code`** — the corpus **answer
key** — resolved to a registry `fault_name` (`global_fault_registry.json`, read once for the
label only). This is oracle ground truth, not a consumer threshold → no back-solve. Five
sub-fault codes map to bands:

| oracle code | fault_name | band | separable? | discriminating gate |
|---|---|---|---|---|
| ERR-EF-006 (×8) | ecu_fault_lean_bias | C3-LEAN-BIAS | yes | ground drop > 0.20 V + Δλ ≥ 0.05 |
| ERR-EF-007 (×3) | ecu_fault_rich_bias | C3-RICH-BIAS | yes | KOEO \|MAP−BARO\| ≥ 5 kPa + Δλ ≥ 0.05 |
| ERR-ECU-001 (×7) | ecu_internal_processor_fault (P0606) | C3-PROCESSOR | yes | bidirectional bool=False (deterministic) + Vmod < 12 V |
| ERR-EF-002 (×3) | ecu_fault_poa_context | C3-POA-CONFOUNDER | **NO** | physical oil-burn → gas+OBD agree, no Δλ |
| ERR-EF-008 (×1) | ecu_fault_intermittent | C3-INTERMITTENT | **NO** | fault not active in one snapshot |

**Separability split: 18 C3-separable + 4 stay-abstained = 22.** ✔ The 4 abstain cases are the
C3-PRE §6 confounders (POA physical-fault mimics + intermittent); seeded honestly BELOW every
producer gate, never into a passing band, flagged `stay_abstained=true`.

## Grounding tags (carried from C3-PRE §7 — not laundered)
- `gas_obd_lambda_delta` / `lambda_perception_delta` — **empirical-anecdotal** (Δλ ≥ 0.05 is a
  practitioner heuristic, not an OEM/SAE constant). Flagged in report + manifest.
- `dlc_signal_ground_drop_v` — **standardized** (0.1/0.2 V DMM voltage-drop convention).
- `koeo_map_baro_delta_kpa`, `module_voltage_loaded_v`, `bidirectional_..._bool` —
  **manufacturer-typical**. The bool is **deterministic per fault** (only P0606 → False), not
  sampled — stated explicitly.

## Web corroboration (6 cited sources, in report + manifest)
- Ground-circuit voltage drop 0.1/0.2 V standard; computer grounds fault > 0.10 V (Fluke, aa1car,
  CARDONE ECM bulletin).
- Ground-offset → ECU perceives rich → negative trim → engine physically lean (vehicleservicepros,
  fordfiesta forum).
- KOEO MAP ≈ BARO ~98–102 kPa; split sets P0069 (aa1car, engineerfix, underhoodservice).
- P0606 = ECM CPU/RAM/ROM self-test fail; engine often runs normal, weak battery < 12.4 V a common
  trigger (obd-codes, fixdapp, skanyx).
- Δλ ≥ 0.05 gas-vs-OBD divergence + bidirectional O2 swing < 0.1 V (cluster3_prepped.md lines 183/188).

Where the web was **stricter** than the research answer (computer grounds fault below 0.10 V vs the
0.20 V signal-ground gate), bands were set to fire the gate robustly while staying field-realistic.

---

## VERIFICATION GATE (wired-verification-loop)

**Phase 1 — Scope confirm:** posted before code; task = seed side file only, no wire/score.
**Phase 2 — Per-file Inner Loop (generator):**
```
.venv-wired/bin/python -m py_compile v3/gen_c3_synth_seed.py   → OK
.venv-wired/bin/python -m ruff check   v3/gen_c3_synth_seed.py → All checks passed!
.venv-wired/bin/python -m pyright      v3/gen_c3_synth_seed.py → 0 errors, 0 warnings, 0 informations
```
**Phase 3 — Task verification block (spec §Verification):**
- `python v3/gen_c3_synth_seed.py` twice → **byte-identical** (sha256 CSV
  `a055c788…`, JSON `4b2491fd…`, MD `95c0fdb9…` unchanged across reruns).
- `_assert_no_backsolve` passes: 22 rows; every separable case fires its designed gate across
  its band; every abstain case clears BELOW every gate; bool deterministic.
- `grep -icE 'synthetic|band|citation|anecdotal|standardized|abstain'` on bands report → **23**.
- Separability reconciles: 18 + 4 = **22**. Oracle-code split
  `{ERR-EF-006:8, ERR-EF-007:3, ERR-ECU-001:7, ERR-EF-002:3, ERR-EF-008:1}` = 22.
**Phase 4 — Scope / no-regression:** `git status --porcelain` shows **only 4 new files under
`v3/`** (`gen_c3_synth_seed.py`, `data/c3_synthetic_seed_2026-07-05.{csv,json}`,
`reports/V3_C3_SYNTH_BANDS_2026-07-05.md`). Live corpus (`cases_petrol_v7.csv`), engine,
registry rules (`ecu_fault.json`/`sensor_fault.json`), scorer (`run_suite.py`), yardstick, and
abstain dial **untouched by this task**. (`fault_atlas_router.py` shows as modified in
`git status` but was already modified at session start — pre-existing, not this task.)
**Phase 5 — Guardrails:** no `Vault/` edit, no `graphify`/frozen-graph rebuild, no secrets, no
`git add`. **Phase 6:** ledger row + this note updated.

**GATE: CLEAN.**

## CODE REVIEW (wired-code-review, incl. structural-craft WARNING axis)

- **No back-solve (correctness of the core invariant):** generator inputs = oracle
  `expected_fault_code` + band table only. Never opens `ecu_fault.json`/`sensor_fault.json` or
  any run/rank file. The research limits in the module are used only to *validate* the seed in
  `_assert_no_backsolve`, and are the producer/research constants from `cluster3_prepped.md`, not
  consumer-rule values. ✔
- **Determinism:** per-case `random.Random(sha256(case_id))`; no wall-clock, no `Math.random`;
  proven byte-identical on rerun. ✔
- **Honesty / signal-noise:** stay-abstained cases are seeded below every gate (cannot silently
  pass); `synthetic=true` + `stay_abstained` flags + grounding tags preserved per value for the
  downstream scoreboard split. Weakest grounding (Δλ anecdotal) disclosed in report §2/§5 and
  manifest, not laundered. Consumer named: C3A dry-run + C3B commit (signal/noise §Consumer). ✔
- **House style:** frozen dataclasses (`Band`, `CodeBandInfo`); typed; `cast` at CSV-string
  boundaries; one purpose per function; numeric research limits carry a source-cite comment
  (cluster3 line refs). No speculative abstraction. ✔
- **Structural-craft WARNING axis:** mirrors the approved `gen_c4_synth_seed.py` dataclass shape;
  bool handled as a first-class deterministic column (not shoehorned into the float `Band`
  sampler) — a deliberate divergence from C2/C4 (both float-only) because C3 has a genuine
  boolean discriminator. Flagged here so the reviewer sees the intentional shape change. No
  dead code, no orphaned params.

**GATE: CLEAN.**

## Handoff
Unblocks **[[T-V3-P4-C3A]]** (dry-run, forward-registered): in-memory ControlPlausibilityState +
EF/SF consumer sim over this seed vs the `POST_T_V3_P4_C2B` baseline, zero-overlay self-check
drift=0, WOULD_BANK/STILL_SHORT split, FT-8 audit on the live-derived 48-neighbour union
(C3-PRE §5). C3A must expect the **4 stay-abstained** cases to NOT bank and treat that as
correct, not a shortfall.
