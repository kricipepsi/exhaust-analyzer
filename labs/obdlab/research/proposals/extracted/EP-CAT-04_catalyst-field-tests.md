---
proposal_id: EP-CAT-04
title: Catalyst field-test inputs (backpressure, IR Δ-temp, Mode 06 monitor)
target_lab: catalyst (input fields) → COMLab
source: sources/o2-logic/master_catalyst_guide.md §5-6
type: input_field
status: PROPOSAL (named consumer; manual-entry physical tests)
date_extracted: 2026-06-07
---

## What it proposes
Manual-entry physical confirmation inputs for catalyst verdicts:
- **Backpressure:** idle ≤ 1.5 psi, 2500 RPM ≤ 3.0 psi (snap ≤ 5 psi); above ⇒ substrate
  restriction.
- **IR Δ-temp:** outlet ≥ 20 °C above inlet ⇒ converting; outlet ≤ inlet ⇒ dead.
- **Mode 06 cat monitor:** test value vs OEM threshold (within 10 % = borderline; 50 %+
  from threshold = genuinely failed).
- **Misfire-rate >1 %** = catalyst-meltdown boundary (Type A monitor calibration).

## Diagnostic rationale
Confirms a real failure before recommending replacement and feeds the false-P0420 demotion.

## Proposed consumer + code path
COMLab catalyst routing reads these as optional manual inputs. Numeric thresholds carry
wiki citations if they enter gaslab/obdlab code.

## Related
[[EP-CAT-03_false-p0420-cluster]] · [[EP-OBD-IN-07_per-cylinder-misfire-counts]] (1 % rule).
