# Master Mechanical Engine Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define compression testing, cylinder leak-down testing, vacuum-gauge interpretation, ring vs valve-seal differentiation, head-gasket failure-mode signatures, relative-compression electrical test, and the gas-analysis patterns that identify mechanical faults *before* disassembly. Mechanical faults are the most expensive to fix and the most often misdiagnosed — getting them right pays for itself in one job.

**Scope.** Petrol engines, all valvetrain configurations (SOHC, DOHC, OHV), all cylinder counts. VVT systems touched briefly because they affect compression and timing. Diesel high-compression engines have different absolute numbers but same mechanical principles.

---

## 1. Compression testing

The compression test measures peak cylinder pressure during cranking with all spark plugs removed and throttle held wide open.

| Result | Interpretation |
|---|---|
| **120–180 psi** (most petrol engines) | Healthy range |
| **180+ psi** | High-compression engine (some sport / race / direct-injection) — verify against manufacturer spec, not generic |
| **100–120 psi** | Marginal — investigate further; could be acceptable on older engines or after cold cranking |
| **< 100 psi** | Weak — worn rings, leaking valves, or blown head gasket on that cylinder |
| **≤ 10 % variation across cylinders** | Acceptable |
| **> 10 % variation** | Investigate the low cylinder specifically |
| **Two adjacent cylinders both low** | Suspect blown head gasket between those cylinders |
| **All cylinders evenly low (~60–80 psi)** | Timing belt jumped or ring wear across the block |

**Wet vs dry test:** Repeat the compression test after adding ~1 teaspoon of clean engine oil to the low cylinder via the spark-plug hole. Oil temporarily seals ring leakage:

- **Wet reading rises significantly (≥ 20 psi):** Rings are worn — the oil sealed the ring-to-bore gap.
- **Wet reading stays low (< 10 psi rise):** Rings are not the leak path — suspect valves, head gasket, or piston damage.

The wet test is one of the highest-leverage diagnostic discriminators in mechanical engine work.

---

## 2. Cylinder leak-down testing

Leak-down applies regulated compressed air to the cylinder at TDC compression stroke (both valves closed) and measures the percentage that escapes.

| Leakage % | Engine condition |
|---|---|
| 0–5 % | Excellent — fresh engine |
| 5–10 % | Good — healthy engine, normal ring blow-by |
| 10–20 % | Acceptable but wearing; monitor |
| 20–30 % | Significant leak — investigate now |
| > 30 % | Severe — requires teardown |

**Leakage-source identification — listen carefully:**

| Air escaping from | Fault |
|---|---|
| **Intake manifold / throttle body** | Intake valve not sealing |
| **Tailpipe / exhaust manifold** | Exhaust valve not sealing |
| **Oil filler cap / dipstick tube / PCV valve** | Worn piston rings (blow-by past rings into crankcase) |
| **Coolant / radiator (bubbles)** | Head gasket failure into a coolant passage |
| **Adjacent spark-plug hole (with that plug removed)** | Head gasket failure between cylinders |
| **External (audible hiss outside engine)** | External head gasket failure or cracked block |

Leak-down combined with the wet compression test isolates the failure to the level of "rings" or "intake valve" or "exhaust valve" or "head gasket" before any disassembly. This is the highest-leverage diagnostic pair in mechanical engine work.

---

## 3. Vacuum-gauge interpretation — the field instrument

A vacuum gauge connected to manifold vacuum provides instant engine-condition information without disassembly. **Baseline: steady 17–22 inHg at warm idle, sea level.** Deduct ~1 inHg per 1000 ft elevation.

| Vacuum-gauge pattern | Indicates | Gas correlate |
|---|---|---|
| **Steady 17–22 inHg** | Normal, healthy engine | Normal gases |
| **Steady low (10–15 inHg)** | Late ignition or valve timing; low compression overall | Low CO₂; variable HC |
| **Needle vibrates rapidly at idle, steadies at RPM** | Worn valve guides | Intermittent HC spikes at idle |
| **Regular low-to-high swing** | Head gasket blown between adjacent cylinders | Two cylinders' compression low |
| **Needle drops drastically as RPM increases** | Exhaust restriction (clogged cat, collapsed muffler) | High CO₂ at idle, collapses under load |
| **Needle drops momentarily, returns** | Sticking valve, intermittent ignition miss | Intermittent HC spikes |
| **Abnormally high reading (> 22 inHg)** | Restricted air cleaner | Low O₂ under load |
| **Slow, drifting drop** | Ignition or fuel issue (cylinder slowly fouling) | Gradual HC rise |

The vacuum gauge is the single most informative *single instrument* for mechanical-engine diagnosis. Modern equivalent: read MAP at idle and on snap-throttle (cross-ref `master_air_induction_guide.md §9`).

**Snap-throttle pass/fail criteria (§3.1):** At warm idle, snap the throttle open then immediately release. A healthy engine:
- Plunges to **0–2 inHg** (near zero) on snap.
- Rebounds to **> 25 % above the idle baseline** (e.g. idle reads 20 inHg → plunges to 1 inHg → rebounds to 25+ inHg).

Failure to plunge to near zero = throttle-plate restriction or sluggish throttle response. Failure to rebound indicates poor mechanical sealing — worn rings, valves not seating, or head-gasket leakage between cylinders. Combined with a compression and leak-down test, the snap-throttle response is the third leg of the non-invasive mechanical screen.

**Exhaust backpressure limits (§3.2):** To detect physical exhaust restriction (clogged catalyst, crushed pipe, collapsed muffler), connect a low-pressure gauge to the upstream O₂ sensor port or exhaust-manifold test port.

| Test point | Healthy limit | Action if exceeded |
|------------|--------------|-------------------|
| **Idle** | **< 1.5 psi** | Suspect restriction — proceed to 2500 RPM test |
| **2500 RPM steady** | **< 3.0 psi** | Confirmed restriction — check catalyst substrate, pipe crush, muffler collapse |
| **Snap-throttle peak** | ≤ 5 psi momentarily | Above 5 psi on snap = severe restriction |

A healthy converter shows a slight increase from idle to 2500 RPM, never exceeding 3.0 psi. Cross-ref `master_catalyst_guide.md §6` (backpressure test in P0420 work-up).

---

## 4. Ring vs valve-seal differentiation

| Test | Worn rings | Worn valve seals |
|---|---|---|
| **Compression dry** | Low on affected cylinders | May be normal (seals leak when not under cranking pressure) |
| **Compression wet** | Rises significantly | Little or no change |
| **Leak-down** | Air escapes from oil filler / dipstick (crankcase) | Air escapes from intake or exhaust port |
| **Smoke timing** | Continuous, especially under acceleration | On startup or after prolonged idle (oil pools on valve stem during sit) |
| **Vacuum gauge** | Steady low reading | Needle vibration at idle, steadies with RPM |
| **HC at idle** | High (oil burning) | High (oil burning, especially after idle) |
| **PCV blow-by check** | Excessive blow-by at oil filler | Normal blow-by |

Ring wear is **continuous** (oil burns whenever the engine runs); valve-seal wear is **transient** (oil burns at startup or after sit, then stops). This is the cleanest behavioural splitter without disassembly.

---

## 5. Head-gasket failure — seven distinct modes

A head gasket can fail in seven distinct patterns, each with different signatures. The gas analyser sees only some.

| Failure mode | Tailpipe gas signature | Other signs |
|---|---|---|
| **Combustion → coolant** | May be normal at idle; under load coolant enters chamber → white smoke; reduced CO₂ | Bubbles in radiator; pressure in cooling system; block test (chemical) positive; coolant smell from tailpipe |
| **Combustion → adjacent cylinder** | Two adjacent cylinders very low compression; uneven cranking | Vacuum gauge shows low-to-high swing; misfire on those cylinders |
| **Combustion → external** | Normal gases at tailpipe | Audible hiss/chuff from engine bay; soot streaks at gasket-line; possible oil-leak nearby |
| **Coolant → oil** | Normal gases initially | "Milkshake" oil (mayonnaise on dipstick / oil cap); low coolant level |
| **Coolant → external** | Normal gases | External coolant leak at gasket-deck interface; no oil contamination |
| **Oil → coolant** | Normal gases | Oil film in coolant reservoir; coolant smells of oil |
| **Oil → external** | Normal gases | External oil leak at block-deck joint |

The **block test** (chemical test for combustion gases dissolved in coolant) is the definitive head-gasket-to-coolant test. The 4D engine should surface `head_gasket_failure` as a candidate when:

- Compression loss is cylinder-specific (especially adjacent cylinders both low).
- Vacuum gauge shows the low-to-high swing.
- Coolant contamination is reported.
- White exhaust smoke under load (steam from coolant entering chamber).
- Block test positive.
- Co-DTC: P0301/P0302 or other adjacent-cylinder misfire pattern.

---

## 6. Mechanical-fault gas fingerprints — the analyser's view

| Mechanical fault | HC | CO | CO₂ | O₂ | λ | Compression test |
|---|---|---|---|---|---|---|
| **Worn rings (oil burning)** | High | Normal | Low–Normal | Normal | ≈ 1.00 | Low; rises with wet test |
| **Leaking exhaust valve** | High | Normal | Low | Normal | ≈ 1.00 (balanced) | Low on that cylinder |
| **Leaking intake valve** | Normal–High | Normal | Low | Low | ≈ 1.00 | Low on that cylinder |
| **Head gasket cyl-to-cyl** | High (misfire) | Normal | Low | High | ≈ 1.00 | Two adjacent low |
| **Head gasket → coolant** | Variable | Variable | Low | Variable | Variable | One or more cylinders may compression-test fine |
| **Slipped timing belt / chain** | Variable | Variable | Variable | Variable | Variable | Low across multiple cylinders; backfire possible |
| **Worn camshaft lobe** | High | Low | Low | High | ≈ 1.00 | Low on affected cylinder(s); timing chain noise |
| **Wrong valve timing (HC > 1000 + O₂ > 5)** | Very high | High | Low | Very high | < 1.0 (mild rich) | All cylinders low if global timing; one if VVT phaser |
| **Low compression all cylinders (general wear)** | Slightly elevated | Normal | Slightly low | Slightly elevated | ≈ 1.00 | All low together |

The "wrong valve timing" pattern is the classic mechanical fingerprint that fits no fuel-mixture rule (`master_gas_guide.md §8.4`) — both rich and lean side products coexist in unusual combinations because what enters the chamber gets only partially burned and exits partially.

---

## 7. Key diagnostic rule for the 4D engine — the single most leverage rule

When **λ ≈ 1.00 AND HC very high (> 500 ppm) AND CO normal AND O₂ normal**:
- The engine is in *balance* (lambda is correct).
- The combustion is *incomplete* (CO₂ is low, HC is high).
- This is a **mechanical or ignition** fault, NOT a mixture fault.

Do not pursue fuel-trim-related candidates. Route to:

- `master_ignition_guide.md §6` (ignition misfire — high HC, balanced λ).
- This guide §1–§5 (mechanical: rings, valve, head gasket).

This single rule is the most common misdiagnosis-prevention measure in petrol diagnostics. Without it, the engine returns "rich mixture" (because HC is high) for what is really a mechanical fault (where mixture is fine but combustion isn't happening).

---

## 8. Relative compression — electrical test alternative

For engines that crank but you cannot easily compression-test (engine bay tight, plugs hard to reach), the **starter-current method** approximates compression non-invasively:

- Connect a current clamp to the battery cable feeding the starter motor.
- Crank the engine and observe peaks of starter current.
- Each compression event causes a current peak (motor torque rises against the resisting cylinder).
- **Even peaks across all cylinders** ⇒ compression is uniform.
- **One peak much smaller than the others** ⇒ that cylinder has compression loss.

This is "relative compression" — it tells you if a cylinder is below the others, not the absolute psi. Cross-ref `master_non_starter_guide.md §7` (cranking MAP test, which works on similar principle).

---

## 9. VVT (Variable Valve Timing) faults

VVT phasers use oil pressure to advance or retard cam timing. Failure modes:

| Failure | Symptom | DTC | Gas signature |
|---|---|---|---|
| **Phaser stuck retarded** | Power loss; high-load misfire; low MPG | P0011 / P0014 / P0021 / P0024 family | Late-timing pattern: high HC 1000–3000, mild rich λ 0.93–0.99, modest CO bump |
| **Phaser stuck advanced** | Knock under light load; rough idle | P0011 / P0021 | High NOx; possible knock-retard active |
| **Phaser oil-control solenoid stuck** | Inability to change cam timing | P0010 / P0020 | Variable depending on stuck position |
| **Phaser sludge / lag** | Slow response; transient power loss | Often no DTC; subtle | Mild load-time-of-day variations |

Cross-ref `master_gas_guide.md §8.4` (wrong valve timing fingerprint) and v4 audit finding F2/F3 (`late_timing` pattern thresholds need correction).

---

## 10. Cross-references

| Topic | Other master guide |
|---|---|
| HC very high ignition vs mechanical | `master_ignition_guide.md §6` |
| Wrong valve timing fingerprint | `master_gas_guide.md §8.4` |
| Cranking compression test (no-start) | `master_non_starter_guide.md §7` |
| Vacuum-gauge analogue: MAP at idle | `master_air_induction_guide.md §9` |
| Head-gasket DTCs (none directly; misfire and coolant codes) | `master_obd_guide.md §5.3` |
| Catalyst meltdown caused by sustained misfire | `master_catalyst_guide.md §5` |

---

## 11. Citations

- `cases/library/automotive/mix/Diagnostic Dilemmas  The Pressures of Intake Manifold Vacuum Tests.pdf` — vacuum-gauge methodology.
- `cases/library/automotive/mix/advanced-fault-diagnosis-tom-denton.md` and `advanced-fault-diagnosis-2nd.md` — Tom Denton's textbook chapters on compression, leak-down, head-gasket diagnosis.
- `cases/library/gases/master_gas_guide.md §8.4` — wrong-valve-timing fingerprint.
- `cases/library/automotive/mix/Random-Misfire Page2.pdf` — cross-references mechanical causes for random misfire.
- Cross-ref: `master_gas_guide.md §8.7` (AFR-vs-engine-condition consequence chart — burned valves, scored cylinders).
