# Master Catalytic Converter Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define three-way catalyst (TWC) chemistry, light-off behaviour, oxygen storage capacity (OSC), the OBD catalyst efficiency monitor, failure modes, backpressure tests, and how the 4D engine distinguishes a truly dead catalyst from "cat masking" (rich engine + healthy cat presents clean tailpipe). Defends against the most common single misdiagnosis in petrol diagnostics: replacing a fine catalyst because the engine is rich-running.

**Scope.** Petrol three-way catalysts (1990–2020). Diesel SCR/DPF/AdBlue out of scope. GPF (gasoline particulate filter) on GDI vehicles is touched in §5 but is a separate device.

---

## 1. What a three-way catalyst does

A TWC promotes two reactions simultaneously inside a narrow lambda window (0.97–1.03):

1. **Oxidation:** CO → CO₂; HC → H₂O + CO₂. Requires excess O₂.
2. **Reduction:** NOx → N₂ + O₂. Requires CO as reducing agent.

The two reactions need *opposite* mixture conditions, but the catalyst stores small amounts of oxygen on its washcoat (cerium oxide, CeO₂) so it can do both in alternation as the ECU oscillates the mixture around stoichiometric. **Outside the 0.97–1.03 lambda window** the cat cannot do all three — it will oxidise CO/HC if O₂ is plentiful (lean) but cannot reduce NOx; or it will reduce NOx if CO is plentiful (rich) but cannot oxidise the rest. This is why ECU fuel control aims at λ = 1.000.

Both reactions require the catalyst to be above **light-off temperature**, typically ~250–300 °C (482–572 °F). Below this, conversion drops sharply. Cold-start emissions are dominated by the time it takes the cat to reach light-off — modern systems use heated cats and aggressive ignition retard at start-up to shorten this window.

---

## 2. Oxygen storage capacity (OSC) — the diagnostic basis of the catalyst monitor

The cerium-oxide washcoat stores O₂ when the mixture is lean and releases it when the mixture is rich. This averaging effect **damps** the O₂ swings between upstream and downstream of the catalyst — the OBD catalyst monitor uses this damping ratio as its principal evidence.

A **healthy catalyst** has high OSC, and the post-cat sensor shows a slow, mostly stable signal (around 0.5–0.7 V on a narrowband). A **degraded catalyst** has low OSC, and the post-cat sensor begins to mirror the upstream switching activity. When the post-cat-to-pre-cat switching ratio approaches 1:1, the ECU sets P0420 (Bank 1) or P0430 (Bank 2).

OSC degrades through:
- **Thermal ageing** (gradual sintering of precious metals).
- **Poisoning** (oil → phosphorus/zinc; coolant → silicates; leaded fuel → lead; RTV silicone → silicon dioxide).
- **Mechanical damage** (impact, internal substrate cracking).

---

## 3. The catalyst efficiency monitor

The monitor compares post-cat-to-pre-cat switching frequency on a healthy cycle. In a healthy system the ratio is ~2:1 or higher (front switches twice for every one rear switch). When rear approaches front, the cat is flagged.

**Monitor enable conditions are strict:**
- ECT ≥ 70 °C (warm engine, not warm-up).
- Steady 2000–3000 RPM cruise (not idle, not WOT).
- Closed loop (`fuel_sys_status = CL`).
- No active misfire DTCs (P0300–P0312).
- No active fuel-trim DTCs (P0171/P0172/P0174/P0175).
- Time since last `codes_cleared`: at least one drive cycle.

If freeze-frame for a P0420 shows any of these conditions violated, demote the catalyst-failure candidate and surface `dtc_set_outside_enable_window`.

---

## 4. Cat masking — critical to the 4D engine

A rich-running engine with a **healthy** catalyst can present **clean tailpipe gases** (low HC, low CO at the tailpipe, near-stoichiometric tailpipe λ) while the engine itself is rich at the feed-gas level. The cat is scrubbing the evidence — using stored O₂ to oxidise the excess CO and HC into CO₂. The signature:

- **Negative LTFT** at idle and cruise.
- **Tailpipe λ within catalyst window** (0.97–1.03) despite the rich feed.
- **Tailpipe HC and CO normal** despite the rich feed.
- **Pre-cat O₂ sensor stuck rich** (steady > 0.7 V on narrowband).

The engine must surface `Catalyst_Masking_Rich` whenever this pattern is present. Without this rule, the engine will return `insufficient_evidence` for what is actually a serious rich-running condition (leaking injector, high fuel pressure, GDI HPFP failure) and let the user drive away with a damaged engine being saved temporarily by the catalyst.

The mirror situation — `Catalyst_Masking_Lean` — also exists, but it is rare (a lean engine with a healthy cat saturates the cat with O₂ and converts very little, so HC drift quickly).

---

## 5. Converter failure modes

| Mode | Cause | Diagnostic signs |
|---|---|---|
| **Overheating / meltdown** | Persistent misfire dumping raw fuel; sustained rich mixture; ignition retard runaway | Substrate physically melted; rattling sound when shaken; high backpressure; tailpipe HC very high; CO₂ collapses; cat housing discoloured |

**Misfire rate threshold for catalyst damage:** A sustained misfire rate above **1 %** of combustion events is the industry-accepted boundary above which unburned HC and free O₂ entering the catalyst create sufficient exothermic reaction to raise substrate temperature into the meltdown zone (> 1000 °C). OBD-II Type A misfire monitors are calibrated to this physical boundary. Even a single-cylinder misfire in a 4-cylinder engine at idle corresponds to a 25 % per-cylinder rate — well above the 1 % total threshold. Cross-ref `master_ignition_guide.md §6.1`.
| **Poisoning — phosphorus/zinc** | Oil burning into exhaust over months | Gradual P0420 onset; substrate visually coated; no acute symptom |
| **Poisoning — silicon (RTV sealant)** | RTV silicone used on engine seals near intake | Sudden P0420 within days/weeks of the silicone application |
| **Poisoning — lead** | Leaded fuel (now rare, occurs in some markets) | Sudden permanent P0420; cat replacement only fix |
| **Physical damage** | Road impact; broken welds; cracked housing | External exhaust leak; rattling; backpressure may be normal |
| **Normal ageing** | Gradual OSC depletion | Slow P0420 onset over 150,000+ km; substrate intact |
| **GPF clogging (GDI only)** | Particulate buildup, missed regen | Power loss under load; high backpressure; P244A or P2459 family |

**Substrate visual:** A healthy cat has a clean honeycomb. A melted cat shows discoloured / glassy / collapsed honeycomb when looked through. A clogged GPF shows soot. Field tests:

- **Backpressure test:** ≤ 1.5 psi at idle, ≤ 2.5 psi at 2500 RPM. Above these, suspect substrate restriction.
- **IR thermometer:** Outlet weld-ring should be 20 °C+ hotter than inlet weld-ring at operating temperature. If outlet ≤ inlet, the cat is doing nothing.
- **Mode $06 cat monitor results:** Read the catalyst monitor's actual test value and compare to the manufacturer's threshold. If the test value is within 10 % of threshold, cat is borderline; if 50 %+ from threshold, cat is genuinely failed.

---

## 6. Diagnosis flow for P0420 / P0430

1. **Rule out feed-gas problems first.** No active P0300–P0312, fuel trims within ±10 %, no exhaust leak before the rear sensor, no recent codes-cleared event. Per `master_obd_guide.md §5.4`, a misfire or lean-trim DTC invalidates the catalyst test.
2. **Verify monitor enable conditions** held during the freeze frame. If freeze frame says ECT < 70 °C, fuel_sys_status = OL, or RPM not steady, the test was invalid.
3. **Backpressure test** at idle and 2500 RPM. Physical pass/fail limits: **idle < 1.5 psi; 2500 RPM < 3.0 psi** (snap-throttle peak ≤ 5 psi). Above 3.0 psi at 2500 RPM = confirmed substrate restriction — replace converter. Cross-ref `master_mechanical_guide.md §3.2`.
4. **IR temperature delta.** Outlet ≥ 20 °C above inlet → cat is converting. Outlet ≤ inlet → dead.
5. **Mode $06 catalyst monitor data.** Far below threshold = real fail. Just below = borderline.
6. **Check OEM TSBs.** Some manufacturers issued reflash bulletins that resolve false P0420 without hardware change.
7. **Only after 1–6 confirm a real failure**, consider replacement.

---

## 7. Reference emission values at the tailpipe (cross-ref `master_gas_guide.md §8.6`)

| Condition | CO | CO₂ | HC | O₂ | Lambda |
|---|---|---|---|---|---|
| With cat (good) | ≤ 0.5 % | ≥ 14.5 % | ≤ 50 ppm | ≤ 0.5 % | 0.97–1.03 |
| Without cat | ≤ 1.5 % | ≥ 13 % | ≤ 250 ppm | 0.5–2 % | 0.90–1.10 |
| Pre-cat (efficient feed gas) | ~0.6 % | ~14.7 % | ~100 ppm | ~0.7 % | 1.00 |
| Post-cat (efficient) | ~0.1 % | ~15.2 % | ~15 ppm | ~0.1 % | 1.00 |

The cat reduces HC roughly an order of magnitude and CO similarly when working. Tailpipe HC > 50 ppm with-cat is suspect; tailpipe HC > 250 ppm with-cat strongly suggests cat failure or feed-gas breakthrough.

---

## 8. The "false P0420" cluster

The 4D engine must surface `false_P0420_suspected` when the following co-occur:

- Active P0420 (or P0430).
- No misfire DTCs.
- Trims within ±10 %.
- IR temp test passes (outlet > inlet by 20 °C).
- Tailpipe gases within with-cat reference values.
- No exhaust leak detected.

In this cluster, the catalyst is fine; the monitor is glitching. Common causes:
- Aged but functional rear sensor.
- ECU calibration drift on certain make/model years (TSBs exist for many).
- Slightly degraded but in-spec cat that the monitor's tight threshold flags.

---

## 9. Cross-references

| Topic | Other master guide |
|---|---|
| Lambda window 0.97–1.03 | `master_gas_guide.md §8.5` (catalyst window) |
| Pre-cat O₂ stuck rich and cat masking | `master_o2_sensor_guide.md §6` |
| Misfire DTC invalidates cat test | `master_obd_guide.md §5.3` and `master_ignition_guide.md` |
| Fuel trim DTC invalidates cat test | `master_fuel_trim_guide.md §3` |
| Rich mixture causes from §1 | `master_fuel_system_guide.md §3` |
| Exhaust leak false-lean confounder | `master_gas_guide.md §8.5` (5 % air leak rule) |

---

## 10. Citations

- `cases/library/gases/Understanding Catalitic Converters.md` — existing in-repo reference, base of this guide.
- SAE J1979 — Mode $06 catalyst monitor PID definitions.
- US EPA OBD-II catalyst monitor guidance documents.
- `cases/library/automotive/mix/Seeing The Whole Picture  The Importance of Loop Status - iATN.pdf` — closed-loop validation for catalyst monitor.
- Cross-ref: `master_gas_guide.md §5` (catalyst-aware caveats), `§8.6` (reference emission values), `§8.7` (AFR consequence chart).
