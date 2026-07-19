# Oil-Burn Test Signatures — Citroën 5FR (EP6CDT 1.6 THP, turbo + GDI)

**Vehicle:** `VF7SA5FR8AW511081` · Citroën · engine **5FR / EP6CDT** · 1598 cc I4 · **turbocharged** (TwinScroll K03) · **direct injection (GDI)** · EURO 5 · idle ≈ 700 rpm · high idle ≈ 2500 rpm · target λ = 1.00.
**ECU:** Bosch **MED17.4** with **secondary (post-cat) fuel-trim control** on the downstream sensor.
**Sensor config (corrected):** *Modern Standard* — **wideband upstream (S1)** + **narrowband downstream (S2)**. Upstream reports continuous **λ**; downstream reports **voltage (0.1–0.9 V)** *and* drives **post-cat fuel trim (B1S2 STFT/LTFT)**. (`5fr.md`, `O2NBvsWB.md`.)
**Purpose:** five oil-consumption cases on the **same vehicle**, each with a distinct **gas** set *and* a distinct **OBD** set (now including B1S2), tuned to this turbo-GDI engine, to drive the diagnostic end-to-end.
**Source chemistry:** `planning/OilburnCases.md` §P_NEW_09–13. **Rules:** `mechanical_wear.json` (MW-001/002/003/008/009). **Sim oracle:** `planning/sim/oil_burn_5fr_sim.py` (5/5 green).
**Status:** numbers authored & checked against the simulation. Real-pipeline routing depends on **T-VIN-FIX-3** (decoder) + **PCT-1…PCT-10** (post-cat trim build).

---

## 0. Baseline & how the post-cat loop reads oil

GDI + turbo healthy idle: CO ≈ 0.10 %, CO₂ ≈ 14.8 %, O₂ ≈ 0.4 %, HC < 50 ppm, **upstream λ ≈ 1.00**, **downstream ≈ 0.65 V**, STFT/LTFT (S1) within ±5 %, **B1S2 ≈ 0 to −2 %** (downstream holds only ±1–2 % authority when healthy).

```
 oil enters exhaust → O2 consumed at downstream sensor → S2 reads FALSE-RICH (high V)
   → ECU's secondary loop PULLS FUEL → NEGATIVE post-cat trim (B1S2)
   while the WIDEBAND upstream may still read ~λ 1.00 (combustion itself ok)
```

The *pattern* of that negative B1S2 trim is the per-failure fingerprint (steady / transient / divergent / fuel-cut).

---

## 1. Gas signatures — 5 cases (low idle 700 / high idle 2500)

| # | Case (tier_2 symptom) | Target | Idle | CO % | CO₂ % | O₂ % | HC ppm | NOx ppm | λ |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **Worn piston rings** (blue_smoke_under_acceleration) | MW-001 | low | 0.15 | 14.2 | 0.5 | 150 | 45 | 1.002 |
| | | | high | 0.85 | 13.1 | 0.7 | 380 | 180 | 0.985 |
| 2 | **Worn valve stem seals** (blue_smoke_on_cold_start_clears) | MW-002 | low | 0.95 | 13.0 | 0.3 | 450 | 35 | 0.962 |
| | | | high | 0.10 | 14.7 | 0.4 | 60 | 75 | 1.001 |
| 3 | **Blown head gasket (oil→cyl)** (oil_loss_no_visible_smoke) | MW-003 | low | 0.65 | 11.0 | 2.6 | 340 | 18 | 1.085 |
| | | | high | 1.15 | 11.0 | 2.1 | 440 | 38 | 1.055 |
| 4 | **PCV stuck open** (oil_loss_no_visible_smoke) | MW-008 | low | 1.90 | 11.8 | 0.2 | 610 | 25 | 0.925 |
| | | | high | 0.45 | 13.8 | 0.4 | 170 | 105 | 0.988 |
| 5 | **Turbo turbine-seal leak** (blue_smoke_after_idle) | MW-009 | low | 0.07 | 14.5 | 0.5 | 720 | 28 | 1.000 |
| | | | high | 0.09 | 14.6 | 0.4 | 130 | 80 | 1.002 |

---

## 2. OBD signatures — wideband upstream + narrowband downstream + post-cat trim

### 2a. O₂ sensor readings (idle)

| # | Target | Upstream λ (WB) low → high | Downstream S2 voltage | Reads as |
|---|---|---|---|---|
| 1 | MW-001 | 1.002 → 0.985 | 0.80 V (false rich) | mild persistent rich at S2 |
| 2 | MW-002 | 0.962 → 1.001 | 0.85 V at idle, settles | plume on tip-in, cleans |
| 3 | MW-003 | 1.085 → 1.055 (false lean) | 0.28 V (lean/erratic) | coolant raw-O₂ at S2 |
| 4 | MW-008 | 0.925 → 0.988 | 0.85 V (false rich) | heavy rich at idle |
| 5 | MW-009 | 1.000 → 1.002 (stoich) | 0.80 V (false rich) | clean combustion, rich S2 |

### 2b. Fuel trims + load (idle), with the post-cat signature

| # | Target | STFT S1 % | LTFT S1 % | **STFT B1S2 %** | **LTFT B1S2 %** | DFCO B1S2 % | MAF g/s | MAP kPa | ECT °C | Post-cat signature |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | MW-001 | −2 | +5 | −6 | **−9** | −3 | 3.2 | 36 | 92 | **FIXED_NEGATIVE** (steady neg LTFT-B1S2, all RPM) |
| 2 | MW-002 | −8 | −3 | **−13** | −4 | −2 | 3.0 | 34 | 92 | **TRANSIENT_NEGATIVE** (sharp neg STFT-B1S2 at idle/tip-in) |
| 3 | MW-003 | +12 | +10 | +4 | +2 | 0 | 3.4 | 41 | **99** | NEUTRAL — gas + **ECT>95** drive MW-003 |
| 4 | MW-008 | **+15** | +8 | **−16** | −9 | −4 | 4.5 | 45 | 92 | **DIVERGENT** (upstream **+**, downstream **−**) |
| 5 | MW-009 | +1 | 0 | −7 | −5 | **−14** | 3.2 | 36 | 92 | **DFCO_NEGATIVE** (B1S2 pinned rich during fuel-cut) |

*Evidence the rule gates on:* #1 LTFT-B1S2 fixed-negative · #2 STFT-B1S2 transient-negative · #3 ECT > 95 + gas · #4 divergent split (S1 + / B1S2 −) · #5 DFCO B1S2 ≤ −10. Trim band reference: healthy ±~10 %, ±25 % extreme; B1S2 ≈ 0 when downstream isn't contributing.

---

## 3. Sensor-config coverage (the "both O₂ types" requirement)

The data model must carry the sensor at **each position** plus the trim role (not a single `o2_type`). Three real configs exist (`O2NBvsWB.md`):

| Config | Upstream | Downstream | Correction method | Example |
|---|---|---|---|---|
| Traditional | narrowband | narrowband | switch/switch | older cars |
| **Modern Standard ← 5FR** | **wideband** | **narrowband** | voltage-threshold integrator | most modern GDI |
| Premium | wideband | wideband | OSC mass-balance model | BMW / Mercedes / Subaru |

**Factory 5FR = wideband upstream + narrowband downstream + `downstream_trim_role = SECONDARY_FUEL_TRIM`.**
Coverage runs: (A) the factory **WB+NB** config as primary; (B) optionally the **WB+WB** premium variant as a test override to exercise the OSC path. (The old "NB upstream" assumption is dropped.)

> **Data fix (PCT-4):** `vref.db` currently stores a single `o2_type='NB'`, wrong for this engine. Replace with `upstream_o2_type=WIDEBAND`, `downstream_o2_type=NARROWBAND`, `downstream_trim_role=SECONDARY_FUEL_TRIM`.

---

## 4. Routing status

With post-cat trim modelled, **all 5 route** — proven in the simulation (`oil_burn_5fr_sim.py`, 5/5). Post-cat trim is what unblocks the two cases gas chemistry alone could not separate:

| # | Target | Discriminator |
|---|---|---|
| 1 | MW-001 | WORN_PISTON_RINGS chem + **FIXED_NEGATIVE** B1S2 |
| 2 | MW-002 | WORN_VALVE_SEALS chem + **TRANSIENT_NEGATIVE** B1S2 |
| 3 | MW-003 | COOLANT_LEAK_INTERNAL chem + **ECT > 95** |
| 4 | MW-008 | POA_SIGNATURE + **DIVERGENT** split trim |
| 5 | MW-009 | POA_SIGNATURE + **DFCO_NEGATIVE** B1S2 (+ stoich λ, low CO) |

Real-pipeline parity requires **PCT-1…PCT-10** (post-cat trim build) on top of **T-VIN-FIX-3** (decoder). Until then the simulation is the reference oracle.

---

## Sources

- `labs/vinlab/tasks/5fr.md` — Bosch MED17.4 post-cat fuel-trim strategy + per-mode B1S2 signatures
- `labs/vinlab/tasks/O2NBvsWB.md` — upstream/downstream sensor configs + secondary-loop logic
- [carsart.net — EP6CDT specs](https://carsart.net/en/engine/EP6CDT) · [motor-doctor — C4 1.6 THP 5FV lambda sensors](https://www.motor-doctor.co.uk/o2-sensor/citroen/c4/c4-ii-b7/467-1-6-thp-155) · [Prince engine — Wikipedia](https://en.wikipedia.org/wiki/Prince_engine)
- Fuel-trim reference (STFT ±25 band; B1S2 99.2 % = non-contributing): [Ross-Tech Fuel Trim Info](http://wiki.ross-tech.com/index.php/Fuel_Trim_Info), [Bosch MED17.4 — autotuner](https://www.autotuner.com/blogs/news/bosch-med17-4), [aussiefrogs 1.6 THP STFT thread](https://www.aussiefrogs.com/forum/index.php?threads/high-short-term-fuel-trim-on-1-6-thp.143583/)
- `planning/OilburnCases.md`, `labs/comlab/registry/rules/mechanical_wear.json`
