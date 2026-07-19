# BDD — DTCLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-11
**Scope:** Behaviour specification for the DTCLab v2 pipeline and Phase-2 scorer

Format: Gherkin (`Given / When / Then`) per `_skills/doc/BDD.md`. Scenarios are declarative,
business-focused executable specifications — one behaviour each. Every scenario maps to shipped
behaviour and its backing test in `labs/dtclab/tests/`; the mapping is named under each feature so
the design→code→test spine stays explicit.

Convention reminder (the Iron Law): no production behaviour ships without a failing test first.
These scenarios are the source examples those tests encode.

---

## Feature: DTC ingestion gate
*Backing tests: `tests/unit/test_dtc_ingestion_gate.py`.*

```gherkin
Scenario: A well-formed confirmed DTC list passes through unchanged
  Given a Mode "$03" list ["P0171", "P0300", "U0100"]
  When the ingestion gate validates the list for mode "$03"
  Then the same list is returned unchanged

Scenario: The first malformed code fails fast
  Given a Mode "$03" list ["P0171", "p0300", "P0420"]
  When the ingestion gate validates the list
  Then a DTCFormatError is raised for "p0300"
  And no later code in the list is evaluated

Scenario: An unrecognised OBD mode is rejected before any code is checked
  Given any DTC list
  When the gate is asked to validate it for mode "$05"
  Then a ValueError is raised naming the three valid modes "$03", "$07", "$0A"

Scenario Outline: Canonical regex accepts and rejects exact forms
  Given the code "<code>"
  When it is validated for mode "$03"
  Then it is <verdict>

  Examples:
    | code    | verdict   |
    | P0171   | accepted  |
    | U0100   | accepted  |
    | p0171   | rejected  |  # lowercase system byte
    | P017    | rejected  |  # too short
    | P01711  | rejected  |  # too long
    | X0171   | rejected  |  # invalid system byte
    | P0A71   | accepted  |  # uppercase hex is valid
    | P0a71   | rejected  |  # lowercase hex
```

---

## Feature: Freeze-frame extraction and symptom flags
*Backing tests: `tests/unit/test_freeze_frame_extractor.py`.*

```gherkin
Scenario: A complete snapshot yields a validated record
  Given a raw Mode $02 snapshot containing all 12 mandatory PIDs
  When the freeze frame is extracted
  Then a FreezeFrameRecord is returned
  And numeric strings are coerced (e.g. "800" becomes 800)
  And "OL_FAULT" is coerced to FuelSystemStatus.OL_FAULT

Scenario: A missing mandatory PID is reported with the exact gap
  Given a raw snapshot missing "maf_gps"
  When the freeze frame is extracted
  Then a FreezeFrameIncompleteError is raised
  And its missing attribute lists "maf_gps"

Scenario Outline: Derived symptom flags fire at their thresholds
  Given a snapshot where <condition>
  When the freeze frame is extracted
  Then <flag> is True

  Examples:
    | condition                                            | flag                     |
    | fuel_system_status is OL_FAULT                       | ff_open_loop_at_fault    |
    | calculated_load_pct = 71 and engine_rpm = 1400       | ff_load_high_at_low_rpm  |
    | coolant_temp_c = 59                                  | ff_ect_warmup            |
    | intake_air_temp_c - coolant_temp_c = 31, engine_rpm 0| ff_iat_ect_biased        |
    | ignition_advance_deg = -11                           | ff_timing_retard_severe  |

Scenario: Clearing codes this session invalidates the snapshot
  Given a complete snapshot and codes_cleared = True
  When the freeze frame is extracted
  Then ff_codes_cleared_invalidated is True
```

---

## Feature: Historical fault-context classification
*Backing tests: `tests/unit/test_historical_context_classifier.py`.*

```gherkin
Scenario: Cold start dominates idle and load context
  Given coolant_temp_c = 50, engine_rpm = 800, calculated_load_pct = 20
  When the historical context is classified
  Then the result is COLD_START_TRANSIT_FAULT
  And idle/load conditions are not evaluated

Scenario: Idle fault requires both low RPM and low load
  Given coolant_temp_c = 90, engine_rpm = 900, calculated_load_pct = 20
  When the historical context is classified
  Then the result is HISTORICAL_IDLE_FAULT

Scenario: The 60 degree boundary is exclusive
  Given coolant_temp_c = 60, engine_rpm = 2500, calculated_load_pct = 50
  When the historical context is classified
  Then the result is HISTORICAL_LOAD_FAULT
  And it is not COLD_START_TRANSIT_FAULT
```

---

## Feature: Mode $06 monitor evaluation
*Backing tests: `tests/unit/test_mode06_evaluator.py`.*

```gherkin
Scenario Outline: Margin is classified into the tri-state
  Given a Mode $06 margin of <margin>
  When the monitor is evaluated
  Then its state is <state>

  Examples:
    | margin | state                  |
    | -3.0   | CRITICAL_FAIL          |
    | 0.0    | CRITICAL_FAIL          |  # boundary owned by fail side
    | 8.0    | PENDING_FAIL_MARGINAL  |
    | 15.0   | PENDING_FAIL_MARGINAL  |  # inclusive upper
    | 16.0   | PASSED                 |

Scenario: A known MID resolves its target component
  Given the monitor key "MID_21_TID_81"
  When the monitor is evaluated against the hex dictionary
  Then the target_component is "Catalyst OSC Bank 1"

Scenario: An unknown MID resolves to UNKNOWN, not an error
  Given the monitor key "MID_FF_TID_01"
  When the monitor is evaluated
  Then the target_component is "UNKNOWN"

Scenario: A malformed monitor key is rejected
  Given the monitor key "MID_A2"
  When the monitor is evaluated
  Then a ValueError naming the MID_<HEX>_TID_<HEX> form is raised
```

---

## Feature: Routing-tag mapping with DNA gates
*Backing tests: `tests/unit/test_routing_tag_mapper.py`, `tests/integration/test_dtclab_pipeline.py`.*

```gherkin
Scenario: Ungated DTCs always map to their tag
  Given confirmed DTCs ["P0171", "P0300"]
  When the DTCs are mapped to routing tags
  Then the tags include LEAN_HISTORY and MISFIRE_HISTORY

Scenario: A catalyst code on a catalyst-equipped vehicle (HIGH confidence) emits
  Given a HIGH-confidence DNA view with has_catalyst = True
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags include CATALYST_HISTORY

Scenario: A catalyst code on a non-catalyst vehicle (HIGH confidence) is suppressed
  Given a HIGH-confidence DNA view with has_catalyst = False
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags do not include CATALYST_HISTORY

Scenario: A low-confidence VIN never suppresses a real DTC
  Given a NONE-confidence DNA view (or dna_view = None)
  And confirmed DTCs ["P0420"]
  When the DTCs are mapped
  Then the tags include CATALYST_HISTORY

Scenario Outline: The gpf_combined compound gate
  Given a HIGH-confidence DNA view with has_particulate_filter = <filter>
  And resolved_horizon = <horizon>
  And confirmed DTCs ["P244A"]
  When the DTCs are mapped
  Then GPF_HISTORY is <result>

  Examples:
    | filter | horizon          | result      |
    | True   | HORIZON_MODERN   | present     |
    | True   | HORIZON_CLASSIC  | suppressed  |
    | False  | HORIZON_MODERN   | suppressed  |

Scenario: POA_HISTORY is never emitted by the mapper
  Given any set of confirmed DTCs
  When the DTCs are mapped
  Then POA_HISTORY is never in the result
  # POA_HISTORY is injected by COMLab on GASLab POA_SIGNATURE (T-FX-3)
```

---

## Feature: Cross-field coolant/fluid signatures (pipeline step 5b)
*Backing tests: `tests/integration/test_dtclab_pipeline.py`, `tests/regression/test_dtclab_regression.py`.*

```gherkin
Scenario: Thermostat code while in open-loop-fault flags coolant malfunction
  Given confirmed DTCs include "P0128"
  And the freeze frame fuel_system_status is OL_FAULT
  When the full pipeline runs
  Then routing_tags include COOLANT_SYSTEM_MALFUNCTION

Scenario: A misfire code while in closed loop flags a fluid-quench misfire
  Given confirmed DTCs include "P0301"
  And the freeze frame fuel_system_status is CL
  When the full pipeline runs
  Then routing_tags include CYLINDER_FLUID_MISFIRE

Scenario: The same misfire code in open loop does NOT flag fluid quench
  Given confirmed DTCs include "P0301"
  And the freeze frame fuel_system_status is OL
  When the full pipeline runs
  Then routing_tags do not include CYLINDER_FLUID_MISFIRE
```

---

## Feature: Payload assembly and contract validation
*Backing tests: `tests/unit/test_payload.py`.*

```gherkin
Scenario: A valid payload round-trips through JSON
  Given a fully populated DTCLabPayload
  When it is serialised and re-parsed
  Then the re-parsed payload equals the original

Scenario: A malformed DTC in the payload is rejected with a contract code
  Given a payload whose confirmed_dtcs contains "p0171"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-001

Scenario: An invalid routing tag is rejected with a contract code
  Given a payload whose routing_tags contains "NOT_A_TAG"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-002
```

---

## Feature: Phase-2 candidate scoring
*Backing tests: `tests/unit/test_rank_candidates.py`, `tests/unit/test_classify_top3.py`.*

```gherkin
Scenario: A confirmed DTC scores its family as DEFINITIVE at full weight
  Given a payload whose confirmed_dtcs map to lean_condition
  When candidates are ranked
  Then lean_condition has raw_confidence 1.0
  And its match_type is DEFINITIVE

Scenario: A pending-only DTC scores its family as INDICATIVE
  Given a payload whose only evidence is a pending DTC mapping to misfire
  When candidates are ranked
  Then misfire has raw_confidence 0.5
  And its match_type is INDICATIVE

Scenario: A DNA-gated family is down-weighted when VIN confidence is PARTIAL
  Given a catalyst_failure candidate at weight 1.0
  And a PARTIAL-confidence DNA view
  When candidates are ranked
  Then catalyst_failure raw_confidence is 0.7   # 1.0 x 0.7 DNA factor

Scenario: classify_top3 clamps, dedups, and caps at three families
  Given candidates spanning five distinct families
  When classify_top3 is called
  Then at most three (family, confidence) pairs are returned
  And every confidence is within [0, 1]
  And the list is sorted by descending confidence then family name
  And the confidences are NOT normalised to sum to 1
```

---

## Feature: Lab isolation (cross-cutting invariant)
*Backing tests: `tests/unit/test_dna_view.py` (import audit).*

```gherkin
Scenario: DTCLab imports nothing from a sibling lab
  Given the dtclab package source
  When its imports are audited
  Then there is no import from gaslab, obdlab, comlab, or dnalab
  And the DNA view it consumes is its own local mirror
```
