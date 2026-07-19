# T-OBDV2-BANK-ASYM-1 — per-bank trim-delta emit for bank asymmetry

**Status:** `pending` — **coder-runnable** (research gate CLOSED) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** re-homed from GASLab `T-GV2-14` (**void**, 2026-06-05; `DECISIONS.md` Q-B) · **Registry:** DEP-3
**Blocked by:** — (T-OBDV2-0 = revive **done**; audit **Q2 + Q6** answered → `research/AUDIT_ANSWERS_OBDLab.md`)
**Consumer (signal/noise):** COMLab fusion verdict **`T-COMV2-BANK-FUSE-1`** (Stage 4) — forward-registered by this task.
**Run order:** after `T-OBDV2-ECU-PERCEPT-1` (sequencing advice; both are unblocked, ECU-PERCEPT is higher-value/first).

## Why this exists (the re-home — unchanged)

Bank asymmetry **cannot** come from gas: a single tailpipe sample is both banks mixed. The only channel that
sees banks separately is **per-bank STFT/LTFT (B1 vs B2)** — an OBD channel. OBD emits the per-bank trim
divergence; COMLab fuses it into a bank-asymmetry verdict last. OBD emits no asymmetry label.

## Research gate — CLOSED

`AUDIT_ANSWERS_OBDLab.md` (Q2, Q6):

- **Q2** — real per-family warm-idle trims pinned; bank-to-bank **match bound = within ±5 %** (common-mode); banks differing by **> ±5 %** = bank-specific. This is the asymmetry threshold (applied in the COMLab verdict, not by OBD).
- **Q6** — per-bank trims (`$08`/`$09`) are present on **2-bank OBD-II engines 1996+**; trust is **reduced pre-2001** (pre-CAN). ⇒ **no kill-switch**: the channel ships, gated to vehicles that actually have two banks; the fusion consumer carries the pre-2001 confidence caveat.

## Scope (now PINNED)

OBDLab emits one typed field on its output payload (frozen contract; COMLab mirrors locally):

> **`per_bank_trim_delta: float | None`** = `total_trim_correction_delta` (B1) **−**
> `total_trim_correction_delta_b2` (B2), signed. Emitted as a value **only when** both banks' trims are present
> (`total_trim_correction_delta_b2 is not None`, i.e. the bank-2 null contract indicates a 2-bank engine);
> **`None`** on single-bank engines. OBDLab emits the raw delta; it does **not** apply the ±5 % bound or emit
> an asymmetry verdict (that is the COMLab fusion step).

Applicability is gated by **bank-2 trim presence** (`shrtft2`/`longft2` → `total_trim_correction_delta_b2`),
not by a DNA field — `ObdLabDnaView` has **no `number_of_banks`** (post-PURGE); the bank-2 null contract is the
identity signal, consistent with the T-OBDV2-1a logset design.

## Success criteria

- New `per_bank_trim_delta: float | None` on `OBDLivePayload`, typed.
- **Applicability gate verified:** `None` on a single-bank fixture (no `shrtft2`/`longft2`); a signed float on a V-engine fixture with both banks.
- **Emitter discipline:** no asymmetry verdict / fault-family label emitted (grep-guard).
- Tests green at Stage 2 against the frozen contract.
- **Forward-registered** consumer row `T-COMV2-BANK-FUSE-1` in the COMLab ledger (Stage 4), naming `per_bank_trim_delta` + the ±5 % bound (Q2) + the pre-2001 confidence caveat (Q6) as its inputs.
- Inner loop clean.

## Deliverables

1. `obdlab/schemas/payload.py` — add `per_bank_trim_delta: float | None`.
2. `obdlab/core/trim_vector_aggregator.py` — compute the signed B1−B2 delta under the bank-2-presence gate; `None` when single-bank.
3. Tests: unit cases for the single-bank (`None`) and V-engine (float) branches + emitter-discipline assertion. Reuse `tests/pid_logset/` V-engine + single-bank fixtures.
4. Forward-register `T-COMV2-BANK-FUSE-1` in the COMLab ledger (Stage 4) with the ±5 % bound and pre-2001 caveat noted.

## Files to touch

- `obdlab/obdlab/schemas/payload.py`
- `obdlab/obdlab/core/trim_vector_aggregator.py`
- `obdlab/tests/unit/…` (new test module)
- `comlab` ledger — forward-registration row only

## Out of scope

No asymmetry **verdict** (COMLab applies the ±5 % bound). No `number_of_banks` DNA field (use bank-2 presence).
No gas import. No per-cylinder/Mode-06 misfire localisation. Off-scope finds → `PROGRESS.md` follow-ups.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ tests/
pyright obdlab/
# emitter discipline — no verdict (must return nothing)
grep -rn "bank_asym\|asymmetry_verdict\|fault_family\|FaultFamily" obdlab/obdlab/core/trim_vector_aggregator.py \
  && { echo "FAIL: OBDLab emits a verdict"; exit 1; } || echo "OK channel-only"
pytest -x -q
```

All steps pass; field is `None` single-bank, signed float on a 2-bank engine.

## Progress hook

`tasks/progress_notes/T-OBDV2-BANK-ASYM-1.md` opens with the confirmed `## Plan`, then `VERIFICATION GATE` +
`CODE REVIEW`. PROGRESS.md row → `done` with Files changed + "per_bank_trim_delta emitted under bank-2-presence
gate; emitter-only; T-COMV2-BANK-FUSE-1 forward-registered (±5 % bound, pre-2001 caveat); Stage-2 green".

> **Anti-orphan note:** read by `T-COMV2-BANK-FUSE-1` at Stage-4 close (DEP-3). Ships at Stage 2 under the
> frozen contract; Q6 confirms availability on 2-bank OBD-II — not a kill-switch.
