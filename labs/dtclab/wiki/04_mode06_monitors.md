---
node_type: wiki
lab: dtclab
module: dtclab
subsystem: mode-06-monitoring
implements:
  - "labs/dtclab/dtclab/schemas/mode06_result.py"
  - "labs/dtclab/dtclab/core/mode06_evaluator.py"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py mode_06_monitors no-start branch"
drift_guards:
  - "labs/dtclab/tests/unit/test_mode06_evaluator.py"
tags: [dtclab, wiki, mode-06-monitoring]
source: "labs/dtclab/wiki/04_mode06_monitors.md"
---
# 04 — Mode `$06` as pre-DTC early warning

Anchors: `DTC_VOCABULARY.md §7` (`Mode06MonitorState`), `§13`
(`Mode06MonitorResult`), `§13.2` (universal MID inventory). See `00_INDEX.md`.

---

## 4.1 Why Mode `$06` matters before a DTC sets

Mode `$06` is valuable precisely when **no DTC has set**. A
`PENDING_FAIL_MARGINAL` result reveals a system drifting toward failure before
the MIL illuminates.

The COMLab fault router includes marginal Mode `$06` results as evidence
**regardless of DTC presence**. A catalyst showing 8% OSC margin with no P0420
set is a higher-confidence catalyst candidate than a P0420 stored 6 months ago in
a different operating context.

**Monitor fault threshold (v2 pin).** Denton §5.3 pins the generic OBD monitor
fault trigger at **1.5 × the applicable emission limit** for catalyst, misfire,
and O₂ monitors. A Mode `$06` test value crossing toward that 1.5× boundary is
the early-warning signal; a value at the min/max limit means the monitor has
already failed. Source: ANALYSIS §D. (This is a reference threshold for reading
marginal `$06` results — not a DTCLab-computed value.)

**Snapshot caveat.** Mode `$06` data is the snapshot from the **last completed
monitor cycle** — not a live reading. A test result stored at 800 RPM cannot be
compared against data at 4000 RPM stress idle. Two snapshots are comparable only
when taken under identical monitor-enable conditions (same RPM band, load range,
ECT gate). This is why OBDLab's RPM-state buckets (`STABILIZED_IDLE`,
`STRESS_IDLE`) do **not** parameterize Mode `$06` readings — COMLab consumes them
as point-in-time evidence, not as part of multi-state comparison.

---

## 4.2 MID/TID early-warning reference

The following monitor IDs recur across the case corpus as the highest-value
pre-DTC indicators. Values are read against each monitor's own min/max limit
(supplied in the `$06` payload); a value near the limit is the warning.

| MID | Monitor | Early-warning use |
|---|---|---|
| `$01`–`$0B` (per-cyl) / `$A1`–`$A9` | Misfire (per-cylinder counts) | Cylinder-specific count rising while others near zero isolates the fault before P030x crosses threshold |
| `$13` | Fuel-system monitor (trim limit) | Value pushing toward max allowed limit ⇒ chronic lean drift before P0171 |
| `$21` (Bank 1) / `$22` (Bank 2) | Catalyst OSC (TID `$81`) | Value near minimum limit ⇒ degrading catalyst before P0420/P0430 |
| `$31` | VVT / cam-phaser plausibility | Phase-correlation value near limit ⇒ timing drift before P0011/P0016 |
| `$3B` | EGR / EVAP flow & position | Value at minimum ⇒ valve not moving or passages clogged |
| `$05` | O₂-sensor heater (current) | Heater current below min ⇒ heater fault before P0135 |
| `$71` | Boost-pressure control | Target-vs-actual deviation over limit ⇒ under/overboost before P0299/P0234 |
| `$00` | Comprehensive Component Monitor | Catch-all driver/range fault flag |

MID/TID assignments are manufacturer-specific before CAN (pre-2008) and
standardized for CAN-equipped vehicles 2008+ (`DTC_VOCABULARY.md §13.2`).
Sources: `cases/FF+$06DS.md`, `DtcDoc.md` non-start era cases.

## Graph relations (explicit)

**Mode06MonitorState** ENUMERATES **PASSED**, **PENDING_FAIL_MARGINAL**, **CRITICAL_FAIL**
**PASSED** status MAPS_TO **Mode06MonitorState.PASSED**
**PENDING_FAIL_MARGINAL** status MAPS_TO **Mode06MonitorState.PENDING_FAIL_MARGINAL**
**CRITICAL_FAIL** status MAPS_TO **Mode06MonitorState.CRITICAL_FAIL**
**Mode06MonitorState** CONSUMED_BY **dtclab/schemas/vocabulary.py**
**Mode06MonitorResult** CONSUMED_BY **dtclab/schemas/mode06_result.py**
**MID $01-$0B** / **MID $A1-$A9** IDENTIFIES **misfire per-cylinder counts**
**MID $13** IDENTIFIES **fuel-system monitor trim limit**
**MID $21** / **MID $22** IDENTIFIES **catalyst OSC**
**MID $31** IDENTIFIES **VVT / cam-phaser plausibility**
**MID $3B** IDENTIFIES **EGR / EVAP flow & position**
**MID $05** IDENTIFIES **O₂-sensor heater current**
**MID $71** IDENTIFIES **boost-pressure control**
**MID $00** IDENTIFIES **Comprehensive Component Monitor**
**Mode06MonitorResult** EVALUATED_BY **dtclab/core/mode06_evaluator.py**

## Core Entities

- **Mode06MonitorState** — Enum representing the evaluated severity of a Mode $06 test margin. Consumer: `dtclab/schemas/vocabulary.py`.
- **Mode06MonitorResult** — Struct representing an individual evaluated monitor result (MID/TID, value, limits, state). Consumer: `dtclab/schemas/mode06_result.py`.

