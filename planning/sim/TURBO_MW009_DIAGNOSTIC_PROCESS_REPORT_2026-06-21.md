# Turbo turbine-seal case — diagnostic process report

**Date:** 2026-06-21  
**Case:** P_NEW_13 / turbo turbine-side oil-seal leak  
**Vehicle profile:** Citroën 5FR / EP6CDT 1.6 THP, turbocharged GDI, Euro 5  
**VIN used by the simulation:** `VF7SA5FR8AW511081`  
**Final simulated verdict:** `MW-009` — Turbo turbine-seal oil leak  
**Simulated confidence:** `0.91`  
**Demand score:** `4.0` — tied for the most demanding oil-consumption case

## Executive finding

The case resolves because two apparently contradictory observations are combined:

1. In-cylinder combustion looks healthy: lambda remains almost exactly stoichiometric
   (`1.000` at idle and `1.002` at 2500 RPM), CO remains very low, and upstream fuel correction
   is nearly neutral.
2. The exhaust downstream of the cylinders behaves as if a rich hydrocarbon source remains
   present, including during deceleration fuel cut-off (DFCO), when injector fuel should be absent.

That contradiction places the oil source after the combustion chamber. On a turbocharged 5FR,
the modeled explanation is oil passing the turbocharger turbine-side seal into the hot exhaust
housing. The decisive presentation-simulation discriminator is `DFCO_NEGATIVE`: B1S2 trim reaches
`-14%` during fuel cut while the downstream sensor remains false-rich.

The case therefore follows this reasoning:

```text
healthy-looking combustion
        +
extreme tailpipe HC that falls with exhaust flow
        +
downstream rich response persisting during zero-fuel DFCO
        ↓
post-cylinder oil source
        ↓
turbo turbine-side seal leak
        ↓
MW-009
```

## 1. Physical failure model

The turbine-side turbo seal normally retains pressurized lubricating oil inside the turbo
center housing. In this case, oil is modeled as escaping directly into the hot turbine housing.
It therefore enters the exhaust after combustion rather than passing through the cylinder.

This location explains the central diagnostic pattern:

- The cylinders still burn the commanded petrol mixture correctly.
- The upstream wideband sensor sees lambda near `1.00`.
- Oil thermally cracks or burns in the exhaust and creates a large hydrocarbon load.
- The downstream narrowband sensor sees oxygen depletion and reports a false-rich condition.
- The secondary post-catalyst controller responds by commanding negative B1S2 correction.
- During DFCO, injected fuel stops but leaking oil can continue reaching the turbine housing.

The DFCO observation is unusually valuable because it separates oil-derived downstream
hydrocarbons from normal petrol combustion.

## 2. Evidence presented to the simulation

### Vehicle and sensor context

| Item | Value | Diagnostic role |
|---|---|---|
| Engine | 5FR / EP6CDT | Defines the turbo-GDI architecture |
| Induction | Turbocharged | Makes a turbine-side oil path physically possible |
| Upstream O₂ | Wideband AFR | Reports combustion lambda |
| Downstream O₂ | Narrowband 0–1 V | Reports post-catalyst oxygen condition |
| Downstream trim role | Secondary fuel trim | Supplies B1S2 STFT/LTFT behavior |

### Gas evidence

| Channel | Idle | 2500 RPM | Interpretation |
|---|---:|---:|---|
| HC | 720 ppm | 130 ppm | Extreme idle HC, then strong cleanup/dilution |
| CO | 0.07% | 0.09% | Very low; no rich in-cylinder combustion |
| CO₂ | 14.5% | 14.6% | Near healthy combustion output |
| O₂ | 0.5% | 0.4% | No false-lean combustion pattern |
| NOx | 28 ppm | 80 ppm | Rises with RPM; not the primary discriminator |
| Lambda | 1.000 | 1.002 | Combustion remains stoichiometric |

The low-to-high-idle HC reduction is `590 ppm`, approximately an `82%` drop. HC is extreme at
idle but does not remain high as exhaust flow increases. At the same time, lambda and CO remain
clean. This is inconsistent with a conventional rich-mixture fault and unlike worn rings, where
HC worsens under load in the authored case set.

### OBD and post-catalyst evidence

| Channel | Value | Interpretation |
|---|---:|---|
| STFT S1 | +1% | Primary fuel loop is nearly neutral |
| LTFT S1 | 0% | No learned in-cylinder rich/lean correction |
| Downstream S2 | 0.80 V | Downstream sensor reports rich |
| STFT B1S2 | -7% | Secondary loop pulls fuel |
| LTFT B1S2 | -5% | Persistent downstream negative bias |
| DFCO B1S2 | **-14%** | Strong negative response while injector fuel is cut |

The upstream total correction is only `+1%`, while normal downstream correction totals `-12%`.
The most specific observation is the `-14%` DFCO value, crossing the simulation's
`DFCO_NEGATIVE` threshold of `<= -10%`.

## 3. How the standalone simulation reached MW-009

### Stage 1 — gas classification

The simulation applies its gas-state rules in fixed order. The turbo case:

- does not meet the coolant-leak pattern;
- does not meet the valve-seal cleanup threshold because high-idle HC is `130`, not `<100`;
- does not meet the piston-ring pattern because idle HC is not low and HC does not rise;
- does meet `idle HC >= 500` and `high-idle HC < 250`.

It is therefore classified as:

```text
POA_SIGNATURE
```

This is deliberately a catch-all oil-aftertreatment family, not yet a specific root cause.
Gas chemistry establishes an oil-related abnormality but cannot by itself choose between the
PCV and turbo branches in the standalone presentation model.

### Stage 2 — post-catalyst signature

The simulation evaluates post-catalyst signatures in this order:

1. `DIVERGENT`
2. `DFCO_NEGATIVE`
3. `FIXED_NEGATIVE`
4. `TRANSIENT_NEGATIVE`
5. `NEUTRAL`

For this case:

- upstream trim sum = `+1 + 0 = +1%`;
- downstream trim sum = `-7 + -5 = -12%`;
- the divergent test fails because upstream correction is not `> +10%`;
- DFCO B1S2 is `-14%`, satisfying `<= -10%`.

The selected signature is therefore:

```text
DFCO_NEGATIVE
```

### Stage 3 — fault selection

The decision table then receives:

```text
gas state:       POA_SIGNATURE
post-cat state:  DFCO_NEGATIVE
```

Within the `POA_SIGNATURE` branch:

- `DIVERGENT` routes to PCV `MW-008`;
- `DFCO_NEGATIVE` routes to turbo seal `MW-009`.

The prediction matches the authored expected fault, so the result is `PASS`, with the
simulation-assigned confidence of `0.91`.

### Stage 4 — demand scoring

The demand score is calculated as:

| Component | Score |
|---|---:|
| Base gas chemistry | 1.0 |
| Ambiguous `POA_SIGNATURE` family | +1.0 |
| DFCO capture decoupled from combustion | +2.0 |
| **Total** | **4.0** |

This makes the turbo case demanding because diagnosis depends on a transient operating mode,
not merely a static idle sample.

## 4. Jaeger evidence

Jaeger trace:

```text
8855a7208a566366a2a9ba2dd8af09b3
```

Service:

```text
wiredv2-oil-case
```

The trace contains the intended four-span diagnostic narrative:

| Span | Recorded conclusion |
|---|---|
| `oil_case_turbo_turbine-seal_leak` | Expected and predicted `MW-009`; match `PASS`; demand `4.0` |
| `gas_state` | HC `720 → 130`, lambda `1.000 → 1.002`, state `POA_SIGNATURE` |
| `post_cat_trim` | B1S2 `-7/-5`, DFCO `-14`, S2 `0.80 V`, signature `DFCO_NEGATIVE` |
| `verdict` | `MW-009`, mechanical wear, confidence `0.91` |

This trace is the presentation simulation, not a trace from the current live COMLab registry.

## 5. How the production-oriented diagnostic path evolved

The workspace now contains a second, live registry route for `MW-009`. It was added through the
oil-consumption task sequence:

1. The original single-snapshot contract could not discriminate PCV from turbo.
2. GASLab and COMLab gained optional high-idle gas fields.
3. The integration shim gained resolvers for `high_idle_hc`, `high_idle_co`, and
   `high_idle_lambda`.
4. The live `MW-009` registry rule was added and tested.

The current live registry does not require post-cat B1S2 or DFCO. It routes the same authored
turbo shape using:

| Live rule evidence | Requirement |
|---|---|
| Chemical state | `POA_SIGNATURE` |
| Idle HC | `>= 500 ppm` |
| Idle CO | `< 0.15%` |
| Idle lambda | `0.99–1.01` |
| High-idle HC | `< 200 ppm` |

A focused live-registry run with the turbo payload selected `MW-009`; its three dedicated tests
passed on 2026-06-21:

```text
3 passed in 0.23s
```

The live registry produced confidence `1.0`, not `0.91`. This difference is expected:

- `0.91` is a fixed confidence authored into the standalone simulation.
- `1.0` is the live registry's computed score: base weight plus satisfied definitive evidence,
  clamped at the hard cap.

The values must not be treated as directly equivalent probability estimates.

## 6. Differential diagnosis

### Versus PCV stuck open (`MW-008`)

Both cases can show high idle HC followed by cleanup at 2500 RPM. The separation is:

| Feature | Turbo seal | PCV stuck open |
|---|---|---|
| Idle lambda | Stoichiometric (`1.000`) | Rich (`0.925`) |
| Idle CO | Very low (`0.07%`) | High (`1.90%`) |
| Upstream trims | Near neutral | Strongly positive |
| Post-cat pattern | DFCO-negative | Upstream/downstream divergent |
| Oil path | Directly into turbine exhaust housing | Through crankcase ventilation into intake |

The simulation uses the post-cat pattern. The live registry uses stoichiometric lambda and low CO.

### Versus worn piston rings (`MW-001`)

Rings introduce oil through the cylinder, so their authored HC increases with RPM/load
(`150 → 380 ppm`) and combustion becomes slightly rich at high idle (`lambda 0.985`).
The turbo case does the opposite: HC drops (`720 → 130 ppm`) while lambda remains stoichiometric.

### Versus valve stem seals (`MW-002`)

Valve seals also clean up with RPM, but their authored case begins with rich combustion
(`lambda 0.962`, CO `0.95%`) and high-idle HC falls below `100 ppm`. The turbo case retains
stoichiometric combustion and has the stronger post-cylinder/DFCO contradiction.

### Versus a mixture or injector fault

A petrol-rich fault should affect upstream lambda, CO, or primary fuel trims. Those channels are
nearly normal here. The abnormality appears downstream while combustion remains controlled.

## 7. Strengths of the diagnosis

- It explains the combination of extreme HC and nearly perfect lambda rather than treating
  high HC as automatically equivalent to rich combustion.
- It uses two operating points, preventing a single idle snapshot from carrying the verdict.
- The DFCO discriminator creates a zero-injected-fuel challenge condition.
- PCV and ring alternatives have explicit exclusion evidence.
- The standalone trace and generated JSON agree on all case values.
- The current live registry independently reproduces the `MW-009` verdict from gas-delta evidence.

## 8. Limitations and engineering findings

### The presentation simulation is not the real pipeline

The simulation explicitly mocks the post-cat-trim pipeline. Its B1S2 and DFCO values are authored
test inputs, not measurements collected from the real vehicle. The Jaeger trace proves deterministic
routing of those inputs; it does not prove that the vehicle has a failed turbo seal.

### The live registry and simulation use different decisive evidence

The simulation selects turbo through `DFCO_NEGATIVE`. The live registry currently selects turbo
through gas chemistry and the idle-to-2500 HC delta. Post-cat trim is therefore corroborating
future-state evidence in the presentation model, not a current live `MW-009` rule input.

### PCV is not hard-pruned for the turbo-shaped live payload

In the live registry, `MW-008` still scored approximately `0.92` for the turbo payload, while
`MW-009` won at `1.0`. The PCV rich-lambda condition is `SUGGESTIVE`, not `GATING`; therefore
stoichiometric lambda reduces PCV evidence but does not exclude the rule.

The current result is correct, but separation is score-based rather than a strict PCV rejection.
This is weaker than wording in the R5 task that says rich lambda “excludes turbo.” Any future
weight changes should retain a regression test that the turbo payload cannot be stolen by `MW-008`.

### Forced induction is not a hard live guard

The 5FR case is known to be turbocharged, but the live registry intentionally treats forced
induction as corroborating context rather than a required gate. This avoids false negatives from
missing VIN data, but it also means a non-turbo payload with the same gas signature could reach
`MW-009`. A future architecture-aware guard remains a separate design decision.

### Trace observability is simulation-specific

The Jaeger gas span records HC and lambda but omits CO, even though low CO is central to the live
registry route. It also does not show live-registry candidate competition. A production trace
should identify the actual route used and record the decisive evidence rows without exposing
unnecessary payload data.

## 9. Required real-vehicle confirmation

Before authorizing turbo replacement, the software verdict should be followed by physical checks:

1. Reproduce the symptom after prolonged idle and during controlled deceleration.
2. Confirm that injector fuel cut is genuinely active during the DFCO sample.
3. Verify upstream lambda and primary trims remain normal while downstream rich behavior persists.
4. Inspect the exhaust downpipe immediately after the turbine for wet oil or heavy oil deposits.
5. Inspect compressor/intercooler plumbing to distinguish turbine-side from compressor-side leakage.
6. Check crankcase pressure and the integrated PCV system before condemning the turbo.
7. Check turbo shaft condition, oil feed/return restriction, and boost-control behavior.
8. Assess downstream O₂ sensor and catalyst contamination; oil poisoning may create secondary faults.

These checks convert the analytical verdict into a defensible repair decision and reduce the risk
of replacing the turbo when PCV or oil-return conditions are the actual cause.

## 10. Final assessment

The turbo case is a strong presentation case because the engine appears healthy if only upstream
combustion is examined. The diagnosis emerges only after the system recognizes that the hydrocarbon
source is downstream of the cylinders.

For the presentation simulation, the decisive sequence is:

```text
POA_SIGNATURE + DFCO_NEGATIVE → MW-009
```

For the current live registry, the decisive sequence is:

```text
POA_SIGNATURE
+ HC >= 500
+ CO < 0.15
+ lambda 0.99–1.01
+ high-idle HC < 200
→ MW-009
```

Both paths reach the same root cause through independent but compatible reasoning. The simulation
demonstrates the stronger future-state DFCO story; the live rule demonstrates that the case is
already routable through the shipped two-point gas contract.

## Sources inspected

- `planning/sim/oil_burn_5fr_sim.py`
- `planning/sim/oil_burn_5fr_results.json`
- `planning/OIL_CASE_SIGNATURES_5FR.md`
- `planning/OilburnCases.md`
- `planning/oil_consumption/PROGRESS.md`
- `planning/oil_consumption/tasks/T-OIL-R5.md`
- `labs/vinlab/tasks/5fr.md`
- `labs/gaslab/wiki/06a_fault_atlas_oil_mechanical.md`
- `labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md`
- `labs/comlab/registry/rules/mechanical_wear.json`
- `labs/comlab/registry/integration_shim.py`
- `labs/comlab/registry/tests/test_turbo_rule.py`
- Jaeger service `wiredv2-oil-case`, trace `8855a7208a566366a2a9ba2dd8af09b3`
