# T-PREP-WIRE-1 — rings / PCV chemistry-contradiction ruling

**Date:** 2026-06-28 (architect, Cowork — evidence-based, run against the live tree)
**Method:** read GASLab `resolution.py` emit logic + registry rule JSON + the registry
validation corpus (`registry/corpus_curated.csv`); ran rings/PCV payloads through the live
registry `route_case_with_diagnostics`. Both contradictions were re-verified against the
**current** tree (not taken from the 2026-06-21 archived `U-WV2-*` notes).

---

## Case 1 — Worn piston rings (MW-001 / U-WV2-1): **ACCEPT-KNOWN-BLOCKED + cross-lab reconcile**

**Decision:** `ACCEPT-KNOWN-BLOCKED` for the HC-rising rings mode; forward-register a
cross-lab reconcile (`T-XLAB-RINGS-RECONCILE-1`). **Not** a safe quick fix.

**The contradiction (deeper than U-WV2-1 originally stated): GASLab and the registry hold
opposite HC-vs-RPM models for worn rings.**
- **GASLab** (`labs/gaslab/gaslab/resolution.py`, mechanical-wear differentiator) routes
  `WORN_PISTON_RINGS` when **low-idle HC ∈ [100,150] and high-idle HC > 300 and high > low**
  (HC *rises*; ring-flutter model), with `co_high > 0.5`, `λ_high < 0.99`, `fuel_trim ≤ −12`.
- **Registry MW-001** (`registry/rules/mechanical_wear.json`) gates its DEFINITIVE OBD evidence
  on **low-idle `hc ≥ 200`** (+ `co2 < 13`, `o2 ≥ 1.5`), and its own description says
  *"at higher RPM ring flutter improves sealing and HC drops"* — HC *drops*. Its validation
  corpus agrees: `MECH-001` (HC 1200 idle) and `EXT-223` (HC 800 idle → 200 at 2500) are
  **high-idle-HC, dropping** cases.

**Empirical proof (live `route_case`):**
- Rings payload in GASLab's emitted shape (`WORN_PISTON_RINGS`, low HC 120, high 380) →
  **winner `CF-001`, NOT MW-001.** MW-001's `hc ≥ 200` never fires on low-idle HC 120, so it
  loses the competition. (U-WV2-1 confirmed current.)
- Rings payload in the registry/corpus shape (`WORN_PISTON_RINGS`, low HC 380) → **winner
  `MW-001`.** So MW-001 works only for the high-idle-HC model.

**Why not fix now:** the fix requires deciding **which HC-vs-RPM model is correct for worn
rings** (a domain call) and then reconciling three artefacts — GASLab `resolution.py`, registry
`MW-001` evidence, and the regression-locked `corpus_curated.csv` (`MECH-001`/`EXT-223`/`CSV-117`/
`case_044` are MW-001 `passes_cases`). Blind-editing either side risks corpus regression and
mis-calibrating a shipped diagnostic. **Owner domain question surfaced separately:** *worn rings —
does idle→2500 HC rise (flutter) or drop (seal-improves)?*

**Consequence for `T-WIRE-2`:** a rings fixture whose GASLab emission is the low-idle-HC-rising
shape will mis-route (→ CF-001) — assert that as the **documented known-blocked** outcome until
`T-XLAB-RINGS-RECONCILE-1` lands. A high-idle-HC rings fixture routes to MW-001.

**Forward-registered:** `T-XLAB-RINGS-RECONCILE-1` (gaslab + registry ledgers).

---

## Case 2 — PCV stuck-open (MW-008 / U-WV2-2): **ACCEPT-KNOWN-BLOCKED pending verify + reconcile**

**Decision:** `ACCEPT-KNOWN-BLOCKED` pending an end-to-end verify; forward-register
`T-XLAB-PCV-VERIFY-1`. The original U-WV2-2 "POA→INCOMPLETE_OXIDATION re-classify" claim is
**partly stale** (the reworked `resolution.py` keeps `POA_SIGNATURE` as the catch-all rather than
re-routing to `INCOMPLETE_OXIDATION`), but a real gap remains.

**The gap:**
- **Registry MW-008** gates on `POA_SIGNATURE` (GATING) + `hc ≥ 500` + `high_idle_hc < 250` +
  `λ < 0.94`. It routes correctly **when handed `POA_SIGNATURE`** — proven by
  `registry/tests/test_turbo_rule.py` and `test_pcv_rule.py` (both green) and re-confirmed live:
  PCV payload (POA, HC 610, high 170, λ 0.93) → **winner `MW-008`.**
- **GASLab** routes the `POA_SIGNATURE` *leaf* only when **both** low and high HC > 500 (or the
  forced-induction turbo branch). A real PCV case where HC **drops** (low > 500 → high < 250) does
  not satisfy that leaf. Whether `POA_SIGNATURE` then survives as the mechanical-wear **catch-all**
  (→ MW-008 fires) or the case routes elsewhere is **unverified** — a synthetic PCV reading
  classified as `COOLANT_LEAK_INTERNAL` here, indicating the exact PCV gas chemistry must come
  from a real fixture, not synthesis.

**Consequence for `T-WIRE-2`:** the registry side is proven; the open question is GASLab's actual
emission for a real HC-dropping PCV case. The runner's first PCV step should **capture and assert
GASLab's emitted `chemical_state`**; if it is `POA_SIGNATURE`, PCV → MW-008 (works); if not,
assert the documented mis-route and the fix is `T-XLAB-PCV-VERIFY-1`.

**Forward-registered:** `T-XLAB-PCV-VERIFY-1` (gaslab ledger; registry MW-008 already green).

---

## Summary for the wiring pack
| Case | Ruling | Registry side | GASLab side | T-WIRE-2 expectation |
|---|---|---|---|---|
| Rings MW-001 | ACCEPT-KNOWN-BLOCKED + reconcile | works for HC≥200 only | emits HC-rising low-HC shape | low-HC rings → CF-001 (known-blocked); high-HC rings → MW-001 |
| PCV MW-008 | ACCEPT-KNOWN-BLOCKED pending verify | works when handed POA | POA leaf needs HC>500 both | capture GASLab chem; POA→MW-008, else known-blocked |

Neither blocks **authoring** the wiring pack; both are case-level expectations for `T-WIRE-2`.
