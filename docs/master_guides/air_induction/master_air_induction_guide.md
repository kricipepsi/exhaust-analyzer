# Master Air Induction Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define MAF (hot-wire / hot-film) physics, MAP sensor interpretation, expected airflow values, MAF contamination signatures, speed-density fallback behaviour, vacuum-leak topology by location, the P0068 correlation check, and the patterns that differentiate MAF faults from vacuum leaks. Joins `master_fuel_trim_guide.md` and `master_gas_guide.md` at the lean-misfire / vacuum-leak boundary.

**Scope.** Naturally aspirated and turbocharged petrol (1990–2020). Throttle bodies are mostly DBW (drive-by-wire) post-2003; cable-throttle vehicles obey the same airflow rules. PCV and crankcase ventilation touched only insofar as they create unmetered air paths.

---

## 1. MAF sensor physics

A hot-wire (or hot-film) MAF sensor maintains a sensing element at a fixed temperature above ambient. As airflow increases, more current is required to maintain that temperature. The sensor outputs:

- **Analog voltage (0–5 V):** Higher airflow ⇒ higher voltage. At idle ~0.7–1.0 V; at WOT ~4.0–4.5 V.
- **Digital frequency (Hz):** Higher airflow ⇒ higher frequency.
- **Grams per second (g/s):** Reported by the ECU after internal conversion via the manufacturer's transfer function.

The 4D engine reads the `maf` PID (g/s) directly when available; otherwise it reads voltage and applies a piecewise transfer.

---

## 2. MAF expected values — "Double the Displacement" rule of thumb

At idle, a naturally aspirated petrol engine draws roughly **two times the engine displacement** in grams per second (warm idle, no accessories).

| Displacement | Expected idle MAF (g/s) | Expected WOT peak (g/s) |
|---|---|---|
| 1.6 L | ~3.2 | ~64 |
| 2.0 L | ~4.0 | ~80 |
| 2.5 L | ~5.0 | ~100 |
| 3.0 L | ~6.0 | ~120 |
| 4.0 L | ~8.0 | ~160 |
| 5.0 L | ~10.0 | ~200 |

**Peak WOT rule:** approximately **forty times displacement (g/s)** for naturally aspirated. Turbocharged engines exceed this in proportion to boost ratio.

These are *screening* tests only — a MAF can pass both rules and still be contaminated, producing wrong fuel trim under specific load conditions. The decisive test is the linearity-and-response curve under snap throttle: the g/s reading should track TPS and RPM smoothly without dropouts or spikes (`Air-Induction §3` below).

**MAF scope test — idle frequency anchor:** On a hot-wire MAF, the analogue voltage output rides on a carrier frequency that a lab-scope can observe. A healthy hot-wire MAF at idle produces a signal frequency of approximately **~30 Hz**. Significant deviation from this frequency, or an erratic/intermittent frequency, indicates a failing hot-wire element or damaged sensor body. This frequency test complements the voltage-range check and can reveal a failing sensor before voltage drops out of range.

---

## 3. MAF contamination signatures — the "double whammy" pattern

Hot-wire MAF sensors are sensitive to oil and dirt deposits on the sensing wire. Contamination changes the heat-transfer characteristics:

| Contamination type | Effect on MAF reading | Resulting fuel trim pattern | Gas signature |
|---|---|---|---|
| **Dirty hot-wire (oil + dirt deposit)** | Under-reads at idle (insulating layer); over-reads at high flow (turbulence transitions) | **Positive at idle, negative under load** ("double whammy") | Lean λ at idle, rich λ under load |
| **Oil-saturated (reusable filter over-oiled)** | Always under-reads | Positive at all RPM | Lean λ, high O₂ |
| **Damaged sensing element** | Random, unpredictable | Erratic trims, possible P0101–P0103 | Unstable gases |
| **Air leak before MAF housing (e.g. cracked intake duct between filter and MAF)** | Reads low (some air bypasses sensor) | Positive (ECU under-fuels because it thinks airflow is low) | Lean λ |

The double-whammy pattern (`master_fuel_trim_guide.md §4` row 5) is the calling-card of contaminated MAF — almost no other fault produces opposite-direction trim at idle vs load.

**Cleaning vs replacing.** A contaminated MAF can be cleaned with electronics-safe MAF cleaner (CRC MAF Cleaner or equivalent — never carb cleaner, which leaves residue). One clean usually restores function; repeat contamination within months means the air filter or PCV oil-mist is the upstream cause.

---

## 4. MAP sensor fundamentals

A Manifold Absolute Pressure (MAP) sensor measures intake manifold pressure on an absolute scale (referenced to vacuum, not to ambient). At sea level:

| Engine state | Sea-level MAP | Equivalent vacuum (gauge) |
|---|---|---|
| KOEO (key-on engine-off) | ~101 kPa | 0 inHg |
| Idle (healthy) | 30–50 kPa | 15–21 inHg |
| Cruise (light load) | 50–70 kPa | 9–15 inHg |
| Decel (closed throttle) | 15–25 kPa | 22–26 inHg |
| WOT | ~95–100 kPa | ~0 inHg |

MAP decreases by approximately 3.5 kPa per 1000 ft elevation (lower atmospheric pressure). The 4D engine should read `altitude_band` from the v5 corpus context column to apply this correction.

**MAP voltage profile at key test points:**

| Test point | MAP voltage | MAP pressure | Interpretation |
|-----------|------------|--------------|---------------|
| **Key ON / engine OFF** | **~4.5 V** | Atmospheric (~101 kPa / ~30 inHg) | MAP reads full atmospheric — confirms sensor and circuit are live |
| **Warm idle** | **1.0–1.5 V** | ~20–25 inHg (67–85 kPa) | Closed throttle; manifold vacuum established |
| **Steady cruise (~2000 RPM)** | 1.6–2.2 V | Moderate vacuum | Partial throttle — MAP rises from idle baseline |
| **WOT** | 4.0–4.5 V | Near atmospheric | Throttle fully open; vacuum collapses |

The key-on/engine-off reading of ~4.5 V is the single most important MAP reference check: if this reading is outside 4.3–4.7 V with key on, the sensor, its 5 V reference feed, or its ground is faulty before any vacuum testing is attempted.

**Diagnostic from MAP alone:**
- **Higher than expected at idle** (e.g. 65 kPa instead of 35) ⇒ low manifold vacuum. Causes: vacuum leak, retarded valve timing, exhaust restriction, low compression.
- **Lower than expected at WOT** (e.g. 85 kPa instead of near-barometric) ⇒ intake restriction. Causes: clogged air filter, collapsed intake duct, throttle plate not fully opening (carbon, DBW fault).
- **KOEO MAP ≠ local barometric** ⇒ MAP sensor calibration drift or referenced incorrectly.

---

## 5. Vacuum-leak topology by location

The location of an unmetered-air leak determines its diagnostic signature. This table is the highest-leverage rule for separating vacuum-leak sub-categories:

| Leak location | Affects | Trim pattern | Gas signature | How to find |
|---|---|---|---|---|
| **Before throttle plate** | None (all air is metered if downstream of MAF) | Normal | Normal | Not actually a leak — air is metered |
| **After throttle, before all cylinders (plenum / intake gasket common)** | All cylinders equally | Both banks positive at idle, normalises at cruise | Lean λ at idle | Spray test (carb cleaner around plenum gaskets); smoke machine |
| **After throttle, one bank only (one bank's intake gasket)** | One bank | One bank positive | Bank-specific lean λ | Smoke machine; check gasket on that bank |
| **Vacuum hose to FPR / brake booster / heater valve** | All cylinders | Both banks positive | Lean λ, may worsen with brake applied (booster) | Visual inspection of vacuum lines; pinch test |
| **Injector O-ring** | One cylinder only | May not show in global trim | Lean misfire on that cylinder | Injector spray test, cylinder-balance test |
| **PCV system stuck open / cracked PCV hose** | All cylinders | Both banks positive at idle | Lean λ at idle | Pinch PCV hose at idle; trims should normalise |
| **Brake booster diaphragm tear** | All cylinders, worse with brake applied | Both banks positive when brake pressed | Lean only with brake applied | Pinch booster line; trim should normalise |
| **EVAP purge leak (post-MAF)** | All cylinders | Bank-symmetric positive | Lean λ at idle | Smoke test the EVAP system |
| **Exhaust manifold leak before pre-cat O₂** | None (this is on the *exhaust* side) | False positive (ECU adds fuel chasing false-lean O₂) | Real λ from analyser is correct; ECU λ is wrong | Cold-start chuff sound; soap-water test on manifold |

**The discriminator:** post-MAF leaks ⇒ trim positive at idle, normalises at cruise (because the leak becomes a smaller fraction of total airflow). Pre-MAF leaks (cracked airbox, broken intake duct) cause MAF under-reading instead of vacuum-leak signature.

---

## 6. MAF-fault vs vacuum-leak — the splitter

Both produce positive fuel trim at idle. The discriminator is RPM behaviour:

| | MAF under-reading | Vacuum leak (post-MAF) |
|---|---|---|
| Idle trim | Positive | Positive |
| 2500 RPM trim | Positive (persists or worsens) | Approaches normal |
| Snap throttle MAF response | Erratic / dropouts | Smooth |
| Unplug MAF (force speed-density) | Engine usually runs **better** | Engine runs the same or worse |
| MAF cleaning | Often restores function | No effect |

The "unplug the MAF" test is the cleanest field discriminator: if the engine runs better with MAF disconnected (ECU falls back to a calibrated speed-density lookup using MAP + RPM + IAT), the MAF reading was wrong. If the engine runs the same or worse, the MAF was fine.

---

## 7. P0068 — MAP/MAF correlation check

Modern PCMs run a "rationality check" on the load-calculation sensors. The MAF, MAP, and TPS should agree on what the engine is doing:

- High TPS + high MAF ⇒ MAP should be high (manifold approaching ambient under WOT).
- Low TPS + low MAF ⇒ MAP should be low (closed-throttle decel).

When they disagree, P0068 sets. Common causes:

- **Throttle-plate carbon (coking).** TPS reports the commanded angle but airflow is reduced because carbon partially blocks the throttle bore. Common on DBW vehicles after 100k km. Cleaning the throttle body resolves.
- **Intake leak between MAP sensor and the cylinders.** MAP reads atmospheric pressure rather than manifold vacuum; MAF still reads correctly.
- **MAF contaminated, MAP good.** MAF reads low; MAP reads correctly. ECU sees the conflict.
- **Cracked intake duct between MAF and throttle.** Air bypasses MAF; MAP is correct. P0068 is one of the first DTCs to fire.

The 4D engine should consume P0068 as a **strong** signal that one of the three sensors is wrong, then use the trim-pattern decision tree (`master_fuel_trim_guide.md §4`) to narrow which.

---

## 8. Inferred BARO PID

Many MAF-equipped vehicles do not have a dedicated barometric pressure sensor. The PCM calculates barometric pressure during hard WOT acceleration (when MAP approaches atmospheric and MAF is at peak flow) and stores this as an "inferred BARO" PID. The 4D app can read this PID where available.

If inferred BARO deviates from actual local barometric (verifiable via airport METAR, a known-good MAP, or altitude lookup) by more than ~3 inHg, the MAF is almost certainly mis-calibrated and providing false data. This is one of the highest-confidence single tests for MAF health on Ford/GM applications.

---

## 9. Snap-throttle and idle-stability cross-checks

| Test | Healthy result | Abnormal | Suggests |
|---|---|---|---|
| **Snap throttle, watch g/s** | Smooth rise to peak, smooth fall | Spike / dropout / hesitation | MAF damage or contamination |
| **Idle MAP stability** | Steady ±0.5 kPa | Bouncing, periodic dips | Misfire (each missed firing event drops MAP momentarily); leaking valve |
| **Idle MAF stability** | Steady ±0.2 g/s | Bouncing | Contamination, broken element, vacuum-leak fluttering |
| **Cranking MAP** | Should drop ~30 kPa from BARO during each compression event | Pulses are uneven | Cylinder-specific compression loss |

The cranking-MAP test is an electronic vacuum-gauge equivalent — see `master_mechanical_guide.md §3` for the full mechanical interpretation.

---

## 10. Citations

- Bosch Automotive Handbook — MAF / MAP physics.
- SAE J1979 — Mode $01 PIDs `$0B` (intake MAP), `$10` (MAF flow rate), `$11` (TPS), `$33` (BARO).
- `cases/library/automotive/mix/Intake-manifold-pressure-error-at-idle-Troubleshooting-in-vehicles-with-MAP-sensors_54596.pdf` — MAP at-idle troubleshooting.
- `cases/library/automotive/mix/map-sensor-troubleshooting.md` — extracted MAP reference.
- `cases/library/automotive/mix/Diagnostic Dilemmas  The Pressures of Intake Manifold Vacuum Tests.pdf` — vacuum-test methodology.
- `cases/library/automotive/mix/P0101 Mass or Volume Air Flow Circuit Range_Performance Problem...maff` — P0101 failure-mode tree.
- Cross-ref: `master_fuel_trim_guide.md §4` (vacuum-leak vs MAF row), `master_obd_guide.md §5.6` (MAF DTC mapping), `master_gas_guide.md §8.3` (lean-mixture causes — vacuum leak listed).
