# Master Exhaust Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for the exhaust system on petrol engines (MY 1990–2020) — the physical function of each exhaust component from manifold to tailpipe, the exhaust-leak and probe-air physics that affect gas-analyser readings, the canonical gas signatures for exhaust restriction, pre-catalyst air leak, post-catalyst air leak, and exhaust backpressure faults, the physical justification for every threshold the 4D engine uses in the `exhaust_leak_pre_cat`, `exhaust_leak_post_cat`, `exhaust_restricted`, `probe_air_sample_error`, and `exhaust_backpressure_elevated` KG nodes, and the relationship between exhaust integrity and gas-analyser validity. Rows in the CSV that cite exhaust system faults as the expected diagnosis cite the rules below.

---

## 1. Exhaust system architecture — petrol engines

The exhaust system performs four functions: gas transport, noise attenuation, emission after-treatment, and (with forced induction) energy recovery for the turbocharger turbine.

### 1.1 Component chain (front to rear)

```
Cylinder head exhaust port
    → exhaust manifold (or turbo manifold on forced-induction engines)
        → exhaust manifold gasket (head-to-manifold seal)
            → upstream O₂ sensor (pre-cat, bank-specific)
                → close-coupled three-way catalyst (TWC) or under-floor catalyst
                    → downstream O₂ sensor (post-cat, catalyst monitor)
                        → flex pipe / flex joint (absorbs engine movement)
                            → resonator (cancels specific frequencies, typically 1500–2500 RPM drone)
                                → muffler / silencer (broadband noise reduction)
                                    → tailpipe (final outlet, analyser probe insertion point)
```

### 1.2 Per-component diagnostic relevance

| Component | Diagnostic signal | Failure mode | Gas signature |
|-----------|------------------|-------------|---------------|
| Exhaust manifold gasket | Ticking noise at cold idle; possible cabin CO | Leak between head and manifold | See §3.1 (pre-cat leak) |
| Exhaust manifold (cast iron or tubular) | Visual crack; soot marking at crack | Crack from thermal cycling | See §3.1 |
| Upstream O₂ sensor bung | Black soot around threads | Loose bung; threads stripped | See §3.1 (air enters at sensor) |
| Close-coupled TWC | Rattling from cold start; O₂ storage test failure | Melted substrate, broken monolith | See `master_catalyst_guide.md` |
| Downstream O₂ sensor | Post-cat O₂ mirrors pre-cat → catalyst dead | Sensor or catalyst failure | See `master_o2_sensor_guide.md` |
| Flex pipe | Exhaust noise under acceleration; visible crack in braided section | Fatigue cracking | See §3.1 or §3.2 depending on position relative to downstream O₂ sensor |
| Resonator | Drone at specific RPM; no gas signal effect | Internal baffle failure, rust-through | External leak only; post-treatment, no gas effect |
| Muffler | Exhaust louder; no gas signal effect unless rusted through | Internal baffle collapse (restriction) or external rust-through | See §4 if restricted |
| Tailpipe | Corrosion at outlet; probe cannot seat | Rust-through near outlet; air ingress near probe tip | See §2 (probe air) |

---

## 2. Probe-air physics — the analyser's exhaust-leak detection mechanism

The 5-gas analyser measures exhaust constituents at the tailpipe. If ambient air enters the exhaust stream between the engine and the analyser probe, the sample is contaminated — all readings shift, and the computed Brettschneider λ becomes invalid. The 4D engine must detect probe-air contamination before interpreting any gas data, because contaminated samples can produce gas signatures that mimic lean combustion, rich combustion, or catalyst failure.

### 2.1 The probe-air gas signature

Ambient air is 20.9 % O₂, ~0.04 % CO₂, 0 ppm HC, 0 ppm CO, 78 % N₂. When this air mixes into the exhaust sample:

| Gas | Shift direction | Mechanism |
|-----|----------------|-----------|
| O₂ | **Rises** — to 3–8+ % on a contaminated sample | Ambient air adds 20.9 % O₂; dilutes exhaust O₂ but net O₂ % rises because exhaust at stoich has ~0.5 % O₂ |
| CO₂ | **Falls** — to 8–12 % on a contaminated sample | Ambient air has ~0.04 % CO₂; dilutes exhaust CO₂ (normally 13–15 %) |
| HC | **Falls** (dilution) | Ambient air has 0 ppm HC; dilutes exhaust HC proportionally |
| CO | **Falls** (dilution) | Ambient air has 0 ppm CO; dilutes exhaust CO |
| NOx | **Falls** (dilution) | Ambient air has ~0 ppm NOx |
| λ | **Artificially biased toward 1.00** | The Brettschneider formula is based on atomic balances; diluting all species with ambient air shifts λ toward the ambient-air apparent lambda (~1.00). A truly rich or lean mixture can appear stoich. |

### 2.2 The O₂-CO₂ sum rule — primary probe-air detector

On a properly sealed exhaust with a properly combusting engine, the sum of O₂ + CO₂ at the tailpipe falls in a narrow range: **14.5–16.5 %**. This is the single most reliable probe-air check:

| O₂ + CO₂ sum | Interpretation |
|---------------|---------------|
| 14.5–16.5 % | Sample integrity good — no significant air leak into exhaust |
| 16.5–19.0 % | Mild dilution — small leak; analyser readings are suspect; flag as soft warning |
| > 19.0 % | Significant dilution — all gas readings invalid; do not score gas-based symptoms |
| < 14.0 % | Anomalous — typically measurement error or very rich mixture; re-test |

**Physical basis:** Complete combustion of a stoichiometric hydrocarbon-air mixture produces ~15 % CO₂ and ~0.5 % O₂ (sum ≈ 15.5 %). Any mixture within the combustible range (λ 0.8–1.2) produces a sum in the 14.5–16.5 % band. Outside combustion entirely (pure air), the sum approaches 21 % (20.9 % O₂ + 0.04 % CO₂). An O₂ + CO₂ sum significantly above 16.5 % is unambiguous evidence of air dilution between cylinder and probe — **the analyser is not reading combustion products; it is reading combustion products diluted with ambient air.**

### 2.3 Secondary probe-air check — the λ stability test

If the O₂-CO₂ sum is borderline (16.0–17.0 %): observe λ at idle over 30 seconds. A genuine rich or lean mixture produces a stable λ (or a stable oscillation around stoich in closed-loop). Probe-air contamination produces an **unstable, drifting λ** — as the leak opens and closes with exhaust pulsation and chassis vibration, the dilution ratio changes and λ wanders. This is the secondary check. If λ is stable at a value consistent with other evidence (fuel trims, O₂ sensor voltage, DTCs), the borderline sum may be from a non-stoichiometric but real combustion condition. If λ drifts with no corresponding change in fuel trims, the sample is contaminated.

### 2.4 Probe maintenance as a diagnostic gate

A blocked or partially inserted probe can also cause anomalous readings by sampling stratified exhaust (not a representative cross-section of the tailpipe flow). The 4D engine's VL must check for probe-air contamination as a precondition to gas scoring. If probe-air is detected, all gas-derived symptoms are suppressed and the `probe_air_sample_error` warning flag is set in the result.

---

## 3. Exhaust leak gas signatures — pre-cat vs post-cat

The location of an exhaust leak relative to the oxygen sensors and catalyst determines its gas signature and diagnostic meaning.

### 3.1 Pre-catalyst exhaust leak (upstream of the upstream O₂ sensor)

**Location:** Exhaust manifold gasket, manifold crack, loose O₂ sensor bung, or cracked manifold runner between the cylinder head and the upstream O₂ sensor.

**Physics:** Ambient air enters the exhaust stream through the leak during the low-pressure phase of each exhaust pulse (between cylinder exhaust events, the exhaust pressure momentarily drops below atmospheric, creating a Venturi effect that draws air into the leak). The upstream O₂ sensor sees elevated oxygen and reports "lean." The ECU adds fuel (positive trim). The actual combustion is stoichiometric or rich — the "lean" signal is from post-combustion air contamination.

**Gas signature at tailpipe:**

| HC | CO | CO₂ | O₂ | λ | Fuel trim |
|----|-----|------|-----|-----|-----------|
| Normal or slightly elevated | May be elevated (ECU adds fuel responding to false-lean signal) | Normal | Normal or slightly elevated | Normal (the air leak is between combustion and analyser, but O₂ sensor sees it and commands extra fuel) | Sharply positive at idle |

**Key discriminator vs vacuum leak:** Both cause positive fuel trim at idle. A pre-cat exhaust leak causes O₂ to appear elevated at the O₂ sensor but NOT (or less) at the tailpipe (where the leak has mostly diluted the sampled gas between leak and tailpipe... actually, the air is entering between head and O₂ sensor, and the tailpipe is after the O₂ sensor, so the tailpipe sees the diluted gas plus added fuel products). A vacuum leak causes O₂ to be truly elevated everywhere — in the cylinder, at the O₂ sensor, and at the tailpipe.

**The definitive test:** Block the tailpipe briefly with a rag at idle. If the manifold leak is significant, the exhaust leak sound becomes noticeably louder as backpressure forces more gas through the leak path. Normal engines will simply stall or struggle — the change in leak sound is the diagnostic signal.

**Critical note — this is perception-gap mechanism #1:** The ECU's lambda reading is corrupted by the air leak. The analyser may also be partially corrupted depending on where the leak is relative to the tailpipe probe. This is the physical basis for a perception gap (L01) — the ECU perceives lean, but the true combustion chemistry may be rich. See `master_perception_guide.md §2.1`.

### 3.2 Post-catalyst exhaust leak (downstream of the upstream O₂ sensor)

**Location:** Flex pipe, resonator, muffler, tailpipe, or any joint downstream of the upstream O₂ sensor but upstream of the tailpipe analyser probe.

**Physics:** The upstream O₂ sensor sees true combustion products (no air contamination). The ECU's fuel control is accurate. The leak dilutes the exhaust gas between the sensor location and the analyser probe. The AFR reading at the tailpipe is contaminated; the ECU's fuel trim is correct for the actual combustion.

**Gas signature at tailpipe:**

| HC | CO | CO₂ | O₂ | λ | Fuel trim |
|----|-----|------|-----|-----|-----------|
| **Diluted — all lower than true** | **Diluted** | **Depressed** (below 14 %) | **Elevated** (3–6+ %) | **Biased toward 1.00** | Normal (ECU sees true combustion) |

**Key discriminator vs lean combustion:** Post-cat exhaust leak + normal fuel trims = contamination, not lean combustion. Lean combustion + positive fuel trims (ECU compensating) = genuine lean condition.

**Key discriminator vs pre-cat leak:** Pre-cat leak → positive fuel trim; post-cat leak → normal fuel trim. The fuel-trim channel is the splitter.

### 3.3 Tailpipe probe-adjacent leak

**Location:** Rust hole, crack, or loose clamp within ~30 cm of the tailpipe outlet.

**Physics:** The leak is so close to the probe that ambient air is drawn directly into the sample during the analyser pump's intake stroke. This is the most severe contamination case — it can produce gas readings that are 80–90 % ambient air, with O₂ near 20 %, CO₂ near 1 %, and all other gases near zero.

**Detection:** O₂ + CO₂ sum > 19 % (§2.2). Flag as `probe_air_sample_error` immediately. No gas-based symptoms can be scored when this condition is present. The VL must reject the sample and flag it to the user.

---

## 4. Exhaust restriction — elevated backpressure

### 4.1 Physical mechanism

Exhaust restriction increases the pressure the piston must work against during the exhaust stroke (pumping loss). Causes include:
- Collapsed catalyst substrate (melted monolith blocks flow path)
- Collapsed muffler baffle (internal corrosion, manufacturing defect)
- Crushed exhaust pipe (road debris, incorrect jack placement)
- Carbon-clogged catalyst (sustained rich operation deposits carbon in the substrate channels)
- Flex pipe inner liner collapsed (inner braid separates, blocks flow while outer braid appears intact)

### 4.2 Gas and mechanical signatures

| Signal | Effect | Mechanism |
|--------|--------|-----------|
| MAP at idle | **Elevated** — manifold vacuum is lower (closer to BARO) | Backpressure reduces gas evacuation → residual exhaust gas remains in cylinder → next intake stroke has less cylinder depression → MAP rises |
| MAP at WOT | **Insufficient rise** — cannot reach target for RPM | Exhaust cannot exit fast enough → cylinder scavenging incomplete → less fresh charge for next cycle |
| HC | Elevated | Incomplete scavenging leaves residual HC; poor combustion from EGR effect of trapped exhaust gas |
| CO | Normal or elevated | Reduced volumetric efficiency → ECU adds fuel to maintain power |
| CO₂ | Slightly depressed | Reduced fresh charge per stroke |
| O₂ | Near normal | Combustion still consumes available O₂ |
| λ | May be rich at WOT | ECU enriches to compensate for power loss |
| Exhaust sound | Muffled, hissing, or "whooshing" from restriction point | Gas velocity at restriction increases → noise changes |

### 4.3 Backpressure measurement — the vacuum gauge method

The simplest field test: connect a vacuum gauge to the intake manifold. At warm idle, note the vacuum reading. Snap the throttle to WOT (~2500–3000 RPM) and hold for 10 seconds:
- **Normal:** Vacuum drops at throttle snap, then recovers to near-idle value as RPM stabilises
- **Restricted:** Vacuum drops at throttle snap and **fails to recover** — it continues to fall as exhaust backpressure builds and residual gas accumulates in the cylinders

This is the classic "vacuum gauge exhaust restriction test" and is valid for all petrol engines 1990–2020.

---

## 5. Exhaust system tone and noise as diagnostic signals

Exhaust noise changes are often the first signal of an exhaust fault, arriving before any gas signature or DTC. The 4D engine does not process audio, but technicians entering diagnostic data should be prompted for exhaust noise observations.

| Noise | Timing | Likely cause |
|-------|--------|-------------|
| Ticking / tapping, loudest at cold idle | Cold idle only; disappears or quiets as engine warms | Exhaust manifold gasket leak — manifold and head expand at different rates; leak closes as metal heats |
| Ticking at all temperatures | All conditions; frequency = RPM ÷ 2 | Persistent manifold leak; cracked manifold or failed gasket |
| Hissing under acceleration | Under load, boost (turbo) or high MAP | Exhaust leak at a flange or joint; gas velocity increases under load |
| Rattle from catalyst area | Cold start only; stops after ~30 s | Catalyst substrate broken; monolith pieces rattle until they wedge in place |
| Rattle from muffler | All conditions | Muffler baffle loose; internal corrosion |
| Drone at specific RPM (typically 1500–2500) | Specific RPM band | Resonator failure or exhaust system resonance from a rigid joint (failed flex pipe) |
| "Chuffing" or puffing at idle | Idle, most audible at tailpipe | Misfire producing unburned charge; exhaust pulse is uneven |
| Exhaust louder overall | All conditions | Muffler or resonator rust-through; hole in exhaust pipe |

---

## 6. Exhaust system — interaction with other diagnostic domains

### 6.1 Catalyst interaction

The exhaust system is the catalyst's housing. A pre-cat exhaust leak admits oxygen downstream of combustion, directly into the catalyst's inlet. The upstream O₂ sensor sees this oxygen and drives the mixture rich. The catalyst receives a rich mixture with excess air at the same time — this can drive the cat into an exothermic reaction (fuel + O₂ on the catalyst surface → heat) that can melt the substrate. **A pre-cat exhaust leak is a catalyst-destroying fault** — prolonged operation with a manifold leak can cause P0420/P0430 from catalyst thermal degradation.

Source guide: `docs/master_guides/catalyst/master_catalyst_guide.md`

### 6.2 O₂ sensor interaction

The upstream O₂ sensor's accuracy depends on an intact exhaust ahead of it. Any air entering upstream of the sensor (§3.1) corrupts its reading. The downstream O₂ sensor's catalyst-monitor function depends on an intact exhaust between the catalyst and the sensor — a leak between the cat and downstream O₂ sensor causes the downstream sensor to read lean (ambient air), which the ECU interprets as a failed catalyst (P0420).

Source guide: `docs/master_guides/o2_sensor/master_o2_sensor_guide.md`

### 6.3 EGR interaction

External EGR systems tap exhaust gas from the exhaust manifold or a dedicated EGR port. An exhaust restriction (§4) upstream of the EGR tap point increases exhaust backpressure, which can force more exhaust gas through the EGR valve than commanded — producing EGR over-dilution symptoms (HC spike, lean misfire) indistinguishable from a stuck-open EGR valve. **An exhaust restriction upstream of the EGR tap is a hidden EGR fault.** Always check exhaust backpressure before condemning an EGR valve that appears to be over-diluting.

Source guide: `docs/master_guides/egr/master_egr_guide.md`

### 6.4 Turbocharger interaction

On turbocharged engines (§2), the exhaust system provides the energy source for the turbine. A pre-turbine exhaust leak (manifold gasket, manifold crack) bleeds exhaust energy before it reaches the turbine → slower spool, lower boost, underboost DTC (P0299). A post-turbine restriction (collapsed catalyst, crushed pipe) creates high turbine outlet pressure → reduced pressure ratio across the turbine → slower spool, lower boost. **Exhaust leaks and restrictions are common root causes of underboost DTCs that are misdiagnosed as turbocharger failure.**

Source guide: `docs/master_guides/turbo/master_turbo_guide.md` §5.2, §5.4

---

## 7. Exhaust thresholds — provenance table

Every numeric threshold the 4D engine applies to exhaust system signals. All values are petrol-only, MY 1990–2020.

| Parameter | Value | Unit | Applies to | Physical basis | Source guide |
|-----------|-------|------|-----------|----------------|-------------|
| `o2_co2_sum_normal_min` | 14.5 | % | All conditions | Stoich combustion produces ~15 % CO₂ + ~0.5 % O₂; lower bound for very lean (λ 1.20) | `docs/master_guides/exhaust/master_exhaust_guide.md` §2.2 |
| `o2_co2_sum_normal_max` | 16.5 | % | All conditions | Upper bound for very rich (λ 0.80); above 16.5 → dilution suspected | `docs/master_guides/exhaust/master_exhaust_guide.md` §2.2 |
| `o2_co2_sum_soft_warning` | 17.0 | % | All conditions | Mild dilution; flag gas results as suspect; proceed with reduced confidence | `docs/master_guides/exhaust/master_exhaust_guide.md` §2.2 |
| `o2_co2_sum_hard_fail` | 19.0 | % | All conditions | Severe dilution; all gas-based symptoms suppressed; `probe_air_sample_error` flag set | `docs/master_guides/exhaust/master_exhaust_guide.md` §2.2 |
| `vacuum_drop_restriction_test` | −15 | kPa | Warm idle → snap 2500 RPM, hold 10 s | Vacuum should recover to within 15 kPa of idle vacuum; failure to recover → exhaust restriction | `docs/master_guides/exhaust/master_exhaust_guide.md` §4.3 |
| `exhaust_backpressure_max_idle` | 10 | kPa | Warm idle, measured at O₂ sensor bung or EGR port | Normal backpressure at idle is low (~3–7 kPa); above 10 kPa → restriction or catalyst block | `docs/master_guides/exhaust/master_exhaust_guide.md` §4 |
| `exhaust_backpressure_max_wot` | 25 | kPa | WOT, measured upstream of catalyst | Backpressure above 25 kPa at WOT → significant restriction; catalyst, muffler, or crushed pipe | `docs/master_guides/exhaust/master_exhaust_guide.md` §4 |
| `lambda_stability_window_sec` | 30 | s | Idle, warm, closed-loop | λ should be stable or oscillating regularly around 1.00; drifting λ with stable fuel trims → probe-air contamination | `docs/master_guides/exhaust/master_exhaust_guide.md` §2.3 |

---

## 8. Exhaust — engine-state modifiers

| Engine state | Exhaust behaviour | Diagnostic meaning |
|-------------|------------------|-------------------|
| Cold start (ECT < 40 °C) | Manifold leak at its loudest (thermal expansion not yet sealed); exhaust system cold, metal contracted | Ticking noise at cold idle → manifold gasket leak; quiets as warm → confirms thermal-seal leak |
| Warm idle | Steady exhaust flow; best condition for O₂-CO₂ sum check and probe-air detection | Run probe-air check (§2.2) at warm idle for most stable reading |
| Closed-loop cruise | Exhaust flow varies with load; flex pipe moves with engine rocking | Exhaust noise may change under load vs idle; use for leak localisation |
| WOT | Maximum exhaust flow and pressure; backpressure test (§4.3) most informative | Restriction most evident at WOT; backpressure rises exponentially with flow |
| Decel fuel cut | Exhaust carries only air (fuel injected = 0) → O₂ spike → this is normal | Do not score O₂-CO₂ sum during DFCO — the sum is meaningless during fuel cut |

---

## 9. Multi-bank exhaust considerations (V6/V8/V10/V12 engines)

On multi-bank engines, each bank has an independent exhaust manifold and (typically) its own upstream O₂ sensor and TWC. A bank-specific exhaust leak affects only that bank's readings:

| Configuration | Exhaust layout | Bank-specific leak detection |
|---------------|---------------|---------------------------|
| V-engine, dual exhaust (true dual) | Each bank has independent exhaust to tailpipe; two tailpipe analyser probe points | Bank leak → affected tailpipe shows dilution; unaffected tailpipe is clean |
| V-engine, Y-pipe merge (single tailpipe) | Banks merge after cats into single exhaust; one tailpipe probe point | Bank leak → tailpipe shows partial dilution; bank-to-bank asymmetry may be detectable in OBD PIDs (trim split, O₂ sensor voltage split) |
| V-engine, H-pipe or X-pipe (dual with crossover) | Banks cross-connected for scavenging; two tailpipes but not independent | Cross-pipe complicates bank isolation; probe both tailpipes; the diluted bank is the one with the more severely affected reading |

**Bank-symmetry correlation:** The arbitrator (M3) performs bank symmetry analysis. An exhaust leak on one bank produces O₂ and trim asymmetry that M3 must distinguish from genuine bank-to-bank breathing or fuelling faults. The exhaust-leak bank will show positive fuel trim (false-lean at O₂ sensor) with O₂ elevated at that bank's tailpipe relative to the other bank. See `master_arbitrator_guide.md` for the bank-symmetry algorithm.

---

## 10. Petrol-only scope boundary (R12)

This guide covers spark-ignition petrol exhaust systems only. Diesel exhaust systems differ significantly:
- Diesel exhaust carries particulate matter (soot) requiring DPF after-treatment
- Diesel exhaust temperature is lower, affecting catalyst light-off and thermal sealing behaviour
- Diesel exhaust backpressure sensitivity is higher due to turbocharger dependence on exhaust enthalpy
- Diesel exhaust has excess oxygen at all times (lean-burn) — the O₂-CO₂ sum rule (§2.2) does not apply because tailpipe O₂ can legitimately be 5–15 % on a healthy diesel engine
- No diesel exhaust thresholds, mechanisms, or diagnostic pathways appear in this guide or in the 4D engine.

---

## 11. Cross-references

| Domain | Guide | Why linked |
|--------|-------|-----------|
| Catalyst | `docs/master_guides/catalyst/master_catalyst_guide.md` | Pre-cat leaks destroy catalysts; exhaust restriction from collapsed cat substrate |
| O₂ sensor | `docs/master_guides/o2_sensor/master_o2_sensor_guide.md` | Upstream sensor corrupted by pre-cat leaks; downstream sensor corrupted by post-cat leaks |
| Perception | `docs/master_guides/perception/master_perception_guide.md` | Pre-cat exhaust leak is Perception Gap cause #1 — ECU sees lean, chemistry is normal |
| EGR | `docs/master_guides/egr/master_egr_guide.md` | Exhaust restriction upstream of EGR tap mimics stuck-open EGR; backpressure forces EGR flow |
| Turbo | `docs/master_guides/turbo/master_turbo_guide.md` | Pre-turbine leaks bleed exhaust energy → underboost; post-turbine restriction → same symptom |
| Gas chemistry | `docs/master_guides/gases/master_gas_guide.md` | Gas reading validity depends on exhaust integrity; probe-air corrupts all gas channels |
| Air induction | `docs/master_guides/air_induction/master_air_induction_guide.md` | Exhaust restriction raises MAP at idle — same symptom as vacuum leak; must distinguish |
| Mechanical | `docs/master_guides/mechanical/master_mechanical_guide.md` | Burned exhaust valve mimics pre-cat leak — exhaust gas leaks past valve seat into exhaust port between pulses |
