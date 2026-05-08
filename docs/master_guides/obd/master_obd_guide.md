# Master OBD-II / DTC Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for decoding OBD-II powertrain DTCs — what each P-code structure means, which monitor sets it, what freeze-frame data attaches, and how the engine maps codes to fault hypotheses. Rows in the CSV cite the rules below; this document is the citation target.

**Scope.** Petrol only, OBD-II era (1996–2020). Generic codes (P0xxx) take priority over manufacturer-specific (P1xxx) for the engine's reasoning. Proprietary modes ($22, $23) are out of scope; only Mode $03 (stored DTCs), $07 (pending), $0A (permanent) are consumed.

---

## 1. DTC format

Every OBD-II DTC is a 5-character alphanumeric string per SAE J2012 / ISO 15031-6:

```
[System][Standard][Sub-system][Fault][Fault]
   P        0        1         7  1
```

| Position | Meaning | Values |
|---|---|---|
| 1 — System | Vehicle system | `P` Powertrain, `B` Body, `C` Chassis, `U` Network |
| 2 — Standard | Generic vs manufacturer | `0` SAE/Generic (all makes), `1` Manufacturer-specific, `2` mixed (3rd char defines), `3` 3000–3399 manufacturer / 3400–3999 generic |
| 3 — Sub-system | Powertrain sub-system | See §2 |
| 4–5 — Fault | Specific fault, often cylinder-indexed | 00–99 |

The 4D engine treats only `P0xxx`, `P2xxx`, and `P34xx`–`P39xx` as portable across vehicles. `P1xxx` and `P30xx`–`P33xx` are manufacturer-specific and require make/model context to decode — flag as `dtc_manufacturer_specific` and demote until the make is known.

---

## 2. Third-character sub-system index (Powertrain)

| 3rd digit | Sub-system | Key DTC families relevant to the 4D engine |
|---|---|---|
| `0` | Fuel & Air Metering, Auxiliary Emission Controls | P0100–P0104 (MAF), P0110–P0118 (IAT/ECT), P0130–P0167 (O₂ sensors) |
| `1` | Fuel & Air Metering | P0171–P0175 (fuel trim lean / rich) |
| `2` | Injector Circuit (Fuel or Air) | P0201–P0212 (injector circuit per cylinder) |
| `3` | Ignition System & Misfire Detection | P0300–P0312 (misfire), P0325–P0334 (knock), P0335–P0349 (CKP/CMP), P0350–P0362 (coil) |
| `4` | Auxiliary Emission Controls | P0400–P0408 (EGR), P0420–P0434 (catalyst), P0440–P0457 (EVAP), P0480–P0498 (cooling fan, AIR) |
| `5` | Vehicle Speed, Idle Control | P0500–P0503 (VSS), P0505–P0507 (IAC) |
| `6` | Computer Output Circuit | P0601–P0606 (ECM internal), P0620–P0635 (alternator/PCM relays) |
| `7`–`9` | Transmission | Out of scope for petrol-engine fault hypothesis |

---

## 3. DTC type — MIL illumination class

Only Types A and B matter to the 4D engine because they illuminate the MIL.

- **Type A — Emissions-critical.** MIL illuminates immediately on first detection. Misfire codes (P0300–P0312) and lean/rich fuel-trim codes (P0171/P0172/P0174/P0175) are Type A. **Flashing MIL** during active misfire signals a catalyst-damaging condition — the engine must surface `catalyst_damage_imminent` whenever the user reports flashing MIL plus a P030x.
- **Type B — Emissions-related.** MIL illuminates on the second consecutive drive cycle the fault recurs. Most EVAP codes (P0442, P0455, P0456) and catalyst codes (P0420/P0430) are Type B.
- **Types C and D.** Do not illuminate MIL; not engine-relevant for the 4D corpus.

---

## 4. Monitors — what triggers each DTC family

| Monitor | What it watches | Typical enable conditions |
|---|---|---|
| **Misfire** | CKP tooth-period variation; samples every 200 (Type A) or 1000 (Type B) revolutions | Continuous; ECT > 60 °C, RPM 600–6000, no fuel cut |
| **Fuel system** | STFT/LTFT departure from stoichiometric target | Closed loop, ECT ≥ ~70 °C, steady cruise |
| **Catalyst efficiency** | Switch-frequency ratio of post-cat O₂ vs pre-cat | ECT ≥ 70 °C, steady 2000–3000 RPM, no misfire DTC, fuel trims within ±10 % |
| **O₂ sensor** | Response time, switching frequency, heater resistance | Closed loop, sensor at operating temperature |
| **EVAP** | Tank pressure decay during purge and sealed phase | Cold start needed for some tests; ECT < 40 °C at start, tank 15–85 % full |
| **EGR** | Expected vs actual MAP/MAF change during EGR command | Decel or steady cruise; throttle-off rapid commanded EGR open |
| **Comprehensive Component (CCM)** | Sensor electrical / range checks | Continuous; key-on |

The engine must respect the **monitor enable conditions** — a P0420 set during a cold-start drive cycle is suspect because the catalyst monitor enable usually requires ECT ≥ 70 °C. If the freeze-frame ECT shows < 70 °C, flag `dtc_set_outside_enable_window` and demote the catalyst-failure candidate.

---

## 5. DTC-to-cause mapping — the rule the engine uses

DTCs are **evidence channels**, not diagnoses. A DTC says *what the ECU measured*, which may be a symptom rather than the root cause. The mapping rules are:

### 5.1 Lean codes (P0171 / P0174)

The ECU has maxed positive fuel trim — typically LTFT ≈ +25 %. Possible causes, in priority order per `cases/library/automotive/mix/extracted/Fuel Trim Info - Ross-Tech Wiki.md`:

- **Both banks lean (P0171 + P0174):** Vacuum leak post-MAF, low fuel pressure, contaminated MAF reading low, exhaust leak before pre-cat O₂ sensor, stuck-open EGR.
- **One bank lean only (P0171 or P0174):** Intake gasket leak on that bank, single clogged injector on that bank, single bank fuel-rail issue on V-engines.

### 5.2 Rich codes (P0172 / P0175)

LTFT ≈ −25 % sustained. Possible causes:

- **Both banks rich:** High fuel pressure, contaminated MAF reading high, stuck-open EVAP purge, faulty ECT (stuck cold), saturated charcoal canister.
- **One bank rich only:** Leaking injector on that bank, fuel-rail pressure imbalance.

### 5.3 Misfire codes (P0300 vs P0301–P0312)

- **P0300 (Random):** Multiple cylinders or rotating misfire. Points to fuel/air or common ignition (coil pack, distributor, fuel pressure, vacuum leak, stuck-open EGR at idle).
- **P0301–P0312 (Cylinder-specific):** Plug, coil, injector, or compression on that hole. The number after `P030` is the cylinder index (1–12).

The engine must combine the misfire DTC with gas signature per `master_gas_guide.md §3 rule 5`: high HC + low CO + high O₂ on a single-cylinder misfire. If gases say lean and DTC says random, suspect a vacuum leak feeding lean misfire.

### 5.4 Catalyst codes (P0420 / P0430)

Catalyst oxygen-storage below threshold. **Do NOT default to cat replacement.** Confirm in order:

1. No active P0300–P0312 (a misfire dumps raw fuel and overwhelms the cat).
2. Fuel trims within ±10 % at idle and cruise.
3. No exhaust leak before or near the rear sensor (false-lean rear sensor mimics dead cat).
4. `master_gas_guide.md §5 catalyst-aware caveats` — gases at idle are not the test; the cat fails on the drive-cycle monitor.

### 5.5 O₂ sensor codes (P0130–P0167)

- **P0131 / P0151 (low voltage):** Sensor stuck lean. Causes: exhaust leak before sensor, sensor poisoned, signal short to ground.
- **P0132 / P0152 (high voltage):** Sensor stuck rich. Causes: silicone poisoning (RTV sealant), short to voltage.
- **P0133 / P0153 (slow response):** Lazy sensor — cross-counts < 8 per 10-second window at 2500 RPM.
- **P0134 / P0154 (no activity):** Sensor not switching. Could be cold (ECT low), heater fault, or open circuit.
- **P0135 / P0141 / P0155 / P0161 (heater circuit):** Heater current draw out of spec.

### 5.6 MAF codes (P0100–P0104)

- **P0101 (range/performance):** MAF reading is within electrical bounds but does not correlate with TPS, RPM, MAP. Almost always contamination or air leak before MAF.
- **P0102 (low input) / P0103 (high input):** Electrical fault or extreme contamination. See `cases/library/automotive/mix/P0101 Mass or Volume Air Flow Circuit Range_Performance Problem...maff` for the failure-mode tree.

### 5.7 EVAP codes (P0440–P0457)

- **P0442 (small leak):** Equivalent to a 0.5 mm hole. Often loose fuel cap.
- **P0455 (large leak):** Gross leak — fuel cap off, cracked filler neck.
- **P0446 (vent valve):** Vent valve circuit fault.
- **P0455 + P0457:** Cap loose or cap seal degraded.

### 5.8 EGR codes (P0400–P0408)

- **P0401 (insufficient flow):** Carbon-clogged EGR passage, stuck-closed valve, vacuum supply lost.
- **P0402 (excessive flow):** Stuck-open EGR. Idle gas signature: high HC, low CO, high O₂, low NOx (per `master_gas_guide.md §3 rule 6`).

---

## 6. Pending vs stored vs permanent

The engine must distinguish DTC severity by where it was read:

| Source | What it means | Engine treatment |
|---|---|---|
| **Mode $03 (stored)** | Confirmed DTC — failed twice (Type B) or once (Type A). MIL is on. | Full weight in fault inference. |
| **Mode $07 (pending)** | Failed once but not yet confirmed. MIL may not be on. | Half weight — surface as "pending" hint, not a confirmed fault. |
| **Mode $0A (permanent)** | DTC that cannot be cleared by scan tool — only by drive-cycle confirmation. Indicates the ECU saw a real fault recently. | Full weight; treat as authoritative even if user "cleared codes". |
| **Codes_cleared = true** | User has cleared codes recently. STFT/LTFT have reset. | Demote fuel-trim-derived faults until trims have re-learned (≥ 1 drive cycle). |

---

## 7. Freeze-frame attachment

When a DTC sets, the ECU snapshots a freeze-frame containing (per SAE J1979): RPM, calc_load, ECT, MAP/MAF, STFT, LTFT, IAT, throttle, vehicle speed, fuel-system status, ignition advance. The 4D engine reads freeze-frame fields from the v5 CSV columns prefixed `ff_*`.

**Rules for using freeze frame:**

- **Single-frame priority:** ECU stores freeze frame only for the *first* emissions-critical DTC of the session. A later P0420 freeze-frame overwrites only if no earlier emission DTC is present.
- **Mismatch with live PIDs:** if freeze frame says `ECT = 35 °C` but live ECT now reads 90 °C, the fault was set during warm-up — the conditions that triggered it may no longer be present. Flag `dtc_set_during_warmup` and gate cold-start enrichment per `master_cold_start_guide.md §4`.
- **Closed-loop check:** `ff_fuel_status` should equal `closed_loop` for fuel-trim and catalyst DTCs to be valid. If freeze-frame fuel status is `open_loop`, the trims at that moment were invalid and the DTC is suspect.

---

## 8. Cross-reference map — which other master guides consume DTCs

| DTC family | Other master guide(s) the engine must also consult |
|---|---|
| P0100–P0104 (MAF) | `master_air_induction_guide.md` §1–§3 |
| P0110–P0118 (IAT/ECT) | `master_cold_start_guide.md` §6 (ECT bias) |
| P0130–P0167 (O₂) | `master_o2_sensor_guide.md` §6 (sensor bias rule) |
| P0171/P0174 (lean), P0172/P0175 (rich) | `master_fuel_trim_guide.md` §4 (decision tree) |
| P0201–P0212 (injector) | `master_fuel_system_guide.md` §1–§3 |
| P0300–P0312 (misfire) | `master_ignition_guide.md` §1, §6 |
| P0335–P0349 (CKP/CMP) | `master_non_starter_guide.md` §5 |
| P0400–P0408 (EGR) | `master_gas_guide.md` §3 rule 6 |
| P0420/P0430 (catalyst) | `master_catalyst_guide.md` §3, §6 |
| P0440–P0457 (EVAP) | `master_fuel_system_guide.md` §4 |
| P0601–P0606 (ECM internal) | Treat as ECU fault; do NOT demote other candidates — ECU may be hallucinating |

---

## 9. Sanity rails — common false-positive traps

- **A single MIL with a single DTC is rarely the whole story.** Always check pending codes (Mode $07) — they often reveal the chain.
- **A P0420 with no fuel-trim DTC and no misfire DTC** is the only configuration where catalyst replacement is even plausible. Any other configuration points to a *cause* that will reappear after cat replacement.
- **Codes cleared + no DTCs now** ≠ healthy. The 4D engine should never use "no DTCs" as positive evidence — only as absence of negative evidence.
- **Generic vs manufacturer code overlap.** Some manufacturers re-use generic ranges with different meanings. When in doubt, prefer the generic interpretation and flag `dtc_manufacturer_specific_overlap`.

---

## 10. Citations

- SAE J2012 / ISO 15031-6 — DTC numbering standard.
- SAE J1979 — Mode $01–$0A definitions and freeze-frame data.
- `cases/library/automotive/mix/extracted/Generic OBD II DTC CODES P0100 to P0199.md` … `P0900 to P0999.md` — full P-code definitions, 4D-app's primary lookup.
- `cases/library/automotive/mix/extracted/Interpreting OBDII Data.md` — practical DTC interpretation patterns.
- `cases/library/automotive/mix/extracted/Fuel Trim Info - Ross-Tech Wiki.md` — fuel-trim DTC mapping cross-check.
- `cases/library/automotive/mix/Seeing The Whole Picture  The Importance of Loop Status - iATN.pdf` — closed-loop / open-loop DTC validity.

*Cross-check: where this guide and `master_gas_guide.md` disagree, gas chemistry (`master_gas_guide.md`) wins per the Truth-vs-Perception override (`PRD_4D_App.md` §5).*
