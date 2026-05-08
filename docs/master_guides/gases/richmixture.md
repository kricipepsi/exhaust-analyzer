---
source: richmixture.pdf (Crypton Diagnostic Equipment) — extracted 2026-05-03 via tesseract OCR + visual verification
tags: [rich, mixture, gas, exhaust, CO, CO2, HC, O2, valve_timing]
---

# Rich Mixture

The following lists some of the possible combinations of exhaust gas values and the most likely causes.

| CO | CO2 | HC | O2 | A/F Ratio too Rich: possible problems, conditions or causes |
|---|---|---|---|---|
| High | Low | Low to Moderate | Low | Rich fuel mixture; Leaking injectors; Incorrect carburettor adjustment; Power valve leaking; Choke operating rich (closed); Float level too high; Air filter dirty; EVAP canister purge system faulty; PCV system problem; ECM malfunctioning; Crankcase contaminated with raw fuel |
| Moderate to High | Low | Low to Moderate | Low | All of the above **but with catalytic converter operating correctly** (CO partly oxidised post-cat) |
| High | Low | High | High | Rich mixture **with ignition misfire** |
| Low | High | Low | Low | Good combustion efficiency and catalytic converter working properly! |

> **Note (very important):** High CO, Low CO2, **VERY High HC (>1000 ppm)** and **VERY High O2 (>5 %)** is sometimes an indicator of **WRONG ENGINE VALVE TIMING**. Simply explained, what enters the engine (air + fuel) gets out only partially burned because of poor mechanical condition.

## Causes of Excessive Exhaust Emissions

As a general rule, excessive HC, CO and NOx levels are most often caused by:

- **Excessive HC** — ignition misfire, or misfire due to excessively lean or rich air/fuel mixtures.
- **Excessive CO** — rich air/fuel mixtures.
- **Excessive NOx** — excessive combustion temperatures.

When troubleshooting these failures, identify the cause of the underlying conditions: for excessive CO, check every possible cause of "too much fuel or too little air".

## Causes of Excessive HC (Hydrocarbons)

High HC on fuel-injected vehicles is most commonly caused by ignition misfire or by mixture/mechanical faults that interrupt combustion:

- **Ignition system failures** — faulty ignition secondary component; faulty individual primary circuit on a distributorless ignition system; weak coil output due to coil or primary-circuit problem.
- **Excessively lean air/fuel mixture** — leaky intake manifold gasket; worn throttle shaft.
- **Excessive EGR dilution** — EGR valve stuck open or excessive EGR flow rate; EGR modulator bleed plugged.
- **Restricted or plugged fuel injector(s).**
- **Closed-loop control system incorrectly shifted lean.**
- **False input signal to ECM** — incorrect indication of load, coolant temp, O2 content, or throttle position.
- **Exhaust leakage past exhaust valve(s)** — tight valve clearances; burned valve or seat.
- **Incorrect spark timing** — incorrect initial timing; false input signal to ECM; worn piston rings or cylinder walls.
- **Insufficient cylinder compression.**
- **Carbon deposits on intake valves.**

## Causes of Excessive CO (Carbon Monoxide)

High CO is caused by anything that makes the mixture richer than ideal:

- Excessive fuel pressure at the injector(s).
- Leaking fuel injector(s).
- Ruptured fuel pressure regulator diaphragm.
- Loaded or malfunctioning EVAP system (use the two-speed idle test).
- Crankcase fuel contamination (two-speed idle test).
- Plugged PCV valve or hose (two-speed idle test).
- Closed-loop control system incorrectly shifted rich.
- Excessive combustion blow-by.
- False input signal to ECM — incorrect indication of load, coolant temp, O2 content, or throttle position.

> **Note:** Due to the reduction ability of the catalytic converter, increases in CO emissions tend to **reduce** NOx emissions. It is not uncommon to repair a CO emissions failure and, as a result of another sub-system deficiency, see NOx increase enough to fail a loaded-mode transient test.

## Causes of Excessive NOx (Oxides of Nitrogen)

Excessive NOx is caused by anything that makes combustion temperatures rise:

- **Cooling-system problems** — insufficient radiator airflow; low coolant level; poor cooling-fan operation; thermostat stuck closed or restricted; internal radiator restriction.
- **Excessively lean air/fuel mixture** — leaky intake manifold gasket; worn throttle shaft.
- **Closed-loop control system incorrectly shifted lean.**
- **Improper oxygen sensor operation** — slow rich-to-lean switch time; rich-biased O2-sensor voltage.
- **Improper or inefficient operation of EGR system** — restricted EGR passage; EGR valve inoperative; EGR modulator inoperative; plugged E or R port in throttle body; faulty EGR VSV operation; leaky/misrouted EGR hoses.
- **Improper spark advance system operation** — incorrect base timing; false signal input to ECM; improper operation of knock-retard system.
- **Carbon deposits on intake valves.**

## Implications for the 4D engine

The four-row table is the rich-side analogue of the lean table. Three of the rows have low CO2; the diagnostic split is whether (a) HC is also low (no misfire), (b) HC is high *and* O2 is high (rich + ignition misfire — fuel dumped, never lit), or (c) the cat is doing its job and CO has been partly oxidised down to "moderate". The "wrong valve timing" cell — High CO + Low CO2 + HC > 1000 + O2 > 5 — is a rare but important fingerprint that does not fit any pure rich/lean category and should map to a cam-timing or valve-mechanical fault node, not a generic rich.
