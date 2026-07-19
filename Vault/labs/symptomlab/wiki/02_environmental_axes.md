---
node_type: "wiki"
lab: "symptomlab"
module: "symptomlab"
subsystem: "environmental-axes"
implements:
  - "labs/symptomlab/symptomlab/models.py"
consumers:
  - "symptomlab: labs/symptomlab/symptomlab/validator.py SymptomValidator.validate (axis-enum validation)"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (engine_state / occurs_during)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_validator.py"
  - "labs/symptomlab/tests/unit/test_models.py"
tags: [symptomlab, finished, wiki]
source: "labs/symptomlab/wiki/02_environmental_axes.md"
---

# 2. The Three Environmental Context Axes

> **Chunk summary.** Every report carries the symptom pair (SYMWIKI-01) **and**
> three typed context values describing the conditions under which the symptom
> appears. These axes are kept orthogonal to the symptom so the same complaint
> under different conditions stays distinguishable. This note mirrors the three
> `StrEnum`s in `models.py`; it explains *why* each axis exists, not how the
> downstream engine re-weights candidates — that is COMLab-B.

## 2.1 Why context is a separate axis {#CONCEPT_AXES_ROLE}

A symptom alone is ambiguous: "rough idle" caused by a manifold gasket leak behaves
very differently when cold than when hot. Folding "cold" or "hot" into the symptom
sub-filter (as the legacy catalog did) collides with the temperature axis and
blurs the signal. Keeping context on its own axes preserves that separation:

```
   SymptomDNA
     ├─ tier_1 / tier_2          (the sensation — SYMWIKI-01)
     └─ environmental_conditions (the conditions — this note)
            ├─ occurs_during   : OccursDuring
            ├─ engine_state    : EngineState
            └─ load_state      : LoadState
```

The validator accepts only enum-member strings on each axis; anything else is
rejected at `validate()`.

# source: labs/symptomlab/symptomlab/models.py (EnvironmentalConditions)

## 2.2 `occurs_during` — temporal / thermal trigger {#CONCEPT_AXIS_OCCURS_DURING}

Mirrors `OccursDuring`. When in the symptom's life it shows up.

| Value | Meaning |
|---|---|
| `always` | Present continuously, independent of temperature or time. |
| `cold_only` | Appears on a cold engine and fades as it warms. |
| `hot_only` | Appears only once the engine is at operating temperature. |
| `intermittent` | Comes and goes without a clear thermal pattern. |

The thermal split is physically meaningful: elastomeric/paper gaskets shrink cold
and seal as they expand warm (so a `cold_only` rough idle leans toward a structural
vacuum leak), whereas electronic parts such as coils and position sensors break
down as winding resistance rises with heat (so `hot_only` stalls/hard-starts lean
toward ignition and sensor faults). The actual candidate promotion/demotion these
states drive is COMLab-owned — see §2.5.

# source: labs/dnalab/research/DNAresearch.md#Environmental Context Modifiers

## 2.3 `engine_state` — running mode {#CONCEPT_AXIS_ENGINE_STATE}

Mirrors `EngineState`. What the engine is doing when the symptom is reported.

| Value | Meaning |
|---|---|
| `running` | Engine has started and is running. |
| `cranking` | Starter is turning the engine but it has not caught. |
| `will_not_start` | Engine does not start at all. |

(`will_not_start` is the spelled-out enum value; the older `wont_start` label was
reconciled to it in code.)

# source: labs/symptomlab/symptomlab/models.py (EngineState)

## 2.4 `load_state` — mechanical load axis {#CONCEPT_AXIS_LOAD_STATE}

Mirrors `LoadState`. The mechanical load the engine is under when the symptom
appears.

| Value | Meaning |
|---|---|
| `idle` | Throttle closed, no road load. |
| `steady_cruise` | Constant-speed cruising under light, steady load. |
| `transient_acceleration` | Throttle opening, rising cylinder pressure. |
| `coasting_deceleration` | Throttle closed while the vehicle still rolls. |

### Why `load_state` exists (physical derivation) {#CONCEPT_LOAD_STATE_DERIVATION}

The legacy schema had only `occurs_during` and `engine_state`; it could not
distinguish a static air-metering fault from a transient load fault. For petrol
engines of the operating envelope (1990–2010, Euro 1 – Euro 5), manifold vacuum
behaves inversely to throttle opening:

```
            Vacuum  ∝  1 / (throttle valve opening)

   throttle CLOSED ─► manifold vacuum PEAKS  ─► engine pulls hard on any
   (idle, coasting)                              compromised gasket
                                                 → vacuum-leak-sensitive regime

   throttle OPEN   ─► manifold vacuum COLLAPSES ─► cylinder pressure rises,
   (acceleration)                                  spark must jump a denser gap
                                                 → coil-dielectric-stress regime
```

So at closed throttle (`idle`, `coasting_deceleration`) the engine is most
sensitive to unmetered air through a leak; under `transient_acceleration` the high
cylinder pressure raises the voltage needed to fire the plug, exposing weak coil
insulation. That single mechanism is why a *load* axis carries diagnostic signal
the two thermal/temporal axes cannot. The axis is supported by SAE J2944
(operational definitions of driving-performance measures).

# source: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=9101EUTV.TXT
# source: https://www.dinmedia.de/en/standard/sae-j-2944/365090629

## 2.5 What this note does NOT own {#CONCEPT_AXES_SPLIT}

This note owns the **axis vocabulary** the validator enforces. It does **not** own
the engine's re-weighting behaviour. How a given `load_state` or `occurs_during`
value promotes or demotes a candidate family — and the cap on how far a single
report may move the result — is COMLab-owned, registered as proposal **COMLab-B**
(consumer `FaultAtlasRouter.execute_triage_loop`). Adding a promotion weight here
would have no SymptomLab consumer and would be noise.

# source: labs/comlab/comlab/config/proposals/entries.yaml (COMLab-B)


## Graph relations (explicit)

**OccursDuring** ENUMERATES **always**, **cold_only**, **hot_only**, **intermittent**
**EngineState** ENUMERATES **running**, **cranking**, **will_not_start**
**LoadState** ENUMERATES **idle**, **steady_cruise**, **transient_acceleration**, **coasting_deceleration**
**EnvironmentalConditions** CONSUMES **OccursDuring**, **EngineState**, **LoadState**
**SymptomValidator.validate** VERIFIES **OccursDuring**, **EngineState**, **LoadState**
**COMLab-B** CONSUMES **occurs_during**, **load_state** (context modifier promotions/demotions + report-trust cap)
**cold_only** MAPS_TO **vacuum_leak_regime** (cold gasket contraction → unmetered air)
**hot_only** MAPS_TO **ignition_sensor_regime** (winding resistance rise → coil/sensor breakdown)
**idle** MAPS_TO **vacuum_leak_sensitive_regime** (closed throttle → peak manifold vacuum)
**transient_acceleration** MAPS_TO **coil_dielectric_stress_regime** (high cylinder pressure → denser spark gap)
**LoadState** DISAMBIGUATED_BY **manifold_vacuum_regime** (vacuum ∝ 1/throttle opening)
**occurs_during** IS_ORTHOGONAL_TO **symptom_catalog** (temperature states removed from Tier-2 into separate axis)


## Core Entities

- **OccursDuring** (StrEnum, live) — CONSUMED_BY **SymptomValidator.validate**, **EnvironmentalConditions** (symptomlab/symptomlab/models.py)
- **EngineState** (StrEnum, live) — CONSUMED_BY **SymptomValidator.validate**, **EnvironmentalConditions** (symptomlab/symptomlab/models.py)
- **LoadState** (StrEnum, live) — CONSUMED_BY **SymptomValidator.validate**, **EnvironmentalConditions** (symptomlab/symptomlab/models.py)
- **EnvironmentalConditions** (dataclass, live) — CONSUMED_BY **SymptomDNA** (symptomlab/symptomlab/models.py)
- **COMLab-B** (proposal) — CONSUMED_BY **FaultAtlasRouter.execute_triage_loop** (labs/comlab/comlab/config/proposals/entries.yaml)
