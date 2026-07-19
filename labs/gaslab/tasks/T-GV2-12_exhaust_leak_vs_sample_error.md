# T-GV2-12 — Pre-cat Exhaust-Leak vs Sample-Error Separation (`fuel_trim`)

### Goal ###

Today the "low CO + elevated O₂ + low HC" dilution signature collapses to
`SAMPLE_INVALID` at the triangle/validity gate (the "7/9 die at the gate"
symptom): a **real pre-cat exhaust leak** (cracked manifold / failed flex pipe)
is *chemically identical* to a **sampling-apparatus leak** (loose probe, leaking
hose) — both inject ~20.9 % O₂ (`GAS_WIKI §4.4` {#CONCEPT_LEAK_VS_SAMPLING},
L404–417). The wiki is explicit: **the analyser cannot separate them from gas
data alone — it needs a second source of truth: OBD short-term fuel trim.**

Wire a new optional context input `fuel_trim` (perception/DNA-context signal,
`GAS_VOCABULARY §10.8`) and add a single resolution branch that uses it to split
the EXTERNAL_O2_SUSPECT-band leak signature into:

- **`EXHAUST_AIR_LEAK`** (`GAS_WIKI §7.7`, family `exhaust_leak`) when fuel trim
  is clearly positive — the ECU is adding fuel, so the engine is truly lean /
  the leak is **physical**.
- **`SAMPLE_INVALID`** (`GAS_WIKI §7.11`, family `invalid_input`) when fuel trim
  is within the normal closed-loop band (≈ 0 / oscillating) — the leak is in the
  **sampling apparatus**.

Both target signatures already exist in `ChemicalSignature` and already have
COMLab family consumers (`exhaust_leak`, `invalid_input` in `family_map.py`
L14/L16). **No new enum value ships.**

### Signal/noise consumer ###

`fuel_trim` → new leak-vs-sampling resolution branch → routes to
`EXHAUST_AIR_LEAK` vs `SAMPLE_INVALID` (fault-atlas routing, `GAS_WIKI §4.4` +
§7.7/§7.11). **Anti-orphan gate:** after this task `grep fuel_trim` must show a
live read in `rule_engine.py`/`resolution.py`, not just the field definition.

### ⚠ Open literal — architect flag (ratify before coding) ###

`GAS_WIKI §4.4` gives only a **qualitative** discriminator ("Positive ⇒ physical;
≈ 0 / oscillating ⇒ apparatus") — it pins **no numeric idle STFT band**. The only
`fuel_trim` band in the vocabulary is `§10.8 stable_band = {min: -8.0, max: 8.0}`,
and §10.8 states those values are read at **2500 RPM / high-idle**, *not* the
idle baseline this leak test runs at.

**Pinned proxy (coder uses exactly this, no invention):** `fuel_trim > 8.0`
(strictly above §10.8 `stable_band.max`) ⇒ "clearly positive" ⇒ `EXHAUST_AIR_LEAK`;
`fuel_trim ≤ 8.0` ⇒ within band ⇒ `SAMPLE_INVALID`. Carry both citations inline:
`# wiki: GAS_WIKI §4.4` and `# vocab: GAS_VOCABULARY §10.8`.

This reuse of a 2500-RPM band at idle is the **one judgement call**. If you want a
dedicated idle band, add it to `GAS_VOCABULARY §4.4`/§10.8 as an out-of-band wiki
patch first and the coder cites that instead. Until then the proxy above is the
citable rule. **Coder: do not change this literal.**

### Steps ###

1. Add `fuel_trim: float | None = None  # vocab: GAS_VOCABULARY §10.8` to
   `GasLabContext` (`process.py`), pass it through `classify(...)` like
   `block_test_passed` / `reading_high`. Field added **once here**; T-GV2-13
   (mechanical-wear) consumes the same field, does not re-add it.
2. In `rule_engine.py`, in/after the existing leak path (`_is_low_triangle_
   exhaust_air_leak` L189 and the validity branch L192–194), gate on `fuel_trim`
   per the pinned proxy. When `fuel_trim is None`, **behaviour is unchanged**
   (current SAMPLE_INVALID/triangle outcome) — no regression on the no-OBD path.
3. Tests per success criteria.

### Success criteria ###

- `test_leak_physical_when_fuel_trim_positive` — dilution signature (low CO,
  high O₂, low HC, triangle in 16–18 band) with `fuel_trim = 12.0` →
  `EXHAUST_AIR_LEAK`.
- `test_leak_sampling_error_when_fuel_trim_in_band` — **same gases** with
  `fuel_trim = 2.0` → `SAMPLE_INVALID`.
- `test_leak_unchanged_when_fuel_trim_none` — same gases, `fuel_trim = None` →
  identical to today's output (no-OBD regression guard).
- All existing GASLab tests pass (195 baseline from T-GV2-9).

### Files to touch ###

- `GASLab/gaslab/process.py` (MODIFY — add `fuel_trim` to `GasLabContext`)
- `GASLab/gaslab/rule_engine.py` (MODIFY — leak-vs-sampling branch)
- `GASLab/tests/test_rule_engine.py` (MODIFY — 3 tests above)

### Out of scope ###

- **`mechanical_wear` distinct chemistry** (the second clause of the original
  one-liner) → **split to T-GV2-13** per owner decision 2026-06-05. That task
  consumes the same `fuel_trim` field for the §7.23.1 worn-valve-seals vs
  worn-piston-rings RPM-differential discriminator (§10.8 `negative_load_cut`),
  a different family at 2500 RPM. Do not touch WORN_* routing here.
- No new `ChemicalSignature` value. `probe-occlusion test` (`§4.4` step 2,
  TEST_PROBE_OCCLUSION) is an operator/OBD action, not a GASLab input — out.
- Forced-induction / NOₓ (T-GV2-9), POA/oil routing (T-GV2-7).

### Sequencing note (architect) ###

Blocked-by **T-GV2-4** (validity-gate + EXTERNAL_O2_SUSPECT plumbing already
landed there). T-GV2-13 is Blocked-by **T-GV2-12 + T-GV2-7** (needs this field +
the WORN_* routing). Author T-GV2-12 first so `fuel_trim` is defined once.
