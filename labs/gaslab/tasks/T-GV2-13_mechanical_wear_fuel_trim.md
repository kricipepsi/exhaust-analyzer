# T-GV2-13 — Worn valve-seals vs piston-rings: fuel-trim corroboration (`fuel_trim` @ 2500)

### Goal ###

The §7.23.1 RPM-differential discriminator that routes a catch-all oil hit to a
`WORN_*` leaf has **three** load-state columns at 2500 RPM: HC-direction, CO, and
**Trims** (`GAS_WIKI §7.23.1` table, L709–710 / `06a §CONCEPT_RPM_DIFFERENTIAL_
DISCRIMINATOR` L100–101). T-GV2-7 implemented the HC-direction / CO / λ columns
in the `apply_differentiators` `mechanical_wear` router but **not** the trim
column — `fuel_trim` did not yet exist as an input. T-GV2-12 has since landed
`fuel_trim` on `GasLabContext` → `classify`. This task wires the **trim column**
into the existing valve-seals-vs-rings split so the discriminator matches the
wiki table in full.

Add the trim predicate to the **two** branches the wiki gives a trim bound for:

- **`WORN_VALVE_SEALS`** — trims in the normal closed-loop band: `−8 % ≤ fuel_trim
  ≤ 8 %` (`GAS_VOCABULARY §10.8 stable_band`, the table's "± 8 %").
- **`WORN_PISTON_RINGS`** — ECU cuts fuel hard under load: `fuel_trim ≤ −12 %`
  (`GAS_VOCABULARY §10.8 negative_load_cut`, the table's "≤ −12 %").

`WORN_ENGINE` (table "~ 0 %") and `POA_SIGNATURE` (turbo-seal "~ 0 %" / severe
"variable") are **left unchanged** — the wiki gives them no discriminating trim
bound (≈0 overlaps the valve-seal band; "variable" is not a predicate). Adding a
trim gate there would be invented precision → out of scope.

### Premise (verified — read before authoring/altering) ###

- The `mechanical_wear` leaf router lives in `resolution.apply_differentiators`,
  `resolution.py:448–505` (landed by T-GV2-7). The `WORN_VALVE_SEALS` branch is
  L454–460; the `WORN_PISTON_RINGS` branch is L462–468. Both already gate on
  `reading_high` (HC≤35 / HC>300, CO, HC-direction). This task **adds one
  conjunct** to each — it does not restructure the router.
- `fuel_trim` is defined **once** on `GasLabContext` (`process.py:33`) and
  threaded into `classify` (`rule_engine.py:373`, used in the T-GV2-12 leak branch
  L250–253). It is **not** yet passed into `apply_differentiators`
  (`rule_engine.py:231` calls it without `fuel_trim`). This task threads
  `fuel_trim` through that one call + the `apply_differentiators` signature.
  **No new field, no new enum.**
- §10.8 bands are read at **2500 RPM / high-idle** (the §10.8 note), which is
  exactly the state `reading_high` represents — the band is being used at its
  declared RPM, no reuse-at-idle judgement call (unlike T-GV2-12).

### Signal/noise consumer ###

Existing `mechanical_wear` `ChemicalSignature` values `WORN_VALVE_SEALS` /
`WORN_PISTON_RINGS` → COMLab `chemical_state` / fault-atlas routing
(GASWIKI-06A, same consumer as T-GV2-7). This task adds **no** output field — it
adds a **second live read of `fuel_trim`** (the first is T-GV2-12's leak branch)
inside the WORN_* router. **No new field, no new enum.** Anti-orphan: after this
task, `grep fuel_trim GASLab/gaslab/resolution.py` must show a live read in the
WORN_* branches, not just a threaded parameter.

### Pinned literals (coder uses exactly these — no invention) ###

| Branch | Existing gate (T-GV2-7, unchanged) | **Add this conjunct** | Citation |
|---|---|---|---|
| `WORN_VALVE_SEALS` | HC≤35 ∧ HC↓ ∧ CO≤0.15 | `fuel_trim is None or -8.0 <= fuel_trim <= 8.0` | `# vocab: GAS_VOCABULARY §10.8 stable_band` |
| `WORN_PISTON_RINGS` | HC>300 ∧ HC↑ ∧ CO>0.5 | `fuel_trim is None or fuel_trim <= -12.0` | `# vocab: GAS_VOCABULARY §10.8 negative_load_cut` |

**No-regression guard (mandatory):** each conjunct is `fuel_trim is None or
<band>`. When `fuel_trim is None` the predicate is vacuously true and the branch
behaves **exactly as T-GV2-7 left it** — the no-OBD path is unchanged. The trim
band only *tightens* the route when trim is present and *contradicts* the HC/CO
evidence (e.g. a "valve-seal-looking" HC drop but trim ≤ −12 % no longer routes
to valve seals — it falls through to the unchanged `WORN_ENGINE` / POA tail).

### Steps ###

1. `rule_engine.py` — add `fuel_trim: float | None = None` to the
   `apply_differentiators` caller's signature (the function around L231) and pass
   `fuel_trim=fuel_trim` into the `apply_differentiators(...)` call at L231.
2. `resolution.py` — add `fuel_trim: float | None = None` to the
   `apply_differentiators` signature (after `reading_high`, L264); document it in
   the docstring. Add the two pinned conjuncts to the `WORN_VALVE_SEALS` (L454–460)
   and `WORN_PISTON_RINGS` (L462–468) branches, each with its inline `# vocab`
   citation. Touch no other branch.
3. Tests in `GASLab/tests/test_rule_engine.py` (mirror the T-GV2-7 WORN_* tests'
   shape — same fixtures, add `fuel_trim` to the context).

### Success criteria ###

- `test_worn_valve_seals_trim_in_stable_band` — valve-seal HC/CO vector +
  `reading_high` + `fuel_trim = 2.0` → `WORN_VALVE_SEALS` (band corroborates).
- `test_worn_piston_rings_trim_negative_load_cut` — ring HC/CO vector +
  `fuel_trim = -15.0` → `WORN_PISTON_RINGS`.
- `test_valve_seal_hc_but_negative_trim_falls_through` — valve-seal-looking HC
  drop but `fuel_trim = -15.0` → **not** `WORN_VALVE_SEALS` (trim contradicts;
  falls through to WORN_ENGINE/POA tail per the unchanged precedence).
- `test_worn_routing_unchanged_when_fuel_trim_none` — both vectors with
  `fuel_trim = None` reproduce the exact T-GV2-7 outputs (no-OBD regression guard).
- All existing GASLab tests pass (200 GAS-green baseline from T-GV2-12); inner
  loop clean on each edited file (`ruff` → `pyright` → `pytest -x -q`).

### Files to touch ###

- `GASLab/gaslab/rule_engine.py` (MODIFY — thread `fuel_trim` into the
  `apply_differentiators` call)
- `GASLab/gaslab/resolution.py` (MODIFY — `fuel_trim` param + two WORN_* conjuncts)
- `GASLab/tests/test_rule_engine.py` (MODIFY — 4 tests above)

### Out of scope ###

- **`WORN_ENGINE` / `POA_SIGNATURE` trim gates** — wiki gives "~ 0 %" / "variable",
  not a discriminating bound. No predicate ships for them (signal/noise: a gate
  with no citable threshold is invented precision).
- **No new `fuel_trim` band in the vocabulary** — both literals already exist in
  `§10.8`. Do not add an idle band (this test runs at 2500 RPM, the band's
  declared state).
- Leak-vs-sampling branch (T-GV2-12 — already consumes `fuel_trim` at idle),
  POA/induction routing (T-GV2-7 / T-GV2-9), bank-asymmetry (T-GV2-14).

### Harness compatibility ###

No schema-surface change (`fuel_trim` already on the contract since T-GV2-12) ⇒
descriptor / box table untouched, no fixture invalidation. The trim column is a
2500-RPM input — validated by gaslab pytest now and the dual-RPM box oracle
(harness T-TH-14) later.

### Sequencing note (architect) ###

Blocked-by **T-GV2-12** (defines `fuel_trim` on the contract) **+ T-GV2-7**
(defines the WORN_* router this extends). Both `done` → runnable now.
