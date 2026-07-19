---
node_type: wiki
lab: dtclab
module: dtclab
subsystem: dtc-lifecycle
implements:
  - "labs/dtclab/dtclab/schemas/vocabulary.py"
  - "labs/dtclab/dtclab/core/data_fusion_sanitizer.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DTCLabPayload (mil_flashing, confirmed_dtcs, codes_cleared)"
  - "dtclab: labs/dtclab/dtclab/core/freeze_frame_extractor.py (codes_cleared -> ff_codes_cleared_invalidated)"
drift_guards:
  - "labs/dtclab/tests/unit/test_vocabulary.py"
  - "labs/dtclab/tests/unit/test_freeze_frame_extractor.py"
tags: [dtclab, wiki, dtc-lifecycle]
source: "labs/dtclab/wiki/01_dtc_state_lifecycle.md"
---
# 01 — DTC state lifecycle & monitor readiness

Anchors: `DTC_VOCABULARY.md §6` (`DTCState`), `§7` (`Mode06MonitorState`),
`§16` (confidence weights per DTC state). See `00_INDEX.md` for scope.

---

## 1.1 DTC state lifecycle (`DTC_VOCABULARY.md §6`)

```
Monitor FAILS (once)
        │
        ▼
  PENDING  ← Mode $07 — stored in pending_dtcs
  (1 drive cycle)
        │
        │ Monitor fails again (subsequent drive cycle)
        ▼
  CONFIRMED ← Mode $03 — stored in confirmed_dtcs
  MIL illuminates
        │
        │ Monitor PASSES (healing condition)
        ▼
  CONFIRMED + PASSING (MIL off after clean drive cycles)
        │
        │ Scanner clears codes (or battery disconnect)
        ▼
  CLEARED — KAM (LTFT reset to 0%)
        │
        ╠═══════════════════════════╗
        │ Emissions-critical DTC    │ Non-emissions DTC
        ▼                           ▼
  PERMANENT ←              Code removed cleanly
  Mode $0A — survives clears
  until monitor re-runs
```

**Key behavioural rules:**

- Permanent DTCs (`$0A`) persist across battery disconnects and scanner clears
  until the relevant monitor completes and passes.
- Clearing codes resets LTFT to 0%. A STFT pegged at +25% with LTFT at 0% is the
  signature of recently cleared codes — the PCM has not yet re-learned the
  chronic lean condition.
- If `codes_cleared == true` in session context, flag
  `ff_codes_cleared_invalidated` and weight all freeze-frame fuel-trim evidence
  lower.

---

## 1.2 Authoritative state-machine pin (v2)

v1 described the lifecycle qualitatively. Denton §5.4.4 / §5.4.6 pins the exact
cycle counts, which the COMLab fault-atlas uses to weight a DTC's confidence by
how far it has progressed through the lifecycle. These numbers refine — they do
**not** add a new field — the existing consumer `DTC_VOCABULARY.md §16`
(confidence weights per `DTCState`). Source:
`obdlab/research/AdvAutomotiveFaultDiagnosis_ANALYSIS.md` §A1 / §D, citing
Denton §5.4.4.

| Transition | Cycle count | Resulting state |
|---|---|---|
| Failure detected | immediately, MIL **not** lit | `PENDING` (Mode `$07`) |
| Failure recurs | on the **3rd consecutive driving cycle** | `CONFIRMED` (Mode `$03`), MIL lit |
| Monitor passes | **3 subsequent clean driving cycles** | MIL heals (code retained, not erased) |
| No recurrence | **≥ 40 warm-up cycles** | code / distance / freeze-frame **erased** |

A **warm-up cycle** is defined as coolant rising **≥ +22°C from start AND
reaching ≥ 70°C** (Denton; reconciled against 4DLab's ≥ 75°C operating-read
floor, which sits safely above the 70°C warm-up minimum). This is distinct from
a **driving cycle** (the engine-run-to-shutoff unit used for the 3-cycle confirm
and 3-cycle heal counts).

**Cross-book reconciliation:** the cardiagnosis corpus said "~40 restarts";
Denton's three-number model (3 confirm / 3 heal / ≥ 40 warm-up erase) supersedes
that vague figure. Use Denton's three numbers.

**Routing implication:** a `PERMANENT` (`$0A`) code that survived a clear but has
not yet re-run its monitor is higher-confidence than a `CONFIRMED` code stored
many warm-up cycles ago in an unknown operating context. The age-in-warm-up-
cycles of a code is therefore a legitimate down-weight signal for stale evidence.

---

## 1.3 Monitor readiness / status trust gate **[PROPOSAL]**

> **Signal/noise:** v2-new. Consumer named below; full disposition in
> `11_proposals_register.md`. Source: Denton §5.4.6 via ANALYSIS §A2.

Each OBD monitor carries a **Ready / Not-Ready** status flag. A "no fault" report
from a monitor whose readiness is **Not-Ready** is *untested*, not *passed* — and
must not be trusted as evidence of health.

- **Continuous monitors** (always ready once running): misfire and fuel-system.
- **Non-continuous monitors** (catalyst, EVAP, EGR, O₂, O₂-heater) run only
  under their preconditions and read Not-Ready until they have.
- Readiness flags reset to **Not-Ready** on **battery disconnect or scan-tool
  clear** — this is the mechanism that produces an "all clear" scan that is in
  fact entirely untested.
- Era allowance for a still-valid inspection: **MY 1996–2000 may have ≤ 2
  monitors Not-Ready; MY 2001+ ≤ 1 Not-Ready.** (Source: Denton §5.4.6.)

**Proposed contract:** a `monitor_status` map (per-monitor `READY` /
`NOT_READY`) and a derived `readiness_reset_suspected` bool when a cleared-codes
context coincides with multiple Not-Ready monitors.

**Named consumer + code path:** COMLab confidence-weighting — the fault-atlas
router demotes any monitor-derived evidence whose `monitor_status == NOT_READY`,
and raises a `readiness_reset_suspected` caveat on the session. Pairs with the
OBDLab `analytics_preconditions` family (`T-OBDV2-6`). Absorbs the cardiagnosis
EVAP-readiness candidate (B3): EVAP Not-Ready is one such precondition
(temperature + fuel-fill constrained).

---

## 1.4 One-trip vs two-trip maturation & corpus skew

Monitors mature a fault on either **one trip (Type A)** or **two trips (Type B)**,
and that asymmetry biases which faults end up with a stored code. Source:
`DTCanswers.md` / `DTCansw2.md` (web-research synthesis, 2026-06-11), reconciled
with the §1.2 cycle pins.

- **One-trip (Type A)** — critical systems that threaten the catalyst or engine
  durability. A single failed cycle illuminates the MIL, stores a confirmed DTC,
  and captures a freeze frame: catalyst-damaging misfire (the **Type A** misfire,
  chunk `06.4`), critical fuel-pressure/fuel-system deviations, and hard sensor-
  circuit faults under the CCM (open/short).
- **Two-trip (Type B)** — emissions monitors that don't cause immediate damage.
  First failed trip stores a **pending** `$07` code (MIL off, no freeze frame); a
  second *consecutive* failure under similar load/temp matures it to confirmed
  `$03` + MIL + freeze frame. No recurrence on trip two erases the pending code.

| Monitor | Class | Maturation | Enable criteria |
|---|---|---|---|
| Severe (catalyst-damaging) misfire | A | one-trip | Continuous; crank-speed fluctuation over ~200/1000 revs |
| Emissions misfire | B | two-trip | Continuous; misfire rate > ~2% over 1000 revs |
| Fuel-system | variable | one- or two-trip | Continuous once closed-loop (ECT ≥ 75 °C); depends on trim deviation severity |
| Catalyst | B | two-trip | Non-continuous; stable closed loop, 30–60 mph, stabilised cat temp |
| EVAP (leak check) | B | two-trip | Non-continuous; cold start, > 8 h soak, fuel level 15–85% |
| EGR | B | two-trip | Non-continuous; DFCO or steady-state cruise |
| CCM (circuit checks) | A/B | variable | Continuous electrical at key-on; rationality may need speed/temp |

**Corpus-skew implication.** Continuous one-trip faults (misfire, fuel-system,
circuit opens) mature fast with minimal drive-cycle demands, so they are
**over-represented** in a manually-collected corpus. Non-continuous two-trip
faults (catalyst, EVAP, EGR) need restrictive enables (narrow temp, precise fuel
level, highway steady-state) — on short urban trips they often never mature and
stay pending/no-code, so they are **under-represented by an estimated ~1.5–2.0×**
(catalyst/EVAP ≈ 50% under-counted in code-only data vs true physical occurrence).

**Consumer.** The COMLab family prior must **not** be read straight off corpus
DTC counts: it up-weights catalyst/EVAP/EGR priors to offset the maturation
under-count, and discounts the apparent dominance of misfire/fuel-system codes.
This is the corpus-realism correction behind the §12.1 prevalence figures and the
Mode `$06`-as-pre-DTC rule (chunk `04`).

## Graph relations (explicit)

**DTCState** ENUMERATES **PENDING**, **CONFIRMED**, **PERMANENT**
**confirmed** status MAPS_TO **DTCState.CONFIRMED**
**pending** status MAPS_TO **DTCState.PENDING**
**permanent** status MAPS_TO **DTCState.PERMANENT**
**DTCState** CONSUMED_BY **dtclab/schemas/vocabulary.py**
**codes_cleared** context flag TRIGGERES **ff_codes_cleared_invalidated**
**ff_codes_cleared_invalidated** CONSUMED_BY **dtclab/core/data_fusion_sanitizer.py**
**driving_cycle** DETERMINES transitions of **DTCState**
**warmup_cycle** GATED_BY **coolant_temp_c >= 70°C** AND **coolant_temp_c rise >= 22°C**
**one-trip maturation** DESCRIBES **Type A monitors**
**two-trip maturation** DESCRIBES **Type B monitors**
**monitor_status** (proposed) MAPS_TO **per-monitor READY / NOT_READY**
**readiness_reset_suspected** (proposed) CARRIED_AS **context only**

## Core Entities

- **DTCState** — Enum representing the confirmation state of a stored trouble code. Consumer: `dtclab/schemas/vocabulary.py`.
- **codes_cleared** — Context boolean indicating if diagnostic memory has been recently cleared. Consumer: `dtclab/core/data_fusion_sanitizer.py`.
- **ff_codes_cleared_invalidated** — Derived flag that weights freeze-frame evidence lower when codes were recently cleared. Consumer: `dtclab/core/data_fusion_sanitizer.py`.
- **monitor_status** — Proposed map of per-monitor readiness flags. Status: PROPOSAL. Consumer: COMLab confidence-weighting.
- **readiness_reset_suspected** — Proposed flag raised when multiple monitors are Not-Ready in cleared-codes context. Status: PROPOSAL. Consumer: COMLab confidence-weighting.

