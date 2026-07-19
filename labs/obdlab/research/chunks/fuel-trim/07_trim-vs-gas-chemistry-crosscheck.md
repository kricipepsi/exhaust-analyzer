---
chunk: fuel-trim/07_trim-vs-gas-chemistry-crosscheck
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §7
consumer: COMLab truth-vs-perception override (PRD_4D_App.md §5) — gas-chemistry λ is ground truth, trim is ECU perception; this table is the fusion rule that COMLab applies when GAS and OBD disagree
consumer_status: active
cross_topic: o2-logic
dedup: canonical truth-vs-perception trim table; the GAS-side λ definition lives in GASLab, mirrored locally by COMLab (no cross-lab import)
---

# Trim direction vs gas chemistry — the cross-check rule

The 4D **Truth-vs-Perception** override (`PRD_4D_App.md §5`): when fuel trim and
gas chemistry disagree, **gas chemistry (Brettschneider λ from the analyser) is
ground truth**; trim is *what the ECU thinks is happening*.

| Gas λ | Trim direction | Verdict |
|---|---|---|
| ≤ 0.95 (rich) | Negative | Agreement — real rich condition |
| ≤ 0.95 (rich) | Positive | **Contradiction** — ECU over-fuelling because pre-cat O₂ reads lean. Suspect O₂ bias or exhaust leak before sensor (`master_o2_sensor_guide.md §6`) |
| ≥ 1.05 (lean) | Positive | Agreement — real lean condition |
| ≥ 1.05 (lean) | Negative | **Contradiction** — ECU subtracting fuel because pre-cat O₂ reads rich. Suspect O₂ silicone poisoning or wideband bias |
| 0.97–1.03 (stoich) | within ±10 % | Healthy |
| 0.97–1.03 (stoich) | > ±15 % | ECU fighting an unknown disturbance — suspect `ECU_Logic_Inversion` or a biased-reference sensor |

**Consumer note (signal/noise).** This is the single most important fuel-trim
consumer: it is the COMLab fusion rule, not an OBD-internal rule. OBDLab emits the
trim direction (`02_sign-convention`); GASLab emits λ; **COMLab** mirrors both
types locally and applies this table. The "Contradiction" rows are exactly what
make trim a *perception* channel rather than ground truth — they justify OBDLab
emitting trim at all under the signal/noise rule.

Citation: PRD_4D_App.md §5 (truth-vs-perception override); Brettschneider λ
(GASLab analyser); λ bands 0.95 / 1.05 / 0.97–1.03 per master_fuel_trim_guide.md §7.


## Core Entities

- lambda_chem, POSITIVE_TRIM, NEGATIVE_TRIM, ECU_Logic_Inversion
- COMLab truth-vs-perception override (consumer, active)

## Graph relations (explicit)

**lambda_chem** IS_GROUND_TRUTH over trim perception
**RICH_MIXTURE** lambda with **POSITIVE_TRIM** INDICATES **O2_BIAS** or pre-sensor exhaust leak
**LEAN_MIXTURE** lambda with **NEGATIVE_TRIM** INDICATES **O2_BIAS**
stoich lambda with trim above +/-15% INDICATES **ECU_Logic_Inversion**
**trim-vs-gas-chemistry crosscheck** CONSUMED_BY **COMLab truth-vs-perception override**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
