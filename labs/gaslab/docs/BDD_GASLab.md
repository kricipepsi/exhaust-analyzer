# BDD — GASLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-10
**Authored from:** `_skills/doc/BDD.md` (Gherkin Given/When/Then, declarative, one behaviour per scenario)
**Code baseline:** GASLab v2.1 (34-value surface, dual-RPM input)

These are **executable specifications** for GASLab's observable behaviour at the `gaslab.process.process()` boundary. Each scenario is declarative — it states what the system does for a given exhaust reading and DNA view, never how. Every feature names the test module that exercises it, so the scenarios stay honest against `pytest`. Numeric values are illustrative of the documented bands (see LLD §4, §6); they are not new thresholds.

A shared vocabulary used throughout:

- **A reading** = the five analyser inputs (HC ppm, CO/CO₂/O₂ vol%, NOx ppm).
- **A high-idle reading** = an optional second reading taken at 2500 RPM (`reading_high`).
- **A DNA view** = the 13-field `GasLabDnaView` slice for the vehicle.
- **The verdict** = `(chemical_state, sample_validity)` carried in `GasLabPayload`.

---

## Feature: Sample validity gating
*Tests: `unit/test_validity_gates.py`, `unit/test_rule_engine.py`*

```gherkin
Scenario: A clean idle sample is accepted
  Given a reading whose CO + CO2 + O2 sums to between 14 and 16
    And CO + CO2 is above the 6% dilution floor
  When the reading is classified
  Then sample_validity is VALID
    And classification proceeds to fault matching

Scenario: A diluted or contaminated sample halts the diagnosis
  Given a reading whose CO + CO2 + O2 is below 14 or above 18
  When the reading is classified
  Then chemical_state is SAMPLE_INVALID
    And sample_validity is INVALID

Scenario: An air-rich sample is flagged but not rejected
  Given a reading whose CO + CO2 + O2 sums to between 16 and 18
  When the reading is classified
  Then sample_validity is EXTERNAL_O2_SUSPECT
    And the diagnosis continues with that warning

Scenario: A sample that passes the triangle but fails dilution is rejected
  Given a reading inside the triangle band
    But CO + CO2 is at or below 6%
  When the reading is classified
  Then sample_validity is INVALID
```

---

## Feature: Brettschneider lambda as ground truth
*Tests: `unit/test_brettschneider.py`*

```gherkin
Scenario: A stoichiometric burn reads near unity
  Given a clean stoichiometric reading
  When lambda is computed from chemistry
  Then lambda_chem is approximately 1.000

Scenario: A misfiring cylinder does not fool lambda
  Given a reading with high HC and high O2 in stoichiometric proportion
  When lambda is computed from chemistry
  Then lambda_chem stays near 1.000
  # misfire-immunity: raw fuel and raw air leave together (GAS_WIKI §4.3)

Scenario: NOx is included when the analyser reports it
  Given a reading with a non-zero NOx channel
  When lambda is computed from chemistry
  Then the NOx correction term is added to the 4-gas lambda

Scenario: A degenerate all-zero sample returns a safe value
  Given a reading whose carbon sum is zero
  When lambda is computed from chemistry
  Then lambda_chem is the 1.0 sentinel
    And validity gating independently flags SAMPLE_INVALID
```

---

## Feature: Definitive overrides fire in priority order
*Tests: `unit/test_rule_engine.py`*

```gherkin
Scenario: Combustion gases in the coolant are caught only with the block test
  Given a reading with suppressed CO2 and elevated HC
    And the technician has confirmed a positive block test
  When the reading is classified
  Then chemical_state is COOLANT_LEAK_INTERNAL

Scenario: The same chemistry without the block test does not claim a coolant leak
  Given a reading with suppressed CO2 and elevated HC
    And no block test has been performed
  When the reading is classified
  Then chemical_state is not COOLANT_LEAK_INTERNAL

Scenario: An ignition misfire is confirmed by the oxygen spike
  Given a reading with very high HC, high O2, and suppressed NOx
    And the O2 spike is consistent with at least one dropped cylinder for this cylinder count
  When the reading is classified
  Then chemical_state is IGNITION_MISFIRE

Scenario: A collision pattern with low HC routes to an air leak
  Given a reading where both CO and O2 are elevated
    And the triangle sum is above 16
    And HC is normal
  When the reading is classified
  Then chemical_state is EXHAUST_AIR_LEAK
    And sample_validity is EXTERNAL_O2_SUSPECT

Scenario: A collision pattern with high HC stays a rich misfire
  Given a reading where both CO and O2 are elevated
    And HC is above the normal ceiling
  When the reading is classified
  Then chemical_state is RICH_MISFIRE
```

---

## Feature: Fuel-trim disambiguates an air-rich leak
*Tests: `unit/test_rule_engine.py`, `unit/test_resolution.py`*

```gherkin
Scenario: A leak chemistry with strong positive trim is a real air leak
  Given a reading in the EXTERNAL_O2_SUSPECT band matching leak chemistry
    And a short-term fuel trim above 8%
  When the reading is classified
  Then chemical_state is EXHAUST_AIR_LEAK

Scenario: The same chemistry without compensating trim is treated as a bad sample
  Given a reading in the EXTERNAL_O2_SUSPECT band matching leak chemistry
    And a short-term fuel trim at or below 8%
  When the reading is classified
  Then chemical_state is SAMPLE_INVALID
```

---

## Feature: DNA gates suppress impossible faults
*Tests: `unit/test_rule_engine.py`, `unit/test_resolution.py`, `unit/test_ontology.py`*

```gherkin
Scenario: A catalyst fault is impossible on a catalyst-free vehicle
  Given a reading whose chemistry matches a catalyst fault
    And a DNA view where has_catalyst is false
  When the reading is classified
  Then no CATALYST_* signature survives resolution

Scenario: A GDI fault is impossible on a port-injected vehicle
  Given a reading whose chemistry matches a GDI fault
    And a DNA view where fuel_delivery_type is not GDI
  When the reading is classified
  Then no GDI_* signature survives resolution

Scenario: An EGR fault is impossible on a vehicle without EGR
  Given a reading whose chemistry matches an EGR fault
    And a DNA view where egr_equipped is false
  When the reading is classified
  Then no EGR_STUCK_* signature survives resolution
```

---

## Feature: Per-vehicle CoC targets reshape the normal window
*Tests: `unit/test_rule_engine.py`, `unit/test_dna_view.py`*

```gherkin
Scenario: A certified lambda target tightens the normal band
  Given a DNA view carrying target_lambda_v112
  When NORMAL_OPERATION bounds are evaluated
  Then the lambda window is centred on v112 plus or minus 0.005
    And it is clamped within 0.85 and 1.15

Scenario: A per-vehicle idle CO ceiling overrides the Euro default
  Given a DNA view carrying co_low_idle
  When NORMAL_OPERATION bounds are evaluated
  Then the CO ceiling uses the per-vehicle value rather than the Euro-scaled default

Scenario: A wideband upstream sensor recalibrates the O2-bias signatures
  Given a DNA view whose upstream_o2_type contains "wideband"
  When O2_SENSOR_BIASED_LOW or _HIGH bounds are evaluated
  Then their CO and lambda windows use the wideband calibration
```

---

## Feature: RPM-differential separation of the cam-timing family
*Tests: `unit/test_resolution.py`, `unit/test_t_p8_7_hc_discriminator.py`, `unit/test_rule_engine_reachability.py`*

```gherkin
Scenario: A retarded-cam MAF lean persists at high idle
  Given a lean idle reading matching the cam-MAF pattern
    And a high-idle reading where the lean condition persists
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_RETARDED_MAF

Scenario: A vacuum lean that normalises at high idle is not cam timing
  Given a lean idle reading
    And a high-idle reading where lambda normalises toward 1.0 and O2 falls below 1%
  When the reading is classified with both readings
  Then chemical_state is LEAN_MIXTURE
    And CAM_TIMING_RETARDED_MAF does not survive

Scenario: An advanced cam shows rising NOx and falling HC into high idle
  Given a rough idle reading with a mild-lean lambda offset
    And a high-idle reading where NOx rises while HC and CO fall
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_ADVANCED

Scenario: A retarded-cam MAP rich condition partially normalises at high idle
  Given a rich idle reading matching the Speed-Density over-fuel pattern
    And a high-idle reading where lambda rises toward 1.0 and CO falls
  When the reading is classified with both readings
  Then chemical_state is CAM_TIMING_RETARDED_MAP

Scenario: An over-advanced ignition shows a clean idle with a NOx-only spike
  Given a clean idle reading
    And a high-idle reading whose only abnormality is a very high NOx spike
  When the reading is classified with both readings
  Then TIMING_OVER_ADVANCED is among the survivors

Scenario: A confirmed cam timing prunes generic low-HC misfire noise
  Given a confirmed cam-timing survivor
    And a co-surviving generic misfire candidate whose HC is below the misfire floor
  When resolution completes
  Then the generic misfire candidate is dropped as overlap noise
```

---

## Feature: Catalyst weak-versus-dead routing needs two speeds
*Tests: `unit/test_resolution.py`*

```gherkin
Scenario: A catalyst weak at idle but working at high idle is not lighting off
  Given a catalyst-equipped vehicle with healthy fuel control at both speeds
    And an idle reading showing weak catalyst chemistry
    And a high-idle reading showing a working catalyst
  When the reading is classified with both readings
  Then chemical_state is CATALYST_NOT_LIGHTING_OFF

Scenario: A catalyst degraded at both speeds is overwhelmed
  Given a catalyst-equipped vehicle with healthy fuel control at both speeds
    And both readings show dead-catalyst chemistry
  When the reading is classified with both readings
  Then chemical_state is CATALYST_OVERWHELMED

Scenario: Bad fuel control rejects any catalyst verdict
  Given a catalyst-equipped vehicle whose lambda is outside 0.98 to 1.02 at either speed
  When the reading is classified with both readings
  Then no CATALYST_* signature survives
```

---

## Feature: Mechanical-wear family resolves to a leaf
*Tests: `unit/test_resolution.py`*

```gherkin
Scenario: HC that drops sharply into high idle points to worn valve seals
  Given an idle reading with moderate HC
    And a high-idle reading where HC drops sharply and CO stays clean
  When the reading is classified with both readings
  Then chemical_state is WORN_VALVE_SEALS

Scenario: HC that climbs under load points to worn piston rings
  Given an idle reading with low HC
    And a high-idle reading where HC rises and CO climbs
    And a strongly negative fuel trim when trim is available
  When the reading is classified with both readings
  Then chemical_state is WORN_PISTON_RINGS

Scenario: A wear pattern with no matching leaf drops the whole family
  Given a co-surviving mechanical-wear family
    And no idle-to-high-idle pattern matches a specific leaf
  When resolution completes
  Then no WORN_* or POA_SIGNATURE candidate remains
```

---

## Feature: Deterministic candidate ranking
*Tests: `unit/test_rank_candidates.py`, `unit/test_rule_engine.py`*

```gherkin
Scenario: The narrowest signature wins over a broader one
  Given two surviving candidates that both match the reading
    And neither is a catch-all
  When the verdict is chosen
  Then the candidate with the narrower total signature width is emitted

Scenario: Catch-all signatures are chosen last
  Given a specific fault and a catch-all fault both match
  When the verdict is chosen
  Then the specific fault is emitted and the catch-all is not

Scenario: No surviving candidate yields normal operation
  Given a reading that matches no fault signature after resolution
  When the verdict is chosen
  Then chemical_state is NORMAL_OPERATION

Scenario: Identical candidates resolve deterministically
  Given two candidates that tie on every ranking key
  When the verdict is chosen
  Then the winner is the one declared first in the ontology
    And the result is identical across process restarts
```

---

## Feature: The payload contract is always honoured
*Tests: `unit/test_process.py`, `unit/test_contracts.py`*

```gherkin
Scenario: Every diagnosis emits a complete, in-bounds payload
  Given any valid reading and DNA view
  When the diagnosis completes
  Then GasLabPayload carries chemical_state, the five gases, lambda_chem, and sample_validity
    And every numeric field is within its declared Pydantic range

Scenario: A directly-measured lambda is passed through when supplied
  Given a context carrying lambda_measured
  When the diagnosis completes
  Then the payload's lambda_measured equals the supplied value
  # consumer: COMLab perception-contradiction detector, no-OBD path (T-FX-7)

Scenario: No directly-measured lambda leaves the field null
  Given a context without lambda_measured
  When the diagnosis completes
  Then the payload's lambda_measured is null
```

---

## Red–Green–Refactor note (Iron Law)

Per `_skills/doc/BDD.md`, no production code in `gaslab/` ships without a failing test first. Each scenario above corresponds to one or more cases in the named `tests/unit/` module; the `tests/generative/` suite (boundary, combinatorial, fuzz, noise, overlap) then asserts these behaviours hold as **properties** across the synthetic grid, not just at the worked examples. A new fault or field follows the same cycle: write the scenario and its failing test, add the ontology entry and the named COMLab consumer, then make it green — never the reverse.
