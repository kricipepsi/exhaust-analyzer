
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Freeze-frame extraction and symptom flags · Parent document: BDD_DTCLab.md
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


## Graph relations (explicit)

**Feature: Freeze-frame extraction and symptom flags** DESCRIBES **DTCLab BDD v1.0**
**test_freeze_frame_extractor.py** VERIFIES **Feature: Freeze-frame extraction and symptom flags**
