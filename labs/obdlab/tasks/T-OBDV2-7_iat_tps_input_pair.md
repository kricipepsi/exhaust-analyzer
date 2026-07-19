# T-OBDV2-7 — IAT + TPS input pair (ECU-perception inputs)

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** proposals **EP-OBD-IN-08** (IAT) + **EP-OBD-IN-05** (TPS) · **Registry:** DEP-9 · **Audit:** `research/proposals/PROPOSAL_AUDIT_v2_boost.md`
**Blocked by:** —
**Consumer (signal/noise):**
- **IAT** — **live in OBDLab today**: `ve_engine.py` already reads `intake_air_temp_c` (density term); + COMLab ECU-hardware checker **`T-COMV2-ECU-HW-1`** (Stage 4, forward-registered).
- **TPS** — COMLab ECU-hardware checker **`T-COMV2-ECU-HW-1`** + idle-air-leak validator (P0505) in `fault_atlas_router` (Stage 4, forward-registered).

**Run order:** after `T-OBDV2-6` (same pack; FUELSYS is the must-have, this follows).

> **Why now.** The ECU-PERCEPT task (`T-OBDV2-ECU-PERCEPT-1`) explicitly **deferred TPS/IAT** to
> "the ECU checker that names them." That checker is now named (`T-COMV2-ECU-HW-1`), and IAT is
> already half-wired (the VE engine consumes it as an untyped raw input). This formalises both as
> typed input + payload fields with their named consumers.

## What it adds

Two typed manual-input fields, each also emitted on `OBDLivePayload`:

1. **`intake_air_temp_c: float`** (−40…140 °C). **Already consumed** by `ve_engine.py` (air-density
   term in the speed-density VE/airflow math) — this task gives it a typed input + validator entry +
   payload emit so COMLab's ECU checker can read it. Numeric bounds carry a wiki cite
   (`OBDLab_KG_Wiki.md §3.1`).
2. **`throttle_pos_pct: float`** (0…100 %). New field (today absent — flagged a payload gap by the
   ecu-diagnosis pass). Feeds the idle-air-leak validator and the ECU ground-trace tell.

## Diagnostic value (named, not speculative)

- **IAT** completes the VE/airflow density term **and** is half of the Mode-4 ECU ground-trace
  digital-lie signature: `IAT = −40 °C` + `ECT = −40 °C` + `TPS = 100 %` simultaneously — a pattern
  no single bad sensor produces (consumer: `T-COMV2-ECU-HW-1`).
- **TPS** drives the idle-air-leak validator (TP closed but RPM/load high ⇒ unmetered air, P0505)
  and supplies the `TPS = 100 % at idle` ground-trace tell.

## Success criteria

- `intake_air_temp_c` + `throttle_pos_pct` added to the input validator (bounds + wiki cites) **and**
  emitted on `OBDLivePayload`.
- **IAT live-consumer confirmed:** grep shows `ve_engine.py` reads `intake_air_temp_c` (already true);
  the typed field now feeds it cleanly.
- **Emitter discipline:** fields only, no idle-leak / ECU verdict (those are COMLab).
- **Forward-registered** `T-COMV2-ECU-HW-1` (Stage 4) naming `intake_air_temp_c` + `throttle_pos_pct`
  (+ `coolant_temp_c`) as the ground-trace digital-lie inputs, and the idle-air-leak validator
  reading TPS.
- Inner loop clean.

## Deliverables

1. `obdlab/obdlab/schemas/payload.py` — add `intake_air_temp_c`, `throttle_pos_pct`.
2. Input validation surface — accept + bound both (wiki cites).
3. Tests: both fields validate at bounds and emit; IAT flows into `ve_engine` VE math; a ground-trace
   fixture (IAT/ECT/TPS = −40/−40/100) carries through without OBD raising a verdict.
4. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-IN-08` + `EP-OBD-IN-05` entries.
5. **Confirm** the pre-registered `T-COMV2-ECU-HW-1` row in `comlab/tasks/PROGRESS.md`.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/core/pid_ingestion_validator.py` (+ bounds config)
- `obdlab/tests/unit/…`
- `comlab/comlab/config/proposals/proposals.yaml`, `comlab/tasks/PROGRESS.md` (rows only)

## Out of scope

No idle-air-leak or ECU-hardware **verdict** in OBDLab (COMLab `T-COMV2-ECU-HW-1`). No BARO / no
rationality module (deferred, RQ-B). No relative-throttle `throttle_rel_pct` unless the idle-leak
validator names it — add only on demand. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# IAT already has a live OBD consumer (not an orphan)
grep -n "intake_air_temp_c" obdlab/obdlab/core/ve_engine.py
# emitter discipline — fields only
grep -rn "idle_leak_verdict\|P0505\|ecu_hw_verdict\|FaultFamily" obdlab/obdlab/core/ \
  && { echo "FAIL: OBD emits a verdict"; exit 1; } || echo "OK fields-only"
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-7.md` → `## Plan` (two fields, IAT live VE consumer, forward-registered
ECU-HW checker), then `VERIFICATION GATE` + `CODE REVIEW`. Row → `done` with "intake_air_temp_c +
throttle_pos_pct added; IAT feeds live ve_engine; T-COMV2-ECU-HW-1 forward-registered; Stage-2 green."

## Anti-orphan note

IAT has a **live OBD consumer immediately** (`ve_engine`), so it is not an orphan at Stage 2. TPS's
consumer (idle-leak + ECU-HW checker) lands at Stage 4 (`T-COMV2-ECU-HW-1`) — same emit-S2 /
consume-S4 pattern as the rest of the pack.
