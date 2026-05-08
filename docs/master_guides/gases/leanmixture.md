---
source: leanmixture.pdf (Crypton Diagnostic Equipment) — extracted 2026-05-03 via tesseract OCR + visual verification
tags: [lean, mixture, gas, exhaust, CO, CO2, HC, O2]
---

# Lean Mixture

The following lists some of the possible combinations of exhaust gas values and the most likely causes.

| CO | CO2 | HC | O2 | A/F Ratio too Lean: possible problems, conditions or causes |
|---|---|---|---|---|
| Low | Low | High | High | Lean fuel mixture; Ignition misfire; Vacuum leaks / air leaks (between air flow sensor and throttle body); Bad EGR valve or vacuum hoses misrouted; Carburettor settings incorrect; Fuel injector/s bad; O2 sensor bad or failing; ECM malfunctioning; Float level too low |
| Low | High | Low | Low | Good combustion efficiency and catalytic converter working properly! |

## Reading

The lean fingerprint is **Low CO + Low CO2 + High HC + High O2**: combustion is happening, but a fraction of the air–fuel charge is leaving without burning. The HC rise is a *lean misfire* signature — the flame front does not propagate, so raw fuel slips out alongside excess air. The high O2 is the same physics: the lean mixture has more air than the fuel can consume, so oxygen is left over.

The contrast row (Low CO + High CO2 + Low HC + Low O2) is the diagnostic gold standard — a clean stoichiometric burn through a working three-way cat. CO2 climbs to its near-theoretical maximum, HC and O2 are scrubbed, and CO has nowhere to come from because everything that could become CO became CO2 instead.

## Implications for the 4D engine

When all four signals match the lean row above and `lambda_analyser > 1.05`, the engine should activate generic `lean_condition`. Specific children (vacuum leak, dirty MAF, EGR-stuck-open, PCV) are then chosen by the discriminator that fires alongside (idle-only trims for PCV, dual-bank trims for vacuum leak, MAF voltage for MAF, NOx > 1000 ppm at idle for EGR).
