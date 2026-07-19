# Why the v2 rebuild did not move accuracy — root-cause audit
**Date:** 2026-06-30 · **Author:** architect (Cowork), read-only · **Status:** evidence-backed; one link marked **inferred** pending a runtime trace.
**Question being answered (owner):** "We addressed the *data* — reworked wikis, researched the missing signals, trimmed 10 years of hard-to-diagnose modern vehicles, and did a full rebuild. Why is accuracy still ~48%?"

---

## 1. Bottom line
The rebuild improved the layers that were **not** the bottleneck (architecture, rules, wikis, oracle) and left untouched the one that **is**: the **physical discriminating power of the input data**. New data that is not *discriminating* data cannot move a discrimination-bound score. Your own June-3 audit predicted exactly this; this run now **proves it at the row level**, where the v1 effort could only infer it.

This is not a code regression and not a bluff. Three independent lines of evidence converge on the same wall (§2–§4).

---

## 2. The mechanism, shown on real rows (verified this session)
Take the `mechanical_wear` family — 0/14 routed correctly in the v7 run, the single largest dead cluster, and representative of the pattern.

**What the v2 engine has (verified):**
- The v2 registry **does** carry rules for the "dead" families: `mechanical_wear` 10 rules, `exhaust_leak` 4, `non_starter` 5. **Coverage is not the gap.**
- `MW-001` (worn piston rings) requires chemistry state **`WORN_PISTON_RINGS` as GATING** — a hard precondition. If GASLab doesn't emit that exact state, the rule is pruned before scoring.
- GASLab *can* emit `WORN_PISTON_RINGS` (`gaslab/contracts.py:60`, `family_map.py:50`, `resolution.py:452`). The producer exists.

**What the cases actually carry (verified, from `cases_petrol_v7.csv`):**
All 14 `mechanical_wear` rows are a warm-idle 5-gas snapshot with **high HC (850–1100 ppm)** and DTC **`P0300`** (random misfire). Example: `hc=950, co=0.7, co2=11.0, o2=3.2`, `dtc=["P0300"]`, expected `ERR-MW-002`.

**What the misfire rules do with that same input (verified):**
`MF-001/005/006` gate on `IGNITION_MISFIRE` / `TIMING_RETARDED` chemistry, score on **`hc ≥ 200`**, and match **`P0300`** as DTC evidence. `P0300` appears **8×** across misfire rules vs **2×** in mechanical_wear. So the high HC *and* the misfire DTC both point at misfire.

**The collision:** worn rings and misfire both raise HC at idle, and the case carries `P0300` (a misfire code). The mechanical_wear rule needs a *distinct* chemistry state (`WORN_PISTON_RINGS`) to survive pruning; the misfire rules only need the *generic* high-HC state plus the DTC that is already present. The louder family wins every tie — exactly the v7 result (`mechanical_wear → misfire`, 10 cases).

## 3. The one link still to confirm at runtime (honest gap)
I could **not** run GASLab in this environment (no host venv here). So this link is **inferred, not runtime-proven**: that for these high-HC + `P0300` rows GASLab emits a generic misfire-ish state (`IGNITION_MISFIRE` / `TIMING_RETARDED`) rather than `WORN_PISTON_RINGS`, pruning `MW-001`. It is a strong inference (the audit already records `TIMING_RETARDED` as ~25% of emissions mapping to 7 families, and mechanical_wear as emitting "no distinct chemistry"), but it must be confirmed. **Cheapest confirmation: the Jaeger `phase.prune` span (T-V7-6) on one MW case, or a single host run** — it will show `MW-001` dropped on unsatisfied GATING and a misfire rule as winner. This is the first thing to do before any further spend.

## 4. Why this is a producer/physics gap, not a rules gap
The discriminating decision has to be **produced upstream** (GASLab classifies the chemistry; OBDLab produces trims) from the raw signal. The raw signal modality — **one warm-idle 5-gas snapshot + whatever DTC happens to exist** — physically does not separate the confusable families. You can author a `WORN_PISTON_RINGS` rule, but if the input cannot be classified as that state, the rule is dead weight. This is your own **signal/noise rule violated upstream**: the *consumer* (the MW rule) was added without a reliable *producer* (the distinct GASLab state). It is the June-3 audit's Culprit 1 (ranking, data-starved) + Culprit 4 (indistinguishable families) — now confirmed on the rows.

---

## 5. Why the three things you changed could not have moved the number
- **"Reworked wikis + researched missing data."** Wikis and the oracle are the **truth/grading** layer, not the **signal** layer. Better wikis make the oracle *stricter* (it grades against a sharper expected answer) but give GASLab/OBDLab **no new input** to separate families with. A sharper oracle can even *lower* the measured score. The researched values are still the **same modality** (idle 5-gas, sparse DTC) the audit already proved non-discriminating.
- **"Trimmed 10 years of modern vehicles."** The June-3 `PURGE` wave already did exactly this in v1 → **0.0pp**. Removing modern cars removes **easy/noise** cases; the dead families (worn rings vs misfire on a 2003 car) are **old-fleet, single-snapshot** confusions. Narrowing model years doesn't touch them — and by deleting easy wins it can nudge the percentage *down*.
- **"Full rebuild."** It rebuilt the **architecture** — which the audit already called clean — and consolidated the two-registry split. Real engineering value, but aimed at a layer that was never the constraint.

## 6. What the rebuild *did* buy (so the month isn't written off)
Verified from the v7 run and this audit: the engine is now **crash-free across 314 cases**, **all 12 families reachable**, **multi-dimensionally scored**, and the rule-registry split the audit complained about is consolidated. And this run produced the **row-level proof** of where the ceiling is — which the v1 campaign only inferred after ~60 tasks. That proof is what lets you *stop* spending against the wrong layer. If the rebuild's goal was "lift accuracy," that goal was pointed at the wrong layer — and the June-3 audit said so in writing before the rebuild started.

---

## 7. Options now (honest, with the real trade)
**A. Confirm the mechanism cheaply, then decide (do this first).** Trace one MW case (T-V7-6) to prove the prune-on-GATING + misfire-wins chain. Near-zero cost; removes the one inferred link. *No engine change.*

**B. Measure what is actually separable (reframe success).** Have GASLab/the engine **explicitly abstain** on families that a single idle snapshot cannot separate (`mechanical_wear`, `exhaust_leak`, `non_starter`, much of `ecu_fault`) and report accuracy on the separable subset. Likely a **defensible 70–85%** on a stated scope instead of an unwinnable 48% across everything. This is the audit's own GASLab Q9. Modest effort; changes what "accuracy" means, honestly.

**C. Add a discriminating channel (the only path to high accuracy on *all* families).** The separation the engine lacks isn't in the data because the **measurement** doesn't capture it: e.g. **snap-throttle / transient gas** (worn valve seals show a transient HC plume vs steady misfire — your own MW-004 note says this), **dual-RPM deltas**, **real STFT/LTFT**, **Mode $06**. This is a **test-protocol / data-acquisition** change, not engine code. Slow; needs real-vehicle or standards data. It is what the June-3 research questions are for.

**D. Change the product definition.** Several families are **provably tied** on the available evidence. A single-verdict classifier will always lose those ties. Shipping a **ranked top-3 differential with confidence + abstention** is honest where the data is ambiguous, and is achievable now.

## 8. The hard truth to sit with
With the current input modality — one warm-idle 5-gas snapshot plus whatever DTC exists — **~50% single-verdict accuracy across all families may be at or near the physical ceiling**, for v1 and v2 alike. No amount of rules, wikis, oracle work, or rebuilding moves a discrimination limit that lives in the measurement. The levers that *do* move it are **B** (narrow the claim), **C** (capture a new signal), or **D** (change the verdict shape). Engine tuning is not on that list — and the audit's FT-8 finding says tuning the ties *regresses* neighbours.

---
*Verified vs inferred is marked throughout. The only inferred link (§3) is cheap to confirm and is the recommended first action.*
