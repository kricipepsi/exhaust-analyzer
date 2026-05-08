# Master NOx Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for oxides of nitrogen (NOx) on petrol engines — the physical chemistry of NOx formation, the 4-gas vs 5-gas analyser distinction, the canonical gas-analyser signatures for every NOx-producing fault state, the EGR and catalyst reduction mechanisms, the physical justification for every threshold the 4D engine uses in the `nox_elevated`, `nox_lean_combustion`, `nox_egr_failure`, and `nox_catalyst_degraded` KG nodes, and the DTC-to-cause mapping for the P0400–P0408 (EGR) and P0420/P0430 (catalyst) families where NOx is the primary evidence channel. Rows in the CSV that cite NOx as a diagnostic signal cite the rules below.

---

## 1. What NOx is — formation physics

NOx is the collective term for nitric oxide (NO, ~95 % in spark-ignition engines) and nitrogen dioxide (NO₂, ~5 %). Both are formed when atmospheric nitrogen (N₂) and oxygen (O₂) combine at high temperature inside the combustion chamber.

**The Zeldovich mechanism (thermal NOx):** The dominant formation pathway in petrol engines is the extended Zeldovich mechanism:

```
O + N₂ → NO + N
N + O₂ → NO + O
N + OH → NO + H
```

The rate-limiting step is the first — breaking the N₂ triple bond (bond dissociation energy 941 kJ/mol). This bond breaks only at temperatures above approximately 1370 °C (2500 °F). Below this temperature, NOx formation is negligible regardless of mixture composition.

**The three NOx governors — temperature, time, oxygen:**

| Factor | Effect on NOx | Physical mechanism |
|--------|---------------|-------------------|
| **Peak combustion temperature** | Primary driver | Above ~1370 °C, N₂ becomes reactive. Every 100 °C increase above 1370 °C roughly doubles the NOx formation rate. |
| **Residence time at peak temperature** | Secondary | The longer the charge spends above 1370 °C, the more NOx forms. High-RPM operation reduces residence time but increases peak pressure (more complex net effect). |
| **Available oxygen** | Tertiary | Lean mixtures (λ > 1.0) leave excess O₂ after combustion that can combine with N. Peak NOx formation occurs slightly lean of stoichiometric (~λ = 1.05) where both temperature and O₂ availability are high. |

**The fundamental NOx-HC trade-off:** NOx and HC emissions move in opposite directions across the lambda range. Rich mixtures (λ < 1.0) produce high HC and CO with low NOx (cooler burn, oxygen-starved). Lean mixtures (λ ≥ 1.0) produce low HC and CO with climbing NOx (hotter burn, oxygen-rich). An engine cannot simultaneously minimise all three without after-treatment. This inverse relationship is a core diagnostic signal — when HC is very low and NOx is very high, suspect lean combustion.

---

## 2. 4-gas vs 5-gas analyser — the hardware distinction

This is the single most important operational distinction for NOx measurement in the workshop. The task verification section requires this be stated explicitly.

### 2.1 4-gas analyser — NOx is invisible

A 4-gas analyser measures **HC, CO, CO₂, and O₂** only. It does NOT measure NOx. The four gases are sufficient to compute Brettschneider lambda, assess mixture balance, detect rich/lean conditions, and evaluate catalyst efficiency via the O₂ storage test. However, a 4-gas analyser is **blind to NOx-specific faults.**

On a 4-gas analyser, NOx problems must be inferred indirectly:
- High NOx from lean combustion → O₂ elevated, CO low, λ > 1.00
- High NOx from EGR failure → O₂ elevated at warm idle, HC normal, CO normal, λ ≈ 1.00
- High NOx from cooling system overheating → all gases may appear normal at idle

A 4-gas analyser cannot confirm an EGR malfunction — it can only flag the gas pattern that EGR malfunction produces. The diagnostic engine must treat NOx-related symptoms as **inferred** (lower confidence ceiling) when running on 4-gas data, and **direct** (full confidence ceiling) when running on 5-gas data.

### 2.2 5-gas analyser — NOx is visible

A 5-gas analyser adds an electrochemical or chemiluminescence NOx sensor, measuring **HC, CO, CO₂, O₂, and NOx** (in ppm). The NOx channel provides direct evidence for:
- Lean combustion detection (high NOx confirms the mixture is burning lean, not just lean-measured)
- EGR valve function verification (NOx suppressed at warm idle → EGR working; NOx present at warm idle → EGR not diluting the charge)
- Catalyst reduction efficiency (pre-cat vs post-cat NOx gradient)
- Combustion chamber temperature inference (high NOx → hot burn; zero NOx → cold or diluted burn)

### 2.3 Confidence ceiling per L16

The 4D engine's confidence ceiling (L16) keys on evidence layers used:

| Analyser type | NOx evidence | Confidence ceiling |
|---------------|-------------|-------------------|
| 4-gas | Inferred only | Gas-only 0.40; +DTC 0.60; +FF 0.95 |
| 5-gas | Direct measurement | Gas-only 0.55; +DTC 0.70; +FF 0.95; full DNA 1.00 |

When NOx is a required discriminator for a fault node and only 4-gas data is available, the node cannot fire at full confidence — the engine must flag `insufficient_evidence` or downgrade to a parent family node.

---

## 3. NOx behaviour across the operating envelope

### 3.1 Idle — NOx near zero

At warm idle, combustion chamber temperatures rarely exceed 1370 °C for sustained periods. Cylinder charge density is low, and the exhaust gas residence time in the cylinder is short. NOx at idle is typically close to 0 ppm on a healthy engine, regardless of lambda. **A non-zero NOx reading at idle is a diagnostic signal** — it suggests either:

- Cooling system problem raising base chamber temperature (ECT > 105 °C, thermostat stuck, restricted radiator)
- Over-advanced ignition timing raising peak pressure and temperature
- EGR valve not opening (the lack of dilution cooling allows chamber temperature to rise)
- Carbon deposits retaining heat and creating hot spots

### 3.2 Light load / cruise — moderate NOx

Under part-throttle cruise, chamber temperatures are higher than idle but below WOT peaks. Lambda control is active (closed-loop). EGR is open and modulating. NOx should be present in the 50–200 ppm range on a 5-gas analyser. Higher readings suggest EGR restriction or lean bias.

### 3.3 WOT / heavy load — peak NOx

Under wide-open throttle, peak cylinder pressure is highest and peak temperature approaches maximum. EGR is closed (engine needs oxygen for power). NOx can reach 2000–4000+ ppm on an unmitigated engine. The three-way catalyst must handle this NOx spike through its reduction cycle.

### 3.4 Decel — NOx near zero

On deceleration fuel cut (DFCO), combustion stops — no NOx is produced. On throttle-close, manifold vacuum spikes, charge density drops, and temperature falls below the formation threshold.

---

## 4. Causes of elevated NOx

Every cause reduces to one of the three governors (§1): temperature too high, time at temperature too long, or oxygen available that should not be.

### 4.1 Lean air/fuel mixture (λ > 1.00)

The most common cause of elevated NOx on petrol engines. When the mixture burns lean, excess oxygen is available after combustion and peak temperature rises (lean flame is hotter until it becomes too lean to sustain, around λ 1.25–1.30).

**Gas signature:** O₂ elevated, CO low, λ > 1.00, HC low or normal, NOx elevated
**Common causes:** vacuum leak (unmetered air), low fuel pressure, clogged injector(s), MAF under-reading, O₂ sensor biased lean, intake manifold gasket leak
**Source guide:** `docs/master_guides/gases/leanmixture.md`

The lean-burn NOx threshold: λ > 1.05 sustained → NOx begins climbing sharply. At λ 1.10, NOx may be 2–5× the stoichiometric baseline. At λ 1.20, NOx falls again as the lean limit approaches and combustion temperature drops.

### 4.2 EGR system malfunction

When the EGR valve fails to open (clogged passage, faulty solenoid, vacuum leak in EGR control circuit), inert exhaust gas does not dilute the intake charge. Peak temperature rises unchecked, and NOx spikes — most noticeably at warm idle and cruise, where EGR should be actively diluting.

**Gas signature at warm idle:** O₂ normal, CO normal, λ ≈ 1.00, HC normal, NOx elevated (should be near zero)
**Key discriminator:** This is the only common fault where all four standard gases (HC, CO, CO₂, O₂) appear normal but NOx is elevated. A 4-gas analyser will see *nothing wrong*.
**Source guide:** `docs/master_guides/egr/master_egr_guide.md §1–§4`

### 4.3 Over-advanced ignition timing

Advancing ignition timing beyond the calibrated MBT (maximum brake torque) point raises peak cylinder pressure before TDC, increasing peak temperature. Every degree of over-advance increases NOx potential by ~5–10 % while also raising the knock risk.

**Gas signature:** HC normal, CO normal, O₂ normal, λ ≈ 1.00, NOx elevated; may be accompanied by knock sensor DTCs
**Source guide:** `docs/master_guides/ignition/master_ignition_guide.md`

### 4.4 Cooling system problems

Elevated engine coolant temperature (ECT) increases base combustion chamber temperature, shifting the entire thermal profile upward. A thermostat stuck closed (ECT > 105 °C), low coolant, or restricted radiator all elevate NOx.

**Gas signature:** All gases may appear normal at idle; NOx elevated. ECT PID > 105 °C.
**Source guide:** `docs/master_guides/mechanical/master_mechanical_guide.md`

### 4.5 Carbon deposits (hot spots)

Carbon buildup on intake valves, piston crowns, and combustion chamber surfaces retains heat between cycles and creates localised hot spots that can exceed 1370 °C even when the bulk chamber temperature is below threshold. These hot spots act as NOx ignition sites.

**Gas signature:** Similar to over-advanced timing — NOx elevated with otherwise normal gases. Often accompanied by HC spikes from absorption/desorption of fuel on carbon deposits.
**Source guide:** `docs/master_guides/mechanical/master_mechanical_guide.md`

---

## 5. EGR as the primary NOx control mechanism

EGR recirculates inert exhaust gas (primarily CO₂, H₂O, N₂) into the intake, cooling peak combustion temperature through three mechanisms: dilution (O₂ displacement), thermal (high specific heat of triatomic molecules), and chemical (minor). This is the engine's primary in-cylinder NOx control.

**EGR valve position vs NOx:**

| EGR state | NOx effect | Condition |
|-----------|-----------|-----------|
| EGR open (warm idle) | NOx suppressed → near 0 ppm | Normal operation |
| EGR modulating (cruise) | NOx moderated → 50–200 ppm | Normal operation |
| EGR closed (WOT) | NOx uncontrolled → 2000+ ppm | Normal — EGR intentionally closed |
| EGR stuck closed (warm idle) | NOx elevated → 100–500+ ppm | **Fault** — EGR should be open |
| EGR stuck open (all conditions) | NOx suppressed everywhere but HC spikes from dilution misfire | **Fault** — see `master_egr_guide.md §4.2` |

**Source guide:** `docs/master_guides/egr/master_egr_guide.md §1–§4`

---

## 6. Three-way catalyst NOx reduction

The three-way catalyst (TWC) reduces NOx to N₂ and O₂ through the **reduction** reaction:

```
2 CO + 2 NO → 2 CO₂ + N₂
HC + NO → CO₂ + H₂O + N₂
```

This requires CO and HC to be present as reducing agents — a lean-running engine (λ > 1.00) produces insufficient CO to drive the reduction reaction. The lambda window for effective TWC operation is 0.98–1.02. Outside this window, NOx conversion efficiency drops sharply.

**Pre-cat vs post-cat NOx measurement:** A properly functioning catalyst removes 90–99 % of NOx. If tailpipe NOx approaches pre-catalyst levels, the catalyst reduction capability has failed, typically from:

- Catalyst thermal degradation (melted substrate from sustained rich misfire dumping raw fuel into the cat)
- Catalyst poisoning (lead, silicone, phosphorus, zinc from contaminated fuel or incorrect oil)
- Catalyst mechanical failure (broken substrate, restricted exhaust)
- Lambda outside the TWC window (lean → no CO for reduction reaction; rich → excess CO but poor NOx reduction due to low initial NOx)

**Source guide:** `docs/master_guides/catalyst/master_catalyst_guide.md`

---

## 7. DTC families where NOx is the primary evidence

| DTC family | Description | NOx role | Source guide |
|------------|-------------|----------|-------------|
| P0400 | EGR flow malfunction | Insufficient EGR → NOx elevated at warm idle | `master_egr_guide.md` |
| P0401 | EGR flow insufficient | Same as P0400; lower severity threshold | `master_egr_guide.md` |
| P0402 | EGR flow excessive | Over-dilution → HC spike, NOx suppressed | `master_egr_guide.md` |
| P0403–P0408 | EGR circuit/position faults | Electrical failure of EGR control; mechanical effects as above | `master_egr_guide.md` |
| P0420/P0430 | Catalyst system efficiency below threshold (bank 1/2) | Catalyst NOx reduction degraded; tailpipe NOx rises toward pre-cat level | `master_catalyst_guide.md` |
| P0171/P0174 | System too lean (bank 1/2) | Lean mixture → elevated NOx; see §4.1 above | `docs/master_guides/fuel_trim/master_fuel_trim_guide.md` |
| P0010–P0025 | VVT/cam timing faults | Altered valve timing can shift effective compression and combustion temperature | `master_mechanical_guide.md §9` |

---

## 8. NOx thresholds — provenance table

Every numeric threshold the 4D engine applies to NOx signals. All values are petrol-only, MY 1990–2020, 5-gas analyser unless noted.

| Parameter | Value | Unit | Applies to | Physical basis | Source guide |
|-----------|-------|------|-----------|----------------|-------------|
| `nox_idle_normal_max` | 30 | ppm | Warm idle, 5-gas | Idle chamber temp rarely exceeds 1370 °C; NOx near zero on healthy engine | `docs/master_guides/nox/master_nox_guide.md` §3.1 |
| `nox_idle_warning` | 50 | ppm | Warm idle, 5-gas | Above 50 ppm at idle is unambiguous — something (EGR, cooling, timing) is raising chamber temp | `docs/master_guides/nox/master_nox_guide.md` §3.1 |
| `nox_cruise_normal_max` | 300 | ppm | Cruise, 5-gas | Part-throttle with EGR modulating; 300 ppm is the upper bound of typical closed-loop cruise NOx | `docs/master_guides/nox/master_nox_guide.md` §3.2 |
| `nox_wideband_lean_threshold` | 500 | ppm | Any speed/load, 5-gas | Above 500 ppm with λ > 1.05 → lean-combustion NOx confirmed | `docs/master_guides/nox/master_nox_guide.md` §4.1 |
| `nox_egr_failure_idle` | 100 | ppm | Warm idle, EGR commanded open, 5-gas | EGR at warm idle should suppress NOx below 100 ppm; above → EGR not diluting | `docs/master_guides/egr/master_egr_guide.md` §4 |
| `nox_cat_efficiency_min` | 90 | % | Pre-cat vs post-cat delta | TWC must reduce NOx by ≥ 90 % at operating temperature | `docs/master_guides/catalyst/master_catalyst_guide.md` |
| `nox_formation_temp` | 1370 | °C | n/a | Temperature at which N₂ becomes reactive (Zeldovich rate-limiting step) | `docs/master_guides/nox/master_nox_guide.md` §1 |
| `nox_peak_lambda` | 1.05 | λ | All conditions | Peak NOx formation occurs slightly lean of stoich — maximum temperature + excess O₂ | `docs/master_guides/nox/master_nox_guide.md` §1 |
| `tolerance_idle_4gas` | — | — | 4-gas only | NOx not measurable on 4-gas; this field intentionally blank — flag nodes firing on NOx discriminators when only 4-gas data present | `docs/master_guides/nox/master_nox_guide.md` §2.3 |

---

## 9. NOx — engine-state modifiers

NOx behaviour changes across engine states. The 4D engine must gate NOx symptoms on M0's `engine_state` output (L15).

| Engine state | NOx behaviour | Diagnostic meaning |
|-------------|---------------|-------------------|
| Cold start (ECT < 40 °C) | Near zero regardless of mixture | Chamber cold; formation temp not reached; EGR disabled — no EGR assessment possible |
| Warm idle | Near zero on healthy engine with working EGR | Non-zero → cooling/timing/EGR fault |
| Closed-loop cruise | Moderate, EGR-modulated | Elevated → EGR restriction or lean bias |
| Open-loop WOT | High (2000+ ppm possible) | Normal — EGR intentionally closed; use absolute NOx with caution at WOT |
| OL_FAULT / OL_DRIVE | Unreliable — open-loop fuel control may mask or amplify NOx | Fuel-status gate (L18) must fire before any NOx symptom — if fuel control is open-loop, NOx evidence is unreliable |

---

## 10. Petrol-only scope boundary (R12)

This guide covers spark-ignition petrol engines only. Diesel NOx formation follows a different physical pathway (compression-ignition lean burn, diffusion flame, NOx formed in the flame front at stoichiometric despite overall lean mixture). Diesel NOx control uses DOC + DPF + SCR (urea injection) rather than TWC reduction. No diesel NOx thresholds, mechanisms, or DTCs appear in this guide or in the 4D engine. The `test_petrol_only_lint.py` CI guard enforces this boundary.

---

## 11. Cross-references

| Domain | Guide | Why linked |
|--------|-------|-----------|
| EGR | `docs/master_guides/egr/master_egr_guide.md` | Primary NOx control mechanism; EGR failure is the most common cause of elevated NOx |
| Catalyst | `docs/master_guides/catalyst/master_catalyst_guide.md` | TWC NOx reduction chemistry; catalyst efficiency thresholds |
| Lean mixture | `docs/master_guides/gases/leanmixture.md` | Lean combustion is the second most common cause of elevated NOx |
| Ignition | `docs/master_guides/ignition/master_ignition_guide.md` | Over-advanced timing raises peak temperature → elevated NOx |
| Mechanical | `docs/master_guides/mechanical/master_mechanical_guide.md` | Cooling system faults, carbon deposits, VVT altering effective compression |
| O₂ sensor | `docs/master_guides/o2_sensor/master_o2_sensor_guide.md` | Biased O₂ sensor can drive lean-bias → elevated NOx |
| Freeze frame | `docs/master_guides/freeze_frame/master_freeze_frame_guide.md` | FF captures ECT, RPM, LOAD_PCT, SHRTFT, LONGFT at DTC trigger — all NOx-relevant |
