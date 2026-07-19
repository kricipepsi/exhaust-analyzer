# T-OBDV2-5 — Mode $06 no-start discrimination branch (PROPOSAL, cross-lab, CAN-era)

**Status:** `pending (registration)` — **coder-runnable home is DTCLab + COMLab, not OBDLab** · **Lab:** OBDLab tasks dir (audit-Q8 owner) · **Stage:** producer S3 (DTCLab) → reader S4 (COMLab) · **Mode:** STRICT
**Origin:** OBDLab audit **Q8** (Mode $06 MID/TID discriminators) · **Registry:** DEP-8 · **Proposal:** `EP-DTC-NOSTART-1`
**Blocked by:** — (audit **Q8** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** COMLab **`T-COMV2-NOSTART-1`** (Stage 4) — fault_atlas no-start branch keyed on the monitor-aborted + freeze-frame-cut state; producer **`T-DTCV2-NOSTART-1`** (Stage 3, DTCLab). The **COMLab reader is already pre-registered** in `comlab/tasks/PROGRESS.md` (DEP-8, this pack); the **DTCLab producer row** still needs registering in the DTCLab ledger.

> **Task shape — read first.** This is a **cross-lab PROPOSAL registration**, authored here only because the
> audit question (Q8) lives in the OBDLab set. **OBDLab writes no code for it.** The runnable coder tasks are
> **DTCLab** (producer — extend the existing Mode-06 evaluator with the "Incomplete/aborted" monitor state) and
> **COMLab** (reader — fault_atlas no-start branch). OBDLab's only structural role is the **already-present**
> `OBDLivePayload.freeze_frame_pids` ferry (no change). The deliverable here is the proposal entry + the two
> forward-registered rows + DEP-8.

## Why this exists

A DTC says *where*; **Mode $06** (on-board monitor test values) + **Mode $02** (freeze frame) say *why* — the
only way to split a **crank-no-start** from a **no-crank-no-start** when no running PIDs exist. The decisive,
non-OEM-specific signal is the **"Incomplete/aborted" monitor state itself**: a Misfire Monitor that reads all-
zero/Incomplete because *no ignition was authorised* (immobilizer lock-out) versus one that *could not run*
(CKP/CMP loss) versus a mechanical failure. A pure DTC list cannot make that split.

## Research gate — CLOSED (Q8)

`AUDIT_ANSWERS_OBDLab.md` Q8 + `pids-protocol/01_mode06-freezeframe-nostart-method.md`:

- **Discriminators (portable on CAN only):**
  - Misfire Monitor **MID $A1 / TID $53** — "Incomplete"/all-zero CIDs = monitor aborted → **security lock-out vs mechanical no-start**.
  - Fuel System Monitor **MID $81 / TID $01/$02** — value vs ±20/±25 % limit → lean/rich (e.g. +28/+32 % over a +20/+25 % limit = Failed lean).
  - EGR Monitor **TID $41** — e.g. 65,227 vs max 896 = stuck.
  - MAF rationality — "fails to reach peak (`< 40 × Disp.` g/s at WOT)".
- **The "Incomplete/aborted" state is itself diagnostic** (security lock-out vs mechanical no-start).
- **CAN-era gate:** Mode $06 is only standardized/portable on **CAN (≈ 2008+)**; pre-CAN MID/TID are per-OEM →
  **exclude or flag** (Q6/Q8). New Mode-06 fields earn their place only via the named consumer below.
- Sources: `pids-protocol/01_mode06-freezeframe-nostart-method.md`, `o2-logic/07_o2-dtc-families.md`.

## Scope (now PINNED — owner may ratify the field names/gate)

A two-lab proposal; both halves ship together (signal/noise):

> **Producer (DTCLab, S3):** extend the existing Mode-06 evaluator (`dtclab/dtclab/core/mode06_evaluator.py`,
> `schemas/mode06_result.py`) to surface a distinct **monitor-aborted / Incomplete** state for MID $A1/TID $53
> (today the tri-state classifies pass/fail/marginal margins; it does **not** flag "aborted"). Pair it with the
> freeze-frame fuel/spark-cut-at-key-on flag. **CAN-era-gated** (emit the no-start signal only when the protocol
> is CAN; pre-CAN → flag as per-OEM/unreliable, do not assert).
>
> **Reader (COMLab, S4):** a fault_atlas **no-start branch** keyed on (monitor-aborted + FF cut) → routes to a
> **security-lockout** node vs a **mechanical-no-start** node (`comlab/comlab/core/fault_atlas_router.py`).

OBDLab: **no change** (the `freeze_frame_pids` ferry already exists).

## Success criteria (registration only this session)

- Proposal entry `EP-DTC-NOSTART-1` added to `comlab/comlab/config/proposals/proposals.yaml`, naming **both**
  the DTCLab producer code path and the COMLab reader code path + the CAN-era gate + ISO/SAE cite.
- Producer row `T-DTCV2-NOSTART-1` forward-registered in the **DTCLab** ledger; reader row `T-COMV2-NOSTART-1`
  in the **COMLab** ledger.
- DEP-8 row added to `v2-restructure/CROSS_LAB_DEPENDENCIES.md` (producer S3 → reader S4, CAN-era).
- Q8 marked dispositioned-to-cross-lab in `obdlab/tasks/PROGRESS.md` (no OBDLab code).
- **No OBDLab source change**; no inner loop required for OBDLab (registration is doc/ledger only).

## Deliverables

1. `comlab/comlab/config/proposals/proposals.yaml` — `EP-DTC-NOSTART-1` proposal entry (both consumers, CAN-era gate).
2. `comlab/tasks/PROGRESS.md` — **confirm** the pre-registered `T-COMV2-NOSTART-1` row (Stage 4 reader; already registered this pack).
3. `dtclab` ledger — forward-register `T-DTCV2-NOSTART-1` (Stage 3 producer, extends `mode06_evaluator`).
4. `v2-restructure/CROSS_LAB_DEPENDENCIES.md` — DEP-8 row.
5. `obdlab/tasks/PROGRESS.md` — ledger row recording Q8 dispositioned cross-lab.

## Files to touch

- `comlab/comlab/config/proposals/proposals.yaml`
- `comlab/tasks/PROGRESS.md` and the `dtclab` ledger — forward-registration rows only
- `v2-restructure/CROSS_LAB_DEPENDENCIES.md` — DEP-8 row
- `obdlab/tasks/PROGRESS.md`
- **No `obdlab/obdlab/**` source change.**

## Out of scope

No OBDLab code. No pre-CAN MID/TID per-OEM tables (excluded/flagged). The producer/reader **implementation** is
the separate DTCLab (`T-DTCV2-NOSTART-1`) and COMLab (`T-COMV2-NOSTART-1`) coder tasks — not this session. No
new OBD payload field (the `freeze_frame_pids` ferry already carries Mode-06 data). Off-scope finds → follow-ups.

## Verification

```bash
cd <repo>/labs
# DTCLab Mode-06 substrate exists (producer extends it, not greenfield)
grep -n "evaluate_monitor\|Mode06MonitorResult\|MID_KEY_PATTERN" dtclab/dtclab/core/mode06_evaluator.py
# proposal registered with BOTH named consumers + CAN-era gate
grep -n "EP-DTC-NOSTART-1\|T-DTCV2-NOSTART-1\|T-COMV2-NOSTART-1\|CAN" comlab/comlab/config/proposals/proposals.yaml
# OBDLab untouched
git -C obdlab status --short obdlab/ | grep . && echo "NOTE: OBD source changed — Q8 should not touch it" || echo "OK OBD untouched"
```

All steps pass; the proposal and both forward-registered rows exist; OBDLab source is untouched.

## Anti-orphan note

The no-start signal is produced (DTCLab S3) and read (COMLab S4) in the **same proposal** — it is not an
orphan. CAN-era gating bounds applicability; pre-CAN is flagged per-OEM, not asserted. Anti-orphan grep-confirm
closes at the COMLab `T-COMV2-NOSTART-1` reader task.

## Progress hook

`tasks/progress_notes/T-OBDV2-5.md` opens with the confirmed `## Plan` (name both code paths, the CAN-era gate,
the proposal id), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with "Q8 dispositioned
cross-lab: EP-DTC-NOSTART-1 registered; T-DTCV2-NOSTART-1 (producer) + T-COMV2-NOSTART-1 (reader) forward-
registered; CAN-era gated; no OBDLab code."
