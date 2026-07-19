---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "fuel-trim-reasoning"
implements:
  - "labs/dtclab/dtclab/schemas/freeze_frame.py"
consumers:
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py Mixture scoring"
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py Total Fuel Trim evaluation"
drift_guards:
  - "labs/dtclab/tests/unit/test_freeze_frame_extractor.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/03_fuel_trim_grammar.md"
---
# 03 — Fuel-trim formulas, patterns & self-healing

Anchors: `DTC_VOCABULARY.md §12.1` (STFT/LTFT fields), `§13` (`Mode06MonitorResult`).
The Δ_Healing and TFT formulas are **computed by COMLab** from inputs DTCLab
emits; DTCLab's job is to emit both inputs cleanly. See `00_INDEX.md` for scope.

---

## 3.1 Self-healing delta formula

Quantifies recovery between the time the DTC was stored (freeze frame) and the
current scan session.

```
Δ_Healing = |FF_Total_Trim| − |Mode$06_Current_Correction|

FF_Total_Trim     = |FF_STFT1 + FF_LTFT1|
Mode$06_Current   = |current_stft1 + current_ltft1|
```

| Δ_Healing | Interpretation |
|---|---|
| ≥ +20% | **Healed** — fault more severe when DTC set; currently resolving |
| +10 to +19% | Partial recovery |
| −10 to +10% | **Still active** — current trim magnitude matches freeze frame |
| < −10% | **Worsening** — current deviation exceeds freeze frame |

**Worked example (`DTCcase2.md`):** P0171 with loose gas cap. Freeze frame STFT
+22%, LTFT +11% → `|FF_Total_Trim| = 33%`. After cap tightened: current STFT +1%,
LTFT +1% → `|Mode$06_Current| = 2%`. `Δ_Healing = 33 − 2 = +31%` → healed.

**Ownership note:** the formula is *computed by COMLab* using inputs DTCLab
supplies (freeze-frame trims + Mode `$06` current corrections). DTCLab does not
compute Δ_Healing — it ensures both inputs are emitted cleanly.

---

## 3.2 Total fuel trim (TFT)

```
TFT = STFT + LTFT
```

| TFT range | Interpretation |
|---|---|
| −10 to +10% | Healthy |
| +10 to +25% | Lean condition; PCM compensating |
| ≥ +25% | Severe lean — approaching P0171 |
| −10 to −25% | Rich condition; PCM cutting fuel |
| ≤ −25% | Severe rich — approaching P0172 |

**Fuel-mass model (Denton corroboration).** Denton §5.4 gives the adaptive trim
model: STFT is the instantaneous correction; **LTFT is learned, stored in KAM,
battery-robust, and reset only by a technician clear**; an LTFT pinned at its
limit forces a fuel-system DTC. Denton's fuel-mass relation uses the AFR
constant **14.64** (`fuel_mass = (air_mass × LTFT) / (STFT × 14.64)`); 4DLab
keeps **14.7** as the physical stoichiometric ratio and notes 14.64 as Denton's
trim-equation constant. This corroborates the existing OBDLab trim channels
(`BANK-ASYM-1`); it adds no DTCLab field. Source: ANALYSIS §B.

---

## 3.3 STFT/LTFT RPM-dependence patterns

| Pattern | Most likely fault |
|---|---|
| LTFT high+ at idle, drops at 2500–3000 RPM | **Vacuum leak** — constant unmetered volume more dilutive at low airflow |
| Trims moderate+ at idle, **worsens** at high RPM | **Fuel delivery** — pump/filter cannot maintain volume |
| Trims + at idle, − under load | **MAF under-reading** — contaminated sensor |
| One bank −, persists across RPM | **Leaking injector** on that bank |
| − at idle, normalises at cruise | **Stuck-open EVAP purge** |
| High+ at idle, normalises at cruise | **Stuck-open EGR** |
| STFT and LTFT opposite signs | **Healing** — PCM reversing learned correction |
| STFT and LTFT same sign + similar magnitude | **Active and severe** |

---

## 3.4 Bank asymmetry rules (V engines)

| Cross-bank pattern | Interpretation |
|---|---|
| One bank drifts, other normal | Single-bank fault: intake gasket, injectors, pre-cat leak on that side |
| Both banks drift same direction | Common-mode: fuel pump, MAF, post-MAF intake leak, EVAP/EGR |
| Banks drift opposite directions | Sensor fault on at least one bank, or exhaust crossover |

---

## 3.5 Preconditions for a valid fuel-trim reading

All must hold; otherwise the fuel-trim reading is invalid:

- `coolant_temp_c ≥ 70°C`
- `fuel_system_status = CL`
- No active P0130 – P0161 (O₂ sensor circuit)
- No active P0335 / P0340 (crank / cam sensor)
- ≥ 1 drive cycle since `codes_cleared`
- Not at WOT (`throttle_pos_pct < 80%`)

## Graph relations (explicit)

**TFT** DEFINED_AS **STFT + LTFT**
**Δ_Healing** DEFINED_AS **|FF_Total_Trim| − |Mode$06_Current_Correction|**
**LTFT** STORED_IN **KAM**
**TFT** CONSUMED_BY **COMLab**
**Δ_Healing** CONSUMED_BY **COMLab**
**LTFT high+ at idle, drops at high RPM** INDICATES **vacuum_leak**
**LTFT moderate+ at idle, worsens at high RPM** INDICATES **fuel_delivery**
**LTFT + at idle, − under load** INDICATES **MAF contamination**
**One bank −, persists across RPM** INDICATES **leaking injector**
**LTFT − at idle, normalises at cruise** INDICATES **stuck_open EVAP purge**
**LTFT high+ at idle, normalises at cruise** INDICATES **stuck_open EGR**
**coolant_temp_c >= 70°C** VALIDATES **TFT**
**fuel_system_status == CL** VALIDATES **TFT**
**throttle_pos_pct < 80%** VALIDATES **TFT**

## Core Entities

- **TFT** — Total Fuel Trim, sum of short-term and long-term fuel trim corrections. Consumer: COMLab mixture scoring.
- **Δ_Healing** — Diagnostic metric quantifying trim deviation recovery between freeze-frame trigger and current scan. Consumer: COMLab healing classification.
- **LTFT** — Long-Term Fuel Trim, adaptive correction stored in keep-alive memory. Consumer: `dtclab/schemas/freeze_frame.py`.

