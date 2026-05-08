---
source: lambda.pdf (Crypton Diagnostic Equipment)
converted: 2026-05-03
tags: [lambda, brettschneider, AFR, mixture, exhaust, gas, catalyst]
---

# Lambda

Oxygen/Combustibles balance (Lambda) is calculated from the measured values of O2, CO, CO2, HC, NOx and water vapour in the exhaust gas. This is a direct measurement of Air/Fuel ratio, and may be easily used to assess fuel mixture balance. The Lambda calculation compares all of the oxygen in the exhaust gases to all of the carbon and hydrogen in the gases. (Water, which contains both hydrogen and oxygen, is determined by estimation using the fraction of the sum of CO to CO2 in the exhaust.)

The result of the calculation is **Lambda**, a dimensionless term that relates nicely to the Stoichiometric value of air to fuel. At the Stoichiometric point, Lambda = 1.000. A Lambda value of 1.050 is **5.0 % lean**, and a Lambda value of 0.950 is **5.0 % rich**. Once Lambda is calculated, A/F ratio can be determined by simply multiplying Lambda times the Stoichiometric A/F ratio for the fuel used (e.g. 14.71 for petrol).

## Details of the Lambda Calculation

The Brettschneider equation is the de-facto standard method used to calculate the normalised Air/Fuel Balance (Lambda) for domestic and international Inspection Programs. It is derived from a paper written by Dr. J. Brettschneider in 1979. He established a method to calculate Lambda (Balance of Oxygen to Fuel) by comparing the ratio of oxygen molecules to carbon molecules in the exhaust.

Although this equation is very complex, the result is relatively easy to use in practice. Lambda directly reflects the "degree of leanness" of the air/fuel mixture and is **independent of how efficiently the fuel is oxidised** — a very important factor when dealing specifically with air/fuel balance issues. The manner in which this equation is to be used is strictly a function of the application, and it is an excellent replacement for "old" commonly used conventions such as CO measurement for rich-side applications (performance tuning), or wide-range lambda sensors which are not only very non-linear but also very sensitive to combustibles in the exhaust stream. The only dependable air/fuel ratio measurement that has been found to date is one that first makes an accurate measure of the constituent gases in the exhaust stream (at least the four gases of HC, CO, CO2 and O2) and calculates the oxygen and combustibles content and then the Lambda and A/F value.

## Using Lambda as a Diagnostic Aid

It is important to actually use Lambda in practice to see how well it correlates to the real world. A little experience here goes a long way in building confidence as to the efficacy of this parameter.

It is possible to use Lambda as an aid when tuning an engine provided that the engine is in good running order.

Using Lambda alone, however, is not enough to diagnose a particular emission-related problem. Having a 4- or 5-Gas Analyser at your disposal is an invaluable tool for engine diagnostics. Here are some general guidelines:

| Lambda — Low — < 1.0 | Lambda — High — > 1.0 | Lambda — High — > 1.0 | Lambda = 1.0 |
|---|---|---|---|
| CO = High | CO = Low | CO = Low | CO = Low |
| CO2 = Low | CO2 = Low | CO2 = Low | CO2 = High |
| HC = High | HC = Low | HC = High | HC = Low |
| O2 = Low | O2 = High | O2 = High | O2 = Low |
| **Rich Mixture** | **Exhaust Leak** | **Lean Mixture** | **Tuned** |

Note: the second column ("exhaust leak") and the third column ("lean mixture") share the same lambda direction (>1.0) but differ in HC — an exhaust/sample air leak shows low HC because the leak is downstream of any combustion event, while a real lean mixture pushes HC up through lean-misfire. This is the signature the engine should use to distinguish a falsely lean lambda from a truly lean burn.

## Typical Emission Values With and Without Catalytic Converter (good system — guide lines only)

|  | CO | CO2 | HC | O2 | Lambda | AFR |
|---|---|---|---|---|---|---|
| With Catalyst | 0.5 % or less | 14.5 % or more | 50 ppm or less | 0.5 % or less | 0.97 – 1.03 | 14.3:1 to 15.1:1 |
| Without Catalyst | 1.5 % or less | 13 % or more | 250 ppm or less | 0.5 % – 2 % | 0.90 – 1.10 | 13.2:1 to 16.2:1 |

## Typical Emission Values Measured Before and After the Catalytic Converter (good system — guide lines only)

|  | CO | CO2 | HC | O2 | Lambda | AFR |
|---|---|---|---|---|---|---|
| Before Catalyst | 0.6 % | 14.7 % | 100 ppm | 0.7 % | 1.0 | 14.7 |
| After Catalyst | 0.1 % | 15.2 % | 15 ppm | 0.1 % | 1.0 | 14.7 |

## The effect of various "octane" fuel mixes on Lambda

Various mixes of gasoline contain differing ratios of short and long hydrocarbon chains, resulting in a variation of octane-rated fuels. This has a small effect on the ratio of hydrogen to carbon in the fuel, but these variations have a trivial effect on the Lambda calculation. So before you blame your gas analyser for the Lambda being "rubbish", make sure you actually know what fuel (or mixture of fuels) the engine is running on. A difficult task to achieve, so if everything else looks normal, then the improbable must be the truth — trust your equipment.

## The effect of Oxygenated fuels on Lambda

Oxygenated fuels release a very small amount of oxygen contained in the fuel as it burns. The total O2 equivalence in typical oxygenated fuel is on the order of 0.1 % O2, so this effect is small.

## The effect of NOx on Lambda

NOx has a relatively immaterial effect on the Lambda calculation, as 1 000 ppm NOx is only equivalent to 0.05 % oxygen utilisation. **A 4-gas analyser is adequate for Lambda calculation** — but at least 4 gases must be measured. At idle NOx is typically close to 0 ppm, so it can be ignored. At fast idle and light load, the gas analyser replaces the NOx value with an "automatic replacement equation" so that as-close-as-possible results are achieved even with a 4-gas analyser. Using a 5-Gas Analyser, however, is the ultimate way to go.

## Sample Dilution and Air Injection Effects on Lambda

As a side note, it is important to understand the effect that sampling air leaks or outright air injection may have on the Lambda calculation. **The percentage of extra air in the exhaust gases will result in the same percentage error in the Lambda calculation.** I.e., a 5 % air leak will not only dilute (lower) the CO, HC, CO2 and NOx gas readings by 5 %, but will increase the oxygen reading by about 1.00 % (5 % of 20.9 %) and will result in the calculated Lambda being 5 % leaner than it should. That means that a perfect Lambda of 1.000 will be reported as 1.050 if there is a 5 % air leak or injection.

This is a significant error, and can occur relatively easily. It should be noted that air leaks or injection will always bias the lambda calculation toward the lean side, so they should be dealt with and corrected before any lambda calculations using measured gases are attempted. Air injection should be disabled for Lambda to be calculated correctly.

## Engine Misfire & the effect of Combustion Efficiency on Lambda

Because the Lambda calculation determines the balance between oxygen and combustible gases by comparing all the oxygen available to the combustibles-bearing gases, it is relatively insensitive to the degree to which the combustibles have been oxidised. **Thus, an engine misfire has absolutely no effect on the Lambda calculation.**

## Pre and Post Catalytic Converter gases

Because the Lambda calculation determines the balance between oxygen and combustible gases by comparing all the oxygen available to the combustibles-bearing gases, it is relatively insensitive to the degree to which the combustibles have been oxidised. Thus, the gas stream before a catalytic converter should calculate the same Lambda value as the gases after a catalytic converter.

In essence, because ALL of the gases are used in the Lambda calculation, the gas mix in the intake manifold, half-way through the combustion process, before a catalytic converter, or at the tailpipe should ALL yield the same Lambda result. The intake manifold will contain oxygen, HC, and no CO, CO2 or NOx. They will, however, be in balance. The tailpipe should contain low levels of oxygen and HC and CO (the sources of combustion), but high levels of CO2 and water vapour. They will be at the same balance as the intake manifold gases. **Nothing is lost or gained, just converted! It really does not matter where the gases are measured, or how efficient the combustion process is.**
