---
chunk: o2-logic/05_bias-vs-real-truth-perception
topic: o2-logic
sources:
  - master_o2_sensor_guide.md §6 (sensor bias vs real mixture — the diagnostic rule)
  - master_o2_sensor_guide.md §8 (sensor↔analyser λ delta cross-check)
  - O2logic.md §Scenario-2 step 4 (wideband BIASED_OFFSET via λ_obd vs λ_chem)
consumer: COMLab perception-contradiction detector / truth-vs-perception override (PRD §5) — compares normalized_obd_lambda (perception) against GASLab lambda_chem (ground truth); emits perception_contradiction. Same fusion that fuel-trim chunk 07 feeds.
consumer_status: active
related: [[03_failure-modes-taxonomy]], [[04_normalized-lambda-translation]], [[../fuel-trim/07_trim-vs-gas-chemistry-crosscheck]]
---

# Bias vs real mixture — the truth-vs-perception rule

The single most important O₂ rule. The ECU's λ (perception) can disagree with
the analyser's Brettschneider λ (ground truth). COMLab's perception-contradiction
detector resolves the disagreement; this chunk supplies the decision table.

| Sensor (`normalized_obd_lambda`) | Tailpipe / Brettschneider λ_chem | Verdict |
|---|---|---|
| Lean | Rich or normal | **Sensor stuck low** — exhaust leak pre-sensor, silicone poisoning, circuit fault. ECU is feeding fuel into a fine engine. Surface `Exhaust_Air_Leak_Pre_Cat` or `STUCK_LEAN`. |
| Rich | Lean or normal | **Sensor stuck high** — silicone poisoning (most common), short-to-voltage, end-of-life. ECU is starving a fine engine. Surface `STUCK_RICH`. |
| Lean | Lean (λ_chem ≥ 1.05) | **Real lean** — vacuum leak, low fuel pressure, MAF under-read. Route to lean candidates (fuel-trim §4). |
| Rich | Rich (λ_chem ≤ 0.95) | **Real rich** — high fuel pressure, leaking injector, EVAP purge stuck open. Route to rich candidates (fuel-trim §4). |

## The contradiction trigger

```
| normalized_obd_lambda − lambda_chem | ≥ 0.08   ⟹  emit perception_contradiction
```

When gases are otherwise consistent, this delta is the COMLab contradiction
signal. The override resolution: **when in doubt, gas chemistry wins**
(truth-vs-perception, PRD §5 / master_gas_guide §3 rule 7).

**One caveat before declaring sensor bias:** a 5 % exhaust air leak shifts the
analyser λ ~0.05 lean (master_gas_guide §8.5). Rule out an exhaust leak before
attributing the disagreement to sensor bias — otherwise a real pre-cat leak is
misread as `STUCK_LEAN`.

## Wideband offset is detected here, not as a failure mode

A wideband sensor with a calibration-resistor or reference-voltage fault
reports a **constant λ offset** while the engine runs stoichiometrically. With
no narrowband-style switching to fail, the only way to catch it is this
cross-lab comparison: persistent `|λ_obd − 1.0| > 0.05` while GASLab confirms
`λ_chem ≈ 1.0`.

This chunk's `perception_contradiction` is the **interim** sink. v2 promotes
the offset to a first-class, two-stage expression (O2-FU-1): OBDLab emits
`o2_failure_mode = WIDEBAND_OFFSET_CANDIDATE`, and this detector confirms it
against `λ_chem` and routes to a `SENSOR_FAULT` wideband-calibration node —
turning a generic contradiction into a specific sensor verdict. New field +
named consumer ship together (see `03_failure-modes-taxonomy`).

> On a `SECONDARY_FUEL_TRIM` platform (see `02_upstream-vs-downstream-roles`),
> an in-tolerance λ agreement is *weak* evidence of a healthy upstream sensor —
> the downstream loop may be masking drift. The detector down-weights agreement
> accordingly.

Citation: decision table master_o2_sensor_guide.md §6; λ-delta ≥ 0.08 and
open-loop invalidity §8; exhaust-leak caveat master_gas_guide.md §8.5;
override master_gas_guide.md §3 rule 7 / PRD §5.


## Core Entities

- normalized_obd_lambda, lambda_chem, perception_contradiction, STUCK_LEAN, STUCK_RICH
- WIDEBAND_OFFSET_CANDIDATE, Exhaust_Air_Leak_Pre_Cat, SENSOR_FAULT
- COMLab perception-contradiction detector / truth-vs-perception override (consumer, active)

## Graph relations (explicit)

sensor-lean with rich-or-normal **lambda_chem** INDICATES **STUCK_LEAN**
sensor-rich with lean-or-normal **lambda_chem** INDICATES **STUCK_RICH**
abs(normalized_obd_lambda minus lambda_chem) >= 0.08 EMITS **perception_contradiction**
**lambda_chem** WINS over sensor perception (truth-vs-perception)
exhaust leak SHIFTS **lambda_chem** ~0.05 lean (rule out before **STUCK_LEAN**)
**WIDEBAND_OFFSET_CANDIDATE** CONFIRMED_AGAINST **lambda_chem** routes to **SENSOR_FAULT** node

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
