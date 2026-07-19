# T-OBDV2-2 — VE-as-independent-evidence gated on `air_metering_strategy`

**Status:** `pending` — **coder-runnable** (research gate CLOSED) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab audit **Q5** (single-air-sensor VE circularity) · **Registry:** DEP-6
**Blocked by:** — (T-OBDV2-0 = revive **done**; audit **Q5** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** COMLab fusion verdict **`T-COMV2-VE-GATE-1`** (Stage 4) — the only reader of `ve_pct`/`ve_validity` as VE evidence. **Already pre-registered** in `comlab/tasks/PROGRESS.md` (DEP-6, this pack) — the coder **confirms** the row, does not re-create it.

> **Task shape — read first.** This is a **contract / forward-registration** task, not a new-field task.
> OBDLab **already emits every signal the gate needs** (`air_metering_strategy` on the DNA view;
> `maf_status`, `map_status`, `ve_pct`, `ve_validity` on the payload). There is **no OBDLab code change
> expected.** The deliverable is to (a) freeze the gate bound into the inter-lab contract, and (b)
> forward-register the Stage-4 COMLab consumer that applies it. The implementation lands at Stage 4 as
> `T-COMV2-VE-GATE-1`. If the coder finds an actual OBD-side gap, it ships as a **proposal**, not silently.

## Why this exists

VE is a cross-check between **two independent air measurements** (MAF and MAP). With only one air sensor the
missing quantity is **back-calculated from the present one**, so VE cannot independently confirm anything — it
is circular. The chunks give the concrete failure: on a **speed-density (MAP-only)** engine a vacuum leak
produces **ΔTrim ≈ 0** (the "Speed-Density paradox": MAP reads the true higher manifold pressure, the ECU adds
matching fuel), so VE/trim is blind to it; the leak instead shows as reduced IAC counts and elevated idle MAP
(**≈ 45 kPa** vs healthy **≈ 30 kPa**). Therefore a VE **fault verdict** is only valid evidence on a
dual-sensor engine; on single-sensor engines the consumer must route to rationality, not VE.

## Research gate — CLOSED (Q5)

`AUDIT_ANSWERS_OBDLab.md` Q5:

- **No independent VE cross-check exists with a single air sensor — it is circular.** VE evidence is valid
  **only** for `air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`.
- The substitute on single-sensor engines is the **MAF/MAP/TPS rationality cross-check (P0068)** + inferred-BARO,
  + IAC counts / idle-MAP (≈ 45 vs ≈ 30 kPa) — **not** VE.
- Sources: `delta-relations/06_architecture-modifiers.md` (Speed-Density paradox), `pids-protocol/02_maf-map-tps-rationality-p0068.md`.

## Scope (now PINNED — owner may ratify the bound)

The frozen inter-lab contract bound (consumed at Stage 4, applied by COMLab — **not** by OBDLab):

> A VE fault verdict (`ve_validity ∈ {FAULT_VE_IDLE_COLLAPSE, FAULT_MAF_CONTAMINATION, FAULT_VE_SENSOR_SKEW}`)
> counts as **independent sensor-diagnosis evidence only when `air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`**
> (equivalently `maf_status == REAL_SENSOR_FEED` **and** `map_status == REAL_SENSOR_FEED`). On
> `MAP_ONLY_SPEED_DENSITY` or `MAF_ONLY`, the VE channel is **circular** and the consumer **must not** raise a
> VE-based verdict from it — it routes to **P0068 MAF/MAP/TPS rationality + IAC/idle-MAP** instead.

OBDLab's role is unchanged: it emits the typed VE channel **plus the provenance** (`maf_status` /
`map_status`) that tells the consumer the channel is single-sourced. The **judgment** (independent vs circular)
is COMLab's, consistent with the emitter/fusion split.

## Success criteria

- **Forward-registered** consumer row `T-COMV2-VE-GATE-1` added to the COMLab ledger (Stage 4), naming
  `ve_pct` + `ve_validity` + `air_metering_strategy` (+ `maf_status`/`map_status`) as inputs, the
  `DUAL_MAF_MAP_CROSSCHECK`-only bound, and the single-sensor **P0068 rationality route** as the fallback.
- The bound above is written into the inter-lab contract surface the COMLab consumer mirrors (no cross-lab import).
- **Emitter discipline:** OBDLab emits **no** VE *verdict* — `compute_ve` returns only `(ve_pct, …, ve_validity)`;
  the verdict is COMLab's. Grep-guard in verification.
- **Confirm OBD already emits the gating signals** (grep): `air_metering_strategy` on `ObdLabDnaView`;
  `maf_status`, `map_status`, `ve_pct`, `ve_validity` on `OBDLivePayload`. No new OBD field.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean (expected: no OBD source change ⇒ suite unchanged-green).

## Deliverables

1. **Confirm** the pre-registered `T-COMV2-VE-GATE-1` row in `comlab/tasks/PROGRESS.md` (Stage 4) carries the
   `DUAL_MAF_MAP_CROSSCHECK` bound + P0068 single-sensor route + the named OBD inputs (already registered this pack).
2. Record the bound in the OBD↔COMLab contract doc the COMLab mirror reads (no code/import crossing).
3. Log the orphan + stale-docstring follow-up (see below) in `PROGRESS.md`.

## Files to touch

- `comlab/tasks/PROGRESS.md` — forward-registration row only (no COMLab code this task).
- the OBD↔COMLab boundary contract doc (bound text only).
- `obdlab/tasks/PROGRESS.md` — ledger row + follow-up.
- **No `obdlab/obdlab/**` source change expected.**

## Out of scope

No VE **verdict** in OBDLab (COMLab applies the bound at Stage 4). No new `VEValidity` value — the existing
provenance (`maf_status`/`map_status`) plus `air_metering_strategy` already carry single-sensor identity; a new
value would be a separate **proposal** only if the coder shows the provenance is insufficient. No P0068
detector code here (that is the Stage-4 consumer's body). No gas import. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
# OBD already emits the gating signals (must all be present)
grep -n "air_metering_strategy" obdlab/obdlab/schemas/dna_view.py
grep -n "maf_status\|map_status\|ve_pct\|ve_validity" obdlab/obdlab/schemas/payload.py
# emitter discipline — VE engine returns a channel, not a verdict (no fault-family label)
grep -rn "FaultFamily\|fault_family\|ve_verdict\|sensor_fault" obdlab/obdlab/core/ve_engine.py \
  && { echo "FAIL: OBDLab emits a VE verdict — it is an emitter"; exit 1; } || echo "OK channel-only"
ruff check obdlab/ tests/ && pyright obdlab/ && pytest -x -q
```

All steps pass; the consumer row `T-COMV2-VE-GATE-1` exists in the COMLab ledger with the DUAL-only bound.

## Anti-orphan note

`ve_pct` / `ve_validity` (and `maf_status` / `map_status`) are currently **carried in COMLab's
`OBDLiveDataPayload` ingestion schema but read by no live COMLab path** — the ingestion docstring
(`comlab/comlab/schemas/ingestion.py` lines ~312–316) names consumers that do **not** yet exist. This task
**names their Stage-4 reader** (`T-COMV2-VE-GATE-1`), closing the orphan at Stage 4 — the same emit-S2 /
consume-S4 pattern as `T-OBDV2-ECU-PERCEPT-1`. The stale ingestion docstring is logged as a follow-up (not
fixed here — COMLab-owned).

## Progress hook

`tasks/progress_notes/T-OBDV2-2.md` opens with the confirmed `## Plan` (name the bound, the forward-registered
consumer, "no OBD code change"), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with Files
changed + "VE-as-evidence gate frozen (DUAL_MAF_MAP_CROSSCHECK only; single-sensor → P0068); T-COMV2-VE-GATE-1
forward-registered; no OBD source change; orphan ve_pct/ve_validity closes at Stage 4."
