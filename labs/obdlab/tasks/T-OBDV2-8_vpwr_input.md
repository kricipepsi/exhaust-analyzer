# T-OBDV2-8 — Control-module-voltage (VPWR) input field

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** proposal **EP-OBD-IN-04** (promoted from `PROPOSAL_AUDIT_v2_boost.md`, 2026-06-08) · **Registry:** DEP-10
**Blocked by:** —
**Consumer (signal/noise):** COMLab electrical-health pre-check **`T-COMV2-VPWR-GATE-1`** (Stage 4) — `perception_contradiction` suppresses/down-weights sensor-fault routing when the rail is out of band; also feeds the alternator-AC-ripple node (`EP-FA-05`). Forward-registered by this task.

> **Why now.** A drifting ECU supply rail shifts every sensor reference *before* any air/fuel
> sensor is at fault — so a low/high/ripply rail must be ruled out first or the engine blames the
> wrong subsystem. No field carries it today. Wiki coverage authored alongside in
> `ecu-diagnosis/09_control-module-voltage.md`.

## What it adds

One typed manual-input field, also emitted on `OBDLivePayload`:

> **`control_module_voltage_v: float`** (PID `0x42` / VPWR, ~0–18 V). Supply voltage at the PCM
> pins. Numeric bounds + thresholds carry a wiki cite (`ecu-diagnosis/09` / `OBDLab_KG_Wiki.md §3.1`).

## Diagnostic value (named, not speculative)

- **Static:** `< 12.0 V` or `> 15.0 V` ⇒ flag a charging/ground fault **before** sensor-fault
  routing (false references; e.g. false P0606-class processor codes on some ECUs).
- **Δ-signature:** `ΔVPWR < −1.0 V` under revs ⇒ alternator/regulator diode; `ΔVPWR > +2.5 V`
  (system `> 15.5 V`) ⇒ over-charging, AC ripple corrupting references (consumer: `EP-FA-05`).

## Success criteria

- `control_module_voltage_v` added to the input validator (bounds + wiki cite) **and** emitted on
  `OBDLivePayload`.
- **Emitter discipline:** field only — no charging/electrical *verdict* (that is COMLab).
- **Forward-registered** `T-COMV2-VPWR-GATE-1` (Stage 4) naming `control_module_voltage_v` as the
  rail-health pre-check input + the `ΔVPWR` signatures.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/payload.py` — add `control_module_voltage_v: float`.
2. Input validation surface (`pid_ingestion_validator` + bounds config) — accept + bound (wiki cite).
3. Tests: field validates at bounds + emits; a low-rail fixture (`11.0 V`) carries through without
   OBD raising a verdict.
4. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-IN-04` entry (consumer + cite).
5. **Confirm** the pre-registered `T-COMV2-VPWR-GATE-1` row in `comlab/tasks/PROGRESS.md`.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/core/pid_ingestion_validator.py` (+ bounds config)
- `obdlab/tests/unit/…`
- `comlab/comlab/config/proposals/proposals.yaml`, `comlab/tasks/PROGRESS.md` (rows only)

## Out of scope

No electrical/charging **verdict** in OBDLab (COMLab `T-COMV2-VPWR-GATE-1` / `EP-FA-05`). No
AC-ripple waveform capture — VPWR is a scalar rail read; ripple is inferred downstream from ΔVPWR.
Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# emitter discipline — field only
grep -rn "charging_verdict\|electrical_verdict\|FaultFamily" obdlab/obdlab/core/ \
  && { echo "FAIL: OBD emits a verdict"; exit 1; } || echo "OK field-only"
# wiki coverage exists for the rebuilt KG
test -f research/chunks/ecu-diagnosis/09_control-module-voltage.md && echo "OK chunk present" || echo "MISS chunk"
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-8.md` → `## Plan` (field, thresholds, forward-registered consumer,
chunk coverage), then `VERIFICATION GATE` + `CODE REVIEW`. Row → `done` with "control_module_voltage_v
added; field-only (no verdict); T-COMV2-VPWR-GATE-1 forward-registered; chunk ecu-diagnosis/09 authored;
Stage-2 green."

## Anti-orphan note

VPWR's consumer (electrical pre-check + `EP-FA-05`) lands at Stage 4 (`T-COMV2-VPWR-GATE-1`) — the
emit-S2 / consume-S4 pattern. Wiki coverage (`ecu-diagnosis/09`) is authored now so the next KG
rebuild captures the field + consumer.
