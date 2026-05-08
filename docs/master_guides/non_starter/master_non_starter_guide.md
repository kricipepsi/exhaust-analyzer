# Master Non-Starter Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define the three-criteria non-starter test (compression + fuel + spark, all timed correctly), gas fingerprints for no-spark vs no-fuel vs no-compression vs flooded vs immobiliser-cut, CKP/CMP failure signatures, the cranking RPM and cranking-MAP electronic-vacuum-gauge tests, and the 4D engine's routing rules for non-starter cases. The non-starter pipeline is parallel to the running-engine pipeline — different gates, different rules.

**Scope.** Petrol engines that crank but do not start. Engines that won't even crank (battery, starter motor, immobiliser-disable-crank) are upstream of this guide and routed via the pre-diag form to a separate flow.

---

## 1. The fundamental truth

An internal-combustion engine needs **exactly three things** to start, all at the right time:

1. **Compression** — the chamber must seal well enough to produce a combustible mixture pressure.
2. **Fuel** — vapourised petrol delivered to the chamber within calibrated AFR limits.
3. **Spark** — high-voltage discharge across the plug gap at the right crank angle.

If the engine cranks but does not start, one or more of those is missing. The diagnostic task is to identify which — **fast** — using the gas analyser as the principal tool. The gas analyser is uniquely suited to non-starter diagnosis because it sees the *output* of all three systems simultaneously.

---

## 2. Cranking gas fingerprints

The analyser probe inserted during cranking provides the single most informative non-starter data point. Each non-starter cause produces a distinct fingerprint:

| Fingerprint | HC | CO | CO₂ | O₂ | λ | Diagnosis |
|---|---|---|---|---|---|---|
| **No fuel** | ≈ 0 | ≈ 0 | ≈ 0 | ≈ 20.9 % (ambient) | → ∞ | Fuel pump dead, injectors not firing, immobiliser fuel-cut, CKP-failure-cuts-injection |
| **Flooded (excess fuel, no spark)** | Very high (often > 5000 ppm) | High (3–8 %) | Low | Low | < 0.7 | Injectors firing, ignition missing; raw fuel exits |
| **No spark / ignition** | Very high (> 1000 ppm) | Low | Low | High (10–18 %) | ≈ 1.0 (raw fuel + raw air balance) or unstable | Coil failure, ignition switch fault, ECU output stage fail, all-coils-failed event |
| **No compression** | 0–500 ppm | 0–0.5 % | Very low (< 2 %) | 15–19 % | ≈ 1.0 (balanced) | Timing belt jumped/broken, severe ring/valve wear, head off, all cylinders affected |
| **Normal cranking (will start with patience)** | 200–800 ppm | 0.5–1.5 % | 8–12 % | 5–12 % | 0.9–1.1 | Engine is healthy; will fire if cranked long enough or fuel/air settles |

**The discriminators:**

- **HC ≈ 0 + O₂ ≈ 20.9 % + λ → ∞** ⇒ no fuel reaching cylinders. Engine pumping pure air.
- **HC ≈ 0 + CO₂ very low + O₂ 15–19 % + λ ≈ 1** ⇒ no compression — mixture enters but does not compress and burn.
- **HC very high + CO low + O₂ high** ⇒ no spark — fuel and air both exit unreacted (lean misfire signature *without* the engine running).
- **HC very high + CO high + O₂ low + λ rich** ⇒ flooded — too much fuel, raw fuel exits.

These fingerprints are written down in `master_gas_guide.md §3 rule 8` (cranking shape) but elaborated here for the non-starter routing.

---

## 3. Cranking RPM test

Read the RPM PID during cranking. The RPM value itself is diagnostic:

| Cranking RPM | Indicates | Action |
|---|---|---|
| 0 RPM (no signal) | CKP sensor not reporting; ECU disables injection AND ignition | Check CKP first (`master_ignition_guide.md §7`); engine cannot start until CKP is fixed |
| Normal (150–300 RPM) | Cranking system OK; problem is fuel, spark, or compression | Use gas fingerprint (§2) to narrow |
| Too fast (> 350 RPM) | Low compression — washed cylinders, broken timing belt, all-cylinder ring wear | Compression test |
| Too slow (< 100 RPM) / uneven | Weak battery; bad starter; mechanical binding (seized accessory); hydrolocked cylinder | Battery + starter draw test |

A 0-RPM PID with engine cranking is the single most common no-start cause that mimics multiple problems. **Always check CKP first** when RPM PID reads zero.

---

## 4. Quick sequential test procedure

The 4D app should walk users through this sequence in order. Each step rules out one major branch.

1. **Key-on, MIL behaviour.** If MIL stays off entirely (no bulb-check), the ECU may not be powered. Check main relay, ECU power supply, ground straps. Engine cannot start without ECU power.
2. **Read cranking RPM PID.** Zero ⇒ CKP failure, do not proceed until resolved (P0335 family).
3. **Smell test.** After 10 s of cranking, remove the oil filler cap and smell. Strong raw-fuel smell ⇒ injectors are firing and fuel is reaching cylinders ⇒ spark is the missing element. No fuel smell ⇒ fuel delivery problem.
4. **Spark test.** Disable the fuel pump (pull fuse), crank, and check spark with a spark tester on at least two cylinders. Visible blue spark across a wide gap ⇒ ignition system is delivering. Weak orange / no spark ⇒ ignition fault.
5. **Fuel pressure test.** Key-on engine-off (KOEO), measure pressure at the fuel rail. Should reach spec within ~2 seconds of key-on (pump prime). If pressure fails to build, fuel-pump or wiring issue.
6. **Injector pulse test.** Use a noid light (or test light across a disconnected injector connector) during cranking. If no pulse, check CKP/CMP signal (the ECU does not pulse injectors without crank-position sync) and ECU power.
7. **Compression test.** Only if spark and fuel are confirmed. Compression < 100 psi on multiple cylinders ⇒ timing belt jumped, severe wear, head gasket. Cross-ref `master_mechanical_guide.md §1`.

**Run gas analyser concurrently from step 2 onward** — the gas signature appears within seconds and points to the right branch faster than the manual sequence alone.

---

## 5. CKP and CMP failure mode specifics

The two crank/cam sensors are the most common non-starter root causes that *look like* fuel or spark problems.

| Sensor | Failure | DTC | Effect on starting |
|---|---|---|---|
| **CKP open / shorted** | P0335 / P0336 | Engine cranks but never fires; no RPM signal; ECU disables injection AND ignition simultaneously |
| **CKP reluctor wheel damaged** | Intermittent P0335 | Engine starts cold but stalls hot; misfire under transient |
| **CMP open** | P0340 / P0341 | Modern ECUs fall back to batch-fire and engine starts (hard); older ECUs may not start without CMP |
| **CKP/CMP correlation lost** | P0016 family | Misfire under load; starts but runs rough |

CKP failure is the *single most common* non-starter root cause that produces both no-fuel AND no-spark gas signatures simultaneously, because both injection and ignition are disabled by the same ECU logic when crank position is unknown. The 4D engine should weight CKP failure highly whenever the gas signature is "no fuel" AND cranking RPM is zero.

---

## 6. Immobiliser and security-system gates

A functioning immobiliser may permit cranking but cut fuel injector pulse or ignition. Symptoms:

- Engine cranks normally.
- No DTCs (or only an immobiliser-related DTC, often manufacturer-specific).
- No fuel injector pulse during cranking (noid light test).
- Security indicator light flashing on instrument cluster.
- Key chip or transponder failure history.

This is **not** a mechanical fault. The 4D engine should flag `immobiliser_active` and route away from mechanical / fuel-system / ignition candidates until the immobiliser is ruled out (key swap, scanner immobiliser-status PID, or dealership-level diagnostic).

The corresponding gas signature: identical to "no fuel" (§2) — HC ≈ 0, ambient O₂, λ → ∞.

---

## 7. Electronic vacuum gauge — the cranking MAP test

When mechanical compression testing is unavailable, the cranking MAP signal is a strong substitute. With the engine cranking (throttle wide-open, fuel disabled = "clear-flood mode" on most ECUs):

| Reading | Interpretation |
|---|---|
| MAP drops ~30 kPa from BARO during each compression event, regular | Healthy cylinders, valve timing intact |
| MAP drops 5–10 kPa only, regular | Low compression on all cylinders (timing belt slipped, ring wear, all-cylinder valve issue) |
| MAP drops normally on most cylinders, one cylinder pulses with smaller drop | That cylinder has compression loss |
| MAP shows a brief positive spike during compression stroke on one cylinder | Leaking intake valve on that cylinder (compression leaks back into manifold) |
| MAP completely flat | No camshaft motion (timing belt broken) — cross-ref `master_mechanical_guide.md §5` |

This test is gold when a compression gauge isn't immediately available. Cross-ref `master_air_induction_guide.md §9` (snap-throttle and idle-stability checks) and `master_mechanical_guide.md §3` (vacuum gauge interpretation).

---

## 8. Routing rules — what the 4D engine returns for non-starter cases

| Gas fingerprint | Cranking RPM | DTCs present | Engine returns |
|---|---|---|---|
| No fuel | 0 | P0335 | `Non_Starter_CKP_Failure` |
| No fuel | normal | P02xx (injector) | `Non_Starter_Injector_Circuit` |
| No fuel | normal | none | `Non_Starter_Fuel_Pump` or `Non_Starter_Immobiliser` (need to disambiguate via security light, manufacturer scan) |
| No spark | normal | P0351–P0358 | `Non_Starter_Coil_Failure` |
| No spark | normal | none | `Non_Starter_Ignition_Switch` or `Non_Starter_ECU_Output_Stage` |
| No compression | normal | none | `Non_Starter_Timing_Belt_Or_Compression` |
| Flooded | normal | none | `Non_Starter_Flooded` (clear by holding throttle WOT during cranking, or wait 15 minutes) |
| Cranking shape but slow RPM | < 100 | none | `Non_Starter_Battery_Or_Starter` (battery, starter, ground strap) |

These leaf labels need to exist in the SKG (`exhaust-analyzer-main/schema/nodes.yaml`); if they don't, the audit module flags `node_missing_non_starter_*`.

---

## 9. Cross-references

| Topic | Other master guide |
|---|---|
| Cranking-shape gases λ → ∞ | `master_gas_guide.md §3 rule 8` |
| CKP/CMP DTCs | `master_obd_guide.md §2` (P033x family) and `master_ignition_guide.md §7` |
| Fuel-pump fault patterns | `master_fuel_system_guide.md §1, §5` |
| Coil / ignition switch | `master_ignition_guide.md §3` |
| Compression test | `master_mechanical_guide.md §1` |
| Cold-start gas signature (warm-start scenarios) | `master_cold_start_guide.md §4` (don't confuse warm-up with non-starter) |

---

## 10. Citations

- SAE J1979 — Mode $01 PIDs `$0C` (RPM), `$04` (calc engine load), `$0B` (intake MAP).
- `cases/library/automotive/mix/extracted/Engine Misfire Diagnosis.md` — overlaps non-starter cranking diagnosis.
- `cases/library/automotive/mix/extracted/Interpreting OBDII Data.md` — practical fuel-status / RPM interpretation.
- Cross-ref: `master_gas_guide.md §3 rule 8` (non-combustion shape), `master_ignition_guide.md §7` (CKP/CMP), `master_mechanical_guide.md §3` (cranking-vacuum interpretation).
