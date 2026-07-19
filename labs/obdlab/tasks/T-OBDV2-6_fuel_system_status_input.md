# T-OBDV2-6 — Fuel-system-status manual input (Closed/Open-Loop dropdown)

**Status:** `pending` — **coder-runnable** · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** proposal **EP-OBD-IN-03** (owner must-have, 2026-06-08) · **Registry:** DEP-9 · **Audit:** `research/proposals/PROPOSAL_AUDIT_v2_boost.md` (RQ-D, RQ-F)
**Blocked by:** —
**Consumer (signal/noise):** **live in OBDLab today** — `analytics_preconditions` (sets `TrimAnalyticsGate.OPEN_LOOP`) and `semantic_consistency_checker` (closed-loop gate) already read `fuel_sys_status`. COMLab Stage-A reader **`T-COMV2-FUELSYS-GATE-1`** (Stage 4) forward-registered for the raw-field exposure.

> **Why now (owner ruling RQ-D).** OBDLab must carry its **own** fuel-system-status input even
> though DTCLab parses it from freeze-frame — because a **DTC is not always set and DTCLab may not
> be in use at all**, so OBDLab cannot depend on it for loop state. The owner requires a
> **manual-entry dropdown (Closed-Loop / Open-Loop), mirroring DTCLab.**

## What it adds

1. A **local mirror** of DTCLab's `FuelSystemStatus` enum (**no cross-lab import** — per the
   boundary rule, OBDLab owns its copy): `CL` / `OL` / `OL_DRIVE` / `OL_FAULT`
   (closed-loop / open-loop base map / open-loop driving / open-loop fault).
2. A typed `fuel_system_status: FuelSystemStatus` **manual input** (the dropdown surface) +
   the same field **emitted on `OBDLivePayload`** for COMLab.
3. **Migration of the two existing internal consumers** from ad-hoc strings to the enum:
   - `analytics_preconditions.py:72` — `fuel_status != "Closed_Loop"` → `!= FuelSystemStatus.CL`.
   - `semantic_consistency_checker.py:124,241` — `== "Open_Loop_Cold"` / `!= "Closed_Loop"` →
     `in {OL, OL_FAULT}` / `!= CL`.

   **String→enum mapping (owner-confirm):** `"Closed_Loop"→CL`, `"Open_Loop_Cold"→OL`. The
   warm-but-still-open-loop semantic gate becomes "warm AND status ∈ {`OL`,`OL_FAULT`}".

## Why this is in scope as a single change

The enum migration is **required for parity** (the owner asked for DTCLab-equivalence) and to
avoid two competing loop-state representations inside OBDLab. The field and the migration ship
together; the dropdown without the migration would leave the live gates reading stale strings.

## Success criteria

- Local `FuelSystemStatus` enum (CL/OL/OL_DRIVE/OL_FAULT) in `obdlab/obdlab/schemas/vocabulary.py`,
  values mirroring DTCLab (cite `DTC_VOCABULARY.md §8` + the no-import boundary note).
- `fuel_system_status: FuelSystemStatus` accepted as a manual input (validated) **and** emitted on
  `OBDLivePayload`.
- The two internal consumers migrated to the enum; **behaviour preserved** (existing tests for the
  OPEN_LOOP gate + closed-loop semantic gate stay green after fixture values map to the enum).
- **Emitter discipline:** OBDLab emits the status field, **no** fuel-system *verdict*.
- **Forward-registered** `T-COMV2-FUELSYS-GATE-1` (Stage 4) — COMLab Stage-A gate reading the raw
  `fuel_system_status` + the CL→OL_FAULT-across-RPM Δ-signature.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/vocabulary.py` — local `FuelSystemStatus` enum.
2. `obdlab/obdlab/schemas/payload.py` — add `fuel_system_status: FuelSystemStatus`.
3. Input validation surface (`pid_ingestion_validator` / `raw_user_inputs` handling) — accept the
   typed dropdown value.
4. `obdlab/obdlab/core/analytics_preconditions.py` + `semantic_consistency_checker.py` — migrate
   string checks to the enum (string→enum mapping above).
5. Tests: enum round-trip; OPEN_LOOP gate + closed-loop semantic gate still fire on the enum
   values; payload carries the field.
6. `comlab/comlab/config/proposals/proposals.yaml` — `EP-OBD-IN-03` entry (consumer + cite).
7. **Confirm** the pre-registered `T-COMV2-FUELSYS-GATE-1` row in `comlab/tasks/PROGRESS.md`.

## Files to touch

- `obdlab/obdlab/schemas/vocabulary.py`, `schemas/payload.py`
- `obdlab/obdlab/core/{analytics_preconditions,semantic_consistency_checker,pid_ingestion_validator}.py`
- `obdlab/tests/unit/…`
- `comlab/comlab/config/proposals/proposals.yaml`, `comlab/tasks/PROGRESS.md` (rows only)

## Out of scope

No fuel-system *verdict* (COMLab). **No cross-lab import** of DTCLab's enum — mirror it. No DTCLab
changes. No new gate logic beyond the string→enum migration. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# no cross-lab import
grep -rn "from dtclab\|import dtclab" obdlab/obdlab && { echo "FAIL: cross-lab import"; exit 1; } || echo "OK isolated"
# enum is consumed in a live path (not an orphan)
grep -n "FuelSystemStatus" obdlab/obdlab/core/analytics_preconditions.py obdlab/obdlab/core/semantic_consistency_checker.py
# emitter discipline — status only, no verdict
grep -rn "fuel_system_verdict\|FaultFamily" obdlab/obdlab/core/ && { echo "FAIL: verdict"; exit 1; } || echo "OK status-only"
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-6.md` → `## Plan` (enum mirror, dropdown field, migration mapping,
forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. Row → `done` with
"fuel_system_status dropdown added (FuelSystemStatus mirror, no import); 2 internal consumers
migrated string→enum; T-COMV2-FUELSYS-GATE-1 forward-registered; Stage-2 green."

## Anti-orphan note

The enum has a **live OBD consumer immediately** (the two migrated gates), so it is not an orphan
at Stage 2. The payload-field's COMLab Stage-A reader lands at Stage 4 (`T-COMV2-FUELSYS-GATE-1`).
