# Follow-up Research Questionnaire — Petrol Engine Symptom-to-Fault Diagnostics

You are an automotive diagnostics researcher. The accompanying document (the "original
research") establishes a driver-symptom taxonomy, heuristic fault priors, exhaust-gas
chemistry footprints, and environmental context modifiers for petrol passenger cars. It has
**gaps**. Your task is to fill the gaps below with sourced, quantitative answers.

## Operating envelope (constrain every answer to this)

- Passenger **petrol** cars, model years **1990–2010**, Euro 1 to Euro 5.
- **Warm engine** operating condition.
- Exhaust-gas chemistry (HC, CO, NOₓ, lambda) treated as diagnostic ground truth.

## Evidence standard

- Every numeric value must carry a **source URL**.
- **Prefer primary sources** — SAE standards, EPA/NHTSA reports, peer-reviewed papers, OEM
  service data — over blogs, forums, or parts-retailer pages.
- Where a value is an expert estimate rather than a measured figure, **label it "estimated."**
- If no reliable data exists for an item, **say so explicitly** — do not invent a number.

---

## Gap 1 — Exhaust-chemistry footprints for the missing fault families (highest priority)

The original research gives HC / CO / NOₓ / fuel-consumption percentage shifts (vs baseline
stoichiometry, warm engine) for only six component families: throttle-body butterfly fault,
throttle idle-control valve, spark-plug misfire, oxygen-sensor lean bias (0.1 V), oxygen-sensor
rich bias (0.9 V), and EGR valve stuck open.

For **each** additional fault family below, find the measured warm-engine exhaust-gas shift
(direction, and percentage if available) versus baseline, with a source:

1. Ignition coil / secondary-insulation breakdown (under load)
2. Vacuum leak / unmetered air (intake manifold gasket)
3. Catalytic converter (melted or restricted)
4. Mass-airflow (MAF) sensor contamination / bias
5. EVAP purge valve stuck
6. Crankshaft / camshaft position sensor dropout
7. Valve-stem seals or piston rings (oil burning)
8. Head gasket (coolant entering combustion chamber)
9. Leaking or stuck-open fuel injector (rich condition)
10. Coolant-temperature-sensor bias (cold-enrichment table)

## Gap 2 — Measured (not estimated) fault frequencies per symptom category

The original research's per-category fault-family priors are mostly expert estimates. For each
of the **six primary symptom categories** in the attached catalog (vehicle starting issues;
rough idle and shudder; lack of power and hesitation; poor economy/odor/sound; engine dies or
stalls; visible exhaust smoke), find **measured** fault-family frequency data from automotive
repair databases (e.g. RepairPal, CarMD Vehicle Health Index, large repair-record studies, or
peer-reviewed analyses) for the 1990–2010 petrol envelope. For each, note: the database/source,
the sample size if reported, and whether the figure is measured or estimated.

## Gap 3 — Environmental context-modifier gaps

The original research maps how engine temperature state (cold-only / hot-only) and engine load
state (idle / steady cruise / transient acceleration / coasting deceleration) shift the
likelihood of specific fault families — but several combinations are marked "neutral / no
correlation found." For each such gap, determine whether a documented thermal- or load-based
correlation actually exists, giving the physical rationale and a source. Prioritise the load-
state axis, which is the least-documented dimension.

## Gap 4 — Labeled symptom-to-repair datasets (empirical validation feasibility)

The original research concludes that validating these priors empirically requires paired data
(raw driver complaint → technician-verified repair) available only from proprietary commercial
databases. Confirm or refute this: is there **any** openly available or academic dataset that
pairs plain-language driver symptoms with verified repairs for 1990–2010 petrol vehicles? If
yes, provide the link, structure, and license terms. If no, restate the feasibility conclusion
citing current (2025–2026) sources.

## Gap 5 — Source-quality upgrades

Several numeric claims in the original research are currently backed by blogs or parts-retailer
pages. For each such claim, find a stronger primary source (SAE standard, EPA/NHTSA report, OEM
service bulletin, or peer-reviewed paper). Present these as old-source → better-source pairs.

---

## Output format

- Answer gap by gap, using the same numbering above.
- Present numeric results in **tables**, one value per row, with columns: item, value,
  direction (increase/decrease), measured-or-estimated, source URL.
- Write any equations as plain text or inline notation — **no images or figures**.
- State units explicitly (e.g. "% change vs baseline," "share of verified cases").
