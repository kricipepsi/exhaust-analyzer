# T-OBDV2-ECU-PERCEPT-1 — OBD perception-delta channel for `ecu_fault`

**Status:** `pending (next)` — **coder-runnable** (research gate CLOSED) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** cross-lab fusion split of `ecu_fault` (GASLab `T-GV2-6d`, 2026-06-05) · **Registry:** DEP-2
**Blocked by:** — (T-OBDV2-0 = revive **done**; audit **Q1 + Q4** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** COMLab fusion verdict **`T-COMV2-ECU-FUSE-1`** (Stage 4) — the only reader of this channel; forward-registered by this task.

## Why this exists (the split — unchanged)

`ecu_fault` = "the ECU is wrong about the mixture." No single lab can emit it: GASLab sees *reality* (5-gas
Brettschneider λ), OBD sees *perception* (what the ECU commands vs what its own sensor reports). The verdict is
the **divergence**, which lives in COMLab fusion. GASLab emits the reality half (`T-GV2-6d` done); **OBD emits
the perception half here**; COMLab fuses last. OBD emits **no** `ecu_fault` label.

## Research gate — CLOSED

`AUDIT_ANSWERS_OBDLab.md` answers the two gating questions:

- **Q1** — `ecu_fault` is **not** separable from OBD-II data alone; it is a gas↔OBD truth-vs-perception verdict. OBD's contribution is (a) a λ command-vs-sensor gap and (b) bank-symmetry context (internal/shared-plane faults hit B1≈B2 symmetrically; external faults are bank-specific).
- **Q4** — a *usable continuous* λ exists only on **wideband/linear** sensors; a **commanded** λ exists only where the vehicle reports **PID 0x44** (commanded equivalence ratio). Narrowband is a switch, not a meter → no meaningful delta. ⇒ the channel is computable on the Era-2+ (~2000–2010) wideband/0x44 fleet, **None** elsewhere (this is the kill-switch, resolved to a per-sample computability guard rather than a drop).

## Scope (now PINNED — owner may ratify the field semantics)

OBDLab emits one typed field on its output payload (frozen inter-lab contract; COMLab mirrors locally, no
cross-lab import):

> **`lambda_perception_delta: float | None`** = `normalized_obd_lambda` (sensor perception) **−**
> `commanded_lambda` (ECU intent, from PID **0x44**). Emitted as a value **only when** (a)
> `dna_view.upstream_o2_type == WIDEBAND_LINEAR` **and** (b) a commanded-λ input (PID 0x44) is present;
> otherwise **`None`** (Q4 computability guard). OBDLab computes the delta from inputs it can see; it does
> **not** compare against gas (that is the fusion step) and does **not** judge `ecu_fault`.

The bank-symmetry discriminator (Q1) is **not a new field** — it is the already-emitted
`total_trim_correction_delta` vs `total_trim_correction_delta_b2`, which the Stage-4 fusion consumer reads
(closing that field's current orphan status). This task does not add a symmetry field.

## Success criteria

- New `lambda_perception_delta: float | None` on `OBDLivePayload` (`obdlab/schemas/payload.py`), typed, defaulting/None per the Q4 guard.
- Ingestion of the commanded-λ raw input (PID 0x44 / `commanded_equivalence_ratio`) in the `translate()` input path; absent input ⇒ `lambda_perception_delta = None`.
- **Computability guard verified:** `None` on a narrowband fixture and on a wideband fixture lacking commanded-λ; a real float on a `WIDEBAND_LINEAR` + commanded-λ fixture.
- **Emitter discipline:** no `ecu_fault` (or any fault-family) label emitted; grep-guard in verification.
- Tests green at Stage 2 against the frozen contract (divergent-until-consumer is acceptable — the reader lands at Stage 4).
- **Forward-registered** consumer row `T-COMV2-ECU-FUSE-1` added to the COMLab ledger (Stage 4), naming this field + the B1/B2 symmetry read as its inputs.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean.

## Deliverables

1. `obdlab/schemas/payload.py` — add `lambda_perception_delta: float | None`.
2. `obdlab/core/sensor_signal_translator.py` (+ the o2/normalizer path) — ingest commanded-λ (PID 0x44); compute the delta under the Q4 guard; emit `None` when not computable.
3. Tests: `tests/` unit cases covering the three computability branches + the emitter-discipline (no verdict) assertion. Reuse `tests/pid_logset/` wideband/narrowband fixtures where possible.
4. Forward-register `T-COMV2-ECU-FUSE-1` in the COMLab ledger (Stage 4) — the fusion verdict that reads `lambda_perception_delta` + B1/B2 symmetry + GASLab `λ_chem`.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/core/sensor_signal_translator.py` (and the O2/commanded-λ ingestion helper)
- `obdlab/tests/unit/…` (new test module for the delta channel)
- `comlab` ledger — forward-registration row only (no COMLab code this task)

## Out of scope

No `ecu_fault` verdict (COMLab). No GASLab import / no gas comparison in OBDLab. **No TPS/IAT fields** — the
ground-trace/Mode-4 signature needs them, but they belong to the ECU-hardware checker (EP-COM-04 / ECU-FU-3),
added only if that consumer names them; do not add speculatively here. No bank-symmetry *field* (use the
existing `_b2` delta). No catalyst/Mode-06 work. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/
pyright obdlab/
# emitter discipline — no fault-family verdict emitted (must return nothing)
grep -rn "ecu_fault\|fault_family\|FaultFamily" obdlab/obdlab/core/sensor_signal_translator.py \
  && { echo "FAIL: OBDLab emits a verdict — it is an emitter"; exit 1; } || echo "OK channel-only"
# computability guard: None on narrowband, float on wideband+commanded-λ (spec test asserts this)
pytest -x -q
```

All steps pass; the field is `None` on the narrowband branch and a float on the wideband+0x44 branch.

## Progress hook

`tasks/progress_notes/T-OBDV2-ECU-PERCEPT-1.md` opens with the confirmed `## Plan` (name the field, the Q4
guard, the forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done`
with Files changed + "lambda_perception_delta emitted under WIDEBAND/0x44 guard; emitter-only (no verdict);
T-COMV2-ECU-FUSE-1 forward-registered; Stage-2 green (anti-orphan closes at Stage 4)."

> **Anti-orphan note:** this field is read by `T-COMV2-ECU-FUSE-1` at Stage-4 close. Per DEP-2 it ships at
> Stage 2 under the frozen contract; the Stage-4 close performs the grep-confirm. Kill-switch (Q4) is already
> resolved: computable on the wideband/0x44 fleet, `None` elsewhere — not dropped.
