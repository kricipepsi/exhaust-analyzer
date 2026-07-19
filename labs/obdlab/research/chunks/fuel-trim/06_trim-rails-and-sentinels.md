---
chunk: fuel-trim/06_trim-rails-and-sentinels
topic: fuel-trim
sources:
  - master_fuel_trim_guide.md §6
  - Research10.md §2 (±127/±99 sentinel meaning)
consumer: COMLab trim-validity gating — pegged/frozen/reset states demote or invalidate trim-derived candidates before fault-atlas routing consumes them
consumer_status: active
dedup: canonical rails/sentinel rule; supersedes scattered "pegged value" notes in Fuel Trim Diagnostics.txt
---

# Trim rails and sentinels

- **±25 %** — typical OBD-II DTC trigger point. Beyond this the ECU stops learning.
- **±127 %** — absolute signed-8-bit register maximum. Treat as "very large
  deviation, magnitude unknown". **±99 %** scan-tool readings mean the ECU is
  commanding maximum correction; both are **sentinel/range-limit** values, not
  physically plausible measured trims, and are rare in normal closed loop with a
  healthy sensor (Research10 §2).
- **Frozen at last value** — during open-loop operation (cold-start, WOT,
  decel-fuel-cut, O₂ fault) the ECU does not update trims. Per
  `master_cold_start_guide.md §1`, do **not** interpret trim when
  `fuel_sys_status = OL` (open loop). See `08_validity-preconditions`.
- **Reset to zero** — after codes cleared or battery disconnect, LTFT resets and
  the ECU relearns over ~1 drive cycle. Do not draw conclusions from trim within
  < 1 drive cycle of `codes_cleared = true`.

**Consumer note.** This chunk feeds the validity gate, not the routing table: a
pegged, frozen, or freshly-reset trim is demoted so it cannot drive a false
P0171/P0172 route. The active interpretation logic lives in
`03_normal-ranges-and-dtc-thresholds` and `04_trim-pattern-decision-tree`; this
chunk says *when not to trust them*.

Citation: SAE J1979 (signed-8-bit ±127 % register); open-loop freeze per
master_cold_start_guide.md §1.


## Core Entities

- TOTAL_TRIM, register sentinel +/-127 +/-99, TrimAnalyticsGate.OPEN_LOOP
- codes_cleared, fuel_sys_status OL
- COMLab trim-validity gating (consumer, active)

## Graph relations (explicit)

**pegged-trim** DEMOTED_BY **COMLab trim-validity gate**
**fuel_sys_status OPEN_LOOP** FREEZES **TOTAL_TRIM**
**codes_cleared** RESETS **LTFT**
**frozen-trim** INVALIDATES **P0171** and **P0172** routing

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
