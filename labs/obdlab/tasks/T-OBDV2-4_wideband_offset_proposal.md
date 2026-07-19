# T-OBDV2-4 — `WIDEBAND_OFFSET_CANDIDATE` O₂ failure mode (PROPOSAL, two-stage)

**Status:** `pending` — **coder-runnable** (research gate CLOSED) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab audit **Q9** (separate lazy / biased / dead / **offset** O₂ faults) · **Registry:** DEP-7 · **Proposal:** `EP-OBD-17` (O2-FU-1)
**Blocked by:** — (T-OBDV2-0 = revive **done**; audit **Q9** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** COMLab fusion confirm **`T-COMV2-O2OFFSET-1`** (Stage 4) — reads `o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE`, confirms vs GASLab `λ_chem`, routes to a wideband-calibration `SENSOR_FAULT` node. **Already pre-registered** in `comlab/tasks/PROGRESS.md` (DEP-7, this pack) — coder confirms the row, does not re-create it. **Ships together with the new field (PROPOSAL) — signal/noise satisfied.**

> **Task shape — read first.** This is a **PROPOSAL** (v2 forward progress): a new `O2FailureMode` value
> **plus** its named consumer ship together. The new value is registered in the **proposals registry**
> (`comlab/comlab/config/proposals/proposals.yaml`, id `EP-OBD-17`), **never** silently in the live enum
> without its consumer. OBDLab emits only what it can see — the **candidate**; COMLab confirms.

## Why this exists

A wideband (UEGO) sensor with a **drifted reference-current circuit** keeps its loop internally consistent but
externally wrong: the ECU reads `λ = 1.00` while the engine runs lean. This **constant-offset** fault is
invisible to the shipped narrowband taxonomy (`STUCK_LEAN`/`STUCK_RICH`/`SLUGGISH`/`DEAD`/`WRONG_CENTERLINE`)
because the reported value looks plausible. It is the one O₂ separability gap Q9 leaves open. It is detectable
**only** by cross-checking the Ip-derived λ against ground-truth `λ_chem` — which is a fusion step — so the
expression is **two-stage**: OBD asserts a candidate, COMLab confirms.

## Research gate — CLOSED (Q9)

`AUDIT_ANSWERS_OBDLab.md` Q9 + chunks:

- Lazy/biased/dead are **already** the live `O2FailureMode` triggers (`SLUGGISH` / `STUCK_*` / `WRONG_CENTERLINE` / `DEAD`). The single gap is the **wideband constant offset**.
- Two-stage expression (`o2-logic/03_failure-modes-taxonomy.md` §reconciliation, `BIASED_OFFSET` → accepted v2 addition):
  - **OBDLab** emits `o2_failure_mode = WIDEBAND_OFFSET_CANDIDATE` — all it can assert: **persistent
    `|normalized_obd_lambda − 1.0| > 0.05` on a `WIDEBAND_LINEAR` sensor**.
  - **COMLab** confirms against GASLab `λ_chem ≈ 1.0` and routes to a wideband-calibration `SENSOR_FAULT` node
    (more specific than a generic `perception_contradiction`).
- Mechanism: `o2-logic/08_wideband-pumping-current-logic.md` (`Ip ∝ λ−1`; drifted reference current → loop
  internally consistent, externally wrong). `0.05` band per `o2-logic/03` / `o2-logic/08`.

## Scope (now PINNED — owner may ratify the field name/threshold)

OBDLab emits one new enum value (proposal):

> **`O2FailureMode.WIDEBAND_OFFSET_CANDIDATE`** — raised by `O2Normalizer._wideband_passthrough`
> (`obdlab/obdlab/core/o2_normalizer.py`) **only when** the sensor is `WIDEBAND_LINEAR` **and**
> `|normalized_obd_lambda − 1.0| > 0.05` **persistently** (not a transient sweep — WOT/DFCO excluded; warm
> closed-loop only). Otherwise unchanged (`NO_FAULT`). OBDLab does **not** compare to gas and does **not**
> assert a confirmed offset — that is the Stage-4 fusion step.

The numeric literal `0.05` carries a wiki-citation comment (`# wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08`)
per the obdlab/ numeric-literal rule.

## Success criteria

- New `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` value added (with wiki cite), raised by the wideband path under
  the persistent-`|λ−1.0|>0.05` guard; **registered as a proposal** in `comlab/comlab/config/proposals/proposals.yaml`
  (`id: EP-OBD-17`, `consumer: T-COMV2-O2OFFSET-1`, `status: proposed`).
- **Computability/guard verified:** `NO_FAULT` on a narrowband fixture and on an in-band wideband fixture
  (`|λ−1.0| ≤ 0.05`); `WIDEBAND_OFFSET_CANDIDATE` on a `WIDEBAND_LINEAR` fixture with persistent `λ ≈ 1.08`.
- **Emitter discipline:** OBDLab emits only the *candidate* — no confirmed `SENSOR_FAULT` verdict, no gas
  comparison. Grep-guard in verification.
- **Forward-registered** consumer row `T-COMV2-O2OFFSET-1` in the COMLab ledger (Stage 4): reads the candidate,
  confirms vs `λ_chem ≈ 1.0`, routes to the wideband-calibration `SENSOR_FAULT` node.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean.

## Deliverables

1. `obdlab/obdlab/schemas/vocabulary.py` — add `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` (+ wiki cite).
2. `obdlab/obdlab/core/o2_normalizer.py` — raise it in `_wideband_passthrough` under the persistent-offset guard.
3. Tests: unit cases for the three branches (narrowband `NO_FAULT`, in-band wideband `NO_FAULT`, offset wideband
   `WIDEBAND_OFFSET_CANDIDATE`) + emitter-discipline (no confirmed verdict) assertion.
4. `comlab/comlab/config/proposals/proposals.yaml` — proposal entry `EP-OBD-17` naming the consumer + ISO/SAE cite.
5. **Confirm** the pre-registered `T-COMV2-O2OFFSET-1` row in `comlab/tasks/PROGRESS.md` (Stage 4) — the fusion confirm/route (already registered this pack).

## Files to touch

- `obdlab/obdlab/schemas/vocabulary.py`
- `obdlab/obdlab/core/o2_normalizer.py`
- `obdlab/tests/unit/…` (new test module)
- `comlab/comlab/config/proposals/proposals.yaml` — proposal row only
- `comlab/tasks/PROGRESS.md` — forward-registration row only (no COMLab code this task)

## Out of scope

No confirmed `SENSOR_FAULT` / wideband-calibration verdict in OBDLab (Stage-4 COMLab). No gas import / no
`λ_chem` comparison in OBDLab. No change to existing O₂ modes. Do not fix the O₂-delta stress-band
inconsistency (O2-FU-3) — log it. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/ && pyright obdlab/
# emitter discipline — candidate only, no confirmed verdict, no gas
grep -rn "SENSOR_FAULT\|lambda_chem\|gas_\|FaultFamily" obdlab/obdlab/core/o2_normalizer.py \
  && { echo "FAIL: OBDLab confirms an offset verdict — it emits a candidate only"; exit 1; } || echo "OK candidate-only"
# proposal registered with a named consumer
grep -n "EP-OBD-17\|WIDEBAND_OFFSET_CANDIDATE\|T-COMV2-O2OFFSET-1" \
  ../comlab/comlab/config/proposals/proposals.yaml
pytest -x -q
```

All steps pass; candidate raised on the offset wideband branch, `NO_FAULT` otherwise, proposal registered.

## Anti-orphan note

`o2_failure_mode` is currently **carried in COMLab ingestion but read by no live COMLab path** (orphan; same as
`ve_*`). This proposal **ships its consumer** — `T-COMV2-O2OFFSET-1` reads `WIDEBAND_OFFSET_CANDIDATE` at
Stage 4 — so the new value is not an orphan: both halves land together per the v2 forward-progress rule. The
grep-confirm of the live read closes at the Stage-4 consumer task.

## Progress hook

`tasks/progress_notes/T-OBDV2-4.md` opens with the confirmed `## Plan` (name the new value, the `0.05`/persistent
guard, the proposal id + forward-registered consumer), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row
→ `done` with Files changed + "WIDEBAND_OFFSET_CANDIDATE emitted under WIDEBAND_LINEAR + persistent |λ−1|>0.05;
candidate-only (no verdict); proposal EP-OBD-17 + T-COMV2-O2OFFSET-1 forward-registered; Stage-2 green."
