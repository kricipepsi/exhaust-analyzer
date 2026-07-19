---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "non-start-routing"
implements:
  - "labs/dtclab/dtclab/config/routing_tag_map.yaml"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py DTCRoutingTag routing"
drift_guards:
  - "labs/dtclab/tests/unit/test_routing_tag_mapper.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/10_nonstart_diagnostics.md"
---
# 10 — Non-start diagnostics & extended PID profiles

Sources: `cases/NonStartCases.md`, `DtcDoc.md` (30 era cases),
`Advanced Diagnostic Correlation … Powertrain Control Systems_*.md`, and Denton
§5.2.1 via ANALYSIS §A6. See `00_INDEX.md`.

Non-start cases need a different approach: no gas sample can be taken and no
closed-loop PIDs are active. DTCLab's role is limited to cranking-speed check,
voltage threshold, immobiliser/security codes, and the Mode `$06` baseline from
the prior drive session.

---

## 10.1 Non-start era classification

| Era | Date range | Diagnostic approach |
|---|---|---|
| Early OBD-II | 1990 – 2000 | Few DTCs; rely on freeze frame and prior-session monitors; ECU memory often lost on battery disconnect; pre-CAN manufacturer-specific Mode `$06` TIDs |
| CAN Bus / Security | 2000 – 2010 | PATS/immobiliser codes (B1600–B1602, B3055, P1260) block crank or fuel; ECU U-codes common; standardized MIDs |
| GDI / late CAN | 2005 – 2010 | HPFP, GDI rail-pressure, EGR carbon, cam-phaser codes; multiple ECUs over CAN — U-code storms from ECU power-down |

---

## 10.2 Non-start validity checks

| Check | Pass | Fail action |
|---|---|---|
| Cranking RPM | ≥ 100 RPM | < 100 → battery/starter fault before further DTC analysis |
| Battery voltage at crank | ≥ 9.6 V | < 9.6 → charging/battery fault; all DTCs suspect |
| Mode `$06` baseline | No `CRITICAL_FAIL` on MID `$A1`–`$A9` | Active misfire history rules out cranking fault |
| Immobiliser DTCs | No B16xx, B3055, P1260, manufacturer PATS | Immobiliser fault — no-fuel or no-spark by design |

---

## 10.3 Non-start signature patterns (DTC ↔ FF ↔ Mode `$06`)

Distilled from the 30 `DtcDoc.md` era cases. The diagnostic value is the
*combination* of code, freeze-frame snapshot, and the Mode `$06` monitor state at
the failed crank. Representative patterns:

| Root cause | DTC | Freeze-frame tell | Mode `$06` tell |
|---|---|---|---|
| Immobiliser / security lockout (Passlock, PATS, Passkey) | P1626, B2960, B1600/P1260, B3055 | Cranking RPM 150–180, OL-Fault, security active | MID `$00`/`$A1` "Incomplete" — monitors aborted by lockout |
| Crank/cam sensor thermal or solder failure | P0335, P0340, P1604 | **Engine speed 0 RPM while physically cranking** | Misfire MID `$A1` "Incomplete" (no speed profile) |
| Total power loss (relay/TIPM/fuse solder) | none stored ("No Communication") | none available | all MIDs "Incomplete"/"No Comm" |
| Fuel pump / FPDM / pump-fuse loss | P0171 (pending), P1233, P025A, P0230 | OL-Fault, low system voltage on long crank | fuel-system MID `$81` over max limit (+28% etc.) |
| Massive unmetered vacuum leak (PCV collapse) | P2187 | **MAP ≈ 98 kPa at crank** (expected 25–35) | fuel-system MID `$81` over max (+32%) |
| MAF short to ground | P0102 | MAF 0.0 g/s, calc load 0% | comprehensive MID `$00` failed |
| EGR stuck open cold | P1404 | MAP ≈ 28 inHg (no vacuum), rough crank | EGR pre-CAN TID `$41` far over max |
| FPR diaphragm rupture (flooding) | P0172 | STFT −25%, heavy fuel chugging | fuel-system TID `$81` under min (−25%) |
| Cam-timing chain jump | P0016 | VVT phase deviation 18.5° (max 6°) | VVT MID `$31` correlation over limit |
| O₂/AF heater cold-start lockout | P0135 | ECT very cold, OL | O₂-heater MID `$05` heater-current 0.0 A (min 0.8) |
| GDI HPFP / spill-valve / rail-sensor | P0087, P0090, P0191 | rail pressure stuck at low-feed value (62–75 PSI), or falsely high (2800 PSI) | fuel-system MID `$81` TID `$02` failed |
| Throttle correlation fail-safe | P0121, P1602, P2135 | TPS1/TPS2 voltages out of mirrored correlation | TAC/comprehensive MID `$00` failed |
| GDI injector short / cold-start carbon | P0200/P0201, P0300, P050D | OL-Fault or cold rough-run-then-stall | misfire MID `$A1` per-cyl counts rising at crank |

### 10.3.1 Catalyst damage in non-start

If the vehicle was running with a flashing MIL (a Type A misfire — chunk `06`)
before the no-start event, the catalyst may have been flooded by unburned fuel.
On restart, expect `CRITICAL_FAIL` on Mode `$06` MID `$21`. Flag
`catalyst_damage_imminent` and escalate to `CRITICAL_IMMEDIATE_STOP`.

---

## 10.4 Extended PID profiles — curb idle vs. stress idle

Curb idle vs. stress idle PID comparison is the core discriminator for fault-type
identification across `freeze_frame`-derived evidence. (Source:
`Advanced Diagnostic Correlation … Powertrain Control Systems_*.md`, `DtcDoc.md`.)

| PID | Curb idle (~800 RPM) | Stress idle (3500–4500 RPM, VIN-dependent) | Discriminator |
|---|---|---|---|
| STFT + LTFT (TFT) | reference | worsens → fuel delivery; improves → vacuum leak | Load-dependence of trim |
| `calculated_load_pct` | 5 – 25% | 40 – 60% (no road load) | CLV validates stress test |
| MAF g/s | ≈ 1 g/s per L displacement | ≈ 3 – 5 g/s/L (≈ 4× idle) | Sensor linearity |
| MAP kPa | ≈ 30 – 40 (high vacuum) | rising toward ≈ 80 | Restricted exhaust if MAP stays low |
| `ignition_advance_deg` | 5 – 15° BTDC | 25 – 40° BTDC | Knock retard if advance lags |
| Misfire counters | near zero | may increment under load | Coil arcing under load |

**Absolute vs. Calculated Engine Load:**

| PID | SAE | Characteristic | Use |
|---|---|---|---|
| `calculated_engine_load_pct` | `$04` | Normalized to 100% at WOT regardless of altitude/boost | Load context in freeze frame |
| `absolute_engine_load_pct` | `$43` | Tracks actual air mass per intake stroke; correlates with VE | Volumetric efficiency monitoring |

If `absolute_engine_load_pct` significantly lower than `calculated_engine_load_pct`
at WOT, volumetric efficiency is compromised — check restricted exhaust,
restricted intake, or cam timing.

---

## 10.5 FMEM / limp-home perception-trust flag **[PROPOSAL]**

> **Signal/noise:** v2-new, **weak** disposition. Consumer named below; full
> disposition in `11_proposals_register.md`. Source: Denton §5.2.1 via
> ANALYSIS §A6.

On a sensor fault the ECU enters **Failure Mode Effects Management (FMEM)** and
substitutes a **safe default value** for the failed sensor. A PID reading taken
while a sensor is under FMEM is **not a real measurement** — it is a calibration
default — and any perception derived from it should be down-trusted.

**Proposed contract:** a `fmem_suspected` bool, set when a sensor-circuit DTC
(e.g. P0102 MAF, P0113 IAT, P0118 ECT) is active AND the corresponding PID sits
at an implausibly flat default. The flag is only viable if FMEM state is
detectable from the available PIDs/DTCs; otherwise **DEFER**.

**Named consumer + code path:** OBDLab perception-trust / `analytics_preconditions`
→ COMLab confidence weighting demotes any PID-derived evidence whose source
sensor is `fmem_suspected`. This is the electronic mirror of the
`monitor_status` readiness gate (chunk `01`): both stop COMLab from trusting a
"reading" that the ECU never actually measured.

## Graph relations (explicit)

**cranking_speed** < 100 RPM DEMOTES **DTC analysis**
**battery_voltage** < 9.6 V DEMOTES **DTC analysis**
**P1260** INDICATES **security/immobiliser lockout**
**P1260** ROUTES_TO **DTCRoutingTag.MISFIRE_HISTORY**
**B1600** INDICATES **security/immobiliser lockout**
**B3055** INDICATES **security/immobiliser lockout**
**fmem_suspected** (proposed) GATED_BY **sensor circuit DTC** AND **flat default PID value**
**fmem_suspected** (proposed) DEMOTES **PID-derived evidence**
**absolute_engine_load_pct** < **calculated_engine_load_pct** INDICATES **compromised VE**

## Core Entities

- **P1260** — Manufacturer-specific DTC for Theft Detected (immobiliser lockout). Consumer: `dtclab/config/routing_tag_map.yaml`.
- **fmem_suspected** — Proposed flag indicating a sensor is operating under default FMEM substitution. Status: PROPOSAL. Consumer: OBDLab/COMLab perception trust.

