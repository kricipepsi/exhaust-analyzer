# T-OBDV2-3 — downstream-trim-masking gap closed via existing `downstream_trim_role`

**Status:** `pending` — **coder-runnable** (research gate CLOSED) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab audit **Q7** (secondary-trim loop masking upstream O₂ drift) · **Registry:** DEP-3 (shares the O₂-role wiring)
**Blocked by:** — (T-OBDV2-0 = revive **done**; audit **Q7** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** **already live** — `comlab/comlab/core/perception_contradiction.py::detect` reads `downstream_trim_role`.

> **Task shape — read first.** This is an **anti-orphan / contract-close** task. The audit flagged a *missing
> signal channel* for "rear loop masking upstream drift." The research verdict is that **no new channel is
> needed** — the signal is the existing `downstream_trim_role` role field, and its consumer **already exists in
> a live COMLab path.** This task formally closes Q7 by grep-confirming the consumer and the source-of-truth of
> the field, and recording that the OBD boundary needs **no new emit**. **No OBDLab code change.**

## Why this exists

When the rear O₂ sensor drives a real secondary fuel-trim loop (`SECONDARY_FUEL_TRIM`), an *in-tolerance*
upstream λ agreement is only **weak** evidence of a healthy upstream sensor — the rear loop can mask upstream
drift. The audit asked whether OBDLab needed a new "masking" signal channel. It does not: the discriminator is
the **role classification**, which is sourced from DNALab/VINLab's emissions profile (mirrored on the COMLab
DNA boundary, populated by `T-FX-10`), not from any OBD PID.

## Research gate — CLOSED (Q7)

`AUDIT_ANSWERS_OBDLab.md` Q7:

- The masking signal is carried by `downstream_trim_role`, **not** a raw post-cat waveform.
- `SECONDARY_FUEL_TRIM` → post-cat trim analytics run, P2096/P2099 eligible, and an in-tolerance upstream
  agreement is **down-weighted** (the detector qualifies it as weak evidence).
- `CATALYST_MONITOR_ONLY` → COMLab **suppresses** post-cat trim verdicts entirely.
- "No new signal channel is needed — close the gap by routing it through the existing role field."
- Sources: `o2-logic/06_downstream-trim-suppression.md`, `o2-logic/02_upstream-vs-downstream-roles.md`,
  `o2-logic/05_bias-vs-real-truth-perception.md`.

## Scope (now PINNED)

Confirm and record, do **not** add:

> The `downstream_trim_role` consumer is **live** at `comlab/comlab/core/perception_contradiction.py::detect`:
> on `SECONDARY_FUEL_TRIM` an in-tolerance agreement appends `QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM` (down-weight),
> and a de-cat + `SECONDARY_FUEL_TRIM` config is flagged incoherent. The field is sourced DNA-side
> (`OrchestratorInboundRequest.downstream_trim_role`, populated by `T-FX-10`). **OBDLab emits nothing here** —
> the OBD boundary has no `downstream_trim_role` field and needs none.

## Success criteria

- **Anti-orphan grep confirms** `downstream_trim_role` is read in a live COMLab path (`perception_contradiction.py`),
  and that the down-weight (`QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM`) and suppression branches exist.
- **No new OBD channel:** grep-confirm `downstream_trim_role` is **absent** from `obdlab/obdlab/schemas/` (by design).
- Q7 recorded as closed-by-existing-consumer in `PROGRESS.md` (no proposal, no field).
- Inner loop clean (expected: no source change ⇒ suite unchanged-green).

## Deliverables

1. `obdlab/tasks/PROGRESS.md` — ledger row marking Q7 closed via the existing role consumer; note the
   `o2-logic/06` doc-bug follow-up (O2-FU-2: `SUPPRESS_POST_CAT_TRIM` is **not** a `TrimAnalyticsGate` value).
2. (optional) one-line cross-reference in the OBD↔COMLab boundary note that the masking signal is DNA-sourced,
   not an OBD channel.

## Files to touch

- `obdlab/tasks/PROGRESS.md` — ledger row + O2-FU-2 follow-up.
- **No `obdlab/obdlab/**` source change; no COMLab code change.**

## Out of scope

No new OBD field / no PID. No post-cat waveform analytics (the role field is the signal). Do **not** fix the
`o2-logic/06` doc-bug (O2-FU-2) or the O₂-delta stress-band inconsistency (O2-FU-3) here — log them. No gas import.

## Verification

```bash
cd <repo>/labs
# consumer is live
grep -n "downstream_trim_role\|QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM\|SECONDARY_FUEL_TRIM" \
  comlab/comlab/core/perception_contradiction.py
# OBD boundary carries no such field (by design)
grep -rn "downstream_trim_role" obdlab/obdlab/schemas/ \
  && { echo "FAIL: OBD added a role field — Q7 needs none"; exit 1; } || echo "OK no OBD channel"
cd obdlab && ruff check obdlab/ tests/ && pyright obdlab/ && pytest -x -q
```

All steps pass; the consumer is confirmed live and OBD adds nothing.

## Anti-orphan note

Unlike the Stage-2-emit / Stage-4-consume DEP rows, Q7's consumer is **already live today** — this task is a
pure verification close, not a forward-registration. The field is DNA-sourced and read by COMLab now.

## Progress hook

`tasks/progress_notes/T-OBDV2-3.md` opens with the confirmed `## Plan` (name the live consumer, "no OBD emit"),
then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with "Q7 closed via existing
`downstream_trim_role` consumer (perception_contradiction.detect); no OBD channel added; O2-FU-2 logged."
